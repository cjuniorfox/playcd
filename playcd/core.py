import logging
from playcd.domain.InputParams import InputParams
from playcd.usecases.MainUC import MainUC
from playcd.domain.RepeatEnum import RepeatEnum

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

def main(log_level, shuffle, repeatStr, only_track, track_number = 1):
    try:
        inputParams = InputParams(log_level, shuffle, RepeatEnum(repeatStr), only_track, track_number)
        mainUC = MainUC(logging)
        mainUC.execute(inputParams)
        
    except KeyboardInterrupt:
        logging.info("Keyboard Interrupt detected! Stopping the execution!")
    finally:
        print("\n\n\nClosing the application. Please wait...")
        if mainUC != None and mainUC.get_keyboard_listener() != None:
            mainUC.get_keyboard_listener().stop()
        if mainUC != None and mainUC.get_api_listener() != None:
            mainUC.get_api_listener().stop()
        if mainUC != None and mainUC.get_cd() != None:
            mainUC.get_cd().close()
        logging.info("Application closed.")
