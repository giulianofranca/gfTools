#pragma once

#include <maya\MPxNode.h>

#include <maya\MFnEnumAttribute.h>
#include <maya\MFnUnitAttribute.h>
#include <maya\MFnNumericAttribute.h>

#include <maya\MVector.h>
#include <maya\MEulerRotation.h>
#include <maya\MAngle.h>


class EulerScalarMath : MPxNode{
public:
    EulerScalarMath();
    virtual ~EulerScalarMath();

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
    static MObject                      inEuler;
    static MObject                      inEulerRotOrder;
    static MObject                      inScalar;
    static MObject                      inResRotOrder;
    static MObject                      outEuler;
};