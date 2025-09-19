import logging
from playcd.domain.DiscInformation import DiscInformation
from playcd.domain.adapter.DisplayInformation import DisplayInformation
from playcd.domain.CDPlayerEnum import CDPlayerEnum
from typing import Tuple
import queue

class DisplayInformationService:
    
    def __init__(self):
        self.logging = logging.getLogger(__name__)
        self.disc_information: DiscInformation = None
        self.cdplayer_status = queue.Queue()
        self.last_cdplayer_status : Tuple[int,CDPlayerEnum] = None

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

    def put(self,lsn: int, command: CDPlayerEnum) -> None:
        self.last_cdplayer_status = {"lsn": lsn, "command": command}
        self.cdplayer_status.put(self.last_cdplayer_status)
        
    def get_cdplayer_status(self) -> Tuple[str,CDPlayerEnum] | None:
        try:
            cdplayer_status = self.cdplayer_status.get_nowait()
            return cdplayer_status
        except queue.Empty:
            return None
        
    def get_disc_information(self):
        return self.disc_information
    
    def get_last_cdplayer_status(self):
        return self.last_cdplayer_status
