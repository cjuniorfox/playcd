import random
import sys
import os
import logging
import cdio, pycdio
import sounddevice as sd
import time
from playcd.pipe_listener import PipeListener
from playcd.keyboard_listener import KeyboardListener
from playcd.cd_display import CDDisplay, CDIcons
from playcd.cd_player import CDPlayer

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

CDINFO = {}
VALID_TTY = False

KEYBOARD_LISTENER=None
PIPE_LISTENER=None

def display(sector, icon = CDIcons.PLAY):
    if VALID_TTY:
        CD_DISPLAY.display(sector,icon)

def get_command_from_pipe():
    try:
        return PIPE_LISTENER.get_command()
    except Exception as e:
        logging.error("Error getting the listener command %s.",e)

def get_command_from_keyboard():
    if KEYBOARD_LISTENER == None:
        return None
    try:
        return KEYBOARD_LISTENER.get_command()
    except Exception as e:
        logging.error("Error getting the keyboard comand %s",e)

def get_command(sector=0):
    command = get_command_from_pipe()
    if not command:
        command = get_command_from_keyboard()
    return command

def process_command(lsn,cd_player):
    command = get_command()
    if command:
        logging.info("%s issued",command)
        if command == "pause":
            display(lsn,CDIcons.PAUSE)
            cd_player.pause()
        elif command == "stop":
            display(lsn,CDIcons.STOP)
            cd_player.stop()
        elif command == "play":
            cd_player.play()
        elif command == "fast forward":
            display(lsn,CDIcons.FF)
            cd_player.fast_forward()
        elif command == "rewind":
            display(lsn,CDIcons.REW)
            cd_player.rewind()
        elif command == "next":
            display(lsn,CDIcons.NEXT)
        elif command == "prev":
            display(lsn,CDIcons.PREV)
        elif command == "quit":
            cd_player.close()
            raise KeyboardInterrupt
        return command

def get_icon_from_cd_player(cd_player):
    if cd_player.is_stop():
        return CDIcons.STOP
    elif cd_player.is_pause():
        return CDIcons.PAUSE
    elif cd_player.is_playing():
        return CDIcons.PLAY

def play_cd(playlist, position, single_track = False):
    start = playlist[position]["start"]
    length = playlist[position]["length"] if single_track else CDINFO["total"]
    cd_player = CDPlayer(CD, logging)
    cd_player.start(start,length)
    while cd_player.is_playing():
        lsn = cd_player.get_lsn()
        command = process_command(lsn,cd_player)
        if command:
            if command in ["next","prev"]:
                if single_track:
                    cd_player.close()
                    return command
                i = 0
                while i < len(playlist):
                    if playlist[i]["number"] == get_track_by_lsn(lsn) and i < len(playlist) - 1:
                        int_track = min(i+1,len(playlist)-1) if command == "next" else max(i-1,0)
                        if command == "prev" and lsn - playlist[i]["start"] > 150:
                            int_track = i
                        cd_player.jump(playlist[int_track]["start"])
                    i+=1
        icon = get_icon_from_cd_player(cd_player)
        time.sleep(0.5)
        display(lsn,icon)

def play_playlist(playlist, repeat, shuffle):
    i = 0
    single_track = (repeat == "1" or shuffle)
    if not shuffle:
        play_cd(playlist, 0, single_track)
    else:
        while i < len(playlist):
            command = play_cd(playlist,i,True)
            i = max(i-1,0) if command == "prev" else min(i+1,len(playlist)-1)
    
    if repeat in ["1","all"]: # If repeat 1, the playlist contains a single track
        logging.debug("Repeat All enabled. Playing the entire disc again.")
        play_playlist(playlist,repeat,shuffle)

def get_track_by_lsn(sector):
    tracks = CDINFO["tracks"]

    for t in tracks:
        start = t["start"]
        end = t["start"] + t["length"]
        track_number = t["number"]
        if start <= sector <= end:
            return track_number
    logging.warn("Track sector out of range, assuming track 1")
    return 1

def create_playlist(tracks,shuffle,repeat,only_track,track_number=1):
    filtered_tracks = [t for t in tracks if int(t["number"]) >= int(track_number)]
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

def enable_cd_display():
    global CD_DISPLAY
    CD_DISPLAY = CDDisplay(CDINFO)

def is_tty_valid():
    global VALID_TTY
    VALID_TTY = os.isatty(sys.stdout.fileno())
    return VALID_TTY

def start_keyboard_listener():
    if not VALID_TTY:
        logging.warn("stdout is redirected or invalid. Keyboard listener not enable on this environment")
        return
    keys=["[Q","A","S","W","D","E","Space]"]
    icons=[f"{CDIcons.REW}", f"{CDIcons.PREV}", f"{CDIcons.STOP}", f"{CDIcons.PLAY}", f"{CDIcons.NEXT}", f"{CDIcons.FF}", f"  {CDIcons.PAUSE}"]
    
    print("Keyboard Commands:")
    print("","]  [".join(keys),)
    print(" ","    ".join(icons),"\n")
    global KEYBOARD_LISTENER
    KEYBOARD_LISTENER = KeyboardListener(logging)
    KEYBOARD_LISTENER.start()

def start_pipe_listener():
    pipe_name = "/tmp/playcd"
    logging.info("Control the CD by writing commands to the pipe '%s'. Accepted commands: [prev] [next] [play] [pause] [stop].",pipe_name)
    global PIPE_LISTENER
    PIPE_LISTENER = PipeListener(pipe_name,logging)
    PIPE_LISTENER.start()
    

def main(log_level, shuffle, repeat, only_track, track_number = 1): 
    try:
        print("PlayCD Player\n")
        logging.getLogger().setLevel(log_level)
        logging.debug("Parameters: Track:%s, Log level: %s, Shuffle: %s, Repeat: %s, Only Track: %s",track_number, log_level, shuffle, repeat, only_track)
        load_cd_driver()
        cdinfo()
        enable_cd_display()
        logging.info("This CD has %s tracks.",len(CDINFO["tracks"]))
        playlist = create_playlist(CDINFO["tracks"],shuffle,repeat,only_track, track_number)
        start_pipe_listener()
        is_tty_valid()
        start_keyboard_listener()
        play_playlist(playlist, repeat, shuffle)
        
    except KeyboardInterrupt:
        logging.info("Keyboard Interrupt detected! Stopping the execution!")
    finally:
        print("\n\n\nClosing the application. Please wait...")
        CD.close()
        if PIPE_LISTENER != None:
            PIPE_LISTENER.stop()
        if KEYBOARD_LISTENER != None:
            KEYBOARD_LISTENER.stop()
