import pycdio,cdio
import sounddevice as sd
import time
import threading
import logging

class CDPlayer:

    CHUNK_SECTORS = 37
    
    SAMPLE_RATE = 44100
    CHANNELS = 2

    _lsn = 0
    _pause = False
    _stop = False
    _is_running = False
    _start_lsn=0
    _length=0

    def __init__(self,cd: cdio.Device, logging: logging):
        self._cd = cd
        self._logging = logging

    def _play_cd(self):
        self._lsn = self._start_lsn
        last_lsn = self._start_lsn + self._length

        with sd.RawOutputStream(
                samplerate=self.SAMPLE_RATE, 
                channels=self.CHANNELS, 
                dtype="int16"
        ) as pcm_audio_stream:
           """If pause, sleep until not paused"""
           while self._lsn < last_lsn:
                while self._pause or self._stop:
                    time.sleep(0.2)
                    if self._stop:
                        self._lsn = self._start_lsn
                lsn_to_read = min(self.CHUNK_SECTORS, last_lsn - self._lsn)
                blocks, data = self._cd.read_sectors(self._lsn, pycdio.READ_MODE_AUDIO, lsn_to_read)
                pcm_audio_stream.write(bytes(data.encode("utf-8",errors="surrogateescape")))
                self._lsn += lsn_to_read
                if not self._is_running:
                    break

    def get_lsn(self):
        return self._lsn

    def pause(self):
        self._logging.debug("Pause issued. Current state %s",self._pause)
        self._pause = not self._pause
    
    def play(self):
        self._stop = False
        self._pause = False

    def stop(self):
        self._stop = True

    def close(self):
        self._is_running = False

    def fast_forward(self):
        self._lsn = min(self._lsn + 500,self._start_lsn + self._length)

    def rewind(self):
        self._lsn = max(self._lsn - 500, self._start_lsn)

    def jump(self, lsn:int, length=0):
        self._start_lsn=lsn
        self._lsn = lsn
        if length > 0:
            self._length=length

    def is_playing(self):
        return self._listener_thread.is_alive()
    
    def is_stop(self):
        return self._stop

    def is_pause(self):
        return self._pause

    def start(self,start_lsn,length):
        self._start_lsn = start_lsn
        self._length = length
        """Start player"""
        self._is_running = True
        self._listener_thread = threading.Thread(target=self._play_cd, daemon=True)
        self._listener_thread.start()
