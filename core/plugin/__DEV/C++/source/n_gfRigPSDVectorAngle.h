#pragma once

#ifdef _WIN64
#define _USE_MATH_DEFINES
#endif
#include <cmath>

#include <algorithm>
#include <vector>
#include <cstdint>

#include <maya/MPxNode.h>

#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MRampAttribute.h>
#include <maya/MFloatArray.h>
#include <maya/MIntArray.h>
#include <maya/MFloatMatrix.h>
#include <maya/MFloatVector.h>


class VectorAnglePSD : MPxNode{
public:
    VectorAnglePSD();
    virtual ~VectorAnglePSD();

    virtual MPxNode::SchedulingType schedulingType(){
        return MPxNode::SchedulingType::kParallel;
    }

    virtual MStatus                     compute(const MPlug& plug, MDataBlock& dataBlock);
    static MStatus                      initialize();
    static void*                        creator();
    virtual void                        postConstructor();

public:
    const static MString                kNodeName;
    const static MString                kNodeClassify;
    const static MTypeId                kNodeID;

    static MObject                      inBase;
    static MObject                      inSource;
    static MObject                      inTarget;
    static MObject                      inTargetEnvelope;
    static MObject                      inTargetFalloff;
    static MObject                      inRampWeights;
    static MObject                      outWeights;
};