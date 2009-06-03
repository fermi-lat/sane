#!/usr/bin/env python
"""
Generate test data with obsSim.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#
import shutil
import random

from setPaths import *
from GtApp import GtApp

obsSim = GtApp('gtobssim', 'observationSim')

def random_int(scale=1e5):
    return int(random.random()*scale)

def sourceNamesDat(filename='source_names.txt',
                   srcList=('anticenter-32mev',
                            'Extragalactic_diffuse')):
    file = open(filename, 'w')
    for src in srcList:
        file.write(src + '\n')
    file.close()

def xmlFilesDat(filename='xmlFiles.txt',
                fileList=('anticenter_sources.xml',
                          '$(OBSERVATIONSIMROOT)/xml/' +
                          'obsSim_source_library.xml')):
    xmlFiles = open(filename, "w")
    for file in fileList:
        xmlFiles.write(file + "\n")
    xmlFiles.close()

def run(clean=False):
    sourceNamesDat()
    xmlFilesDat()
    obsSim['irfs'] = irfs
    if irfs == 'DSS':
        obsSim['irfs'] = 'DC2'
#    obsSim['seed'] = random_int()
    obsSim['seed'] = 479153
    obsSim['tstart'] = 86400
    obsSim.run(infile='xmlFiles.txt', srclist='source_names.txt',
               scfile='none', evroot='test', simtime=86400,
               use_ac='yes', ra=90, dec=20, radius=20, emin=100, emax=3e5)
    shutil.copy('test_scData_0000.fits', 'orbSim_scData_0000.fits')
    if clean:
        cleanUp()

def cleanUp():
    removeFile('test_*.fits')
    removeFile('source_names.txt')
    removeFile('fit_comparison_*.fits')

def compareFit(clean=False):
    sourceNamesDat(srcList=['all_in_flux_model.xml'])
    obsSim['infile'] = 'flux_model.xml'
    obsSim['evroot'] = 'fit_comparison'
    obsSim['irfs'] = irfs
    if irfs == 'DSS':
        obsSim['irfs'] = 'DC2'
    obsSim.run()
    if clean:
        cleanUp()

if __name__ == "__main__":
    run()
