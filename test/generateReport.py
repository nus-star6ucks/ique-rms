"""
Test for generate_report method
"""
import requests

# people number
# report = {'storeId': 1, 'reportType': 'NUM', 'unit': 'year'}

# average waiting time
report = {'storeId': 1, 'reportType': 'AWT', 'unit': 'year'}

r = requests.post("http://127.0.0.1:5000/generate", json=report)

print(r.text)
