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
    def run(self, print_command=True, catchError="at the top level:"):
        if print_command:
            print self.command()
        if catchError is not None:
            input, output = self.runWithOutput()
            for line in output:
                print line.strip("\n")
                if line.find(catchError) != -1:
                    return sys.exit(1)
        else:
            os.system(self.command())
    def runWithOutput(self):
        if os.name == 'posix':
            input, output = os.popen4(self.command())
        else:
            import win32pipe
            output, input = win32pipe.popen4(self.command())
        return input, output
    def command(self):
        return self.app + self.pars()

if __name__ == '__main__':
    orbSim = GtApp('orbSim', 'observationSim')
    orbSim['Output_file_prefix'] = 'gtApp_test'
    input, output = orbSim.runWithOutput()
    for line in output:
        print line.strip('\n')
