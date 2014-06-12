<%import parsing_c as p
p.parsingGernet(a)%>
  %for v in a.read_data["blocks"]+a.read_data["depends"]:
  AddDependency(args,'${p.artifactId(v["path"])}',join(args['PROJECTS_ROOT_PATH'],'src/${p.getPath(v["path"])}/c'))
  %endfor