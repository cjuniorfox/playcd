from playcd.domain.DisplayInformation import DisplayInformation
from playcd.adapter.repository.DisplayInformationRepository import DisplayInformationRepository
import logging

class ReadStatusService:
    def __init__(self, display_information_repository: DisplayInformationRepository):
        self.logging = logging.getLogger(__name__)
        self.display_information_repository = display_information_repository

    def execute(self) -> DisplayInformation:
        logging.debug("Reading disc information from repository")
        display_information = self.display_information_repository.get()
        if display_information == None:
            logging.warning("Display information is null at this moment")
        else:
            logging.debug("Retrieved display information from repository: %s", display_information)
        return display_information