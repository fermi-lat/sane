#!/usr/bin/env python
"""
Interface to .par files.

@author J. Chiang
"""
#
#$Header$
#

def accept(line):
    if (line.find('#') == 0 or len(line.split()) == 0):
        return 0
    return 1

def name(line):
    return line.split(',')[0].strip()

def fields(line):
    return [item.strip() for item in line.split(',')[1:]]

class Pil(object):
    def __init__(self, parfile, raiseKeyErrors=True):
        self.raiseKeyErrors = raiseKeyErrors
        self.params = {}
        self.names = []
        file = open(parfile, 'r')
        for line in file:
            if accept(line):
                self.params[name(line)] = fields(line)
                self.names.append(name(line))
    def keys(self):
        return self.names
    def __getitem__(self, name):
        return (self.params[name][2]).strip('"').strip("'")
    def __setitem__(self, name, value):
        if name in self.names:
            self.params[name][2] = `value`
        elif self.raiseKeyErrors:
            raise KeyError, name
    def __call__(self):
        args = ''
        for name in self.keys():
            args += ' ' + self.__getitem__(name)
        return args

if __name__ == '__main__':
    pars = Pil('../data/likelihood.par')
    print pars['event_file']
    print pars['Spacecraft_file_hdu']
    pars['Spacecraft_file_hdu'] = 3
    pars['event_file'] = 'foo'
    print pars['Spacecraft_file_hdu']
    try:
        pars['wrong_parameter'] = 0
    except KeyError, name:
        print "KeyError exception raised for", name
    print pars()

