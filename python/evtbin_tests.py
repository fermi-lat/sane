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
from obsSim_tests import sourceNamesDat

obsSim = GtApp('obsSim', 'observationSim')
filter = GtApp('dataSubselector')               
evtbin = GtApp('evtbin')

def Crab_only():
    sourceNamesDat(srcList=('_3EG_J0534p2200-32mev',))
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
    filter.run()

def run():
    Crab_only()
    Crab_filter()
    evtbin.run()

if __name__ == "__main__":
    run()
