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

def run_LikelihoodApp(appName, pars=None):
    likeApp = GtApp(appName, 'Likelihood', raiseKeyErrors=False)
    likeApp['Spacecraft_file'] = 'orbSim_scData_0000.fits'
    likeApp['Source_model_file'] = 'srcModel.xml'
    likeApp['Statistic'] = 'UNBINNED'
    likeApp['ROI_file'] = 'RoiCuts.xml'
    likeApp['ROI_cuts_file'] = 'RoiCuts.xml'
    likeApp['event_file'] = 'filtered_events_0000.fits'
    likeApp['Response_functions'] = irfs
    likeApp.run()

def cleanUp():
    removeFile('flux_model.xml')
    removeFile('exp*.fits')
    removeFile('TsMap.fits')

def run(clean=False):
    expCube['Spacecraft_file'] = 'orbSim_scData_0000.fits'
    expCube['Output_file'] = '!expcube_1_day.fits'
    expCube['cos_theta_step'] = 0.05
    expCube['pixel_size'] = 1
    expCube['ROI_file'] = 'RoiCuts.xml'
    expCube.run()
    
    expMap.copy(expCube)
    expMap['ROI_cuts_file'] = expCube['ROI_file']
    expMap['Response_functions'] = irfs
    expMap['Source_region_radius'] = 30
    expMap['number_of_longitude_points'] = 120
    expMap['number_of_latitude_points'] = 120
    expMap['number_of_energies'] = 20
    expMap['exposure_cube_file'] = 'expcube_1_day.fits'
    expMap['Exposure_map_file'] = 'expMap.fits'
    expMap.run()

    diffResps.copy(expMap)
    diffResps['Source_model_file'] = 'srcModel.xml'
    diffResps['event_file'] = 'filtered_events_0000.fits'
    diffResps.run()

    like.copy(expMap)
    like.copy(diffResps)
    like['Statistic'] = 'UNBINNED'
    like['optimizer'] = 'MINUIT'
    like['fit_verbosity'] = 1
    like['fit_tolerance'] = 1e-4
    like['query_for_refit'] = 'no'
    like.run()

#    TsMap = GtApp('TsMap', 'Likelihood', raiseKeyErrors=False)
#    TsMap['Source_model_file'] = 'Ts_srcModel.xml'
#    TsMap.run()
    if clean:
        cleanUp()

if __name__ == "__main__":
    run()
