"""
Binned likelihood tests.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from obsSim_tests import sourceNamesDat, random_int
from gt_apps import obsSim, counts_map, expCube, srcMaps, like, model_map

makeCube = expCube
likelihood = like

#def generateData():
#    sourceNamesDat(srcList=('anticenter-32mev',))
#    obsSim["xml_source_file"] = "anticenter_sources.xml"
#    obsSim["outfile_prefix"] = "ptsrcs"
#    obsSim['scfile'] = "none"
#    obsSim["rspfunc"] = irfs
#    obsSim["emin"] = 32
#    obsSim["emax"] = 2e5
#    obsSim["random_seed"] = random_int()
#    obsSim.run()

def makeCountsMap():
    counts_map['evfile'] = 'filtered_events_0000.fits'
    counts_map['scfile'] = 'orbSim_scData_0000.fits'
    counts_map['outfile'] = 'countsMap.fits'
    counts_map["emin"] = 32
    counts_map["emax"] = 2e5
    counts_map.run()

#def makeExposureCube():
#    makeCube['evfile'] = 'filtered_events_0000.fits'
#    makeCube['scfile'] = 'orbSim_scData_0000.fits'
#    makeCube['outfile'] = 'expcube_1_day.fits'
#    makeCube.run()
    
def makeSourceMaps():
    srcMaps["scfile"] = 'orbSim_scData_0000.fits'
    srcMaps['counts_map_file'] = counts_map['outfile']
    srcMaps['source_model_file'] = 'srcModel.xml'
    srcMaps['outfile'] = 'sourceMaps.fits'
    srcMaps['exposure_cube_file'] = 'expcube_1_day.fits'
    srcMaps['binned_exposure_map'] = 'binned_exposure.fits'
    srcMaps["rspfunc"] = irfs
    srcMaps.run()

def runLikelihood():
    likelihood['scfile'] = 'orbSim_scData_0000.fits'
    likelihood['statistic'] = 'BINNED'
    likelihood['source_model_file'] = 'srcModel.xml'
    likelihood["rspfunc"] = irfs
    likelihood['counts_map_file'] = 'sourceMaps.fits'
    likelihood['exposure_cube_file'] = 'expcube_1_day.fits'
    likelihood['binned_exposure_map'] = 'binned_exposure.fits'
    likelihood['optimizer'] = 'MINUIT'
    likelihood.run()

def makeModelMap():
    model_map['srcmaps'] = likelihood['counts_map_file']
    model_map['source_model_file'] = likelihood['source_model_file']
    model_map['outfile'] = 'model_map.fits'
    model_map.run()

def run():
#    generateData()
    makeCountsMap()
#    makeExposureCube()
    makeSourceMaps()
    runLikelihood()
    makeModelMap()

if __name__ == "__main__":
    run()
