"""
This module uses GtApp to wraps the Science Tools as python objects.
"""
from getApp import GtApp

#
# Likelihood applications
#
expCube = GtApp('gtlivetimecube', 'Likelihood')
expMap = GtApp('gtexpmap', 'Likelihood')
diffResps = GtApp('gtdiffresp', 'Likelihood')
like = GtApp('gtlikelihood', 'Likelihood')
TsMap = GtApp('gttsmap', 'Likelihood')

counts_map = GtApp('gtcntsmap', 'Likelihood')
srcMaps = GtApp('gtsrcmaps', 'Likelihood')

#
# observationSim
#
obsSim = GtApp('gtobssim', 'observationSim')
orbSim = GtApp('gtorbsim', 'observationSim')

#
# dataSubselector
#
filter = GtApp('gtselect', 'dataSubselector')

#
# Pulsar-related
#
pulsePhase = GtApp('pulsePhase')
psearch = GtApp('gtpsearch', 'periodSearch')

#
# map_tools
#
count_map = GtApp('count_map', 'map_tools')

#
# others
#
evtbin = GtApp('gtbin', 'evtbin')
rspgen = GtApp('gtrspgen', 'rspgen')



