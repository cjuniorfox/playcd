import sys
from typing import List, Tuple
from playcd.domain.CDIconsEnum import CDIcons
from playcd.domain.DiscInformation import DiscInformation
from playcd.domain.Track import Track

class CDDisplay:
    
    LINES_ISNULL = "_lines is null. Call create_display first."
    def __init__(self,cdinfo: DiscInformation):
        self.cdinfo = cdinfo
        self._lines = None
        self._string = None

    def _sec_to_time(self, sector: int ,sector_start=0) -> Tuple[int,int]:
        sectors_per_second=75
        qt_sectors = sector - sector_start
        seconds = int(qt_sectors / sectors_per_second)
        minutes, secs = divmod(seconds, 60)
        return minutes, secs
    
    def _format_time(self, times: Tuple[int, int]) -> str:
        minutes, secs = times
        return f"{minutes:02}:{secs:02}"
    
    def _assemble_display_string(self) -> None:
        if self._lines == None:
            raise ValueError(self.LINES_ISNULL)
        car_ret = "\033[F" #\033F return the carriage to the beginning of the previous line
        data = "\n".join(["\r"+l for l in self._lines])
        self._string = car_ret+data

    def create_display(self, lsn: int ,icon = CDIcons.PLAY) -> None:
        tracks = self.cdinfo.get_tracks()
        count = len(tracks)
        track = [ t for t in tracks if (t.get_start_lsn() <= lsn and t.get_end_lsn() >= lsn )] [0]
        number = track.get_number()
    
        track_time = self._format_time(self._sec_to_time(lsn,track.get_start_lsn()))
        track_total = self._format_time(self._sec_to_time(track.get_length()))
        disc_time = self._format_time(self._sec_to_time(lsn))
        disc_total = self._format_time(self._sec_to_time(self.cdinfo.get_total()))
        
        lines = []
        self._display = {
                            "disc": {
                                "operaton": CDIcons.DISC.name.lower(),
                                "icon": CDIcons.DISC,
                                "tracks" : count,
                                "time": { "current": disc_time, "total": disc_total }
                            },
                            "track": {
                                "operation" : icon.name.lower(),
                                "icon" : icon,
                                "track" : number,
                                "time" : { "current" : track_time, "total" : track_total }
                            }
                        }
    
        lines.append(f"{CDIcons.DISC} {count:2} {disc_time} / {disc_total}")
        lines.append(f"{icon} {number:2} {track_time} / {track_total}")
    
        self._lines = lines

    def print_display(self) -> None:
        if self._lines == None:
            raise ValueError(self.LINES_ISNULL)
        self._assemble_display_string()
        print(self._string,flush=True, end="", file=sys.stderr)

    def display(self, sector: int, icon = CDIcons.PLAY) -> None:
        self.create_display(sector, icon)
        self._assemble_display_string()
        self.print_display()

    def get_display(self):
        return self._display
    
    def display_lines(self, sector: int, icon = CDIcons.PLAY) -> List[str]:
        self.create_display(sector,icon)
        return self._lines
