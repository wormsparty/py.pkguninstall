#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-y', '--yes', action='store_true', dest='yes', default=False,
                    help='Uninstall without asking for confirmation')
parser.add_argument('packages', nargs='*',
                    help='List of packages to uninstall (you can use regular expressions). '
                         'Specify none to list all available packages.')
args = parser.parse_args()

# Print all available packages (except Apple ones) when called with no argument.
# Does not require any privilege.
if not args.packages:
    parser.print_help()

    print("\n  List of available packages:\n")
    pkgutil = subprocess.Popen(('pkgutil', '--pkgs'), stdout=subprocess.PIPE)
    output = subprocess.call(('grep', '-v', '^com.apple.'), stdin=pkgutil.stdout)
    pkgutil.wait()
    print("\n")
    sys.exit(0)

# To uninstall, we need to be root.
if not os.geteuid() == 0:
    print("This script must be run as root")
    sys.exit(1)

roots = ['']

for d in os.listdir('/Users'):
    try:
        os.listdir('/Users/' + d)
        roots.append(d)
    except NotADirectoryError:
        pass


packages = []

# List the packages to uninstall according to the script arguments.
# Note that we do not make any restrictions here and can
# remove Apple packages if asked to!
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


def uninstall_package(pkg):
    info = subprocess.check_output(['pkgutil', '--pkg-info', pkg])
    location = info.splitlines()[3][10:].decode('utf-8')

    if not location.startswith('/'):
        location = '/' + location

    # We only to remove duplicated slashes when showing the files to the user
    # The filesystem doesn't care
    if location.endswith('/'):
        location = location[:-1]

    print("I'll be removing the following files:\n")

    files = subprocess.check_output(['pkgutil', '--files', pkg]).splitlines()

    for f in files:
        print(location + '/' + f.decode('utf-8'))

    if not args.yes:
        sys.stdout.write("\nProceed? This cannot be undone. (y/N) ")
        yesno = input().lower()

        if not yesno == 'y':
            return

    for f in files:
        remove_file(location + '/' + f.decode('utf-8'))

    for root in roots:
        ''' We clear this file for all users, because sometimes
            packages are detected to be installed according to the presence of these files,
            including the AppStore. '''
        subprocess.call(['rm', '-fr', root + '/Library/Preferences/' + pkg.decode('utf-8') + '.plist'])
        ''' We clear the Containers folder, which can contain large caching files depending on
            the application. For others, like Cache folder, they usually use the product 
            name instead of the package name, making it hard to find and delete them. '''
        subprocess.call(['rm', '-fr', root + '/Library/Containers/' + pkg.decode('utf-8')])
    
    subprocess.check_output(['pkgutil', '--forget', pkg])


for package in packages:
    for p in package.splitlines():
        if not args.yes:
            sys.stdout.write("Uninstall " + p.decode('utf-8') + " ? (y/N) ")
            choice = input().lower()

            if choice == 'y':
                uninstall_package(p)
        else:
            uninstall_package(p)
