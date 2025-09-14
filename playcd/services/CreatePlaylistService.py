import logging
from playcd.domain.DiscInformation import DiscInformation
from playcd.domain.InputParams import InputParams
from playcd.domain.Track import Track
from playcd.domain.RepeatEnum import RepeatEnum
from typing import List
import random

class CreatePlaylistService:
    
    def __init__(self, logging: logging):
        self.logging = logging

    def _filter_tracks(self, tracks: List[Track], params: InputParams) -> List[Track]:
        filtered_tracks = [t for t in tracks if int(t.get_number()) >= int(params.get_track_number()) and t.get_format() == "audio"]
        self.logging.debug("Filtered tracks based on starting track number %s: %s", params.get_track_number(), [t.get_number() for t in filtered_tracks])
        return filtered_tracks

    def _single_track(self, filtered_tracks: List[Track], params: InputParams) -> List[Track]:
        self.logging.debug("Only one track requested or repeat set to 1. Playing only the first track: %s", filtered_tracks[0].get_number())
        return [ filtered_tracks[0] ]
    
    def _shuffle_tracks_from_track_number(self, tracks: List[Track], start_track: Track) -> List[Track]:
        self.logging.debug("The first track is %s, playing this as first track and shuffling the rest",tracks[0].get_number())
        otherTracks = [ t for t in tracks if t != tracks[0] ]
        random.shuffle(otherTracks)
        self.logging.debug("Playlist created: %s", [t.get_number() for t in [tracks[0]] + otherTracks])
        return [tracks[0]] + otherTracks

    def _shuffle_tracks(self, filtered_tracks: List[Track]) -> List[Track]:
        self.logging.debug("Shuffle enabled. Shuffling the musics before playing")
        if int(filtered_tracks[0].get_number()) > 1:
            return self._shuffle_tracks_from_track_number(filtered_tracks, filtered_tracks[0])
        else:
            self.logging.debug("The first track is %s, shuffling all tracks",filtered_tracks[0].get_number())
            random.shuffle(filtered_tracks)
            return filtered_tracks
        
    def create(self, cdinfo: DiscInformation, params: InputParams) -> List[Track]:
        self.logging.info("Creating playlist based on input parameters")
        filtered_tracks = self._filter_tracks(cdinfo.get_tracks(), params)
        if (params.is_only_track() or params.get_repeat() == RepeatEnum.ONE):
            return self._single_track(filtered_tracks, params)
        if(params.is_shuffle()):
            return self._shuffle_tracks(filtered_tracks)
            
        self.logging.debug("Playlist created: %s", [t.get_number() for t in filtered_tracks])
        return filtered_tracks