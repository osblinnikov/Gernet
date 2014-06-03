import os.path
import os, sys, inspect
# realpath() with make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
  sys.path.insert(0, cmd_folder)

# use this if you want to include modules from a subforder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"tools/Mako")))
if cmd_subfolder not in sys.path:
  sys.path.insert(0, cmd_subfolder)

from mako.template import Template
from mako.lookup import TemplateLookup

class a(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

def tpl(cog, strfile, args):
  strfile = os.path.abspath(os.path.join(os.getcwd(),strfile))
  mylookup = TemplateLookup(directories=[
    os.path.abspath(os.getcwd()),
    os.path.abspath(os.path.join(os.getcwd(),'..')),
    os.path.abspath(os.path.join(os.getcwd(),'..','..')),
    os.path.abspath(os.path.join(os.getcwd(),'..','..','..')),
    os.path.abspath(os.path.join(os.getcwd(),'..','..','..','..')),
    os.path.abspath(os.path.join(os.getcwd(),'..','..','..','..','..'))
  ])
  tplFromFile = Template(filename=strfile, lookup=mylookup, imports=['from attrs import attrs'])
  cog.out(tplFromFile.render(a=args,p=args.prefix))