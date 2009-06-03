"""
Use Likelihood applications to analyze obsSim data.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from gt_apps import expCube, expMap, diffResps, like, TsMap, filter, addCubes
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
    filter['tmin'] = 0. + start_time
    filter['tmax'] = 86400/2 + start_time
    filter['outfile'] = 'filtered1.fits'
    filter.run()
    
    expCube['evfile'] = 'filtered1.fits'
    expCube['scfile'] = 'orbSim_scData_0000.fits'
    expCube['outfile'] = 'expcube1.fits'
    expCube['dcostheta'] = 0.05
    expCube['binsz'] = 1
#    expCube['phibins'] = 10
    expCube['phibins'] = 0
    expCube.run()

    filter['tmin'] = 86400/2 + start_time
    filter['tmax'] = 86400 + start_time
    filter['outfile'] = 'filtered2.fits'
    filter.run()
   
    expCube['evfile'] = 'filtered2.fits'
    expCube['scfile'] = 'orbSim_scData_0000.fits'
    expCube['outfile'] = 'expcube2.fits'
    expCube['dcostheta'] = 0.05
    expCube['binsz'] = 1
    expCube.run()

    addCubes['infile1'] = 'expcube1.fits'
    addCubes['infile2'] = 'expcube2.fits'
    addCubes['outfile'] = 'expcube_1_day.fits'
    addCubes.run()
   
    expMap.copy(expCube)
    expMap['evfile'] = 'filtered_events_0000.fits'
    expMap['irfs'] = irfs
    expMap['srcrad'] = 30
    expMap['nlong'] = 120
    expMap['nlat'] = 120
    expMap['nenergies'] = 20
    expMap['expcube'] = 'expcube_1_day.fits'
    expMap['outfile'] = 'expMap.fits'

    diffResps.copy(expMap)
    diffResps['srcmdl'] = 'srcModel.xml'
    diffResps['evfile'] = 'filtered_events_0000.fits'

    like.copy(expCube)
    like.copy(diffResps)
    like['expmap'] = expMap['outfile']
    like['expcube'] = addCubes['outfile']
    like['statistic'] = 'UNBINNED'
    like['optimizer'] = 'MINUIT'
    like['chatter'] = 2
    like['ftol'] = 1e-4
    like['refit'] = 'no'

    expMap.run()
    diffResps.run()
    like.run()

    try:
        pylike = unbinnedAnalysis(mode='h')
        pylike.fit(verbosity=0, tol=like['ftol'])
        print pylike.model
        print "Ts values:"
        for src in pylike.sourceNames():
            print src, pylike.Ts(src)
    except NameError, message:
        print "NameError occurred for pyLike analysis:"
        print message
    
#    TsMap['srcmdl'] = 'Ts_srcModel.xml'
#    TsMap.run()
    if clean:
        cleanUp()

if __name__ == "__main__":
    run()
