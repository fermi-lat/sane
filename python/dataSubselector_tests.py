#!/usr/bin/env python
"""
Generate test data with dataSubselector.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *

dataSubselectorRoot = os.environ["DATASUBSELECTORROOT"]
dataSubselectorApp = os.path.join(dataSubselectorRoot, bindir,
                                  'dataSubselector.exe')
dataSubselectorPar = os.path.join(sysData, 'dataSubselector.par')

def run(clean=False):
    pars = Pil(dataSubselectorPar)
    pars['input_file'] = 'test_events_0000.fits'
    pars['output_file'] = 'filtered_events_0000.fits'
    pars['ra'] = 86
    pars['dec'] = 29
    pars['rad'] = 20
    command = dataSubselectorApp + pars()
    print command
    os.system(command)

if __name__ == "__main__":
    run()
