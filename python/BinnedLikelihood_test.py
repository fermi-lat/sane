"""
Binned likelihood tests.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from getApp import GtApp, getApp
from obsSim_tests import sourceNamesDat

def generateData():
    obsSim = GtApp('obsSim', 'observationSim')
    sourceNamesDat(srcList=('anticenter-32mev',))
    obsSim["XML_source_file"] = "anticenter_sources.xml"
    obsSim["Output_file_prefix"] = "ptsrcs"
    obsSim['Pointing_history_file'] = "none"
    obsSim["Response_functions"] = irfs
    obsSim.run()

def makeCountsMap():
    counts_map = GtApp('gtcntsmap', 'Likelihood')
    counts_map.run()

def makeExposureCube():
    makeCube = GtApp('makeExposureCube', 'Likelihood')
    makeCube['Spacecraft_file'] = 'ptsrcs_scData_0000.fits'
    makeCube['Output_file'] = 'expcube_1_day.fits'
    makeCube.run()
    
def makeSourceMaps():
    srcMaps = GtApp('gtsrcmaps', 'Likelihood')
    srcMaps["Response_functions"] = irfs
    srcMaps.run()

def runLikelihood():
    likelihood = GtApp('likelihood', 'Likelihood')
    likelihood['Statistic'] = 'BINNED'
    likelihood['Source_model_file'] = 'ptsrcModel.xml'
    likelihood["Response_functions"] = irfs
    likelihood.run()

def run():
    generateData()
    makeCountsMap()
#    makeExposureCube()
    makeSourceMaps()
    runLikelihood()

if __name__ == "__main__":
    run()
