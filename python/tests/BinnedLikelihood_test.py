"""
Binned likelihood tests.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from obsSim_tests import sourceNamesDat, random_int
from BinnedAnalysis import *
from GtApp import GtApp, _failed_exes
gtselect = GtApp('gtselect')
gtbin = GtApp('gtbin', 'evtbin')
gtltcube = GtApp('gtltcube', 'Likelihood')
gtexpcube2 = GtApp('gtexpcube2', 'Likelihood')
gtsrcmaps = GtApp('gtsrcmaps', 'Likelihood')
gtlike = GtApp('gtlike', 'Likelihood')
gtmodel = GtApp('gtmodel', 'Likelihood')

#irfs = 'INDEF'
evfile = 'filtered_events.fits'

def makeCountsMap():
    gtselect.run(infile='test_events_0000.fits',
                 outfile=evfile,
                 ra='INDEF', dec='INDEF', rad='INDEF',
                 tmin='INDEF', tmax='INDEF', zmax=180,
                 irfs=irfs0,
                 emin=30, emax=300000)
                 
    gtbin['algorithm'] = 'CCUBE'
    gtbin['evfile'] = evfile
    gtbin['outfile'] = 'countsMap.fits'
    gtbin['scfile'] = 'orbSim_scData_0000.fits'
    gtbin['emin'] = 100
    if model_type == 'GALPROP_DIFFUSE':
        gtbin['emax'] = 1e5
    else:
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
    gtltcube.run(evfile=evfile,
                 scfile='orbSim_scData_0000.fits',
                 outfile='ltcube.fits')
    gtexpcube2.run(infile='ltcube.fits',
                   cmap='countsMap.fits',
                   outfile='bexpmap.fits',
                   irfs=irfs)
    gtexpcube2.run(infile='ltcube.fits',
                   cmap='none',
                   outfile='bexpmap_allsky.fits',
                   irfs=irfs0,
                   proj='CAR',
                   coordsys='GAL',
                   emin=gtbin['emin'],
                   emax=gtbin['emax'],
                   enumbins=gtbin['enumbins'])

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
        _failed_exes.pop()
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
    gtmodel['bexpmap'] = gtlike['bexpmap']
    gtmodel.run()

    gtmodel.run(outtype='ccube', outfile='model_cube.fits')
    
    like = binnedAnalysis(mode='h', srcmdl=gtlike['sfile'])
    Npred_tot = sum([like.NpredValue(srcname) 
                     for srcname in like.sourceNames()])
    import pyfits
    modelmap = pyfits.open('model_map.fits')
    modelcube = pyfits.open('model_cube.fits')
    delta1 = abs(sum(modelmap[0].data.flat) - Npred_tot)
    delta2 = abs(sum(modelcube[0].data.flat) - Npred_tot)
    if delta1 > 1e-3 or delta2 > 1e-3:
        raise RuntimeError("Npred mismatch in gtmodel output: "
                           + "delta1 = %s, delta2 = %s" % (delta1, delta2))

def run():
    makeCountsMap()
    makeExpCubes()
    makeSourceMaps()
    runLikelihood()
    makeModelMap()
   
if __name__ == "__main__":
    run()
