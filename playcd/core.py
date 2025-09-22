import logging
from playcd.domain.InputParams import InputParams
from playcd.usecases.MainUC import MainUC
from playcd.usecases.CloseApplicationUC import CloseApplicationUC
from playcd.domain.RepeatEnum import RepeatEnum

from playcd.services.CDDriverService import CDDriverService
from playcd.services.RegisterDiscInformationService import RegisterDiscInformationService
from playcd.services.ReadDiscInformationService import ReadDiscInformationService
from playcd.services.CreatePlaylistService import CreatePlaylistService
from playcd.services.IsTtyValidService import IsTtyValidService
from playcd.services.PlayService import PlayService
from playcd.services.TrackService import TrackService
from playcd.services.ControlService import ControlService
from playcd.adapter.repository.CommandRepository import CommandRepository
from playcd.services.RegisterStatusService import RegisterStatusService
from playcd.adapter.listeners.ApiListener import ApiListener
from playcd.adapter.listeners.KeyboardListener import KeyboardListener
from playcd.adapter.tty.KeyboardCommands import KeyboardCommands
from playcd.adapter.tty.DisplayDiscInformationTty import DisplayDiscInformationTty
from playcd.adapter.repository.DiscInformationRepository import DiscInformationRepository
from playcd.adapter.repository.DisplayInformationRepository import DisplayInformationRepository
from playcd.services.ReadStatusService import ReadStatusService

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

class Core:
    def __init__(self):
        self.disc_information_repository = DiscInformationRepository()
        self.display_information_repository = DisplayInformationRepository()
        self.command_repository = CommandRepository()
        self.cd_driver_service = CDDriverService(logging)
        self.register_disc_information_service = RegisterDiscInformationService(self.disc_information_repository)
        self.read_disc_information_service = ReadDiscInformationService(self.disc_information_repository)
        self.create_playlist_service = CreatePlaylistService(logging)
        self.is_tty_valid_service = IsTtyValidService(logging)
        self.control_service = ControlService(logging)
        self.register_status_service = RegisterStatusService(self.display_information_repository)
        self.read_status_service = ReadStatusService(self.display_information_repository)
        self.track_service = TrackService(
            command_repository= self.command_repository,
            cd_driver_service= self.cd_driver_service,
            control_service= self.control_service,
            register_status_service= self.register_status_service,
            read_disc_information_service=self.read_disc_information_service
        )
        self.play_service = PlayService(logging, self.track_service)

        self.main_uc = MainUC(
            cd_driver_service= self.cd_driver_service,
            register_disc_information_service= self.register_disc_information_service,
            create_playlist_service= self.create_playlist_service,
            is_tty_valid_service= self.is_tty_valid_service,
            play_service= self.play_service,
        )

        self.close_application_uc = CloseApplicationUC(
            logging= logging,
            cd_driver_service= self.cd_driver_service,
        )

        self.api_listener = ApiListener(self.command_repository,"::",8001)
        self.keyboard_listener = KeyboardListener(self.command_repository)
        self.keyboard_commands = KeyboardCommands(self.is_tty_valid_service)
        self.display_disc_information = DisplayDiscInformationTty(self.read_status_service, self.is_tty_valid_service)

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
        core.tty()
        core.listeners()
        core.main_uc.execute(inputParams)
        
    except KeyboardInterrupt:
        logging.info("Keyboard Interrupt detected! Stopping the execution!")
    finally:
        core.display_disc_information.stop()
        print("\n\rClosing the application. Please wait...")
        core.api_listener.stop()
        core.keyboard_listener.stop()
        core.close_application_uc.execute()
        logging.info("Application closed.")
