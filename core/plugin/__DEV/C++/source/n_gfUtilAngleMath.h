#pragma once

#include <algorithm>

#include <maya/MPxNode.h>

#include <maya/MFnEnumAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MAngle.h>


class AngularMath : MPxNode{
public:
    AngularMath();
    virtual ~AngularMath();

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

    static MObject                      inAngle1;
    static MObject                      inAngle2;
    static MObject                      inOperation;
    static MObject                      outAngle;
};