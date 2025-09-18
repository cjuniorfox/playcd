from playcd.domain.DiscInformation import DiscInformation
from playcd.domain.Track import Track
from typing import List

class PreparedPlayback:
    def __init__(
            self, 
            cdinfo: DiscInformation, 
            playlist: List[Track], 
            tty_valid: bool = False
        ):
        self.cdinfo = cdinfo
        self.playlist = playlist
        self.tty_valid = tty_valid

    
    def get_cdinfo(self) -> DiscInformation:
        return self.cdinfo
    
    def get_playlist(self) -> List[Track]:
        return self.playlist
    
    def is_tty_valid(self) -> bool:
        return self.tty_valid
    
    def __repr__(self):
        return f"PreparedPlayback(cdinfo={self.cdinfo}, playlist={self.playlist}, tty_valid={self.tty_valid})"
