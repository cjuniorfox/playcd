import logging
from playcd.domain.DisplayInformation import DisplayInformation
from playcd.domain.exceptions.ValueNotFoundError import ValueNotFoundError

class DisplayInformationRepository:

    def __init__(self):
        self.logging = logging.getLogger(__name__)
        self.display_information : DisplayInformation = None

    def set(self, display_information: DisplayInformation) -> None:
        if self.display_information == None:
            self.logging.debug("Registering display information for the first time")
        else: 
            self.logging.debug("Refreshing display information: %s", display_information)
        self.display_information = display_information
    
    def get(self) -> DisplayInformation:
        self.logging.debug("Retrieveing display information: %s", self.display_information)
        if self.display_information == None:
            raise ValueNotFoundError("The DisplayInformation is was set yet","DisplayInformationRepository.display_information is None")
        return self.display_information