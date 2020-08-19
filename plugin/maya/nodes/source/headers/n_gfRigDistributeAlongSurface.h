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
    Distribute objects along a line in surface. The distribution is uniform and based
    on a number of outputs.

Attributes:
    * Input Surface: The input Nurbs Surface shape to be used.
    * Distribute Along: The direction of the distribution line.
    * Displace Tangent: Displace the line tangent along the surface.
    * Always Uniform: Asure that the distribution is always uniform. (Affect performance).
    * Output Transform: The world matrix of each output object.

Todo:
    * NDA

Sources:
    * NDA
*/
#pragma once

#include <cstdint>

#include <maya/MPxNode.h>

#include <maya/MFnTypedAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNurbsSurface.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MDoubleArray.h>
#include <maya/MVector.h>
#include <maya/MMatrix.h>
#include <maya/MGlobal.h>


class DistributeAlongSurface : public MPxNode{
public:
    DistributeAlongSurface();
    virtual ~DistributeAlongSurface();

    virtual MPxNode::SchedulingType schedulingType() const{
        return MPxNode::SchedulingType::kParallel;
    }

    virtual MStatus                 compute(const MPlug& plug, MDataBlock& dataBlock);
    static MStatus                  initialize();
    static void*                    creator();

public:
    const static MString            kNodeName;
    const static MString            kNodeClassify;
    const static MTypeId            kNodeID;

    static MObject                  inSurface;
    static MObject                  inDistributeAlong;
    static MObject                  inDisplace;
    static MObject                  inAlwaysUniform;
    static MObject                  outTransform;
};