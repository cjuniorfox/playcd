from playcd.domain.adapter.DisplayInformation import DisplayInformation
from playcd.domain.CDPlayerEnum import CDPlayerEnum

class DisplayInformationMapper:
    @staticmethod
    def map(lsn: int, command: CDPlayerEnum, disc_information) -> DisplayInformation:
        track = [
            t for t in disc_information.get_tracks()
            if (t.get_start_lsn() <= lsn and t.get_end_lsn() >= lsn)
        ][0]

        def sec_to_time(sector: int, sector_start=0):
            sectors_per_second = 75
            qt_sectors = sector - sector_start
            seconds = int(qt_sectors / sectors_per_second)
            minutes, secs = divmod(seconds, 60)
            return minutes, secs

        def format_time(times):
            minutes, secs = times
            return f"{minutes:02}:{secs:02}"

        return DisplayInformation(
            DisplayInformation.Disc(
                command=CDPlayerEnum.DISC,
                time=DisplayInformation.Time(
                    current=format_time(sec_to_time(lsn)),
                    total=format_time(sec_to_time(disc_information.get_total()))
                ),
                tracks=len(disc_information.get_tracks())
            ),
            DisplayInformation.Track(
                command=command,
                time=DisplayInformation.Time(
                    current=format_time(sec_to_time(lsn, track.get_start_lsn())),
                    total=format_time(sec_to_time(track.get_length()))
                ),
                track=track.get_number()
            )
        )