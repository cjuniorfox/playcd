from typing import Optional
from playcd.domain.CDPlayerEnum import CDPlayerEnum

class BaseDisc:

    @property
    def command(self) -> CDPlayerEnum:
        return self._command

    @property
    def icon(self) -> str:
        return self._icon

    @property
    def time(self) -> "DisplayInformation.Time":
        return self._time

class DisplayInformation:

    class Time:
        def __init__(self, current: str, total: str):
            self._current = current
            self._total = total

        @property
        def current(self) -> str:
            return self._current

        @property
        def total(self) -> str:
            return self._total

    def __init__(self, command: CDPlayerEnum, time: "DisplayInformation.Time"):
        self._command = command
        self._time = time

    class Disc(BaseDisc):
        def __init__(self, command: CDPlayerEnum, time: "DisplayInformation.Time", tracks: int):
            super().__init__(command, time)
            self._tracks = tracks

        @property
        def tracks(self) -> int:
            return self._tracks

    class Track(BaseDisc):
        def __init__(self, command: CDPlayerEnum, time: "DisplayInformation.Time", track: int):
            super().__init__(command, time)
            self._track = track

        @property
        def track(self) -> int:
            return self._track

    def __init__(self, disc: Optional["DisplayInformation.Disc"], track: Optional["DisplayInformation.Track"]):
        self._disc = disc
        self._track = track

    @property
    def disc(self) -> Optional["DisplayInformation.Disc"]:
        return self._disc

    @property
    def track(self) -> Optional["DisplayInformation.Track"]:
        return self._track
