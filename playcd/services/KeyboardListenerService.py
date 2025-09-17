import logging
from playcd.libs.KeyboardListener import KeyboardListener
from playcd.domain.CDPlayerEnum import CDPlayerEnum

class KeyboardListenerService:
    def __init__(self, logging: logging) -> None:
        self.logging = logging
        self.keyboard_listener = KeyboardListener(self.logging)

    def start(self, is_tty_valid: bool) -> None:
        self.logging.info("Starting API listener service...")
        if not is_tty_valid:
            self.logging.warning("stdout is redirected or invalid. Keyboard listener not enable on this environment")
            return

        self.keyboard_listener.start()
        self.logging.info("API listener service started.")

    def get_keyboard_listener(self) -> KeyboardListener:
        return self.keyboard_listener

    def print_keyboard_commands(self, is_tty_valid: bool) -> None:
        if not is_tty_valid:
            return

        keys=[i.key_display for i in list(CDPlayerEnum) if i.key_display != None]
        # Add extra spaces around the pause icon for better alignment
        icons=["  " + i.icon + "  " if i.command == "pause" else i.icon for i in list(CDPlayerEnum) if i.key_display != None]
    
        print("Keyboard Commands:")
        print(" "," ".join(keys))
        print("  ","   ".join(icons),"\n")
