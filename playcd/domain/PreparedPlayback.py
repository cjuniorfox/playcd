from playcd.domain.DiscInformation import DiscInformation
from playcd.domain.Track import Track
from typing import List

class PreparedPlayback:
    def __init__(
            self, 
            disc_information: DiscInformation, 
            playlist: List[Track], 
            tty_valid: bool = False
        ):
        self._disc_information = disc_information
        self._playlist = playlist
        self._tty_valid = tty_valid

    
    @property
    def disc_information(self) -> DiscInformation:
        return self._disc_information
    
    @property
    def playlist(self) -> List[Track]:
        return self._playlist
    
    @property
    def tty_valid(self) -> bool:
        return self._tty_valid
    
    def __repr__(self):
        return f"PreparedPlayback(disc_information={self._disc_information}, playlist={self._playlist}, tty_valid={self._tty_valid})"
