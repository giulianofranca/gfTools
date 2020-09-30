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
    * Target World Matrix: The world matrix of the target object.
    * Target Parent Inverse Matrix: The world inverse matrix of the parent of the target object.
    * Target Joint Orient: The joint orient of the target object.
    * Use Axis as Aim: Use one of the axis of the target object as aim vector.
    * Aim World Matrix: The world matrix of the aim object.
    * Aim Axis: the specific axis of the target object to be used as aim vector.
    * Out Twist: The output twist channel of the target object.

Todo:
    * NDA.

Sources:
    * NDA.
*/
#pragma once

#include <vector>
#include <cstdint>

#include <maya/MPxNode.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MMatrix.h>
#include <maya/MTransformationMatrix.h>
#include <maya/MVector.h>
#include <maya/MEulerRotation.h>
#include <maya/MAngle.h>


class HelperJoint : public MPxNode{
public:
    HelperJoint();
    virtual ~HelperJoint();

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
    
    static MObject                      inSource;
    static MObject                      inSourceParent;
    static MObject                      inParInvMtx;
    static MObject                      inSourceParSca;
    static MObject                      inPositionOffset;
    static MObject                      inRotationOffset;
    static MObject                      inRotAngle;
    static MObject                      inRestAngle;
    static MObject                      inRotInterp;
    static MObject                      inPosMult;
    static MObject                      inNegMult;
    static MObject                      inTargetList;
    static MObject                      outTransform;
};