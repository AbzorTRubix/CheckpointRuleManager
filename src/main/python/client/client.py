import json
import cpapi
import logging

logger = logging.getLogger(__name__)

class Client:
    def __init__(self, server):
        self.server = server.rstrip('/')
        self.sid = None
        self.username = None
        self.client_args = cpapi.APIClientArgs(server=self.server)
        self.client = cpapi.APIClient(self.client_args)

    def login(self,username,password):
        self.username = username
        login_res = self.client.login(self.username, password)
        if not login_res.success:
            raise Exception(f"Login failed: {login_res.error_message}")
        self.sid = login_res.data.get("sid")
        logger.info(f'Successful login for {self.username} - sid is {self.sid}')

    def api_call(self, command, params=None):
        params = params or {}
        response = self.client.api_call(command, params)
        if response.success:
            logger.info(f' - executed command {command} successfully')
        else:
            logger.error(f' - failed to execute command - Error:\n{response.error_message}')
        return response

    def publish(self):
        comments = input("please add a description of changes here: ")
        logger.info(f' - publishing changes')
        self.api_call("set-session",{"description":comments})
        self.api_call("publish", {})
        logger.info(f' - published changes')

    def logout(self):
        logger.info(f' - logging out')
        del(self.client)
        logger.info(f' - successful log out')