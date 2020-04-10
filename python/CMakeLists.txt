pybind11_add_module(_xcfun MODULE THIN_LTO
  export_xcfun.cpp
  )

target_include_directories(_xcfun
  PRIVATE
    ${PROJECT_BINARY_DIR}/include
    ${PROJECT_SOURCE_DIR}/src
    ${PROJECT_SOURCE_DIR}/external/upstream/taylor
  )

target_link_libraries(_xcfun
  PRIVATE
    xcfun
  )

set_target_properties(_xcfun
  PROPERTIES
    PREFIX "${PYTHON_MODULE_PREFIX}"
    SUFFIX "${PYTHON_MODULE_EXTENSION}"
    MACOSX_RPATH ON
    SKIP_BUILD_RPATH OFF
    BUILD_WITH_INSTALL_RPATH OFF
    INSTALL_RPATH_USE_LINK_PATH ON
    LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/${PYMOD_INSTALL_FULLDIR}
    RESOURCE "${CMAKE_CURRENT_SOURCE_DIR}/__init__.py;${CMAKE_CURRENT_SOURCE_DIR}/xcfun.py"
  )

foreach(_f __init__.py xcfun.py)
  add_custom_target(symlink_${_f} ALL
    COMMAND
      ${CMAKE_COMMAND} -E create_symlink
      ${CMAKE_CURRENT_SOURCE_DIR}/${_f}
      ${PROJECT_BINARY_DIR}/${PYMOD_INSTALL_FULLDIR}/${_f}
    )
endforeach()

install(
  TARGETS
    _xcfun
  LIBRARY
    DESTINATION ${PYMOD_INSTALL_FULLDIR}
    COMPONENT lib
  RESOURCE
    DESTINATION ${PYMOD_INSTALL_FULLDIR}
    COMPONENT lib
  )
