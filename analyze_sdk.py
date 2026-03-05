import requests
import re

r = requests.get('https://unpkg.com/moltbook@1.1.0/dist/index.cjs', timeout=10)
text = r.text

# Look for endpoint definitions
patterns = [
    r'endpoint["\']?\s*[:=]\s*["\']([^"\']+)["\']',
    r'["\']\/api[^\'"]+["\']',
    r'["\']posts["\']',
]

for p in patterns:
    matches = re.findall(p, text)
    if matches:
        print(f"Pattern: {p}")
        for m in set(matches):
            print(f"  {m}")

# Also look for URL patterns
url_patterns = re.findall(r'https?://[^\s"\)]+', text)
print("\n=== URLs ===")
for u in list(set(url_patterns))[:10]:
    print(u)
