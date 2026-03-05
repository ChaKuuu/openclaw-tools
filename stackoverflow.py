import requests

# Get latest Python questions from Stack Overflow
url = "https://api.stackexchange.com/2.3/questions"
params = {
    "order": "desc",
    "sort": "activity",
    "tagged": "python",
    "site": "stackoverflow",
    "pagesize": 10
}

r = requests.get(url, params=params, timeout=10)
data = r.json()

print("=== 最新 Python 问题 ===\n")
for q in data.get('items', [])[:10]:
    title = q.get('title', '')[:70]
    link = q.get('link', '')
    print(f"Q: {title}")
    print(f"   {link}\n")

print(f"Total: {data.get('total')} questions")
