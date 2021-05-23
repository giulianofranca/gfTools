/*
Copyright 2020 Giuliano Franca

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Todo:
    * Stretch Mult attributes zeroed causes NaN values on joints.
    * Different Primary Axis return flipped rotation on end joint in hierarchy mode.
*/ 
#pragma once

#include <cmath>
#include <algorithm>

#include <maya/MPxNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MVector.h>
#include <maya/MMatrix.h>
#include <maya/MTransformationMatrix.h>
#include <maya/MMatrixArray.h>
#include <maya/MQuaternion.h>
#include <maya/MEulerRotation.h>

#include <maya/MGlobal.h>
#include <maya/MAngle.h>


class IKSolver : public MPxNode{
public:
    IKSolver();
    ~IKSolver() override;

    // Public Enums
    enum Axis{
        xAxis = 0,
        xAxisNeg = 1,
        yAxis = 2,
        yAxisNeg = 3,
        zAxis = 4,
        zAxisNeg = 5
    };

    // Public Override Methods
    MPxNode::SchedulingType     schedulingType() const override;
    MStatus                     compute(const MPlug& plug,
                                        MDataBlock& dataBlock) override;

    // Public Methods
    MVector     axisEnumToMVector(IKSolver::Axis axis);
    double      clamp(double val, double minVal, double maxVal);

    // Public Static Methods
    static MStatus              initialize();
    static void*                creator();

    // Public Members
    const static MString        kNodeName;
    const static MString        kNodeClassify;
    const static MTypeId        kNodeID;

    // Attributes
    static MObject      inPrimAxis;
    static MObject      inUpAxis;
    static MObject      inFlatMode;
    static MObject      inStretchScale;
    static MObject      inRoot;
    static MObject      inHandle;
    static MObject      inPole;
    static MObject      inRestStartLen;
    static MObject      inRestEndLen;
    static MObject      inStartJntOri;
    static MObject      inMidJntOri;
    static MObject      inEndJntOri;
    static MObject      inStartOffset;
    static MObject      inMidOffset;
    static MObject      inEndOffset;
    static MObject      inParInvMtx;
    static MObject      inSoftness;
    static MObject      inStretch;
    static MObject      inSquash;
    static MObject      inStartStMult;
    static MObject      inEndStMult;
    static MObject      inStartSqMult;
    static MObject      inEndSqMult;
    static MObject      outTranslate;
    static MObject      outRotate;
    static MObject      outScale;
    static MObject      outTransforms;
};