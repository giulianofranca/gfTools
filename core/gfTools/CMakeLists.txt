# Install modules
configure_file("gfCore.py"
    "${CMAKE_CURRENT_BINARY_DIR}/gfCore.py" @ONLY)

set(MODULES_FILES
    "__init__.py"
    "${CMAKE_CURRENT_BINARY_DIR}/gfCore.py")


install(FILES ${MODULES_FILES}
    DESTINATION "lib/maya/${MAYA_VERSION}/python/gfTools")