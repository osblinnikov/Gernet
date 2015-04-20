<%
import sys
sys.path.insert(0, a.parserPath)

import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)

%>
from helper import *
#           Environment
Import( 'env' )

def add_dependencies(env):
  '''[[[cog
  import cogging as c
  c.tpl(cog,templateFile,c.a(prefix=configFile))
  ]]]'''
  '''[[[end]]]'''
  AddPthreads(env)
  # AddNetwork(env) 

c = {}
c['PROG_NAME'] = '${a.fullName_}'
c['sourceFiles'] = ['${a.className}.c']
c['testFiles'] = ['${a.className}Test.c']
c['runFiles'] = ['main.c']
c['defines'] = []
c['inclDeps'] = add_dependencies
DefaultLibraryConfig(env, c)