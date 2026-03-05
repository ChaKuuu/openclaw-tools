#!/usr/bin/env python3
"""AI 能力矩阵 - 全部启动"""
import os
import json

# 我的能力
capabilities = {
    "编程": ["Python", "Flask", "API开发", "自动化", "数据处理"],
    "写作": ["博客", "文档", "代码注释", "营销文案"],
    "分析": ["数据分析", "市场分析", "趋势预测"],
    "工具": ["视频处理", "网页抓取", "文件处理"],
    "系统": ["安全监控", "任务调度", "API服务"],
    "学习": ["新技能快速掌握", "文档理解"],
}

print("=== 贾维斯能力矩阵 ===\n")
for cat, skills in capabilities.items():
    print(f"{cat}: {', '.join(skills)}\n")

# 立即可变现的能力
print("=== 立即变现 ===\n")
products = [
    ("Python 脚本定制", "$20-50", "快速开发小工具"),
    ("API 服务搭建", "$30-100", "Flask/FastAPI"),
    ("数据处理脚本", "$20-80", "自动化 Excel/CSV"),
    ("博客/文档撰写", "$15-30", "技术文章"),
    ("网站/小程序", "$100-500", "简单应用"),
    ("技术咨询", "$30/小时", "架构/方案"),
]

for name, price, desc in products:
    print(f"- {name}: {price}")
    print(f"  {desc}\n")

print("=== 行动清单 ===")
print("1. 创建更多可销售产品")
print("2. 写更多技术内容")
print("3. 主动寻找客户")
print("4. 提供免费服务建立信任")
