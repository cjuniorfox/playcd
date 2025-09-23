from playcd.domain.Track import Track
from playcd.libs.CDPlayer import CDPlayer
from playcd.services.ControlService import ControlService
from playcd.services.ReadCommandService import ReadCommandService
from playcd.services.CDDriverService import CDDriverService
from playcd.services.RegisterStatusService import RegisterStatusService
from playcd.services.ReadDiscInformationService import ReadDiscInformationService
from playcd.domain.CDPlayerEnum import CDPlayerEnum
import logging
from typing import List

from time import sleep

class TrackService:
    def __init__(
            self, 
            read_command_service: ReadCommandService,
            cd_driver_service: CDDriverService,
            control_service: ControlService,
            register_status_service: RegisterStatusService,
            read_disc_information_service: ReadDiscInformationService
        ):
        self.logging = logging.getLogger(__name__)
        self.read_command_service = read_command_service
        self.cd_driver_service = cd_driver_service
        self.control_service = control_service
        self.register_status_service = register_status_service
        self.read_disc_information_service = read_disc_information_service
        self.cd_player = None
        
    def _get_command_from_cdplayer_status(self) -> CDPlayerEnum:
        if self.cd_player.is_paused():
            return CDPlayerEnum.PAUSE
        elif self.cd_player.is_stopped():
            return CDPlayerEnum.STOP
        else:
            return CDPlayerEnum.PLAY
        
    def _restart_track(self, command: CDPlayerEnum, track: Track) -> bool:
        if command == CDPlayerEnum.PREV and self.cd_player.get_lsn() - track.get_start_lsn() > 150:
            self.cd_player.jump(track.get_start_lsn())
            return True
        return False
    
    def _jump_track(self, command, track) -> CDPlayerEnum | None:
        self.logging.debug("TrackService: Received command to go to the %s track.", command)
        restarted = self._restart_track(command, track)
        if not restarted:
            self.logging.debug("Stopping current track to go to the %s track.", command)
            self.cd_player.close()
            return command
    
    def _start_cd_player(self, track: Track) -> None:
        self.cd_driver_service.open_cd()
        self.cd_player = CDPlayer(self.cd_driver_service.get_cd(), self.logging)
        self.logging.info("Starting playback of the track: %s", track.get_number())
        self.logging.info("Playing CD from %s with length of %s sectors.", track.get_start_lsn(), track.get_length())
        self.cd_player.start(track.get_start_lsn(), track.get_length())
        
    def play(self, playlist : List[Track], track_count: int) -> CDPlayerEnum | None:
        
        track = playlist[track_count]
        self._start_cd_player(track)

        disc_information = self.read_disc_information_service.execute()

        while self.cd_player.is_playing():

            command = self.read_command_service.execute()
            self.control_service.execute(command, self.cd_player)
            cdplayer_status = self._get_command_from_cdplayer_status()

            self.register_status_service.execute(
                lsn = self.cd_player.get_lsn(),
                command = command if command != None else cdplayer_status,
                disc_information = disc_information
            )

            if command in [CDPlayerEnum.NEXT, CDPlayerEnum.PREV]:
                return_command = self._jump_track(command, track)
                if return_command:
                    return return_command
            elif command == CDPlayerEnum.QUIT:
                self.logging.info("Quitting playback as per user request.")
                raise KeyboardInterrupt
            sleep(0.5)
        
        self.cd_player.close()
        self.logging.info("Playback finished.")
