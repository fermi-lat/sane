"""
Exercise the map_tools applications.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *

map_toolsRoot = os.environ["MAP_TOOLSROOT"]

def run_count_map(clean=False):
    count_mapApp = os.path.join(map_toolsRoot, bindir, 'count_map.exe')
    count_mapPar = os.path.join(sysData, 'count_map.par')
    command = count_mapApp
    print command
    os.system(command)
    if clean:
        cleanUp()

def run(clean=False):
    run_count_map(clean)

def cleanUp():
    os.remove('count_map.fits')

if __name__ == "__main__":
    run()
