"""
Use Likelihood applications to analyze obsSim data.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from gt_apps import expCube, expMap, diffResps, like, TsMap, filter, addCubes

def cleanUp():
    removeFile('flux_model.xml')
    removeFile('exp*.fits')
    removeFile('TsMap.fits')

def run(clean=False):
    filter['tmin'] = 0.
    filter['tmax'] = 86400/2
    filter['outfile'] = 'filtered1.fits'
    filter.run()
    
    expCube['evfile'] = 'filtered1.fits'
    expCube['scfile'] = 'orbSim_scData_0000.fits'
    expCube['outfile'] = 'expcube1.fits'
    expCube['cos_theta_step'] = 0.05
    expCube['pixel_size'] = 1
    expCube.run()

    filter['tmin'] = 86400/2
    filter['tmax'] = 86400
    filter['outfile'] = 'filtered2.fits'
    filter.run()
    
    expCube['evfile'] = 'filtered2.fits'
    expCube['scfile'] = 'orbSim_scData_0000.fits'
    expCube['outfile'] = 'expcube2.fits'
    expCube['cos_theta_step'] = 0.05
    expCube['pixel_size'] = 1
    expCube.run()

    addCubes['infile1'] = 'expcube1.fits'
    addCubes['infile2'] = 'expcube2.fits'
    addCubes['outfile'] = 'expcube_1_day.fits'
    addCubes.run()
    
    expMap.copy(expCube)
    expMap['evfile'] = 'filtered_events_0000.fits'
    expMap['rspfunc'] = irfs
    expMap['source_region_radius'] = 30
    expMap['number_of_longitude_points'] = 120
    expMap['number_of_latitude_points'] = 120
    expMap['number_of_energies'] = 20
    expMap['exposure_cube_file'] = 'expcube_1_day.fits'
    expMap['outfile'] = 'expMap.fits'

    diffResps.copy(expMap)
    diffResps['source_model_file'] = 'srcModel.xml'
    diffResps['evfile'] = 'filtered_events_0000.fits'

    like.copy(expCube)
    like.copy(diffResps)
    like['exposure_map_file'] = expMap['outfile']
    like['exposure_cube_file'] = addCubes['outfile']
    like['statistic'] = 'UNBINNED'
    like['optimizer'] = 'MINUIT'
    like['chatter'] = 2
    like['fit_tolerance'] = 1e-4
    like['query_for_refit'] = 'no'

    expMap.run()
    diffResps.run()
    like.run()
    
#    TsMap['Source_model_file'] = 'Ts_srcModel.xml'
#    TsMap.run()
    if clean:
        cleanUp()

if __name__ == "__main__":
    run()
