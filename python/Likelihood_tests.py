"""
Use Likelihood applications to analyze obsSim data.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from getApp import GtApp

def run_LikelihoodApp(appName, pars=None):
    likeApp = GtApp(appName, 'Likelihood', raiseKeyErrors=False)
    likeApp['Source_model_file'] = 'srcModel.xml'
    likeApp['Statistic'] = 'UNBINNED'
    likeApp['ROI_file'] = 'RoiCuts.xml'
    likeApp['ROI_cuts_file'] = 'RoiCuts.xml'
    likeApp['Spacecraft_file'] = 'orbSim_scData_0000.fits'
    likeApp['event_file'] = 'filtered_events_0000.fits'
    likeApp['Response_functions'] = irfs
    likeApp.run()

def cleanUp():
    removeFile('flux_model.xml')
    removeFile('exp*.fits')
    removeFile('TsMap.fits')

def run(clean=False):
    run_LikelihoodApp('makeExposureCube')
    run_LikelihoodApp('expMap')
    run_LikelihoodApp('diffuseResponses')
    run_LikelihoodApp('likelihood')
#    TsMap = GtApp('TsMap', 'Likelihood', raiseKeyErrors=False)
#    TsMap['Source_model_file'] = 'Ts_srcModel.xml'
#    TsMap.run()
    if clean:
        cleanUp()

if __name__ == "__main__":
    run()
