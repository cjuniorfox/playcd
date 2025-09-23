from unittest.mock import MagicMock
from playcd.services.ReadCommandService import ReadCommandService
from playcd.domain.CDPlayerEnum import CDPlayerEnum

def test_execute_returns_command():
    mock_repo = MagicMock()
    mock_repo.get.return_value = CDPlayerEnum.PLAY
    service = ReadCommandService(mock_repo)
    result = service.execute()
    assert result == CDPlayerEnum.PLAY

def test_execute_returns_none():
    mock_repo = MagicMock()
    mock_repo.get.return_value = None
    service = ReadCommandService(mock_repo)
    result = service.execute()
    assert result is None
    