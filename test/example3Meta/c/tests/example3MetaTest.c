/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/

#include "../include/example3Meta.h"
/*[[[end]]] (checksum: a689c20380f4f98b0f53b3cb4c518146)*/
int main(int argc, char* argv[]){
  com_github_osblinnikov_gernet_test_example3Meta_create(classObj,arrayObjectNULL(),0,writerNULL(),readerNULL());
    com_github_osblinnikov_cnets_runnablesContainer runnables = classObj.getRunnables(&classObj);
    runnables.launch(&runnables,FALSE);
    runnables.stop(&runnables);
    
  return 0;
}