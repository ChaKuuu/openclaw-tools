import requests
import json
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get('https://top.baidu.com/board?tab=realtime', headers=headers)

# 提取 s-data 内容
match = re.search(r'<!--s-data:(\{.*?\})-->', r.text, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    # 提取hotList
    cards = data.get('data', {}).get('cards', [])
    for card in cards:
        if card.get('component') == 'hotList':
            items = card.get('content', [])
            print("百度热搜 Today:")
            print("-" * 40)
            for i, item in enumerate(items[:10], 1):
                word = item.get('word', '')
                hotScore = item.get('hotScore', '')
                print(f"{i}. {word} (热度: {hotScore})")
            break
else:
    print("No s-data found")
