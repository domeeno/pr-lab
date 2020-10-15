import json
import threading

import requests

from logs.log import default_logger
from helpers.utils import data_collector, select_query
from helpers import URL

def travel(road, token):
    content = requests.get(URL + road, headers={'X-Access-Token': token})
    # default_logger.debug("Starting a thread for: " + road + " :: Active threads: " + str(threading.active_count()))
    data_collector(content.text)
    if "link" in json.loads(content.text):
        threadinator(json.loads(content.text)['link'], token)


def new_client(client_to_connect, connection):
    default_logger.debug('New connection with: {}'.format(connection))
    while True:
        msg = client_to_connect.recv(1024)
        if msg.decode() == 'exit':
            break
        default_logger.debug('client message is: {}'.format(msg.decode()))
        if "select " in msg.decode():
            client_to_connect.sendall(select_query(msg.decode())).encode()
        client_to_connect.sendall('sending request: {}'.format(msg.decode()).encode())
    default_logger.debug('{}'.format(connection) + ' disconnected')
    client_to_connect.close()


def threadinator(routes, token, client_data=None):
    workers = []

    if client_data is None:
        for route in routes.values():
            worker = threading.Thread(target=travel, args=(route, token))
            workers.append(worker)
    else:
        client, ip = client_data
        worker = threading.Thread(target=new_client, args=(client, ip))
        workers.append(worker)

    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()
