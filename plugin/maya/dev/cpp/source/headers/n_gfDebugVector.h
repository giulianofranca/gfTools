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

*/
#pragma once

#ifdef _WIN64
#define _USE_MATH_DEFINES
#endif
#include <cmath>
#include <assert.h>

#include <maya/MPxLocatorNode.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MGL.h>
#include <maya/M3dView.h>
#include <maya/MPlug.h>
#include <maya/MVector.h>
#include <maya/MFloatVector.h>
#include <maya/MFloatMatrix.h>
#include <maya/MMatrix.h>
#include <maya/MColor.h>
#include <maya/MDistance.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MGlobal.h>

#include <maya/MDrawRegistry.h>
#include <maya/MPxDrawOverride.h>
#include <maya/MUserData.h>
#include <maya/MDrawContext.h>
#include <maya/MHWGeometryUtilities.h>
#include <maya/MPointArray.h>
#include <maya/MPoint.h>
#include <maya/MEventMessage.h>

using namespace std;


class DebugVector : public MPxLocatorNode{
public:
	DebugVector();
	virtual ~DebugVector();

    virtual void                        postConstructor();
    virtual MStatus   		            compute(const MPlug& plug, MDataBlock& data);

	virtual void                        draw(M3dView & view, const MDagPath & path,
								             M3dView::DisplayStyle style,
								             M3dView::DisplayStatus status);

	virtual bool                        isBounded() const;
	virtual MBoundingBox                boundingBox() const;

	static  MStatus                     initialize();
    static  void*                       creator();

    // drawArrow in Viewport 1.0
    static void                         drawArrow(MFloatVector& startPnt, MFloatVector& endPnt, 
                                                  float size, float radius, int subd, 
                                                  float lineW);
    // drawArrow in Viewport 2.0
    static void                         drawArrow(MFloatVector& startPnt, MFloatVector& endPnt, 
                                                  float size, float radius, int subd, 
                                                  MPointArray& lineList);

public:
    const static MString                kNodeName;
	const static MTypeId		        kNodeID;
	const static MString		        kNodeClassify;
	const static MString		        kNodeRegistrantID;

    static MObject                      inLineWidth;
    static MObject                      inColor;
    static MObject                      inRadius;
    static MObject                      inTipSize;
    static MObject                      inSubdivisions;
    static MObject                      inXRay;
    static MObject                      inDashed;
    static MObject                      inOperation;
    static MObject                      inVec1;
    static MObject                      inVec2;
    static MObject                      inNormalize;
    static MObject                      outVector;

    const static MColor                 kActiveColor;
    const static MColor                 kLeadColor;
};


class DebugVectorData : public MUserData{
public:
	DebugVectorData() : MUserData(false) {} // don't delete after draw
	virtual ~DebugVectorData() {}

    MColor                              fDormantColor;
    MColor                              fActiveColor;
    MColor                              fLeadColor;
    MPointArray                         fLineList;
    float                               fLineWidth;
    float                               fTipSize;
    int                                 fSubd;
    float                               fRadius;
    bool                                fXray;
    bool                                fDashed;
    short                               fOperation;
};


class DebugVectorDrawOverride : public MHWRender::MPxDrawOverride{
private:
    DebugVectorDrawOverride(const MObject& obj);

public:
    virtual ~DebugVectorDrawOverride();

    virtual MHWRender::DrawAPI          supportedDrawAPIs() const{
        return (MHWRender::kOpenGL | MHWRender::kDirectX11 | MHWRender::kOpenGLCoreProfile);
    }

    static MHWRender::MPxDrawOverride*  creator(const MObject& obj);
    static void                         draw(const MHWRender::MDrawContext& context, 
                                             const MUserData* userData) {}

	virtual bool                        isBounded(const MDagPath& objPath,
		                                          const MDagPath& cameraPath) const;
	virtual MBoundingBox                boundingBox(const MDagPath& objPath,
		                                            const MDagPath& cameraPath) const;

	virtual MUserData*                  prepareForDraw(const MDagPath& objPath,
		                                               const MDagPath& cameraPath,
		                                               const MHWRender::MFrameContext& frameContext,
		                                               MUserData* oldData);

	virtual bool                        hasUIDrawables() const { return true; }
	virtual void                        addUIDrawables(const MDagPath& objPath,
		                                               MHWRender::MUIDrawManager& drawManager,
		                                               const MHWRender::MFrameContext& frameContext,
		                                               const MUserData* data);
};