project(gfRig)

configure_file("version.hpp.in"
    "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}/version.hpp" @ONLY)

set(SOURCE_FILES
    "attribute.cpp" "utils.cpp")

set(HEADERS_FILES
    "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}/version.hpp"
    "headers/framework.hpp" "headers/attribute.hpp" "headers/utils.hpp")

set(WRAPPER_FILES
    "python/gfRigWrapper.cpp" 
    "python/attributeWrapper.hpp" "python/utilsWrapper.hpp")

# Find packages
find_package(Maya REQUIRED)
if(USE_MAYAPY)
    set(PYTHON_EXECUTABLE ${MAYA_PYTHON_INTERPRETER})
else()
    set(PYBIND11_PYTHON_VERSION 2.7)
endif()
add_subdirectory("${CMAKE_SOURCE_DIR}/third_party/pybind11" 
    "${CMAKE_CURRENT_BINARY_DIR}/pybind11")

# C++ Library
set(CPP_LIB "${PROJECT_NAME}")
add_library(${CPP_LIB} SHARED ${SOURCE_FILES} ${HEADER_FILES})
target_link_libraries(${CPP_LIB} PRIVATE Maya::Maya)
target_include_directories(${CPP_LIB} PRIVATE ${CMAKE_CURRENT_BINARY_DIR} Maya::Maya)
target_compile_options(${CPP_LIB} PRIVATE ${COMPILE_FLAGS})

install(TARGETS ${CPP_LIB} LIBRARY
    DESTINATION "lib/maya/${MAYA_VERSION}")

# Python Bindings
set(PYTHON_LIB "${PROJECT_NAME}Bindings")
pybind11_add_module(${PYTHON_LIB} ${WRAPPER_FILES} 
    ${HEADER_FILES} ${SOURCE_FILES})
target_link_libraries(${PYTHON_LIB} PRIVATE Maya::Maya)
target_include_directories(${PYTHON_LIB} PRIVATE "${CMAKE_CURRENT_BINARY_DIR}" Maya::Maya)
target_compile_options(${PYTHON_LIB} PRIVATE ${COMPILE_FLAGS})
set_target_properties(${PYTHON_LIB} PROPERTIES OUTPUT_NAME ${PROJECT_NAME})

install(TARGETS ${PYTHON_LIB} LIBRARY
    DESTINATION "lib/maya/${MAYA_VERSION}/python/gfTools")

# Install include
install(FILES ${HEADERS_FILES}
    DESTINATION "include/${PROJECT_NAME}")
