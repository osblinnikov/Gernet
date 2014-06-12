<%
import sys
sys.path.insert(0, a.parserPath)

import parsing_c as p
p.parsingGernet(a)

%>
from helper import *
#           Environment
Import( 'env', 'args' )

def add_dependencies(env, args):
  '''[[[cog
  import cogging as c
  c.tpl(cog,templateFile,c.a(prefix=configFile))
  ]]]'''
  '''[[[end]]]'''
  AddPthreads(env, args)
  # AddNetwork(args) 

c = {}
c['PROG_NAME'] = '${a.fullName_}'
c['sourceFiles'] = ['${a.className}.c']
c['testFiles'] = ['${a.className}Test.c']
c['runFiles'] = ['main.c']
c['defines'] = []
c['inclDepsDynamic'] = add_dependencies
c['inclDepsStatic'] = add_dependencies
DefaultLibraryConfig(c, env, args)