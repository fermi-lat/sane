import glob,os,platform

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

test_saneBin = progEnv.Program('test_sane', 'src/test/main.cxx', LIBS = baseEnv['pythonLibs'])

progEnv.Tool('registerObjects', package = 'sane', testApps = [test_saneBin])