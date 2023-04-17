import requests

# url = 'https://api.divar.ir/v8/web-search/1/refrigerator-freezer'
url = 'https://divar.ir/v/-/AZLQF3i4'

headers = {
    'Content-Type': 'application/json'
}

# json = {"json_schema": {"category": {"value": 'refrigerator-freezer'}},
#         "last-post-date": 16807747371033382}
# res = requests.post(url, json=json, headers=headers)
res = requests.post(url, headers=headers)

data = res.json()

print(data)
