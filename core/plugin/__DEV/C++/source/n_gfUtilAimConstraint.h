#pragma once

#include <maya\MPxNode.h>

#include <maya\MFnEnumAttribute.h>
#include <maya\MFnMatrixAttribute.h>
#include <maya\MFnNumericAttribute.h>
#include <maya\MFnUnitAttribute.h>
#include <maya\MFloatMatrix.h>
#include <maya\MFloatVector.h>
#include <maya\MMatrix.h>
#include <maya\MTransformationMatrix.h>
#include <maya\MVector.h>
#include <maya\MQuaternion.h>
#include <maya\MEulerRotation.h>


class AimConstraint : MPxNode{
public:
    AimConstraint();
    virtual ~AimConstraint();

    virtual MPxNode::SchedulingType schedulingType(){
        return MPxNode::SchedulingType::kParallel;
    }

    virtual MStatus                     compute(const MPlug& plug, MDataBlock& bataBlock);
    static MStatus                      initialize();
    static void*                        creator();

public:
    const static MString                kNodeName;
    const static MString                kNodeClassify;
    const static MTypeId                kNodeID;

    static MObject                      inUpVecType;
    static MObject                      inTarget;
    static MObject                      inWorldUp;
    static MObject                      inUpObj;
    static MObject                      inPivot;
    static MObject                      outConstraint;
};