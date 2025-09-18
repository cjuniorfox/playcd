import logging
from playcd.domain.InputParams import InputParams
from playcd.usecases.MainUC import MainUC
from playcd.usecases.CloseApplicationUC import CloseApplicationUC
from playcd.domain.RepeatEnum import RepeatEnum

from playcd.services.CDDriverService import CDDriverService
from playcd.services.CDInfoService import CDInfoService
from playcd.services.CreatePlaylistService import CreatePlaylistService
from playcd.services.IsTtyValidService import IsTtyValidService
from playcd.services.PlayService import PlayService
from playcd.services.TrackService import TrackService
from playcd.services.ControlService import ControlService
from playcd.services.CommandQueueService import CommandQueueService
from playcd.services.DisplayInformationService import DisplayInformationService
from playcd.adapter.listeners.ApiListener import ApiListener
from playcd.adapter.listeners.KeyboardListener import KeyboardListener
from playcd.adapter.tty.KeyboardCommands import KeyboardCommands
from playcd.adapter.tty.DisplayDiscInformation import DisplayDiscInformation

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

class Core:
    def __init__(self):
        self.command_queue_service = CommandQueueService()
        self.cd_driver_service = CDDriverService(logging)
        self.cd_info_service = CDInfoService(logging)
        self.create_playlist_service = CreatePlaylistService(logging)
        self.is_tty_valid_service = IsTtyValidService(logging)
        self.control_service = ControlService(logging)
        self.display_information_service = DisplayInformationService()
        self.track_service = TrackService(
            command_queue_service= self.command_queue_service,
            cd_driver_service= self.cd_driver_service,
            control_service= self.control_service,
            display_information_service= self.display_information_service
        )
        self.play_service = PlayService(logging, self.track_service)

        self.main_uc = MainUC(
            cd_driver_service= self.cd_driver_service,
            cd_info_service= self.cd_info_service,
            create_playlist_service= self.create_playlist_service,
            is_tty_valid_service= self.is_tty_valid_service,
            play_service= self.play_service,
        )

        self.close_application_uc = CloseApplicationUC(
            logging= logging,
            cd_driver_service= self.cd_driver_service,
        )

        self.api_listener = ApiListener(self.command_queue_service,"::",8001)
        self.keyboard_listener = KeyboardListener(self.command_queue_service)
        self.keyboard_commands = KeyboardCommands(self.is_tty_valid_service)
        self.display_disc_information = DisplayDiscInformation(self.display_information_service, self.is_tty_valid_service)

    def listeners(self):
        self.keyboard_listener.start()
        self.api_listener.start()
        self.display_disc_information.start()
    
    def tty(self):
        self.keyboard_commands.print()
        
def main(log_level, shuffle, repeatStr, only_track, track_number = 1):
    core = Core()
    try:
        logging.getLogger().setLevel(log_level)
        inputParams = InputParams(log_level, shuffle, RepeatEnum(repeatStr), only_track, track_number)
        core.listeners()
        core.tty()
        core.main_uc.execute(inputParams)
        
    except KeyboardInterrupt:
        logging.info("Keyboard Interrupt detected! Stopping the execution!")
    finally:
        print("\nClosing the application. Please wait...")
        core.close_application_uc.execute()
        core.api_listener.stop()
        core.keyboard_listener.stop()
        logging.info("Application closed.")
