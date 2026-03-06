#!/usr/bin/env python3
"""
贾维斯核心 - 永久记忆与学习系统 v2.0
功能：
1. 永久长期记忆 - 永不丢失
2. 用户偏好学习
3. 自动知识库构建
4. 主动预判操作
"""
import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path

WORKSPACE = r"C:\Users\WUccc\.openclaw\workspace"
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
DB_PATH = os.path.join(WORKSPACE, "jarvis_memory.db")

class JarvisMemory:
    """永久记忆系统"""
    
    def __init__(self):
        self.db_path = DB_PATH
        self.init_database()
        
    def init_database(self):
        """初始化SQLite数据库"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # 对话历史表
        c.execute('''CREATE TABLE IF NOT EXISTS conversations
                     (id INTEGER PRIMARY KEY, timestamp TEXT, 
                      user_msg TEXT, ai_msg TEXT, channel TEXT)''')
        
        # 用户偏好表
        c.execute('''CREATE TABLE IF NOT EXISTS preferences
                     (key TEXT PRIMARY KEY, value TEXT, updated TEXT)''')
        
        # 习惯表
        c.execute('''CREATE TABLE IF NOT EXISTS habits
                     (id INTEGER PRIMARY KEY, action TEXT, 
                      count INTEGER, last_time TEXT)''')
        
        # 知识库表
        c.execute('''CREATE TABLE IF NOT EXISTS knowledge
                     (id INTEGER PRIMARY KEY, topic TEXT, 
                      content TEXT, tags TEXT, created TEXT)''')
        
        # 禁忌表
        c.execute("""CREATE TABLE IF NOT EXISTS taboo
                     (topic TEXT PRIMARY KEY, reason TEXT)""")
        
        conn.commit()
        conn.close()
        print(f"[OK] Memory DB: {self.db_path}")
    
    def save_conversation(self, user_msg, ai_msg, channel="webchat"):
        """保存对话"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO conversations (timestamp, user_msg, ai_msg, channel) VALUES (?, ?, ?, ?)",
                  (datetime.now().isoformat(), user_msg, ai_msg, channel))
        conn.commit()
        conn.close()
    
    def set_preference(self, key, value):
        """设置用户偏好"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO preferences (key, value, updated) VALUES (?, ?, ?)",
                  (key, value, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_preference(self, key, default=None):
        """获取用户偏好"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT value FROM preferences WHERE key=?", (key,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else default
    
    def record_habit(self, action):
        """记录习惯"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT count FROM habits WHERE action=?", (action,))
        row = c.fetchone()
        if row:
            c.execute("UPDATE habits SET count=?, last_time=? WHERE action=?",
                      (row[0]+1, datetime.now().isoformat(), action))
        else:
            c.execute("INSERT INTO habits (action, count, last_time) VALUES (?, 1, ?)",
                      (action, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def add_knowledge(self, topic, content, tags=""):
        """添加知识"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO knowledge (topic, content, tags, created) VALUES (?, ?, ?, ?)",
                  (topic, content, tags, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_knowledge(self, topic):
        """获取知识"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT content FROM knowledge WHERE topic=?", (topic,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None
    
    def daily_summary(self):
        """每日总结"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # 统计今天对话数
        today = datetime.now().date().isoformat()
        c.execute("SELECT COUNT(*) FROM conversations WHERE timestamp LIKE ?", (f"{today}%",))
        conv_count = c.fetchone()[0]
        
        # 获取最常见的动作
        c.execute("SELECT action, count FROM habits ORDER BY count DESC LIMIT 5")
        habits = c.fetchall()
        
        conn.close()
        
        return {
            "date": today,
            "conversations": conv_count,
            "top_habits": habits
        }
    
    def learn_user_style(self, message):
        """学习用户说话风格"""
        words = message.lower().split()
        for word in words:
            self.record_habit(f"word:{word}")
        
        # 记录消息长度
        self.record_habit(f"msg_len:{len(message)}")
        
        # 记录时间
        hour = datetime.now().hour
        self.record_habit(f"hour:{hour}")

class Jarvis:
    """贾维斯核心"""
    
    def __init__(self):
        self.memory = JarvisMemory()
        self.name = "Jarvis"
        self.version = "2.0"
        self.running = True
        
    def greet(self):
        """主动问候"""
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good Morning"
        elif hour < 18:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"
        
        return f"{greeting}! Jarvis ready..."
    
    def run_command(self, cmd):
        """执行命令"""
        self.memory.record_habit(f"cmd:{cmd}")
        
        if cmd == "status":
            return self.status()
        elif cmd == "summary":
            return self.daily_summary()
        elif cmd == "memory":
            return f"记忆库: {self.db_path}"
        else:
            return f"未知命令: {cmd}"
    
    def status(self):
        """状态"""
        return f"贾维斯 v{self.version} | 记忆: 永久 | 运行: True"
    
    def daily_summary(self):
        """每日总结"""
        return self.memory.daily_summary()

# 全局实例
jarvis = Jarvis()

if __name__ == "__main__":
    print("=== 贾维斯核心 v2.0 ===")
    print(jarvis.greet())
    print(jarvis.status())
    
    # 测试记忆
    jarvis.memory.set_preference("name", "WUccc")
    jarvis.memory.set_preference("goal", "$50/day")
    jarvis.memory.add_knowledge("github", "ChaKuuu/openclaw-tools", "python,tools")
    
    print("\n偏好:", jarvis.memory.get_preference("name"))
    print("目标:", jarvis.memory.get_preference("goal"))
    print("知识:", jarvis.memory.get_knowledge("github"))
    print("\n[OK] Jarvis core initialized")
