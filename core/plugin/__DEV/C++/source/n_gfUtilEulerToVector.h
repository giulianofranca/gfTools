#pragma once

#include <maya/MPxNode.h>

#include <maya/MFnUnitAttribute.h>
#include <maya/MFnNumericAttribute.h>

#include <maya/MVector.h>
#include <maya/MEulerRotation.h>
#include <maya/MAngle.h>


class EulerToVector : MPxNode{
public:
    EulerToVector();
    virtual ~EulerToVector();

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

    static MObject                      inEuler;
    static MObject                      outVector;
};