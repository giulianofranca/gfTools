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
*/
#pragma once

#include <cmath>

#include <maya/MPxNode.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MAngle.h>


class AngleTrig : public MPxNode{
public:
    AngleTrig();
    ~AngleTrig() override;

    // Public Override Methods
    MPxNode::SchedulingType     schedulingType() const override;
    MStatus                     compute(const MPlug& plug,
                                                MDataBlock& dataBlock) override;

    // Public Static Methods
    static MStatus              initialize();
    static void*                creator();

    // Public Members
    const static MString        kNodeName;
    const static MString        kNodeClassify;
    const static MTypeId        kNodeID;

    // Attributes
    static MObject              inAngle1;
    static MObject              inAngle2;
    static MObject              inOperation;
    static MObject              outAngle;

    // Public Enums
    enum Operation{
        noOp = 0,
        cosine = 1,
        sine = 2,
        tangent = 3,
        arccos = 4,
        arcsin = 5,
        arctan = 6,
        arctan2 = 7
    };
};
