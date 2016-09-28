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

time.sleep(seconds + minutes * 60 + hours * 60 * 60)
