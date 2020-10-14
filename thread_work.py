import json
import threading

import requests

from log import default_logger
from utils import data_collector


def travel(road, token):
    from main import URL
    content = requests.get(URL + road, headers={'X-Access-Token': token})
    # default_logger.debug("Starting a thread for: " + road + " :: Active threads: " + str(threading.active_count()))
    data_collector(content)
    if "link" in json.loads(content.text):
        threadinator(json.loads(content.text)['link'], token)


def threadinator(routes, token):
    drivers = []
    for route in routes.values():
        driver = threading.Thread(target=travel, args=(route, token))
        drivers.append(driver)

    for driver in drivers:
        driver.start()

    for driver in drivers:
        driver.join()
