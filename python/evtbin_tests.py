#!/usr/bin/env python
"""
Exercise evtbin PHA and CMAP using Crab-only obsSim data.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from getApp import GtApp
from obsSim_tests import sourceNamesDat, xmlFilesDat

obsSim = GtApp('obsSim', 'observationSim')
filter = GtApp('dataSubselector')               
evtbin = GtApp('evtbin')

def Crab_only():
    sourceNamesDat(srcList=('_3EG_J0534p2200-32mev',))
    xmlFilesDat()
    obsSim['XML_source_file'] = 'xmlFiles.dat'
    obsSim['Source_list'] = 'source_names.dat'
    obsSim['Output_file_prefix'] = 'Crab'
    obsSim['Response_functions'] = irfs
    obsSim.run()

def Crab_filter():
    filter['input_file'] = 'Crab_events_0000.fits'
    filter['output_file'] = 'Crab_events_filtered.fits'
    filter['ra'] = 83.57
    filter['dec'] = 22.01
    filter['rad'] = 20
    filter['convLayerMin'] = 0
    filter['convLayerMax'] = 11
    filter.run()

def Crab_cmap():
    evtbin['algorithm'] = 'CMAP'
    evtbin['outfile'] = 'Crab_cmap.fits'
    evtbin['numxpix'] = 100
    evtbin['numypix'] = 100
    evtbin['pixscale'] = 0.5
    evtbin['xref'] = 83
    evtbin['yref'] = 22
    evtbin['uselb'] = 'no'
    evtbin.run()

def Crab_pha():
    evtbin['algorithm'] = 'PHA1'
    evtbin['outfile'] = 'Crab.pha'
    evtbin.run()

def Crab_lc():
    evtbin['algorithm'] = 'LC'
    evtbin['outfile'] = 'Crab.lc'
    evtbin['tstart'] = 0
    evtbin['tstop'] = 8.64e4
    evtbin['deltatime'] = 1e3
    evtbin.run()

def run():
    Crab_only()
    Crab_filter()
    Crab_pha()
    Crab_cmap()
    Crab_lc()

if __name__ == "__main__":
    run()
