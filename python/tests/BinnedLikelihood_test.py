"""
Binned likelihood tests.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from obsSim_tests import sourceNamesDat, random_int
from gt_apps import obsSim, counts_map, expCube, srcMaps, like

makeCube = expCube
likelihood = like

def generateData():
    sourceNamesDat(srcList=('anticenter-32mev',))
    obsSim["xml_source_file"] = "anticenter_sources.xml"
    obsSim["outfile_prefix"] = "ptsrcs"
    obsSim['scfile'] = "none"
    obsSim["rspfunc"] = irfs
    obsSim["emin"] = 32
    obsSim["emax"] = 2e5
    obsSim["random_seed"] = random_int()
    obsSim.run()

def makeCountsMap():
    counts_map['evfile'] = 'ptsrcs_events_0000.fits'
    counts_map['scfile'] = 'ptsrcs_scData_0000.fits'
    counts_map['outfile'] = 'countsMap.fits'
    counts_map["emin"] = 32
    counts_map["emax"] = 2e5
    counts_map.run()

def makeExposureCube():
    makeCube['scfile'] = 'ptsrcs_scData_0000.fits'
    makeCube['outfile'] = 'expcube_1_day.fits'
    makeCube.run()
    
def makeSourceMaps():
    srcMaps["scfile"] = 'ptsrcs_scData_0000.fits'
    srcMaps['counts_map_file'] = counts_map['outfile']
    srcMaps['source_model_file'] = 'ptsrcModel.xml'
    srcMaps['outfile'] = 'sourceMaps.fits'
    srcMaps['binned_exposure_map'] = 'none'
    srcMaps["rspfunc"] = irfs
    srcMaps.run()

def runLikelihood():
    likelihood['scfile'] = 'ptsrcs_scData_0000.fits'
    likelihood['statistic'] = 'BINNED'
    likelihood['source_model_file'] = 'ptsrcModel.xml'
    likelihood["rspfunc"] = irfs
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
