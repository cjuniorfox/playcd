import logging
from playcd.domain.DiscInformation import DiscInformation
from playcd.domain.CDPlayerEnum import CDPlayerEnum
from playcd.domain.DisplayInformation import DisplayInformation
from playcd.domain.mapper.DisplayInformationMapper import DisplayInformationMapper
from typing import Tuple

class DisplayInformationService:
    
    def __init__(self):
        self.logging = logging.getLogger(__name__)
        self.disc_information: DiscInformation = None
        self.cdplayer_status : Tuple[int,CDPlayerEnum] = None

    def define_disc_information(self,disc_information: DiscInformation) -> None:
        self.disc_information = disc_information

    def refresh_cdplayer_status(self,lsn: int, command: CDPlayerEnum) -> None:
        self.cdplayer_status = {"lsn": lsn, "command": command}

    def get_display_information(self) -> DisplayInformation:
        return DisplayInformationMapper.map(
            lsn = self.cdplayer_status['lsn'],
            command = self.cdplayer_status['command'],
            disc_information = self.disc_information
        )
