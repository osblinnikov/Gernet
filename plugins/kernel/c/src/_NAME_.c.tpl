<%import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)%>
#include "../include/${a.className}.h"

com_github_osblinnikov_cnets_runnablesContainer ${a.fullName_}_getRunnables(${a.fullName_} *that);
void ${a.fullName_}_run(void *that);
void ${a.fullName_}_onStart(void *that);
void ${a.fullName_}_onStop(void *that);

void ${a.fullName_}_onCreate(${a.fullName_} *that);
void ${a.fullName_}_onDestroy(${a.fullName_} *that);

void ${a.fullName_}_initialize(${a.fullName_} *that){
  that->getRunnables = ${a.fullName_}_getRunnables;
  that->run = ${a.fullName_}_run;
  ${a.fullName_}_onCreate(that);
}

void ${a.fullName_}_deinitialize(struct ${a.fullName_} *that){
  ${a.fullName_}_onDestroy(that);
}

com_github_osblinnikov_cnets_runnablesContainer ${a.fullName_}_getRunnables(${a.fullName_} *that){
  ${p.getRunnables(a)}
}