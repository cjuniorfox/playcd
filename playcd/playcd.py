import random
import sys, os
import logging
import cdio, pycdio
import sounddevice as sd
import threading
import time
from playcd.pipe_listener import PipeListener
from playcd.keyboard_listener import KeyboardListener

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

CDINFO = {}

PREV="\uf049"
STOP="\uf04d"
PLAY="\uf04b"
NEXT="\uf050"
PAUSE="\uf04c"
DISC="\uede9"

def sec_to_time(sector,sector_start=0):
    sectors_per_second=75
    qt_sectors = sector - sector_start
    seconds = int(qt_sectors / sectors_per_second)
    minutes, secs = divmod(seconds, 60)
    return minutes, secs

def format_time(times):
    minutes, secs = times
    return f"{minutes:02}:{secs:02}"

def display(sector,icon=f"{PLAY}"):
    tracks = CDINFO["tracks"]
    count = len(tracks)
    track = [ t for t in tracks if (t["start"] <= sector and t["length"] + t["start"] >= sector )] [0]
    number = track["number"]

    track_time = format_time(sec_to_time(sector,track["start"]))
    track_total = format_time(sec_to_time(track["length"]))
    disc_time = format_time(sec_to_time(sector))
    disc_total = format_time(sec_to_time(CDINFO["total"]))

    print(f"\r {DISC} {count:2} {disc_time} / {disc_total}", flush=True, file=sys.stderr)
    print(f"\r {icon} {number:2} {track_time} / {track_total}",end="\033[F",flush=True, file=sys.stderr)
    #\033F return the carriage to the beginning of the previous line

def get_command(sector=0):
    command = get_command_from_listener()
    if not command:
        command = get_command_from_keyboard()
    return command

def process_command(sector=0):
    command = get_command()
    if command:
        if(command in ["pause","stop"]):
            logging.info(f"{command} issued.")
            is_stop = command == "stop"
            icon=f"{STOP}" if is_stop else f"{PAUSE}"
            display(0 if is_stop else sector, icon)
            while True:
                time.sleep(0.5)
                command = get_command()
                if command and command in ["pause", "play"]:
                   logging.info("Resume issued.")
                   if is_stop:
                       '''Restart from the begining of the playlist'''
                       return "restart"
                   break

        if(command in ["next","prev"]):
            logging.info(f"{command} track issued")
            display(sector,f"{NEXT}" if command == "next" else f"{PREV}")
            return command
        if(command == "quit"):
            raise KeyboardInterrupt

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
            display(sector)
            '''Process command interface'''
            command = process_command(sector)
            if command:
                if command in ["next","restart"]:
                    return command
                '''If at the beginning of the track, play the previous track. If not, play the beggining of the track'''
                if command == "prev":
                    if (sector - start) > 150:
                        sector = start
                    else:
                        return command
            else:
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
    return play_cd(start,length)

def play_playlist(playlist, repeat, shuffle, position):
    start_pos = position
    i = 0
    while i < len(playlist):
        command = play_track(playlist[i],True, start_pos)
        '''If command is next, just play the next track. No further validation required'''
        if not command and not shuffle:
            '''If no command was issued, just leave the loop, as the disc was played entirely'''
            #break - Testing the playback as list
        if command == "prev":
            i=max(i-1,0)
        elif command == "restart":
            i=0
        else:
            i=i+1
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
        if int(filtered_tracks[0]["number"]) > 1:
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

def start_listener():
    global LISTENER
    global KEYBOARD
    LISTENER = PipeListener("/tmp/playcd",logging)
    LISTENER.start()
    KEYBOARD = KeyboardListener(logging)
    KEYBOARD.start()

def get_command_from_listener():
    try:
        return LISTENER.get_command()
    except Exception as e:
        logging.error("Error getting the listener command %s.",e)

def get_command_from_keyboard():
    try:
        return KEYBOARD.get_command()
    except Exception as e:
        logging.error("Error getting the keyboard comand %s",e)

def print_instructions():
    print("PlayCD player\n")
    print(f"Keyboard Commands:\n [A]  [S]  [W]  [D]  [Space]\n  {PREV}    {STOP}    {PLAY}    {NEXT}      {PAUSE}\n")
    print("You can also send the commands to a pipe by writing to '/tmp/playcd'\nAccepted commands:\n[prev] [next] [play] [pause] [stop]\n")

def main(log_level, shuffle, repeat, only_track, track_number = 1, start_second=0, start_sector=0):
    try:
        logging.getLogger().setLevel(log_level)
        logging.debug("Parameters: Track:%s, Log level: %s, Shuffle: %s, Repeat: %s, Only Track: %s, Start Second: %s, Start sector: %s",track_number, log_level, shuffle, repeat, only_track, start_second, start_sector)
        if start_second > 0:
            position = start_second * 75
        else:
            position = start_sector
        load_cd_driver()
        cdinfo()
        logging.info("This CD has %s tracks.",len(CDINFO["tracks"]))
        playlist = create_playlist(CDINFO["tracks"],shuffle,repeat,only_track, track_number,position)
        print_instructions()
        start_listener()
        play_playlist(playlist, repeat, shuffle, position)
        
    except KeyboardInterrupt:
        logging.info("Keyboard Interrupt detected! Stopping the execution!")
    finally:
        print("\n\n\nClosing the application. Please wait...")
        CD.close()
        LISTENER.stop()
        KEYBOARD.stop()
