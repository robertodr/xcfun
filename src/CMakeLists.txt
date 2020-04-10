add_library(xcfun-objlib
  OBJECT
    XCFunctional.cpp
    xcint.cpp
  )

set_property(GLOBAL APPEND
  PROPERTY public_headers_property
    ${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME}/XCFunExport.h
    ${CMAKE_CURRENT_SOURCE_DIR}/config.hpp
    ${CMAKE_CURRENT_SOURCE_DIR}/densvars.hpp
    ${CMAKE_CURRENT_SOURCE_DIR}/functional.hpp
    ${CMAKE_CURRENT_SOURCE_DIR}/specmath.hpp
    ${CMAKE_CURRENT_SOURCE_DIR}/xcint.hpp
    ${CMAKE_CURRENT_SOURCE_DIR}/XCFunctional.hpp
  )
add_subdirectory(functionals)

include(GenerateExportHeader)
generate_export_header(xcfun-objlib
  BASE_NAME "XCFun"
  EXPORT_MACRO_NAME "xcfun_EXPORTS"
  EXPORT_FILE_NAME "${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME}/XCFunExport.h"
  DEPRECATED_MACRO_NAME "xcfun_DEPRECATED"
  NO_EXPORT_MACRO_NAME "xcfun_NO_EXPORTS"
  STATIC_DEFINE "xcfun_STATIC_DEFINE"
  NO_DEPRECATED_MACRO_NAME "xcfun_NO_DEPRECATED"
  DEFINE_NO_DEPRECATED
  )

target_compile_options(xcfun-objlib
  PRIVATE
    "${XCFun_CXX_FLAGS}"
    "$<$<CONFIG:Debug>:${XCFun_CXX_FLAGS_DEBUG}>"
    "$<$<CONFIG:Release>:${XCFun_CXX_FLAGS_RELEASE}>"
    "$<$<BOOL:${ENABLE_CODE_COVERAGE}>:${XCFun_CXX_FLAGS_COVERAGE}>"
  )

target_compile_definitions(xcfun-objlib
  PUBLIC
    XCFUN_MAX_ORDER=${XCFUN_MAX_ORDER}
    xcfun_objlib_EXPORTS
  )

target_include_directories(xcfun-objlib
  PRIVATE
    ${PROJECT_SOURCE_DIR}/api
    ${PROJECT_BINARY_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}
  )

target_include_directories(xcfun-objlib
  SYSTEM
  PRIVATE
    ${PROJECT_SOURCE_DIR}/external/upstream/taylor
  )

get_property(public_headers GLOBAL PROPERTY public_headers_property)

set_target_properties(xcfun-objlib
  PROPERTIES
    POSITION_INDEPENDENT_CODE 1
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN 1
  )

add_library(xcfun $<TARGET_OBJECTS:xcfun-objlib>)

target_compile_definitions(xcfun-objlib
  INTERFACE
    $<INSTALL_INTERFACE:USING_XCFun>
  )

target_include_directories(xcfun
  INTERFACE
    $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_INCLUDEDIR}>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
  )

set_target_properties(xcfun
  PROPERTIES
    VERSION ${PROJECT_VERSION_MAJOR}
    SOVERSION ${PROJECT_VERSION_MAJOR}
    MACOSX_RPATH ON
    OUTPUT_NAME "xcfun"
    DEBUG_POSTFIX "_d"
    PUBLIC_HEADER "${public_headers}"
  )

target_link_libraries(xcfun
  PUBLIC
    "$<$<BOOL:${ENABLE_CODE_COVERAGE}>:gcov>"
  )

install(
  TARGETS
    xcfun
  EXPORT
    "XCFunTargets"
  ARCHIVE
    DESTINATION ${CMAKE_INSTALL_LIBDIR}
    COMPONENT lib
  RUNTIME
    DESTINATION ${CMAKE_INSTALL_BINDIR}
    COMPONENT bin
  LIBRARY
    DESTINATION ${CMAKE_INSTALL_LIBDIR}
    COMPONENT lib
  PUBLIC_HEADER
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/XCFun
    COMPONENT dev
  )

# The alias is useful with FetchContent
add_library(XCFun::xcfun ALIAS xcfun)

# <<<  Export Config  >>>
include(CMakePackageConfigHelpers)

write_basic_package_version_file(
  ${PROJECT_BINARY_DIR}/${CMAKECONFIG_INSTALL_DIR}/XCFunConfigVersion.cmake
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY SameMajorVersion
  )

configure_package_config_file(
  ${PROJECT_SOURCE_DIR}/cmake/XCFunConfig.cmake.in
  ${PROJECT_BINARY_DIR}/${CMAKECONFIG_INSTALL_DIR}/XCFunConfig.cmake
  INSTALL_DESTINATION
    ${CMAKECONFIG_INSTALL_DIR}
  )

install(
  FILES
    ${PROJECT_BINARY_DIR}/${CMAKECONFIG_INSTALL_DIR}/XCFunConfig.cmake
    ${PROJECT_BINARY_DIR}/${CMAKECONFIG_INSTALL_DIR}/XCFunConfigVersion.cmake
  DESTINATION
    ${CMAKECONFIG_INSTALL_DIR}
  )

install(
  EXPORT
    "XCFunTargets"
  NAMESPACE
    "XCFun::"
  DESTINATION
    ${CMAKECONFIG_INSTALL_DIR}
  )
