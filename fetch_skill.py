import requests
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
r = requests.get('https://moltbook.com/skill.md', timeout=10)
print(r.text)
