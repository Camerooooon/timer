from notifypy import Notify
import time
import timer as t
import argparse

FILE_LOCATION = "/tmp/timer_state"

parser = argparse.ArgumentParser(description='Interact with timer')
parser.add_argument('--mod', type=int, default=0,
                    help='change the timer by a certain increment (seconds)')
parser.add_argument('--set', type=int, default=0,
                    help='set the timer to a certain time (seconds)')
parser.add_argument('--default', type=int, default=0,
                    help='change the timer by a certain increment (seconds)')
parser.add_argument('--format', default="%H:%M:%S",
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

args = parser.parse_args()

try:
    timer = timer_from_file(FILE_LOCATION)
except:
    timer = t.from_duration(args.default)

if timer.expired() and not timer.alerted_expired:
    notification = Notify()
    notification.title = "Time expired"
    notification.message = "Your time has expired!"

    notification.send()

    timer = t.from_duration(args.default)
    timer.alerted_expired = True
    save_timer(FILE_LOCATION, timer.serialise())

if args.mod != 0:
    if timer.expired():
        timer = t.from_duration(0)
    timer.mod_duration(args.mod)
    save_timer(FILE_LOCATION, timer.serialise())
    print("Changed timer by " + str(args.mod))

if args.set != 0:
    timer = t.from_duration(args.set + 1) # Adding a little bit so it appears to start at the correct time
    save_timer(FILE_LOCATION, timer.serialise())
    print("Set timer to " + str(args.set))


if args.format != "":
    print(args.prefix + time.strftime(args.format, time.gmtime(timer.time_left())))


