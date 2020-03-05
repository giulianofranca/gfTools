set(SOURCE_FILES
    "test.cpp"
)

find_package(PythonLibs 3.7 REQUIRED)
find_package(PythonInterp 3.7 REQUIRED)
find_package(Python3 COMPONENTS Development)

# Add a shared library and link Maya libs
add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})

target_link_libraries(${PROJECT_NAME} PRIVATE Python3::Python)
target_include_directories(${PROJECT_NAME} PRIVATE Python3::Python)

# target_link_libraries(${PROJECT_NAME} PRIVATE Maya::Maya)
# target_include_directories(${PROJECT_NAME} PRIVATE Maya::Maya)
if(WIN32)
    # Windows
    set(API_SUFFIX ".pyd")
else()
    # Linux and MacOS
    set(API_SUFFIX ".so")
endif()

set_target_properties(
    ${PROJECT_NAME}
    PROPERTIES
        PREFIX ""
        OUTPUT_NAME "hello"
        LINKER_LANGUAGE C
        SUFFIX ${API_SUFFIX}
)