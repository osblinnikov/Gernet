

#ifndef com_github_airutech_gernet_test_lib_H
#define com_github_airutech_gernet_test_lib_H

/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/

#include "github.com/airutech/cnets/runnablesContainer/c/include/runnablesContainer.h"
#include "github.com/airutech/cnets/readerWriter/c/include/readerWriter.h"
#include "github.com/airutech/cnets/types/c/include/types.h"

#undef com_github_airutech_gernet_test_lib_EXPORT_API
#if defined WIN32 && !defined __MINGW32__ && !defined(CYGWIN) && !defined(com_github_airutech_gernet_test_lib_STATIC)
  #ifdef com_github_airutech_gernet_test_lib_EXPORT
    #define com_github_airutech_gernet_test_lib_EXPORT_API __declspec(dllexport)
  #else
    #define com_github_airutech_gernet_test_lib_EXPORT_API __declspec(dllimport)
  #endif
#else
  #define com_github_airutech_gernet_test_lib_EXPORT_API extern
#endif

struct com_github_airutech_gernet_test_lib;

com_github_airutech_gernet_test_lib_EXPORT_API
void com_github_airutech_gernet_test_lib_initialize(struct com_github_airutech_gernet_test_lib *that);

com_github_airutech_gernet_test_lib_EXPORT_API
void com_github_airutech_gernet_test_lib_deinitialize(struct com_github_airutech_gernet_test_lib *that);

com_github_airutech_gernet_test_lib_EXPORT_API
void com_github_airutech_gernet_test_lib_onKernels(struct com_github_airutech_gernet_test_lib *that);

com_github_airutech_gernet_test_lib_EXPORT_API
com_github_airutech_cnets_runnablesContainer com_github_airutech_gernet_test_lib_getRunnables(struct com_github_airutech_gernet_test_lib *that);

#undef com_github_airutech_gernet_test_lib_onCreateMacro
#define com_github_airutech_gernet_test_lib_onCreateMacro(_NAME_) /**/

#define com_github_airutech_gernet_test_lib_create(_NAME_)\
    com_github_airutech_gernet_test_lib _NAME_;\
    com_github_airutech_gernet_test_lib_onCreateMacro(_NAME_)\
    com_github_airutech_gernet_test_lib_initialize(&_NAME_);\
    com_github_airutech_gernet_test_lib_onKernels(&_NAME_);

typedef struct com_github_airutech_gernet_test_lib{
  
  
  com_github_airutech_cnets_runnablesContainer (*getRunnables)(struct com_github_airutech_gernet_test_lib *that);
  void (*run)(void *that);
/*[[[end]]] (checksum: 169466efcb9f20efc603cc4911215bbd)*/

}com_github_airutech_gernet_test_lib;

#undef com_github_airutech_gernet_test_lib_onCreateMacro
#define com_github_airutech_gernet_test_lib_onCreateMacro(_NAME_) /**/

#endif /* com_github_airutech_gernet_test_lib_H */