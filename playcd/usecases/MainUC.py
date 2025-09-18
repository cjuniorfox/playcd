import logging
from playcd.services.CDDriverService import CDDriverService
from playcd.services.CDInfoService import CDInfoService
from playcd.services.CreatePlaylistService import CreatePlaylistService
from playcd.services.IsTtyValidService import IsTtyValidService
from playcd.services.PlayService import PlayService
from playcd.domain.InputParams import InputParams
from playcd.domain.PreparedPlayback import PreparedPlayback


class MainUC:
    """ Main use case to run the application."""

    def __init__(
            self,
            cd_driver_service: CDDriverService,
            cd_info_service: CDInfoService,
            create_playlist_service: CreatePlaylistService,
            is_tty_valid_service: IsTtyValidService,
            play_service: PlayService
        ):
        self.logging = logging.getLogger(__name__)
        self.cd_driver_service = cd_driver_service
        self.cd_info_service = cd_info_service
        self.create_playlist_service = create_playlist_service
        self.is_tty_valid_service = is_tty_valid_service
        self.play_service = play_service

    def execute(self,params : InputParams):
        self.cd = self.cd_driver_service.open_cd()
        cdinfo = self.cd_info_service.get_cd_info(self.cd)
        playlist = self.create_playlist_service.create(cdinfo,params)
        tty_valid = self.is_tty_valid_service.execute()

        preparedPlayback = PreparedPlayback(
            cdinfo= cdinfo,
            playlist= playlist,
            tty_valid= tty_valid
        )

        self.play_service.play(preparedPlayback, params.repeat, params.shuffle)
