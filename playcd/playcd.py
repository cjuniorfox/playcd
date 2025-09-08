import subprocess
import re
import random
import sys
import logging
import cdio, pycdio

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

CDINFO = {}

def get_trackinfo(track):
    info = track.split()
    return {
        "number" : info[0].replace('.','').strip(),
        "length" :  int(info[1]),
        "lengthTime" : info[2].replace('[','').replace(']',''),
        "start" : int(info[3]),
        "startTime" : info[4].replace('[','').replace(']','')
    }

def get_total(line):
    info = line.split()
    return {
        "length" : int(info[1]),
        "lengthTime" : info[2].replace('[','').replace(']','')
    }

def display_time(sector):
    tracks = CDINFO["tracks"]
    count = len(tracks)
    track = [ t for t in tracks if (t["start"] <= sector and t["length"] + t["start"] >= sector ) ]
    number = track[0]["number"]
    
    seconds = int((sector - track[0]["start"]) / 75)
    minutes, secs = divmod(seconds, 60)
    
    len_seconds = int(track[0]["length"]/75)
    len_minutes, len_secs = divmod(len_seconds,60)

    disc_seconds = int(sector/75) 
    disc_minutes, disc_secs = divmod(disc_seconds, 60)

    total_seconds = int(CDINFO["total"]["length"]/75)
    total_minutes, total_secs = divmod(total_seconds, 60)

    print(f"Total: {count:2} {disc_minutes:02}:{disc_secs:02} / {total_minutes:02}:{total_secs:02}", flush=True, file=sys.stderr)
    print(f"Track: {number:2} {minutes:02}:{secs:02} / {len_minutes:02}:{len_secs:02}",end="",flush=True, file=sys.stderr)
    sys.stderr.write("\033[F") 

def play_cd(start,length):
    CHUNK_SIZE = 44100 * 2 * 2
    CHUNK_SECTORS = 37 # Max of 52  
    BYTES_PER_SECTOR = 2352 * 2
    
    cd = cdio.Device(driver_id=pycdio.DRIVER_UNKNOWN)
    drive_name = cd.get_device()
    aplay = ['aplay', '-f', 'S16_LE', '-c2', '-r44100']
    aplay_proc = subprocess.Popen(aplay,stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)

    sector = start
    try:
        while sector < start + length:
            sectors_to_read = min(CHUNK_SECTORS, (start + length) - sector)
            blocks,data = cd.read_sectors(sector, pycdio.READ_MODE_AUDIO, sectors_to_read)
            aplay_proc.stdin.write(bytes( data.encode('utf-8', errors='surrogateescape') ) )
            aplay_proc.stdin.flush()

            display_time(sector)
            sector += sectors_to_read

    finally:
        aplay_proc.stdin.close()
        aplay_proc.wait()
        print(file=sys.stderr)


def play_cd3(start,length):
    CHUNK_SIZE = 44100 * 2 * 2
    cdread = ['cd-read', '-m', 'audio' ,'-s' ,f'{start}', '-n', f'{length}', '--no-header', '--no-hexdump']
    aplay = ['aplay', '-f', 'S16_LE', '-c2', '-r44100']
    cdread_proc = subprocess.Popen(cdread,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL) 
    aplay_proc = subprocess.Popen(aplay,stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)

    logging.debug("CD-play from sector %s with length %s",start,length)
    sectors = start 

    buffer = b""
    try:
        while True:
            chunk = cdread_proc.stdout.read(CHUNK_SIZE)
            if not chunk:
                break
                        
            aplay_proc.stdin.write(chunk)
            aplay_proc.stdin.flush()
            
            display_time(sectors)
            sectors += 75

            sys.stdout.flush()

    finally:
        cdread_proc.stdout.close()
        aplay_proc.stdin.close()
        cdread_proc.wait()
        aplay_proc.wait()
        print("")

def play_track(track,repeat,shuffle):
    length = CDINFO["total"]["length"] if not shuffle and not repeat else track["length"]
    logging.info("Playing track: %s [%s]",track['number'],track['lengthTime'])
    logging.debug("Repeat: %s, Shuffle: %s",repeat,shuffle)
    play_cd(track['start'],length)
    if repeat:
        logging.debug("Repeat track enabled. Playing again")
        play_track(track,repeat,shuffle)

def play_tracks(tracks, repeat, shuffle):
    if shuffle:
        for track in tracks:
            play_track(track,False,shuffle)
    else:
        #If theres no shuffle, play the entire disc from the actual track
        play_track(tracks[0],False,False)
    if repeat:
        logging.debug("Repeat All enabled. Playing the entire disc again.")
        play_tracks(track,repeat,shuffle)

def prepare_tracks(tracks,shuffle,repeat,only_track):
    tracksToPlay = tracks
    if (only_track or repeat == "1"):
        play_track(tracks[0],repeat == "1", shuffle) 
        return
    if(shuffle):
        logging.debug("Shuffle enabled. Shuffling the musics before playing")
        if tracks[0]["number"] != "1":
            logging.debug("The first track is %s, playing this as first track and shuffling the rest",tracks[0]['number'])
            otherTracks = [ t for t in tracks if t != tracks[0] ]
            random.shuffle(otherTracks)
            tracksToPlay = [tracks[0]] + otherTracks
        else:
            random.shuffle(tracks)
            tracksToPlay = tracks
    play_tracks(tracksToPlay, repeat == "all", shuffle )

def retrieve_cdinfo():
    try:
        logging.debug("Retrieving information from the CD using 'cdparanoia'")
        cdinfo = subprocess.check_output(['cdparanoia', '-Q'], stderr=subprocess.STDOUT).decode().split('\n')
        tracks = [get_trackinfo(track) for track in cdinfo if re.match(r'^\d', track.lstrip())]
        total = [get_total(line) for line in cdinfo if line.startswith("TOTAL")][0]
        logging.debug("Retrieved information from the CD using 'cdparanoia'. Number of tracks %s",len(tracks))
        global CDINFO
        CDINFO = { "tracks" : tracks, "total" : total }
    except Exception as e:
        logging.exception('Error retrieving data from cdparanoia: %s',str(e))
        raise(e)

def main(track_number, log_level, shuffle, repeat, only_track):
    logging.getLogger().setLevel(log_level)
    logging.debug("Parameters: Track:%s, Log level: %s, Shuffle: %s, Repeat: %s, Only Track: %s",track_number, log_level, shuffle, repeat, only_track)
    retrieve_cdinfo()
    logging.info("This CD has %s tracks with the full length of %s",len(CDINFO["tracks"]),CDINFO["total"]["lengthTime"])
    startTrack = track_number or "1"
    tracks = [t for t in CDINFO["tracks"] if int(t["number"]) >= int(startTrack)]
    if(only_track): 
        logging.debug("Only track selected. Play a single track and exit")
        #Shuffle is true for a single track just to flag play only the track length
        play_track(tracks[0],repeat == "1", True)
        return
    prepare_tracks(tracks,shuffle,repeat,only_track)
    return
