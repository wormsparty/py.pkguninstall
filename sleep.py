#!/usr/bin/env python

import sys
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('t', nargs='*', help='time to sleep (Xh Ym Zs)')
args = parser.parse_args()

if not args.t:
    parser.print_help()
    sys.exit(1)

hours = 0
minutes = 0
seconds = 0

for t in args.t:
	try:
		i = int(t[0:-1])
	except ValueError:
    		parser.print_help()
    		sys.exit(1)
			
	if t[-1] == 'h':
		hours += i
	elif t[-1] == 'm':
		minutes += i
	elif t[-1] == 's':
		seconds += i

before = time.time()

try:
	time.sleep(seconds + minutes * 60 + hours * 60 * 60)
except KeyboardInterrupt:
	pass

passed = time.time() - before
hours = int(passed / 3600)
minutes = int(passed / 60 - (hours * 60))
seconds = int(passed - (minutes * 60))
slept = '\nSlept for '

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

if seconds > 0 or (hours == 0 and minutes == 0):
	slept += str(seconds)

	if seconds > 1:
		slept += ' seconds '
	else:
		slept += ' second'

print(slept)
