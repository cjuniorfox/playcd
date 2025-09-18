from playcd.libs.CDDisplay import CDDisplay
from playcd.libs.CDPlayer import CDPlayer
from playcd.domain.DiscInformation import DiscInformation
from playcd.domain.CDPlayerEnum import CDPlayerEnum
import logging

class DisplayService:
    def __init__(self):
        self.logging = logging.getLogger(__name__)

    def _display_info_from_cdplayer(self, cd_player: CDPlayer) -> tuple[int, CDPlayerEnum]:
        if cd_player.is_paused():
            return cd_player.get_lsn(), CDPlayerEnum.PAUSE
        elif cd_player.is_stopped():
            return 0, CDPlayerEnum.STOP
        else:
            return cd_player.get_lsn(), CDPlayerEnum.PLAY
        
    def set_cd_info(self, cd_info: DiscInformation):
        self.cd_info = cd_info
        self.cd_display = CDDisplay(cd_info)
        
    def write_screen(
            self,
            command: CDPlayerEnum | None,
            cd_player: CDPlayer,
            is_tty_valid: bool
        ):
        if command == None:
            lsn, command = self._display_info_from_cdplayer(cd_player)
        else:
            lsn = cd_player.get_lsn()
        if is_tty_valid:
            self.cd_display.display(lsn, command)
        else:
            self.cd_display.create_display(lsn, command)
