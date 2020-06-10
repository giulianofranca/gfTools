set(SOURCE_FILES
    "main.cpp"
)

# Find packages
find_package(OpenGL REQUIRED)

# Add a executable file
add_executable(${PROJECT_NAME} ${SOURCE_FILES})

install(TARGETS ${PROJECT_NAME} DESTINATION bin)                                    # ${CMAKE_INSTALL_PREFIX}/bin
if(${INSTALL_SOURCE})
    message(STATUS "Installation of source code is enabled.")
    install(FILES ${SOURCE_FILES} DESTINATION source)                               # ${CMAKE_INSTALL_PREFIX}/source
    install(DIRECTORY ${CMAKE_MODULE_PATH} DESTINATION ${CMAKE_INSTALL_PREFIX})     # ${CMAKE_INSTALL_PREFIX}/modules
endif()


# """
# cmake -G "Visual Studio 16 2019" -S . -B ./build
# cmake --build ./build --config Release --target install
# """