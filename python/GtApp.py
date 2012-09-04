#!/usr/bin/env python
"""
Provide a unified interface to FTOOL and par file.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#
import sys, os
import subprocess
from pil import Pil
from facilities import py_facilities
os_environ = py_facilities.commonUtilities_getEnvironment

_failed_exes = []

#bindir = os.environ['BINDIR']
bindir = os_environ('BINDIR')

def getApp(appName, package=None, raiseKeyErrors=True,
           preserveQuotes=False):
    if not package:
        package = appName
    try:
#        app = os.path.join(os.environ[package.upper() + 'ROOT'], bindir,
        app = os.path.join(os_environ(package.upper() + 'ROOT'), bindir,
                           appName + '.exe')
        if not os.path.exists(app): # assume it lives in the users PATH
            app = appName
    except KeyError:
        app = appName # assume it lives in the users PATH
    pars = Pil(appName + '.par', raiseKeyErrors, preserveQuotes)
    return (app, pars)

class GtApp(object):
    def __init__(self, appName, package=None, raiseKeyErrors=True,
                 preserveQuotes=False):
        self.app, self.pars = getApp(appName, package, raiseKeyErrors,
                                     preserveQuotes)
        self.appName = appName
    def __setitem__(self, key, value):
        self.pars[key] = value
    def __getitem__(self, key):
        return self.pars[key]
    def __getattr__(self, attrname):
        return getattr(self.pars, attrname)
    def run(self, print_command=True, catchError="at the top level:", 
            dry_run=False, **kwds):
        for item in kwds.keys():
            if self.pars.has_key(item):
                self.pars[item] = kwds[item]
        try:
            if self.pars['chatter'] == 0:
                print_command = False
        except KeyError:
            pass
        if dry_run:
            return self.command()
        if catchError is not None:
            input, output = self.runWithOutput(print_command)
            for line in output:
                print line.strip("\n")
                if line.find(catchError) != -1:
                    _failed_exes.append(self.app)
                    input.close()
                    output.close()
                    raise RuntimeError, self.appName + " execution failed"
            input.close()
            output.close()
        else:
            if print_command:
                print self.command()
#            retcode = os.system(self.command(do_timing=print_command))
            retcode = subprocess.call(self.command(do_timing=print_command),
                                      shell=True)
            if retcode != 0:
                _failed_exes.append(self.app)
                raise RuntimeError, self.appName + " execution failed"
    def runWithOutput(self, print_command=True):
        if print_command:
            print self.command()
        process = subprocess.Popen(self.command(print_command),
                                   shell=True, bufsize=-1,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   close_fds=True)
        return (process.stdin, process.stdout)
    def command(self, do_timing=True):
        chatter = 2
        try:
            chatter = self.pars['chatter']
        except KeyError:
            pass
        if do_timing and os.name == 'posix' and chatter != 0:
            return 'time -p ' + self.app + self.pars()
        else:
            return self.app + self.pars()

if __name__ == '__main__':
    orbSim = GtApp('orbSim', 'observationSim')
    orbSim['Output_file_prefix'] = 'gtApp_test'
    input, output = orbSim.runWithOutput()
    for line in output:
        print line.strip('\n')
