<%import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)%>/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/
/*[[[end]]]*/

void ${a.fullName_}_run(void *t){
  /*struct ${a.fullName_} *that = (struct ${a.fullName_}*)t;*/
}

void ${a.fullName_}_onStart(void *t){
  /*struct ${a.fullName_} *that = (struct ${a.fullName_}*)t;*/
}

void ${a.fullName_}_onStop(void *t){
  /*struct ${a.fullName_} *that = (struct ${a.fullName_}*)t;*/
}

void ${a.fullName_}_onCreate(struct ${a.fullName_} *that){
  
  return;
}

void ${a.fullName_}_onDestroy(struct ${a.fullName_} *that){
  
  return;
}

void ${a.fullName_}_onKernels(struct ${a.fullName_} *that){
  
  return;
}
