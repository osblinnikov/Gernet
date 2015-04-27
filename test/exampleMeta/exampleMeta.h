#ifndef exampleMeta_test_gernet_osblinnikov_github_com_H
#define exampleMeta_test_gernet_osblinnikov_github_com_H

/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/

#include "github.com/osblinnikov/gernet/test/example3Meta/example3Meta.h"
#include "github.com/osblinnikov/gernet/test/block0/block0.h"
#include "github.com/osblinnikov/gernet/test/block3/block3.h"
#include "github.com/osblinnikov/gernet/test/block4/block4.h"
#include "github.com/osblinnikov/cnets/selector/selector.h"
#include "github.com/osblinnikov/cnets/mapBuffer/mapBuffer.h"
#include "github.com/osblinnikov/cnets/queue/queue.h"
#include "github.com/osblinnikov/cnets/runnablesContainer/runnablesContainer.h"
#include "github.com/osblinnikov/cnets/readerWriter/readerWriter.h"
#include "github.com/osblinnikov/cnets/types/types.h"

#undef exampleMeta_test_gernet_osblinnikov_github_com_EXPORT_API
#if defined WIN32 && !defined __MINGW32__ && !defined(CYGWIN) && !defined(EXAMPLEMETA_TEST_GERNET_OSBLINNIKOV_GITHUB_COM_STATIC)
  #ifdef exampleMeta_test_gernet_osblinnikov_github_com_EXPORT
    #define exampleMeta_test_gernet_osblinnikov_github_com_EXPORT_API __declspec(dllexport)
  #else
    #define exampleMeta_test_gernet_osblinnikov_github_com_EXPORT_API __declspec(dllimport)
  #endif
#else
  #define exampleMeta_test_gernet_osblinnikov_github_com_EXPORT_API extern
#endif

struct exampleMeta_test_gernet_osblinnikov_github_com;

exampleMeta_test_gernet_osblinnikov_github_com_EXPORT_API
void exampleMeta_test_gernet_osblinnikov_github_com_init(struct exampleMeta_test_gernet_osblinnikov_github_com *that,
    arrayObject _unsignedArr,
    uint32_t _parallelBlock,
    writer _wexportChannel0,
    reader _rimportChannel0);

exampleMeta_test_gernet_osblinnikov_github_com_EXPORT_API
void exampleMeta_test_gernet_osblinnikov_github_com_deinit(struct exampleMeta_test_gernet_osblinnikov_github_com *that);

typedef struct exampleMeta_test_gernet_osblinnikov_github_com{
    arrayObject unsignedArr;
  uint32_t parallelBlock;
  arrayObject longArr;
  arrayObject longArr_3;
  writer wexportChannel0;
  reader rimportChannel0;

  block0_test_gernet_osblinnikov_github_com* kernel0;
  block3_test_gernet_osblinnikov_github_com kernel1;
  block4_test_gernet_osblinnikov_github_com* kernel2;
  block0_test_gernet_osblinnikov_github_com* kernel3;
  block3_test_gernet_osblinnikov_github_com kernel4;
  block4_test_gernet_osblinnikov_github_com* kernel5;
  example3Meta_test_gernet_osblinnikov_github_com* kernel6;
  mapBuffer_cnets_osblinnikov_github_com mapBuffer1;
  mapBuffer_cnets_osblinnikov_github_com mapBuffer2;
  mapBuffer_cnets_osblinnikov_github_com mapBuffer1_3;
  mapBuffer_cnets_osblinnikov_github_com mapBuffer2_3;
  
runnablesContainer_cnets_osblinnikov_github_com* arrContainers;
  
  struct runnablesContainer_cnets_osblinnikov_github_com (*getRunnables)(struct exampleMeta_test_gernet_osblinnikov_github_com *that);
/*[[[end]]] (checksum: c26d5017daf05b385eee91ad4b54e377)*/

}exampleMeta_test_gernet_osblinnikov_github_com;

#endif /* exampleMeta_test_gernet_osblinnikov_github_com_H */