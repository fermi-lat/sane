#!/usr/bin/env python
"""
Generate test data with dataSubselector.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from getApp import GtApp

filter = GtApp('dataSubselector')

def run(clean=False):
    filter['input_file'] = 'test_events_0000.fits'
    filter['output_file'] = 'filtered_events_0000.fits'
    filter['ra'] = 86.4
    filter['dec'] = 28.9
    filter['rad'] = 30
    filter.run()

if __name__ == "__main__":
    run()
