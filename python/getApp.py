#!/usr/bin/env python
"""
Provide a unified interface to FTOOL and par file.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#
import sys, os
from pil import Pil

_failed_exes = []

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
    def __getattr__(self, attrname):
        return getattr(self.pars, attrname)
    def run(self, print_command=True, catchError="at the top level:"):
        if catchError is not None:
            input, output = self.runWithOutput(print_command)
            for line in output:
                print line.strip("\n")
                if line.find(catchError) != -1:
                    _failed_exes.append(self.app)
#                    return sys.exit(1)
        else:
            if print_command:
                print self.command()
            retcode = os.system(self.command())
            if retcode != 0:
                _failed_exes.append(self.app)
#                return sys.exit(1)
    def runWithOutput(self, print_command=True):
        if print_command:
            print self.command()
        return os.popen4(self.command())
    def command(self):
        return self.app + self.pars()

if __name__ == '__main__':
    orbSim = GtApp('orbSim', 'observationSim')
    orbSim['Output_file_prefix'] = 'gtApp_test'
    input, output = orbSim.runWithOutput()
    for line in output:
        print line.strip('\n')
