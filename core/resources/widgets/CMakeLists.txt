set(WIDGETS_PY_FILES
    "python/gfLayouts.py" "python/gfMayaWidgets.py" "python/gfResources.py"
    "python/gfWidgets.py")
    
install(FILES ${WIDGETS_PY_FILES}
    DESTINATION "core/resources/widgets/python")
