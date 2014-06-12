import os
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