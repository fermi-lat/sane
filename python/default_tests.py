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

if __name__ == "__main__":
    cleanUp = False

    obsSim.run(cleanUp)
    map_tools.run(cleanUp)
    dataSubselector.run(cleanUp)
    like.run(cleanUp)
    #obsSim.compareFit(cleanUp)
