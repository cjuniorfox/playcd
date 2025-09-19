import logging
from playcd.domain.DiscInformation import DiscInformation
from playcd.domain.DisplayInformation import DisplayInformation
from playcd.domain.CDPlayerEnum import CDPlayerEnum
from typing import Tuple

class DisplayInformationService:
    
    def __init__(self):
        self.logging = logging.getLogger(__name__)
        self.disc_information : DiscInformation = None
        self.display_information: DisplayInformation = None

    def _sec_to_time(self, sector: int ,sector_start=0) -> Tuple[int,int]:
        sectors_per_second=75
        qt_sectors = sector - sector_start
        seconds = int(qt_sectors / sectors_per_second)
        minutes, secs = divmod(seconds, 60)
        return minutes, secs
    
    def _format_time(self, times: Tuple[int, int]) -> str:
        minutes, secs = times
        return f"{minutes:02}:{secs:02}"

    def set_disc_information(self,disc_information: DiscInformation) -> None:
        self.disc_information = disc_information

    def clear(self):
        self.display_information = None

    def update(self,lsn: int, command: CDPlayerEnum) -> None:
        if self.disc_information == None:
            raise ValueError("disc_information cannot be null. Set disc_information first")
        
        track = [ 
            t for t in self.disc_information.get_tracks() 
            if (t.get_start_lsn() <= lsn and t.get_end_lsn() >= lsn )
        ] [0]
        
        self.display_information = DisplayInformation(
            DisplayInformation.Disc(
                command=CDPlayerEnum.DISC,
                time=DisplayInformation.Time(
                    current=self._format_time(self._sec_to_time(lsn)),
                    total=self._format_time(self._sec_to_time(self.disc_information.get_total()))
                ),
                tracks= len(self.disc_information.get_tracks())
            ),
            DisplayInformation.Track(
                command=command,
                time=DisplayInformation.Time(
                    current=self._format_time(self._sec_to_time(lsn,track.get_start_lsn())),
                    total=self._format_time(self._sec_to_time(track.get_length()))
                ),
                track=track.get_number()
            )
        )

    def get(self) -> DisplayInformation:
        if self.display_information == None:
            raise ValueError("display_information cannot be null. Set update first")
        return self.display_information
        