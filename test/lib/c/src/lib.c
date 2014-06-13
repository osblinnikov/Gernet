/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/

#include "../include/lib.h"
void com_github_airutech_gernet_test_lib_onCreate(com_github_airutech_gernet_test_lib *that);
void com_github_airutech_gernet_test_lib_onDestroy(com_github_airutech_gernet_test_lib *that);
void com_github_airutech_gernet_test_lib_initialize(com_github_airutech_gernet_test_lib *that){
  com_github_airutech_gernet_test_lib_onCreate(that);
}

void com_github_airutech_gernet_test_lib_deinitialize(struct com_github_airutech_gernet_test_lib *that){
  com_github_airutech_gernet_test_lib_onDestroy(that);
}
/*[[[end]]] (checksum: 0e165e202c1a24d3618f200bcf80e136)*/

void com_github_airutech_gernet_test_lib_onCreate(com_github_airutech_gernet_test_lib *that){
  
  return;
}

void com_github_airutech_gernet_test_lib_onDestroy(com_github_airutech_gernet_test_lib *that){
  
  return;
}


void com_github_airutech_gernet_test_lib_onKernels(com_github_airutech_gernet_test_lib *that){
  
  return;
}