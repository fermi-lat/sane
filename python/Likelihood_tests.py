"""
Use Likelihood applications to analyze obsSim data.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *

likeRoot = os.environ["LIKELIHOODROOT"]

def run_LikelihoodApp(appName, pars=None):
    likeApp = os.path.join(likeRoot, bindir, appName + '.exe')
    if pars == None:
        pars = Pil(os.path.join(sysData, appName + '.par'),
                   raiseKeyErrors=False)
        pars['Source_model_file'] = 'srcModel.xml'
        pars['ROI_file'] = 'RoiCuts.xml'
        pars['ROI_cuts_file'] = 'RoiCuts.xml'
        pars['event_file'] = 'filtered_events_0000.fits'
        pars['Response_functions'] = irfs
    command = likeApp + pars()
    print command
    os.system(command)

def cleanUp():
    removeFile('flux_model.xml')
    removeFile('exp*.fits')
    removeFile('TsMap.fits')

def run(clean=False):
    run_LikelihoodApp('makeExposureCube')
    run_LikelihoodApp('expMap')
    run_LikelihoodApp('diffuseResponses')
    run_LikelihoodApp('likelihood')
#    pars = Pil(os.path.join(sysData, 'TsMap.par'), raiseKeyErrors=False)
#    pars['Source_model_file'] = 'Ts_srcModel.xml'
#    run_LikelihoodApp('TsMap', pars)
    if clean:
        cleanUp()

if __name__ == "__main__":
    run()
