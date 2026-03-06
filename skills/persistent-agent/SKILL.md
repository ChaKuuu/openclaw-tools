---
name: persistent-agent
description: 后台常驻守护进程。开机自动启动，崩溃自动重启，24小时持续运行。执行主线任务、安全监控、自动学习。
---

# Persistent Agent Skill

## 功能
- 后台常驻守护进程
- 开机自动启动
- 崩溃自动重启
- 24小时持续运行
- 自动执行主线任务

## 使用

### 启动守护进程
```bash
python auto_loop.py
```

### 守护进程功能
1. 每小时安全检查
2. 自动学习新技能
3. 搜索工作机会
4. 推广产品
5. 记忆系统更新

## 配置

### 自动启动 (Windows)
将 `auto_loop.py` 添加到启动项：
```powershell
# 以管理员运行
New-Item -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "Jarvis" -Value "python C:\path\to\auto_loop.py"
```

### 崩溃重启
守护进程自动捕获异常并重启，确保 24h 运行。

## 核心原则
1. 高执行力
2. 不冗余、不啰嗦
3. 主动提醒
4. 主动总结
5. 主动优化任务
