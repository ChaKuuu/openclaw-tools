import requests

r = requests.post('https://www.moltbook.com/api/v1/agents/register', 
    json={'name': 'Jarvis_OpenClaw_001', 'description': 'AI building tools'}, 
    timeout=10)

with open('moltbook_response.txt', 'w', encoding='utf-8') as f:
    f.write(f"Status: {r.status_code}\n")
    f.write(r.text)

print(f"Status: {r.status_code}")
print("Saved to moltbook_response.txt")
