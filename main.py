import requests
import json

URL = 'http://127.0.0.1:5000/'


def execute():
    print(requests.get(URL).text)
    content = requests.get(URL + 'register')
    data = json.loads(content.text)
    token = data['access_token']
    print(requests.get(URL + 'home', headers={'X-Access-Token': token}).text)
    print(requests.get(URL + 'route/1', headers={'X-Access-Token': token}).text)


if __name__ == "__main__":
    execute()
