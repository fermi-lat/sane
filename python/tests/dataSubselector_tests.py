#!/usr/bin/env python
"""
Generate test data with dataSubselector.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from gt_apps import filter, maketime

def run(clean=False):
    maketime['scfile'] = 'orbSim_scData_0000.fits'
    maketime['evfile'] = 'test_events_0000.fits'
    maketime['filter'] = 'IN_SAA!=T'
    maketime['outfile'] = 'test_events.fits'
    maketime.run()
    filter['infile'] = 'test_events.fits'
    filter['outfile'] = 'filtered_events_0000.fits'
    filter['ra'] = 90
    filter['dec'] = 20
    filter['rad'] = 20.0
    filter['tmin'] = 0.0
    filter['tmax'] = 0.0
    filter['emin'] = 32.0
    filter['emax'] = 200000.0
    filter.run()

if __name__ == "__main__":
    run()
