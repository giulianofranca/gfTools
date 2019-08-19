#pragma once

#include <cmath>

#include <maya\MPxNode.h>

#include <maya\MFnMatrixAttribute.h>
#include <maya\MFnNumericAttribute.h>
#include <maya\MFnUnitAttribute.h>
#include <maya\MFloatVector.h>
#include <maya\MFloatMatrix.h>
#include <maya\MMatrix.h>
#include <maya\MTransformationMatrix.h>
#include <maya\MEulerRotation.h>
#include <maya\MAngle.h>


struct LocationData {
	MFloatVector translate;
	MEulerRotation rotate;
};


class PvDebug : public MPxNode {
public:
	PvDebug();
	virtual ~PvDebug();

	virtual MPxNode::SchedulingType schedulingType() {
		return MPxNode::SchedulingType::kParallel;
	}

	virtual MStatus								compute(const MPlug& plug, MDataBlock& dataBlock);
	static MStatus								initialize();
	static void*								creator();

	static LocationData							retriveLocation(MFloatVector& startPos, MFloatVector& midPos, MFloatVector& endPos, float dist);
	static MFloatVector							pvLocationRatioColor(MFloatVector& startPos, MFloatVector& midPos, MFloatVector& pvPos);
	static MFloatVector							convertHSVtoRGB(float hValue, float sValue, float vValue);
	static float								fit(float value, float oldMin, float oldMax, float newMin, float newMax);
public:
	const static MString						kNODE_NAME;
	const static MString						kNODE_CLASSIFY;
	const static MTypeId						kNODE_ID;

	static MObject								inStart;
	static MObject								inMid;
	static MObject								inEnd;
	static MObject								inDistMult;
	static MObject								outPos;
	static MObject								outRot;
	static MObject								outRotX;
	static MObject								outRotY;
	static MObject								outRotZ;
	static MObject								outResult;
};