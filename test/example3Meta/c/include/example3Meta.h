#ifndef com_github_osblinnikov_gernet_test_example3Meta_H
#define com_github_osblinnikov_gernet_test_example3Meta_H

/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/

#include "github.com/osblinnikov/gernet/test/block0/c/include/block0.h"
#include "github.com/osblinnikov/gernet/test/block3/c/include/block3.h"
#include "github.com/osblinnikov/gernet/test/block4/c/include/block4.h"
#include "github.com/osblinnikov/cnets/mapBuffer/c/include/mapBuffer.h"
#include "github.com/osblinnikov/cnets/queue/c/include/queue.h"
#include "github.com/osblinnikov/cnets/runnablesContainer/c/include/runnablesContainer.h"
#include "github.com/osblinnikov/cnets/readerWriter/c/include/readerWriter.h"
#include "github.com/osblinnikov/cnets/types/c/include/types.h"
#include "github.com/osblinnikov/cnets/selector/c/include/selector.h"

#undef com_github_osblinnikov_gernet_test_example3Meta_EXPORT_API
#if defined WIN32 && !defined __MINGW32__ && !defined(CYGWIN) && !defined(COM_GITHUB_OSBLINNIKOV_GERNET_TEST_EXAMPLE3META_STATIC)
  #ifdef com_github_osblinnikov_gernet_test_example3Meta_EXPORT
    #define com_github_osblinnikov_gernet_test_example3Meta_EXPORT_API __declspec(dllexport)
  #else
    #define com_github_osblinnikov_gernet_test_example3Meta_EXPORT_API __declspec(dllimport)
  #endif
#else
  #define com_github_osblinnikov_gernet_test_example3Meta_EXPORT_API extern
#endif

struct com_github_osblinnikov_gernet_test_example3Meta;

com_github_osblinnikov_gernet_test_example3Meta_EXPORT_API
void com_github_osblinnikov_gernet_test_example3Meta_init(struct com_github_osblinnikov_gernet_test_example3Meta *that,
    unsigned[] _unsignedArr,
    unsigned _parallelBlock,
    writer _wexportChannel0,
    reader _rimportChannel0);

com_github_osblinnikov_gernet_test_example3Meta_EXPORT_API
void com_github_osblinnikov_gernet_test_example3Meta_deinit(struct com_github_osblinnikov_gernet_test_example3Meta *that);

typedef struct com_github_osblinnikov_gernet_test_example3Meta{
    arrayObject unsignedArr;
  uint32_t parallelBlock;
  arrayObject longArr;
  writer wexportChannel0;
  reader rimportChannel0;

  com_github_osblinnikov_gernet_test_block0* kernel0;
  com_github_osblinnikov_gernet_test_block3 kernel1;
  com_github_osblinnikov_gernet_test_block4* kernel2;
  com_github_osblinnikov_cnets_mapBuffer mapBuffer1;
  com_github_osblinnikov_cnets_mapBuffer mapBuffer2;
  
com_github_osblinnikov_cnets_runnablesContainer* arrContainers;
  
  struct com_github_osblinnikov_cnets_runnablesContainer (*getRunnables)(struct com_github_osblinnikov_gernet_test_example3Meta *that);
/*[[[end]]] (checksum: 26cbb230cb2383d3a6ffe6567816ee79)*/

}com_github_osblinnikov_gernet_test_example3Meta;

#endif /* com_github_osblinnikov_gernet_test_example3Meta_H */