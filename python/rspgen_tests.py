#!/usr/bin/env python
"""
Exercise rspgen.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from getApp import GtApp

def run():
    rspgen = GtApp('rspgen')
    rspgen.run()

if __name__ == "__main__":
    run()
