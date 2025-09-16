from playcd.services.KeyboardListenerService import KeyboardListenerService
from playcd.services.StartApiListenerService import StartApiListenerService
from playcd.services.CDDriverService import CDDriverService
import logging

class CloseApplicationUC:
    """ Use case to close the application gracefully."""

    def __init__(
            self, 
            logging: logging, 
            keyboard_listener_service: KeyboardListenerService,
            api_listener_service: StartApiListenerService,
            cd_driver_service: CDDriverService,
            ):
        self.logging = logging
        self.keyboard_listener_service = keyboard_listener_service
        self.api_listener_service = api_listener_service
        self.cd_driver_service = cd_driver_service

    def execute(self):
        self.keyboard_listener_service.get_keyboard_listener().stop()
        self.api_listener_service.get_api_listener().stop()
        self.cd_driver_service.get_cd().close()