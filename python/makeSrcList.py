"""
This module provides classes for processing a white-space delimited
ascii file of (id, l, b, nsigma) values. Methods for acceptance cone
selection and creating an xml source model file for Likelihood are
provided.

@author J. Chiang <jchiang@slac.stanford.edu>

$Header$
"""
import copy, string
import celgal
from xmlSrcLib import *

converter = celgal.celgal()

class SourceList:
    def __init__(self, filename='src_list.dat', coordsys='GAL'):
        srcFile = open(filename, 'r')
        srcs = srcFile.readlines()
        self.srcList = {}
        for src in srcs:
            if src.find("#") != 0:
                id, l, b, nsigma = src.split()[:4]
                if coordsys == 'CEL':
                    self.srcList[id] = converter.gal((string.atof(l),
                                                      string.atof(b)))
                else:
                    self.srcList[id] = (string.atof(l), string.atof(b))
#    def __getitem__(self, id):
#        return self.srcList[id]
#    def keys(self):
#        return self.srcList.keys()
    def encircledSources(self, acceptanceCone):
        l, b, radius = acceptanceCone
        srcs = {}
        for name in self.srcList.keys():
            if celgal.dist( self.srcList[name], (l, b) ) <= radius:
                srcs[name] = self.srcList[name]
        return srcs
    def makeSrcModel(self, filename, acceptanceCone=None, exclude=()):
        file = open(filename, 'w')
        file.write('<?xml version="1.0" ?>\n')
        file.write('<source_library title="source library">\n')
        if "eg_diffuse" not in exclude:
            file.write(EGDiffuse().toxml() + '\n')
        if "galdiffuse" not in exclude:
            file.write(GalDiffuse().toxml() + '\n')
        if acceptanceCone != None:
            mySrcs = self.encircledSources(acceptanceCone)
        else:
            mySrcs = self.srcList
        for name in mySrcs.keys():
            if name not in exclude:
                ptsrc = PointSource(name, pos=converter.cel(mySrcs[name]))
                file.write(ptsrc.write() + '\n')
        file.write('</source_library>\n')
        file.close()

class PointSource:
    def __init__(self, name, pos=(0, 0)):
        self.src = copy.deepcopy(ptSrc())
        self.src.setAttribute('name', name)
        self._setDir(pos)
    def _setDir(self, pos):
        dir = self.src.getElementsByTagName('spatialModel')[0]
        coords = dir.getElementsByTagName('parameter')
        for coord in coords:
            if coord.getAttribute('name').encode('ascii') == 'RA':
                coord.setAttribute('value', "%.2f" % pos[0])
            if coord.getAttribute('name').encode('ascii') == 'DEC':
                coord.setAttribute('value', "%.2f" % pos[1])
    def write(self):
        return self.src.toxml()
