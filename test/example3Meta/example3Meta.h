#ifndef example3Meta_test_gernet_osblinnikov_github_com_H
#define example3Meta_test_gernet_osblinnikov_github_com_H

/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/

#include "github.com/osblinnikov/gernet/test/block0/block0.h"
#include "github.com/osblinnikov/gernet/test/block3/block3.h"
#include "github.com/osblinnikov/gernet/test/block4/block4.h"
#include "github.com/osblinnikov/cnets/selector/selector.h"
#include "github.com/osblinnikov/cnets/mapBuffer/mapBuffer.h"
#include "github.com/osblinnikov/cnets/queue/queue.h"
#include "github.com/osblinnikov/cnets/runnablesContainer/runnablesContainer.h"
#include "github.com/osblinnikov/cnets/readerWriter/readerWriter.h"
#include "github.com/osblinnikov/cnets/types/types.h"

#undef example3Meta_test_gernet_osblinnikov_github_com_EXPORT_API
#if defined WIN32 && !defined __MINGW32__ && !defined(CYGWIN) && !defined(EXAMPLE3META_TEST_GERNET_OSBLINNIKOV_GITHUB_COM_STATIC)
  #ifdef example3Meta_test_gernet_osblinnikov_github_com_EXPORT
    #define example3Meta_test_gernet_osblinnikov_github_com_EXPORT_API __declspec(dllexport)
  #else
    #define example3Meta_test_gernet_osblinnikov_github_com_EXPORT_API __declspec(dllimport)
  #endif
#else
  #define example3Meta_test_gernet_osblinnikov_github_com_EXPORT_API extern
#endif

struct example3Meta_test_gernet_osblinnikov_github_com;

example3Meta_test_gernet_osblinnikov_github_com_EXPORT_API
void example3Meta_test_gernet_osblinnikov_github_com_init(struct example3Meta_test_gernet_osblinnikov_github_com *that,
    arrayObject _unsignedArr,
    uint32_t _parallelBlock,
    writer _wexportChannel0,
    reader _rimportChannel0);

example3Meta_test_gernet_osblinnikov_github_com_EXPORT_API
void example3Meta_test_gernet_osblinnikov_github_com_deinit(struct example3Meta_test_gernet_osblinnikov_github_com *that);

typedef struct example3Meta_test_gernet_osblinnikov_github_com{
    arrayObject unsignedArr;
  uint32_t parallelBlock;
  arrayObject longArr;
  writer wexportChannel0;
  reader rimportChannel0;

  block0_test_gernet_osblinnikov_github_com* kernel0;
  block3_test_gernet_osblinnikov_github_com kernel1;
  block4_test_gernet_osblinnikov_github_com* kernel2;
  mapBuffer_cnets_osblinnikov_github_com mapBuffer1;
  mapBuffer_cnets_osblinnikov_github_com mapBuffer2;
  
runnablesContainer_cnets_osblinnikov_github_com* arrContainers;
  
  struct runnablesContainer_cnets_osblinnikov_github_com (*getRunnables)(struct example3Meta_test_gernet_osblinnikov_github_com *that);
/*[[[end]]] (checksum: 0a35286725404122ed5ffe52ac462a3a)*/

}example3Meta_test_gernet_osblinnikov_github_com;

#endif /* example3Meta_test_gernet_osblinnikov_github_com_H */