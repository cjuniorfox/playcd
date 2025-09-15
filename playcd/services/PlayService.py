import logging
from playcd.domain.PreparedPlayback import PreparedPlayback
from playcd.services.TrackService import TrackService
from playcd.domain.RepeatEnum import RepeatEnum

class PlayService:
    def __init__(self,logging: logging,track_service: TrackService):
        self.logging = logging
        self.track_service = track_service

    def play(self, preparedPlayback: PreparedPlayback, repeat: RepeatEnum, shuffle: bool):
        self.logging.info("Starting playback with repeat=%s and shuffle=%s", repeat, shuffle)
        playlist = preparedPlayback.get_playlist()
        position = 0

        while position < len(playlist):
            command = self.track_service.play(preparedPlayback, position)
            if command == "next":
                position += 1
            elif command == "prev":
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
