#!/usr/bin/env python
"""
Exercise evtbin PHA and CMAP using Crab-only obsSim data.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from obsSim_tests import obsSimPar, obsSimApp, sourceNamesDat
from dataSubselector_tests import dataSubselectorPar, dataSubselectorApp

evtbinRoot = os.environ["EVTBINROOT"]
evtbin = os.path.join(evtbinRoot, bindir, 'evtbin.exe')
evtbinPar = os.path.join(sysData, 'evtbin.par')

def Crab_only():
    sourceNamesDat(srcList=('_3EG_J0534p2200-32mev',))
    pars = Pil(obsSimPar)
    pars['XML_source_file'] = 'xmlFiles.dat'
    pars['Source_list'] = 'source_names.dat'
    pars['Output_file_prefix'] = 'Crab'
    pars['Response_functions'] = irfs
    command = obsSimApp + pars()
    print command
    os.system(command)    

def Crab_filter():
    pars = Pil(dataSubselectorPar)
    pars['input_file'] = 'Crab_events_0000.fits'
    pars['output_file'] = 'Crab_events_filtered.fits'
    pars['ra'] = 83.57
    pars['dec'] = 22.01
    pars['rad'] = 20
    command = dataSubselectorApp + pars()
    print command
    os.system(command)

def run():
    Crab_only()
    Crab_filter()
    pars = Pil(evtbinPar)
    command = evtbin + pars()
    print command
    os.system(command)

if __name__ == "__main__":
    run()
