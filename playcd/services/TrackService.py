from playcd.domain.PreparedPlayback import PreparedPlayback
from playcd.libs.CDPlayer import CDPlayer
from playcd.services.ControlService import ControlService
from playcd.services.DisplayService import DisplayService
from playcd.services.CommandQueueService import CommandQueueService
from playcd.services.CDDriverService import CDDriverService
from playcd.domain.CDPlayerEnum import CDPlayerEnum
import logging
from time import sleep

class TrackService:
    def __init__(
            self, 
            command_queue_service: CommandQueueService,
            cd_driver_service: CDDriverService,
            control_service: ControlService,
            display_service: DisplayService
        ):
        self.logging = logging.getLogger(__name__)
        self.command_queue_service = command_queue_service
        self.cd_driver_service = cd_driver_service
        self.control_service = control_service
        self.display_service = display_service

   

    def play(self, preparedPlayback : PreparedPlayback, position: int) -> CDPlayerEnum | None:
        
        track = preparedPlayback.get_playlist()[position]

        self.logging.info("Starting playback of the track: %s", track.get_number())
        self.logging.info("Playing CD from %s with length of %s sectors.", track.get_start_lsn(), track.get_length())
        
        cd_player = CDPlayer(self.cd_driver_service.get_cd(), self.logging)
        cd_player.start(track.get_start_lsn(), track.get_length()) 

        while cd_player.is_playing():
            
            command = self.command_queue_service.get()

            self.control_service.control_cdplayer(command, cd_player)
            
            self.display_service.write_screen(
                command,
                cd_player, 
                preparedPlayback.is_tty_valid()
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
            sleep(0.1)

        self.logging.info("Playback finished.")
