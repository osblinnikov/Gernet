<%import parsing_c
import gernetHelpers
h = reload(gernetHelpers)
p = reload(parsing_c)
p.parsingGernet(a)
dependencies = h.getDependenciesDict(a.read_data)
%>
  %for k,v in dependencies:
  AddDependency(env,'${h.getFullName_(v["name"])}','${h.getPath(v)}/c')
  %endfor 