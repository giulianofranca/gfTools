/*
Copyright (c) 2019 Giuliano França

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

====================================================================================================

How to use:
    * Copy the plugin file to the MAYA_PLUG_IN_PATH.
    * To find MAYA_PLUG_IN_PATH paste this command in a Python tab:
        import os; os.environ["MAYA_PLUG_IN_PATH"].split(";")
    * In Maya, go to Windows > Settings/Preferences > Plug-in Manager.
    * Find the plugin file and import it. Can be:
        Windows: gfTools.mll
        OSX: gfTools.bundle
        Linux: gfTools.so

Requirements:
    * Maya 2017 or above.

Description:
    Blend transformations (SRT) between an array of objects.

Attributes:
    * Blender: The weight value of the blend.
    * Rotation Interpolation: The type of the rotation interpolation. Can be Euler LERP or Quaternion SLERP.
    * Translate 1: The translate value of the first object to be blended.
    * Rotate 1: The rotate value of the first object to be blended.
    * Scale 1: The scale value of the first object to be blended.
    * Rotate Order 1: The rotation order of the first object to be blended.
    * Translate 2: The translate value of the second object to be blended.
    * Rotate 2: The rotate value of the second object to be blended.
    * Scale 2: The scale value of the second object to be blended.
    * Rotate Order 2: The rotation order of the second object to be blended.
    * Out Rotate Order: The rotation order of the output object.
    * Out Translate: The translate value of the output object.
    * Out Rotate: The rotate value of the output object.
    * Out Scale: The scale value of the output object.
    * Out Visibility: Boolean visibility based on the blender value.
    * Out Reverse Visibility: The reverse value of the out visibility.

Todo:
    * NDA

Sources:
    * NDA
*/
#pragma once

#include <vector>
#include <algorithm>
#include <cstdint>

#include <maya/MPxNode.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFloatVector.h>
#include <maya/MVector.h>
#include <maya/MEulerRotation.h>
#include <maya/MQuaternion.h>

struct VisibilityData{
    bool visibility;
    bool reverseVisibility;
};

class BlendTransform : public MPxNode {
public:
    BlendTransform();
    virtual ~BlendTransform();

    virtual MPxNode::SchedulingType schedulingType() const{
        return MPxNode::SchedulingType::kParallel;
    }

    virtual MStatus                     compute(const MPlug& plug, MDataBlock& dataBlock);
    static MStatus                      initialize();
    static void*                        creator();

    static VisibilityData               visibilityCalculation(float blender);
    static short                        checkRotateOrderArrayHandle(MArrayDataHandle& arrayHandle, uint32_t iterValue);

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