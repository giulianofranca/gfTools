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
    * In gfTools API MayaUtils class make makeInputAttr() and makeOutputAttr() to use in nodes.

Sources:
    * NDA
*/
#pragma once 

#include <cmath>

#include <maya/MPxNode.h>

#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MRampAttribute.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MFloatArray.h>

#include <maya/MGlobal.h>




class PoseReader : public MPxNode{
public:
    PoseReader();
    ~PoseReader() override;

    // Public Override Methods
    MPxNode::SchedulingType     schedulingType() const override;
    void                        postConstructor() override;
    MStatus                     compute(const MPlug& plug,
                                        MDataBlock& dataBlock) override;

    // Public Static Methods
    static MStatus      initialize();
    static void*        creator();

    // Public Methods
    void    degToRad(float& deg);

    // Public Members
    const static MString    kNodeName;
    const static MString    kNodeClassify;
    const static MTypeId    kNodeID;

    // Attributes
    static MObject      inMode;
    static MObject      inTarget;
    static MObject      inTargetAxis;
    static MObject      inVecAngInterp;
    static MObject      inPose;
    static MObject      inEnvelope;
    static MObject      inPosition;
    static MObject      inStartAngle;
    static MObject      outWeight;

    // Public Enums
    enum Axis{
        xAxis = 0,
        yAxis = 1,
        zAxis = 2
    };
    enum Mode{
        vectorAngle = 0,
        rbf = 1
    };
};