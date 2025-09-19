import logging
import sys
import time
import threading
from typing import List, Tuple
from playcd.domain.adapter.DisplayInformation import DisplayInformation
from playcd.services.DisplayInformationService import DisplayInformationService
from playcd.services.IsTtyValidService import IsTtyValidService
from playcd.domain.CDPlayerEnum import CDPlayerEnum
from playcd.domain.mapper.DisplayInformationMapper import DisplayInformationMapper
from playcd.domain.adapter.DisplayInformation import DisplayInformation

class DisplayDiscInformation:

    def __init__(
            self, 
            display_information_service: DisplayInformationService, 
            is_tty_valid_service: IsTtyValidService
        ):
        self.logging = logging.getLogger(__name__)
        self.display_information_service = display_information_service
        self.is_tty_valid_service = is_tty_valid_service
        self.running = False

    def _convert_disc_data(self,display_information_disc: DisplayInformation.Disc) -> Tuple[str,str,int,str,str]:
        disc_command : CDPlayerEnum = display_information_disc.command
        disc_icon = disc_command.icon
        tracks = display_information_disc.tracks
        current_disc_time = display_information_disc.time.current
        total_disc_time = display_information_disc.time.total
        return disc_icon, tracks, current_disc_time, total_disc_time
    
    def _convert_track_data(self,display_information_track: DisplayInformation.Track) -> Tuple[str,str,int,str,str]:
        track_command : CDPlayerEnum = display_information_track.command
        track_icon = track_command.icon
        track_number = display_information_track.track
        current_track_time = display_information_track.time.current
        total_track_time = display_information_track.time.total
        return track_icon, track_number, current_track_time, total_track_time

    def _format_lines(self, display_information: DisplayInformation) -> List[DisplayInformation]:
        lines = []

        disc_icon, tracks, current_disc_time, total_disc_time = self._convert_disc_data(display_information.disc)
        track_icon, track_number, current_track_time, total_track_time = self._convert_track_data(display_information.track)

        lines.append(f"{disc_icon} {tracks:2} {current_disc_time} / {total_disc_time}")
        lines.append(f"{track_icon} {track_number:2} {current_track_time} / {total_track_time}")

        return lines

    def print_data(self) -> None:
        try:
            lsn, command = self.display_information_service.get_cdplayer_status()
            disc_information = self.display_information_service.get_disc_information()
            display_information = DisplayInformationMapper.map(lsn, command, disc_information)
            lines = self._format_lines(display_information)

        except ValueError:
            return

        car_ret = "\033[F" #\033F return the carriage to the beginning of the previous line
        data = "\n".join(["\r"+l for l in lines])
        printable_text = car_ret+data
        print(printable_text, flush=True, end="", file=sys.stderr)

    def listener(self):
        """Core Listener"""
        while self.running:
            self.print_data()
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

