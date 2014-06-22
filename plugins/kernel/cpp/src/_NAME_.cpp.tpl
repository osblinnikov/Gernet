<%import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)%>

#include "./${a.className}Impl.hpp"

${a.className}* ${a.fullNameSpace}::${a.className}::create(${p.getConstructorArgs(a)}){
  return new ${a.fullNameSpace}::${a.className}Impl(${p.passConstructorArgs(a)});
}

${a.fullNameSpace}::${a.className}Impl::${a.className}Impl(${p.getConstructorArgs(a)}){
  onCreate();
  ${p.initializeBuffers(a)}
  onKernels();
  ${p.initializeKernels(a)}
}

${a.fullNameSpace}::${a.className}Impl::~${a.className}Impl(){
  onDestroy();
}

com::github::airutech::cnets::runnablesContainer ${a.fullNameSpace}::${a.className}Impl::getRunnables(){
  ${p.getRunnables(a)}
}