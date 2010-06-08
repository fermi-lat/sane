"""
Get paths for system tests, move to data subdirectory

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os
import sys
import glob
from pil import Pil

#bindir = os.environ['BINDIR']
sysData = os.path.join(os.environ["SANEROOT"], 'data')
os.chdir(sysData)

# ensure the desired .par files are used.
os.environ['PFILES'] = sysData

# set the response functions to be used in all tests:
#irfs = 'G25'
#irfs = 'TEST'
#irfs = 'DC1'
irfs = 'DC1A'
#irfs = 'DC2'
#irfs = 'DSS'
#irfs = 'P5_v0_source'
#irfs = 'PASS5_v0'
#irfs = 'P6_v2'
#irfs = 'P6_V1_TRANSIENT'

def removeFile(file):
    files = glob.glob(file)
    for file in files:
        os.remove(file)

def setup_env_vars():
    try:
        os.environ['DATASUBSELECTORROOT']
    except KeyError:
        inst_dir = lambda x : os.path.join(os.environ['INST_DIR'], x)
        os.environ['DATASUBSELECTORROOT'] = inst_dir('dataSubselector')
        os.environ['LIKELIHOODROOT'] = inst_dir('Likelihood')
        os.environ['OBSERVATIONSIMROOT'] = inst_dir('observationSim')
        os.environ['MAP_TOOLSROOT'] = inst_dir('map_tools')
        os.environ['EVTBINROOT'] = inst_dir('evtbin')
        os.environ['RSPGENROOT'] = inst_dir('rspgen')
        os.environ['PULSEPHASEROOT'] = inst_dir('pulsePhase')
        os.environ['PERIODSEARCHROOT'] = inst_dir('periodSearch')
        os.environ['ST_APPROOT'] = inst_dir('st_app')
        os.environ['PYLIKELIHOODROOT'] = inst_dir('pyLikelihood')
        os.environ['FACILITIESROOT'] = inst_dir('facilities')
        os.environ['SANEROOT'] = inst_dir('sane')
        os.environ['GENERICSOURCESROOT'] = inst_dir('celestialSources/genericSources')
        os.environ['PULSARDBROOT'] = inst_dir('pulsarDb')

def copy_par_files():
    packages = ['observationSim', 'map_tools', 'dataSubselector',
                'Likelihood', 'evtbin', 'rspgen', 'pulsePhase', 'periodSearch']
    for package in packages:
        pfile_path = os.path.join(os.environ[package.upper()+'ROOT'], 'pfiles')
        pfiles = os.listdir(pfile_path)
        for file in pfiles:
            if file.find('.par') != -1 and file.find('~') == -1:
                pars = Pil(os.path.join(pfile_path, file))
                for par in pars.params:
                    if pars.params[par][0] == "fr":
                        pars.params[par][0] = "f"
                pars.write(file)

setup_env_vars()
copy_par_files()
