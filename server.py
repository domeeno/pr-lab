import socket
import argparse

from logs.log import default_logger
from helpers.fetch import execute
from helpers.thread_work import threadinator

parser = argparse.ArgumentParser(description="Server")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=9999)
args = parser.parse_args()

default_logger.debug(f"Running server on: {args.host}:{args.port}")

default_logger.info('Waiting for server to collect data from pr-server')
execute()
default_logger.info('Server {}:{} ready to use.\n\n'.format(args.host, args.port))

sck = socket.socket()
sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    sck.bind((args.host, args.port))
    sck.listen(5)
except Exception as e:
    default_logger.warning(str(e) + " host: {}:{}".format(args.host, args.port))
    raise SystemExit(f"Couldn't bind the server on host: {args.host}:{args.port}")


while True:
    try:
        threadinator(routes="", token="", client_data=sck.accept())
    except KeyboardInterrupt as e:
        default_logger.debug('Shutting down server')
    except Exception as e:
        default_logger.debug(e)
