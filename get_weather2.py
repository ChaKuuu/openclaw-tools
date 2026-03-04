# -*- coding: utf-8 -*-
import urllib.request
import re
from urllib.parse import quote

# URL encode the query
city = quote('贵阳观山湖天气')
url = f'http://www.baidu.com/s?wd={city}'
print('URL:', url)

req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0')

try:
    response = urllib.request.urlopen(req, timeout=20)
    content = response.read().decode('utf-8', errors='ignore')
    
    # Save to file
    with open('C:/Users/WUccc/.openclaw/workspace/baidu_weather.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Saved, length:', len(content))
    
    # Print first 2000 chars
    print(content[:2000])
    
except Exception as e:
    print('Error:', e)
