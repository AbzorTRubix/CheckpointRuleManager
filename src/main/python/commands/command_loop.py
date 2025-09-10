from client.client import Client
from .dictionary import *
from .errors import CommandException
import logging

logger = logging.getLogger(__name__)

def command_loop(client: Client):
    while True:
        request = input('>>').split()
        command = request[0]
        args = request[1:] if len(request) > 1 else None
        if command in commands:
            try:
                commands.get(command)(client,args)
            except CommandException as err:
                logger.error(f'CommandException Error : {err}')
        else:
            if command == 'exit':
                break
            elif command == 'publish':
                client.publish()