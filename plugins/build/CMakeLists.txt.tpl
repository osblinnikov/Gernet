<%import parsing_c
import gernetHelpers
h = reload(gernetHelpers)
p = reload(parsing_c)
p.parsingGernet(a)
dependencies = h.getDependenciesDict(a.read_data)
%>
  include_directories(${'../' * len(a.read_data["name"].split('/'))})
  %for v in dependencies:
  add_dependencies(${a.fullName_+'${buildType}'} ${p.getFullName_(v["name"])+'${dstBuildType}'})
  target_link_libraries(${a.fullName_+'${buildType}'} ${p.getFullName_(v["name"])+'${dstBuildType}'})
  %endfor

# install includes
install(DIRECTORY . DESTINATION include/${a.read_data["name"]} FILES_MATCHING PATTERN "*.h" PATTERN "tests" EXCLUDE PATTERN "src" EXCLUDE PATTERN "Release" EXCLUDE  PATTERN "Debug" EXCLUDE PATTERN ".s*" EXCLUDE )
install(DIRECTORY . DESTINATION include/${a.read_data["name"]} FILES_MATCHING PATTERN "*.hpp" PATTERN "tests" EXCLUDE PATTERN "src" EXCLUDE PATTERN "Release" EXCLUDE  PATTERN "Debug" EXCLUDE PATTERN ".s*" EXCLUDE )
