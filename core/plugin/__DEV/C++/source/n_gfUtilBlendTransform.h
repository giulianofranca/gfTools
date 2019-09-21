#pragma once

#include <vector>
#include <algorithm>
#include <cstdint>

#include <maya\MPxNode.h>

#include <maya\MFnNumericAttribute.h>
#include <maya\MFnUnitAttribute.h>
#include <maya\MFnCompoundAttribute.h>
#include <maya\MFnEnumAttribute.h>
#include <maya\MFloatVector.h>
#include <maya\MVector.h>
#include <maya\MEulerRotation.h>
#include <maya\MQuaternion.h>

struct VisibilityData{
    bool visibility;
    bool reverseVisibility;
};

class BlendTransform : MPxNode {
public:
    BlendTransform();
    virtual ~BlendTransform();

    virtual MPxNode::SchedulingType schedulingType(){
        return MPxNode::SchedulingType::kParallel;
    }

    virtual MStatus                     compute(const MPlug& plug, MDataBlock& dataBlock);
    static MStatus                      initialize();
    static void*                        creator();

    static VisibilityData               visibilityCalculation(float blender);
    static short                        checkRotateOrderArrayHandle(MArrayDataHandle& arrayHandle, uint32_t iterValue);
    static MEulerRotation               createMEulerRotation(MVector& value, short rotOrder);
    static void                         reorderMEulerRotation(MEulerRotation& euler, short rotOrder);

public:
    const static MString                kNodeName;
    const static MString                kNodeClassify;
    const static MTypeId                kNodeID;

    static MObject                      inBlender;
    static MObject                      inRotInterp;
    static MObject                      inTrans1;
    static MObject                      inRot1;
    static MObject                      inSca1;
    static MObject                      inRot1Order;
    static MObject                      inTransform1;
    static MObject                      inTrans2;
    static MObject                      inRot2;
    static MObject                      inSca2;
    static MObject                      inRot2Order;
    static MObject                      inTransform2;
    static MObject                      inOutRotOrder;
    static MObject                      outTrans;
    static MObject                      outRot;
    static MObject                      outSca;
    static MObject                      outVis;
    static MObject                      outRevVis;
};