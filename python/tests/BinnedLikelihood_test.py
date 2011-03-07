"""
Binned likelihood tests.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from obsSim_tests import sourceNamesDat, random_int
from GtApp import GtApp
gtbin = GtApp('gtbin', 'evtbin')
gtltcube = GtApp('gtltcube', 'Likelihood')
gtexpcube2 = GtApp('gtexpcube2', 'Likelihood')
gtsrcmaps = GtApp('gtsrcmaps', 'Likelihood')
gtlike = GtApp('gtlike', 'Likelihood')
gtmodel = GtApp('gtmodel', 'Likelihood')

def makeCountsMap():
    gtbin['algorithm'] = 'CCUBE'
    gtbin['evfile'] = 'test_events_0000.fits'
    gtbin['outfile'] = 'countsMap.fits'
    gtbin['scfile'] = 'orbSim_scData_0000.fits'
    gtbin['emin'] = 100
    gtbin['emax'] = 2e5
    gtbin['enumbins'] = 30
    gtbin['nxpix'] = 160
    gtbin['nypix'] = 160
    gtbin['binsz'] = 0.25
    gtbin['coordsys'] = 'CEL'
    gtbin['xref'] = 90
    gtbin['yref'] = 20
    gtbin['axisrot'] = 0
    gtbin['proj'] = 'STG'
    gtbin.run()

def makeExpCubes():
    gtltcube.run(evfile='test_events_0000.fits',
                 scfile='orbSim_scData_0000.fits',
                 outfile='ltcube.fits')
    gtexpcube2.run(infile='ltcube.fits',
                   cmap='countsMap.fits',
                   outfile='bexpmap.fits',
                   irfs=irfs)
    gtexpcube2.run(infile='ltcube.fits',
                   cmap='none',
                   outfile='bexpmap_allsky.fits',
                   irfs=irfs,
                   proj='CAR',
                   coordsys='GAL',
                   emin=100,
                   emax=2e5,
                   enumbins=30)

def makeSourceMaps():
    gtsrcmaps["scfile"] = 'orbSim_scData_0000.fits'
    gtsrcmaps['cmap'] = gtbin['outfile']
    gtsrcmaps['srcmdl'] = srcmdl
    gtsrcmaps['outfile'] = 'sourceMaps.fits'
    gtsrcmaps['expcube'] = 'ltcube.fits'
    gtsrcmaps['bexpmap'] = 'bexpmap.fits'
    gtsrcmaps["irfs"] = irfs
    #
    # test for failure
    #
    try:
        gtsrcmaps.run()
    except RuntimeError:
        pass
    #
    # test emapbnds override
    #
    gtsrcmaps["emapbnds"] = "no"
    gtsrcmaps.run()

    gtsrcmaps.run(outfile='sourceMaps_allsky.fits',
                  bexpmap='bexpmap_allsky.fits')

def runLikelihood():
    gtlike['scfile'] = 'orbSim_scData_0000.fits'
    gtlike['statistic'] = 'BINNED'
    gtlike['srcmdl'] = srcmdl
    gtlike["irfs"] = irfs
    gtlike['cmap'] = 'sourceMaps.fits'
    gtlike['expcube'] = 'ltcube.fits'
    gtlike['bexpmap'] = 'bexpmap.fits'
    gtlike['optimizer'] = 'MINUIT'
    if sys.platform == 'darwin':
        gtlike['optimizer'] = 'NEWMINUIT'
    gtlike['sfile'] = 'binned_fit_model.xml'
    gtlike.run()
    gtlike.run(cmap='sourceMaps_allsky.fits',
               bexpmap='bexpmap_allsky.fits')

def makeModelMap():
    gtmodel['srcmaps'] = gtlike['cmap']
    gtmodel['srcmdl'] = gtlike['sfile']
    gtmodel['outfile'] = 'model_map.fits'
    gtmodel['irfs'] = irfs
    gtmodel['expcube'] = gtlike['expcube']
    gtmodel.run()

def run():
    makeCountsMap()
    makeExpCubes()
    makeSourceMaps()
    runLikelihood()
    makeModelMap()

if __name__ == "__main__":
    run()
