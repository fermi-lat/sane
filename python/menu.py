#!/bin/env python

import sys, time, os
from Tkinter import *
from tkMessageBox import *

class RunProgram:
    def __init__(self, name, command):
        self.name = name
        self.command = command
    def __call__(self):                   #  button press callback
        print "executing ", self.command
        if sys.platform[:3] == 'win':
            os.system( 'start ' + '"' + self.name + '" /BELOWNORMAL cmd /k ' + self.command )
        else:
            pass
            
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
    if sys.platform[:3] == 'win': char=";" 
    else: char=":"
    applist = os.environ[env].split(char);
    tools = []
    for app_entry in applist:
        tools.append(app_entry.split( '='))
    return tools
    
title = "Science Tools"
#showinfo(title, 'starting')
runLauncher( get_tools('ST_apps'), title)
