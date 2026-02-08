import urllib.request
import json

url = "https://api.github.com/users/wanyview/repos?per_page=100&sort=updated"
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        for repo in data:
            name = repo.get('name', '')
            desc = repo.get('description', '') or ''
            print(f"{name} - {desc}")
except Exception as e:
    print(f"Error: {e}")
