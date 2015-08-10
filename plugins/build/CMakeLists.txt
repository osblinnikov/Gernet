<%
import parsing_c
p = reload(parsing_c)
p.parsingGernet(a)

%>
cmake_minimum_required(VERSION 2.8)
project(${a.fullName_} C CXX)

set(CMAKE_CXX_FLAGS "${'${'}CMAKE_CXX_FLAGS}")

include_directories(.)

function(addDeps buildType dstBuildType)
# [[[cog
# import cogging as c
# c.tpl(cog,templateFile,c.a(prefix=configFile,module=configModule))
# ]]]
# [[[end]]]
endfunction(addDeps)

file(GLOB ${a.fullName_.upper()}_HDRS "*.h")

set (${a.fullName_.upper()}_SRCS
    src/${a.className}.c
    )
set(${a.fullName_.upper()}_TEST
    tests/${a.className}Test.c
    )

add_custom_target(${a.fullName_})

if (NOT BUILD_STATIC_ONLY)
    add_library(${a.fullName_}_shared SHARED ${'${'+a.fullName_.upper()}_SRCS} ${'${'+a.fullName_.upper()}_HDRS})
    add_dependencies(${a.fullName_}_shared ${a.fullName_})
    target_link_libraries(${a.fullName_}_shared ${'${'}LD_FLAGS} )
    addDeps(_shared _shared)
    if(NOT WIN32)
        install(TARGETS ${a.fullName_}_shared LIBRARY DESTINATION lib)
    endif()

    add_executable(${a.fullName_}_test_shared ${'${'+a.fullName_.upper()}_TEST})
    add_dependencies(${a.fullName_}_test_shared ${a.fullName_}_shared)
    target_link_libraries(${a.fullName_}_test_shared
                          ${'${'}LD_FLAGS}
                          ${a.fullName_}_shared)
    addDeps(_test_shared _shared)
endif ()

if (BUILD_STATIC_ONLY OR BUILD_STATIC)
    add_library(${a.fullName_}_static STATIC ${'${'+a.fullName_.upper()}_HDRS} ${'${'+a.fullName_.upper()}_SRCS})
    add_dependencies(${a.fullName_}_static ${a.fullName_})
    addDeps(_static _static)
    if(NOT WIN32)
        install(TARGETS ${a.fullName_}_static ARCHIVE DESTINATION lib)
    endif()

    add_executable(${a.fullName_}_test_static ${'${'+a.fullName_.upper()}_TEST})
    add_dependencies(${a.fullName_}_test_static ${a.fullName_}_static)
    target_link_libraries(${a.fullName_}_test_static
                            ${'${'}LD_FLAGS}
                            ${a.fullName_}_static)
    addDeps(_test_static _static)
endif ()



link_directories(${'${'}LD_DIRS})
include_directories(. ${'${'}INCLUDE_DIRS})



