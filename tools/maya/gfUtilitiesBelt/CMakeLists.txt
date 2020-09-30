project(gfUtilitiesBelt)

set(TOOL_DEST "tools/maya/${PROJECT_NAME}")

set(MAIN_FILES
    "__init__.py" "run.py")
set(CORE_FILES
    "core/__init__.py" "core/appInfo.py" "core/config.py"
    "core/getMayaInfo.py" "core/pockets.py" "core/resources.py"
    "core/ui.py")
set(GUI_FILES
    "gui/resources.qrc" "gui/win_about.ui" "gui/win_add.ui"
    "gui/win_main.ui" "gui/win_settings.ui")
set(GUI_IMAGES
    "gui/img/gfUtilitiesBelt_aboutApp32.svg" "gui/img/gfUtilitiesBelt_addPocket32.svg"
    "gui/img/gfUtilitiesBelt_close16.svg" "gui/img/gfUtilitiesBelt_editPocket32.svg"
    "gui/img/gfUtilitiesBelt_hammer32.svg" "gui/img/gfUtilitiesBelt_icon32.svg"
    "gui/img/gfUtilitiesBelt_iconView16.svg" "gui/img/gfUtilitiesBelt_listView16.svg"
    "gui/img/gfUtilitiesBelt_menu16.svg" "gui/img/gfUtilitiesBelt_python32.svg"
    "gui/img/gfUtilitiesBelt_pythonMini32.svg" "gui/img/gfUtilitiesBelt_search16.svg"
    "gui/img/gfUtilitiesBelt_settings32.svg" "gui/img/gfUtilitiesBelt_tool32.svg"
    "gui/img/gfUtilitiesBelt_updateLibraries32.svg")
set(POCKETS_FILES
    "pockets/Test.gfpocket")

# Install files
install(FILES ${MAIN_FILES}
    DESTINATION "${TOOL_DEST}")
install(FILES ${CORE_FILES}
    DESTINATION "${TOOL_DEST}/core")
install(FILES ${GUI_FILES}
    DESTINATION "${TOOL_DEST}/gui")
install(FILES ${GUI_IMAGES}
    DESTINATION "${TOOL_DEST}/gui/img")
install(FILES ${POCKETS_FILES}
    DESTINATION "${TOOL_DEST}/pockets")
