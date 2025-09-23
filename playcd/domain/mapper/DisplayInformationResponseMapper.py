from playcd.domain.adapter.DisplayInformationResponse import DisplayInformationResponse
from playcd.domain.DisplayInformation import DisplayInformation

class DisplayInformationResponseMapper:
    @staticmethod
    def map(display_info: DisplayInformation):
        def icon_to_unicode(icon):
            # Returns the unicode escape string for JSON (e.g., "\uf04a")
            return "\\u{:04x}".format(ord(icon)) if icon else None

        disc = None
        if display_info.disc:
            disc = DisplayInformationResponse.DiscResponse(
                tracks=display_info.disc.tracks,
                icon=icon_to_unicode(display_info.disc.command.icon),
                command=display_info.disc.command.command,
                time=DisplayInformationResponse.TimeResponse(
                    current=display_info.disc.time.current,
                    total=display_info.disc.time.total
                ) if display_info.disc.time else None
            )
        track = None
        if display_info.track:
            track = DisplayInformationResponse.TrackResponse(
                track=display_info.track.track,
                icon=icon_to_unicode(display_info.track.command.icon),
                command=display_info.track.command.command,
                time=DisplayInformationResponse.TimeResponse(
                    current=display_info.track.time.current,
                    total=display_info.track.time.total
                ) if display_info.track.time else None
            )
        return DisplayInformationResponse(disc=disc, track=track)