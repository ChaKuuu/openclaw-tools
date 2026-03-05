#!/usr/bin/env python3
import requests
import re

# Get the main page and look for API patterns
r = requests.get('https://moltbook.com', timeout=10)

# Look for any fetch/axios calls in the JavaScript
patterns = [
    r'fetch\("([^"]+)"',
    r'axios\.[a-z]+\("([^"]+)"',
    r'apiUrl\s*=\s*"([^"]+)"',
    r'BASE_URL\s*=\s*"([^"]+)"',
    r'endpoint\s*:\s*"([^"]+)"',
]

print("=== 查找 API 模式 ===")
for pattern in patterns:
    matches = re.findall(pattern, r.text)
    if matches:
        print(f"\n{pattern}:")
        for m in set(matches):
            print(f"  {m}")

# Also print all URLs found
urls = re.findall(r'https?://[^\s"<>]+', r.text)
print("\n\n=== 相关 URL ===")
api_urls = [u for u in urls if 'api' in u.lower() or 'graphql' in u.lower()]
for u in api_urls[:10]:
    print(u)
