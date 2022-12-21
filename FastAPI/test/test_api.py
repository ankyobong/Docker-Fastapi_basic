import requests
import json


url = "http://127.0.0.1:8000/items/"
data = {"name": "new_challenge", "description": "test1", "price": 2020, "tax": 2021}

res = requests.post(url, data=json.dumps(data))

print(res.text)
