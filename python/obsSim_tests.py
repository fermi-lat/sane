#!/usr/bin/env python
"""
Generate test data with obsSim.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from getApp import GtApp

obsSim = GtApp('obsSim', 'observationSim')
orbSim = GtApp('orbSim', 'observationSim')

def sourceNamesDat(filename='source_names.dat',
                   srcList=('anticenter-32mev', 'diffuse-20mev')):
    file = open(filename, 'w')
    for src in srcList:
        file.write(src + '\n')
    file.close()

def xmlFilesDat(filename='xmlFiles.dat',
                fileList=('anticenter_sources.xml',
                          '$(OBSERVATIONSIMROOT)/xml/' +
                          'obsSim_source_library.xml')):
    xmlFiles = open(filename, "w")
    for file in fileList:
        xmlFiles.write(file + "\n")
    xmlFiles.close()

def run(clean=False):
    orbSim['Output_file_prefix'] = 'orbSim'
    orbSim.run()
    sourceNamesDat()
    xmlFilesDat()
    obsSim['XML_source_file'] = 'xmlFiles.dat'
    obsSim['Source_list'] = 'source_names.dat'
    obsSim['Output_file_prefix'] = 'test'
    obsSim['Response_functions'] = irfs
    obsSim['Pointing_history_file'] = "orbSim_scData_0000.fits"
    obsSim.run()
    if clean:
        cleanUp()

def cleanUp():
    removeFile('test_*.fits')
    removeFile('source_names.dat')
    removeFile('fit_comparison_*.fits')

def compareFit(clean=False):
    sourceNamesDat(srcList=['all_in_flux_model.xml'])
    obsSim['XML_source_file'] = 'flux_model.xml'
    obsSim['Output_file_prefix'] = 'fit_comparison'
    obsSim['Response_functions'] = irfs
    obsSim.run()
    if clean:
        cleanUp()

if __name__ == "__main__":
    run()
