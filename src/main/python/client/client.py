import json
import cpapi
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Client:
    def __init__(self, server: str) -> None:
        '''
        Function: __init__()
        Description: Constructor for Client class. Stores server IP address.
        '''
        self.server = server.rstrip('/')
        self.sid = None
        self.username = None
        self.client_args = cpapi.APIClientArgs(server=self.server)
        self.client = cpapi.APIClient(self.client_args)
        self.login_timestamp = None

    def login(self,username: str,password: str) -> None:
        '''
        Function: login()
        Description: logs a user in using an API call and stores the returned SID.
        '''
        self.username = username
        login_res = self.client.login(self.username, password)
        if not login_res.success:
            raise Exception(f"Login failed: {login_res.error_message}")
        self.sid = login_res.data.get("sid")
        logger.info(f'Successful login for {self.username} - sid is {self.sid}')
        self.login_timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")

    def api_call(self, command: str, params: dict = None):
        '''
        Function: api_call()
        Description: Performs an API call using the command and dictionary provided.
        '''
        params = params or {}
        response = self.client.api_call(command, params)
        if response.success:
            logger.info(f' - executed command {command} successfully')
        else:
            logger.error(f' - failed to execute command - Error:\n{response.error_message}')
        return response

    def publish(self):
        '''
        Function: publish()
        Description: Publishes changes made through the API. Prompts user to description of changes.
        '''
        comments = input("please add a description of changes here: ")
        logger.info(f' - publishing changes')
        self.api_call("set-session",{"description":comments})
        self.api_call("publish", {})
        logger.info(f' - published changes')

    def logout(self):
        '''
        Function: logout()
        Description: logs a user out. deletes API client object.
        '''
        logger.info(f' - logging out')
        del(self.client)
        logger.info(f' - successful log out')