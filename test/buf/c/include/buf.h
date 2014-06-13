

#ifndef com_github_airutech_gernet_test_buf_H
#define com_github_airutech_gernet_test_buf_H

/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/

#include "github.com/airutech/cnets/types/c/include/types.h"
#include "github.com/airutech/cnets/readerWriter/c/include/readerWriter.h"
#include "github.com/airutech/cnets/queue/c/include/queue.h"

#undef com_github_airutech_gernet_test_buf_EXPORT_API
#if defined WIN32 && !defined __MINGW32__ && !defined(CYGWIN) && !defined(com_github_airutech_gernet_test_buf_STATIC)
  #ifdef com_github_airutech_gernet_test_buf_EXPORT
    #define com_github_airutech_gernet_test_buf_EXPORT_API __declspec(dllexport)
  #else
    #define com_github_airutech_gernet_test_buf_EXPORT_API __declspec(dllimport)
  #endif
#else
  #define com_github_airutech_gernet_test_buf_EXPORT_API extern
#endif

struct com_github_airutech_gernet_test_buf;

com_github_airutech_gernet_test_buf_EXPORT_API
reader com_github_airutech_gernet_test_buf_getReader(struct com_github_airutech_gernet_test_buf *that, void* container, int grid_id);

com_github_airutech_gernet_test_buf_EXPORT_API
writer com_github_airutech_gernet_test_buf_getWriter(struct com_github_airutech_gernet_test_buf *that, void* container, int grid_id);

com_github_airutech_gernet_test_buf_EXPORT_API
void com_github_airutech_gernet_test_buf_initialize(struct com_github_airutech_gernet_test_buf *that);

com_github_airutech_gernet_test_buf_EXPORT_API
void com_github_airutech_gernet_test_buf_deinitialize(struct com_github_airutech_gernet_test_buf *that);

com_github_airutech_gernet_test_buf_EXPORT_API
void com_github_airutech_gernet_test_buf_onKernels(struct com_github_airutech_gernet_test_buf *that);

#undef com_github_airutech_gernet_test_buf_onCreateMacro
#define com_github_airutech_gernet_test_buf_onCreateMacro(_NAME_) /**/


#define com_github_airutech_gernet_test_buf_createReader(_NAME_,_that,_grid_id)\
  reader _NAME_ = com_github_airutech_gernet_test_buf_getReader(_that,NULL,_grid_id);

#define com_github_airutech_gernet_test_buf_createWriter(_NAME_,_that,_grid_id)\
  writer _NAME_ = com_github_airutech_gernet_test_buf_getWriter(_that,NULL,_grid_id);

#define com_github_airutech_gernet_test_buf_create(_NAME_,_buffers,_timeout_milisec,_uniqueId,_readers_grid_size,_statsInterval)\
    com_github_airutech_gernet_test_buf _NAME_;\
    _NAME_.buffers = _buffers;\
    _NAME_.timeout_milisec = _timeout_milisec;\
    _NAME_.uniqueId = _uniqueId;\
    _NAME_.readers_grid_size = _readers_grid_size;\
    _NAME_.statsInterval = _statsInterval;\
    com_github_airutech_gernet_test_buf_onCreateMacro(_NAME_)\
    com_github_airutech_gernet_test_buf_initialize(&_NAME_);\
    com_github_airutech_gernet_test_buf_onKernels(&_NAME_);

typedef struct com_github_airutech_gernet_test_buf{
    arrayObject buffers;long timeout_milisec;char* uniqueId;int readers_grid_size;int statsInterval;

  
/*[[[end]]] (checksum: bab87c389f6c7e632ba0c8880eda26c5)*/

}com_github_airutech_gernet_test_buf;

#undef com_github_airutech_gernet_test_buf_onCreateMacro
#define com_github_airutech_gernet_test_buf_onCreateMacro(_NAME_) /**/

#endif /* com_github_airutech_gernet_test_buf_H */