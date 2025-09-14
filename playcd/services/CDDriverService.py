import cdio, pycdio
import logging

class CDDriverService:

    def __init__(self,logging: logging):
        self.logging = logging

    def open_cd(self) -> cdio.Device:
        self.logging.info("Opening CD device...")
        cd = cdio.Device(driver_id=pycdio.DRIVER_UNKNOWN)
        cd.open()
        self.logging.debug("CD device opened successfully.")
        return cd