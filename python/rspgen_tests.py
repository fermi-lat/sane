#!/usr/bin/env python
"""
Exercise rspgen.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *

rspgenRoot = os.environ["RSPGENROOT"]
rspgen = os.path.join(rspgenRoot, bindir, 'rspgen.exe')
rspgenPar = os.path.join(sysData, 'rspgen.par')

def run():
    pars = Pil(rspgenPar)
    command = rspgen + pars()
    print command
    os.system(command)

if __name__ == "__main__":
    run()
