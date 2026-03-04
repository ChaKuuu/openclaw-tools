#!/usr/bin/env python3
"""
OpenClaw AI Tools API - 企业级安全加固版本
完整的安全解决方案
"""

import os
import re
import hashlib
import time
import json
import logging
import uuid
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict

from flask import Flask, request, jsonify, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

# ==================== 初始化 ====================

app = Flask(__name__)

# 强制配置密钥
if not os.environ.get('SECRET_KEY'):
    print("⚠️  警告: 未设置 SECRET_KEY，使用随机密钥（重启后失效）")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(32).hex())
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['JSON_AS_ASCII'] = False

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_security.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==================== 安全头 ====================

@app.after_request
def add_security_headers(response):
    """企业级安全响应头"""
    # 防止点击劫持
    response.headers['X-Frame-Options'] = 'DENY'
    # 防止 MIME 类型嗅探
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # XSS 防护
    response.headers['X-XSS-Protection'] = '1; mode=block'
    # 跨域策略
    response.headers['Access-Control-Allow-Origin'] = os.environ.get('ALLOWED_ORIGIN', '')
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-API-Key, X-Request-ID'
    # HSTS
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    # 禁用缓存
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    # 内容安全策略
    response.headers['Content-Security-Policy'] = "default-src 'none'; frame-ancestors 'none'"
    # 移除服务器信息
    response.headers['Server'] = 'Secure'
    return response

# CORS
CORS(app, origins=[os.environ.get('ALLOWED_ORIGIN', '')] if os.environ.get('ALLOWED_ORIGIN') else [])

# ==================== 请求追踪 ====================

@app.before_request
def before_request():
    """生成请求追踪 ID"""
    g.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    g.start_time = time.time()
    
    # 记录请求
    logger.info(f"[{g.request_id}] {request.method} {request.path} from {request.remote_addr}")

@app.after_request
def after_request(response):
    """记录响应时间"""
    if hasattr(g, 'start_time'):
        duration = time.time() - g.start_time
        logger.info(f"[{g.request_id}] {response.status_code} in {duration:.3f}s")
    
    # 添加请求 ID 到响应头
    response.headers['X-Request-ID'] = g.request_id
    return response

# ==================== 速率限制高级版 ====================

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour", "10 per minute"],
    storage_uri="memory://"
)

# IP 黑名单
IP_BLACKLIST = set(os.environ.get('IP_BLACKLIST', '').split(','))

# 连续失败计数
failed_attempts = defaultdict(list)
BLOCKED_IPS = {}

def check_ip_blacklist():
    """检查 IP 黑名单"""
    if request.remote_addr in IP_BLACKLIST:
        logger.warning(f"黑名单 IP 访问: {request.remote_addr}")
        return jsonify({"error": "访问被拒绝", "code": "BLOCKED_IP"}), 403
    
    # 检查临时封禁
    if request.remote_addr in BLOCKED_IPS:
        if time.time() < BLOCKED_IPS[request.remote_addr]:
            logger.warning(f"临时封禁 IP 访问: {request.remote_addr}")
            return jsonify({"error": "IP 被临时封禁", "code": "IP_BLOCKED"}), 403
        else:
            del BLOCKED_IPS[request.remote_addr]
    
    return None

def record_failed_attempt():
    """记录失败尝试，连续 5 次失败封禁 1 小时"""
    failed_attempts[request.remote_addr].append(time.time())
    
    # 清理 old attempts
    cutoff = time.time() - 3600
    failed_attempts[request.remote_addr] = [
        t for t in failed_attempts[request.remote_addr] if t > cutoff
    ]
    
    if len(failed_attempts[request.remote_addr]) >= 5:
        BLOCKED_IPS[request.remote_addr] = time.time() + 3600
        logger.warning(f"IP 被封禁 1 小时: {request.remote_addr}")
        failed_attempts[request.remote_addr] = []

# ==================== 认证系统 ====================

class AuthManager:
    """认证管理器"""
    
    def __init__(self):
        self.keys = {}
        self.load_keys()
    
    def load_keys(self):
        """从环境变量加载密钥"""
        key_data = os.environ.get('API_KEYS', '')
        if key_data:
            for item in key_data.split(','):
                if ':' in item:
                    key, name = item.split(':', 1)
                    self.keys[key] = {'name': name, 'daily': 0, 'reset_date': datetime.now().date()}
        
        # 默认密钥
        default_key = os.environ.get('API_KEY', 'demo_key_12345')
        if default_key not in self.keys:
            self.keys[default_key] = {'name': 'default', 'daily': 0, 'reset_date': datetime.now().date()}
    
    def validate(self, api_key):
        """验证 API 密钥"""
        if api_key not in self.keys:
            return False, "无效的 API 密钥"
        
        key_info = self.keys[api_key]
        
        # 重置每日计数
        if key_info['reset_date'] != datetime.now().date():
            key_info['daily'] = 0
            key_info['reset_date'] = datetime.now().date()
        
        # 检查每日限额
        if key_info['daily'] >= 1000:
            return False, "今日配额已用完"
        
        key_info['daily'] += 1
        return True, key_info
    
    def add_key(self, name):
        """添加新密钥"""
        key = hashlib.sha256(f"{name}{time.time()}{os.urandom(16)}".encode()).hexdigest()[:32]
        self.keys[key] = {'name': name, 'daily': 0, 'reset_date': datetime.now().date()}
        return key

auth_manager = AuthManager()

def require_auth(f):
    """认证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # 检查 IP 黑名单
        check = check_ip_blacklist()
        if check:
            return check
        
        # 获取 API 密钥
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key:
            record_failed_attempt()
            logger.warning(f"[{g.request_id}] 缺少 API 密钥 from {request.remote_addr}")
            return jsonify({"error": "缺少 API 密钥", "code": "NO_KEY"}), 401
        
        valid, info = auth_manager.validate(api_key)
        if not valid:
            record_failed_attempt()
            logger.warning(f"[{g.request_id}] 认证失败: {info} from {request.remote_addr}")
            return jsonify({"error": info, "code": "INVALID_KEY"}), 401
        
        g.key_name = info['name']
        logger.info(f"[{g.request_id}] 认证成功: {info['name']}")
        
        return f(*args, **kwargs)
    return decorated

# ==================== 输入验证器 ====================

class InputValidator:
    """企业级输入验证器"""
    
    @staticmethod
    def validate(pattern, text, field_name):
        """通用验证"""
        if not text:
            raise ValueError(f"{field_name} 不能为空")
        if not isinstance(text, str):
            raise ValueError(f"{field_name} 必须是字符串")
        if len(text) > 10000:
            raise ValueError(f"{field_name} 过长")
        if not re.match(pattern, text):
            raise ValueError(f"{field_name} 格式错误")
        return text
    
    @staticmethod
    def stock_code(code):
        return InputValidator.validate(r'^\d{6}$', code, "股票代码")
    
    @staticmethod
    def city(city):
        return InputValidator.validate(r'^[\u4e00-\u9fa5a-zA-Z]{1,20}$', city, "城市")
    
    @staticmethod
    def content(content):
        return InputValidator.validate(r'^.{1,10000}$', content, "内容")
    
    @staticmethod
    def scan_threats(text):
        """威胁扫描"""
        if not text:
            return True
        
        threats = [
            ('SQL 注入', ['select ', 'insert ', 'update ', 'delete ', 'drop ', 'union ', '--', ';--']),
            ('XSS', ['<script', '</script', 'javascript:', 'onerror=', 'onload=', '<iframe']),
            ('命令注入', ['|', '&', ';', '`', '$(', '${']),
            ('路径遍历', ['../', '..\\', '/etc/', 'C:\\']),
            ('模板注入', ['{{', '}}', '{%', '%}']),
        ]
        
        text_lower = text.lower()
        for threat_type, patterns in threats:
            for pattern in patterns:
                if pattern.lower() in text_lower:
                    logger.warning(f"[{g.request_id}] 检测到{threat_type}: {pattern}")
                    return False
        return True

validator = InputValidator()

# ==================== 错误处理 ====================

class APIError(Exception):
    def __init__(self, message, code="ERROR", status_code=400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)

@app.errorhandler(APIError)
def handle_api_error(error):
    logger.error(f"[{g.request_id}] API 错误: {error.code} - {error.message}")
    response = jsonify({
        "error": error.message,
        "code": error.code,
        "request_id": g.request_id
    })
    response.status_code = error.status_code
    return response

@app.errorhandler(429)
def ratelimit_handler(e):
    logger.warning(f"[{g.request_id}] 速率限制: {request.remote_addr}")
    return jsonify({
        "error": "请求过于频繁",
        "code": "RATE_LIMITED",
        "request_id": g.request_id
    }), 429

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "接口不存在", "code": "NOT_FOUND", "request_id": g.request_id}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"[{g.request_id}] 服务器错误")
    return jsonify({
        "error": "服务器错误",
        "code": "SERVER_ERROR",
        "request_id": g.request_id
    }), 500

# ==================== 路由 ====================

@app.route('/')
def index():
    """API 信息"""
    return jsonify({
        "name": "OpenClaw AI Tools API",
        "version": "4.0.0",
        "security": "Enterprise Grade",
        "features": [
            "API Key 认证",
            "请求追踪",
            "威胁扫描",
            "IP 封禁",
            "速率限制",
            "完整日志"
        ],
        "endpoints": {
            "/": "API 信息",
            "/health": "健康检查",
            "/stats": "使用统计",
            "/stock/analyze": "股票分析",
            "/weather": "天气查询",
            "/news": "新闻分析"
        }
    })

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": time.time(),
        "version": "4.0.0"
    })

@app.route('/stats')
@require_auth
def stats():
    """使用统计"""
    return jsonify({
        "your_daily_usage": auth_manager.keys.get(
            request.headers.get('X-API-Key'), {}
        ).get('daily', 0),
        "total_keys": len(auth_manager.keys),
        "blocked_ips": len(BLOCKED_IPS),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/stock/analyze', methods=['POST'])
@limiter.limit("10 per minute")
@require_auth
def stock_analyze():
    """股票分析"""
    try:
        data = request.get_json()
        if not data:
            raise APIError("请求体不能为空", "EMPTY_BODY")
        
        code = str(data.get('code', ''))
        validator.stock_code(code)
        
        if not validator.scan_threats(code):
            raise APIError("检测到安全威胁", "THREAT_DETECTED")
        
        return jsonify({
            "code": code,
            "timestamp": datetime.now().isoformat(),
            "prediction": "涨",
            "confidence": 0.65,
            "signal": "买入"
        })
    except ValueError as e:
        raise APIError(str(e), "VALIDATION_ERROR")

@app.route('/weather')
@limiter.limit("20 per minute")
@require_auth
def weather():
    """天气查询"""
    try:
        city = request.args.get('city', '北京')
        validator.city(city)
        
        if not validator.scan_threats(city):
            raise APIError("检测到安全威胁", "THREAT_DETECTED")
        
        return jsonify({
            "city": city,
            "timestamp": datetime.now().isoformat(),
            "temperature": 22,
            "weather": "晴"
        })
    except ValueError as e:
        raise APIError(str(e), "VALIDATION_ERROR")

@app.route('/news', methods=['POST'])
@limiter.limit("10 per minute")
@require_auth
def news_analyze():
    """新闻分析"""
    try:
        data = request.get_json()
        if not data:
            raise APIError("请求体不能为空", "EMPTY_BODY")
        
        content = str(data.get('content', ''))
        validator.content(content)
        
        if not validator.scan_threats(content):
            raise APIError("检测到安全威胁", "THREAT_DETECTED")
        
        # 情感分析
        pos = sum(1 for w in ['好', '增长', '涨', '盈利'] if w in content)
        neg = sum(1 for w in ['跌', '亏损', '降', '风险'] if w in content)
        
        sentiment = "positive" if pos > neg else ("negative" if neg > pos else "neutral")
        
        return jsonify({
            "timestamp": datetime.now().isoformat(),
            "sentiment": sentiment,
            "summary": content[:200]
        })
    except ValueError as e:
        raise APIError(str(e), "VALIDATION_ERROR")

# ==================== 启动 ====================

if __name__ == '__main__':
    print("=" * 60)
    print("🔒 OpenClaw AI Tools API - 企业级安全版 v4.0")
    print("=" * 60)
    print("✅ 企业级安全特性:")
    print("  - 请求追踪 (X-Request-ID)")
    print("  - 企业级输入验证")
    print("  - 威胁扫描 (SQL注入/XSS/命令注入)")
    print("  - IP 黑名单 + 临时封禁")
    print("  - 智能速率限制")
    print("  - 完整审计日志")
    print("  - 每日使用统计")
    print("=" * 60)
    print("⚠️  生产环境配置:")
    print("  export SECRET_KEY='your-256-bit-key'")
    print("  export API_KEY='your-api-key'")
    print("  export ALLOWED_ORIGIN='https://yourdomain.com'")
    print("  gunicorn -w 4 -b 0.0.0.0:5000 api_server:app")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
