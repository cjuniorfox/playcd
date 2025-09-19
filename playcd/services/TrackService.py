from playcd.domain.PreparedPlayback import PreparedPlayback
from playcd.libs.CDPlayer import CDPlayer
from playcd.services.ControlService import ControlService
from playcd.services.CommandQueueService import CommandQueueService
from playcd.services.CDDriverService import CDDriverService
from playcd.services.DisplayInformationService import DisplayInformationService
from playcd.domain.CDPlayerEnum import CDPlayerEnum
import logging
from time import sleep

class TrackService:
    def __init__(
            self, 
            command_queue_service: CommandQueueService,
            cd_driver_service: CDDriverService,
            control_service: ControlService,
            display_information_service: DisplayInformationService
        ):
        self.logging = logging.getLogger(__name__)
        self.command_queue_service = command_queue_service
        self.cd_driver_service = cd_driver_service
        self.control_service = control_service
        self.display_information_service = display_information_service

    def _display_info_from_cdplayer(self, cd_player: CDPlayer) -> tuple[int, CDPlayerEnum]:
        if cd_player.is_paused():
            return cd_player.get_lsn(), CDPlayerEnum.PAUSE
        elif cd_player.is_stopped():
            return 0, CDPlayerEnum.STOP
        else:
            return cd_player.get_lsn(), CDPlayerEnum.PLAY

    def play(self, prepared_playback : PreparedPlayback, position: int) -> CDPlayerEnum | None:
        
        track = prepared_playback.get_playlist()[position]

        self.logging.info("Starting playback of the track: %s", track.get_number())
        self.logging.info("Playing CD from %s with length of %s sectors.", track.get_start_lsn(), track.get_length())
        
        cd_player = CDPlayer(self.cd_driver_service.get_cd(), self.logging)
        cd_player.start(track.get_start_lsn(), track.get_length()) 

        self.display_information_service.set_disc_information(prepared_playback.get_cdinfo())

        while cd_player.is_playing():
            
            command = self.command_queue_service.get()

            self.control_service.control_cdplayer(command, cd_player)

            print_lsn, print_command = self._display_info_from_cdplayer(cd_player)

            self.display_information_service.update(print_lsn, command if command != None else print_command)

            if command in [CDPlayerEnum.NEXT, CDPlayerEnum.PREV]:
                self.logging.debug("TrackService: Received command to go to the %s track.", command)
                if command == CDPlayerEnum.PREV and cd_player.get_lsn() - track.get_start_lsn() > 150:
                    cd_player.jump(track.get_start_lsn())
                else:
                    self.logging.debug("Stopping current track to go to the %s track.", command)
                    cd_player.close()
                    return command
            elif command == CDPlayerEnum.QUIT:
                self.display_information_service.clear()
                self.logging.info("Quitting playback as per user request.")
                raise KeyboardInterrupt
            sleep(0.1)

        self.logging.info("Playback finished.")
        self.display_information_service.clear()
