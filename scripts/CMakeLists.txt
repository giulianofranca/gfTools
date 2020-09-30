project(gfToolsScripts)

set(STANDALONE_SCRIPTS
    "mayaInstall.py" "mayaUninstall.py")

set(MAYA_SCRIPTS
    "maya/gfToolsMenu.py" "maya/gfToolsShelf.py" "maya/userSetup.py"
    "maya/gfToolsLauncher.py")

set(MAYA_AETEMPLATES_FILES
    "maya/AETemplates/AEgfAimConstraintTemplate.mel" 
    "maya/AETemplates/AEgfAngleMathTemplate.mel"
    "maya/AETemplates/AEgfAngleScalarMathTemplate.mel"
    "maya/AETemplates/AEgfAngleToDoubleTemplate.mel"
    "maya/AETemplates/AEgfAngleTrigMathTemplate.mel"
    "maya/AETemplates/AEgfBlendTransformTemplate.mel"
    "maya/AETemplates/AEgfDecompRowMtxTemplate.mel"
    "maya/AETemplates/AEgfDistributeAlongSurfaceTemplate.mel"
    "maya/AETemplates/AEgfDoubleToAngleTemplate.mel"
    "maya/AETemplates/AEgfEulerMathTemplate.mel"
    "maya/AETemplates/AEgfEulerScalarMathTemplate.mel"
    "maya/AETemplates/AEgfEulerToVectorTemplate.mel"
    "maya/AETemplates/AEgfIKVChainTemplate.mel"
    "maya/AETemplates/AEgfParentConstraintTemplate.mel"
    "maya/AETemplates/AEgfPSDVectorAngleTemplate.mel"
    "maya/AETemplates/AEgfTwistExtractorTemplate.mel"
    "maya/AETemplates/AEgfVectorToEulerTemplate.mel")

set(MAYA_SHELVES_FILES
    "maya/shelves/shelf_gfTools.mel")

install(FILES ${STANDALONE_SCRIPTS}
    DESTINATION "scripts")
install(FILES ${MAYA_SCRIPTS}
    DESTINATION "scripts/maya")
if(BUILD_NODES)
    install(FILES ${MAYA_AETEMPLATES_FILES}
        DESTINATION "scripts/maya/AETemplates")
endif()
install(FILES ${MAYA_SHELVES_FILES}
    DESTINATION "scripts/maya/shelves")
