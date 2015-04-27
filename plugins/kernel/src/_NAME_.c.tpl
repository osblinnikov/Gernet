<%import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)%>
#include "../${a.className}.h"
#include <stdlib.h>

void ${a.fullName_}_run(void *that);
void ${a.fullName_}_onStart(void *that);
void ${a.fullName_}_onStop(void *that);
void ${a.fullName_}_onCreate(struct ${a.fullName_} *that);
void ${a.fullName_}_onDestroy(struct ${a.fullName_} *that);
void ${a.fullName_}_onKernels(struct ${a.fullName_} *that);

struct runnablesContainer_cnets_osblinnikov_github_com ${a.fullName_}_getRunnables(struct ${a.fullName_} *that){
  return that->_runnables;
}

void ${a.fullName_}_init(${p.getArgs(a)}){
  ${p.getInit(a)}
  ${p.initializeBuffers(a)}
  ${a.fullName_}_onKernels(that);
  ${p.initializeKernels(a)}
  that->getRunnables = ${a.fullName_}_getRunnables;
  ${p.getRunnables(a)}
  ${a.fullName_}_onCreate(that);
}

void ${a.fullName_}_deinit(struct ${a.fullName_} *that){
  ${a.fullName_}_onDestroy(that);
  ${p.getDeinit(a)}
}

