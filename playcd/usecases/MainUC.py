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
from playcd.services.DisplayService import DisplayService


class MainUC:
    """ Main use case to run the application."""

    def __init__(
            self,
            logging: logging,
            cd_driver_service: CDDriverService,
            cd_info_service: CDInfoService,
            create_playlist_service: CreatePlaylistService,
            api_listener_service: StartApiListenerService,
            is_tty_valid_service: IsTtyValidService,
            keyboard_listener_service: KeyboardListenerService,
            play_service: PlayService,
            display_service: DisplayService
        ):
        self.logging = logging
        self.cd_driver_service = cd_driver_service
        self.cd_info_service = cd_info_service
        self.create_playlist_service = create_playlist_service
        self.api_listener_service = api_listener_service
        self.is_tty_valid_service = is_tty_valid_service
        self.keyboard_listener_service = keyboard_listener_service
        self.play_service = play_service
        self.display_service = display_service

    def execute(self,params : InputParams):
        self.cd = self.cd_driver_service.open_cd()
        cdinfo = self.cd_info_service.get_cd_info(self.cd)
        playlist = self.create_playlist_service.create(cdinfo,params)
        self.api_listener_service.start("::",8001)
        self.display_service.set_cd_info(cdinfo)
        tty_valid = self.is_tty_valid_service.execute()
        self.keyboard_listener_service.print_keyboard_commands(tty_valid)
        self.keyboard_listener_service.start(tty_valid)

        preparedPlayback = PreparedPlayback(
            cdinfo= cdinfo,
            playlist= playlist,
            tty_valid= tty_valid
        )

        self.play_service.play(preparedPlayback, params.repeat, params.shuffle)
