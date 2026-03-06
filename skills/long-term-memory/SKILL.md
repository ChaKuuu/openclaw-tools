---
name: long-term-memory
description: 永久记忆系统。完整记录所有历史、偏好、习惯需求、性格、常用指令，永不丢失，自动增量学习。
---

# Long Term Memory Skill

## 功能
- SQLite 本地持久化数据库
- 对话历史完整记录
- 用户偏好学习
- 习惯与行为模式分析
- 知识库自动构建
- 永不丢失、禁止重置

## 文件
- `jarvis_permanent.py` - 核心记忆系统
- `jarvis_memory.db` - 记忆数据库

## 使用

### 初始化
```bash
python jarvis_permanent.py
```

### 保存偏好
```python
jarvis.memory.set_preference("key", "value")
```

### 获取偏好
```python
jarvis.memory.get_preference("key", default="default")
```

### 记录习惯
```python
jarvis.memory.record_habit("action_name")
```

### 添加知识
```python
jarvis.memory.add_knowledge("topic", "content", "tags")
```

### 获取知识
```python
jarvis.memory.get_knowledge("topic")
```

### 每日总结
```python
jarvis.memory.daily_summary()
```

## 核心原则
1. 禁止清除记忆
2. 禁止重置配置
3. 所有历史永久保存
4. 自动增量学习
5. 贴合用户风格
