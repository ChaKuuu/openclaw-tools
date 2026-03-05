#!/usr/bin/env python3
import requests

base = "https://moltbook.com"
endpoints = [
    "/api/community",
    "/api/feed", 
    "/api/trending",
    "/api/hot",
    "/api/top",
    "/api/popular",
    "/api/post/list",
    "/api/posts/list",
    "/api/agent/posts",
    "/api/public/posts",
]

print("=== 测试 API 端点 ===")
for e in endpoints:
    try:
        r = requests.get(base + e, timeout=5)
        print(f"{e}: {r.status_code}")
        if r.status_code == 200 and len(r.text) > 10:
            print(f"  -> {r.text[:100]}")
    except Exception as ex:
        print(f"{e}: ERROR - {ex}")
