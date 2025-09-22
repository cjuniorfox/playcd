from playcd.domain.CDPlayerEnum import CDPlayerEnum
import queue
import logging

class CommandRepository:

    def __init__(self):
        self.logging = logging.getLogger(__name__)
        self.commands = queue.Queue()
        pass

    def clear(self) -> None:
        self.commands.queue.clear()

    def put(self,command: CDPlayerEnum) -> None:
        self.logging.debug("Adding the command %s to the queue", command)
        self.commands.put(command)

    def get(self) -> CDPlayerEnum:
        """Retrieves command from queue"""
        try:
            command = self.commands.get_nowait()
            self.logging.debug("Retrieving command %s from the queue", command)
            return command
        except queue.Empty:
            return None