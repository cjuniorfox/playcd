import logging
from playcd.libs.ApiListener import ApiListener

class StartApiListenerService:
    def __init__(self, logging: logging):
        self.logging = logging

    def start(self, host: str, port: int) -> ApiListener:
        logging.info("Starting the API server for host %s on port %s", host, port)
        apiListener = ApiListener(host,port,self.logging)
        apiListener.start()
        return apiListener