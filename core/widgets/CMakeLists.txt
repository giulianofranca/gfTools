cmake_minimum_required(VERSION 3.1)
project(gfWidgets)

set(CMAKE_AUTOMOC ON)
set(AUTOGEN_BUILD_DIR "${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}_autogen/include")
# set(MAYA_LOCATION "C:/Program Files/Autodesk/Maya2019")
# set(DEVKIT_LOCATION "C:/Program Files/Autodesk/Maya2019/devkitBase")
# set(CMAKE_PREFIX_PATH "C:/Program Files/Autodesk/Maya2019/devkitBase/cmake")

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

add_subdirectory(source)





###########################################################################################
# Test for mainwindow.cpp
# cmake_minimum_required(VERSION 3.1)
# project(helloSignalSlots)

# set(CMAKE_AUTOMOC ON)
# set(CMAKE_AUTOUIC ON)
# set(AUTOGEN_BUILD_DIR "${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}_autogen/include")

# if(CMAKE_VERSION VERSION_LESS "3.7.0")
#     set(CMAKE_INCLUDE_CURRENT_DIR ON)
# endif()

# if(NOT DEFINED INSTALL_SOURCE)
#     set(INSTALL_SOURCE OFF CACHE BOOL "Install source code into generated build files.")
# endif()

# set(RELEASE_NAME "${PROJECT_NAME}_${CMAKE_SYSTEM_NAME}")
# set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/${RELEASE_NAME})

# add_subdirectory(source)

# If needed to wrap the Widgets to PySide2
# https://github.com/giumas/shiboken2_minimal
# https://wiki.qt.io/PySide_Binding_Generation_Tutorial:_Module_5_Building_the_generator
# https://blog.basyskom.com/2019/using-shiboken2-to-create-python-bindings-for-a-qt-library/