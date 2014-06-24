import os
import mako.template
import mako.lookup

class a(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

def tpl(cog, strfile, args):
  strfile = os.path.abspath(os.path.join(os.getcwd(),strfile))
  mylookup = mako.lookup.TemplateLookup(directories=[
    os.path.abspath(os.getcwd()),
    os.path.abspath(os.path.join(os.getcwd(),'..')),
    os.path.abspath(os.path.join(os.getcwd(),'..','..')),
    os.path.abspath(os.path.join(os.getcwd(),'..','..','..')),
    os.path.abspath(os.path.join(os.getcwd(),'..','..','..','..')),
    os.path.abspath(os.path.join(os.getcwd(),'..','..','..','..','..'))
  ])
  tplFromFile = mako.template.Template(filename=strfile, lookup=mylookup, imports=['from attrs import attrs'])
  cog.out(tplFromFile.render(a=args,p=args.prefix))