#pragma once

#ifdef _WIN64
#define _USE_MATH_DEFINES
#endif
#include <cmath>

#include <vector>
#include <algorithm>
#include <exception>

#include <maya\MPxNode.h>

#include <maya\MFnMatrixAttribute.h>
#include <maya\MFnNumericAttribute.h>
#include <maya\MFnUnitAttribute.h>
#include <maya\MFnEnumAttribute.h>
#include <maya\MMatrix.h>
#include <maya\MAngle.h>
#include <maya\MVector.h>


class IKVChain : public MPxNode {
public:
	IKVChain();
	virtual ~IKVChain();

	virtual MPxNode::SchedulingType schedulingType() {
		return MPxNode::SchedulingType::kParallel;
	}

	virtual MStatus								compute(const MPlug& plug, MDataBlock& dataBlock);
	static MStatus								initialize();
	static void*								creator();
public:
	const static MString						kNODE_NAME;
	const static MString						kNODE_CLASSIFY;
	const static MTypeId						kNODE_ID;

	static MObject								inRoot;
	static MObject								inHandle;
	static MObject								inUpVector;
	static MObject								inPreferredAngle;
	static MObject								inPvMode;
	static MObject								inTwist;
	static MObject								inRestLength1;
	static MObject								inRestLength2;
	static MObject								inCompressionLimit;
	static MObject								inSoft;
	static MObject								inStretch;
	static MObject								inClampStretch;
	static MObject								inClampValue;
	static MObject								inSquash;
	static MObject								outChain;
	static MObject								outStretchFactor;
};