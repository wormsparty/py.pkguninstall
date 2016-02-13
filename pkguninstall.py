#!/usr/bin/env python

import os
import sys
import argparse
import subprocess

if not os.geteuid() == 0:
    print("This script must be run as root")
    sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument('action', choices=['list', 'remove'])
parser.add_argument('package', nargs='?', help='package to uninstall (you can also use regex)')
args = parser.parse_args()

if args.action == 'list':
    subprocess.call(['pkgutil', '--pkgs'])
    sys.exit(0)

if not args.package:
    parser.print_help()
    sys.exit(1)

packages = subprocess.check_output(['pkgutil', '--pkgs=' + args.package])


def remove_file(f):
    if not os.path.isdir(f):
        os.remove(f)
        os.removedirs(os.path.dirname(f))


def uninstall_package(package):
    info = subprocess.check_output(['pkgutil', '--pkg-info', package])
    location = info.splitlines()[3][10:]

    # Only to remove duplicated slashed when showing the files to the user
    # The filesystem doesn't care
    if location.endswith('/'):
        location = location[:-1]

    print("I'll be removing the following files:\n")

    files = subprocess.check_output(['pkgutil', '--files', package])

    for f in files:
        print(location + '/' + f)

    sys.stdout.write("\nProceed? This cannot be undone. (y/N) ")
    choice = raw_input().lower()

    if not choice == 'y':
        return

    for f in files:
        remove_file(location + '/' + f)

    subprocess.check_output(['pkgutil', '--forget', package])


for package in packages.splitlines():
    sys.stdout.write("Uninstall " + package + " ? (y/N) ")
    choice = raw_input().lower()

    if choice == 'y':
        uninstall_package(package)

