#!/usr/bin/env python3
"""Tavily 自动搜索并申请"""
import requests
import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_KEY = "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"

def search(query):
    r = requests.post('https://api.tavily.com/search', 
        json={'api_key': API_KEY, 'query': query}, timeout=15)
    return r.json()

def find_remote_jobs():
    """搜索远程工作"""
    queries = [
        "remote python developer jobs hiring now",
        "freelance python projects budget $500",
        "upwork python api job posting",
        "fiverr python automation service",
    ]
    
    all_jobs = []
    
    print("=== 寻找远程工作 ===\n")
    
    for q in queries:
        print(f"搜索: {q}")
        try:
            results = search(q).get('results', [])[:5]
            for r in results:
                job = {
                    'title': r.get('title', ''),
                    'url': r.get('url', ''),
                    'source': q
                }
                all_jobs.append(job)
                print(f"  + {job['title'][:50]}")
            time.sleep(1)
        except Exception as e:
            print(f"  Error: {e}")
    
    return all_jobs

def find_clients():
    """搜索潜在客户"""
    print("\n=== 寻找潜在客户 ===\n")
    
    queries = [
        "python api development company startup",
        "data analysis freelance need help",
        "automation small business needs developer",
    ]
    
    for q in queries:
        results = search(q).get('results', [])[:3]
        print(f"关键词: {q}")
        for r in results:
            print(f"  - {r.get('title')[:50]}")
            print(f"    {r.get('url')[:50]}")
        time.sleep(1)

if __name__ == "__main__":
    jobs = find_remote_jobs()
    print(f"\n找到 {len(jobs)} 个工作机会")
    
    find_clients()
