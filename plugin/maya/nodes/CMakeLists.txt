project(gfToolsMayaNodesPlugin)

configure_file("mainPlugin.cpp.in"
    "${CMAKE_CURRENT_BINARY_DIR}/mainPlugin.cpp" @ONLY)

set(SOURCE_FILES
    "${CMAKE_CURRENT_BINARY_DIR}/mainPlugin.cpp"
    "n_gfDebugVector.cpp" "n_gfRigMeshController.cpp" "n_gfRigPSDVectorAngle"
    "n_gfRigIKVChain.cpp" "n_gfRigHelperJoint.cpp" 
    "n_gfRigDistributeAlongSurface.cpp" "n_gfRigTwistExtractor"
    "n_gfUtilBlendTransform.cpp" "n_gfUtilAimConstraint.cpp" 
    "n_gfUtilParentConstraint.cpp" "n_gfUtilPoleVectorConstraint.cpp"
    "n_gfUtilSpaceConstraint.cpp" "n_gfUtilAngleMath.cpp" "n_gfUtilAngleMath.cpp"
    "n_gfUtilAngleScalarMath.cpp" "n_gfUtilAngleTrigMath.cpp" 
    "n_gfUtilAngleToDouble.cpp" "n_gfUtilDoubleToAngle.cpp" "n_gfUtilEulerMath.cpp"
    "n_gfUtilEulerScalarMath.cpp" "n_gfUtilEulerToVector.cpp" 
    "n_gfUtilVectorToEuler.cpp" "n_gfUtilDecompRowMatrix.cpp" 
    "n_gfUtilFindParamFromCurveLength.cpp")

set(HEADER_FILES
    "headers/n_gfDebugVector.h" "headers/n_gfRigMeshController.h"
    "headers/n_gfRigPSDVectorAngle.h" "headers/n_gfRigIKVChain.h"
    "headers/n_gfRigHelperJoint.h" "headers/n_gfRigDistributeAlongSurface.h"
    "headers/n_gfRigTwistExtractor.h" "headers/n_gfUtilBlendTransform.h"
    "headers/n_gfUtilAimConstraint.h" "headers/n_gfUtilParentConstraint.h"
    "headers/n_gfUtilPoleVectorConstraint.h" "headers/n_gfUtilSpaceConstraint.h"
    "headers/n_gfUtilAngleMath.h" "headers/n_gfUtilAngleScalarMath.h"
    "headers/n_gfUtilAngleTrigMath.h" "headers/n_gfUtilAngleToDouble.h"
    "headers/n_gfUtilDoubleToAngle.h" "headers/n_gfUtilEulerMath.h"
    "headers/n_gfUtilEulerScalarMath.h" "headers/n_gfUtilEulerToVector.h"
    "headers/n_gfUtilVectorToEuler.h" "headers/n_gfUtilDecompRowMatrix.h"
    "headers/n_gfUtilFindParamFromCurveLength.h")

set(MPX_FILES
    "mpx/MPxDeformerNode.py" "mpx/MPxLocatorNode.cpp" "mpx/MPxLocatorNode.py"
    "mpx/MPxNode.cpp" "mpx/MPxNode.py" "mpx/MPxTransform.py")

add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} PRIVATE Maya::Maya ${OPENGL_gl_LIBRARY})
target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} Maya::Maya)
target_compile_options(${PROJECT_NAME} PRIVATE ${COMPILE_FLAGS})
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "gfToolsNodes")

MAYA_PLUGIN(${PROJECT_NAME})

if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    install(TARGETS ${PROJECT_NAME}
        ${MAYA_TARGET_TYPE} DESTINATION "plugin/maya/${MAYA_VERSION}")
else()
    install(TARGETS ${PROJECT_NAME}
        ${MAYA_TARGET_TYPE} DESTINATION "plugin/maya/${MAYA_VERSION}")
    if(BUILD_TOOLS)
        install(FILES ${MPX_FILES}
            DESTINATION "plugin/maya/mpx")
    endif()
endif()