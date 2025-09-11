from client.client import Client
from .dictionary import *
from .errors import CommandException
from.parser import parse_command_args
import logging

logger = logging.getLogger(__name__)

def command_loop(client: Client):
    '''
    Function: command_loop()
    Description: Driving command loop for the TUI. User input is split so the command and it's arguments are different objects.
    '''
    while True:
        request = parse_command_args(list(input('>>')))
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