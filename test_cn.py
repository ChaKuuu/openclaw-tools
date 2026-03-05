import requests

sites = ['baidu.com', 'qq.com', 'bilibili.com', 'zhihu.com', 'juejin.cn', 'csdn.net', 'baidu.com', 'aliyun.com']

print("=== 国内网站测试 ===\n")
for s in sites:
    try:
        r = requests.get(f'https://{s}', timeout=5)
        print(f"{s}: {r.status_code}")
    except Exception as e:
        print(f"{s}: FAIL")
