from fastapi import FastAPI, Response, status
import queue
import threading
import uvicorn
from typing import List
import logging
from playcd.domain.CDPlayerEnum import CDPlayerEnum

class ApiListener:
    def __init__(self, host, port, logging):
        self._host = host
        self._port = port
        self._logging = logging
        self._command_queue = queue.Queue()
        self._display_data = None
        self._app = FastAPI()
        self._setup_routes()
        self._is_running = False

    def _setup_routes(self) -> None:
        @self._app.post("/command/{cmd}")
        def send_command(cmd:str, response: Response) -> dict[str,str]:
            try:
                cmd = cmd.lower()
                comamnd = CDPlayerEnum.from_command(cmd)
                self._command_queue.queue.clear()
                self._command_queue.put(comamnd)
                return { "status" : "queued", "command": comamnd }
            except ValueError:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return { "status": "invalid", "command": cmd }

        @self._app.get("/display")
        def get_display(response: Response) -> dict:
            """Returns information about the reproduction of the disc"""
            if self._display_data:
                return { "status": "ok", "display": self._display_data }
            """If there's no data to display"""
            response.status_code = status.HTTP_204_NO_CONTENT
            return { "status" : "no content"}

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

    def get_command(self) -> str:
        """Retrieves the command from the queue"""
        try:
            return self._command_queue.get_nowait()
        except queue.Empty:
            return None

    def set_display(self,display:dict) -> None:
        self._display_data = display


