from xml.dom import minidom

def ptSrc():
    (src, ) = ('  <source name=" " type="PointSource">\n'
               + '    <spectrum type="PowerLaw">\n'
               + '      <parameter free="1" max="1000.0" min="1e-5" '
               + 'name="Prefactor" scale="1e-09" value="1"/>\n'
               + '      <parameter free="1" max="-1.0" min="-5." '
               + 'name="Index" scale="1.0" value="-2.1"/>\n'
               + '      <parameter free="0" max="2000.0" min="30.0" '
               + 'name="Scale" scale="1.0" value="100.0"/>\n'
               + '    </spectrum>\n'
               + '    <spatialModel type="SkyDirFunction">\n'
               + '      <parameter free="0" max="360." '
               + 'min="-360." name="RA" scale="1.0" value="83.45"/>\n'
               + '      <parameter free="0" max="90." '
               + 'min="-90." name="DEC" scale="1.0" value="21.72"/>\n'
               + '    </spatialModel>\n'
               + '  </source>\n', )
    ptsrc = minidom.parseString(src).getElementsByTagName('source')[0]
    return ptsrc

def EGDiffuse():
    (src, ) = ('   <source name="Extragalactic Diffuse" '
               + 'type="DiffuseSource">\n'
               + '    <spectrum type="PowerLaw">\n'
               + '      <parameter max="100" min="1e-05" free="1" '
               + 'name="Prefactor" scale="1e-07" value="1.45" />\n'
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
