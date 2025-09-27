import logging
from playcd.domain.RepeatEnum import RepeatEnum
from playcd.domain.CDPlayerEnum import CDPlayerEnum

class JumpTrackService:
    def __init__(self):
        self.logging = logging.getLogger(__name__)

    def _repeat_all(self, repeat: RepeatEnum, track_int: int, length: int) -> int:
        if track_int >= length and repeat == RepeatEnum.ALL:
            self.logging.info("Repeating playlist from the beginning.")
            return 0
        return track_int
    
    def _prev_or_next_track(self, command: CDPlayerEnum, track_count: int) -> int:
        if command == CDPlayerEnum.PREV:
            return max(0, track_count - 1)
        else:
            return track_count + 1

    def execute(self,command: CDPlayerEnum | None, repeat: RepeatEnum, track_count: int, length: int) -> int:
        track_count = self._prev_or_next_track(command, track_count)
        if repeat == RepeatEnum.ALL:
            track_count = self._repeat_all(repeat, track_count, length)

        return track_count