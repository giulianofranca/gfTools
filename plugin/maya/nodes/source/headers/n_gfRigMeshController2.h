// #include <ctime>

// clock_t startTime = clock();
// double runTime = (double)(clock() - startTime);
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
    Node to visualize vectors in the viewport and vector math operations.
    Draws a simple arrow to represent the vector connected.
    Operates vector addition, subtraction and cross product.

Attributes:
    * Line Width: Control the width of the lines drawed.
    * Color: Color of the lines.
    * Radius: Radius of the arrow.
    * Tip Size: The size of the tip of the arrow.
    * Subdivisions: The number of subdivisions of the arrow.
    * XRay: Draw the vector in top of other objects.
    * Operation: The math operation. (No operation will return Vector 1 attribute)
    * Vector 1: The first vector of the operation.
    * Vector 2: The second vector of the operation.
    * Normalize: Normalize the output vector.
    * OutVector: The result vector of the operation.

Todo:
    * RGBA Support.

Sources:
    * https://gitlab.com/gmendieta/mayaplugins-custom_locator/tree/master/src
    * https://www.opengl.org/archives/resources/code/samples/redbook/lines.c
    * https://groups.google.com/forum/#!topic/python_inside_maya/vGIVwWt0JLQ

*/
#pragma once

#include <ctime>

#include <maya/MPxSurfaceShape.h>
#include <maya/MPxSurfaceShapeUI.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/MPointArray.h>


class MeshController : public MPxSurfaceShape{
public:
	MeshController();
	virtual ~MeshController();

    virtual bool                        isBounded() const;
    virtual MBoundingBox                boundingBox() const;

    static MStatus                      initialize();
    static void                         *creator();

public:
    void                                points(MPointArray &points) const;
    static MPointArray                  basicCurvePoints;

public:
    const static MString                kNodeName;
    const static MTypeId                kNodeID;
    const static MString                kNodeClassify;
    const static MString                kNodeRegistrantID;

    static MObject                      inColor;
};


class MeshControllerUI : public MPxSurfaceShapeUI{
public:
    MeshControllerUI();
    virtual ~MeshControllerUI();

    static void                         *creator();

    virtual void                        getDrawRequests(const MDrawInfo &info,
                                                        bool objectAndActiveOnly,
                                                        MDrawRequestQueue &requests);
    virtual void                        draw(const MDrawRequest &request, M3dView &view) const;
    virtual bool                        select(MSelectInfo &selectInfo, 
                                               MSelectionList &selectionList,
                                               MPointArray &worldSpaceSelectPts) const;

public:
    void                                drawWireframe(M3dView &view) const;
};