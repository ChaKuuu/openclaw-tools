#!/usr/bin/env python3
"""Stack Overflow 自动回答系统"""
import requests

def get_python_questions():
    """获取最新 Python 问题"""
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "order": "desc",
        "sort": "activity",
        "tagged": "python",
        "site": "stackoverflow",
        "pagesize": 20
    }
    r = requests.get(url, params=params, timeout=10)
    return r.json().get('items', [])

def generate_answer_template(title):
    """生成回答模板"""
    title_lower = title.lower()
    
    templates = {
        'error': "Based on the error message, I'd recommend checking the traceback. The issue is likely in the line where the error occurs. Can you share your full code?",
        'how to': "Great question! Here's a step-by-step approach: 1) First, understand the requirements 2) Start with a simple implementation 3) Test incrementally",
        'difference': "The main difference is in their use cases. Let me explain both approaches...",
        'help': "I'd be happy to help! Could you share your code and the specific error message?",
    }
    
    for key, template in templates.items():
        if key in title_lower:
            return template
    
    return "Thanks for asking! Could you provide more details about your specific use case?"

def main():
    print("=== Stack Overflow 自动回答系统 ===\n")
    questions = get_python_questions()
    
    print(f"找到 {len(questions)} 个问题\n")
    
    for q in questions[:5]:
        title = q.get('title', '')[:60]
        link = q.get('link', '')
        answer = generate_answer_template(title)
        
        print(f"Q: {title}...")
        print(f"建议回答: {answer[:80]}...")
        print(f"链接: {link}\n")
    
    print("=" * 40)
    print("注意: 实际回答需要 Stack Overflow 账号")
    print("下一步: 在平台回复问题建立信任")

if __name__ == "__main__":
    main()
