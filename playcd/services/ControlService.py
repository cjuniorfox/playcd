from playcd.libs.CDPlayer import CDPlayer
from playcd.domain.CDPlayerEnum import CDPlayerEnum

class ControlService:

    def __init__(self, logging):
        self.logging = logging

    def execute(self, command: str, cd_player: CDPlayer):
        if command:
            if command == CDPlayerEnum.PAUSE:
                cd_player.pause()
            elif command == CDPlayerEnum.STOP:
                cd_player.stop()
            elif command == CDPlayerEnum.PLAY:
                cd_player.play()
            elif command == CDPlayerEnum.FF:
                cd_player.fast_forward()
            elif command == CDPlayerEnum.REW:
                cd_player.rewind()
            elif command == CDPlayerEnum.QUIT:
                cd_player.close()        