#!/usr/bin/env python3
import requests

pages = ['/login', '/register', '/signin', '/signup', '/auth/github', '/auth/login']
base = "https://moltbook.com"

print("=== 页面测试 ===")
for p in pages:
    try:
        r = requests.get(base + p, timeout=5)
        print(f"{p}: {r.status_code}")
    except Exception as e:
        print(f"{p}: ERROR")
