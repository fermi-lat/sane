"""
Tests of Pulsar source and pulsar-related tools.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from setPaths import *
from getApp import GtApp
from obsSim_tests import sourceNamesDat, xmlFilesDat

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

def run():
    preparePulsarSource()

    obsSim = GtApp('obsSim', 'observationSim')
    obsSim['XML_source_file'] = 'xmlFiles.dat'
    obsSim['Output_file_prefix'] = 'Geminga'
    obsSim.run()

    pulsePhase = GtApp('pulsePhase')
    pulsePhase['ephstyle'] = "FREQ"
    pulsePhase['f0'] = freq
    pulsePhase['f1'] = fdot
#    pulsePhase['ephstyle'] = "PER"
    pulsePhase['p0'] = period
    pulsePhase['p1'] = pdot
    pulsePhase.pars.write()
    pulsePhase.run()

    psearch = GtApp('stpsearch')
    psearch['eventfile'] = 'Geminga_events_0000.fits'
    psearch['f0'] = freq
    psearch['fstep'] = 1e-5
    psearch['numtrials'] = 200
    psearch['correctfdot'] = 'yes'
    psearch['f1'] = fdot
    psearch['plot'] = 'no'
    input, output = psearch.runWithOutput()
    for line in output:
        if line.find('Maximum at') != -1:
            print line.strip()
        if line.find('Statistic:') != -1:
            print line.split("Chance probability:")[0]

if __name__ == '__main__':
    run()
