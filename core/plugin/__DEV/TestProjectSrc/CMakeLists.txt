# SOURCE CMAKELISTS FILE

set(SOURCE_FILES
    "pluginMain.cpp"
    "sampleCmd.cpp"
    "sampleCmd.h"
)

# Find FindMaya.cmake
find_package(Maya REQUIRED)

# Find Maya libs and headers
include_directories(${MAYA_INCLUDE_DIR})
link_directories(${MAYA_LIBRARY_DIR})

# Add a shared library and link Maya libs
add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} ${MAYA_LIBRARIES})

MAYA_PLUGIN(${PROJECT_NAME})

install(TARGETS ${PROJECT_NAME} ${MAYA_TARGET_TYPE} DESTINATION plug-ins)




# HOW TO COMPILE
# 1- cd <build folder>
# 2- cmake -h
# 3- cmake -G "Visual Studio 11 2012 Win64" -DMAYA_VERSION=2017 ../         # Pass the project CMakeLists.txt location
# 4- cmake --build . --config Release
# 5- cmake --build . --config Release --target Install