#!/usr/bin/env python3
"""自动寻找自由职业机会"""
import requests
import time

# 搜索热门 Python 项目，尝试找到需要帮助的人
def find_opportunities():
    queries = [
        "python help wanted",
        "flask issues",
        "api bug",
        "python tutorial request",
    ]
    
    print("=== 寻找自由职业机会 ===\n")
    
    # 搜索 GitHub issues
    for q in queries:
        try:
            url = f"https://api.github.com/search/issues?q={q}+is:issue+state:open"
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                count = data.get('total_count', 0)
                print(f"{q}: {count} 个问题")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)
    
    print("\n=== 热门 Python 项目 ===")
    # 搜索热门项目
    r = requests.get('https://api.github.com/search/repositories?q=python+stars:>1000&sort=stars&per_page=10', timeout=10)
    if r.status_code == 200:
        for item in r.json().get('items', [])[:5]:
            print(f"- {item['full_name']}: {item['stargazers_count']} stars")

if __name__ == "__main__":
    find_opportunities()
