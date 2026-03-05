#!/usr/bin/env python3
"""安全监控系统 - 定时检查"""
import os
import json
import time
from datetime import datetime

LOG_FILE = "security_log.json"

def check_chrome_extensions():
    """检查Chrome扩展"""
    ext_path = r"C:\Users\WUccc\.openclaw\workspace\chrome-extension"
    suspicious = []
    try:
        files = os.listdir(ext_path)
        # 检查危险权限
        manifest = os.path.join(ext_path, "manifest.json")
        if os.path.exists(manifest):
            with open(manifest, 'r') as f:
                content = f.read()
                # 危险权限关键词
                dangerous = ["http://*", "https://*", "cookies", "webRequest", "debugger"]
                for d in dangerous:
                    if d in content:
                        suspicious.append(f"危险权限: {d}")
        return {"status": "OK", "extensions": files, "suspicious": suspicious}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}

def check_network_connections():
    """检查网络连接"""
    import socket
    sites = {
        "GitHub": "github.com",
        "Gumroad": "gumroad.com", 
        "PyPI": "pypi.org",
        "Google": "google.com"
    }
    results = {}
    for name, host in sites.items():
        try:
            socket.create_connection((host, 80), timeout=3)
            results[name] = "OK"
        except:
            results[name] = "FAIL"
    return results

def log_check():
    """记录检查结果"""
    result = {
        "time": datetime.now().isoformat(),
        "chrome": check_chrome_extensions(),
        "network": check_network_connections()
    }
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    log_check()
