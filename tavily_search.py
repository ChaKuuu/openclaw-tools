#!/usr/bin/env python3
"""Tavily 搜索 - 寻找赚钱机会"""
import requests
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_KEY = "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"

def search(query):
    r = requests.post('https://api.tavily.com/search', 
        json={'api_key': API_KEY, 'query': query}, timeout=15)
    return r.json()

# 搜索各种机会
queries = [
    "python freelance jobs remote",
    "flask developer needed",
    "upwork python projects hiring",
]

print("=== 赚钱机会搜索 ===\n")

for q in queries:
    print(f"Query: {q}")
    try:
        results = search(q).get('results', [])[:3]
        for r in results:
            title = r.get('title', '')[:70]
            url = r.get('url', '')[:60]
            print(f"  - {title}")
            print(f"    {url}")
        print()
    except Exception as e:
        print(f"  Error: {e}")
