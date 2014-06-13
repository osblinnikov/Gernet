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

void ${a.fullName_}_run(void *t){
${p.runBlocks(a)}
}

void ${a.fullName_}_onStart(void *t){
  /*${a.fullName_} *that = (${a.fullName_}*)t;*/
}

void ${a.fullName_}_onStop(void *that){
  /*${a.fullName_} *that = (${a.fullName_}*)t;*/
}


void ${a.fullName_}_onCreate(${a.fullName_} *that){
  
  return;
}

void ${a.fullName_}_onDestroy(${a.fullName_} *that){
  
  return;
}


void ${a.fullName_}_onKernels(${a.fullName_} *that){
  
  return;
}