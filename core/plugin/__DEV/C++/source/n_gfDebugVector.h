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

// Viewport 2.0 includes
#include <maya/MDrawRegistry.h>
#include <maya/MPxDrawOverride.h>
#include <maya/MUserData.h>
#include <maya/MDrawContext.h>
#include <maya/MHWGeometryUtilities.h>
#include <maya/MPointArray.h>
#include <maya/MPoint.h>
#include <maya/MEventMessage.h>


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

private:
	static void                         OnModelEditorChanged(void *clientData);

	DebugVector*                        fDebugVector;
	MCallbackId                         fModelEditorChangedCbId;
};