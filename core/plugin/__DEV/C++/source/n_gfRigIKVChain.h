#pragma once

#ifdef _WIN64
#define _USE_MATH_DEFINES
#endif
#include <cmath>
#include <vector>
#include <algorithm>
#include <cstdint>

#include <maya\MPxNode.h>

#include <maya\MFnMatrixAttribute.h>
#include <maya\MFnNumericAttribute.h>
#include <maya\MFnUnitAttribute.h>
#include <maya\MFnEnumAttribute.h>
#include <maya\MMatrix.h>
#include <maya\MVector.h>
#include <maya\MAngle.h>
#include <maya\MEulerRotation.h>
#include <maya\MTransformationMatrix.h>


class IKVChainSolver : MPxNode{
public:
    IKVChainSolver();
    virtual ~IKVChainSolver();

    virtual MPxNode::SchedulingType schedulingType(){
        return MPxNode::SchedulingType::kParallel;
    }

    virtual MStatus                     compute(const MPlug& plug, MDataBlock& dataBlock);
    static MStatus                      initialize();
    static void*                        creator();

public:
    const static MString                kNodeName;
    const static MString                kNodeClassify;
    const static MTypeId                kNodeID;

    static MObject                      inRoot;
    static MObject                      inHandle;
    static MObject                      inUpVector;
    static MObject                      inParInvMtx;
    static MObject                      inJointOrient;
    static MObject                      inPreferredAngle;
    static MObject                      inPvMode;
    static MObject                      inTwist;
    static MObject                      inHierarchyMode;
    static MObject                      inRestLength1;
    static MObject                      inRestLength2;
    static MObject                      inCompressionLimit;
    static MObject                      inSoftness;
    static MObject                      inStretch;
    static MObject                      inClampStretch;
    static MObject                      inClampValue;
    static MObject                      inSquash;
    static MObject                      outChain;
};