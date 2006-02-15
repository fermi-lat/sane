#!/usr/bin/env python
"""
Generate test data with obsSim.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#
import random

from setPaths import *
from gt_apps import obsSim, orbSim

def random_int(scale=1e5):
    return int(random.random()*scale)

def sourceNamesDat(filename='source_names.txt',
                   srcList=('anticenter-32mev', 'Extragalactic_diffuse')):
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
    orbSim['outfile_prefix'] = 'orbSim'
    orbSim['pointing_strategy'] = 'ONEPERORBIT'
    orbSim['rocking_angle'] = 35.0
    orbSim['simulation_time'] = 86400.0
    orbSim.run()
    sourceNamesDat()
    xmlFilesDat()
    obsSim['xml_source_file'] = 'xmlFiles.txt'
    obsSim['source_list'] = 'source_names.txt'
    obsSim['scfile'] = 'orbSim_scData_0000.fits'
    obsSim['outfile_prefix'] = 'test'
    obsSim['simulation_time'] = 86400.0
    obsSim['use_acceptance_cone'] = 'yes'
    obsSim['ra'] = 86.4
    obsSim['dec'] = 28.9
    obsSim['radius'] = 20
    obsSim['emin'] = 32
    obsSim['emax'] = 2e5
    obsSim['rspfunc'] = irfs
    obsSim['random_seed'] = random_int()
    obsSim.run()
    if clean:
        cleanUp()

def cleanUp():
    removeFile('test_*.fits')
    removeFile('source_names.txt')
    removeFile('fit_comparison_*.fits')

def compareFit(clean=False):
    sourceNamesDat(srcList=['all_in_flux_model.xml'])
    obsSim['xml_source_file'] = 'flux_model.xml'
    obsSim['outfile_prefix'] = 'fit_comparison'
    obsSim['rspfunc'] = irfs
    obsSim.run()
    if clean:
        cleanUp()

if __name__ == "__main__":
    run()
