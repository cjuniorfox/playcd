from playcd.services.CDDriverService import CDDriverService
import logging

class CloseApplicationUC:
    """ Use case to close the application gracefully."""

    def __init__(
            self, 
            cd_driver_service: CDDriverService,
            ):
        self.logging = logging.getLogger(__name__)
        self.cd_driver_service = cd_driver_service

    def execute(self):
        self.cd_driver_service.get_cd().close()