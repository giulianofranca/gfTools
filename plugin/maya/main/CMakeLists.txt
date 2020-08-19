cmake_minimum_required(VERSION 3.10)
project(gfTools)

if(NOT FULL_BUILD)
    set(RELEASE_NAME "${PROJECT_NAME}_${CMAKE_SYSTEM_NAME}")
    set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/${RELEASE_NAME})
    set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/modules)
endif()

add_subdirectory(source)

# Load/Unload menu
# Load/Unload shelf
# Undo stack for rig framework
