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

obsSim = GtApp('obsSim', 'observationSim')
counts_map = GtApp('gtcntsmap', 'Likelihood')
makeCube = GtApp('makeExposureCube', 'Likelihood')
srcMaps = GtApp('gtsrcmaps', 'Likelihood')

def generateData():
    sourceNamesDat(srcList=('anticenter-32mev',))
    obsSim["xml_source_file"] = "anticenter_sources.xml"
    obsSim["outfile_prefix"] = "ptsrcs"
    obsSim['scfile'] = "none"
    obsSim["rspfunc"] = irfs
    obsSim.run()

def makeCountsMap():
    counts_map['event_file'] = 'ptsrcs_events_0000.fits'
    counts_map['spacecraft_file'] = 'ptsrcs_scData_0000.fits'
    counts_map['output_file_name'] = 'countsMap.fits'
    counts_map.run()

def makeExposureCube():
    makeCube['Spacecraft_file'] = 'ptsrcs_scData_0000.fits'
    makeCube['Output_file'] = 'expcube_1_day.fits'
    makeCube.run()
    
def makeSourceMaps():
    srcMaps["Spacecraft_file"] = 'ptsrcs_scData_0000.fits'
    srcMaps['counts_map_file'] = counts_map['output_file_name']
    srcMaps['source_model_file'] = 'ptsrcModel.xml'
    srcMaps['output_file'] = 'sourceMaps.fits'
    srcMaps['binned_exposure_map'] = 'none'
    srcMaps["Response_functions"] = irfs
    srcMaps.run()

def runLikelihood():
    likelihood = GtApp('likelihood', 'Likelihood')
    likelihood['Spacecraft_file'] = 'ptsrcs_scData_0000.fits'
    likelihood['Statistic'] = 'BINNED'
    likelihood['Source_model_file'] = 'ptsrcModel.xml'
    likelihood["Response_functions"] = irfs
    likelihood['counts_map_file'] = 'sourceMaps.fits'
    likelihood['exposure_cube_file'] = 'expcube_1_day.fits'
    likelihood['binned_exposure_map'] = 'none'
    likelihood.run()

def run():
    generateData()
    makeCountsMap()
#    makeExposureCube()
    makeSourceMaps()
    runLikelihood()

if __name__ == "__main__":
    run()
