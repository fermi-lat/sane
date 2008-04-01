#!/usr/bin/env python
"""
Exercise evtbin PHA and CMAP using Crab-only obsSim data.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from obsSim_tests import sourceNamesDat, xmlFilesDat, random_int
from gt_apps import obsSim, filter, evtbin

def Crab_only():
    sourceNamesDat(srcList=('_3EG_J0534p2200-32mev',))
    xmlFilesDat()
    obsSim['infile'] = 'xmlFiles.txt'
    obsSim['srclist'] = 'source_names.txt'
    obsSim['evroot'] = 'Crab'
    obsSim['scfile'] = 'none'
    obsSim['irfs'] = irfs
    if irfs == 'DSS':
        obsSim['irfs'] = 'DC2'
    obsSim['use_ac'] = 'no'
    obsSim['seed'] = random_int()
    obsSim.run()

def Crab_filter():
    filter['infile'] = 'Crab_events_0000.fits'
    filter['outfile'] = 'Crab_events_filtered.fits'
    filter['ra'] = 83.57
    filter['dec'] = 22.01
    filter['rad'] = 20
    filter['tmin'] = 0
    filter['tmax'] = 0
#    filter['eventClass'] = 0
    filter.run()

def Crab_cmap(useWorkAround=False):
    evtbin['algorithm'] = 'CMAP'
    evtbin['evfile'] = 'Crab_events_filtered.fits'
    evtbin['outfile'] = 'Crab.fits'
    evtbin['scfile'] = 'Crab_scData_0000.fits'
    evtbin['tbinalg'] = 'LIN'
    evtbin['tstart'] = 0.
    evtbin['tstop'] = 86400.
    evtbin['dtime'] = 1000.0
    evtbin['tbinfile'] = 'numxpix=100'
    evtbin['nxpix'] = 100
    evtbin['nypix'] = 100
    evtbin['binsz'] = 0.5
    evtbin['coordsys'] = 'CEL'
    evtbin['xref'] = 83.0
    evtbin['yref'] = 22.0
    evtbin['axisrot'] = 0.0
    evtbin['ebinalg'] = 'LOG'
    evtbin['emin'] = 30.0
    evtbin['emax'] = 200000.0
    evtbin['enumbins'] = 20
    evtbin['denergy'] = 0.0
    evtbin['proj'] = 'CAR'
    evtbin['snratio'] = 1
    evtbin['lcemin'] = 0
    evtbin['lcemax'] = 0
    if useWorkAround:
        evtbin.write()
    evtbin.run()

def Crab_pha():
    evtbin['algorithm'] = 'PHA1'
    evtbin['outfile'] = 'Crab.pha'
    evtbin.write()
    evtbin.run()

def Crab_lc():
    evtbin['algorithm'] = 'LC'
    evtbin['outfile'] = 'Crab.lc'
    evtbin['tstart'] = 0
    evtbin['tstop'] = 8.64e4
    evtbin['dtime'] = 1e3
    evtbin.write()
    evtbin.run()

def run(useWorkAround=False):
    Crab_only()
    Crab_filter()
    Crab_cmap(useWorkAround)
    Crab_pha()
    Crab_lc()

if __name__ == "__main__":
    run(True)
