#!/usr/bin/env python
"""
Exercise rspgen.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from gt_apps import rspgen

def run():
    rspgen['respalg'] = 'PS'
    rspgen['specfile'] = 'Crab.pha'
    rspgen['scfile'] = 'Crab_scData_0000.fits'
    rspgen['outfile'] = 'Crab.rsp'
    rspgen['time'] = 1000.0
    rspgen['thetacut'] = 70.0
    rspgen['thetabinsize'] = 1.0
    rspgen['energybinalg'] = 'LOG'
    rspgen['emin'] = 30.0
    rspgen['emax'] = 200000.0
    rspgen['enumbins'] = 20
    rspgen['deltaenergy'] = 0.0
    rspgen['resptype'] = 'DC1F'
    rspgen.run()

if __name__ == "__main__":
    run()
