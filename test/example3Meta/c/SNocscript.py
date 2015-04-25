from helper import *
#           Environment
Import( 'env' )

def add_dependencies(env):
  '''[[[cog
  import cogging as c
  c.tpl(cog,templateFile,c.a(prefix=configFile))
  ]]]'''

  AddDependency(env,'com_github_osblinnikov_gernet_test_block0','github.com/osblinnikov/gernet/test/block0/c')
  AddDependency(env,'com_github_osblinnikov_gernet_test_block3','github.com/osblinnikov/gernet/test/block3/c')
  AddDependency(env,'com_github_osblinnikov_gernet_test_block4','github.com/osblinnikov/gernet/test/block4/c')
  AddDependency(env,'com_github_osblinnikov_cnets_mapBuffer','github.com/osblinnikov/cnets/mapBuffer/c')
  AddDependency(env,'com_github_osblinnikov_cnets_queue','github.com/osblinnikov/cnets/queue/c')
  AddDependency(env,'com_github_osblinnikov_cnets_runnablesContainer','github.com/osblinnikov/cnets/runnablesContainer/c')
  AddDependency(env,'com_github_osblinnikov_cnets_readerWriter','github.com/osblinnikov/cnets/readerWriter/c')
  AddDependency(env,'com_github_osblinnikov_cnets_types','github.com/osblinnikov/cnets/types/c')
  AddDependency(env,'com_github_osblinnikov_cnets_selector','github.com/osblinnikov/cnets/selector/c')
  '''[[[end]]] (checksum: b763830224ef0824b363e018415b0514)'''
  AddPthreads(env)
  # AddNetwork(env) 

c = {}
c['PROG_NAME'] = 'com_github_osblinnikov_gernet_test_example3Meta'
c['sourceFiles'] = ['example3Meta.c']
c['testFiles'] = ['example3MetaTest.c']
c['runFiles'] = ['main.c']
c['defines'] = []
c['inclDeps'] = add_dependencies
DefaultLibraryConfig(env, c)