"""
Use Likelihood applications to analyze obsSim data.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from GtApp import GtApp
from UpperLimits import UpperLimits
import IntegralUpperLimit

gtselect = GtApp('gtselect', 'dataSubselector')
gtltcube = GtApp('gtltcube', 'Likelihood')
gtexpmap = GtApp('gtexpmap', 'Likelihood')
gtdiffrsp = GtApp('gtdiffrsp', 'Likelihood')
gtlike = GtApp('gtlike', 'Likelihood')
gttsmap = GtApp('gttsmap', 'Likelihood')
gtltsum = GtApp('gtltsum', 'Likelihood')

try:
    from UnbinnedAnalysis import *
    pass
except ImportError, message:
    print "ImportError occurred for UnbinnedAnalysis:"
    print message

#start_time = 210211200.
start_time = 86400

def cleanUp():
    removeFile('flux_model.xml')
    removeFile('exp*.fits')
    removeFile('TsMap.fits')

def run(clean=False):
    gtselect['tmin'] = 0. + start_time
    gtselect['tmax'] = 86400/2 + start_time
    gtselect['infile'] = 'test_events_0000.fits'
    gtselect['outfile'] = 'filtered1.fits'
    gtselect['ra'] = 90
    gtselect['dec'] = 20
    gtselect['rad'] = 20
    gtselect.run()
    
    gtltcube['evfile'] = 'filtered1.fits'
    gtltcube['scfile'] = 'orbSim_scData_0000.fits'
    gtltcube['outfile'] = 'expcube1.fits'
    gtltcube['dcostheta'] = 0.05
    gtltcube['binsz'] = 1
#    gtltcube['phibins'] = 10
    gtltcube['phibins'] = 0
    gtltcube.run()

    gtselect['tmin'] = 86400/2 + start_time
    gtselect['tmax'] = 86400 + start_time
    gtselect['outfile'] = 'filtered2.fits'
    gtselect.run()
   
    gtltcube['evfile'] = 'filtered2.fits'
    gtltcube['scfile'] = 'orbSim_scData_0000.fits'
    gtltcube['outfile'] = 'expcube2.fits'
    gtltcube['dcostheta'] = 0.05
    gtltcube['binsz'] = 1
    gtltcube.run()

    gtltsum['infile1'] = 'expcube1.fits'
    gtltsum['infile2'] = 'expcube2.fits'
    gtltsum['outfile'] = 'expcube_1_day.fits'
    gtltsum.run()
   
    gtexpmap.copy(gtltcube)
    gtexpmap['evfile'] = 'filtered_events_0000.fits'
    gtexpmap['irfs'] = irfs
    gtexpmap['srcrad'] = 30
    gtexpmap['nlong'] = 120
    gtexpmap['nlat'] = 120
    gtexpmap['nenergies'] = 20
    gtexpmap['expcube'] = 'expcube_1_day.fits'
    gtexpmap['outfile'] = 'expMap.fits'

    gtdiffrsp.copy(gtexpmap)
    gtdiffrsp['srcmdl'] = srcmdl
    gtdiffrsp['evfile'] = 'filtered_events_0000.fits'

    gtlike.copy(gtltcube)
    gtlike.copy(gtdiffrsp)
    gtlike['expmap'] = gtexpmap['outfile']
    gtlike['expcube'] = gtltsum['outfile']
    gtlike['statistic'] = 'UNBINNED'
    gtlike['optimizer'] = 'MINUIT'
    if sys.platform == 'darwin':
        gtlike['optimizer'] = 'NEWMINUIT'
    gtlike['chatter'] = 2
    gtlike['ftol'] = 1e-4
    gtlike['refit'] = 'no'

    gtexpmap.run()
    gtdiffrsp.run()
    gtlike.run()


    like = unbinnedAnalysis(mode='h', optimizer='NEWMINUIT')
    like.fit(verbosity=0, tol=gtlike['ftol'])
    print like.model
    print "Ts values:"
    for src in like.sourceNames():
        print src, like.Ts(src)

    print "Exercise UpperLimits.py"
    ul = UpperLimits(like)
    for src in like.sourceNames():
        if like[src].src.getType() == 'Point':
            flux_ul = ul[src].compute(emin=100, emax=3e5)[0]
            print src, flux_ul

    print "Exercise IntegralUpperLimit.py"
    for src in like.sourceNames():
        if like[src].src.getType() == 'Point':
            flux_ul = IntegralUpperLimit.calc_int(like, src)
            print src, flux_ul[0]

#            bayes_ul = ul[src].bayesianUL(emin=100, emax=3e5)[0]
#            print src, bayes_ul
    
#    TsMap['srcmdl'] = 'Ts_srcModel.xml'
#    TsMap.run()
    if clean:
        cleanUp()

if __name__ == "__main__":
    run()
