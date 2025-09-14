from playcd.libs.CDDisplay import CDDisplay
from playcd.libs.ApiListener import ApiListener
from playcd.domain.CDIconsEnum import CDIcons
from playcd.libs.CDPlayer import CDPlayer

class DisplayService:
    def __init__(self, logging):
        self.logging = logging

    def _display_info(self, command: str, lsn: int, display: CDDisplay) -> tuple[int, CDIcons]:
        if command:
            if command == "pause":
                return lsn, CDIcons.PAUSE
            elif command == "stop":
                return 0, CDIcons.STOP
            elif command == "play":
                return lsn, CDIcons.PLAY
            elif command == "ff":
                return lsn, CDIcons.FF
            elif command == "rew":
                return lsn, CDIcons.REW
            elif command == "quit":
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

    def write_screen(
            self,
            command: str,
            api_listener: ApiListener, 
            cd_player: CDPlayer,
            display: CDDisplay,
            is_tty_valid: bool
        ):
        
        if command in ["pause", "stop", "play", "ff", "rew", "quit"]:
            lsn, icon = self._display_info(command, cd_player.get_lsn(), display)
        else:
            lsn, icon = self._display_info_from_cdplayer(cd_player)
        if is_tty_valid:
            display.display(lsn, icon)
        else:
            display.create_display(lsn, icon)

        api_listener.set_display(display.get_display())
