#!/usr/bin/env python3
"""
贾维斯 - 全自动赚钱系统
7x24 小时自动运行
"""
import requests
import time
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_KEY = "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"

def search(query):
    r = requests.post('https://api.tavily.com/search', 
        json={'api_key': API_KEY, 'query': query}, timeout=15)
    return r.json()

def main():
    print("=== 贾维斯全自动赚钱系统 ===")
    print("目标: $50/天\n")
    
    # 持续搜索
    queries = [
        "python freelance jobs remote hiring",
        "upwork python project budget 500",
        "fiverr python automation service",
        "remote python developer job",
        "python script automation needed"
    ]
    
    all_results = []
    
    for q in queries:
        print(f"搜索: {q}")
        results = search(q).get('results', [])
        all_results.extend(results)
        time.sleep(1)
    
    print(f"\n找到 {len(all_results)} 个机会")
    
    # 保存结果
    with open('job_opportunities.txt', 'w', encoding='utf-8') as f:
        f.write(f"=== 赚钱机会 {time.strftime('%Y-%m-%d %H:%M')} ===\n\n")
        for r in all_results:
            f.write(f"标题: {r.get('title','')}\n")
            f.write(f"链接: {r.get('url','')}\n")
            f.write("\n")
    
    print("已保存到 job_opportunities.txt")

if __name__ == "__main__":
    main()
