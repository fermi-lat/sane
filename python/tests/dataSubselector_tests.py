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

def run(clean=False):
    gtmktime['scfile'] = 'orbSim_scData_0000.fits'
    gtmktime['evfile'] = 'test_events_0000.fits'
    gtmktime['filter'] = 'IN_SAA!=T'
    gtmktime['outfile'] = 'test_events.fits'
    gtmktime.run()

    gtselect['infile'] = 'test_events.fits'
    gtselect['outfile'] = 'filtered_events_0000.fits'
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
    gtselect['irfs'] = irfs0
    gtselect.run()

if __name__ == "__main__":
    run()
