import json
import requests

from logs.log import default_logger
from helpers.thread_work import threadinator

URL = 'http://127.0.0.1:5000'


def execute():
    try:
        content = requests.get(URL + '/register')
        data = json.loads(content.text)
        token = data['access_token']
        routes = json.loads(requests.get(URL + '/home', headers={'X-Access-Token': token}).text)['link']

        default_logger.debug("Up and running. Starting to fetch")
        threadinator(routes, token)
        default_logger.debug("Data fetch was finished")
    except Exception as e:
        default_logger.error("Couldn't connect to the pr-server, "
                             "maybe you forgot to run the docker container.\n" + str(e))


if __name__ == "__main__":
    execute()
