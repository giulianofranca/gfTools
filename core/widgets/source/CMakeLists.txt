set(SOURCE_FILES
    "mainPlugin.cpp" "headers/mainPlugin.h"
    "analogclock.cpp" "headers/analogclock.h"
    "analogclockplugin.cpp" "headers/analogclockplugin.h"
)

# Find Packages
# find_package(PySide2 REQUIRED))
find_package(Qt5 COMPONENTS Core Gui Widgets UiPlugin REQUIRED)
get_target_property(QTCORE_LOCATION Qt5::Core LOCATION)
message(STATUS "Found Qt: ${QTCORE_LOCATION}")

# Add a shared library
add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})
set_target_properties(${PROJECT_NAME} PROPERTIES DEFINE_SYMBOL QDESIGNER_EXPORT_WIDGETS)
target_link_libraries(${PROJECT_NAME} PRIVATE Qt5::Core Qt5::Gui Qt5::Widgets Qt5::UiPlugin)
# https://wiki.qt.io/How_to_create_a_library_with_Qt_and_use_it_in_an_application#Loading_the_library_using_QLibrary

if(${MAIN_APP_BUILD})
    # Install from main build.py
    install(TARGETS ${PROJECT_NAME}
        RUNTIME DESTINATION "core/widgets")
    if(${INSTALL_SOURCE})
        message(STATUS "Installation of source code is enabled.")
        install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
            DESTINATION "core/widgets")
        install(FILES "../CMakeLists.txt"
            DESTINATION "core/widgets")
        install(FILES "../build.py"
            DESTINATION "core/widgets")
    else()
        install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/headers"
            DESTINATION "core/widgets"
            FILES_MATCHING PATTERN "*.h")
    endif()
else()
    # Install from exclusive widgets build.py
    # Don't use CONFIGURATIONS in Linux
    install(TARGETS ${PROJECT_NAME}
        RUNTIME DESTINATION "Debug"
        CONFIGURATIONS Debug)
    install(TARGETS ${PROJECT_NAME}
        RUNTIME DESTINATION "Release"
        CONFIGURATIONS Release)
    if(${INSTALL_SOURCE})
        message(WARNING "Installation of source code is not available using local build.py. Operation skipped.")
    endif()
endif()
if(${INSTALL_QTDESIGNER})
    # Install plugin to work with QtDesigner
    get_target_property(QT_QMAKE_LOCATION Qt5::qmake LOCATION)
    execute_process(COMMAND ${QT_QMAKE_LOCATION} -query QT_INSTALL_PLUGINS
        OUTPUT_VARIABLE QT_INSTALL_PLUGINS OUTPUT_STRIP_TRAILING_WHITESPACE)
    message(STATUS "Installing QtDesigner plugin in: ${QT_INSTALL_PLUGINS}/designer")
    install(TARGETS ${PROJECT_NAME}
        RUNTIME DESTINATION ${QT_INSTALL_PLUGINS}/designer)
endif()


###########################################################################################
# Test for mainwindow.cpp
# set(SOURCE_FILES
#     "main.cpp"
#     "mainwindow.cpp" "headers/mainwindow.h" "ui/mainwindow.ui"
# )

# Find Packages
# find_package(Qt5 REQUIRED COMPONENTS Core Gui Widgets)

# Add a executable
# add_executable(${PROJECT_NAME} ${SOURCE_FILES})
# target_link_libraries(${PROJECT_NAME} PRIVATE Qt5::Core Qt5::Gui Qt5::Widgets)

# if(${MAIN_APP_BUILD})
#     # Install from main build.py
#     install(TARGETS ${PROJECT_NAME}
#         RUNTIME DESTINATION "core/widgets")
#     if(${INSTALL_SOURCE})
#         message(STATUS "Installation of source code is enabled.")
#         install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
#             DESTINATION "core/widgets")
#         install(FILES "../CMakeLists.txt"
#             DESTINATION "core/widgets")
#         install(FILES "../build.py"
#             DESTINATION "core/widgets")
#     else()
#         install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/headers"
#             DESTINATION "core/widgets"
#             FILES_MATCHING PATTERN "*.h")
#     endif()
# else()
#     # Install from exclusive widgets build.py
#     # Don't use CONFIGURATIONS in Linux
#     install(TARGETS ${PROJECT_NAME}
#         RUNTIME DESTINATION "Debug"
#         CONFIGURATIONS Debug)
#     install(TARGETS ${PROJECT_NAME}
#         RUNTIME DESTINATION "Release"
#         CONFIGURATIONS Release)
#     if(${INSTALL_SOURCE})
#         message(WARNING "Installation of source code is not available using local build.py. Operation skipped.")
#     endif()
# endif()

###########################################################################################

# https://stackoverflow.com/questions/28825200/how-could-i-specify-the-file-name-of-the-qt-designer-form-class-by-cmakeqt5-wra
# https://doc.qt.io/qtcreator/adding-plugins.html
# https://doc.qt.io/qt-5/designer-using-custom-widgets.html
# https://doc.qt.io/qt-5/designer-creating-custom-widgets.html
# https://doc.qt.io/qt-5/plugins-howto.html