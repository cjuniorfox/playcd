import logging
from playcd.services.CDDriverService import CDDriverService
from playcd.services.RegisterDiscInformationService import RegisterDiscInformationService
from playcd.services.CreatePlaylistService import CreatePlaylistService
from playcd.services.JumpTrackService import JumpTrackService
from playcd.services.TrackService import TrackService
from playcd.domain.InputParams import InputParams


class MainUC:
    """ Main use case to run the application."""

    def __init__(
            self,
            cd_driver_service: CDDriverService,
            register_disc_information_service: RegisterDiscInformationService,
            create_playlist_service: CreatePlaylistService,
            jump_track_service: JumpTrackService,
            track_service: TrackService,
        ):
        self.logging = logging.getLogger(__name__)
        self.cd_driver_service = cd_driver_service
        self.register_disc_information_service = register_disc_information_service
        self.create_playlist_service = create_playlist_service
        self.jump_track_service = jump_track_service
        self.track_service = track_service

    def execute(self,params : InputParams):
        self.cd = self.cd_driver_service.open_cd()
        disc_information = self.register_disc_information_service.register(self.cd)
        playlist = self.create_playlist_service.create(disc_information,params)
        track_count = 0
        self.logging.info("Prepared playback with %d tracks.", track_count)
        while track_count < len(playlist):
            command = self.track_service.play(playlist, track_count)
            track_count = self.jump_track_service.execute(command, params.repeat, track_count)