<%
import sys
sys.path.insert(0, a.parserPath)

import parsing_java
p = reload(parsing_java)
p.parsingGernet(a)

%>
package ${a.package};

/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile,module=configModule))
]]]*/
/*[[[end]]]*/

  private void onCreate(){

  }

  private void onKernels(){

  }

  @Override
  public Object readNext(bufferKernelParams params, int waitThreshold) {
    return readNextWithMeta(params, waitThreshold).getData();
  }

  @Override
  public bufferReadData readNextWithMeta(bufferKernelParams params, int waitThreshold) {
    if(this != params.getTarget()){return null;}
    ${a.className} m = (${a.className})params.getTarget();
    bufferReadData res = new bufferReadData();
    if(m==null){
      System.err.print("ERROR: ${a.className} readNextWithMeta: Some Input parameters are wrong");
      return res;
    }
    /*TODO:IMPLEMENTATION GOES HERE*/
    return res;
  }

  @Override
  public int readFinished(bufferKernelParams params) {
    if(this != params.getTarget()){return -1;}
    ${a.className} m = (${a.className})params.getTarget();
    if(m==null){
      System.err.print("ERROR: ${a.className} readFinished: Some Input parameters are wrong");
      return -1;
    }
    /*TODO:IMPLEMENTATION GOES HERE*/
    return 0;
  }

  @Override
  public Object writeNext(bufferKernelParams params, int waitThreshold) {
    if(this != params.getTarget()){return null;}
    ${a.className} m = (${a.className})params.getTarget();
    Object res = null;
    if(m==null){
      System.err.print("ERROR: ${a.className} writeNext: Some Input parameters are wrong");
      return res;
    }
    /*TODO:IMPLEMENTATION GOES HERE*/
    return res;
  }

  @Override
  public int writeFinished(bufferKernelParams params) {
    if(this != params.getTarget()){return -1;}
    ${a.className} m = (${a.className})params.getTarget();
    if(m==null){
      System.err.print("ERROR: ${a.className} writeFinished: Some Input parameters are wrong");
      return -1;
    };
    /*TODO:IMPLEMENTATION GOES HERE*/
    return 0;
  }

  @Override
  public int size(bufferKernelParams params){
    return 0;
  }

  @Override
  public int timeout(bufferKernelParams params){
    return 0;
  }

  @Override
  public int gridSize(bufferKernelParams params){
    return 0;
  }

  @Override
  public int uniqueId(bufferKernelParams params){
    return -1;
  }

  @Override
  public int addSelector(bufferKernelParams params, Object selectorContainer) {
    return 0;
  }
}

