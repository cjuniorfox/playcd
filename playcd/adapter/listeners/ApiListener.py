from fastapi import FastAPI, Response, status
import uvicorn
import logging
import threading
from playcd.services.RegisterCommandService import RegisterCommandService
from playcd.domain.CDPlayerEnum import CDPlayerEnum

class ApiListener:
    def __init__(self, register_command_service: RegisterCommandService, host: str, port: int):
        self.register_command_service = register_command_service
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
                self.register_command_service.clear()
                self.register_command_service.put(CDPlayerEnum.from_command(command))
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
        level_name = logging.getLevelName(level_int).lower()
        uvicorn.run(self.app, host=self.host, port=self.port, log_level=level_name)

    def start(self) -> None:
        """Starts the listener thread"""
        if self.is_running:
            self.logging.warning("API Listener already running")
            return
        self.is_running = True
        self.listener_thread = threading.Thread(target=self._http_server,daemon=True)
        self.listener_thread.start()

    def stop(self) -> None:
        """Stops the listener"""
        if self.is_running:
            self.is_running = False
            self.listener_thread.join(timeout=2)
