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

bindir = os.environ['BINDIR']
sysData = os.path.join(os.environ["SANEROOT"], 'data')
os.chdir(sysData)

# ensure the desired .par files are used.
os.environ['PFILES'] = sysData

# set the response functions to be used in all tests:
#irfs = 'G25'
#irfs = 'TEST'
irfs = 'DC1'

def removeFile(file):
    files = glob.glob(file)
    for file in files:
        os.remove(file)

def copy_par_files():
    packages = ['observationSim', 'map_tools', 'dataSubselector',
                'Likelihood', 'evtbin', 'rspgen', 'pulsePhase', 'stpsearch']
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

copy_par_files()
