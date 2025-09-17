from playcd.libs.CDDisplay import CDDisplay
from playcd.libs.CDPlayer import CDPlayer
from playcd.services.StartApiListenerService import StartApiListenerService
from playcd.domain.DiscInformation import DiscInformation
from playcd.domain.CDPlayerEnum import CDPlayerEnum

class DisplayService:
    def __init__(self, logging, api_listener_service: StartApiListenerService):
        self.logging = logging
        self.api_listener_service = api_listener_service

    def _display_info_from_cdplayer(self, cd_player: CDPlayer) -> tuple[int, CDPlayerEnum]:
        if cd_player.is_paused():
            return cd_player.get_lsn(), CDPlayerEnum.PAUSE.icon
        elif cd_player.is_stopped():
            return 0, CDPlayerEnum.STOP.icon
        else:
            return cd_player.get_lsn(), CDPlayerEnum.PLAY.icon
        
    def set_cd_info(self, cd_info: DiscInformation):
        self.cd_info = cd_info
        self.cd_display = CDDisplay(cd_info)
        
    def write_screen(
            self,
            command: CDPlayerEnum | None,
            cd_player: CDPlayer,
            is_tty_valid: bool
        ):
        if command in [CDPlayerEnum.STOP, CDPlayerEnum.QUIT]:
            lsn = 0
        else:
            lsn = cd_player.get_lsn()
        if is_tty_valid:
            self.cd_display.display(lsn, command)
        else:
            self.cd_display.create_display(lsn, command)

        self.api_listener_service.get_api_listener().set_display(self.cd_display.get_display())
