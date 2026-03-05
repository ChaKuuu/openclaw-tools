#!/usr/bin/env python3
import requests
sites = ['gumroad.com','github.com','ko-fi.com','upwork.com','pypi.org']
for s in sites:
    try:
        r = requests.get(f'https://{s}', timeout=5)
        print(f"{s}: {r.status_code}")
    except Exception as e:
        print(f"{s}: FAIL - {e}")
