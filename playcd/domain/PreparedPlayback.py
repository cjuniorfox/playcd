import cdio
from playcd.domain.DiscInformation import DiscInformation
from playcd.libs.CDDisplay import CDDisplay
from playcd.libs.ApiListener import ApiListener
from playcd.libs.KeyboardListener import KeyboardListener
from playcd.domain.Track import Track
from typing import List

class PreparedPlayback:
    def __init__(
            self, 
            cd: cdio.Device, 
            cdinfo: DiscInformation, 
            display : CDDisplay, 
            playlist: List[Track], 
            api_listener: ApiListener, 
            keyboard_listener: KeyboardListener,
            is_tty_valid: bool = False
        ):
        self.cd = cd
        self.cdinfo = cdinfo
        self.display = display
        self.playlist = playlist
        self.api_listener = api_listener
        self.keyboard_listener = keyboard_listener

    def get_cd(self) -> cdio.Device:
        return self.cd
    
    def get_cdinfo(self) -> DiscInformation:
        return self.cdinfo
    
    def get_display(self) -> CDDisplay:
        return self.display
    
    def get_playlist(self) -> List[Track]:
        return self.playlist
    
    def get_api_listener(self) -> ApiListener:
        return self.api_listener
    
    def get_keyboard_listener(self) -> KeyboardListener:
        return self.keyboard_listener
    
    def is_tty_valid(self) -> bool:
        return self.is_tty_valid
    
    def __repr__(self):
        return f"PreparedPlayback(cd={self.cd}, cdinfo={self.cdinfo}, display={self.display}, playlist={self.playlist}, api_listener={self.api_listener}, keyboard_listener={self.keyboard_listener})"
