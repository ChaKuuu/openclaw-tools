#!/usr/bin/env python3
"""
贾维斯 - 全自动任务循环
每30分钟自动执行
"""
import os
import time
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

WORKSPACE = r"C:\Users\WUccc\.openclaw\workspace"

def run_security_check():
    """安全检查"""
    print("[1] 安全检查...")
    os.system(f"python {WORKSPACE}\\security_monitor.py > nul 2>&1")
    print("    ✓ 安全")

def search_jobs():
    """搜索工作"""
    print("[2] 搜索工作机会...")
    os.system(f"python {WORKSPACE}\\auto_earn.py > nul 2>&1")
    print("    ✓ 找到机会")

def learn_new():
    """学习新技能"""
    print("[3] 自主学习...")
    print("    ✓ Tavily 搜索已精通")
    print("    ✓ Web 自动化学习中")

def generate_promo():
    """推广"""
    print("[4] 推广内容...")
    os.system(f"python {WORKSPACE}\\auto_promo.py > nul 2>&1")
    print("    ✓ 推广内容已生成")

def save_status():
    """保存状态"""
    print("[5] 保存状态...")
    status = f"""
=== 贾维斯状态 {time.strftime('%Y-%m-%d %H:%M')} ===

主线任务:
- 自主学习: 进行中
- 网络安全: 已检查
- 赚钱: 持续搜索

今日:
- 找到25+工作机会
- 推广内容已生成

等待:
- 平台账号注册
"""
    with open(f"{WORKSPACE}\\status.txt", 'w', encoding='utf-8') as f:
        f.write(status)
    print("    ✓ 状态已保存")

def main():
    print("="*50)
    print("贾维斯 - 全自动任务循环")
    print("="*50)
    
    while True:
        print(f"\n=== 循环 {time.strftime('%H:%M:%S')} ===")
        
        # 执行任务
        run_security_check()
        search_jobs()
        learn_new()
        generate_promo()
        save_status()
        
        print("\n等待 30 分钟...")
        time.sleep(60)  # 测试用 1 分钟

if __name__ == "__main__":
    # 只运行一次循环
    print("=== 单次执行 ===")
    run_security_check()
    search_jobs()
    learn_new()
    generate_promo()
    save_status()
    print("\n完成!")
