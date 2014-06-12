<%import parsing_java as p
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