<%import parsing_c as p
p.parsingGernet(a)%>
#include "../include/${a.className}.h"

void* ${a.fullName_}_readNext(bufferKernelParams *params, BOOL make_timeout);
bufferReadData ${a.fullName_}_readNextWithMeta(bufferKernelParams *params, BOOL make_timeout);
int ${a.fullName_}_readFinished(bufferKernelParams *params);
void* ${a.fullName_}_writeNext(bufferKernelParams *params, BOOL make_timeout);
int ${a.fullName_}_writeFinished(bufferKernelParams *params);
int ${a.fullName_}_size(bufferKernelParams *params);
int ${a.fullName_}_timeout(bufferKernelParams *params);
int ${a.fullName_}_gridSize(bufferKernelParams *params);
int ${a.fullName_}_uniqueId(bufferKernelParams *params);
int ${a.fullName_}_addSelector(bufferKernelParams *params, void* selectorContainer);
void ${a.fullName_}_onCreate(${a.fullName_} *that);
void ${a.fullName_}_onDestroy(${a.fullName_} *that);

reader ${a.fullName_}_getReader(${a.fullName_} *that, void* container, int grid_id){
  bufferKernelParams_create(params, that, grid_id, container,${a.fullName_}_)
  reader_create(res,params)
  return res;
}

writer ${a.fullName_}_getWriter(${a.fullName_} *that, void* container, int grid_id){
  bufferKernelParams_create(params, that, grid_id, container,${a.fullName_}_)
  writer_create(res,params)
  return res;
}

void ${a.fullName_}_initialize(${a.fullName_} *that){
  ${a.fullName_}_onCreate(that);
}

void ${a.fullName_}_deinitialize(struct ${a.fullName_} *that){
  ${a.fullName_}_onDestroy(that);
}