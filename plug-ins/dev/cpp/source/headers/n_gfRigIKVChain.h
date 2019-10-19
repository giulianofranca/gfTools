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
    IK Solver to VChain type of rig. Can be used to replace the default Maya
    IKRPSolver with the plus of some cartoony options.

Attributes:
    * Root: The world matrix of the root object.
    * Handle: The world matrix of the handle object.
    * Up Vector: The world matrix of the up vector object.
    * Parent Inverse Matrix: The world inverse matrix of the parent of the output chain.
    * Joint Orient: The array of joint orient sorted by output.
    * Preferred Angle: The preferred angle to be used to calculate the automatic pole vector.
    * Pv Mode: The type of calculation of the pole vector.
    * Twist: Twist the pole vector in automatic mode.
    * Hierarchy Mode: Solve IK in hierarchy mode. (Used by joint chains.)
    * Rest Length 1: The length of the first object.
    * Rest Length 2: The length of the second object.
    * Compression Limit: Limit compression of the solver.
    * Softness: Soft the solver to avoid pops in pole vector.
    * Snap Up Vector: Snap the pole vector to the snap object.
    * Snap Obj: The world matrix of the snap object.
    * Stretch: Enable stretch of the output chain.
    * Clamp Stretch: Clamp the stretch at certain value.
    * Clamp Value: Clamp value of the stretch clamp.
    * Squash: Enable automatic squash of the output chain.
    * Out Chain: The output matrices of the output chain.

Todo:
    * Create and develop the stretchMult attr.
    * Create and develop the squashMult attr.
    * Create and develop the slidePv attr.

Sources:
    * https://www.desmos.com/calculator/wthlznq4aj
*/
#pragma once

#ifdef _WIN64
#define _USE_MATH_DEFINES
#endif
#include <cmath>
#include <vector>
#include <algorithm>
#include <cstdint>

#include <maya/MPxNode.h>

#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MAngle.h>
#include <maya/MEulerRotation.h>
#include <maya/MTransformationMatrix.h>


class IKVChainSolver : public MPxNode{
public:
    IKVChainSolver();
    virtual ~IKVChainSolver();

    virtual MPxNode::SchedulingType schedulingType() const{
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
    static MObject                      inSnapUpVector;
    static MObject                      inSnapObj;
    static MObject                      inStretch;
    static MObject                      inClampStretch;
    static MObject                      inClampValue;
    static MObject                      inSquash;
    static MObject                      outChain;
};