"""
Tests of Pulsar source and pulsar-related tools.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from getApp import GtApp
from obsSim_tests import sourceNamesDat, xmlFilesDat, random_int

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

    obsSim = GtApp('obsSim', 'observationSim')
    obsSim['xml_source_file'] = 'xmlFiles.dat'
    obsSim['outfile_prefix'] = 'Geminga'
    obsSim['random_seed'] = random_int()
    obsSim.run()

    pulsePhase = GtApp('pulsePhase')
    pulsePhase['evfile'] = 'Geminga_events_0000.fits'
    pulsePhase['ephstyle'] = "FREQ"
    pulsePhase['f0'] = freq
    pulsePhase['f1'] = fdot
    if useWorkAround:
        pulsePhase['p0'] = period
        pulsePhase['p1'] = pdot
        pulsePhase.pars.write()
    pulsePhase.run()

    psearch = GtApp('stpsearch')
    psearch['evfile'] = pulsePhase['evfile']
    psearch['ephstyle'] = 'FREQ'
    psearch['f0'] = freq
    psearch['f1'] = fdot
    psearch['p0'] = period
    psearch['p1'] = pdot
    psearch['scanstep'] = 0.5
    psearch['numtrials'] = 200
    psearch['correctpdot'] = 'yes'
    psearch['plot'] = 'no'
    psearch['chatter'] = 0
    if useWorkAround:
        psearch.pars.write()
    input, output = psearch.runWithOutput()
    for line in output:
        if line.find('Maximum at') != -1:
            print line.strip()
        if line.find('Statistic:') != -1:
            print line.strip()
        if line.find('Chance probability') != -1:
            print line.strip()

if __name__ == '__main__':
    run()
