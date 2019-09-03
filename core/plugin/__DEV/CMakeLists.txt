# PROJECT CMAKELISTS FILE

cmake_minimum_required(VERSION 3.1)

# name of the .mll/.bundle/.so file | ${PROJECT_NAME} var
project(sampleplugin)

# build/install
set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_BINARY_DIR}/install)
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/modules)

# Add src directory
add_subdirectory(TestProjectSrc)