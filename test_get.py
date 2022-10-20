"""
Test for getReport method
"""
import requests

require = {'reportId': None, 'merchantId': None, 'storeId': 1}

r = requests.get("http://127.0.0.1:5000/get", params=require)

print(r.text)
