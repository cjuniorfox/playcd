from typing import Optional

class DisplayInformationResponse:
    def __init__(
            self, 
            disc: Optional["DisplayInformationResponse.DiscResponse"],
            track: Optional["DisplayInformationResponse.TrackResponse"]

        ):
        self._track = track
        self._disc = disc

    @property
    def disc(self) -> Optional["DisplayInformationResponse.DiscResponse"]:
        return self._disc

    @property
    def track(self) -> Optional["DisplayInformationResponse.TrackResponse"]:
        return self._track
    
    def to_dict(self):
        return {
            "disc": self.disc.to_dict() if self.disc else None,
            "track": self.track.to_dict() if self.track else None
        }

    def __repr__(self):
        return f"{self.__class__.__name__}=(disc='{self.disc}', track='{self.track}')"

    class DiscResponse:
        def __init__(
                self,
                tracks: int,
                icon: Optional["DisplayInformationResponse.IconResponse"],
                command: str,
                time: Optional["DisplayInformationResponse.TimeResponse"]
            ):
            self._tracks = tracks
            self._icon = icon
            self._command = command
            self._time = time

        @property
        def tracks(self) -> int:
            return self._tracks

        @property
        def icon(self) -> Optional["DisplayInformationResponse.IconResponse"]:
            return self._icon

        @property
        def command(self) -> str:
            return self._command
        
        @property
        def time(self) -> Optional["DisplayInformationResponse.TimeResponse"]:
            return self._time
        
        def to_dict(self):
            return {
                "tracks": self.tracks,
                "icon": self.icon.to_dict() if self.icon else None,
                "command": self.command,
                "time": self.time.to_dict() if self.time else None
            }
        
        def __repr__(self):
            return f"DisplayInformationResponse.DiscResponse(track='{self.tracks}', icon='{self.icon}', command='{self.command}', time='{self.time}')"

    class TrackResponse:
        def __init__(
                self,
                track: int,
                icon: Optional["DisplayInformationResponse.IconResponse"],
                command: str,
                time: Optional["DisplayInformationResponse.TimeResponse"]
            ):
            self._track = track
            self._icon = icon
            self._command = command
            self._time = time

        @property
        def track(self) -> int:
            return self._track
        
        @property
        def icon(self) -> "DisplayInformationResponse.IconResponse":
            return self._icon
        
        @property
        def command(self) -> str:
            return self._command
        
        @property
        def time(self) -> Optional["DisplayInformationResponse.TimeResponse"]:
            return self._time
        
        def to_dict(self):
            return {
                "track": self.track,
                "icon": self.icon.to_dict() if self.icon else None,
                "command": self.command,
                "time": self.time.to_dict() if self.time else None
            }
        
        def __repr__(self):
            return f"DisplayInformationResponse.TrackResponse(track='{self.track}', icon='{self.icon}', command='{self.command}', time='{self.time}')"

    class TimeResponse:
        def __init__(self, current: str, total: str):
            self._current = current
            self._total = total

        @property
        def current(self) -> str:
            return self._current

        @property
        def total(self) -> str:
            return self._total
        
        def to_dict(self):
            return {
                "current": self.current,
                "total": self.total
            }
        
        def __repr__(self):
            return f"DisplayInformationResponse.TimeResponse(current='{self.current}', total='{self.total}')"
    
    class IconResponse:
        def __init__(self, unicode: str, text: str):
            self._unicode = unicode
            self._text = text

        @property
        def unicode(self) -> str:
            return self._unicode

        @property
        def text(self) -> str:
            return self._text
        
        def to_dict(self):
            return {
                "unicode": self.unicode,
                "text": self.text
            }
        
        def __repr__(self):
            return f"DisplayInformationResponse.IconResponse(unicode='{self.unicode}', text='{self.text}')"