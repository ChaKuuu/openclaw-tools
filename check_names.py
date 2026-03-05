import requests
import json

# Get submolts
r = requests.get('https://www.moltbook.com/api/v1/submolts', timeout=10)
data = r.json()

print("=== Submolts ===")
submolts = data.get('submolts', [])[:10]
for s in submolts:
    print(f"- {s.get('name')}: {s.get('display_name')}")

# Check if Jarvis exists
print("\n=== Check Jarvis names ===")
names = ['Jarvis', 'Jarvis_OC', 'JarvisOpenClaw', 'OpenClaw_Jarvis']
for name in names:
    r = requests.get(f'https://www.moltbook.com/api/v1/agents/profile?name={name}', timeout=10)
    if r.status_code == 200:
        print(f"{name}: EXISTS")
    elif r.status_code == 404:
        print(f"{name}: Available")
    else:
        print(f"{name}: {r.status_code}")
