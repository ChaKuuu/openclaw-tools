---
name: voice-wakeup
description: 语音唤醒与持续监听。检测唤醒词"龙虾""OpenClaw""贾维斯"，支持随时打断、随时响应。需要麦克风设备。
---

# Voice Wakeup Skill

## 功能
- 持续监听麦克风
- 检测唤醒词: 龙虾、OpenClaw、贾维斯
- 唤醒后响应用户命令
- 支持随时打断

## 使用方式

### 安装依赖
```bash
pip install pvporcupine numpy pyaudio
```

### 启动唤醒监听
```bash
python skills/voice-wakeup/scripts/wakeup.py
```

### 唤醒词
- **中文**: 贾维斯、龙虾
- **英文**: OpenClaw、Jarvis

### 配置自定义唤醒词
编辑 `scripts/wakeup.py` 中的 `KEYWORDS` 列表。

## 注意
需要麦克风设备。首次使用需下载 Porcupine 唤醒词模型。
