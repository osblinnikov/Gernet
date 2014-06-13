
from helper import *
#           Environment
Import( 'env', 'args' )

def add_dependencies(env, args):
    '''[[[cog
    import cogging as c
    c.tpl(cog,templateFile,c.a(prefix=configFile))
    ]]]'''

    AddDependency(args,'com_github_airutech_cnets_types',join(args['PROJECTS_ROOT_PATH'],'src/github.com/airutech/cnets/types/c'))
    AddDependency(args,'com_github_airutech_cnets_readerWriter',join(args['PROJECTS_ROOT_PATH'],'src/github.com/airutech/cnets/readerWriter/c'))
    AddDependency(args,'com_github_airutech_cnets_queue',join(args['PROJECTS_ROOT_PATH'],'src/github.com/airutech/cnets/queue/c'))
    '''[[[end]]] (checksum: 2e57f3ffe3b475a13699853e26636540)'''
    # AddPthreads(env, args)
    # AddNetwork(args)

c = {}
c['PROG_NAME'] = 'com_github_airutech_gernet_test_buf'
c['sourceFiles'] = ['buf.c']
c['testFiles'] = ['bufTest.c']
c['runFiles'] = ['main.c']
c['defines'] = []
c['inclDepsDynamic'] = add_dependencies
c['inclDepsStatic'] = add_dependencies
DefaultLibraryConfig(c, env, args)