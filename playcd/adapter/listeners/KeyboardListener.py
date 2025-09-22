import sys
import termios
import tty
import logging
import threading
import time
from playcd.domain.CDPlayerEnum import CDPlayerEnum
from playcd.services.RegisterCommandService import RegisterCommandService

class KeyboardListener:
    def __init__(self, register_command_service : RegisterCommandService):
        self.register_command_service = register_command_service
        self.is_running = False
        self.old_console_settings = None
        self.logging = logging.getLogger(__name__)

    def _key_to_command(self, key: str):
        """Maps a key press to a command string."""
        try:
            if ord(key) == 3:
                return CDPlayerEnum.QUIT
            command = CDPlayerEnum.from_key(key)
            logging.debug("KeyboardListener: key %s pressed for command: %s.", key, command)
            return command
        except KeyError:
            self.logging.warning("Unable to parse a command for the key %s",key)
            return None
    

    def _getch(self):
        """Reads a single character from stdin without echoing it to the screen."""
        fd = sys.stdin.fileno()
        try:
            self.old_console_settings = termios.tcgetattr(fd)
        except termios.error as e:
            self.logging.debug("Exception throw trying to enable keyboard input %s",e)
            self.logging.warning("Keyboard input not available in this environment")
            self.stop()
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, self.old_console_settings)
        return ch
    
    def listener(self):
        """Core listener"""
        self.logging.info("Keyboard listener started")
        try:
            while self.is_running:
                key = self._getch()
                command = self._key_to_command(key)
                if command:
                    self.register_command_service.execute(command)
                time.sleep(0.2)
        except KeyboardInterrupt:
            self.stop()
    
    def start(self):
        """Start the keyboard listener"""
        if self.is_running:
            self.logging.warning("Keyboard listener is already running")
            return

        self.is_running = True
        self.listener_thread = threading.Thread(target=self.listener, daemon=True)
        self.listener_thread.start()
        self.logging.info("Keyboard listener started")

    def stop(self):
        """Stop the keyboard listener"""
        if not self.is_running:
            self.logging.warning("Keyboard listener is not running")
            return
        self.is_running = False
        self.listener_thread.join(timeout=2)
        if self.old_console_settings != None:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.old_console_settings)
        self.logging.info("Keyboard listener stopped")
