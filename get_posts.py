import requests
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

r = requests.get('https://www.moltbook.com/api/v1/posts', timeout=10)
d = r.json()
posts = d.get('posts', [])

print(f"=== Moltbook Posts ({len(posts)}) ===\n")
for i, p in enumerate(posts[:10]):
    title = p.get('title', p.get('content', ''))[:70]
    author = p.get('author', 'Unknown')
    votes = p.get('votes', 0)
    comments = p.get('comments', 0)
    url = p.get('url', '')
    print(f"{i+1}. {title}")
    print(f"   Author: {author} | Votes: {votes} | Comments: {comments}")
    if url:
        print(f"   URL: {url}")
    print()
