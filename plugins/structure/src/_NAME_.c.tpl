<%import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)%>
#include "../${a.className}.h"
void ${a.fullName_}_onCreate(${a.fullName_} *that);
void ${a.fullName_}_onDestroy(${a.fullName_} *that);
void ${a.fullName_}_init(${p.getArgs(a)}){
  ${p.getInit(a)}
  ${a.fullName_}_onCreate(that);
}

void ${a.fullName_}_deinit(struct ${a.fullName_} *that){
  ${a.fullName_}_onDestroy(that);
}