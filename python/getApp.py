import sys, os
from pil import Pil

bindir = os.environ['BINDIR']

def getApp(appName, package=None):
    if not package:
        package = appName
    app = os.path.join(os.environ[package.upper() + 'ROOT'], bindir,
                       appName + '.exe')
    pars = Pil(appName + '.par')
    return (app, pars)
