import logging
import argparse
import getpass
import os,datetime
from .client import Client
from commands import command_loop

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('server',type=str,help='SMS Server')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse()
    username = input('Please provide your username: ')
    password = getpass.getpass('Please provide your password: ')
    os.makedirs('logs', exist_ok=True)
    log_name = f'logs/{username}-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.txt'
    logging.basicConfig(filename=log_name, level=logging.INFO,
                        format="%(levelname)s %(name)s %(threadName)s {0} %(message)s".format(username))
    client = Client(args.server)
    client.login(username,password)
    command_loop(client)
    client.logout()