cmake_minimum_required(VERSION 3.10)
project(gfTools)
# Add definitions: USE_CUSTOM_PYBIND11 and USE_CUSTOM_EIGEN | CUSTOM_PYBIND11_PATH and CUSTOM_EIGEN_PATH

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_MODULE_PATH
    "${CMAKE_SOURCE_DIR}/cmake/modules"
    "${CMAKE_SOURCE_DIR}/cmake/defaults")
include(Version)

if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(INSTALL_NAME "${PROJECT_NAME}_${GFTOOLS_STR_VERSION}_${CMAKE_SYSTEM_NAME}")
    set(CMAKE_INSTALL_PREFIX "${CMAKE_SOURCE_DIR}/${INSTALL_NAME}")
endif()
message(STATUS "Install location: ${CMAKE_INSTALL_PREFIX}")

# Add subdirectories
if(BUILD_DOCS)
    add_subdirectory(docs)
endif()
if(BUILD_TOOLS OR BUILD_LIBS)
    add_subdirectory(core)
endif()
if(BUILD_TOOLS OR BUILD_LIBS OR BUILD_NODES)
    add_subdirectory(plugin)
endif()
if(BUILD_TOOLS)
    add_subdirectory(scripts)
    add_subdirectory(tools)
endif()

# Install underworld files
install(FILES "install_instructions.txt" "LICENSE"
    DESTINATION "${CMAKE_INSTALL_PREFIX}")
