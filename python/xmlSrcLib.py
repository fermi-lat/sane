from xml.dom import minidom

powerLaw2 = """<spectrum type="PowerLaw2">
 <parameter free="1" max="1000.0" min="1e-05" name="Integral" scale="1e-06" value="1.0"/>
 <parameter free="1" max="-1.0" min="-5.0" name="Index" scale="1.0" value="-2.0"/>
 <parameter free="0" max="200000.0" min="20.0" name="LowerLimit" scale="1.0" value="30.0"/>
 <parameter free="0" max="200000.0" min="20.0" name="UpperLimit" scale="1.0" value="2e5"/>
</spectrum>
"""

bpl2 = """<spectrum type="BrokenPowerLaw2">
  <parameter free="1" max="1000.0" min="0.001" name="Integral" scale="1e-04" value="1.0"/>
  <parameter free="1" max="-1.0" min="-5.0" name="Index1" scale="1.0" value="-1.8"/>
  <parameter free="1" max="-1.0" min="-5.0" name="Index2" scale="1.0" value="-2.3"/>
  <parameter free="1" max="10000.0" min="30.0" name="BreakValue" scale="1.0" value="1000.0"/>
  <parameter free="0" max="200000.0" min="20.0" name="LowerLimit" scale="1.0" value="30.0"/>
  <parameter free="0" max="200000.0" min="20.0" name="UpperLimit" scale="1.0" value="2e5"/>
</spectrum>
"""

skyDir = """<spatialModel type="SkyDirFunction">
  <parameter free="0" max="360." min="-360." name="RA" scale="1.0" value="83.45"/>
  <parameter free="0" max="90." min="-90." name="DEC" scale="1.0" value="21.72"/>
</spatialModel>
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
               + '      <parameter max="-1" min="-3.5" free="0" '
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

def GalDiffuse():
    (src, ) = ('  <source name="Galactic Diffuse" '
               + 'type="DiffuseSource">\n'
               + '    <spectrum type="PowerLaw">\n'
               + '      <parameter max="1000" min="0.001" free="1" '
               + 'name="Prefactor" scale="0.001" value="11." />\n'
               + '      <parameter max="-1" min="-3.5" free="0" '
               + 'name="Index" scale="1" value="-2.1" />\n'
               + '      <parameter max="200" min="50" free="0" '
               + 'name="Scale" scale="1" value="100" />\n'
               + '    </spectrum>\n'
               + '    <spatialModel file="$(LIKELIHOODROOT)/src/test'
               + '/Data/gas.cel" type="SpatialMap">\n'
               + '      <parameter max="1000" min="0.001" free="0" '
               + 'name="Prefactor" scale="1" value="1" />\n'
               + '    </spatialModel>\n'
               + '  </source>\n', )
    galdif = minidom.parseString(src).getElementsByTagName('source')[0]
    return galdif
