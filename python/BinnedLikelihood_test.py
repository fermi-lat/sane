"""
Binned likelihood tests.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from getApp import getApp
from obsSim_tests import sourceNamesDat

def generateData():
    (obsSim, pars) = getApp('obsSim', 'observationSim')
    sourceNamesDat(srcList=('anticenter-32mev',))
    pars["Output_file_prefix"] = "ptsrcs"
    pars["Response_functions"] = irfs
    command = obsSim + pars()
    os.system(command)

def makeCountsMap():
    (counts_map, pars) = getApp('gtcntsmap', 'Likelihood')
    command = counts_map + pars()
    os.system(command)

def makeExposureCube():
    (makeCube, pars) = getApp('makeExposureCube', 'Likelihood')
    pars['Spacecraft_file'] = 'ptsrcs_scData_0000.fits'
    pars['Output_file'] = 'expcube_1_day.fits'
    command = makeCube + pars()
    os.system(command)
    
def makeSourceMaps():
    (srcMaps, pars) = getApp('gtsrcmaps', 'Likelihood')
    pars["Response_functions"] = irfs
    command = srcMaps + pars()
    os.system(command)

def runLikelihood():
    (likelihood, pars) = getApp('likelihood', 'Likelihood')
    pars['Statistic'] = 'BINNED'
    pars['Source_model_file'] = 'ptsrcModel.xml'
    pars["Response_functions"] = irfs
    command = likelihood + pars()
    os.system(command)

def run():
    generateData()
    makeCountsMap()
#    makeExposureCube()
    makeSourceMaps()
    runLikelihood()

if __name__ == "__main__":
    run()
