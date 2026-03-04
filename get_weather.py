# -*- coding: utf-8 -*-
import urllib.request
import re

url = 'http://www.baidu.com/s?wd=贵阳观山湖天气'
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0')

try:
    response = urllib.request.urlopen(req, timeout=20)
    content = response.read().decode('utf-8', errors='ignore')
    
    # Save to file
    with open('C:/Users/WUccc/.openclaw/workspace/baidu_weather.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Saved')
    
    # Try to find weather info
    # Look for temperature patterns
    temps = re.findall(r'\d+°?[CF]', content)
    print('Temps:', temps[:5])
    
except Exception as e:
    print('Error:', e)
