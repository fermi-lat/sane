#!/usr/bin/env python

import sys, os
from pil import Pil

bindir = os.environ['BINDIR']

def getApp(appName, package=None, raiseKeyErrors=True):
    if not package:
        package = appName
    app = os.path.join(os.environ[package.upper() + 'ROOT'], bindir,
                       appName + '.exe')
    pars = Pil(appName + '.par', raiseKeyErrors)
    return (app, pars)

class GtApp(object):
    def __init__(self, appName, package=None, raiseKeyErrors=True):
        self.app, self.pars = getApp(appName, package, raiseKeyErrors)
    def __setitem__(self, key, value):
        self.pars[key] = value
    def __getitem__(self, key):
        return self.pars[key]
    def run(self, print_command=True):
        if print_command:
            print self.command()
        os.system(self.command())
    def runWithOutput(self):
        input, output = os.popen2(self.command())
        return input, output
    def command(self):
        return self.app + self.pars()

if __name__ == '__main__':
    orbSim = GtApp('orbSim', 'observationSim')
    orbSim['Output_file_prefix'] = 'gtApp_test'
    input, output = orbSim.runWithOutput()
    for line in output:
        print line.strip('\n')
