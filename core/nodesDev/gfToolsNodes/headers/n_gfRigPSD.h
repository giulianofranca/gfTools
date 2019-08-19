#pragma once

#ifdef _WIN64
#define _USE_MATH_DEFINES
#endif
#include <cmath>

#include <vector>
#include <algorithm>

#include <maya\MPxNode.h>

#include <maya\MFnNumericAttribute.h>
#include <maya\MFnMatrixAttribute.h>
#include <maya\MMatrix.h>
#include <maya\MTransformationMatrix.h>
#include <maya\MVector.h>




class SphericalPSD : public MPxNode {
public:
	SphericalPSD();
	virtual ~SphericalPSD();

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

	static MObject								inBase;
	static MObject								inPose;
	static MObject								inTarget;
	static MObject								inTargetEnvelope;
	static MObject								inTargetFalloff;
	static MObject								outWeight;
};