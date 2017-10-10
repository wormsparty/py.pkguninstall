#!/usr/bin/env python3

import os
import sys
import subprocess
import tkinter
from tkinter import messagebox

# First create the window
window = tkinter.Tk()

# Let's construct the list which will contain all packages we can uninstall
tkinter.Label(window, text='Select a package to uninstall:').pack()

list = tkinter.Listbox(window, width=50)
list.pack()


def refresh():
    list.delete(0, list.size())

    # Let's list the packages
    pkgutil = subprocess.Popen(('pkgutil', '--pkgs'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('grep', '-v', '^com.apple.'), stdin=pkgutil.stdout).splitlines()

    # We now fill the list
    i = 1

    for o in output:
        list.insert(i, o)
        i += 1


def remove_file(f):
    if os.path.exists(f) and not os.path.isdir(f):
        os.remove(f)

    try:
        os.removedirs(os.path.dirname(f))
    except OSError:
        pass


def uninstall_package(pkg):
    directory = os.path.dirname(os.path.realpath(__file__))
    script = 'do shell script "' + sys.executable + ' ' + \
             directory + '/pkguninstall.py -y ' + pkg.decode('utf-8') + '" with administrator privileges'
    print(script)
    subprocess.call(['osascript', '-e', script])
    refresh()


def uninstall():
    if messagebox.askyesno("Confirmation", "Are you sure you wish to uninstall " + list.get(list.curselection()).decode('utf-8') + "?"):
        uninstall_package(list.get(list.curselection()))


tkinter.Button(window, text='Refresh', command=refresh).pack()
tkinter.Button(window, text='Uninstall', command=uninstall).pack()

refresh()

window.mainloop()

