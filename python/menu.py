#!/bin/env python
# $Header$

import sys, time, os, copy
from Tkinter import *
from tkMessageBox import *

class RunProgram:
    def __init__(self, name, command):
        self.name = name
        self.command = command
    def __call__(self):                   #  button press callback
        print "executing ", self.command
        if sys.platform[:3] == 'win':
            os.system( 'start ' + '"' + self.name
                       + '" /BELOWNORMAL cmd /k ' + self.command )
        else:
            os.system('/usr/X11R6/bin/xterm -sb -sl 1000 -title "' + 
                      self.name + '" -e nice ' + self.command + ' &')

def runLauncher(tools, title):
    # put up a simple launcher bar for later use
    root = Tk()
    root.title(title)
    for (name, commandLine) in tools:
        b = Button(root, text=name, fg='black', bg='beige', border=2,   
                   command = RunProgram(name, commandLine))
        b.pack(side=LEFT, expand=YES, fill=BOTH)
    root.mainloop()

def get_tools(env):
    applist = os.environ[env].strip(os.pathsep).split(os.pathsep);
    tools = []
    for app_entry in applist:
        tools.append(app_entry.split( '='))
    return tools
    
def run_launcher(packages, title='Science Tools'):
    root = Tk()
    root.title(title)
    menuBar = MenuBar(root, packages)
    root.mainloop()

class MenuBar(Menu):
    def __init__(self, root, packages):
        Menu.__init__(self)
        for item in packages:
            self.add_cascade(label=item, underline=0,
                             menu=PackageMenu(root, packages[item]))
        root.config(menu=self, width=100*len(packages.keys()))

class PackageMenu(Menu):
    def __init__(self, root, package):
        Menu.__init__(self)
        for (appName, exe) in package:
            self.add_command(label=appName, command=RunProgram(appName, exe))

def getTools(env):
    applist = os.environ[env].strip(os.pathsep).split(os.pathsep);
    tools = {}
    for app_entry in applist:
        package, app, exe = parse_entry(app_entry)
        if not tools.has_key(package):
            tools[package] = []
        tools[package].append((app, exe))
    return tools

def parse_entry(entry):
    bindir = os.path.sep + os.environ["BINDIR"]
    app, exe = entry.split("=")
    exe += ' mode=ql'
    package = exe.split(bindir)[0].split(os.path.sep)[-2]
    return package, app, exe

if __name__ == '__main__':
#    showinfo(title, 'starting')
#    runLauncher( tools=get_tools('ST_apps'), title="Science Tools")
    run_launcher(getTools('ST_apps'))
