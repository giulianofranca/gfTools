# This is the full project build settings
cmake_minimum_required(VERSION 3.1)
project(gfTools)

set(MAIN_APP_BUILD ON CACHE BOOL "Set this to allow to build the whole gfTools plug-in.")

if(NOT DEFINED INSTALL_SOURCE)
    set(INSTALL_SOURCE OFF CACHE BOOL "Install source code into generated build files.")
endif()

set(RELEASE_NAME "${PROJECT_NAME}_${CMAKE_SYSTEM_NAME}")
set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/${RELEASE_NAME})
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules)

# To compile the plug-ins
add_subdirectory(plug-ins/dev/cpp/source)

# To compile the framework
# add_subdirectory()

# To compile the applications
# add_subdirectory()