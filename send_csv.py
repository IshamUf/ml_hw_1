import requests

url = "http://127.0.0.1:8000/predict_prices/"
files = {"file": ("test.csv", open("test.csv", "rb"))}

response = requests.post(url, files=files)

print(response.status_code)
print(response.json())
