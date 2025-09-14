from logging import logging
from playcd.domain.Track import Track
from playcd.domain.DiscInformation import DiscInformation

class CDInfoService:
    
    def __init__(self, logging: logging):
        self.logging = logging

    def get_cd_info(self, cd) -> DiscInformation:
        self.logging.info("Getting CD info")
        tracks = []
        num_tracks = cd.get_num_tracks()
        while track_num <= num_tracks:
            track = cd.get_track(track_num)
            tracks.append(
                Track(
                    track.track, 
                    track.get_format(), 
                    track.get_lsn(),
                    track.last_lsn(),
                    track.get_last_lsn() - track.get_lsn()
                )
            )
            track_num += 1

        total = cd.get_disc_last_lsn()

        discInformation = DiscInformation(total, tracks)

        logging.debug(f"CD info retrieved: {discInformation}")

        return discInformation