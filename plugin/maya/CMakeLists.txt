cmake_minimum_required(VERSION 3.10)
project(gfToolsMayaPlugin)

get_filename_component(GFTOOLS_ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../../ ABSOLUTE)
set(CMAKE_MODULE_PATH ${GFTOOLS_ROOT_DIR}/cmake/modules)

# Prefer legacy GL library over GLVND libraries if both are installed.
if (POLICY CMP0072)
    cmake_policy(SET CMP0072 OLD)
endif()
find_package(Maya REQUIRED)
find_package(OpenGL REQUIRED)

if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(RELEASE_NAME "${PROJECT_NAME}_${CMAKE_SYSTEM_NAME}")
    set(CMAKE_INSTALL_PREFIX ${GFTOOLS_ROOT_DIR}/${RELEASE_NAME})
endif()
message(STATUS "Install location: ${CMAKE_INSTALL_PREFIX}")

# add_subdirectory(main)
add_subdirectory(nodes)
