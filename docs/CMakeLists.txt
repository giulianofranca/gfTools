# Look for Doxygen package
find_package(Doxygen REQUIRED)

set(DOXYGEN_INPUT_DIRS "${CMAKE_SOURCE_DIR}/docs/pages"
    "${CMAKE_SOURCE_DIR}/core/gfTools" 
    "${CMAKE_SOURCE_DIR}/core/gfRig/headers"
)
message(STATUS "gfTools directory: ${CMAKE_SOURCE_DIR}")

foreach(INPUT_DIR ${DOXYGEN_INPUT_DIRS})
    set(DOXYGEN_INPUT_DIR "${DOXYGEN_INPUT_DIR} ${INPUT_DIR}")
endforeach()
set(DOXYGEN_OUTPUT_DIR "${CMAKE_CURRENT_BINARY_DIR}")
set(DOXYGEN_INDEX_FILE "${DOXYGEN_OUTPUT_DIR}/html/index.html")
set(DOXYFILE_IN "Doxyfile.in")
set(DOXYFILE_OUT "${CMAKE_CURRENT_BINARY_DIR}/Doxyfile")

configure_file(${DOXYFILE_IN} ${DOXYFILE_OUT} @ONLY)

file(MAKE_DIRECTORY ${DOXYGEN_OUTPUT_DIR})
add_custom_target(gfToolsDocs ALL
    COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYFILE_OUT}
    WORKING DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Generating Documentation"
    VERBATIM)

install(DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/doxy_html"
    DESTINATION "docs")
