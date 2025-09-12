import threading
import sys
import termios
import tty
import queue
import time

class KeyboardListener:
    def __init__(self,logging):
        self.logging = logging
        self.command_queue = queue.Queue()
        self.is_running = False
        self.old_settings = None
    def _listener_thread_func(self):
        """Core listener"""
        self.logging.info("Keyboard listener started")

        try:
            while self.is_running:
                command = self._get_command_from_key()
                if command:
                    self.command_queue.queue.clear()
                    self.command_queue.put(command)
                time.sleep(0.1)
        except KeyboardInterrupt:
            this.stop()

    def _getch(self):
        """Reads a single character from stdin without echoing it to the screen."""
        fd = sys.stdin.fileno()
        try:
            self.old_settings = termios.tcgetattr(fd)
        except termios.error as e:
            self.logging.debug("Exception throw trying to enable keyboard input %s",e)
            self.logging.warn("Keyboard input not available in this environment")
            quit()

        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, self.old_settings)
        return ch
    
    def _get_command_from_key(self):
        key = self._getch()
        self.logging.debug("%s pressed",key)
        if key == 'q':
            return "rewind"
        elif key == 'a':
            return "prev"
        elif key == 'd':
            return "next"
        elif key == "e":
            return "fast forward"
        elif key == ' ':
            return "pause"
        elif key == 's':
            return "stop"
        elif key == 'w':
            return "play"
        elif ord(key) == 3:
            return "quit"

    def start(self):
        """Start the keyboard listener thread"""
        if self.is_running:
            self.logging.warn("Keyboard listener is already running")
            return
        self.is_running = True
        self.listener_thread = threading.Thread(target=self._listener_thread_func, daemon=True)
        self.listener_thread.start()

    def get_command(self):
        """Retrieves command from queue"""
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.listener_thread.join(timeout=2)
            if self.old_settings != None:
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.old_settings)
