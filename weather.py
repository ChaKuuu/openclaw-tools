# -*- coding: utf-8 -*-
import requests
import json

r = requests.get('https://wttr.in/Guiyang?format=j1', timeout=15)
data = r.json()

tomorrow = data['weather'][1]
hourly = tomorrow['hourly']

output = []
output.append('=== 贵阳观山湖 明天(2026年3月2日) 天气预报 ===')
output.append('')
output.append(f'平均温度: {tomorrow["avgtempC"]}°C')
output.append(f'最高温度: {tomorrow["maxtempC"]}°C')
output.append(f'最低温度: {tomorrow["mintempC"]}°C')
output.append(f'日出: {tomorrow["astronomy"][0]["sunrise"]}')
output.append(f'日落: {tomorrow["astronomy"][0]["sunset"]}')
output.append('')
output.append('=== 小时预报 ===')
for h in hourly:
    time = h['time']
    temp = h['tempC']
    desc = h['weatherDesc'][0]['value']
    chance = h['chanceofrain']
    output.append(f'{time}:00 - {temp}°C | {desc} | 降雨概率: {chance}%')

# Save to file
with open('C:/Users/WUccc/.openclaw/workspace/weather.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
print('Done')
