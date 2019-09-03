#pragma once

#include <vector>
#include <algorithm>
#include <cstdint>

#include <maya\MPxNode.h>

#include <maya\MFnMatrixAttribute.h>
#include <maya\MFnNumericAttribute.h>
#include <maya\MMatrix.h>


class ParentConstraint : MPxNode{
public:
    ParentConstraint();
    virtual ~ParentConstraint();

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

    static MObject                      inTarget;
    static MObject                      inOffset;
    static MObject                      inWeight;
    static MObject                      outConstraint;
};