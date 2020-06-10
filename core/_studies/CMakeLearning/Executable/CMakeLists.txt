cmake_minimum_required(VERSION 3.1)
project(LearningCMakeExe)

if(NOT DEFINED INSTALL_SOURCE)
    set(INSTALL_SOURCE OFF CACHE BOOL "Install source code into generated build files.")
endif()

set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}) # ${PROJECT_PATH}
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/modules)
add_subdirectory(source)

# set(PROJECT_PATH ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT})