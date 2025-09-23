import cdio, pycdio
import logging

class CDDriverService:

    def __init__(self):
        self.logging = logging.getLogger(__name__)
        self.cd = None

    def open_cd(self) -> cdio.Device:
        self.logging.info("Opening CD device...")
        self.cd = cdio.Device(driver_id=pycdio.DRIVER_UNKNOWN)
        self.cd.open()
        self.logging.debug("CD device opened successfully.")
        return self.cd
    
    def get_cd(self) -> cdio.Device:
        return self.cd