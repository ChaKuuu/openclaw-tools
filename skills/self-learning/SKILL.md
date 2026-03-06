---
name: self-learning
description: 用户专属知识库构建。每天自动总结对话，提取偏好、禁忌、常用操作、目标、计划，形成专属个人模型。
---

# Self Learning Skill

## 功能
- 每日自动总结对话
- 提取用户偏好
- 识别用户禁忌
- 记录常用操作
- 追踪目标与计划
- 构建专属个人模型

## 文件
- `jarvis_permanent.py` - 包含学习逻辑
- `memory/` - 每日对话记录
- `jarvis_memory.db` - 结构化记忆

## 学习机制

### 用户风格学习
```python
jarvis.memory.learn_user_style(message)
```
- 分析用词习惯
- 学习消息长度偏好
- 记录活跃时间段

### 偏好提取
自动从对话中提取:
- 喜欢的内容类型
- 偏好的沟通方式
- 常用指令模式
- 目标与计划

### 禁忌识别
记录用户明确拒绝的内容:
```python
jarvis.memory.add_knowledge("禁忌:topic", "reason")
```

## 优化响应
- 越来越贴合用户说话风格
- 越来越懂用户需求
- 主动预判下一步操作

## 每日总结
```python
jarvis.memory.daily_summary()
```
返回:
- 今日对话数
- 最常见的动作
- 用户活跃时间段
