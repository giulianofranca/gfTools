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
    Convert vector to euler rotation.

Attributes:
    * Vector: The vector to be converted to euler rotation.
    * Out Euler: The output euler rotation converted from an vector.

Todo:
    * NDA

Sources:
    * NDA
*/
#pragma once

#include <maya/MPxNode.h>

#include <maya/MFnUnitAttribute.h>
#include <maya/MFnNumericAttribute.h>

#include <maya/MVector.h>
#include <maya/MEulerRotation.h>
#include <maya/MAngle.h>


class VectorToEuler : public MPxNode{
public:
    VectorToEuler();
    virtual ~VectorToEuler();

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

    static MObject                      inVector;
    static MObject                      outEuler;
};