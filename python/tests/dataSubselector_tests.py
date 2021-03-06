#!/usr/bin/env python
"""
Generate test data with dataSubselector.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from GtApp import GtApp

gtselect = GtApp('gtselect', 'dataSubselector')
gtmktime = GtApp('gtmktime', 'dataSubselector')
gtvcut = GtApp('gtvcut')

def run(clean=False):
    gtmktime['scfile'] = 'orbSim_scData_0000.fits'
    gtmktime['evfile'] = 'test_events_0000.fits'
    gtmktime['filter'] = 'IN_SAA!=T'
    gtmktime['outfile'] = 'test_events.fits'
    gtmktime.run()

    gtvcut.run(infile=gtmktime['outfile'], table='EVENTS')

    gtselect['infile'] = 'test_events.fits'
    gtselect['outfile'] = 'filtered_events_0000.fits'
    if irfs0 == 'P8R2_SOURCE_V6':
        gtselect['evtype'] = 48
    gtselect['ra'] = 90
    gtselect['dec'] = 20
    gtselect['rad'] = 20.0
    gtselect['tmin'] = 0.0
    gtselect['tmax'] = 0.0
    gtselect['emin'] = 32.0
    if model_type == 'GALPROP_DIFFUSE':
        gtselect['emax'] = 1e5
    else:
        gtselect['emax'] = 200000.0
    gtselect.run()

    gtvcut.run(infile=gtselect['outfile'], table='EVENTS')

if __name__ == "__main__":
    run()
