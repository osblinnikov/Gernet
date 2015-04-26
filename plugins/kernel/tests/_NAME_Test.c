<%import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)%>/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/
/*[[[end]]]*/
int main(int argc, char* argv[]){
  ${p.testRunnables(a)}
  return 0;
}