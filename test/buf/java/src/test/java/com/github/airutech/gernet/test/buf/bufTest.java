
package com.github.airutech.gernet.test.buf;
import org.junit.Test;
/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/


import com.github.airutech.cnets.types.*;
import com.github.airutech.cnets.readerWriter.*;
import com.github.airutech.cnets.queue.*;
/*[[[end]]] (checksum: 5c761cd1f560a00b1621957ac6ea0ca6)*/
public class bufTest {
  @Test
  public void bufTest(){
    buf classObj = new buf(new Object[1],0,null,0,0);
  }
}
