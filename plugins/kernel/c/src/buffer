<%
import sys
sys.path.insert(0, a.parserPath)

import parsing_c as p
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

void* ${a.fullName_}_readNext(bufferKernelParams *params, BOOL make_timeout) {
  bufferReadData res = ${a.fullName_}_readNextWithMeta(params, make_timeout);
  return res.data;
}

bufferReadData ${a.fullName_}_readNextWithMeta(bufferKernelParams *params, BOOL make_timeout) {
  bufferReadData res;
  res.data = NULL;
  if(params == NULL){
    printf("ERROR: ${a.fullName_} readNextWithMeta: params is NULL\n");
    return res;
  }
  ${a.fullName_} *that = (${a.fullName_}*)params->target;
  if(that == NULL){
    printf("ERROR: ${a.fullName_} readNextWithMeta: Some Input parameters are wrong\n");
    return res;
  }
  /*TODO:IMPLEMENTATION GOES HERE*/
  return res;
}

int ${a.fullName_}_readFinished(bufferKernelParams *params) {
  if(params == NULL){
    printf("ERROR: ${a.fullName_} readFinished: params is NULL\n");
    return -1;
  }
  ${a.fullName_} *that = (${a.fullName_}*)params->target;
  if(that == NULL){
    printf("ERROR: ${a.fullName_} readFinished: Some Input parameters are wrong\n");
    return -1;
  }
  /*TODO:IMPLEMENTATION GOES HERE*/
  return 0;
}

void* ${a.fullName_}_writeNext(bufferKernelParams *params, BOOL make_timeout) {
  if(params == NULL){
    printf("ERROR: ${a.fullName_} writeNext: params is NULL\n");
    return NULL;
  }
  ${a.fullName_} *that = (${a.fullName_}*)params->target;
  void* res = NULL;
  if(that == NULL){
    printf("ERROR: ${a.fullName_} writeNext: Some Input parameters are wrong\n");
    return res;
  }
  /*TODO:IMPLEMENTATION GOES HERE*/
  return res;
}

int ${a.fullName_}_writeFinished(bufferKernelParams *params) {
  if(params == NULL){
    printf("ERROR: ${a.fullName_} writeFinished: params is NULL\n");
    return -1;
  }
  ${a.fullName_} *that = (${a.fullName_}*)params->target;
  if(that == NULL){
    printf("ERROR: ${a.className} writeFinished: Some Input parameters are wrong\n");
    return -1;
  };
  /*TODO:IMPLEMENTATION GOES HERE*/
  return 0;
}

int ${a.fullName_}_size(bufferKernelParams *params){
  return 0;
}

int ${a.fullName_}_timeout(bufferKernelParams *params){
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

void ${a.fullName_}_onKernels(${a.fullName_} *that){

  return;
}