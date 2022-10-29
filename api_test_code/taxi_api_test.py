import requests

res = requests.get('http://localhost:5000/taxi/platform/list')

print(res.text)
