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

import obsSim_tests as obsSim
import map_tools_tests as map_tools
import dataSubselector_tests as dataSubselector
import Likelihood_tests as like
import BinnedLikelihood_test as binned_test
import evtbin_tests as evtbin
import rspgen_tests as rspgen
import Pulsar_tests as pulsars

from pil import Pil

if __name__ == "__main__":
    cleanUp = False
    try:
        obsSim.run(cleanUp)
        dataSubselector.run(cleanUp)
        like.run(cleanUp)
        binned_test.run()
        evtbin.run()
        rspgen.run()
        pulsars.run()
        map_tools.run(cleanUp)
    except:
        sys.exit(1)
