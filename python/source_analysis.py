"""
Automated point source analysis within specified regions-of-interest.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#
import os, sys, glob
import tempfile
from xml.dom import minidom
import celgal
from makeSrcList import SourceList

from gt_apps import diffResp, filter, expCube, expMap, like

def haveFile(filename):
    try:
        open(filename)
        return True
    except IOError:
        return False

def parseRoiLine(line):
    id, ra, dec, radius = line.split()
    id = int(id)
    ra = float(ra)
    dec = float(dec)
    radius = float(radius)
    return id, ra, dec, radius

class SourceAnalysis(object):
    def __init__(self, eventfiles, scfiles, srclist=None, erange=(30, 2e5),
                 trange=None, sourceRegionRadius=30., irfs='DC1',
                 expCubeFile='expCubeFile.fits', exclude=(),
                 output_dir=os.curdir, verbose=False, retainFiles=False):
        self.eventfiles = self._addAbsPath(eventfiles)
        self.scfiles = self._addAbsPath(scfiles)
        self.srclist = srclist
        self.emin = erange[0]
        self.emax = erange[1]
        self.trange = trange
        self.sr_radius = sourceRegionRadius
        self.irfs = irfs
        self.expCubeFile = self._addAbsPath((expCubeFile,))[0]
        self.exclude = exclude
        self.output_dir = os.path.abspath(output_dir)
        self.verbose = verbose
        self.retainFiles = retainFiles
        self.home_dir = os.path.abspath(os.curdir)
        self.computeDiffuseResps()
        self._makeExpCube()
    def computeDiffuseResps(self, srcModelFile=None):
        if srcModelFile is not None:
            self._runDiffResps(srcModelFile)
        else:
            try:
                fd, diffModel = tempfile.mkstemp(dir=self.output_dir)
                os.close(fd)
                self.srclist.makeSrcModel(diffModel, (0, 0, 20.),
                                          exclude=self.exclude)
                self._runDiffResps(diffModel)
            except AttributeError:
                pass
            os.remove(diffModel)
    def run(self, roiCone, id, srcModelFile=None, optimizer='MINUIT',
            diffuseSrcs=("Extragalactic Diffuse", "Galactic Diffuse")):
        self._applyCuts(roiCone, id)
        l, b = celgal.celgal().gal(roiCone[:2])
        roi = (l, b, self.sr_radius)
        like['statistic'] = 'UNBINNED'
        if srcModelFile is not None:
            like['source_model_file'] = srcModelFile
        else:
            like['source_model_file'] = self._sourceModelFile(roi, id)
        like['source_model_output_file'] = like['source_model_file']
        like['evfile'] = self.eventfilelist
        like['scfile'] = self._scFiles()
        like['optimizer'] = optimizer
        like['exposure_map_file'] = self._expMapFile(id)
        os.chdir(self.output_dir)
        input, output = like.runWithOutput()
        lines = output.readlines()
        results = {}
        for i, line in zip(xrange(sys.maxint), lines):
            sys.stdout.write(line)
            if line.find("TS value: ") != -1:
                src = lines[i-6].split(':')[0]
                results[src] = {}
                for j in range(i-5, i+1):
                    key, value = tuple(lines[j].split(': '))
                    results[src][key] = value.strip()
            for src in diffuseSrcs:
                if line.find(src) != -1:
                    results[src] = {}
                    for j in range(i+1, i+5):
                        key, value = tuple(lines[j].split(': '))
                        results[src][key] = value.strip()
        self._addResults(results, like['source_model_output_file'])
        os.remove(like['scfile'])
        os.remove(self.eventfilelist)
        if not self.retainFiles:
            for file in self.filtered_files:
                os.remove(file)
        os.chdir(self.home_dir)
        return results
    def _addAbsPath(self, files):
        my_files = []
        for file in files:
            my_files.append(os.path.abspath(file))
        return my_files
    def _scFiles(self):
        fd, filename = tempfile.mkstemp(dir=self.output_dir)
        for file in self.scfiles:
            os.write(fd, file + "\n")
        os.close(fd)
        return filename
    def _runDiffResps(self, diffModel):
        scfiles = self._scFiles()
        for file in self.eventfiles:
            diffResp['evfile'] = file
            diffResp['scfile'] = scfiles
            diffResp['source_model_file'] = diffModel
            diffResp['rspfunc'] = self.irfs
            diffResp['clobber'] = 'no'
            diffResp.run(catchError=None)
        os.remove(scfiles)
    def _makeExpCube(self):
        if not haveFile(self.expCubeFile):
            expCube['evfile'] = self.eventfiles[0]
            expCube['scfile'] = self._scFiles()
            expCube['outfile'] = self.expCubeFile
            expCube['cos_theta_step'] = 0.05
            expCube['pixel_size'] = 1
            expCube.run(catchError=None)
            os.remove(expCube['scfile'])
    def _applyCuts(self, roiCone, id=None):
        ra, dec, radius = roiCone
        filter['ra'] = ra
        filter['dec'] = dec
        filter['rad'] = radius
        filter['emin'] = self.emin
        filter['emax'] = self.emax
        if self.trange is not None:
            filter['tmin'] = self.trange[0]
            filter['tmax'] = self.trange[1]
        self.filtered_files = []
        fd, self.eventfilelist = tempfile.mkstemp(dir=self.output_dir)
        for file in self.eventfiles:
            filter['input_file'] = file
            filtered_file = os.path.basename(file) + '_filtered'
            if id is not None:
                filtered_file += '_%s' % id
            filter['output_file'] = os.path.join(self.output_dir,
                                                 filtered_file)
            self.filtered_files.append(filter['output_file'])
            filter.run(catchError=None)
            os.write(fd, self.filtered_files[-1] + "\n")
        os.close(fd)
    def _expMapFile(self, id):
        expMap['evfile'] = self.filtered_files[0]
        expMap['outfile'] = os.path.join(self.output_dir,
                                         'expMap_%s.fits' % id)
        expMap['rspfunc'] = self.irfs
        expMap['exposure_cube_file'] = self.expCubeFile
        expMap['source_region_radius'] = self.sr_radius
        if not haveFile(expMap['outfile']):
            expMap['scfile'] = self._scFiles()
            expMap.run(catchError=None)
            os.remove(expMap['scfile'])
        return expMap['outfile']
    def _sourceModelFile(self, roiCone, id):
        srcModelFile = os.path.join(self.output_dir, 'srcModel_%s.xml' % id)
        self.srclist.makeSrcModel(srcModelFile, roiCone, exclude=self.exclude)
        return srcModelFile
    def _addResults(self, results, sourceModelFile):
        doc = minidom.parse(sourceModelFile)
        srcs = doc.getElementsByTagName('source')
        for src in srcs:
            name = src.getAttribute('name').encode()
            result = results[name]
            src.setAttribute("Npred", result['Npred'])
            try:
                src.setAttribute("TS_value", result['TS value'])
            except KeyError:
                pass
            try:
                src.setAttribute("ROI_dist", result['ROI distance'])
            except KeyError:
                pass
            params = src.getElementsByTagName('parameter')
            for param in params:
                parname = param.getAttribute('name')
                if parname in result:
                    try:
                        error = result[parname].split("+/-")[1].strip()
                        param.setAttribute("error", error)
                    except:
                        pass
        doc.writexml(open(sourceModelFile, 'w'))
            
if __name__ == '__main__':
    sourceList = SourceList('3EG_src_list.dat', coordsys='CEL')
    roiFile = 'Roi_list.dat'
    roiCones = {}
    roiList = open(roiFile)
    for line in roiList:
        id, ra, dec, radius = parseRoiLine(line)
        roiCones[id] = (ra, dec, radius)

    eventfiles = ['ptsrcs_events_0000.fits', 'eg_diffuse_events_0000.fits',
                  'galdiffuse_events_0000.fits']
    exclude = ()
#    eventfiles = ['ptsrcs_events_0000.fits', 'eg_diffuse_events_0000.fits']
#    exclude = ('galdiffuse',)
#    eventfiles = ['ptsrcs_events_0000.fits']
#    exclude = ('eg_diffuse', 'galdiffuse')

    scfiles = ('ptsrcs_scData_0000.fits',)

    srcAnalysis = SourceAnalysis(eventfiles, scfiles, srclist=sourceList,
                                 exclude=exclude)
    for id in roiCones:
        srcAnalysis.run(roiCones[id], id)
    srcAnalysis.clean()
