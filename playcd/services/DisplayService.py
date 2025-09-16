from playcd.libs.CDDisplay import CDDisplay
from playcd.domain.CDIconsEnum import CDIcons
from playcd.libs.CDPlayer import CDPlayer
from playcd.services.StartApiListenerService import StartApiListenerService
from playcd.domain.DiscInformation import DiscInformation
from playcd.domain.CDPlayerCommadsEnum import CDPlayerCommandsEnum

class DisplayService:
    def __init__(self, logging, api_listener_service: StartApiListenerService):
        self.logging = logging
        self.api_listener_service = api_listener_service

    def _display_info(self, command: CDPlayerCommandsEnum, lsn: int) -> tuple[int, CDIcons]:
        if command:
            if command == CDPlayerCommandsEnum.PAUSE:
                return lsn, CDIcons.PAUSE
            elif command == CDPlayerCommandsEnum.STOP:
                return 0, CDIcons.STOP
            elif command == CDPlayerCommandsEnum.PLAY:
                return lsn, CDIcons.PLAY
            elif command == CDPlayerCommandsEnum.FF:
                return lsn, CDIcons.FF
            elif command == CDPlayerCommandsEnum.REW:
                return lsn, CDIcons.REW
            elif command == CDPlayerCommandsEnum.QUIT:
                return 0, CDIcons.STOP
        else:
            return lsn, CDIcons.PLAY

    def _display_info_from_cdplayer(self, cd_player: CDPlayer) -> tuple[int, CDIcons]:
        if cd_player.is_paused():
            return cd_player.get_lsn(), CDIcons.PAUSE
        elif cd_player.is_stopped():
            return 0, CDIcons.STOP
        else:
            return cd_player.get_lsn(), CDIcons.PLAY
        
    def set_cd_info(self, cd_info: DiscInformation):
        self.cd_info = cd_info
        self.cd_display = CDDisplay(cd_info)
        
    def write_screen(
            self,
            command: CDPlayerCommandsEnum | None,
            cd_player: CDPlayer,
            is_tty_valid: bool
        ):
        
        if command in [CDPlayerCommandsEnum.PAUSE, CDPlayerCommandsEnum.STOP, CDPlayerCommandsEnum.PLAY, CDPlayerCommandsEnum.FF, CDPlayerCommandsEnum.REW, CDPlayerCommandsEnum.QUIT]:
            lsn, icon = self._display_info(command, cd_player.get_lsn())
        else:
            lsn, icon = self._display_info_from_cdplayer(cd_player)
        if is_tty_valid:
            self.cd_display.display(lsn, icon)
        else:
            self.cd_display.create_display(lsn, icon)

        self.api_listener_service.get_api_listener().set_display(self.cd_display.get_display())
