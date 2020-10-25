project(gfToolsMayaNodesPlugin)

configure_file("mainPlugin.cpp.in"
    "${CMAKE_CURRENT_BINARY_DIR}/mainPlugin.cpp" @ONLY)

set(SOURCE_FILES
    "${CMAKE_CURRENT_BINARY_DIR}/mainPlugin.cpp"
    "angleMath.cpp" "angleTrig.cpp" "visualizeVector.cpp"
    "poseReader.cpp")

set(HEADER_FILES
    "headers/angleMath.hpp" "headers/angleTrig.hpp" "headers/visualizeVector.hpp"
    "headers/poseReader.hpp")

add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES} ${HEADER_FILES})
target_link_libraries(${PROJECT_NAME} PRIVATE Maya::Maya ${OPENGL_gl_LIBRARY})
target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} Maya::Maya)
target_compile_options(${PROJECT_NAME} PRIVATE ${COMPILE_FLAGS})
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "gfToolsNodes")

MAYA_PLUGIN(${PROJECT_NAME})

if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    install(TARGETS ${PROJECT_NAME}
        ${MAYA_TARGET_TYPE} DESTINATION "plugin/maya/${MAYA_VERSION}")
else()
    install(TARGETS ${PROJECT_NAME}
        ${MAYA_TARGET_TYPE} DESTINATION "plugin/maya/${MAYA_VERSION}")
endif()