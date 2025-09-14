import logging
from playcd.services.CDDriverService import CDDriverService
from playcd.services.CDInfoService import CDInfoService
from playcd.services.CreatePlaylistService import CreatePlaylistService
from playcd.services.StartApiListenerService import StartApiListenerService
from playcd.services.IsTtyValidService import IsTtyValidService
from playcd.services.KeyboardListenerService import KeyboardListenerService
from playcd.services.PlayService import PlayService
from playcd.domain.InputParams import InputParams
from playcd.domain.PreparedPlayback import PreparedPlayback
from playcd.libs.CDDisplay import CDDisplay
class MainUC:

    def __init__(self,logging: logging):
        self.logging = logging
        self.cd_driver_service = CDDriverService(logging)
        self.cd_info_service = CDInfoService(logging)
        self.create_playlist_service = CreatePlaylistService(logging)
        self.api_listener_service = StartApiListenerService(logging)
        self.is_tty_valid_service = IsTtyValidService(logging)
        self.keyboard_listener_service = KeyboardListenerService(logging)
        self.play_service = PlayService(logging)

    def execute(self,params : InputParams):
        self.cd = self.cd_driver_service.open_cd()
        cdinfo = self.cd_info_service.get_cd_info(self.cd)
        display = CDDisplay(cdinfo)
        playlist = self.create_playlist_service.create(cdinfo,params)
        self.api_listener_service.start("::",8001)
        is_tty_valid = self.is_tty_valid_service.execute()
        self.keyboard_listener_service.start(is_tty_valid)
        self.keyboard_listener_service.print_keyboard_commands(is_tty_valid)

        preparedPlayback = PreparedPlayback(
            self.cd,
            cdinfo,
            display,
            playlist,
            self.api_listener_service.get_api_listener(),
            self.keyboard_listener_service.get_keyboard_listener(),
            is_tty_valid
        )

        self.play_service.play(preparedPlayback, params.repeat, params.shuffle)

    def get_keyboard_listener(self):
        return self.keyboard_listener_service.get_keyboard_listener()
    
    def get_api_listener(self):
        return self.api_listener_service.get_api_listener()
    
    def get_cd(self):
        return self.cd
        
