import random
import sys
import logging
import cdio, pycdio
import sounddevice as sd

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

CDINFO = {}

def sec_to_time(sector,sector_start=0):
    sectors_per_second=75
    qt_sectors = sector - sector_start
    seconds = int(qt_sectors / sectors_per_second)
    minutes, secs = divmod(seconds, 60)
    return minutes, secs

def format_time(times):
    minutes, secs = times
    return f"{minutes:02}:{secs:02}"

def display_time(sector):
    tracks = CDINFO["tracks"]
    count = len(tracks)
    track = [ t for t in tracks if (t["start"] <= sector and t["length"] + t["start"] >= sector )] [0]
    number = track["number"]

    track_time = format_time(sec_to_time(sector,track["start"]))
    track_total = format_time(sec_to_time(track["length"]))
    disc_time = format_time(sec_to_time(sector))
    disc_total = format_time(sec_to_time(CDINFO["total"]))

    print(f"Total: {count:2} {disc_time} / {disc_total}", flush=True, file=sys.stderr)
    print(f"Track: {number:2} {track_time} / {track_total}",end="\033[F",flush=True, file=sys.stderr)
    #\033F return the carriage by two lines

def play_cd(start,length):
    SAMPLE_RATE = 44100
    CHANNELS = 2
    CHUNK_SECTORS = 37 # Max of 52  
    
    sector = start
    last_sector = start + length
    with sd.RawOutputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16"
    ) as stream:
        while sector < last_sector:
            sectors_to_read = min(CHUNK_SECTORS, last_sector - sector)
            blocks,data = CD.read_sectors(sector, pycdio.READ_MODE_AUDIO, sectors_to_read)
            stream.write(bytes( data.encode('utf-8', errors='surrogateescape') ) )

            display_time(sector)
            sector += sectors_to_read

def play_track(track, len_track, position):
    length = CDINFO["total"] if not len_track else track["length"]
    fromTxt = "from " if not len_track else ""
    logging.info("Playing %strack: %s",fromTxt,track['number'])
    start = track["start"]
    if position != 0 :
        # Check if the desired position is within the range
        if track["start"] <= position <= track["start"]+track["length"]:
            start = position
            logging.info("Start playing from %s",format_time(sec_to_time(start)))
        else:
            logging.warn("Position out of the range of the track. Will play from the beginning of the track")
    logging.debug("Track: %s, Use Track Length: %s, Start Position %s",track["number"],len_track, position)
    play_cd(start,length)

def play_playlist(playlist, repeat, shuffle, position):
    start_pos = position
    if shuffle or repeat == "1":
        for track in playlist:
            play_track(track,True,start_pos)
            start_pos = 0 # Reset start_pos for playing the other tracks
    else:
        #If theres no shuffle or repeat 1, play the entire disc from the actual track and position
        play_track(playlist[0],False, start_pos)
        start_pos = 0 #Reset the start pos
    if repeat in ["1","all"]: # If repeat 1, the playlist contains a single track
        logging.debug("Repeat All enabled. Playing the entire disc again.")
        play_tracks(track,repeat,shuffle,start_pos)

def get_track_by_sector(sector):
    tracks = CDINFO["tracks"]

    for t in tracks:
        start = t["start"]
        end = t["start"] + t["length"]
        track_number = t["number"]
        if start <= sector <= end:
            return track_number
    logging.warn("Track sector out of range, assuming track 1")
    return 1

def create_playlist(tracks,shuffle,repeat,only_track,track_number=1, sector = 0):
    track_num = track_number
    if sector > 0:
        track_num = max(get_track_by_sector(sector),track_number)
    filtered_tracks = [t for t in tracks if int(t["number"]) >= int(track_num)]
    if (only_track or repeat == "1"):
        return [ filtered_tracks[0] ]
    if(shuffle):
        logging.debug("Shuffle enabled. Shuffling the musics before playing")
        if tracks[0]["number"] != "1":
            logging.debug("The first track is %s, playing this as first track and shuffling the rest",tracks[0]['number'])
            otherTracks = [ t for t in filtered_tracks if t != filtered_tracks[0] ]
            random.shuffle(otherTracks)
            return [filtered_tracks[0]] + otherTracks
        else:
            random.shuffle(filtered_tracks)
            return filtered_tracks
    return filtered_tracks


def cdinfo():
    track_num = 1
    tracks = []
    num_tracks = CD.get_num_tracks()
    while track_num <= num_tracks:
        track = CD.get_track(track_num)
        tracks.append( {
            "format" : track.get_format(),
            "number" : track.track,
            "length" : track.get_last_lsn() - track.get_lsn(),
            "start" : track.get_lsn()
        } )
        track_num += 1
    total = CD.get_disc_last_lsn()
    global CDINFO
    CDINFO = {"tracks": tracks, "total": total}
    return CDINFO

def load_cd_driver():
    global CD
    CD = cdio.Device(driver_id=pycdio.DRIVER_UNKNOWN)
    CD.open()

def main(log_level, shuffle, repeat, only_track, track_number = 1, start_second=0, start_sector=0):
    logging.getLogger().setLevel(log_level)
    logging.debug("Parameters: Track:%s, Log level: %s, Shuffle: %s, Repeat: %s, Only Track: %s, Start Second: %s, Start sector: %s",track_number, log_level, shuffle, repeat, only_track, start_second, start_sector)
    if start_second > 0:
        position = start_second * 75
    else:
        position = start_sector
    load_cd_driver()
    cdinfo()
    logging.info("This CD has %s tracks",len(CDINFO["tracks"]))
    playlist = create_playlist(CDINFO["tracks"],shuffle,repeat,only_track, track_number,position)
    play_playlist(playlist, repeat, shuffle, position)
    CD.close()
