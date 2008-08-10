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

def makeCountsMap():
    counts_map['algorithm'] = 'CCUBE'
    counts_map['evfile'] = 'filtered_events_0000.fits'
    counts_map['outfile'] = 'countsMap.fits'
    counts_map['scfile'] = 'orbSim_scData_0000.fits'
    counts_map['emin'] = 100
    counts_map['emax'] = 2e5
    counts_map['enumbins'] = 20
    counts_map['nxpix'] = 160
    counts_map['nypix'] = 160
    counts_map['binsz'] = 0.25
    counts_map['coordsys'] = 'CEL'
    counts_map['xref'] = 90
    counts_map['yref'] = 20
    counts_map['axisrot'] = 0
    counts_map['proj'] = 'STG'
    counts_map.run()

def makeSourceMaps():
    srcMaps["scfile"] = 'orbSim_scData_0000.fits'
    srcMaps['cmap'] = counts_map['outfile']
    srcMaps['srcmdl'] = 'srcModel.xml'
    srcMaps['outfile'] = 'sourceMaps.fits'
    srcMaps['expcube'] = 'expcube_1_day.fits'
    srcMaps['bexpmap'] = 'binned_exposure.fits'
    srcMaps["irfs"] = irfs
    srcMaps.run()

def runLikelihood():
    likelihood['scfile'] = 'orbSim_scData_0000.fits'
    likelihood['statistic'] = 'BINNED'
    likelihood['srcmdl'] = 'srcModel.xml'
    likelihood["irfs"] = irfs
    likelihood['cmap'] = 'sourceMaps.fits'
    likelihood['expcube'] = 'expcube_1_day.fits'
    likelihood['bexpmap'] = 'binned_exposure.fits'
    likelihood['optimizer'] = 'MINUIT'
    likelihood.run()

def makeModelMap():
    model_map['srcmaps'] = likelihood['cmap']
    model_map['srcmdl'] = likelihood['srcmdl']
    model_map['outfile'] = 'model_map.fits'
    model_map['irfs'] = irfs
    model_map['expcube'] = likelihood['expcube']
    model_map.run()

def run():
    makeCountsMap()
    makeSourceMaps()
    runLikelihood()
    makeModelMap()

if __name__ == "__main__":
    run()
