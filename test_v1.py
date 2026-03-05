import requests

base = "https://www.moltbook.com/api/v1"
endpoints = ['/posts', '/feed', '/community', '/trending', '/hot', '/top', '/explore']

print("=== 测试 V1 API ===")
for e in endpoints:
    try:
        r = requests.get(base + e, timeout=5)
        print(f"{e}: {r.status_code}")
        if r.status_code == 200:
            print(f"  Data: {r.text[:200]}")
    except Exception as ex:
        print(f"{e}: ERROR - {ex}")
