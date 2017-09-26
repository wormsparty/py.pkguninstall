#!/usr/bin/env python3

import os
import sys
import subprocess
import tkinter
from tkinter import messagebox

# To uninstall, we need to be root.
if not os.geteuid() == 0:
    messagebox.showinfo("Must be root", "This program must be run as root")
    sys.exit(1)


# Let's list the packages
pkgutil = subprocess.Popen(('pkgutil', '--pkgs'), stdout=subprocess.PIPE)
output = subprocess.check_output(('grep', '-v', '^com.apple.'), stdin=pkgutil.stdout).splitlines()

# First create the window
window = tkinter.Tk()

width = 0

for o in output:
    width = max(width, len(o))

# Let's construct the list which will contain all packages we can uninstall
tkinter.Label(window, text='Select a package to uninstall:').pack()
list = tkinter.Listbox(window, width=width)

# We now fill the list
i = 1

for o in output:
    list.insert(i, o)
    i += 1

list.pack()

def remove_file(f):
    if os.path.exists(f) and not os.path.isdir(f):
        os.remove(f)

    try:
        os.removedirs(os.path.dirname(f))
    except OSError:
        pass


def uninstall_package(pkg):
    info = subprocess.check_output(['pkgutil', '--pkg-info', pkg])
    location = info.splitlines()[3][10:]

    if not location.startswith('/'):
        location = '/' + location

    # We only to remove duplicated slashes when showing the files to the user
    # The filesystem doesn't care
    if location.endswith('/'):
        location = location[:-1]

    files = subprocess.check_output(['pkgutil', '--files', pkg]).splitlines()

    for f in files:
        remove_file(location + '/' + f)

    subprocess.check_output(['pkgutil', '--forget', pkg])


def uninstall():
    selection = list.get(list.curselection()).decode('utf-8')

    if messagebox.askyesno("Confirmation", "Are you sure you wish to uninstall " + selection + "?"):
        uninstall_package(selection)


tkinter.Button(window, text='Uninstall', command=uninstall).pack()

window.mainloop()

