from notifypy import Notify
import timer as t
import argparse

FILE_LOCATION = "/tmp/timer_state"

parser = argparse.ArgumentParser(description='Interact with timer')
parser.add_argument('--mod', type=int, default=0,
                    help='change the timer by a certain increment (seconds)')
parser.add_argument('--default', type=int, default=0,
                    help='change the timer by a certain increment (seconds)')
parser.add_argument('--format', default="",
                    help='changes default the format')
parser.add_argument('--prefix', default="",
                    help='changes default the prefix')

def timer_from_file(loc: str) -> t.Timer:
    with open(loc, "r") as f:
        data = f.read()
        f.seek(0)
        return t.from_serialization(f.read())

def save_timer(loc: str, timer: str):
    with open(loc, "w") as f:
        f.truncate()
        f.write(timer)

def format_duration(fmt: str, duration: int) -> str:
    seconds = duration
    minutes = seconds / 60
    hours = minutes / 60
    return fmt.replace("%s", seconds).replace("%m", minutes).replace("%h")

args = parser.parse_args()

try:
    timer = timer_from_file(FILE_LOCATION)
except:
    timer = t.from_duration(args.default)

if timer.expired():
    notification = Notify()
    notification.title = "Timer Expired"
    notification.message = "Your time has expired!"

    notification.send()

    timer = t.from_duration(args.default)

if args.mod != 0:
    timer.mod_duration(args.mod)
    save_timer(FILE_LOCATION, timer.serialise())
    print("Changed timer by " + str(args.mod))

if args.format != "":
    print(args.prefix + str(timer.time_left()))


