import logging
from playcd.domain.DiscInformation import DiscInformation
from playcd.domain.exceptions.ValueNotFoundError import ValueNotFoundError

class DiscInformationRepository:
    def __init__(self):
        self.logging = logging.getLogger(__name__)
        self.disc_information: DiscInformation = None

    def set(self, disc_information: DiscInformation) -> None:
        if self.disc_information == None:
            self.logging.debug("Setting disc information for the first time")
        else:
            self.logging.debug("Refreshing disc information. from: %s to %s", self.disc_information, disc_information)
        self.disc_information = disc_information

    def get(self) -> DiscInformation:
        self.logging.debug("Retrieving disc information %s", self.disc_information)
        if self.disc_information == None:
            raise ValueNotFoundError("The disc information was not set yet","DiscInformationRepository.disc_information is None")
        return self.disc_information