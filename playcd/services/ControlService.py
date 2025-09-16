from playcd.libs.CDPlayer import CDPlayer
from playcd.domain.CDPlayerCommadsEnum import CDPlayerCommandsEnum

class ControlService:

    def __init__(self, logging):
        self.logging = logging

    def control_cdplayer(self, command: str, cd_player: CDPlayer):
        if command:
            if command == CDPlayerCommandsEnum.PAUSE:
                cd_player.pause()
            elif command == CDPlayerCommandsEnum.STOP:
                cd_player.stop()
            elif command == CDPlayerCommandsEnum.PLAY:
                cd_player.play()
            elif command == CDPlayerCommandsEnum.FF:
                cd_player.fast_forward()
            elif command == CDPlayerCommandsEnum.REW:
                cd_player.rewind()
            elif command == CDPlayerCommandsEnum.QUIT:
                cd_player.close()        