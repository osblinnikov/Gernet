<%import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)
dependenciesDict = p.getDependenciesList(a)
%>
  %for k,v  in dependenciesDict:
  AddDependency(args,'${p.artifactId(v["path"])}',join(args['PROJECTS_ROOT_PATH'],'src/${p.getPath(v["path"])}/c'))
  %endfor 