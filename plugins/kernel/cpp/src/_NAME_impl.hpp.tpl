<%import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)%>
${p.importBlocks(a)}
#include "../include/${a.className}.hpp"

class ${a.className}Impl : public ${a.className}{
  ${p.getProps(a)}
  ${p.declareBlocks(a)}
  ${a.className}Impl(${p.getConstructorArgs(a)});
  ~${a.className}Impl();
  void onKernels();
  void onCreate();
  void onDestroy();
public:
  virtual void release();
  virtual void run();
  virtual void onStart();
  virtual void onStop();
  virtual com::github::airutech::cnets::runnablesContainer getRunnables();
};