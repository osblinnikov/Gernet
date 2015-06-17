<%import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)%>
#include "../${a.className}.h"

void* ${a.fullName_}_readNext(bufferKernelParams *params, int waitThreshold);
bufferReadData ${a.fullName_}_readNextWithMeta(bufferKernelParams *params, int waitThreshold);
int ${a.fullName_}_readFinished(bufferKernelParams *params);
void* ${a.fullName_}_writeNext(bufferKernelParams *params, int waitThreshold);
int ${a.fullName_}_writeFinished(bufferKernelParams *params);
int ${a.fullName_}_size(bufferKernelParams *params);
int64_t ${a.fullName_}_timeout(bufferKernelParams *params);
int ${a.fullName_}_gridSize(bufferKernelParams *params);
int ${a.fullName_}_uniqueId(bufferKernelParams *params);
int ${a.fullName_}_addSelector(bufferKernelParams *params, void* selectorContainer);
void ${a.fullName_}_onCreate(${a.fullName_} *that);
void ${a.fullName_}_onDestroy(${a.fullName_} *that);
void ${a.fullName_}_setKernelIds(bufferKernelParams *params, short isReader, void* ids, void (*idsDestructor)(void*));
void* ${a.fullName_}_getKernelIds(bufferKernelParams *params, short isReader);

reader ${a.fullName_}_createReader(${a.fullName_} *that, int gridId){
  bufferKernelParams_create(params, that, gridId, ${a.fullName_}_)
  reader_create(res,params)
  return res;
}

writer ${a.fullName_}_createWriter(${a.fullName_} *that, int gridId){
  bufferKernelParams_create(params, that, gridId, ${a.fullName_}_)
  writer_create(res,params)
  return res;
}

void ${a.fullName_}_init(${p.getArgs(a)}){
  that->_readerIds_ = 0;
  that->_writerIds_ = 0;
  ${p.getInit(a)}
  ${a.fullName_}_onCreate(that);
}

void ${a.fullName_}_deinit(struct ${a.fullName_} *that){
  ${a.fullName_}_onDestroy(that);
  ${p.getDeinit(a)}
  if(that->_readerIds_ && that->readerIdsDestructor){
    that->readerIdsDestructor(that->_readerIds_);
    that->_readerIds_ = 0;
  }
  if(that->_writerIds_ && that->writerIdsDestructor){
    that->writerIdsDestructor(that->_writerIds_);
    that->_writerIds_ = 0;
  }
}


void ${a.fullName_}_setKernelIds(bufferKernelParams *params, short isReader, void* ids, void (*idsDestructor)(void*)) {
  if(params == NULL){
    fprintf(stderr,"ERROR: ${a.fullName_} setKernelIds: params is NULL\n");
    return;
  }
  ${a.fullName_} *that = (${a.fullName_}*)params->target;
  if(that == NULL){
    fprintf(stderr,"ERROR: ${a.fullName_} setKernelIds: Some Input parameters are wrong\n");
    return;
  };
  if(isReader){
    that->_readerIds_ = ids;
    that->readerIdsDestructor = idsDestructor;
  }else{
    that->_writerIds_ = ids;
    that->writerIdsDestructor = idsDestructor;
  }
}

void* ${a.fullName_}_getKernelIds(bufferKernelParams *params, short isReader) {
  if(params == NULL){
    fprintf(stderr,"ERROR: ${a.fullName_} setKernelIds: params is NULL\n");
    return 0;
  }
  ${a.fullName_} *that = (${a.fullName_}*)params->target;
  if(that == NULL){
    fprintf(stderr,"ERROR: ${a.fullName_} setKernelIds: Some Input parameters are wrong\n");
    return 0;
  };
  if(isReader){
    return that->_readerIds_;
  }else{
    return that->_writerIds_;
  }
}
