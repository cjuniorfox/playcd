import logging
from playcd.domain.InputParams import InputParams
from playcd.usecases.MainUC import MainUC
from playcd.usecases.CloseApplicationUC import CloseApplicationUC
from playcd.domain.RepeatEnum import RepeatEnum

from playcd.services.CDDriverService import CDDriverService
from playcd.services.CDInfoService import CDInfoService
from playcd.services.CreatePlaylistService import CreatePlaylistService
from playcd.services.StartApiListenerService import StartApiListenerService
from playcd.services.IsTtyValidService import IsTtyValidService
from playcd.services.KeyboardListenerService import KeyboardListenerService
from playcd.services.PlayService import PlayService
from playcd.services.TrackService import TrackService
from playcd.services.ControlService import ControlService
from playcd.services.DisplayService import DisplayService

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

def initialize_ucs() -> tuple[MainUC, CloseApplicationUC]:
        cd_driver_service = CDDriverService(logging)
        cd_info_service = CDInfoService(logging)
        create_playlist_service = CreatePlaylistService(logging)
        api_listener_service = StartApiListenerService(logging)
        is_tty_valid_service = IsTtyValidService(logging)
        keyboard_listener_service = KeyboardListenerService(logging)
        control_service = ControlService(logging)
        display_service = DisplayService(logging, api_listener_service)
        track_service = TrackService(
             logging,
             cd_driver_service, 
             api_listener_service, 
             keyboard_listener_service,
             control_service,
             display_service
        )
        play_service = PlayService(logging, track_service)

        mainUC = MainUC(
            logging,
            cd_driver_service,
            cd_info_service,
            create_playlist_service,
            api_listener_service,
            is_tty_valid_service,
            keyboard_listener_service,
            play_service,
            display_service
        )

        closeApplicationUC = CloseApplicationUC(
            logging,
            keyboard_listener_service,
            api_listener_service,
            cd_driver_service
        )

        return mainUC, closeApplicationUC

def main(log_level, shuffle, repeatStr, only_track, track_number = 1):
    try:
        logging.getLogger().setLevel(log_level)
        inputParams = InputParams(log_level, shuffle, RepeatEnum(repeatStr), only_track, track_number)
        mainUC , closeApplicationUC = initialize_ucs()
        mainUC.execute(inputParams)
        
    except KeyboardInterrupt:
        logging.info("Keyboard Interrupt detected! Stopping the execution!")
    finally:
        print("\n\n\nClosing the application. Please wait...")
        if closeApplicationUC:
            closeApplicationUC.execute()
        logging.info("Application closed.")
