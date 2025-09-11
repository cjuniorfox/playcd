import argparse
from playcd.core import main

def main_cli():
    parser = argparse.ArgumentParser(description="Play CD using cd-read, aplay and pv")
    parser.add_argument(
        "-l","--log-level",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: INFO)"
    )
    parser.add_argument("-s","--shuffle",action="store_true",help="shuffle tracks")
    parser.add_argument("-r","--repeat",default="off",choices=["off","1","all"], help="Repeat. 1=Actual track, all=whole disc. Default off")
    parser.add_argument("-o","--only-track",action="store_true", help="Plays a single track and exits")
    parser.add_argument("-S","--second", default="0", help="Start playing from this second")
    parser.add_argument("-d","--disc-sector", default="0", help="Start playing from this sector")
    parser.add_argument("track", nargs="?", default="1", help="The start track to play (e.g. 5)")
    args = parser.parse_args()

    main(
        log_level=args.log_level,
        shuffle=args.shuffle,
        repeat=args.repeat,
        only_track=args.only_track,
        track_number=int(args.track),
        start_second=int(args.second),
        start_sector=int(args.disc_sector)
    )
