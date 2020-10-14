import json
import threading
import requests

from log import default_logger
from thread_work import threadinator
from utils import people_data

URL = 'http://127.0.0.1:5000'


def execute():
    content = requests.get(URL + '/register')
    data = json.loads(content.text)
    token = data['access_token']
    routes = json.loads(requests.get(URL + '/home', headers={'X-Access-Token': token}).text)['link']

    # default_logger.debug("Up and running. Starting the processes:")
    threadinator(routes, token)
    # default_logger.debug("Finished the program")

    for people in people_data:
        print(people)
        print("-----------------------------------------------")


if __name__ == "__main__":
    execute()
