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
    filter['rad'] = 22.0
    filter['lonMin'] = 0.0
    filter['lonMax'] = 360.0
    filter['latMin'] = -90.0
    filter['latMax'] = 90.0
    filter['coordSys'] = 'CEL'
    filter['tmin'] = 0.0
    filter['tmax'] = 0.0
    filter['emin'] = 30.0
    filter['emax'] = 200000.0
    filter['convLayerMin'] = 0
    filter['convLayerMax'] = 15
    filter['thetamin'] = 0.0
    filter['thetamax'] = 0.0
    filter['phimin'] = 0.0
    filter['phimax'] = 0.0
    filter['gammaProbMin'] = 0.0
    filter['gammaProbMax'] = 0.0
    filter['zmin'] = 0.0
    filter['zmax'] = 0.0
    filter['bgcut'] = 'yes'
    filter['psfcut'] = 'yes'
    filter['erescut'] = 'yes'
    filter.run()

if __name__ == "__main__":
    run()
