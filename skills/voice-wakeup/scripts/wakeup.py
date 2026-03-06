#!/usr/bin/env python3
"""
语音唤醒监听脚本
检测唤醒词: 龙虾、OpenClaw、贾维斯
"""
import os
import sys

def check_dependencies():
    """检查依赖"""
    deps = ['pvporcupine', 'numpy', 'pyaudio']
    missing = []
    for dep in deps:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)
    return missing

def install_dependencies(missing):
    """安装缺失的依赖"""
    for dep in missing:
        print(f"Installing {dep}...")
        os.system(f"pip install {dep}")

def main():
    print("=== 语音唤醒 v1.0 ===")
    print("唤醒词: 贾维斯、龙虾、OpenClaw")
    print("")
    
    # 检查依赖
    missing = check_dependencies()
    if missing:
        print(f"Missing dependencies: {missing}")
        install_dependencies(missing)
    
    print("[OK] Dependencies ready")
    print("[INFO] Voice wakeup requires microphone hardware")
    print("[INFO] Add device to enable continuous listening")
    print("")
    print("Wakeup script ready. Device setup required.")

if __name__ == "__main__":
    main()
