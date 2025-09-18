import logging
import sys
import time
import threading
from playcd.domain.DisplayInformation import DisplayInformation
from playcd.services.DisplayInformationService import DisplayInformationService
from playcd.services.IsTtyValidService import IsTtyValidService
from typing import List

class DisplayDiscInformation:

    LINES_ISNULL = "_lines is null. Call create_display first."

    def __init__(
            self, 
            display_information_service: DisplayInformationService, 
            is_tty_valid_service: IsTtyValidService
        ):
        self.logging = logging.getLogger(__name__)
        self.display_information_service = display_information_service
        self.is_tty_valid_service = is_tty_valid_service
        self.lines = None
        self.display_information : DisplayInformation = None
        self.running = False

    def _format_lines(self) -> None:
        self.lines = []

        disc_icon = self.display_information.disc.command().icon
        tracks = self.display_information.disc.tracks()
        current_disc_time = self.display_information.disc.time.current()
        total_disc_time = self.display_information.disc.time.total()

        track_icon = self.display_information.track.command().icon
        track_number = self.display_information.track.track()
        current_track_time = self.display_information.track.time.current()
        total_track_time = self.display_information.track.time.total()

        self.lines.append(f"{disc_icon} {tracks:2} {current_disc_time} / {total_disc_time}")
        self.lines.append(f"{track_icon} {track_number:2} {current_track_time} / {total_track_time}")

    def print(self) -> None:
        try:
            self.display_information = self.display_information_service.display_information()
        except ValueError:
            return
        
        self._format_lines()

        if self.lines == None:
            return
        
        car_ret = "\033[F" #\033F return the carriage to the beginning of the previous line
        data = "\n".join(["\r"+l for l in self.lines])
        printable_text = car_ret+data
        print(printable_text, flush=True, end="", file=sys.stderr)

    def listener(self):
        """Core Listener"""
        while self.running:
            print()
            time.sleep(0.5)

    def start(self):
        """Start Display Disc information"""
        if self.running:
            self.logging.warning("Display Disc Information is already running")
            return
        if not self.is_tty_valid_service.execute():
            self.logging.warning("There's no valid TTY to display disc information.")
            return
        
        self.running = True
        self.listener_thread = threading.Thread(target=self.listener, daemon=True)
        self.listener_thread.start()
        self.logging.info("Display Disc Information started")

    def stop(self):
        """Stop Display Disc information"""
        if not self.running:
            self.logging.warning("Display Disc information is not running")
            return
        self.running = False
        self.listener_thread.join(timeout=2)
        