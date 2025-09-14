from playcd.domain.RepeatEnum import RepeatEnum

class InputParams:
    
    def __init__(
            self,
            log_level: str,
            shuffle: bool, 
            repeat: RepeatEnum, 
            only_track: bool, 
            track_number: int = 1
        ):
        self.log_level = log_level
        self.shuffle = shuffle
        self.repeat = repeat
        self.only_track = only_track
        self.track_number = track_number

    def get_log_level(self):
        return self.log_level
    
    def is_shuffle(self):
        return self.shuffle
    
    def get_repeat(self):
        return self.repeat
    
    def is_only_track(self):
        return self.only_track
    
    def get_track_number(self):
        return self.track_number
        
    def __repr__(self):
        return f"InputParams(log_level={self.log_level}, shuffle={self.shuffle}, repeat={self.repeat}, only_track={self.only_track}, track_number={self.track_number})"
        