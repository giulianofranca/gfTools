find_package(Maya REQUIRED)

if(BUILD_TOOLS OR BUILD_LIBS)
    # Add the gfTools plugin to use the contexts in tools or/and undo stack in libs.
    add_subdirectory(main)
endif()

if(BUILD_NODES)
    # Prefer legacy GL library over GLVND libraries if both are installed.
    if (POLICY CMP0072)
        cmake_policy(SET CMP0072 OLD)
    endif()
    find_package(OpenGL REQUIRED)
    add_subdirectory(nodes)
endif()
