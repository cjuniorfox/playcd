import pytest
from playcd.services.JumpTrackService import JumpTrackService
from playcd.domain.CDPlayerEnum import CDPlayerEnum
from playcd.domain.RepeatEnum import RepeatEnum

def test_null_track_no_repeat():
    service = JumpTrackService()
    result = service.execute(None, RepeatEnum.NONE, 2, 5)
    assert result == 3

def test_next_track_no_repeat():
    service = JumpTrackService()
    result = service.execute(CDPlayerEnum.NEXT, RepeatEnum.NONE, 2, 5)
    assert result == 3

def test_prev_track_no_repeat():
    service = JumpTrackService()
    result = service.execute(CDPlayerEnum.PREV, RepeatEnum.NONE, 2, 5)
    assert result == 1

def test_prev_track_at_zero():
    service = JumpTrackService()
    result = service.execute(CDPlayerEnum.PREV, RepeatEnum.NONE, 0, 5)
    assert result == 0

def test_repeat_all_wraps_to_zero():
    service = JumpTrackService()
    result = service.execute(CDPlayerEnum.NEXT, RepeatEnum.ALL, 4, 5)
    assert result == 0

def test_repeat_all_wraps_to_zero_extra_track():
    service = JumpTrackService()
    result = service.execute(CDPlayerEnum.NEXT, RepeatEnum.ALL, 5, 5)
    assert result == 0

def test_repeat_all_does_not_wrap_if_not_at_end():
    service = JumpTrackService()
    result = service.execute(CDPlayerEnum.NEXT, RepeatEnum.ALL, 2, 4)
    assert result == 3