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
    Calculate weights based on a pose. The weights are calculated by the angle between
    world position of objects.

Attributes:
    * Base: The base world matrix of the pose.
    * Source: The tip world matrix of the pose.
    * Target: The list of world matrix of the target objects.
    * Target Envelope: The list of envelope of the input targets.
    * Target Falloff: The rest angle between the target and the source.
    * Out Weights: The output list of the weights.

Todo:
    * NDA

Sources:
    * https://www.desmos.com/calculator/nfggjvzpkn
*/
#pragma once

#ifdef _WIN64
#define _USE_MATH_DEFINES
#endif
#include <cmath>

#include <algorithm>
#include <vector>
#include <cstdint>

#include <maya/MPxNode.h>

#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MRampAttribute.h>
#include <maya/MFloatArray.h>
#include <maya/MIntArray.h>
#include <maya/MFloatMatrix.h>
#include <maya/MFloatVector.h>


class VectorAnglePSD : MPxNode{
public:
    VectorAnglePSD();
    virtual ~VectorAnglePSD();

    virtual MPxNode::SchedulingType schedulingType(){
        return MPxNode::SchedulingType::kParallel;
    }

    virtual MStatus                     compute(const MPlug& plug, MDataBlock& dataBlock);
    static MStatus                      initialize();
    static void*                        creator();
    virtual void                        postConstructor();

public:
    const static MString                kNodeName;
    const static MString                kNodeClassify;
    const static MTypeId                kNodeID;

    static MObject                      inBase;
    static MObject                      inSource;
    static MObject                      inTarget;
    static MObject                      inTargetEnvelope;
    static MObject                      inTargetFalloff;
    static MObject                      inRampWeights;
    static MObject                      outWeights;
};