import requests
import json

url = "http://127.0.0.1:8000/predict_price/"
headers = {"Content-Type": "application/json"}

with open("car_data_test2.json", "r") as file:
    json_data = json.load(file)

response = requests.post(url, json=json_data, headers=headers)

print(response.status_code)
print(response.json())

