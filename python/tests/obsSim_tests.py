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

gtobssim = GtApp('gtobssim', 'observationSim')

def random_int(scale=1e5):
    return int(random.random()*scale)

if model_type == 'EGRET_DIFFUSE':
    source_list = ('anticenter-32mev', 'Galactic_diffuse')
elif model_type == 'GALPROP_DIFFUSE':
    source_list = ('anticenter-32mev', 'GALPROP_diffuse')
else:
    source_list = ('anticenter-32mev', 'Extragalactic_diffuse')

def sourceNamesDat(filename='source_names.txt',
                   srcList=source_list):
    file = open(filename, 'w')
    for src in srcList:
        file.write(src + '\n')
    file.close()

def xmlFilesDat(filename='xmlFiles.txt',
                fileList=(os.path.join(sysData, 'anticenter_sources.xml'),
                          '$(OBSERVATIONSIMROOT)/xml/' +
                          'obsSim_source_library.xml')):
    xmlFiles = open(filename, "w")
    for file in fileList:
        xmlFiles.write(file + "\n")
    xmlFiles.close()

def run(clean=False):
    sourceNamesDat()
    xmlFilesDat()
    gtobssim['irfs'] = irfs
    if irfs == 'DSS':
        gtobssim['irfs'] = 'DC2'
#    gtobssim['seed'] = random_int()
    gtobssim['seed'] = 479153
    gtobssim['tstart'] = 86400
    gtobssim.run(infile='xmlFiles.txt', srclist='source_names.txt',
                 scfile='none', evroot='test', simtime=86400,
                 use_ac='yes', ra=90, dec=20, radius=30, emin=100, emax=3e5)
    shutil.copy('test_scData_0000.fits', 'orbSim_scData_0000.fits')
    if clean:
        cleanUp()

def cleanUp():
    removeFile('test_*.fits')
    removeFile('source_names.txt')
    removeFile('fit_comparison_*.fits')

def compareFit(clean=False):
    sourceNamesDat(srcList=['all_in_flux_model.xml'])
    gtobssim['infile'] = 'flux_model.xml'
    gtobssim['evroot'] = 'fit_comparison'
    gtobssim['irfs'] = irfs
    if irfs == 'DSS':
        gtobssim['irfs'] = 'DC2'
    gtobssim.run()
    if clean:
        cleanUp()

if __name__ == "__main__":
    run()
