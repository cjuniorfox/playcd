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

    def play(self, playlist: List[Track], repeat: RepeatEnum, shuffle: bool):
        self.logging.info("Starting playback with repeat=%s and shuffle=%s", repeat, shuffle)
        position = 0

        while position < len(playlist):
            command = self.track_service.play(playlist, position)
            if command == CDPlayerEnum.NEXT:
                position += 1
            elif command == CDPlayerEnum.PREV:
                position = max(0, position - 1)
            else:
                position += 1

            if position >= len(playlist):
                if repeat in [RepeatEnum.ALL, RepeatEnum.ONE]:
                    position = 0
                    self.logging.info("Repeating playlist from the beginning.")
                else:
                    break

        self.logging.info("Playback finished.")
