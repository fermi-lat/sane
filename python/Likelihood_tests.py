"""
Use Likelihood applications to analyze obsSim data.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *

likeRoot = os.environ["LIKELIHOODROOT"]

def run_LikelihoodApp(appName):
    likeApp = os.path.join(likeRoot, bindir, appName + '.exe')
    pars = Pil(os.path.join(sysData, appName + '.par'), raiseKeyErrors=False)
    pars['Source_model_file'] = os.path.join(sysData, 'srcModel.xml')
    pars['ROI_file'] = os.path.join(sysData, 'RoiCuts.xml')
    pars['ROI_cuts_file'] = os.path.join(sysData, 'RoiCuts.xml')
    command = likeApp + pars()
    print command
    os.system(command)

def cleanUp():
    os.remove('flux_model.xml')
    os.remove('expcube_1_day.fits')
    os.remove('expMap.fits')

def run(clean=False):
    run_LikelihoodApp('makeExposureCube')
    run_LikelihoodApp('expMap')
    run_LikelihoodApp('likelihood')
    if clean:
        cleanUp()

if __name__ == "__main__":
    run()
