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

reader ${a.fullName_}_createReader(${a.fullName_} *that, int gridId){
  bufferKernelParams_create(params, that, gridId, NULL,${a.fullName_}_)
  reader_create(res,params)
  return res;
}

writer ${a.fullName_}_createWriter(${a.fullName_} *that, int gridId){
  bufferKernelParams_create(params, that, gridId, NULL,${a.fullName_}_)
  writer_create(res,params)
  return res;
}

void ${a.fullName_}_init(${p.getArgs(a)}){
  ${p.getInit(a)}
  ${a.fullName_}_onCreate(that);
}
}

void ${a.fullName_}_deinit(struct ${a.fullName_} *that){
  ${a.fullName_}_onDestroy(that);
  ${p.getDeinit(a)}
}