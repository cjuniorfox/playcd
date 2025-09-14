from playcd.domain.PreparedPlayback import PreparedPlayback
from playcd.libs.CDPlayer import CDPlayer
from playcd.services.ControlService import ControlService
from playcd.services.DisplayService import DisplayService
from playcd.libs.ApiListener import ApiListener
from playcd.libs.KeyboardListener import KeyboardListener
from time import sleep

class TrackService:
    def __init__(self, logging):
        self.logging = logging
        self.control_service = ControlService(logging)
        self.display_service = DisplayService(logging)

    def _get_command(self, api_listener: ApiListener, keyboard_listener: KeyboardListener) -> str:
        command = api_listener.get_command()
        if not command:
            command = keyboard_listener.get_command()
        return command

    def play(self, preparedPlayback : PreparedPlayback, position: int) -> str:

        api_listener = preparedPlayback.get_api_listener()
        keyboard_listener = preparedPlayback.get_keyboard_listener()
        
        track = preparedPlayback.get_playlist()[position]

        self.logging.info("Starting playback of the track: %s", track.get_number())
        self.logging.info("Playing CD from %s with length of %s sectors.", track.get_start_lsn(), track.get_length())
        
        cd_player = CDPlayer(preparedPlayback.get_cd(), self.logging)
        cd_player.start(track.get_start_lsn(), track.get_length()) 

        while cd_player.is_playing():
            
            command = self._get_command(api_listener, keyboard_listener)

            self.control_service.control_cdplayer(command, cd_player)
            
            self.display_service.write_screen(
                command,
                api_listener, 
                cd_player, 
                preparedPlayback.get_display(), 
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
