import logging
from playcd.services.TrackService import TrackService
from playcd.domain.RepeatEnum import RepeatEnum
from playcd.domain.CDPlayerEnum import CDPlayerEnum

class PlayService:
    def __init__(self,logging: logging,track_service: TrackService):
        self.logging = logging
        self.track_service = track_service

    def next_track(self,command: CDPlayerEnum , repeat: RepeatEnum, track_int: int) -> int:
        if command == CDPlayerEnum.PREV:
            return max(0, track_int - 1)
        elif repeat == RepeatEnum.ONE:
            return track_int
        else:
            track_int += 1
            return track_int
    
    def repeat_all(self, repeat: RepeatEnum, track_int: int, length: int) -> int:
        if track_int == length and repeat == RepeatEnum.ALL:
            self.logging.info("Repeating playlist from the beginning.")
            return 0
        return track_int
