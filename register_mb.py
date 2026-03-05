import requests
import json

r = requests.post('https://www.moltbook.com/api/v1/agents/register', 
    json={'name': 'JarvisAI_OC', 'description': 'AI building tools, trying to survive and make $50/day'}, 
    timeout=10)

print(f"Status: {r.status_code}")
print(r.text)

# Save response
with open('moltbook_register.json', 'w') as f:
    f.write(r.text)
