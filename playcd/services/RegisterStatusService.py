import logging
from playcd.domain.DiscInformation import DiscInformation
from playcd.domain.CDPlayerEnum import CDPlayerEnum
from playcd.domain.mapper.DisplayInformationMapper import DisplayInformationMapper
from playcd.adapter.repository.DisplayInformationRepository import DisplayInformationRepository

class RegisterStatusService:
    
    def __init__(self, display_information_repository: DisplayInformationRepository):
        self.logging = logging.getLogger(__name__)
        self.display_information_repository = display_information_repository


    def execute(self,lsn: int, command: CDPlayerEnum, disc_information: DiscInformation) -> None:
        logging.debug("Registeiring new display information from lsn %s and command %s", lsn, command)
        display_information = DisplayInformationMapper.map(
            lsn = lsn,
            command = command,
            disc_information = disc_information
        )
        self.display_information_repository.set(display_information)
        logging.debug("Successfully registered display information: %s", display_information)