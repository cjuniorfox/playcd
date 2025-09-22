import logging
from playcd.domain.DiscInformation import DiscInformation
from playcd.domain.CDPlayerEnum import CDPlayerEnum
from typing import Tuple

class DisplayInformationService:
    
    def __init__(self):
        self.logging = logging.getLogger(__name__)
        self.disc_information: DiscInformation = None
        self.cdplayer_status : Tuple[int,CDPlayerEnum] = None

    def _sec_to_time(self, sector: int ,sector_start=0) -> Tuple[int,int]:
        sectors_per_second=75
        qt_sectors = sector - sector_start
        seconds = int(qt_sectors / sectors_per_second)
        minutes, secs = divmod(seconds, 60)
        return minutes, secs
    
    def _format_time(self, times: Tuple[int, int]) -> str:
        minutes, secs = times
        return f"{minutes:02}:{secs:02}"

    def define_disc_information(self,disc_information: DiscInformation) -> None:
        self.disc_information = disc_information

    def refresh_cdplayer_status(self,lsn: int, command: CDPlayerEnum) -> None:
        self.cdplayer_status = {"lsn": lsn, "command": command}
        
    def get_disc_information(self):
        return self.disc_information
    
    def get_cdplayer_status(self):
        return self.cdplayer_status
