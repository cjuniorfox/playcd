from playcd.domain.PreparedPlayback import PreparedPlayback
from playcd.libs.CDPlayer import CDPlayer
from playcd.services.ControlService import ControlService
from playcd.services.DisplayService import DisplayService
from playcd.libs.ApiListener import ApiListener
from playcd.libs.KeyboardListener import KeyboardListener
from playcd.services.StartApiListenerService import StartApiListenerService
from playcd.services.KeyboardListenerService import KeyboardListenerService
from playcd.services.CDDriverService import CDDriverService
import logging
from time import sleep

class TrackService:
    def __init__(
            self, 
            logging: logging,
            api_listener_service: StartApiListenerService,
            keyboard_listener_service: KeyboardListenerService,
            cd_driver_service: CDDriverService,
            control_service: ControlService,
            display_service: DisplayService
        ):
        self.logging = logging
        self.cd_driver_service = cd_driver_service
        self.api_listener_service = api_listener_service
        self.keyboard_listener_service = keyboard_listener_service
        self.control_service = control_service
        self.display_service = display_service

    def _get_command(self) -> str:
        command = self.api_listener_service.get_api_listener().get_command()
        if not command:
            command = self.keyboard_listener_service.get_keyboard_listener().get_command()
        return command

    def play(self, preparedPlayback : PreparedPlayback, position: int) -> str:
        
        track = preparedPlayback.get_playlist()[position]

        self.logging.info("Starting playback of the track: %s", track.get_number())
        self.logging.info("Playing CD from %s with length of %s sectors.", track.get_start_lsn(), track.get_length())
        
        cd_player = CDPlayer(self.cd_driver_service.get_cd(), self.logging)
        cd_player.start(track.get_start_lsn(), track.get_length()) 

        while cd_player.is_playing():
            
            command = self._get_command()

            self.control_service.control_cdplayer(command, cd_player)
            
            self.display_service.write_screen(
                command,
                cd_player, 
                preparedPlayback.is_tty_valid()
            )

            if command in ["next", "prev"]:
                self.logging.debug("TrackService: Received command to go to the %s track.", command)
                if command == "prev" and cd_player.get_lsn() - track.get_start_lsn() > 150:
                    cd_player.jump(track.get_start_lsn())
                else:
                    self.logging.debug("Stopping current track to go to the %s track.", command)
                    cd_player.close()
                    return command
            elif command == "quit":
                self.logging.info("Quitting playback as per user request.")
                raise KeyboardInterrupt
            sleep(0.1)

        self.logging.info("Playback finished.")
