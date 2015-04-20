<%import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)
dependenciesDict = p.getDependenciesList(a)
%>
  %for k,v  in dependenciesDict:
  AddDependency(env,'${p.artifactId(v["path"])}','${p.getPath(v["path"])}/c')
  %endfor 