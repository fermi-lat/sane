"""
Tests of Pulsar source and pulsar-related tools.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from obsSim_tests import sourceNamesDat, xmlFilesDat, random_int

from GtApp import GtApp
from gt_apps import obsSim, pulsePhase, psearch

pulsePhase = GtApp('gtpphase', 'pulsePhase')
psearch = GtApp('gtpsearch', 'periodSearch')

#
# Geminga parameters
#
#period = 0.2371
#pdot = 1.14e-14

#
# Vela-like parameters
#
period = 0.089
pdot = 1e-10

freq = 1./period
fdot = -pdot/period**2

pulsar_source = "\n".join(('<source_library>',
                           '  <source name="Geminga_Pulsar">',
                           '     <spectrum escale="MeV">',
                           '         <SpectrumClass name="Pulsar"',
                           '          params="0.102,1.66,%s,%s,0,' +
                           '$(GENERICSOURCESROOT)/data/GemingaTemplate.dat"/>',
                           '         <celestial_dir ra="98.49" dec="17.86"/>',
                           '      </spectrum>',
                           '  </source>',
                           '</source_library>'))

def preparePulsarSource():
    xmlFilesDat(fileList=('my_pulsar.xml',))
    pulsarFile = open('my_pulsar.xml', 'w')
    pulsarFile.write(pulsar_source % (period, pdot))
    pulsarFile.close()
    sourceNamesDat(srcList=('Geminga_Pulsar', ))

def run(useWorkAround=False):
    preparePulsarSource()

    obsSim['infile'] = 'xmlFiles.txt'
    obsSim['evroot'] = 'Geminga'
    obsSim['scfile'] = 'none'
    obsSim['irfs'] = irfs
    obsSim['seed'] = random_int()
    obsSim.run()

    pulsePhase['evfile'] = 'Geminga_events_0000.fits'
    pulsePhase['scfile'] = 'Geminga_scData_0000.fits'
    pulsePhase['psrdbfile'] = os.environ['PULSARDBROOT'] + '/data/groD4-dc2v5.fits'
    pulsePhase['solareph'] = 'JPL DE405'
    pulsePhase['ephstyle'] = "FREQ"
    pulsePhase['ephepoch'] = 0
    pulsePhase['tcorrect'] = 'none'
    pulsePhase['phi0'] = 0
    pulsePhase['f0'] = freq
    pulsePhase['f1'] = fdot
    pulsePhase['f2'] = 0
    pulsePhase['timesys'] = 'TT'
    if useWorkAround:
        pulsePhase['p0'] = period
        pulsePhase['p1'] = pdot
        pulsePhase['p2'] = 0
        pulsePhase.pars.write()
    pulsePhase.run()

    psearch['evfile'] = pulsePhase['evfile']
    psearch['scfile'] = pulsePhase['scfile']
    psearch['psrdbfile'] = pulsePhase['psrdbfile']
    psearch['outfile'] = 'foo.fits'
    psearch['ephstyle'] = 'FREQ'
    psearch['f0'] = freq
    psearch['f1'] = fdot
    psearch['p0'] = period
    psearch['p1'] = pdot
    psearch['solareph'] = 'JPL DE405'
    psearch['timesys'] = 'TT'
    psearch['scanstep'] = 0.5
    psearch['numtrials'] = 200
    psearch['plot'] = 'no'
    psearch['chatter'] = 0
    if useWorkAround:
        psearch.pars.write()
    psearch.run()

if __name__ == '__main__':
    run(True)
