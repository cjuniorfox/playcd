from unittest.mock import MagicMock
from playcd.services.ControlService import ControlService
from playcd.domain.CDPlayerEnum import CDPlayerEnum

def test_control_service_pause():
    cd_player = MagicMock()
    control_service = ControlService()
    control_service.execute(CDPlayerEnum.PAUSE,cd_player)
    cd_player.pause.assert_called_once()

def test_control_service_stop():
    cd_player = MagicMock()
    control_service = ControlService()
    control_service.execute(CDPlayerEnum.STOP,cd_player)
    cd_player.stop.assert_called_once()

def test_control_service_play():
    cd_player = MagicMock()
    control_service = ControlService()
    control_service.execute(CDPlayerEnum.PLAY,cd_player)
    cd_player.play.assert_called_once()

def test_control_service_play():
    cd_player = MagicMock()
    control_service = ControlService()
    control_service.execute(CDPlayerEnum.FF,cd_player)
    cd_player.fast_forward.assert_called_once()

def test_control_service_play():
    cd_player = MagicMock()
    control_service = ControlService()
    control_service.execute(CDPlayerEnum.REW,cd_player)
    cd_player.rewind.assert_called_once()


def test_control_service_play():
    cd_player = MagicMock()
    control_service = ControlService()
    control_service.execute(CDPlayerEnum.QUIT,cd_player)
    cd_player.close.assert_called_once()