from helper import *
#           Environment
Import( 'env' )

def add_dependencies(env):
  '''[[[cog
  import cogging as c
  c.tpl(cog,templateFile,c.a(prefix=configFile))
  ]]]'''

  AddDependency(env,'example3Meta_test_gernet_osblinnikov_github_com','github.com/osblinnikov/gernet/test/example3Meta')
  AddDependency(env,'block0_test_gernet_osblinnikov_github_com','github.com/osblinnikov/gernet/test/block0')
  AddDependency(env,'block3_test_gernet_osblinnikov_github_com','github.com/osblinnikov/gernet/test/block3')
  AddDependency(env,'block4_test_gernet_osblinnikov_github_com','github.com/osblinnikov/gernet/test/block4')
  AddDependency(env,'selector_cnets_osblinnikov_github_com','github.com/osblinnikov/cnets/selector')
  AddDependency(env,'mapBuffer_cnets_osblinnikov_github_com','github.com/osblinnikov/cnets/mapBuffer')
  AddDependency(env,'queue_cnets_osblinnikov_github_com','github.com/osblinnikov/cnets/queue')
  AddDependency(env,'runnablesContainer_cnets_osblinnikov_github_com','github.com/osblinnikov/cnets/runnablesContainer')
  AddDependency(env,'readerWriter_cnets_osblinnikov_github_com','github.com/osblinnikov/cnets/readerWriter')
  AddDependency(env,'types_cnets_osblinnikov_github_com','github.com/osblinnikov/cnets/types')
  '''[[[end]]] (checksum: 7946f2b570fa68a63ad91a9d33a3a487)'''
  AddPthreads(env)
  # AddNetwork(env) 

c = {}
c['PROG_NAME'] = 'example2Meta_test_gernet_osblinnikov_github_com'
# c['sourceFiles'] = ['example2Meta.c']
c['testFiles'] = ['example2MetaTest.c']
# c['runFiles'] = ['main.c']
# c['defines'] = []
c['inclDeps'] = add_dependencies
DefaultLibraryConfig(env, c)