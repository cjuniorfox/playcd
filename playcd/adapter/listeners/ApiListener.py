from fastapi import FastAPI, Response, status
import uvicorn
import logging
import threading
from playcd.services.RegisterCommandService import RegisterCommandService
from playcd.services.ReadStatusService import ReadStatusService
from playcd.domain.DisplayInformation import DisplayInformation
from playcd.domain.adapter.DisplayInformationResponse import DisplayInformationResponse
from playcd.domain.mapper.DisplayInformationResponseMapper import DisplayInformationResponseMapper

class ApiListener:
    def __init__(
            self, 
            register_command_service: RegisterCommandService, 
            read_status_service: ReadStatusService, 
            host: str, 
            port: int
        ):
        self.register_command_service = register_command_service
        self.read_status_service = read_status_service
        self.host = host
        self.port = port
        self.logging = logging.getLogger(__name__)
        self.app = FastAPI()
        self._routes()
        self.is_running = False

    def _routes(self) -> None:
        @self.app.post("/command/{command}")
        def send(command:str, response: Response) -> dict[str,str]:
            """Send command to the CD Player"""
            try:
                self.register_command_service.execute(command)
                return { "status" : "queued", "command": command }
            except ValueError:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"status": "invalid", "command": command}
            
        @self.app.get("/display")
        def display(response: Response) -> dict:
            """Returns information about the reproduction of the disc"""
            #TODO: Create an service to handle the display information
            try:
                display_information: DisplayInformation = self.read_status_service.execute()
                display_information_response : DisplayInformationResponse = DisplayInformationResponseMapper.map(display_information)
                return { "status": "ok", "display": display_information_response.to_dict() }
            except Exception as e:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {"status": "error", "detail":str(e)}            
        
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
