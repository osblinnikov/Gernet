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

void ${a.fullNameSpace}::${a.className}Impl::run(){
${p.runBlocks(a)}
}

void ${a.fullNameSpace}::${a.className}Impl::onStart(){
}

void ${a.fullNameSpace}::${a.className}Impl::onStop(){
}


void ${a.fullNameSpace}::${a.className}Impl::onCreate(){
  
  return;
}

void ${a.fullNameSpace}::${a.className}Impl::onDestroy(){
  
  return;
}


void ${a.fullNameSpace}::${a.className}Impl::onKernels(){
  
  return;
}