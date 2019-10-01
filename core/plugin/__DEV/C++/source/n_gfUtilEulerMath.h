#pragma once

#include <maya\MPxNode.h>

#include <maya\MFnEnumAttribute.h>
#include <maya\MFnUnitAttribute.h>
#include <maya\MFnNumericAttribute.h>

#include <maya\MVector.h>
#include <maya\MEulerRotation.h>


class EulerMath : MPxNode{
public:
    EulerMath();
    virtual ~EulerMath();

    virtual MPxNode::SchedulingType schedulingType(){
        return MPxNode::SchedulingType::kParallel;
    }

    virtual MStatus                     compute(const MPlug& plug, MDataBlock& dataBlock);
    static MStatus                      initialize();
    static void*                        creator();

    static MEulerRotation               createMEulerRotation(MVector& value, short rotOrder);
    static void                         reorderMEulerRotation(MEulerRotation& euler, short rotOrder);
public:
    const static MString                kNodeName;
    const static MString                kNodeClassify;
    const static MTypeId                kNodeID;

    static MObject                      inOperation;
    static MObject                      inEuler1;
    static MObject                      inEuler1RotOrder;
    static MObject                      inEuler2;
    static MObject                      inEuler2RotOrder;
    static MObject                      inResRotOrder;
    static MObject                      outEuler;
};