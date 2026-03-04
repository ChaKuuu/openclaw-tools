#!/usr/bin/env python3
"""
贾维斯助手 - 你的AI私人助理
功能：语音对话、日程管理、数据分析、浏览器控制、文件管理
"""

import os
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# ==================== 核心功能 ====================

class JarvisAssistant:
    def __init__(self):
        self.workspace = Path(r"C:\Users\WUccc\.openclaw\workspace")
        self.projects_dir = self.workspace / "projects"
        self.projects_dir.mkdir(exist_ok=True)
        
        # 记忆存储
        self.memory_file = self.workspace / "memory" / "jarvis_memory.json"
        self.memory = self.load_memory()
    
    def load_memory(self):
        """加载记忆"""
        if self.memory_file.exists():
            with open(self.memory_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "user_preferences": {},
            "projects": {},
            "tasks": [],
            "notes": []
        }
    
    def save_memory(self):
        """保存记忆"""
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)
    
    # ==================== 日程管理 ====================
    
    def add_task(self, task_name, due_date=None, priority="normal"):
        """添加任务"""
        task = {
            "id": len(self.memory["tasks"]) + 1,
            "name": task_name,
            "due_date": due_date,
            "priority": priority,
            "status": "pending",
            "created": datetime.now().isoformat()
        }
        self.memory["tasks"].append(task)
        self.save_memory()
        return f"✅ 已添加任务: {task_name}"
    
    def list_tasks(self, status=None):
        """列出任务"""
        tasks = self.memory["tasks"]
        if status:
            tasks = [t for t in tasks if t["status"] == status]
        
        if not tasks:
            return "📋 暂无任务"
        
        result = "📋 任务列表:\n"
        for t in tasks:
            status_icon = "✅" if t["status"] == "done" else "⏳"
            result += f"{status_icon} {t['id']}. {t['name']}"
            if t.get("due_date"):
                result += f" (截止: {t['due_date']})"
            result += "\n"
        return result
    
    def complete_task(self, task_id):
        """完成任务"""
        for t in self.memory["tasks"]:
            if t["id"] == task_id:
                t["status"] = "done"
                t["completed"] = datetime.now().isoformat()
                self.save_memory()
                return f"✅ 任务已完成: {t['name']}"
        return "❌ 任务未找到"
    
    # ==================== 项目管理 ====================
    
    def create_project(self, project_name, description=""):
        """创建项目"""
        project_path = self.projects_dir / project_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        # 创建项目结构
        (project_path / "notes").mkdir(exist_ok=True)
        (project_path / "assets").mkdir(exist_ok=True)
        (project_path / "output").mkdir(exist_ok=True)
        
        # 保存项目信息
        self.memory["projects"][project_name] = {
            "path": str(project_path),
            "description": description,
            "created": datetime.now().isoformat()
        }
        self.save_memory()
        
        return f"✅ 项目已创建: {project_name}\n📁 位置: {project_path}"
    
    def list_projects(self):
        """列出项目"""
        if not self.memory["projects"]:
            return "📁 暂无项目"
        
        result = "📁 项目列表:\n"
        for name, info in self.memory["projects"].items():
            result += f"• {name}: {info.get('description', '')}\n"
        return result
    
    # ==================== 笔记功能 ====================
    
    def add_note(self, title, content):
        """添加笔记"""
        note = {
            "id": len(self.memory["notes"]) + 1,
            "title": title,
            "content": content,
            "created": datetime.now().isoformat()
        }
        self.memory["notes"].append(note)
        self.save_memory()
        return f"✅ 笔记已保存: {title}"
    
    def search_notes(self, keyword):
        """搜索笔记"""
        results = []
        for note in self.memory["notes"]:
            if keyword in note["title"] or keyword in note["content"]:
                results.append(note)
        
        if not results:
            return f"🔍 未找到包含 '{keyword}' 的笔记"
        
        result = f"🔍 找到 {len(results)} 条笔记:\n"
        for n in results:
            result += f"• {n['title']}\n"
        return result
    
    # ==================== 用户偏好 ====================
    
    def set_preference(self, key, value):
        """设置用户偏好"""
        self.memory["user_preferences"][key] = value
        self.save_memory()
        return f"✅ 已设置: {key} = {value}"
    
    def get_preference(self, key, default=None):
        """获取用户偏好"""
        return self.memory["user_preferences"].get(key, default)
    
    # ==================== 文件操作 ====================
    
    def list_files(self, directory=None):
        """列出文件"""
        directory = Path(directory) if directory else self.workspace
        if not directory.exists():
            return f"❌ 目录不存在: {directory}"
        
        files = list(directory.iterdir())
        if not files:
            return "📂 目录为空"
        
        result = f"📂 {directory}:\n"
        for f in files[:20]:  # 限制显示数量
            icon = "📁" if f.is_dir() else "📄"
            result += f"{icon} {f.name}\n"
        return result
    
    # ==================== 快速命令 ====================
    
    def help(self):
        """帮助信息"""
        return """
🤖 贾维斯助手 - 可用命令:

📋 任务管理:
  jarvis add task <任务名> [截止日期]
  jarvis list tasks
  jarvis complete <任务ID>

📁 项目管理:
  jarvis create project <项目名>
  jarvis list projects

📝 笔记:
  jarvis add note <标题> <内容>
  jarvis search <关键词>

⚙️ 偏好设置:
  jarvis set <键> <值>
  jarvis get <键>

📂 文件:
  jarvis list [目录]

🎬 视频处理:
  python video_tools.py <命令> [参数]

🔍 搜索:
  web_search <关键词>

📊 数据分析:
  使用 pandas/plotly 进行分析
"""


# ==================== 主程序 ====================

if __name__ == "__main__":
    import sys
    
    jarvis = JarvisAssistant()
    
    if len(sys.argv) < 2:
        print(jarvis.help())
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    args = sys.argv[2:]
    
    if cmd == "help":
        print(jarvis.help())
    
    elif cmd == "add" and len(args) >= 2:
        if args[0] == "task":
            print(jarvis.add_task(" ".join(args[1:])))
        elif args[0] == "note":
            print(jarvis.add_note(args[1], " ".join(args[2:])))
    
    elif cmd == "list" and len(args) >= 1:
        if args[0] == "tasks":
            print(jarvis.list_tasks())
        elif args[0] == "projects":
            print(jarvis.list_projects())
        else:
            print(jarvis.list_files(args[0] if args else None))
    
    elif cmd == "complete" and len(args) >= 1:
        print(jarvis.complete_task(int(args[0])))
    
    elif cmd == "create" and len(args) >= 2:
        if args[0] == "project":
            print(jarvis.create_project(args[1], " ".join(args[2:]) if len(args) > 2 else ""))
    
    elif cmd == "search" and len(args) >= 1:
        print(jarvis.search_notes(args[0]))
    
    elif cmd == "set" and len(args) >= 2:
        print(jarvis.set_preference(args[0], " ".join(args[1:])))
    
    elif cmd == "get" and len(args) >= 1:
        print(jarvis.get_preference(args[0], "未设置"))
    
    else:
        print(jarvis.help())
