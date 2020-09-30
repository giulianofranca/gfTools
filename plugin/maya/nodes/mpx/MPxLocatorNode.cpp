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
    * Copy and paste this file in the MAYA_PLUG_IN_PATH.
    * To find MAYA_PLUG_IN_PATH paste this command in a Python tab on script editor:
        import os; os.environ["MAYA_PLUG_IN_PATH"].split(";")
    * In Maya, go to Windows > Settings/Preferences > Plug-in Manager.
    * Find this file and import it.

Requirements:
    * Maya 2017 or above.

Todo:
    * NDA

Sources:
    * NDA
*/
#pragma once

#include <maya/MPxLocatorNode.h>
#include <maya/MString.h>
#include <maya/MTypeId.h>
#include <maya/MFnPlugin.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/M3dView.h>
#include <maya/MPlug.h>
#include <maya/MVector.h>
#include <maya/MColor.h>
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


class TestLocator : public MPxLocatorNode{
public:
    TestLocator();
    virtual ~TestLocator();

    virtual void                        postConstructor();
    virtual MStatus                     compute(const MPlug& plug, MDataBlock& dataBlock);

    virtual void                        draw(M3dView& view, const MDagPath& path,
                                             M3dView::DisplayStyle style,
                                             M3dView::DisplayStatus status);

    virtual bool                        isBounded() const;
    virtual MBoundingBox                boundingBox() const;

    static MStatus                      initialize();
    static void*                        creator();

public:
    const static MString                kNodeName;
	const static MTypeId		        kNodeID;
	const static MString		        kNodeClassify;
	const static MString		        kNodeRegistrantID;

    static MObject                      inSize;
    static MObject                      inAttr;
    static MObject                      outAttr;
};


// Configure a input attribute.
#define INPUT_ATTR(FNATTR)		\
	FNATTR.setWritable(true);	\
	FNATTR.setReadable(true);	\
	FNATTR.setStorable(true);	\
	FNATTR.setKeyable(true);	\

// Configure a output attribute.
#define OUTPUT_ATTR(FNATTR)		\
	FNATTR.setWritable(false);	\
	FNATTR.setReadable(true);	\
	FNATTR.setStorable(false);	\
	FNATTR.setKeyable(false);	\


// Constructor.
TestLocator::TestLocator() {}

// Destructor.
TestLocator::~TestLocator() {}

MObject TestLocator::inSize;
MObject TestLocator::inAttr;
MObject TestLocator::outAttr;


void TestLocator::postConstructor(){
    // Post Constructor.
    MObject thisMob = thisMObject();
    MFnDependencyNode(thisMob).setName(kNodeName + "Shape#");
}

void* TestLocator::creator(){
    // Maya creator function.
    return new TestLocator();
}

MStatus TestLocator::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to TestLocator class. Instances of TestLocator will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnNumericAttribute nAttr;

    inSize = nAttr.create("size", "size", MFnNumericData::kDouble, 1.0, &status);
    INPUT_ATTR(nAttr);

    inAttr = nAttr.createPoint("inAttr", "inAttr", &status);
    INPUT_ATTR(nAttr);

    outAttr = nAttr.createPoint("outAttr", "outAttr", &status);
    OUTPUT_ATTR(nAttr);

    addAttribute(inSize);
    addAttribute(inAttr);
    addAttribute(outAttr);
    attributeAffects(inAttr, outAttr);

    return status;
}

MStatus TestLocator::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug == outAttr){
        MVector inAttrValue = dataBlock.inputValue(inAttr).asVector();

        MDataHandle outAttrHandle = dataBlock.outputValue(outAttr);
        outAttrHandle.set3Float(inAttrValue.x, inAttrValue.y, inAttrValue.z);
        outAttrHandle.setClean();
    }

    return MStatus::kSuccess;
}

void TestLocator::draw(M3dView & view, const MDagPath &,
					   M3dView::DisplayStyle style,
					   M3dView::DisplayStatus status){
	/*
    Draw custom geometry in the viewport using OpenGL calls.
        * view [M3dView] is a 3D view that is being drawn into.
        * path [MDagPath] to the parent (transform node) of this locator in the DAG.  To obtain the locator shape node,
            use MDagPath::extendToShape() if there is only one shape node under the transform or
            MDagPath::extendToShapeDirectlyBelow(unsigned int index) with the shape index if there are multiple
            shapes under the transform.
        * style [M3dView.DisplayStyle] is the style to draw object in.
        * status [M3dView.DisplayStatus] is the selection status of the object.
    */
    MObject thisMob = thisMObject();
    double size = MPlug(thisMob, inSize).asDouble();

    view.beginGL();

    glPushAttrib(GL_CURRENT_BIT);
    glDisable(GL_CULL_FACE);

    if (status == M3dView::kActive)
        glColor3f(0.3, 1.0, 1.0);
    else if (status == M3dView::kLead)
        glColor3f(1.0, 1.0, 1.0);
    else if (status == M3dView::kDormant)
        glColor3f(1.0, 1.0, 0.0);

    MVector vPoint1 = MVector(1.0, 0.0, -1.0) * size;
    MVector vPoint2 = MVector(-1.0, 0.0, -1.0) * size;
    MVector vPoint3 = MVector(-1.0, 0.0, 1.0) * size;
    MVector vPoint4 = MVector(1.0, 0.0, 1.0) * size;

    glBegin(GL_QUADS);
    glVertex3f(vPoint1.x, vPoint1.y, vPoint1.z);
    glVertex3f(vPoint2.x, vPoint2.y, vPoint2.z);
    glVertex3f(vPoint3.x, vPoint3.y, vPoint3.z);
    glVertex3f(vPoint4.x, vPoint4.y, vPoint4.z);
    glEnd();

    glPopAttrib();

    view.endGL();
}

bool TestLocator::isBounded() const{
	return true;
}

MBoundingBox TestLocator::boundingBox() const{
	// Return the bounding box
    MObject thisMob = thisMObject();
    double size = MPlug(thisMob, inSize).asDouble();

    MPoint corner1 = MPoint(1.0, 0.0, -1.0) * size;
    MPoint corner2 = MPoint(-1.0, 0.0, 1.0) * size;

	return MBoundingBox(corner1, corner2);
}

//---------------------------------------------------------------------------------
//---------------------------------------------------------------------------------
//----------   Viewport 2.0 Implementation   --------------------------------------
//---------------------------------------------------------------------------------
//---------------------------------------------------------------------------------
class TestLocatorData : public MUserData{
public:
    TestLocatorData() : MUserData(false) {} // don't delete after draw
    virtual ~TestLocatorData() {}

    MColor                              fDormantColor;
    MColor                              fActiveColor;
    MColor                              fLeadColor;
    MPointArray                         fQuadList;
    double                              fSize;
};


class TestLocatorDrawOverride : public MHWRender::MPxDrawOverride{
private:
    TestLocatorDrawOverride(const MObject& obj);

public:
    virtual ~TestLocatorDrawOverride();

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

TestLocatorDrawOverride::TestLocatorDrawOverride(const MObject & obj)
            : MHWRender::MPxDrawOverride(obj, TestLocatorDrawOverride::draw, false) {}

TestLocatorDrawOverride::~TestLocatorDrawOverride() {}

MHWRender::MPxDrawOverride* TestLocatorDrawOverride::creator(const MObject& obj){
    // MPxDrawOverride creator function.
    return new TestLocatorDrawOverride(obj);
}

bool TestLocatorDrawOverride::isBounded(const MDagPath& objPath,
                                        const MDagPath& cameraPath) const{
	return true;
}

MBoundingBox TestLocatorDrawOverride::boundingBox(const MDagPath& objPath,
												  const MDagPath& cameraPath) const{
    MObject node = objPath.node();
    double size = MPlug(node, TestLocator::inSize).asDouble();

    MPoint corner1 = MPoint(1.0, 0.0, -1.0) * size;
    MPoint corner2 = MPoint(-1.0, 0.0, 1.0) * size;

	return MBoundingBox(corner1, corner2);
}

// Called by Maya each time the object needs to be drawn.
MUserData* TestLocatorDrawOverride::prepareForDraw(const MDagPath& objPath,
												   const MDagPath& cameraPath,
												   const MHWRender::MFrameContext& frameContext,
												   MUserData* oldData){
	// Any data needed from the Maya dependency graph must be retrieved and cached in this stage.
	// There is one cache data for each drawable instance, if it is not desirable to allow Maya to handle data
	// caching, simply return null in this method and ignore user data parameter in draw callback method.
	// e.g. in this sample, we compute and cache the data for usage later when we create the 
	// MUIDrawManager to draw TestLocator in method addUIDrawables().
	TestLocatorData* data = dynamic_cast<TestLocatorData*>(oldData);
	if (!data)
		data = new TestLocatorData();

	MObject node = objPath.node();
    double size = MPlug(node, TestLocator::inSize).asDouble();

    data->fDormantColor = MColor(1.0, 1.0, 0.0);
    data->fActiveColor = MColor(0.3, 1.0, 1.0);
    data->fLeadColor = MColor(1.0, 1.0, 1.0);

    data->fSize = size;

    MVector vPoint1 = MVector(1.0, 0.0, -1.0) * size;
    MVector vPoint2 = MVector(-1.0, 0.0, -1.0) * size;
    MVector vPoint3 = MVector(-1.0, 0.0, 1.0) * size;
    MVector vPoint4 = MVector(1.0, 0.0, 1.0) * size;

    data->fQuadList.clear();
    data->fQuadList.append(MPoint(vPoint1));
    data->fQuadList.append(MPoint(vPoint2));
    data->fQuadList.append(MPoint(vPoint3));
    data->fQuadList.append(MPoint(vPoint4));
    data->fQuadList.append(MPoint(vPoint1));

    return data;
}

// addUIDrawables() provides access to the MUIDrawManager, which can be used
// to queue up operations for drawing simple UI elements such as lines, circles and
// text. To enable addUIDrawables(), override hasUIDrawables() and make it return true.
void TestLocatorDrawOverride::addUIDrawables(const MDagPath& objPath,
											 MHWRender::MUIDrawManager& drawManager,
											 const MHWRender::MFrameContext& frameContext,
											 const MUserData* data){
	// Get data cached by prepareForDraw() for each drawable instance, then MUIDrawManager 
	// can draw simple UI by these data.
	TestLocatorData* locatorData = (TestLocatorData*)data;
	if (!locatorData)
		return;

	MHWRender::DisplayStatus status = MHWRender::MGeometryUtilities::displayStatus(objPath);

	drawManager.beginDrawable();

    if (status == MHWRender::DisplayStatus::kActive)
        drawManager.setColor(locatorData->fActiveColor);
    else if (status == MHWRender::DisplayStatus::kLead)
        drawManager.setColor(locatorData->fLeadColor);
    else if (status == MHWRender::DisplayStatus::kDormant)
        drawManager.setColor(locatorData->fDormantColor);

    drawManager.setDepthPriority(5);
    drawManager.mesh(MHWRender::MUIDrawManager::kTriStrip, locatorData->fQuadList);

	drawManager.endDrawable();
}


#define REGISTER_LOCATOR_NODE(NODE, PLUGIN, DRAWOVERRIDE)                   \
    status = PLUGIN.registerNode(                                           \
        NODE::kNodeName,                                                    \
        NODE::kNodeID,                                                      \
        NODE::creator,                                                      \
        NODE::initialize,                                                   \
        MPxNode::kLocatorNode,                                              \
        &NODE::kNodeClassify                                                \
    );                                                                      \
    CHECK_MSTATUS(status);                                                  \
    status = MHWRender::MDrawRegistry::registerDrawOverrideCreator(         \
        NODE::kNodeClassify,                                                \
        NODE::kNodeRegistrantID,                                            \
        DRAWOVERRIDE::creator                                               \
    );                                                                      \
    CHECK_MSTATUS(status);                                                  \

#define DEREGISTER_LOCATOR_NODE(NODE, PLUGIN)                               \
    status = PLUGIN.deregisterNode(                                         \
        NODE::kNodeID                                                       \
    );                                                                      \
    CHECK_MSTATUS(status);                                                  \
    status = MHWRender::MDrawRegistry::deregisterDrawOverrideCreator(       \
        NODE::kNodeClassify,                                                \
        NODE::kNodeRegistrantID                                             \
    );                                                                      \
    CHECK_MSTATUS(status);                                                  \


const char* kAuthor = "Giuliano Franca";
const char* kVersion = "1.0";
const char* kRequiredAPIVersion = "Any";

const MString TestLocator::kNodeName = "gfTestLocator";
const MString TestLocator::kNodeClassify = "drawdb/geometry/locator";
const MString TestLocator::kNodeRegistrantID = "gfTestLocatorNodePlugin";
const MTypeId TestLocator::kNodeID = 0x000fff;


MStatus initializePlugin(MObject mobject){
    MStatus status;
    MFnPlugin mPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion, &status);
    status = mPlugin.setName("MPxLocatorNode_start");

    REGISTER_LOCATOR_NODE(TestLocator, mPlugin, TestLocatorDrawOverride);

    return status;
}

MStatus uninitializePlugin(MObject mobject){
    MStatus status;
    MFnPlugin mPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion, &status);

    DEREGISTER_LOCATOR_NODE(TestLocator, mPlugin);

    return status;
}