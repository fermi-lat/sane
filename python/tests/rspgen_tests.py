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
    rspgen['dcostheta'] = 0.025
    rspgen['ebinalg'] = 'LOG'
    rspgen['emin'] = 30.0
    rspgen['emax'] = 200000.0
    rspgen['enumbins'] = 20
    rspgen['denergy'] = 0.0
    rspgen['irfs'] = 'DC1F'
    rspgen.run()

if __name__ == "__main__":
    run()
