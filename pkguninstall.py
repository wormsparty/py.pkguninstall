#!/usr/bin/env python

import os
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('packages', nargs='*', help='packages to uninstall (you can also use regex)')
args = parser.parse_args()

# Print all available packages (accept Apple ones) when called with no argument.
# Does not requier any privileges.
if not args.packages:
    parser.print_help()
    
    print("\n  List of available packages:\n")
    pkgutil = subprocess.Popen(('pkgutil', '--pkgs'), stdout=subprocess.PIPE)
    output = subprocess.call(('grep', '-v', '^com.apple.'), stdin=pkgutil.stdout)
    pkgutil.wait()
    print("\n")
    sys.exit(0)

if not os.geteuid() == 0:
    print("This script must be run as root")
    sys.exit(1)

packages = []

for package in args.packages:
    try:
        output = subprocess.check_output(['pkgutil', '--pkgs=' + package])
        packages.append(output)
    except subprocess.CalledProcessError:
        print('No matching package found for: ' + package)


def remove_file(f):
    if os.path.exists(f) and not os.path.isdir(f):
        os.remove(f)
	
	try:
        	os.removedirs(os.path.dirname(f))
	except OSError:
		pass


def uninstall_package(package):
    info = subprocess.check_output(['pkgutil', '--pkg-info', package])
    location = info.splitlines()[3][10:]

    if not location.startswith('/'):
        location = '/' + location

    # Only to remove duplicated slashed when showing the files to the user
    # The filesystem doesn't care
    if location.endswith('/'):
        location = location[:-1]

    print("I'll be removing the following files:\n")

    files = subprocess.check_output(['pkgutil', '--files', package]).splitlines()

    for f in files:
        print(location + '/' + f)

    sys.stdout.write("\nProceed? This cannot be undone. (y/N) ")
    choice = raw_input().lower()

    if not choice == 'y':
        return

    for f in files:
        remove_file(location + '/' + f)

    subprocess.check_output(['pkgutil', '--forget', package])


for package in packages:
    for p in package.splitlines():
    	sys.stdout.write("Uninstall " + p + " ? (y/N) ")
    	choice = raw_input().lower()

        if choice == 'y':
            uninstall_package(p)

