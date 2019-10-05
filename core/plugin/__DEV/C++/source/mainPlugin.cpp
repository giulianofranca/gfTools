/*
Copyright(c) 2019 Giuliano França

Maya IDs :
	Prototypes: 0x0012f7c0 - 0x0012f7ff
	Releases : 0x00130d80 - 0x00130e7f

Redistribution :
	Something here.

Maya Plugin :
	Something here.

How to use :
    * Copy and paste this file to a Maya plugins path, default: "C:/Users/<user>/Documents/maya/<version>/plug-ins".
		You can create a "plug-ins" folder if not exists.
	* Open your Maya(same version).
	* Go to Windows > Settings / Preferences > Plug-in Manager.
	* Mark this file as loaded.

Requirements:
	Maya 2017 or above.

Todo:
	* NDA
*/
// gfDebug
#include "n_gfDebugVector.h"
// gfRig
#include "n_gfRigPSDVectorAngle.h"
#include "n_gfRigIKVChain.h"
// gfUtil
#include "n_gfUtilBlendTransform.h"
#include "n_gfUtilAimConstraint.h"
#include "n_gfUtilParentConstraint.h"
#include "n_gfUtilAngleMath.h"
#include "n_gfUtilAngleScalarMath.h"
#include "n_gfUtilAngleTrigMath.h"
#include "n_gfUtilAngleToDouble.h"
#include "n_gfUtilDoubleToAngle.h"
#include "n_gfUtilEulerMath.h"
#include "n_gfUtilEulerScalarMath.h"
#include "n_gfUtilEulerToVector.h"
#include "n_gfUtilVectorToEuler.h"
#include "n_gfUtilDecompRowMatrix.h"

#include <maya/MFnPlugin.h>
#include <maya/MDrawRegistry.h>
#include <maya/MString.h>
#include <maya/MTypeId.h>


#define REGISTER_NODE(NODE, PLUGIN)         \
    status = PLUGIN.registerNode(           \
        NODE::kNodeName,                    \
        NODE::kNodeID,                      \
        NODE::creator,                      \
        NODE::initialize,                   \
        MPxNode::kDependNode,               \
        &NODE::kNodeClassify                \
    );                                      \
    CHECK_MSTATUS(status);                  \

#define DEREGISTER_NODE(NODE, PLUGIN)       \
    status = PLUGIN.deregisterNode(         \
        NODE::kNodeID                       \
    );                                      \
    CHECK_MSTATUS(status);                  \

#define REGISTER_LOCATOR_NODE(NODE, PLUGIN, DRAWOVERRIDE)                   \
    status = PLUGIN.registerNode(                                           \
        NODE::kNodeName,                                                    \
        NODE::kNodeID,                                                      \
        NODE::creator,                                                      \
        NODE::initialize,                                                   \
        MPxNode::kLocatorNode,                                              \
        &NODE::kNodeClassify                                                \
    );                                                                      \
    CHECK_MSTATUS(status);                                                  \
    status = MHWRender::MDrawRegistry::registerDrawOverrideCreator(         \
        NODE::kNodeClassify,                                                \
        NODE::kNodeRegistrantID,                                            \
        DRAWOVERRIDE::creator                                               \
    );                                                                      \
    CHECK_MSTATUS(status);                                                  \

#define DEREGISTER_LOCATOR_NODE(NODE, PLUGIN)                               \
    status = PLUGIN.deregisterNode(                                         \
        NODE::kNodeID                                                       \
    );                                                                      \
    CHECK_MSTATUS(status);                                                  \
    status = MHWRender::MDrawRegistry::deregisterDrawOverrideCreator(       \
        NODE::kNodeClassify,                                                \
        NODE::kNodeRegistrantID                                             \
    );                                                                      \
    CHECK_MSTATUS(status);                                                  \


const char* kAuthor = "Giuliano Franca";
const char* kVersion = "1.0 Pro";
const char* kRequiredAPIVersion = "Any";

// gfDebug
const MString DebugVector::kNodeName = "gfDebugVector";
const MString DebugVector::kNodeClassify = "drawdb/geometry/locator";
const MString DebugVector::kNodeRegistrantID = "gfDebugVectorNodePlugin";
const MTypeId DebugVector::kNodeID = 0x00130d80;
// gfRig
const MString VectorAnglePSD::kNodeName = "gfRigPSDVectorAngle";
const MString VectorAnglePSD::kNodeClassify = "utility/general";
const MTypeId VectorAnglePSD::kNodeID = 0x00130d81;
const MString IKVChainSolver::kNodeName = "gfRigIKVChain";
const MString IKVChainSolver::kNodeClassify = "utility/general";
const MTypeId IKVChainSolver::kNodeID = 0x00130d82;
// gfUtil
const MString BlendTransform::kNodeName = "gfUtilBlendTransform";
const MString BlendTransform::kNodeClassify = "utility/general";
const MTypeId BlendTransform::kNodeID = 0x00130d83;
const MString AimConstraint::kNodeName = "gfUtilAimConstraint";
const MString AimConstraint::kNodeClassify = "utility/general";
const MTypeId AimConstraint::kNodeID = 0x00130d84;
const MString ParentConstraint::kNodeName = "gfUtilParentConstraint";
const MString ParentConstraint::kNodeClassify = "utility/general";
const MTypeId ParentConstraint::kNodeID = 0x00130d85;
const MString AngularMath::kNodeName = "gfUtilAngleMath";
const MString AngularMath::kNodeClassify = "utility/general";
const MTypeId AngularMath::kNodeID = 0x00130d86;
const MString AngularScalarMath::kNodeName = "gfUtilAngleScalarMath";
const MString AngularScalarMath::kNodeClassify = "utility/general";
const MTypeId AngularScalarMath::kNodeID = 0x00130d87;
const MString AngularTrigMath::kNodeName = "gfUtilAngleTrigMath";
const MString AngularTrigMath::kNodeClassify = "utility/general";
const MTypeId AngularTrigMath::kNodeID = 0x00130d88;
const MString AngleToDouble::kNodeName = "gfUtilAngleToDouble";
const MString AngleToDouble::kNodeClassify = "utility/general";
const MTypeId AngleToDouble::kNodeID = 0x00130d89;
const MString DoubleToAngle::kNodeName = "gfUtilDoubleToAngle";
const MString DoubleToAngle::kNodeClassify = "utility/general";
const MTypeId DoubleToAngle::kNodeID = 0x00130d8a;
const MString EulerMath::kNodeName = "gfUtilEulerMath";
const MString EulerMath::kNodeClassify = "utility/general";
const MTypeId EulerMath::kNodeID = 0x00130d8b;
const MString EulerScalarMath::kNodeName = "gfUtilEulerScalarMath";
const MString EulerScalarMath::kNodeClassify = "utility/general";
const MTypeId EulerScalarMath::kNodeID = 0x00130d8c;
const MString EulerToVector::kNodeName = "gfUtilEulerToVector";
const MString EulerToVector::kNodeClassify = "utility/general";
const MTypeId EulerToVector::kNodeID = 0x00130d8d;
const MString VectorToEuler::kNodeName = "gfUtilVectorToEuler";
const MString VectorToEuler::kNodeClassify = "utility/general";
const MTypeId VectorToEuler::kNodeID =0x00130d8e;
const MString DecomposeRowMatrix::kNodeName = "gfUtilDecompRowMtx";
const MString DecomposeRowMatrix::kNodeClassify = "utility/general";
const MTypeId DecomposeRowMatrix::kNodeID = 0x00130d8f;


MStatus initializePlugin(MObject mobject){
    MStatus status;
    MFnPlugin mPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion, &status);
    status = mPlugin.setName("gfTools");

    REGISTER_LOCATOR_NODE(DebugVector, mPlugin, DebugVectorDrawOverride);
    REGISTER_NODE(VectorAnglePSD, mPlugin);
    REGISTER_NODE(IKVChainSolver, mPlugin);
    REGISTER_NODE(BlendTransform, mPlugin);
    REGISTER_NODE(AimConstraint, mPlugin);
    REGISTER_NODE(ParentConstraint, mPlugin);
    REGISTER_NODE(AngularMath, mPlugin);
    REGISTER_NODE(AngularScalarMath, mPlugin);
    REGISTER_NODE(AngularTrigMath, mPlugin);
    REGISTER_NODE(AngleToDouble, mPlugin);
    REGISTER_NODE(DoubleToAngle, mPlugin);
    REGISTER_NODE(EulerMath, mPlugin);
    REGISTER_NODE(EulerScalarMath, mPlugin);
    REGISTER_NODE(EulerToVector, mPlugin);
    REGISTER_NODE(VectorToEuler, mPlugin);
    REGISTER_NODE(DecomposeRowMatrix, mPlugin);

    return status;
}

MStatus uninitializePlugin(MObject mobject){
    MStatus status;
    MFnPlugin mPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion, &status);

    DEREGISTER_LOCATOR_NODE(DebugVector, mPlugin);
    DEREGISTER_NODE(VectorAnglePSD, mPlugin);
    DEREGISTER_NODE(IKVChainSolver, mPlugin);
    DEREGISTER_NODE(BlendTransform, mPlugin);
    DEREGISTER_NODE(AimConstraint, mPlugin);
    DEREGISTER_NODE(ParentConstraint, mPlugin);
    DEREGISTER_NODE(AngularMath, mPlugin);
    DEREGISTER_NODE(AngularScalarMath, mPlugin);
    DEREGISTER_NODE(AngularTrigMath, mPlugin);
    DEREGISTER_NODE(AngleToDouble, mPlugin);
    DEREGISTER_NODE(DoubleToAngle, mPlugin);
    DEREGISTER_NODE(EulerMath, mPlugin);
    DEREGISTER_NODE(EulerScalarMath, mPlugin);
    DEREGISTER_NODE(EulerToVector, mPlugin);
    DEREGISTER_NODE(VectorToEuler, mPlugin);
    DEREGISTER_NODE(DecomposeRowMatrix, mPlugin);

    return status;
}