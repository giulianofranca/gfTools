cmake_minimum_required(VERSION 3.1)
project(gfTools)

if(NOT DEFINED INSTALL_SOURCE)
    set(INSTALL_SOURCE OFF CACHE BOOL "Install source code into generated build files.")
endif()

set(RELEASE_NAME "${PROJECT_NAME}_${CMAKE_SYSTEM_NAME}")
set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/${RELEASE_NAME})
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/modules)

add_subdirectory(source)