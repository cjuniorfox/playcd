from typing import List
from playcd.domain.Track import Track

class DiscInformation:
    
    def __init__(self, total : int, tracks : List[Track]):
        self.total = total
        self.tracks = tracks

    def get_total(self):
        return self.total
    
    def get_tracks(self):
        return self.tracks
    
    def __repr__(self):
        return f"DiscInformation(total={self.total}, tracks={self.tracks})"