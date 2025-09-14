from playcd.libs.CDPlayer import CDPlayer
class ControlService:

    def __init__(self, logging):
        self.logging = logging

    def control_cdplayer(self, command: str, cd_player: CDPlayer):
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