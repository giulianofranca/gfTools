if(BUILD_LIBS)
    add_subdirectory(gfRig)
endif()

if(BUILD_TOOLS)
    add_subdirectory(gfTools)
    add_subdirectory(resources)
endif()
