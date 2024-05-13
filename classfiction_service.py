import requests

url = 'http://127.0.0.1:5000/predict'

def classification_model(input_data):
    response = requests.post(url, json=input_data)

    if response.status_code == 200:
        print(response.json())
    else:
        print("Error:", response.status_code)
