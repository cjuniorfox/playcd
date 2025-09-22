import logging
from playcd.domain.Track import Track
from playcd.domain.DiscInformation import DiscInformation
from playcd.adapter.repository.DiscInformationRepository import DiscInformationRepository

class RegisterDiscInformationService:
    
    def __init__(self, disc_information_repository: DiscInformationRepository):
        self.logging = logging.getLogger(__name__)
        self.disc_information_repository = disc_information_repository

    def register(self, cd) -> DiscInformation:
        self.logging.info("Retrieving disc information from CD media and registering it.")
        tracks = []
        track_num = 1
        num_tracks = cd.get_num_tracks()
        while track_num <= num_tracks:
            track = cd.get_track(track_num)
            tracks.append(
                Track(
                    track.track, 
                    track.get_format(), 
                    track.get_lsn(),
                    track.get_last_lsn(),
                    track.get_last_lsn() - track.get_lsn()
                )
            )
            track_num += 1

        total = cd.get_disc_last_lsn()

        disc_information = DiscInformation(total, tracks)
        self.disc_information_repository.set(disc_information=disc_information)

        logging.debug(f"CD info retrieved: %s",disc_information)

        return disc_information
