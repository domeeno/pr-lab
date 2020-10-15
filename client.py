import socket
import argparse

from logs.log import default_logger

parser = argparse.ArgumentParser(description="Client")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=9999)
args = parser.parse_args()

default_logger.debug('Connecting to server: {}:{}'.format(args.host, args.port))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    try:
        sock.connect((args.host, args.port))
        default_logger.debug("Connected to {}:{}".format(args.host, args.port))
    except Exception as e:
        default_logger.error(str(e) + " when trying to connect to {}:{}".format(args.host, args.port))

    while True:
        msg = input()
        sock.sendall(msg.encode('utf-8'))
        if msg == 'exit':
            default_logger.debug('Disconnected.')
            break
        data = sock.recv(1024)
        default_logger.debug('Server response: {}'.format(data.decode()))
