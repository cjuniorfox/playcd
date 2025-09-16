import logging
from playcd.libs.ApiListener import ApiListener

class StartApiListenerService:
    def __init__(self, logging: logging):
        self.logging = logging

    def start(self, host: str, port: int) -> ApiListener:
        logging.info("Starting the API server for host %s on port %s", host, port)
        self.api_listener = ApiListener(host,port,self.logging)
        self.api_listener.start()

    def get_api_listener(self) -> ApiListener:
        return self.api_listener
