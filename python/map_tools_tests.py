"""
Exercise the map_tools applications.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from getApp import GtApp

def run(clean=False):
    count_map = GtApp('count_map', 'map_tools')
    count_map['filter'] = ''
    count_map.run()
    if clean:
        removeFile('count_map.fits')

if __name__ == "__main__":
    run()
