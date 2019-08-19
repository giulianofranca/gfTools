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
	* Go to Windows > Settings / Preferences > Plug - in Manager.
	* Mark this file as loaded.

Requirements:
	Maya 2017 or above.

Todo:
	* gfRigBlendMatrix node.
*/

#include "headers\n_gfDebugPv.h"
#include "headers\n_gfRigBlendTransform.h"
#include "headers\n_gfRigPSD.h"
#include "headers\n_gfRigIKVChain.h"

#include <maya\MFnPlugin.h>

/*
MGlobal::displayInfo() | Print Statement
#pragma warning (disable : 4244)
*/

#define REGISTER_NODE(NODE)					\
	status = fnPlugin.registerNode(			\
		NODE::kNODE_NAME,					\
		NODE::kNODE_ID,						\
		NODE::creator,						\
		NODE::initialize,					\
		MPxNode::kDependNode,				\
		&NODE::kNODE_CLASSIFY				\
	);										\
	CHECK_MSTATUS(status);					\


#define DEREGISTER_NODE(NODE)				\
	status = fnPlugin.deregisterNode(		\
		NODE::kNODE_ID						\
	);										\
	CHECK_MSTATUS(status);					\



const char* kAUTHOR = "Giuliano Franca";
const char* kVERSION = "1.0";
const char* kREQUIRED_API_VERSION = "Any";

const MString PvDebug::kNODE_NAME = "gfDebugPv";
const MString PvDebug::kNODE_CLASSIFY = "utility/general";
const MTypeId PvDebug::kNODE_ID = 0x00130d80;
const MString BlendTransform::kNODE_NAME = "gfRigBlendTransform";
const MString BlendTransform::kNODE_CLASSIFY = "utility/general";
const MTypeId BlendTransform::kNODE_ID = 0x00130d81;
const MString SphericalPSD::kNODE_NAME = "gfRigPSD";
const MString SphericalPSD::kNODE_CLASSIFY = "utility/general";
const MTypeId SphericalPSD::kNODE_ID = 0x00130d83;
const MString IKVChain::kNODE_NAME = "gfRigIKVChain";
const MString IKVChain::kNODE_CLASSIFY = "utility/general";
const MTypeId IKVChain::kNODE_ID = 0x00130d84;



MStatus initializePlugin(MObject obj) {
	MStatus status = MStatus::kFailure;
	MFnPlugin fnPlugin(obj, kAUTHOR, kVERSION, kREQUIRED_API_VERSION, &status);
	status = fnPlugin.setName("gfTools");

	REGISTER_NODE(PvDebug);
	REGISTER_NODE(BlendTransform);
	REGISTER_NODE(SphericalPSD);
	REGISTER_NODE(IKVChain);

	return status;
}

MStatus uninitializePlugin(MObject obj) {
	MStatus status = MStatus::kFailure;
	MFnPlugin fnPlugin(obj, kAUTHOR, kVERSION, kREQUIRED_API_VERSION, &status);

	DEREGISTER_NODE(PvDebug);
	DEREGISTER_NODE(BlendTransform);
	DEREGISTER_NODE(SphericalPSD);
	DEREGISTER_NODE(IKVChain);

	return status;
}