<%
import sys
sys.path.insert(0, a.parserPath)

import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)

%>/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/
/*[[[end]]]*/

void ${a.fullName_}_onCreate(${a.fullName_} *that){
  
  return;
}

void ${a.fullName_}_onDestroy(${a.fullName_} *that){
  
  return;
}

void* ${a.fullName_}_readNext(bufferKernelParams *params, int waitTimeout) {
  bufferReadData res = ${a.fullName_}_readNextWithMeta(params, waitTimeout);
  return res.data;
}

bufferReadData ${a.fullName_}_readNextWithMeta(bufferKernelParams *params, int waitTimeout) {
  bufferReadData res;
  res.data = NULL;
  if(params == NULL){
    fprintf(stderr,"ERROR: ${a.fullName_} readNextWithMeta: params is NULL\n");
    return res;
  }
  ${a.fullName_} *that = (${a.fullName_}*)params->target;
  if(that == NULL){
    fprintf(stderr,"ERROR: ${a.fullName_} readNextWithMeta: Some Input parameters are wrong\n");
    return res;
  }
  /*TODO:IMPLEMENTATION GOES HERE*/
  return res;
}

int ${a.fullName_}_readFinished(bufferKernelParams *params) {
  if(params == NULL){
    fprintf(stderr,"ERROR: ${a.fullName_} readFinished: params is NULL\n");
    return -1;
  }
  ${a.fullName_} *that = (${a.fullName_}*)params->target;
  if(that == NULL){
    fprintf(stderr,"ERROR: ${a.fullName_} readFinished: Some Input parameters are wrong\n");
    return -1;
  }
  /*TODO:IMPLEMENTATION GOES HERE*/
  return 0;
}

void* ${a.fullName_}_writeNext(bufferKernelParams *params, int waitTimeout) {
  if(params == NULL){
    fprintf(stderr,"ERROR: ${a.fullName_} writeNext: params is NULL\n");
    return NULL;
  }
  ${a.fullName_} *that = (${a.fullName_}*)params->target;
  void* res = NULL;
  if(that == NULL){
    fprintf(stderr,"ERROR: ${a.fullName_} writeNext: Some Input parameters are wrong\n");
    return res;
  }
  /*TODO:IMPLEMENTATION GOES HERE*/
  return res;
}

int ${a.fullName_}_writeFinished(bufferKernelParams *params) {
  bufferWriteData writeData;
  writeData.grid_ids = 0;
  return ${a.fullName_}_writeFinishedWithMeta(params, writeData);
}

int ${a.fullName_}_writeFinishedWithMeta(bufferKernelParams *params, bufferWriteData writeData){
  if(params == NULL){
    fprintf(stderr,"ERROR: ${a.fullName_}_writeFinishedWithMeta: params is NULL\n");
    return -1;
  }
  ${a.fullName_} *that = (${a.fullName_}*)params->target;
  if(that == NULL){
    fprintf(stderr,"ERROR: ${a.fullName_}_writeFinishedWithMeta: Some Input parameters are wrong\n");
    return -1;
  };
  /*TODO:IMPLEMENTATION GOES HERE*/
  return 0;
}

int ${a.fullName_}_size(bufferKernelParams *params){
  return 0;
}

int64_t ${a.fullName_}_timeout(bufferKernelParams *params){
  return 0;
}

int ${a.fullName_}_gridSize(bufferKernelParams *params){
  return 0;
}

int ${a.fullName_}_uniqueId(bufferKernelParams *params){
  return 0;
}

int ${a.fullName_}_addSelector(bufferKernelParams *params, void* selectorContainer) {
  return 0;
}


void ${a.fullName_}_enable(bufferKernelParams *params, short isEnabled){
  if(params == NULL){
    fprintf(stderr,"ERROR: ${a.fullName_} enable: params is NULL\n");
    return;
  }
  ${a.fullName_} *that = (${a.fullName_}*)params->target;
  if(that == NULL){
    fprintf(stderr,"ERROR: ${a.fullName_} enable: Some Input parameters are wrong\n");
    return;
  };
  /*IMPLEMENT HERE*/
}
