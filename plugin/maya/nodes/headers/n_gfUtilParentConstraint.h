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
    Custom parent contraint. Parent one object to another. Can be used as point, orient
    or scale constraint.

Attributes:
    * Contraint Joint Orient: The joint orient of the constrainted object.
    * Constraint Rotate Order: The rotate order of the constrainted object.
    * Constraint Parent Inverse Matrix: The world inverse matrix of the parent of the constrainted object.
    * Constraint Parent Scale: The scale of the parent of the constrainted object.
    * Target World Matrix: The world matrix of the parent.
    * Target Offset: The offset matrix of the constraint object in this parent world matrix.
    * Target Weight: The weight of this target matrix.
    * Constraint Translate: The output translation for the constrainted object.
    * Constraint Rotate: The output rotate for the constrainted object.
    * Constraint Scale: The output scale for the constrainted object.

Todo:
    * NDA

Sources:
    * NDA
*/
#pragma once

#include <cstdint>

#include <maya/MPxNode.h>

#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MTransformationMatrix.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MEulerRotation.h>
#include <maya/MQuaternion.h>


class ParentConstraint : public MPxNode{
public:
    ParentConstraint();
    virtual ~ParentConstraint();

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

    static MObject                      inConstraintJntOri;
    static MObject                      inConstraintRotOrder;
    static MObject                      inConstraintParInvMtx;
    static MObject                      inConstraintParSca;
    static MObject                      inTargetWorldMatrix;
    static MObject                      inTargetOffset;
    static MObject                      inTargetWeight;
    static MObject                      inTargetList;
    static MObject                      outConstTrans;
    static MObject                      outConstRot;
    static MObject                      outConstSca;
};