#!/usr/bin/env python3

import os
import sys
import subprocess
import tkinter
from tkinter import messagebox
from _tkinter import TclError

# First create the window
window = tkinter.Tk()

# Let's construct the list which will contain all packages we can uninstall
tkinter.Label(window, text='Select a package to uninstall:').pack()

pkglist = tkinter.Listbox(window, width=50)
pkglist.pack()


def refresh():
    pkglist.delete(0, pkglist.size())

    # Let's list the packages
    pkgutil = subprocess.Popen(('pkgutil', '--pkgs'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('grep', '-v', '^com.apple.'), stdin=pkgutil.stdout).splitlines()

    # We now fill the list
    i = 1

    for o in output:
        pkglist.insert(i, o)
        i += 1


def uninstall_package(pkg):
    directory = os.path.dirname(os.path.realpath(__file__))
    script = 'do shell script "' + sys.executable + ' ' + \
             directory + '/pkguninstall.py -y ' + pkg.decode('utf-8') + '" with administrator privileges'
    subprocess.call(['osascript', '-e', script])
    refresh()


def uninstall():
    try:
        msg = "Are you sure you wish to uninstall " + pkglist.get(pkglist.curselection()).decode('utf-8') + "?"
        if messagebox.askyesno("Confirmation", msg):
            uninstall_package(pkglist.get(pkglist.curselection()))
    except TclError:
        pass


tkinter.Button(window, text='Uninstall', command=uninstall).pack()
refresh()
window.mainloop()
