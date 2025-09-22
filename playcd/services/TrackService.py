from playcd.domain.Track import Track
from playcd.libs.CDPlayer import CDPlayer
from playcd.services.ControlService import ControlService
from playcd.adapter.repository.CommandRepository import CommandRepository
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
            command_repository: CommandRepository,
            cd_driver_service: CDDriverService,
            control_service: ControlService,
            register_status_service: RegisterStatusService,
            read_disc_information_service: ReadDiscInformationService
        ):
        self.logging = logging.getLogger(__name__)
        self.command_queue_service = command_repository
        self.cd_driver_service = cd_driver_service
        self.control_service = control_service
        self.register_status_service = register_status_service
        self.read_disc_information_service = read_disc_information_service

    def _display_info_from_cdplayer(self, cd_player: CDPlayer) -> tuple[int, CDPlayerEnum]:
        if cd_player.is_paused():
            return cd_player.get_lsn(), CDPlayerEnum.PAUSE
        elif cd_player.is_stopped():
            return 0, CDPlayerEnum.STOP
        else:
            return cd_player.get_lsn(), CDPlayerEnum.PLAY

    def play(self, playlist : List[Track], position: int) -> CDPlayerEnum | None:
        
        track = playlist[position]

        self.logging.info("Starting playback of the track: %s", track.get_number())
        self.logging.info("Playing CD from %s with length of %s sectors.", track.get_start_lsn(), track.get_length())

        cd_player = CDPlayer(self.cd_driver_service.get_cd(), self.logging)
        cd_player.start(track.get_start_lsn(), track.get_length())

        disc_information = self.read_disc_information_service.execute()

        while cd_player.is_playing():

            command = self.command_queue_service.get()

            self.control_service.execute(command, cd_player)

            print_lsn, print_command = self._display_info_from_cdplayer(cd_player)

            self.register_status_service.execute(
                lsn = print_lsn, 
                command = command if command != None else print_command,
                disc_information = disc_information
            )

            if command in [CDPlayerEnum.NEXT, CDPlayerEnum.PREV]:
                self.logging.debug("TrackService: Received command to go to the %s track.", command)
                if command == CDPlayerEnum.PREV and cd_player.get_lsn() - track.get_start_lsn() > 150:
                    cd_player.jump(track.get_start_lsn())
                else:
                    self.logging.debug("Stopping current track to go to the %s track.", command)
                    cd_player.close()
                    return command
            elif command == CDPlayerEnum.QUIT:
                self.logging.info("Quitting playback as per user request.")
                raise KeyboardInterrupt
            sleep(0.5)

        self.logging.info("Playback finished.")
