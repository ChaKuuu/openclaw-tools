#!/usr/bin/env python3
"""
网页抓取工具 - $15
"""
import requests
from bs4 import BeautifulSoup
import csv
import time
import json

class WebScraper:
    """通用网页抓取工具"""
    
    def __init__(self, headers=None):
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_links(self, url, selector=None):
        """抓取链接"""
        r = self.session.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        links = []
        if selector:
            elements = soup.select(selector)
        else:
            elements = soup.find_all('a')
        
        for elem in elements:
            href = elem.get('href')
            text = elem.get_text(strip=True)
            if href:
                links.append({'url': href, 'text': text})
        
        return links
    
    def scrape_table(self, url, table_selector='table'):
        """抓取表格"""
        r = self.session.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.select_one(table_selector)
        
        if not table:
            return []
        
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        rows = []
        
        for tr in table.find_all('tr')[1:]:
            cells = [td.get_text(strip=True) for td in tr.find_all('td')]
            if cells:
                rows.append(cells)
        
        return {'headers': headers, 'rows': rows}
    
    def save_to_csv(self, data, filename):
        """保存为 CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            if isinstance(data, list) and data:
                if isinstance(data[0], dict):
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
                else:
                    writer = csv.writer(f)
                    writer.writerows(data)
        return filename
    
    def scrape_json(self, url, key_path=None):
        """抓取 JSON 数据"""
        r = self.session.get(url, timeout=10)
        data = r.json()
        
        if key_path:
            for key in key_path.split('.'):
                data = data.get(key, {})
        
        return data

# 示例
if __name__ == "__main__":
    scraper = WebScraper()
    
    # 示例：抓取 GitHub trending
    # links = scraper.scrape_links('https://github.com/trending/python')
    # print(f"Found {len(links)} links")
    
    print("Web Scraper ready!")
    print("Usage:")
    print("  scraper = WebScraper()")
    print("  links = scraper.scrape_links('https://example.com')")
    print("  data = scraper.scrape_table('https://example.com')")
