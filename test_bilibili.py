# -*- coding: utf-8 -*-
import requests
import json
import os

headers = {'User-Agent': 'Mozilla/5.0'}

# B站热门
r = requests.get('https://api.bilibili.com/x/web-interface/popular?ps=10&pn=1', headers=headers, timeout=10)
data = r.json()

if data.get('code') == 0:
    lst = data['data']['list']
    results = []
    for i, v in enumerate(lst, 1):
        title = v.get('title', 'N/A')
        # Get stats - different fields may have the data
        stat = v.get('stat', {})
        play = stat.get('play', v.get('play', 0))
        danmaku = stat.get('danmaku', v.get('danmaku', 0))
        desc = v.get('desc', '')
        
        results.append(f"{i}. {title}")
        results.append(f"   播放: {play} | 弹幕: {danmaku}")
        if desc:
            results.append(f"   描述: {desc}")
        results.append("")
    
    # Write to file
    with open('C:/Users/WUccc/.openclaw/workspace/bilibili_result.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))
    print("Done!")
else:
    print("Error:", data)
