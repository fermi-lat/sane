#!/usr/bin/env python
"""
System tests for Science Tools

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os
import sys

sys.path.append(os.path.join(os.environ["SANEROOT"], "python"))

from setPaths import *
import GtApp

import obsSim_tests as obsSim
import dataSubselector_tests as dataSubselector
import Likelihood_tests as like
import BinnedLikelihood_test as binned_test
import evtbin_tests as evtbin
import rspgen_tests as rspgen
import Pulsar_tests as pulsars

if __name__ == "__main__":
    cleanUp = False
    useWorkAround = True
    obsSim.run(cleanUp)
    dataSubselector.run(cleanUp)
    like.run(cleanUp)
    binned_test.run()
    evtbin.run(useWorkAround)
    rspgen.run()
    pulsars.run(useWorkAround)
    if GtApp._failed_exes:
        print "The following executables failed: "
        for exe in GtApp._failed_exes:
            print exe
        sys.exit(1)

    #
    # Test importing Toby's package.
    #
    import pointfit
    pointfit.Background

## clean up
#    removeFile('*.fits')
#    removeFile('Crab*')
#    removeFile('*.par')    
#    removeFile('*.dat')
#    removeFile('*.txt')
