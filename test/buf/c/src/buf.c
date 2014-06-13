/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/

#include "../include/buf.h"

void* com_github_airutech_gernet_test_buf_readNext(bufferKernelParams *params, BOOL make_timeout);
bufferReadData com_github_airutech_gernet_test_buf_readNextWithMeta(bufferKernelParams *params, BOOL make_timeout);
int com_github_airutech_gernet_test_buf_readFinished(bufferKernelParams *params);
void* com_github_airutech_gernet_test_buf_writeNext(bufferKernelParams *params, BOOL make_timeout);
int com_github_airutech_gernet_test_buf_writeFinished(bufferKernelParams *params);
int com_github_airutech_gernet_test_buf_size(bufferKernelParams *params);
int com_github_airutech_gernet_test_buf_timeout(bufferKernelParams *params);
int com_github_airutech_gernet_test_buf_gridSize(bufferKernelParams *params);
int com_github_airutech_gernet_test_buf_uniqueId(bufferKernelParams *params);
int com_github_airutech_gernet_test_buf_addSelector(bufferKernelParams *params, void* selectorContainer);
void com_github_airutech_gernet_test_buf_onCreate(com_github_airutech_gernet_test_buf *that);
void com_github_airutech_gernet_test_buf_onDestroy(com_github_airutech_gernet_test_buf *that);

reader com_github_airutech_gernet_test_buf_getReader(com_github_airutech_gernet_test_buf *that, void* container, int grid_id){
  bufferKernelParams_create(params, that, grid_id, container,com_github_airutech_gernet_test_buf_)
  reader_create(res,params)
  return res;
}

writer com_github_airutech_gernet_test_buf_getWriter(com_github_airutech_gernet_test_buf *that, void* container, int grid_id){
  bufferKernelParams_create(params, that, grid_id, container,com_github_airutech_gernet_test_buf_)
  writer_create(res,params)
  return res;
}

void com_github_airutech_gernet_test_buf_initialize(com_github_airutech_gernet_test_buf *that){
  com_github_airutech_gernet_test_buf_onCreate(that);
}

void com_github_airutech_gernet_test_buf_deinitialize(struct com_github_airutech_gernet_test_buf *that){
  com_github_airutech_gernet_test_buf_onDestroy(that);
}
/*[[[end]]] (checksum: b5961eaa7a6623b8a788ec7e0f4c0e8c)*/

void com_github_airutech_gernet_test_buf_onCreate(com_github_airutech_gernet_test_buf *that){
  
  return;
}

void com_github_airutech_gernet_test_buf_onDestroy(com_github_airutech_gernet_test_buf *that){
  
  return;
}

void* com_github_airutech_gernet_test_buf_readNext(bufferKernelParams *params, BOOL make_timeout) {
  bufferReadData res = com_github_airutech_gernet_test_buf_readNextWithMeta(params, make_timeout);
  return res.data;
}

bufferReadData com_github_airutech_gernet_test_buf_readNextWithMeta(bufferKernelParams *params, BOOL make_timeout) {
  bufferReadData res;
  res.data = NULL;
  if(params == NULL){
    printf("ERROR: com_github_airutech_gernet_test_buf readNextWithMeta: params is NULL\n");
    return res;
  }
  com_github_airutech_gernet_test_buf *that = (com_github_airutech_gernet_test_buf*)params->target;
  if(that == NULL){
    printf("ERROR: com_github_airutech_gernet_test_buf readNextWithMeta: Some Input parameters are wrong\n");
    return res;
  }
  /*TODO:IMPLEMENTATION GOES HERE*/
  return res;
}

int com_github_airutech_gernet_test_buf_readFinished(bufferKernelParams *params) {
  if(params == NULL){
    printf("ERROR: com_github_airutech_gernet_test_buf readFinished: params is NULL\n");
    return -1;
  }
  com_github_airutech_gernet_test_buf *that = (com_github_airutech_gernet_test_buf*)params->target;
  if(that == NULL){
    printf("ERROR: com_github_airutech_gernet_test_buf readFinished: Some Input parameters are wrong\n");
    return -1;
  }
  /*TODO:IMPLEMENTATION GOES HERE*/
  return 0;
}

void* com_github_airutech_gernet_test_buf_writeNext(bufferKernelParams *params, BOOL make_timeout) {
  if(params == NULL){
    printf("ERROR: com_github_airutech_gernet_test_buf writeNext: params is NULL\n");
    return NULL;
  }
  com_github_airutech_gernet_test_buf *that = (com_github_airutech_gernet_test_buf*)params->target;
  void* res = NULL;
  if(that == NULL){
    printf("ERROR: com_github_airutech_gernet_test_buf writeNext: Some Input parameters are wrong\n");
    return res;
  }
  /*TODO:IMPLEMENTATION GOES HERE*/
  return res;
}

int com_github_airutech_gernet_test_buf_writeFinished(bufferKernelParams *params) {
  if(params == NULL){
    printf("ERROR: com_github_airutech_gernet_test_buf writeFinished: params is NULL\n");
    return -1;
  }
  com_github_airutech_gernet_test_buf *that = (com_github_airutech_gernet_test_buf*)params->target;
  if(that == NULL){
    printf("ERROR: buf writeFinished: Some Input parameters are wrong\n");
    return -1;
  };
  /*TODO:IMPLEMENTATION GOES HERE*/
  return 0;
}

int com_github_airutech_gernet_test_buf_size(bufferKernelParams *params){
  return 0;
}

int com_github_airutech_gernet_test_buf_timeout(bufferKernelParams *params){
  return 0;
}

int com_github_airutech_gernet_test_buf_gridSize(bufferKernelParams *params){
  return 0;
}

int com_github_airutech_gernet_test_buf_uniqueId(bufferKernelParams *params){
  return 0;
}

int com_github_airutech_gernet_test_buf_addSelector(bufferKernelParams *params, void* selectorContainer) {
  return 0;
}

void com_github_airutech_gernet_test_buf_onKernels(com_github_airutech_gernet_test_buf *that){

  return;
}