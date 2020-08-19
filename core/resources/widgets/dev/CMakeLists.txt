cmake_minimum_required(VERSION 3.1)
project(gfWidgets)

set(CMAKE_AUTOMOC ON)
set(AUTOGEN_BUILD_DIR "${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}_autogen/include")

if(CMAKE_VERSION VERSION_LESS "3.7.0")
    set(CMAKE_INCLUDE_CURRENT_DIR ON)
endif()

if(NOT DEFINED INSTALL_SOURCE)
    set(INSTALL_SOURCE OFF CACHE BOOL "Install source code into generated build files.")
endif()

if(NOT DEFINED INSTALL_QTDESIGNER)
    set(INSTALL_QTDESIGNER OFF CACHE BOOL "Install plugin in QtDesigner plugin path.")
endif()

set(RELEASE_NAME "${PROJECT_NAME}_${CMAKE_SYSTEM_NAME}")
set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/${RELEASE_NAME})
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/modules)

add_subdirectory(source)


# Maya Qt Searches
# https://forums.cgsociety.org/t/c-qt-q-object-problem-with-cmake/1815551/3
# https://gist.github.com/dgovil/852777eca16bfbabac224b50e6d8d739
# https://help.autodesk.com/view/MAYAUL/2019/ENU/?guid=Maya_SDK_MERGED_Working_with_Qt_Using_Qt_in_Plug_ins_html

# If needed to wrap the Widgets to PySide2
# https://github.com/giumas/shiboken2_minimal
# https://wiki.qt.io/PySide_Binding_Generation_Tutorial:_Module_5_Building_the_generator
# https://blog.basyskom.com/2019/using-shiboken2-to-create-python-bindings-for-a-qt-library/
# https://www.qt.io/blog/2018/05/31/write-python-bindings