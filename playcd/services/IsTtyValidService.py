import logging
import os
import sys
import termios

class IsTtyValidService:
    def __init__(self):
        self.logging = logging.getLogger(__name__)

    def execute(self) -> bool:
        try:
            fd = sys.stdin.fileno()
            is_tty_valid = os.isatty(fd)
            self.logging.info(f"Is TTY valid: {is_tty_valid}")
            termios.tcgetattr(fd) # This will raise an error if TTY is not valid
            return is_tty_valid
        except Exception as e:
            self.logging.error(f"Error checking TTY validity: {e}")
            return False