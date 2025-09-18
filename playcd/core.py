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
from playcd.services.DisplayService import DisplayService
from playcd.services.CommandQueueService import CommandQueueService
from playcd.adapter.listeners.ApiListener import ApiListener
from playcd.adapter.listeners.KeyboardListener import KeyboardListener

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
        self.display_service = DisplayService()
        self.track_service = TrackService(
            command_queue_service= self.command_queue_service,
            cd_driver_service= self.cd_driver_service,
            control_service= self.control_service,
            display_service= self.display_service
        )
        self.play_service = PlayService(logging, self.track_service)

        self.main_uc = MainUC(
            logging= logging,
            cd_driver_service= self.cd_driver_service,
            cd_info_service= self.cd_info_service,
            create_playlist_service= self.create_playlist_service,
            is_tty_valid_service= self.is_tty_valid_service,
            play_service= self.play_service,
            display_service= self.display_service
        )

        self.close_application_uc = CloseApplicationUC(
            logging= logging,
            cd_driver_service= self.cd_driver_service,
        )

        self.api_listener = ApiListener("::",8001)
        self.keyboard_listener = KeyboardListener(self.command_queue_service)

    def listeners(self):
        self.keyboard_listener.start()
        self.api_listener.start()
        
def main(log_level, shuffle, repeatStr, only_track, track_number = 1):
    core = Core()
    try:
        logging.getLogger().setLevel(log_level)
        inputParams = InputParams(log_level, shuffle, RepeatEnum(repeatStr), only_track, track_number)
        core.listeners()
        core.main_uc.execute(inputParams)
        
    except KeyboardInterrupt:
        logging.info("Keyboard Interrupt detected! Stopping the execution!")
    finally:
        print("\n\n\nClosing the application. Please wait...")
        core.close_application_uc.execute()
        core.api_listener.stop()
        core.keyboard_listener.stop()
        logging.info("Application closed.")
