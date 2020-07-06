#.rst:
# FindShiboken2
# -------------
# 
# Find Shiboken2 headers, libraries and generators
# 
# Imported targets
# ^^^^^^^^^^^^^^^^
# 
# This module defines the following :prop_tgt:`IMPORTED` target:
# 
# ``Shiboken2::Shiboken2``
#   The Shiboken 2 generator, if found.
# 
# ``Shiboken2::Shiboken2Lib``
#   The Shiboken 2 libraries, if found.
#
# Result variables
# ^^^^^^^^^^^^^^^^
#
# This module will set the following variables in your project:
# 
# ``Shiboken2_FOUND``
#   Defined if Shiboken2 has been detected
# ``SHIBOKEN2_INCLUDE_DIR``
#   Where to find the headers
# ``SHIBOKEN2_LIBRARIES``
#   All the Shiboken2 libraries
# ``SHIBOKEN2_EXECUTABLE``
#   The Shiboken2 generator
# ``SHIBOKEN2_MODULE_PATH``
#   The Shiboken2 module path
# ``Shiboken2_VERSION``
#   The version of Shiboken2
# 

set(_module Shiboken2)
set(_executable Shiboken2)
set(_library Shiboken2Lib)

if (Python3_FOUND)
    if (Python3_SITELIB)
        set(PYTHON_SITE_PACKAGES ${Python3_SITELIB})
    else()
        message(FATAL_ERROR "Could not find Python3 site-packages.")
    endif()
else()
    message(FATAL_ERROR "Could not find Python3.")
endif()

if(WIN32)
    set(PYTHON_EXTENSION_SUFFIX ".pyd")
else()
    set(PYTHON_EXTENSION_SUFFIX ".so")
endif()

set(SHIBOKEN2_MODULE_PATH "${PYTHON_SITE_PACKAGES}/shiboken2")

# Shiboken2 library directory
if (WIN32)
    find_file(SHIBOKEN2_LIBRARY
        NAMES
            "shiboken2${PYTHON_EXTENSION_SUFFIX}"
        PATHS
            "${SHIBOKEN2_MODULE_PATH}"
    )
else()
    find_library(SHIBOKEN2_LIBRARY
        NAMES
            "shiboken2${PYTHON_EXTENSION_SUFFIX}"
            "shiboken2.abi3${PYTHON_EXTENSION_SUFFIX}"
        PATHS
            "${SHIBOKEN2_MODULE_PATH}"
    )
endif()

# Shiboken2 include directory
find_path(SHIBOKEN2_INCLUDE_DIR
    "shiboken.h"
    PATH
        "${PYTHON_SITE_PACKAGES}/shiboken2_generator/include"
    NO_DEFAULT_PATH
)

# Shiboken2 executable
find_file(SHIBOKEN2_EXECUTABLE
    NAMES
        "shiboken2"
        "shiboken2.exe"
    PATHS
        "${PYTHON_SITE_PACKAGES}/shiboken2_generator"
    NO_DEFAULT_PATH
)

set(SHIBOKEN2_LIBRARIES "${SHIBOKEN2_LIBRARY}")

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(${_module}
    FOUND_VAR ${_module}_FOUND
    REQUIRED_VARS SHIBOKEN2_EXECUTABLE SHIBOKEN2_INCLUDE_DIR SHIBOKEN2_LIBRARY
    VERSION_VAR ${_module}_VERSION
)
mark_as_advanced(SHIBOKEN2_EXECUTABLE SHIBOKEN2_INCLUDE_DIR SHIBOKEN2_LIBRARY)


if (NOT TARGET ${_module}::${_library})
    add_library(${_module}::${_library} INTERFACE IMPORTED)
    set_target_properties(${_module}::${_library} PROPERTIES
        INTERFACE_INCLUDE_DIRECTORIES "${SHIBOKEN2_INCLUDE_DIR}"
        INTERFACE_LINK_LIBRARIES "${SHIBOKEN2_LIBRARY}"
    )
endif()

if (NOT TARGET ${_module}::${_executable})
    add_executable(${_module}::${_executable} IMPORTED)
    set_target_properties(${_module}::${_executable} PROPERTIES
        IMPORTED_LOCATION "${SHIBOKEN2_EXECUTABLE}"
    )
endif()

# Add the cmake shared libraries
if (${PySide2_FOUND})
    execute_process(
        COMMAND ${Python3_EXECUTABLE} "${PYSIDE2_CONFIG_FILE}" 
            --shiboken2-module-shared-libraries-cmake
        OUTPUT_VARIABLE _output_var
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    if (${_output_var} STREQUAL "")
        message(FATAL_ERROR "Error: Calling pyside2_config.py returned no output.")
    endif()
    string (REPLACE " " ";" _SHIBOKEN2_CMAKE_LIB ${_output_var})
else()
    message(FATAL_ERROR "Error: Could not find PySide2")
endif()
if (_SHIBOKEN2_CMAKE_LIB)
    add_library(${_module}::CMakeSharedLib INTERFACE IMPORTED)
    set_target_properties(${_module}::CMakeSharedLib PROPERTIES
        INTERFACE_LINK_LIBRARIES "${_SHIBOKEN2_CMAKE_LIB}"
    )
    set_property(TARGET ${_module}::${_library} APPEND PROPERTY
        INTERFACE_LINK_LIBRARIES ${_module}::CMakeSharedLib
    )
    set(SHIBOKEN2_LIBRARIES ${SHIBOKEN2_LIBRARIES} "${_SHIBOKEN2_CMAKE_LIB}")
    mark_as_advanced(_SHIBOKEN_CMAKE_LIB)
endif()


function(SHIBOKEN2_GENERATOR options wrapped_header typesystem_file out_sources)
    set(_dependencies ${wrapped_header} ${typesystem_file})
    add_custom_command(OUTPUT ${generated_sources}
        COMMAND ${SHIBOKEN2_EXECUTABLE} ${options} ${wrapped_header} ${typesystem_file}
        DEPENDS ${_dependemcies}
        IMPLICIT_DEPENDS CXX ${wrapped_header}
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Running Shiboken2 generator for ${typesystem_file}."
    )
    set(${out_sources} ${generated_sources} PARENT_SCOPE)
endfunction()
