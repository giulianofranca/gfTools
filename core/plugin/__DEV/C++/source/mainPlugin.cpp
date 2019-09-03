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
#include "n_gfUtilBlendTransform.h"
#include "n_gfUtilAimConstraint.h"
#include "n_gfUtilParentConstraint.h"
#include "n_gfUtilAngleMath.h"
#include "n_gfUtilAngleScalarMath.h"
#include "n_gfUtilAngleTrigMath.h"
#include "n_gfUtilAngleToDouble.h"
#include "n_gfUtilDoubleToAngle.h"

#include <maya\MFnPlugin.h>
#include <maya\MString.h>
#include <maya\MTypeId.h>


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


const char* kAuthor = "Giuliano Franca";
const char* kVersion = "1.0 Pro";
const char* kRequiredAPIVersion = "Any";

// gfDebug
// gfRig
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


MStatus initializePlugin(MObject mobject){
    MStatus status;
    MFnPlugin mPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion, &status);
    status = mPlugin.setName("gfTools");

    REGISTER_NODE(BlendTransform, mPlugin);
    REGISTER_NODE(AimConstraint, mPlugin);
    REGISTER_NODE(ParentConstraint, mPlugin);
    REGISTER_NODE(AngularMath, mPlugin);
    REGISTER_NODE(AngularScalarMath, mPlugin);
    REGISTER_NODE(AngularTrigMath, mPlugin);
    REGISTER_NODE(AngleToDouble, mPlugin);
    REGISTER_NODE(DoubleToAngle, mPlugin);

    return status;
}

MStatus uninitializePlugin(MObject mobject){
    MStatus status;
    MFnPlugin mPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion, &status);

    DEREGISTER_NODE(BlendTransform, mPlugin);
    DEREGISTER_NODE(AimConstraint, mPlugin);
    DEREGISTER_NODE(ParentConstraint, mPlugin);
    DEREGISTER_NODE(AngularMath, mPlugin);
    DEREGISTER_NODE(AngularScalarMath, mPlugin);
    DEREGISTER_NODE(AngularTrigMath, mPlugin);
    DEREGISTER_NODE(AngleToDouble, mPlugin);
    DEREGISTER_NODE(DoubleToAngle, mPlugin);

    return status;
}