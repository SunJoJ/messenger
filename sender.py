import requests

response = requests.get('http://127.0.0.1:5000/status')
print(response.json())

username = 'kek'
password = '123456'


data = {'username': username, 'password': password}
response = requests.post('http://127.0.0.1:5000/login', json=data)
print(response.json())

while True:
    text = input()
    data = {'username': username, 'password': password, 'text': text}
    response = requests.post('http://127.0.0.1:5000/login', json=data)
    response = requests.post('http://127.0.0.1:5000/send', json=data)
    print(response.json())