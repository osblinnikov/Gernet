
package com.github.airutech.gernet.test.buf;

/*[[[cog
import cogging as c
c.tpl(cog,templateFile,c.a(prefix=configFile))
]]]*/

import com.github.airutech.cnets.types.*;
import com.github.airutech.cnets.readerWriter.*;
import com.github.airutech.cnets.queue.*;

public class buf implements readerWriterInterface{
  Object[] buffers;long timeout_milisec;String uniqueId;int readers_grid_size;int statsInterval;
  
  public buf(Object[] buffers,long timeout_milisec,String uniqueId,int readers_grid_size,int statsInterval){
    this.buffers = buffers;
    this.timeout_milisec = timeout_milisec;
    this.uniqueId = uniqueId;
    this.readers_grid_size = readers_grid_size;
    this.statsInterval = statsInterval;
    onCreate();
    initialize();
  }


public reader getReader(long grid_id){
  Object container = null;
  return new reader(new bufferKernelParams(this, grid_id, container));
}
public writer getWriter(long grid_id){
  Object container = null;
  return new writer(new bufferKernelParams(this, grid_id, container));
}
  private void initialize(){
    
    onKernels();
    
  }
  
/*[[[end]]] (checksum: 6b334e8a97c08853569e08a72f3ed27e)*/

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
    buf m = (buf)params.getTarget();
    bufferReadData res = new bufferReadData();
    if(m==null){
      System.err.print("ERROR: buf readNextWithMeta: Some Input parameters are wrong");
      return res;
    }
    /*TODO:IMPLEMENTATION GOES HERE*/
    return res;
  }

  @Override
  public int readFinished(bufferKernelParams params) {
    if(this != params.getTarget()){return -1;}
    buf m = (buf)params.getTarget();
    if(m==null){
      System.err.print("ERROR: buf readFinished: Some Input parameters are wrong");
      return -1;
    }
    /*TODO:IMPLEMENTATION GOES HERE*/
    return 0;
  }

  @Override
  public Object writeNext(bufferKernelParams params, int waitThreshold) {
    if(this != params.getTarget()){return null;}
    buf m = (buf)params.getTarget();
    Object res = null;
    if(m==null){
      System.err.print("ERROR: buf writeNext: Some Input parameters are wrong");
      return res;
    }
    /*TODO:IMPLEMENTATION GOES HERE*/
    return res;
  }

  @Override
  public int writeFinished(bufferKernelParams params) {
    if(this != params.getTarget()){return -1;}
    buf m = (buf)params.getTarget();
    if(m==null){
      System.err.print("ERROR: buf writeFinished: Some Input parameters are wrong");
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
  public String uniqueId(bufferKernelParams params){
    return "";
  }

  @Override
  public long getStatsInterval(bufferKernelParams buffer) {
    return 0;
  }

  @Override
  public int addSelector(bufferKernelParams params, Object selectorContainer) {
    return 0;
  }
}

