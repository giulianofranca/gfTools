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
    Basic euler rotation operations. No operation value returns the first euler.
    Support addition, subtraction and multiply.

Attributes:
    * Operation: The math operation. Can be add, subtract or multiply.
    * Euler 1: The first euler rotation of the operation.
    * Euler 1 Rotate Order: The rotation order of the first euler rotation.
    * Euler 2: The second euler rotation of the operation.
    * Euler 2 Rotate Order: The rotation order of the second euler rotation.
    * Rotate Order Out Euler: The rotation order of the output euler rotation.
    * Out Euler: The output euler rotation.

Todo:
    * NDA

Sources:
    * NDA
*/
#pragma once

#include <maya/MPxNode.h>

#include <maya/MFnEnumAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnNumericAttribute.h>

#include <maya/MEulerRotation.h>


class EulerMath : public MPxNode{
public:
    EulerMath();
    virtual ~EulerMath();

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

    static MObject                      inOperation;
    static MObject                      inEuler1;
    static MObject                      inEuler1X;
    static MObject                      inEuler1Y;
    static MObject                      inEuler1Z;
    static MObject                      inEuler1RotOrder;
    static MObject                      inEuler2;
    static MObject                      inEuler2X;
    static MObject                      inEuler2Y;
    static MObject                      inEuler2Z;
    static MObject                      inEuler2RotOrder;
    static MObject                      inResRotOrder;
    static MObject                      outEuler;
    static MObject                      outEulerX;
    static MObject                      outEulerY;
    static MObject                      outEulerZ;
};