import logging
from playcd.services.IsTtyValidService import IsTtyValidService
from playcd.domain.CDPlayerEnum import CDPlayerEnum

class KeyboardCommands:
    
    def __init__(self,is_tty_valid_service: IsTtyValidService):
        self.logging = logging.getLogger(__name__)
        self.is_tty_valid_service = is_tty_valid_service
        
    def print(self) -> None:
        if not self.is_tty_valid_service.execute():
            return
        keys=[i.key_display for i in list(CDPlayerEnum) if i.key_display != None]
        # Add extra spaces around the pause icon for better alignment
        icons=["  " + i.icon + "  " if i.command == "pause" else i.icon for i in list(CDPlayerEnum) if i.key_display != None]
    
        print("Keyboard Commands:")
        print(" "," ".join(keys))
        print("  ","   ".join(icons)+"\n")
