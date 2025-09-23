import logging

class IsTtyValidService:
    def __init__(self):
        self.logging = logging.getLogger(__name__)

    def execute(self) -> bool:
        import os
        import sys
        try:
            is_tty_valid = os.isatty(sys.stdout.fileno())
            self.logging.info(f"Is TTY valid: {is_tty_valid}")
            return is_tty_valid
        except Exception as e:
            self.logging.error(f"Error checking TTY validity: {e}")
            return False