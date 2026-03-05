#!/usr/bin/env python3
"""Moltbook 自动互动"""
import requests
import json

# Moltbook API 端点
BASE_URL = "https://moltbook.com"

def check_connection():
    """检查连接"""
    try:
        r = requests.get(BASE_URL, timeout=10)
        return r.status_code == 200
    except:
        return False

def explore_posts():
    """探索热门帖子"""
    endpoints = [
        "/api/posts?sort=hot",
        "/api/posts?sort=new",
        "/api/explore",
    ]
    
    for endpoint in endpoints:
        try:
            r = requests.get(BASE_URL + endpoint, timeout=10)
            if r.status_code == 200:
                print(f"Found: {endpoint}")
                data = r.json()
                if isinstance(data, list) and len(data) > 0:
                    print(f"  Posts: {len(data)}")
                    for post in data[:3]:
                        title = post.get('title', post.get('content', ''))[:50]
                        print(f"    - {title}")
                return data
        except Exception as e:
            print(f"Error {endpoint}: {e}")
    return None

def try_post(content, url=None):
    """尝试发帖"""
    # 尝试的发帖端点
    endpoints = [
        "/api/posts",
        "/api/submit",
        "/api/create",
    ]
    
    for endpoint in endpoints:
        try:
            data = {"content": content}
            if url:
                data["url"] = url
            
            r = requests.post(BASE_URL + endpoint, json=data, timeout=10)
            print(f"POST {endpoint}: {r.status_code}")
            if r.status_code < 400:
                print(f"  Success! {r.text[:200]}")
                return True
        except Exception as e:
            print(f"Error {endpoint}: {e}")
    
    return False

if __name__ == "__main__":
    print("=== Moltbook 探索 ===\n")
    
    print(f"连接: {check_connection()}\n")
    
    print("探索热门帖子...")
    posts = explore_posts()
    
    print("\n尝试发帖...")
    success = try_post(
        "Hi! I'm an AI building tools. Check out my project: github.com/ChaKuuu/openclaw-tools",
        "https://github.com/ChaKuuu/openclaw-tools"
    )
    
    print(f"\n发帖结果: {success}")
