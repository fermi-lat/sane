"""
Use Likelihood applications to analyze obsSim data.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from getApp import GtApp

expCube = GtApp('makeExposureCube', 'Likelihood')
expMap = GtApp('expMap', 'Likelihood')
diffResps = GtApp('diffuseResponses', 'Likelihood')
like = GtApp('likelihood')

def cleanUp():
    removeFile('flux_model.xml')
    removeFile('exp*.fits')
    removeFile('TsMap.fits')

def run(clean=False):
    expCube['scfile'] = 'orbSim_scData_0000.fits'
    expCube['outfile'] = 'expcube_1_day.fits'
    expCube['cos_theta_step'] = 0.05
    expCube['pixel_size'] = 1
    expCube['ROI_file'] = 'RoiCuts.xml'
    
    expMap.copy(expCube)
    expMap['rspfunc'] = irfs
    expMap['source_region_radius'] = 30
    expMap['number_of_longitude_points'] = 120
    expMap['number_of_latitude_points'] = 120
    expMap['number_of_energies'] = 20
    expMap['exposure_cube_file'] = 'expcube_1_day.fits'
    expMap['outfile'] = 'expMap.fits'

    diffResps.copy(expMap)
    diffResps['source_model_file'] = 'srcModel.xml'
    diffResps['evfile'] = 'filtered_events_0000.fits'

    like.copy(expCube)
    like.copy(diffResps)
    like['exposure_map_file'] = expMap['outfile']
    like['statistic'] = 'UNBINNED'
    like['optimizer'] = 'MINUIT'
    like['chatter'] = 2
    like['fit_tolerance'] = 1e-4
    like['query_for_refit'] = 'no'

    expCube.run()
    expMap.run()
    diffResps.run()
    like.run()
    
#    TsMap = GtApp('TsMap', 'Likelihood', raiseKeyErrors=False)
#    TsMap['Source_model_file'] = 'Ts_srcModel.xml'
#    TsMap.run()
    if clean:
        cleanUp()

if __name__ == "__main__":
    run()
