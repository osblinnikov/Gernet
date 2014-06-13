<%
import sys
sys.path.insert(0, a.parserPath)

import parsing_c as p
p.parsingGernet(a)

%>
/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/
/*[[[end]]]*/
int main(int argc, char* argv[]){
  ${p.startRunnables(a)}
  return 0;
}
