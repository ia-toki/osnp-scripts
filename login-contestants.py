import csv
import requests

success = 0

def login(username):
    url = 'https://api.judgels/v2/session/login'
    body = {
        'usernameOrEmail': username,
        'password': 'puspresnas'
    }
    response = requests.post(url, json=body)
    if response.status_code == 200:
        response_data = response.json()
        token = response_data.get("token")
        global success
        success += 1
        print("{},{}".format(username, token))
    else:
        print("Error:", response.status_code)

with open('contestants.csv', 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    for row in reader:
        username = row[0]
        login(username)
