#!/usr/bin/env python
"""
Generate test data with obsSim.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *

obsSimRoot = os.environ["OBSERVATIONSIMROOT"]
obsSimApp = os.path.join(obsSimRoot, bindir, 'obsSim.exe')
obsSimPar = os.path.join(sysData, 'obsSim.par')

def sourceNamesDat(filename='source_names.dat',
                   srcList=('anticenter-32mev', 'diffuse-20mev')):
    file = open(filename, 'w')
    for src in srcList:
        file.write(src + '\n')
    file.close()

def run(clean=False):
    sourceNamesDat()
#    sourceNamesDat(srcList=('anticenter', 'diffuse-100mev'))
    pars = Pil(obsSimPar)
    pars['XML_source_file'] = 'xmlFiles.dat'
    pars['Source_list'] = 'source_names.dat'
    pars['Output_file_prefix'] = 'test'
    pars['Response_functions'] = irfs
    command = obsSimApp + pars()
    print command
    os.system(command)
    if clean:
        cleanUp()

def cleanUp():
    removeFile('test_*.fits')
    removeFile('source_names.dat')
    removeFile('fit_comparison_*.fits')

def compareFit(clean=False):
    sourceNamesDat(srcList=['all_in_flux_model.xml'])
    pars = Pil(obsSimPar)
    pars['XML_source_file'] = 'flux_model.xml'
    pars['Output_file_prefix'] = 'fit_comparison'
    pars['Response_functions'] = irfs
    command = obsSimApp + pars()
    print command
    os.system(command)
    if clean:
        cleanUp()

if __name__ == "__main__":
    run()
