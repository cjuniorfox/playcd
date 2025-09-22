import logging
from typing import List
from playcd.domain.Track import Track
from playcd.services.TrackService import TrackService
from playcd.domain.RepeatEnum import RepeatEnum
from playcd.domain.CDPlayerEnum import CDPlayerEnum

class PlayService:
    def __init__(self,logging: logging,track_service: TrackService):
        self.logging = logging
        self.track_service = track_service

    def _next_track(self,command: CDPlayerEnum , repeat: RepeatEnum, track_int: int) -> int:
        if command == CDPlayerEnum.PREV:
            return max(0, track_int - 1)
        elif repeat == RepeatEnum.ONE:
            return track_int
        else:
            track_int += 1
            return track_int
    
    def _repeat_all(self, repeat: RepeatEnum, track_int: int, length: int) -> int:
        if track_int == length and repeat == RepeatEnum.ALL:
            self.logging.info("Repeating playlist from the beginning.")
            return 0
        return track_int


    def play(self, playlist: List[Track], repeat: RepeatEnum, shuffle: bool):
        self.logging.info("Starting playback with repeat=%s and shuffle=%s", repeat, shuffle)
        track_int = 0

        while track_int < len(playlist):
            command = self.track_service.play(playlist, track_int)
            track_int = self._next_track(command, repeat, track_int)
            track_int = self._repeat_all(repeat, track_int, len(playlist))
        
        self.logging.info("Playback finished.")
