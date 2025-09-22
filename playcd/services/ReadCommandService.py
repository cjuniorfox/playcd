import logging
from playcd.adapter.repository.CommandRepository import CommandRepository
from playcd.domain.CDPlayerEnum import CDPlayerEnum

class ReadCommandService:
    def __init__(self, command_repository: CommandRepository):
        self.logging = logging.getLogger(__name__)
        self.command_repository = command_repository

    def execute(self) -> CDPlayerEnum:
        self.logging.debug("Reading command from repository")
        command = self.command_repository.get()
        if command != None:
            self.logging.debug("There's no command to be retrieved right now")
        else:
            self.logging.debug("Command retrieved: %s", command)
            return command