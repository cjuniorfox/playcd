from playcd.libs.CDPlayer import CDPlayer
from playcd.domain.CDIconsEnum import CDIcons
from playcd.libs.ApiListener import ApiListener
from playcd.libs.KeyboardListener import KeyboardListener
class ControlService:

    def __init__(self, logging):
        self.logging = logging

    def _send_command(self, command: str, cd_player: CDPlayer):
        if command:
            if command == "pause":
                cd_player.pause()
            elif command == "stop":
                cd_player.stop()
            elif command == "play":
                cd_player.play()
            elif command == "ff":
                cd_player.fast_forward()
            elif command == "rew":
                cd_player.rewind()
            elif command == "quit":
                cd_player.close()

    def control_cdplayer(
            self, 
            api_listener : ApiListener, 
            keyboard_listener: KeyboardListener,
            cd_player: CDPlayer
        ):
        command = api_listener.get_command()
        if not command:
            command = keyboard_listener.get_command()
        
        self._send_command(command, cd_player)
        