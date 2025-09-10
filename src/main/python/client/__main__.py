import logging
import argparse
import getpass
import os,datetime
from .client import Client
from commands import command_loop

logger = logging.getLogger(__name__)

def parse() -> argparse.Namespace:
    '''
    Function: parse()
    Description: Parses command line inputs at program start
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('server',type=str,help='SMS Server')
    return parser.parse_args()

def main():
    '''
    Function: main()
    Description: Driver of the program. Prompts user for their username/password, 
    creates the logging directory and file, and establishes client connection with API library.
    '''
    args = parse()
    username = input('Please provide your username: ')
    password = getpass.getpass('Please provide your password: ')
    os.makedirs('logs', exist_ok=True)
    log_name = f'logs/{username}-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.txt'
    logging.basicConfig(filename=log_name, level=logging.INFO,
                        format="%(levelname)s %(name)s %(threadName)s {0} %(message)s".format(username))
    client = Client(args.server)
    try:
        client.login(username,password)
    except Exception as err:
        print('failed log in, check logs for description')
        logger.error(err)
    command_loop(client)
    client.logout()

if __name__ == '__main__':
    main()