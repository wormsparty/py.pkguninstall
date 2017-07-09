#!/usr/bin/env python3

import sys
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('t', nargs='*', help='time to sleep (eg. 1d 2h 0.5m 3s)')
args = parser.parse_args()

if not args.t:
    parser.print_help()
    sys.exit(1)

seconds = 0.0

for t in args.t:
    try:
        i = float(t[0:-1])
    except ValueError:
        parser.print_help()
        sys.exit(1)
	
    if t[-1] == 'd':
        seconds += 60.0 * 60.0 * 24.0 * i
    elif t[-1] == 'h':
        seconds += 60.0 * 60.0 * i
    elif t[-1] == 'm':
        seconds += 60.0 * i
    elif t[-1] == 's':
        seconds += i
    else:
        parser.print_help()
        sys.exit(1)
		
diff = seconds - int(seconds)

if (diff > 0.0):
    print('Warning: Ignoring ' + str(diff) + 's')

before = time.time()

try:
    time.sleep(int(seconds))
except KeyboardInterrupt:
    pass

passed = time.time() - before
days = int(passed / 60.0 / 60.0 / 24.0)
hours = int(passed / 60.0 / 60.0 - (days * 24))
minutes = int(passed / 60 - (hours * 60))
seconds = int(passed - (minutes * 60))
slept = 'Slept for '

if days > 0:
    slept += str(days)

    if days > 1:
        slept += ' days '
    else:
        slept += ' day '

if hours > 0:
    slept += str(hours)

    if hours > 1:
        slept += ' hours '
    else:
        slept += ' hour '

if minutes > 0:
    slept += str(minutes)
    
    if minutes > 1:
        slept += ' minutes '
    else:
        slept += ' minute ' 

if seconds > 0 or (days == 0 and hours == 0 and minutes == 0):
    slept += str(seconds)

    if seconds > 1:
        slept += ' seconds '
    else:
        slept += ' second '

print(slept)
