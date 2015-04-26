<%import parsing_java
p = reload(parsing_java)
p.parsingGernet(a)

fieldsArray = p.getFieldsArrStr(a)

%>${p.importBlocks(a)}
public class ${a.className}{
${"  public "+'; public '.join(fieldsArray)+';' if len(fieldsArray)>0 else ''}
${p.getConstructor(a)}
${p.declareBlocks(a)}
  private void initialize(){
    ${p.initializeBuffers(a)}
    onKernels();
    ${p.initializeKernels(a)}
  }