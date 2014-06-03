<%import parsing_java as p
p.parsingGernet(a)%>${p.importBlocks(a)}
public class ${a.className} implements RunnableStoppable{
${p.getProps(a)}  
${p.getConstructor(a)}
${p.declareBlocks(a)}
  private void initialize(){
    ${p.initializeBuffers(a)}
    onKernels();
    ${p.initializeKernels(a)}
  }
  public runnablesContainer getRunnables(){
    ${p.getRunnables(a)}
  }