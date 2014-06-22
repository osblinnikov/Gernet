<%import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)%>
  %for v in a.read_data["blocks"]+a.read_data["depends"]:
  AddDependency(args,'${p.artifactId(v["path"])}',join(args['PROJECTS_ROOT_PATH'],'src/${p.getPath(v["path"])}/cpp'))
  %endfor 