<%
import sys
sys.path.insert(0, a.parserPath)

import parsing_java as p
p.parsingGernet(a)

%>
package ${a.read_data["path"]};
import org.junit.Test;
/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/
/*[[[end]]]*/
public class ${a.className}Test {
  @Test
  public void ${a.className}Test(){
    ${p.testRunnables(a)}
  }
}

