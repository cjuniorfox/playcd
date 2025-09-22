from playcd.domain.DiscInformation import DiscInformation
from playcd.adapter.repository.DiscInformationRepository import DiscInformationRepository
import logging

class ReadDiscInformationService:
    def __init__(self, disc_information_repository: DiscInformationRepository):
        self.logging = logging.getLogger(__name__)
        self.disc_information_repository = disc_information_repository

    def execute(self) -> DiscInformation:
        self.logging.info("Retrieving disc information from repository")
        disc_information = self.disc_information_repository.get()
        self.logging.debug("Disc information retrieved: %s", disc_information)
        return disc_information
