<%import parsing_java
p = reload(parsing_java)
p.parsingGernet(a)%>${p.importBlocks(a)}
public class ${a.className}{
${p.getProps(a)}  
${p.getConstructor(a)}
${p.declareBlocks(a)}
  private void initialize(){
    ${p.initializeBuffers(a)}
    onKernels();
    ${p.initializeKernels(a)}
  }