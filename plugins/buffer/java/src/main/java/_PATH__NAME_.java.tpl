<%import parsing_java as p
p.parsingGernet(a)%>${p.importBlocks(a)}
${p.getContainerClass(a)}
public class ${a.className} implements readerWriterInterface{
${p.getProps(a)}  
${p.getConstructor(a)}
${p.declareBlocks(a)}
${p.getReaderWriter(a)}
  private void initialize(){
    ${p.initializeBuffers(a)}
    onKernels();
    ${p.initializeKernels(a)}
  }
  