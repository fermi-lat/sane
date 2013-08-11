# -*- python -*-
# $Id$
# Authors: J. Chiang <jchiang@slac.stanford.edu>
# Version: sane-03-22-03

Import('baseEnv')
Import('listFiles')
progEnv = baseEnv.Clone()

progEnv.Tool('dataSubselectorLib')
progEnv.Tool('LikelihoodLib')
progEnv.Tool('observationSimLib')
progEnv.Tool('evtbinLib')
progEnv.Tool('rspgenLib')
progEnv.Tool('st_appLib')
progEnv.Tool('facilitiesLib')
progEnv.Tool('addLibrary', library = baseEnv['pythonLibs'])

test_saneBin = progEnv.Program('test_sane', 'src/test/main.cxx')

progEnv.Tool('registerTargets', package = 'sane', 
             testAppCxts = [[test_saneBin, progEnv]], 
             data = listFiles(['data/*'], recursive = True),
             python=listFiles(['python/*.py']))
