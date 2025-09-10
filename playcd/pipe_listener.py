import threading
import os
import queue
import time

class PipeListener:
    def __init__(self, pipe_name, logging):
        self.pipe_name = pipe_name
        self.logging = logging
        self.command_queue = queue.Queue()
        self.is_running = False

    def _listener_thread_func(self):
        """The core logic that runs in the separate thread."""
        if not os.path.exists(self.pipe_name):
            os.mkfifo(self.pipe_name)
        
        self.logging.info("Listener thread started for pipe %s.",self.pipe_name)

        while self.is_running:
            try:
                with open(self.pipe_name, 'r') as pipe:
                    for line in pipe:
                        command = line.strip()
                        if command:
                            self.command_queue.put(command)
            except Exception as e:
                self.logging.error("Listener error: %s",e)
                time.sleep(1)  # Wait before trying to reconnect

    def start(self):
        """Starts the listener thread."""
        if self.is_running:
            self.logging.warn("Listener is already running.")
            return

        self.is_running = True
        self.listener_thread = threading.Thread(target=self._listener_thread_func, daemon=True)
        self.listener_thread.start()

    def get_command(self):
        """Safely retrieves a command from the queue."""
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None

    def stop(self):
        """Stops the listener and cleans up."""
        if self.is_running:
            self.is_running = False
            self.listener_thread.join(timeout=2) # Wait for the thread to finish
            if os.path.exists(self.pipe_name):
                os.remove(self.pipe_name)
                self.logging.debug("Pipe '%s' removed.",self.pipe_name)
