"""
A module to encapsulate a Likelihood source model xml file.

@author J. Chiang <jchiang@slac.stanford.edu>

$Header$
"""
import os, sys, string
from xml.dom import minidom
from cleanXml import cleanXml

defaultModel = '\n'.join( ('<?xml version="1.0"?>',
                           '<source_library title="source library">',
                           '</source_library>') )

class SourceModel:
    def __init__(self, xmlFile=None):
        if xmlFile and os.path.isfile(xmlFile):
            self.filename = xmlFile.strip(" ")
            self.doc = minidom.parse(self.filename)
        else:
            self.filename = xmlFile
            self.doc = minidom.parseString(defaultModel)
        srcs = self.doc.getElementsByTagName("source")
        self.srcList = {}
        try:
            for src in srcs:
                self.srcList[src.getAttribute("name").encode()] = Source(src)
        except ValueError:
            pass
    def setAttributes(self):
        for src in self.srcList.values():
            src.setAttributes()
    def __getitem__(self, name):
        return self.srcList[name]
    def __setitem__(self, name, value):
        self.srcList[name] = value
        self.doc.childNodes[0].appendChild(value.node)
    def __delitem__(self, name):
        self.doc.childNodes[0].removeChild(self.srcList[name].node)
        del self.srcList[name]
    def names(self):
        return self.srcList.keys()
    def writeTo(self, filename=None):
        if filename == None:  # Overwrite the existing file.
            filename = self.filename
        self.setAttributes()
        try:
            doc = cleanXml(self.doc)
        except:
            doc = self.doc
        file = open(filename, 'w')
        file.write(doc.toxml() + '\n')
        file.close()

class DomElement:
    def __init__(self, node, converter=None):
        self.node = node
        attributes = {}
        for key in node.attributes.keys():
            if converter and key != "name" and key != "free":
                attributes[key] = converter(node.getAttribute(key))
# An ugly kludge here since each Parameter's "free" flag needs to be int.
            elif key == "free":
                attributes[key] = string.atoi(node.getAttribute(key))
            else:
                attributes[key] = node.getAttribute(key).encode("ascii")
        self.__dict__.update(attributes)
    def deleteChildElements(self, tagName):
        children = self.node.getElementsByTagName(tagName)
        for child in children:
            self.node.removeChild(child)
    def setAttributes(self):
        for key in self.node.attributes.keys():
            self.node.setAttribute(key, "%s" % self.__dict__[key])
        
class Source(DomElement):
    def __init__(self, node):
        DomElement.__init__(self, node)
        self.functions = {}
        (spectrum, ) = node.getElementsByTagName("spectrum")
        self.functions["spectrum"] = Function(spectrum)
        (spatialModel, ) = node.getElementsByTagName("spatialModel")
        self.functions["spatialModel"] = Function(spatialModel)
        self.__dict__.update(self.functions)
        self.show = 1
    def setAttributes(self):
        DomElement.setAttributes(self)
        for func in self.functions.values():
            func.setAttributes()
    def summary(self):
        if self.type == "PointSource":
            (line, ) = ("%s: %.2f; (RA, Dec) = (%.2f, %.2f)"
                        % (self.name, self.flux(), 
                           self.spatialModel.RA.value,
                           self.spatialModel.DEC.value), )
        else:
            line = "%s: %.2f" % (self.name, self.spectrum.Prefactor.value)
        return line
    def flux(self, emin=30):
        (prefactor, ) = (self.spectrum.Prefactor.value
                         *self.spectrum.Prefactor.scale, )
        gamma = -self.spectrum.Index.value
        e0 = self.spectrum.Scale.value
        return prefactor*e0/(gamma-1)*(emin/e0)**(1.-gamma)*1e8

class Function(DomElement):
    def __init__(self, node):
        DomElement.__init__(self, node)
        self.parameters = {}
        paramElements = node.getElementsByTagName("parameter")
        for param in paramElements:
            name = param.getAttribute("name").encode("ascii")
            self.parameters[name] = Parameter(param)
        self.__dict__.update(self.parameters)
    def setAttributes(self):
        DomElement.setAttributes(self)
        for param in self.parameters.values():
            param.setAttributes()

class Parameter(DomElement):
    def __init__(self, node):
        DomElement.__init__(self, node, string.atof)
