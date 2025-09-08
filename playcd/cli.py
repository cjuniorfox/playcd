import argparse
import json
from playcd.playcd import main as playcd

def main():
    parser = argparse.ArgumentParser(description="Play CD using cd-read, aplay and pv")
    parser.add_argument("track", nargs="?", default=None, help="The start track to play (e.g. 5)")
    parser.add_argument(
        "-l","--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: INFO)"
    )
    parser.add_argument("-s","--shuffle",action="store_true",help="shuffle tracks")
    parser.add_argument("-r","--repeat",default="off",choices=["off","1","all"], help="Repeat. 1=Actual track, all=whole disc. Default off")
    parser.add_argument("-o","--only-track",action="store_true", help="Plays a single track and exits")
    args = parser.parse_args()

    playcd(
        track_number=args.track,
        log_level=args.log_level,
        shuffle=args.shuffle,
        repeat=args.repeat,
        only_track=args.only_track
    )
