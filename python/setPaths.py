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

sys.path.append(os.path.join(os.environ["SANEROOT"], "python"))

bindir = os.environ['BINDIR']

stTestsPath = os.environ["SANEROOT"]
sysData = os.path.join(stTestsPath, 'data')

os.chdir(sysData)

# ensure the desired .par files are used.
os.environ['PFILES'] = sysData

from pil import Pil

def removeFile(file):
    files = glob.glob(file)
    for file in files:
        os.remove(file)