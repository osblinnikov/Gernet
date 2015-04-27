<%import parsing_c
import gernetHelpers
h = reload(gernetHelpers)
p = reload(parsing_c)
p.parsingGernet(a)
dependencies = h.getDependenciesDict(a.read_data)
%>

  %for v in dependencies:
  add_dependencies(${a.fullName_+'${buildType}'} ${p.getFullName_(v["name"])+'${dstBuildType}'})
  target_link_libraries(${a.fullName_+'${buildType}'} ${p.getFullName_(v["name"])+'${dstBuildType}'})
  include_directories(${'../' * len(a.read_data["name"].split('/'))}${v["name"]})
  %endfor