/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/

#include "../include/example3Meta.h"
#include <stdlib.h>

void com_github_osblinnikov_gernet_test_example3Meta_run(void *that);
void com_github_osblinnikov_gernet_test_example3Meta_onStart(void *that);
void com_github_osblinnikov_gernet_test_example3Meta_onStop(void *that);
void com_github_osblinnikov_gernet_test_example3Meta_onCreate(struct com_github_osblinnikov_gernet_test_example3Meta *that);
void com_github_osblinnikov_gernet_test_example3Meta_onDestroy(struct com_github_osblinnikov_gernet_test_example3Meta *that);

struct com_github_osblinnikov_cnets_runnablesContainer com_github_osblinnikov_gernet_test_example3Meta_getRunnables(struct com_github_osblinnikov_gernet_test_example3Meta *that){
  
    com_github_osblinnikov_cnets_runnablesContainer_create(runnables)
    
    int j;
    for(j=0;j<(int)3;j++){
      that->arrContainers[0+j] = that->kernel0[j].getRunnables(&that->kernel0[j]);
    }
    that->arrContainers[0+3] = that->kernel1.getRunnables(&that->kernel1);
    for(j=0;j<(int)that->parallelBlock;j++){
      that->arrContainers[4+j] = that->kernel2[j].getRunnables(&that->kernel2[j]);
    }

    arrayObject arr;
    arr.array = (void*)&that->arrContainers;
    arr.length = 0+3+1+that->parallelBlock;
    arr.itemSize = sizeof(com_github_osblinnikov_cnets_runnablesContainer);
    runnables.setContainers(&runnables,arr);
    return runnables;
}

void com_github_osblinnikov_gernet_test_example3Meta_init(struct com_github_osblinnikov_gernet_test_example3Meta *that,
    unsigned[] _unsignedArr,
    unsigned _parallelBlock,
    writer _wexportChannel0,
    reader _rimportChannel0){
  
  that->unsignedArr = _unsignedArr;
  that->parallelBlock = _parallelBlock;
  that->wexportChannel0 = _wexportChannel0;
  that->rimportChannel0 = _rimportChannel0;
  that->longArr = arrayObject_init_dynamic(sizeof(int64_t), 10);
  com_github_osblinnikov_cnets_mapBuffer_init(&that->mapBuffer1,that->unsignedArr,1000L,1);
  com_github_osblinnikov_cnets_mapBuffer_init(&that->mapBuffer2,that->longArr,1000L,1);
  writer mapBuffer1w0_0 = com_github_osblinnikov_cnets_mapBuffer_createReader(&that->mapBuffer1,0)
  writer mapBuffer2w1_0 = com_github_osblinnikov_cnets_mapBuffer_createReader(&that->mapBuffer2,0)
  reader mapBuffer1r0_1 = com_github_osblinnikov_cnets_mapBuffer_createWriter(&that->mapBuffer1,0)
  reader mapBuffer2r1_1 = com_github_osblinnikov_cnets_mapBuffer_createWriter(&that->mapBuffer2,0)
  com_github_osblinnikov_gernet_test_example3Meta_onKernels(that);
  that->kernel0 = (com_github_osblinnikov_gernet_test_block0*)arrayObject_init_dynamic(sizeof(com_github_osblinnikov_gernet_test_block0),3);
  int _kernel0_i;
  for(_kernel0_i=0;_kernel0_i<(int)3;_kernel0_i++){
    com_github_osblinnikov_gernet_test_block0_init(&that->kernel0[_kernel0_i],mapBuffer1w0_0,mapBuffer2w1_0,that->wexportChannel0);
  }
  com_github_osblinnikov_gernet_test_block3_init(&that->kernel1,mapBuffer1r0_1,mapBuffer2r1_1);
  that->kernel2 = (com_github_osblinnikov_gernet_test_block4*)arrayObject_init_dynamic(sizeof(com_github_osblinnikov_gernet_test_block4),that->parallelBlock);
  int _kernel2_i;
  for(_kernel2_i=0;_kernel2_i<(int)that->parallelBlock;_kernel2_i++){
    com_github_osblinnikov_gernet_test_block4_init(&that->kernel2[_kernel2_i],that->rimportChannel0);
  }
  that->arrContainers = arrayObject_init_dynamic(sizeof(com_github_osblinnikov_cnets_runnablesContainer),0+3+1+that->parallelBlock);
  that->getRunnables = com_github_osblinnikov_gernet_test_example3Meta_getRunnables;
  com_github_osblinnikov_gernet_test_example3Meta_onCreate(that);
}

void com_github_osblinnikov_gernet_test_example3Meta_deinit(struct com_github_osblinnikov_gernet_test_example3Meta *that){
  com_github_osblinnikov_gernet_test_example3Meta_onDestroy(that);
}

/*[[[end]]] (checksum: 529dcef97397a8816573a2fcb4095d7d)*/

void com_github_osblinnikov_gernet_test_example3Meta_run(void *t){
  /*struct com_github_osblinnikov_gernet_test_example3Meta *that = (struct com_github_osblinnikov_gernet_test_example3Meta*)t;*/
}

void com_github_osblinnikov_gernet_test_example3Meta_onStart(void *t){
  /*struct com_github_osblinnikov_gernet_test_example3Meta *that = (struct com_github_osblinnikov_gernet_test_example3Meta*)t;*/
}

void com_github_osblinnikov_gernet_test_example3Meta_onStop(void *that){
  /*struct com_github_osblinnikov_gernet_test_example3Meta *that = (struct com_github_osblinnikov_gernet_test_example3Meta*)t;*/
}

void com_github_osblinnikov_gernet_test_example3Meta_onCreate(struct com_github_osblinnikov_gernet_test_example3Meta *that){
  
  return;
}

void com_github_osblinnikov_gernet_test_example3Meta_onDestroy(struct com_github_osblinnikov_gernet_test_example3Meta *that){
  
  return;
}

void com_github_osblinnikov_gernet_test_example3Meta_onKernels(struct com_github_osblinnikov_gernet_test_example3Meta *that){
  
  return;
}