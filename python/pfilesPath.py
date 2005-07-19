#!/usr/bin/env python
"""
Search the PFILES environment variable for the first instance of the
desired .par file.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os, sys, re

ParFileError = 'ParFileError'
def pfilesPath(parfile):
    try:
        paths = re.split(r"[;:]", os.environ['PFILES'])
        paths = [path for path in paths if path != ""]
    except KeyError:
        print "Your PFILES environment variable is not set."
        raise KeyError
    for path in paths:
        try:
            if parfile in os.listdir(path):
                return path
        except OSError:
            pass
    raise ParFileError, ".par file " + parfile + " not found."

if __name__ == "__main__":
    if len(sys.argv) == 2:
        parfile = sys.argv[1]
    else:
        parfile = 'likelihood.par'
    print pfilesPath(parfile)
