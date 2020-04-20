set(SOURCE_FILES
    "mainPlugin.cpp"
    "n_gfDebugVector.cpp" "headers/n_gfDebugVector.h"
    "n_gfRigMeshController.cpp" "headers/n_gfRigMeshController.h"
    "n_gfRigPSDVectorAngle.cpp" "headers/n_gfRigPSDVectorAngle.h"
    "n_gfRigIKVChain.cpp" "headers/n_gfRigIKVChain.h"
    "n_gfRigHelperJoint.cpp" "headers/n_gfRigHelperJoint.h"
    "n_gfRigDistributeAlongSurface.cpp" "headers/n_gfRigDistributeAlongSurface.h"
    "n_gfRigTwistExtractor.cpp" "headers/n_gfRigTwistExtractor.h"
    "n_gfUtilBlendTransform.cpp" "headers/n_gfUtilBlendTransform.h"
    "n_gfUtilAimConstraint.cpp" "headers/n_gfUtilAimConstraint.h"
    "n_gfUtilParentConstraint.cpp" "headers/n_gfUtilParentConstraint.h"
    "n_gfUtilPoleVectorConstraint.cpp" "headers/n_gfUtilPoleVectorConstraint.h"
    "n_gfUtilSpaceConstraint.cpp" "headers/n_gfUtilSpaceConstraint.h"
    "n_gfUtilAngleMath.cpp" "headers/n_gfUtilAngleMath.h"
    "n_gfUtilAngleScalarMath.cpp" "headers/n_gfUtilAngleScalarMath.h"
    "n_gfUtilAngleTrigMath.cpp" "headers/n_gfUtilAngleTrigMath.h"
    "n_gfUtilAngleToDouble.cpp" "headers/n_gfUtilAngleToDouble.h"
    "n_gfUtilDoubleToAngle.cpp" "headers/n_gfUtilDoubleToAngle.h"
    "n_gfUtilEulerMath.cpp" "headers/n_gfUtilEulerMath.h"
    "n_gfUtilEulerScalarMath.cpp" "headers/n_gfUtilEulerScalarMath.h"
    "n_gfUtilEulerToVector.cpp" "headers/n_gfUtilEulerToVector.h"
    "n_gfUtilVectorToEuler.cpp" "headers/n_gfUtilVectorToEuler.h"
    "n_gfUtilDecompRowMatrix.cpp" "headers/n_gfUtilDecompRowMatrix.h"
    "n_gfUtilFindParamFromCurveLength.cpp" "headers/n_gfUtilFindParamFromCurveLength.h"
)

# if(WIN32)
#     set(COMPILE_FLAGS "/arch:AVX")
# else()
#     set(COMPILE_FLAGS "-mavx")
# endif()

# Find FindMaya.cmake
find_package(Maya REQUIRED)
find_package(OpenGL REQUIRED)

# Add a shared library and link Maya libs
add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} PRIVATE Maya::Maya ${OPENGL_gl_LIBRARY})
target_include_directories(${PROJECT_NAME} PRIVATE Maya::Maya)
target_compile_options(${PROJECT_NAME} PRIVATE ${COMPILE_FLAGS})

MAYA_PLUGIN(${PROJECT_NAME})





# Find Maya libs and headers
# include_directories(${MAYA_INCLUDE_DIR})
# link_directories(${MAYA_LIBRARY_DIR})


# target_link_libraries(${PROJECT_NAME} ${MAYA_LIBRARIES})



# install(TARGETS ${PROJECT_NAME} ${MAYA_TARGET_TYPE} DESTINATION plug-ins)




# HOW TO COMPILE
# 1- cd <build folder>
# 2- cmake -h
# 3- cmake -G "Visual Studio 11 2012 Win64" -DMAYA_VERSION=2017 ../         # Pass the project CMakeLists.txt location
# 4- cmake --build . --config Release
# 5- cmake --build . --config Release --target Install

# LINUX = https://lexfrench.com/?p=842