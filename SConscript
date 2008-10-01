# -*- python -*-
# $Id$
# Authors: T. Burnett <tburnett@u.washington.edu>
# Version: sane-03-17-01

Import('baseEnv')
Import('listFiles')
progEnv = baseEnv.Clone()

progEnv.Tool('dataSubselectorLib')
progEnv.Tool('LikelihoodLib')
progEnv.Tool('observationSimLib')
progEnv.Tool('map_toolsLib')
progEnv.Tool('evtbinLib')
progEnv.Tool('rspgenLib')
progEnv.Tool('periodSearchLib')
progEnv.Tool('st_appLib')
progEnv.Tool('pyLikelihoodLib')
progEnv.Tool('facilitiesLib')
progEnv.Tool('addLibrary', library = baseEnv['pythonLibs'])

test_saneBin = progEnv.Program('test_sane', 'src/test/main.cxx')

progEnv.Tool('registerObjects', package = 'sane', testApps = [test_saneBin], 
             data = listFiles(['data/*'], recursive = True),
             python=listFiles(['python/*.py']))
                              
