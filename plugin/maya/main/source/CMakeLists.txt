set(SOURCE_FILES
    "mainPlugin.cpp")

add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} PRIVATE Maya::Maya)
target_include_directories(${PROJECT_NAME} PRIVATE Maya::Maya)
target_compile_options(${PROJECT_NAME} PRIVATE ${COMPILE_FLAGS})

MAYA_PLUGIN(${PROJECT_NAME})

if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    install(TARGETS ${PROJECT_NAME}
        ${MAYA_TARGET_TYPE} DESTINATION "maya${MAYA_VERSION}")
else()
    install(TARGETS ${PROJECT_NAME}
        ${MAYA_TARGET_TYPE} DESTINATION "plugin/maya/release/maya${MAYA_VERSION}")
endif()
