# https://www.it-swarm.dev/pt/visual-studio/integre-o-llvm-clang-4.x.x5.x.x6.x.x-ao-visual-studio-2017/830728596/
# https://docs.microsoft.com/pt-br/cpp/build/clang-support-msbuild?view=vs-2019#custom_llvm_location
# https://doc.qt.io/qtforpython/shiboken2/gettingstarted.html
# https://blog.basyskom.com/2019/using-shiboken2-to-create-python-bindings-for-a-qt-library/
# https://www.qt.io/blog/2018/05/31/write-python-bindings
# https://www.ics.com/blog/integrating-custom-widget-qt-designer
# https://gist.github.com/dgovil/852777eca16bfbabac224b50e6d8d739
# https://forums.cgsociety.org/t/c-qt-q-object-problem-with-cmake/1815551/4

#.rst:
# FindPySide2
# -------------
# 
# Find PySide2 headers and libraries
# 
# Imported targets
# ^^^^^^^^^^^^^^^^
# 
# This module defines the following :prop_tgt:`IMPORTED` target:
# 
# ``PySide2::PySide2``
#   The Shiboken 2 libraries, if found.
#
# Result variables
# ^^^^^^^^^^^^^^^^
#
# This module will set the following variables in your project:
# 
# ``PySide2_FOUND``
#   Defined if PySide2 has been detected
# ``PYSIDE2_INCLUDE_DIR``
#   Where to find the headers
# ``PYSIDE2_INCLUDE_DIRS``
#   All the PySide2 headers location
# ``PYSIDE2_MODULE_PATH``
#   The PySide2 module path
# ``PYSIDE2_CONFIG_FILE``
#   The Pyside2 config file (pyside2_config.py)
# ``PYSIDE2_TYPESYSTEMS``
#   The PySide2 typesystems path
# ``PySide2_VERSION``
#   The version of PySide2
# 

set(_module PySide2)
set(_library PySide2)

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

set(PYSIDE2_MODULE_PATH "${PYTHON_SITE_PACKAGES}/PySide2")
set(PYSIDE2_CONFIG_FILE "${PYSIDE2_MODULE_PATH}/examples/utils/pyside2_config.py")

# PySide2 library
execute_process(
    COMMAND ${Python3_EXECUTABLE} "${PYSIDE2_CONFIG_FILE}" 
        --pyside2-shared-libraries-cmake
    OUTPUT_VARIABLE _output_var
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
if(${_output_var} STREQUAL "")
    message(FATAL_ERROR "Error: Calling pyside2_config.py returned no output.")
endif()
string(REPLACE " " ";" PYSIDE2_LIBRARY ${_output_var})


# PySide2 include directory
find_path(PYSIDE2_INCLUDE_DIR
    "pyside.h"
    PATH
        "${PYSIDE2_MODULE_PATH}/include"
    NO_DEFAULT_PATH
)

# PySide2 typesystems directory
find_path(PYSIDE2_TYPESYSTEMS
    "typesystem_core.xml"
    PATHS
        "${PYSIDE2_MODULE_PATH}/typesystems"
        NO_DEFAULT_PATH
)

set(PYSIDE2_INCLUDE_DIRS "${PYSIDE2_INCLUDE_DIR}")

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(${_module}
    FOUND_VAR ${_module}_FOUND
    REQUIRED_VARS PYSIDE2_LIBRARY PYSIDE2_INCLUDE_DIR PYSIDE2_TYPESYSTEMS
    VERSION_VAR ${_module}_VERSION
)
mark_as_advanced(PYSIDE2_INCLUDE_DIR PYSIDE2_LIBRARY)


if (NOT TARGET ${_module}::${_library})
    add_library(${_module}::${_library} INTERFACE IMPORTED)
    set_target_properties(${_module}::${_library} PROPERTIES
        INTERFACE_INCLUDE_DIRECTORIES "${PYSIDE2_INCLUDE_DIR}"
        INTERFACE_LINK_LIBRARIES "${PYSIDE2_LIBRARY}"
    )
endif()

set(_PYSIDE2_INCLUDES QtCore QtGui QtWidgets)
foreach(PYSIDE2_INC ${_PYSIDE2_INCLUDES})
    find_path(PYSIDE2_${PYSIDE2_INC}_INCLUDES
        NAMES
            "${PYSIDE2_INC}"
        PATHS
            "${PYSIDE2_INCLUDE_DIR}"
        NO_DEFAULT_PATH
    )
    mark_as_advanced(PYSIDE2_${PYSIDE2_INC}_INCLUDES)
    if(PYSIDE2_${PYSIDE2_INC}_INCLUDES)
        add_library(${_module}::${PYSIDE2_INC} INTERFACE IMPORTED)
        set_target_properties(${_module}::${PYSIDE2_INC} PROPERTIES
            INTERFACE_INCLUDE_DIRECTORIES "${PYSIDE2_${PYSIDE2_INC}_INCLUDES}"
        )
        set_property(TARGET ${_module}::${_library} APPEND PROPERTY
            INTERFACE_INCLUDE_DIRECTORIES ${_module}::${PYSIDE2_INC}
        )
        set(PYSIDE2_INCLUDE_DIRS ${PYSIDE2_INCLUDE_DIRS} "PYSIDE2_${PYSIDE2_INC}_INCLUDES")
    endif()
endforeach()


function(PYSIDE2_BINDINGS _target)
    set_target_properties(${_target} PROPERTIES
        PREFIX ""
        SUFFIX ${PYTHON_EXTENSION_SUFFIX})
endfunction()