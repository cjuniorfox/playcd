class Track:
    def __init__(self, number, format, start_lsn, end_lsn, length):
        self.number = number
        self.format = format
        self.start_lsn = start_lsn
        self.end_lsn = end_lsn
        self.length = length

    def get_number(self):
        return self.number
    
    def get_format(self):
        return self.format
    
    def get_start_lsn(self):
        return self.start_lsn
    
    def get_end_lsn(self):
        return self.end_lsn
    
    def get_length(self):
        return self.length

    def __repr__(self):
        return f"Track(number={self.number}, format={self.format}, start_lsn={self.start_lsn}, end_lsn={self.end_lsn}, length={self.length})"