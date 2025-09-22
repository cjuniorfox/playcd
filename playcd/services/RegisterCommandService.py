import logging
from playcd.domain.CDPlayerEnum import CDPlayerEnum
from playcd.adapter.repository.CommandRepository import CommandRepository

class RegisterCommandService:

    def __init__(self, command_repository: CommandRepository):
        self.logging = logging.getLogger(__name__)
        self.command_repository = command_repository

    def execute(self, command: CDPlayerEnum) -> None:
        self.logging.info("Sending command %s to the repository queue", command)
        self.command_repository.clear()
        self.command_repository.put(command)
        self.logging.debug("Command sucessfully registered")