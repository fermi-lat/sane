"""
@brief Prototype xml entries for likelihood analysis
@author J. Chiang <jchiang@slac.stanford.edu>
"""
# $Header$
#
from xml.dom import minidom

filefunc = """<spectrum type="FileFunction" file="foo.dat">
 <parameter free="1" max="1e5" min="1e-5" name="Normalization" scale="1" value="1.0"/>
</spectrum>
"""

powerLaw = """<spectrum type="PowerLaw">
 <parameter free="1" max="1000.0" min="1e-03" name="Prefactor" scale="1e-09" value="1.0"/>
 <parameter free="1" max="-1.0" min="-5.0" name="Index" scale="1.0" value="-2.0"/>
 <parameter free="0" max="2000.0" min="30.0" name="Scale" scale="1.0" value="100.0"/>
</spectrum>
"""

powerLaw2 = """<spectrum type="PowerLaw2">
 <parameter free="1" max="1000.0" min="1e-05" name="Integral" scale="1e-06" value="1.0"/>
 <parameter free="1" max="0" min="-5.0" name="Index" scale="1.0" value="-2.0"/>
 <parameter free="0" max="300000.0" min="20.0" name="LowerLimit" scale="1.0" value="20.0"/>
 <parameter free="0" max="300000.0" min="20.0" name="UpperLimit" scale="1.0" value="2e5"/>
</spectrum>
"""

expcutoff = """<spectrum type="ExpCutoff">
  <parameter free="1" max="100000.0" min="0.01" name="Prefactor" scale="1e-09" value="50"/>
  <parameter free="1" max="-1.0" min="-5." name="Index" scale="1.0" value="-2.1"/>
  <parameter free="0" max="2000.0" min="30.0" name="Scale" scale="1.0" value="100.0"/>
  <parameter free="1" max="10000.0" min="1.0" name="Ebreak" scale="1.0" value="10.0"/>
  <parameter free="1" max="300.0" min="0.01" name="P1" scale="1000.0" value="100."/>
  <parameter free="0" max="1.0" min="-1.0" name="P2" scale="1.0" value="0"/>
  <parameter free="0" max="1.0" min="-1.0" name="P3" scale="1.0" value="0"/>
</spectrum>
"""

bpl2 = """<spectrum type="BrokenPowerLaw2">
  <parameter free="1" max="1000.0" min="0.001" name="Integral" scale="1e-04" value="1.0"/>
  <parameter free="1" max="0" min="-5.0" name="Index1" scale="1.0" value="-1.8"/>
  <parameter free="1" max="0" min="-5.0" name="Index2" scale="1.0" value="-2.3"/>
  <parameter free="1" max="10000.0" min="30.0" name="BreakValue" scale="1.0" value="1000.0"/>
  <parameter free="0" max="300000.0" min="20.0" name="LowerLimit" scale="1.0" value="20.0"/>
  <parameter free="0" max="300000.0" min="20.0" name="UpperLimit" scale="1.0" value="2e5"/>
</spectrum>
"""

skyDir = """<spatialModel type="SkyDirFunction">
  <parameter free="0" max="360." min="-360." name="RA" scale="1.0" value="83.45"/>
  <parameter free="0" max="90." min="-90." name="DEC" scale="1.0" value="21.72"/>
</spatialModel>
"""

galProp = """<source name="GalProp Diffuse" type="DiffuseSource">
   <!-- diffuse source units are cm^-2 s^-1 MeV^-1 sr^-1 -->
   <spectrum type="ConstantValue">
      <parameter free="1" max="10" min="0" name="Value" scale="1" value="1"/>
   </spectrum>
   <spatialModel file="$(GALPROP_MODEL)" type="MapCubeFunction">
      <parameter free="0" max="1000" min="0.001" name="Normalization" scale="1" value="1"/>
   </spatialModel>
</source>
"""

def ptSrc(bpl=False):
    if bpl:
        spectrum = bpl2
    else:
        spectrum = powerLaw2
    (src, ) = ('  <source name=" " type="PointSource">\n'
               + spectrum + skyDir + '  </source>\n', )
    ptsrc = minidom.parseString(src).getElementsByTagName('source')[0]
    return ptsrc

def EGDiffuse():
    (src, ) = ('   <source name="Extragalactic Diffuse" '
               + 'type="DiffuseSource">\n'
               + '    <spectrum type="PowerLaw">\n'
               + '      <parameter max="100" min="1e-05" free="1" '
               + 'name="Prefactor" scale="1e-07" value="1.60" />\n'
               + '      <parameter max="-1" min="-3.5" free="1" '
               + 'name="Index" scale="1" value="-2.1" />\n'
               + '      <parameter max="200" min="50" free="0" '
               + 'name="Scale" scale="1" value="100" />\n'
               + '    </spectrum>\n'
               + '    <spatialModel type="ConstantValue">\n'
               + '       <parameter max="10" min="0" free="0" '
               + 'name="Value" scale="1" value="1" />\n'
               + '    </spatialModel>\n'
               + '  </source>\n', )
    egdif = minidom.parseString(src).getElementsByTagName('source')[0]
    return egdif

def EgretDiffuse():
    (src, ) = ('  <source name="EGRET Diffuse" '
               + 'type="DiffuseSource">\n'
               + '    <spectrum type="PowerLaw">\n'
               + '      <parameter max="1000" min="0.001" free="1" '
               + 'name="Prefactor" scale="0.001" value="11." />\n'
               + '      <parameter max="-1" min="-3.5" free="0" '
               + 'name="Index" scale="1" value="-2.1" />\n'
               + '      <parameter max="200" min="50" free="0" '
               + 'name="Scale" scale="1" value="100" />\n'
               + '    </spectrum>\n'
               + '    <spatialModel file="$(EXTFILESSYS)/galdiffuse'
               + '/EGRET_diffuse_gal.fits" type="SpatialMap">\n'
               + '      <parameter max="1000" min="0.001" free="0" '
               + 'name="Prefactor" scale="1" value="1" />\n'
               + '    </spatialModel>\n'
               + '  </source>\n', )
    galdif = minidom.parseString(src).getElementsByTagName('source')[0]
    return galdif

def GalProp():
    galdif = minidom.parseString(galProp).getElementsByTagName('source')[0]
    return galdif

def GalDiffuse():
    return EgretDiffuse()

