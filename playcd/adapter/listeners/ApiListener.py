from fastapi import FastAPI, Response, status
import uvicorn
import logging
import threading
from playcd.services.CommandQueueService import CommandQueueService
from playcd.domain.CDPlayerEnum import CDPlayerEnum

class ApiListener:
    def __init__(self, command_queue_service: CommandQueueService, host: str, port: int):
        self.command_queue_service = command_queue_service
        self.host = host
        self.port = port
        self.logging = logging.getLogger(__name__)
        self.app = FastAPI()
        self._routes()
        self.is_running = False

    def _routes(self) -> None:
        @self.app.post("/command/{command}")
        def send(command:str, response: Response) -> dict[str,str]:
            try:
                self.command_queue_service.clear()
                self.command_queue_service.put(CDPlayerEnum.from_command(command))
                return { "status" : "queued", "command": command }
            except ValueError:
                return { "status": "invalid", "command": command }
            
        @self.app.get("/display")
        def display(response: Response) -> dict:
            """Returns information about the reproduction of the disc"""
            #TODO: Create an service to handle the display information
            return { "status": "ok", "display": "display" }
        
    def _http_server(self) -> None:
        logger = logging.getLogger("")
        level_int = logger.getEffectiveLevel()
        level_name = self._logging.getLevelName(level_int).lower()
        uvicorn.run(self._app, host=self._host, port=self._port, log_level=level_name)

    def start(self) -> None:
        """Starts the listener thread"""
        if self._is_running:
            self._logging.warn("API Listener already running")
            return
        self._is_running = True
        self._listener_thread = threading.Thread(target=self._http_server,daemon=True)
        self._listener_thread.start()

    def stop(self) -> None:
        """Stops the listener"""
        if self._is_running:
            self._is_running = False
            self._listener_thread.join(timeout=2)
