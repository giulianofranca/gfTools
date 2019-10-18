# -*- coding: utf-8 -*-
"""
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

Disclaimer:
    THIS PLUGIN IS JUST A PROTOTYPE. YOU MUST USE THE C++ RELEASE PLUGIN FOR PRODUCTION.
    YOU CAN FIND THE C++ RELEASE PLUGIN FOR YOUR SPECIFIC PLATFORM IN RELEASES FOLDER:
    "gfTools > plug-ins > release

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

This code supports Pylint. Rc file in project.
"""
# pylint: disable=no-name-in-module

import sys
import maya.api._OpenMaya_py2 as om2
import maya.api._OpenMayaUI_py2 as omui2
import maya.api._OpenMayaRender_py2 as omr2
import maya.OpenMayaRender as omr1


def maya_useNewAPI():
    """ Function to Maya recognize the use of the Python API 2.0. """
    # pylint: disable=invalid-name, unnecessary-pass
    pass


def INPUT_ATTR(FNATTR):
    """ Configure a input attribute. """
    # pylint: disable=invalid-name
    FNATTR.writable = True
    FNATTR.readable = True
    FNATTR.storable = True
    FNATTR.keyable = True


def OUTPUT_ATTR(FNATTR):
    """ Configure a output attribute. """
    # pylint: disable=invalid-name
    FNATTR.writable = False
    FNATTR.readable = True
    FNATTR.storable = False
    FNATTR.keyable = False


class TestLocator(omui2.MPxLocatorNode):
    """ Main class of gfTestLocator node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeRegistrantID = ""
    kNodeID = ""

    inSize = om2.MObject()
    inAttr = om2.MObject()
    outAttr = om2.MObject()

    def __init__(self):
        """ Constructor. """
        omui2.MPxLocatorNode.__init__(self)

    def postConstructor(self):
        """ Post Constructor. """
        thisMob = self.thisMObject()
        om2.MFnDependencyNode(thisMob).setName("%sShape#" % TestLocator.kNodeName)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return TestLocator()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to TestLocator class. Instances of TestLocator will use these attributes to create plugs
        for use in the compute() method.
        """
        nAttr = om2.MFnNumericAttribute()

        TestLocator.inSize = nAttr.create("size", "size", om2.MFnNumericData.kDouble, 1.0)
        INPUT_ATTR(nAttr)

        TestLocator.inAttr = nAttr.createPoint("inAttr", "inAttr")
        INPUT_ATTR(nAttr)

        TestLocator.outAttr = nAttr.createPoint("outAttr", "outAttr")
        OUTPUT_ATTR(nAttr)

        TestLocator.addAttribute(TestLocator.inSize)
        TestLocator.addAttribute(TestLocator.inAttr)
        TestLocator.addAttribute(TestLocator.outAttr)
        TestLocator.attributeAffects(TestLocator.inAttr, TestLocator.outAttr)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        if plug == TestLocator.outAttr:
            inAttrValue = dataBlock.inputValue(TestLocator.inAttr).asVector()

            outAttrHandle = dataBlock.outputValue(TestLocator.outAttr)
            outAttrHandle.set3Float(inAttrValue.x, inAttrValue.y, inAttrValue.z)
            outAttrHandle.setClean()

    def draw(self, view, path, style, status):
        """
        Draw custom geometry in the viewport using OpenGL calls.
            * view [M3dView] is a 3D view that is being drawn into.
            * path [MDagPath] to the parent (transform node) of this locator in the DAG.  To obtain the locator shape node,
                use MDagPath::extendToShape() if there is only one shape node under the transform or
                MDagPath::extendToShapeDirectlyBelow(unsigned int index) with the shape index if there are multiple
                shapes under the transform.
            * style [M3dView.DisplayStyle] is the style to draw object in.
            * status [M3dView.DisplayStatus] is the selection status of the object.
        """
        # pylint: disable=unused-argument

        thisMob = self.thisMObject()
        size = om2.MPlug(thisMob, TestLocator.inSize).asDouble()

        view.beginGL()

        glRenderer = omr1.MHardwareRenderer.theRenderer()
        glFT = glRenderer.glFunctionTable()

        glFT.glPushAttrib(omr1.MGL_CURRENT_BIT)
        glFT.glDisable(omr1.MGL_CULL_FACE)

        if status == omui2.M3dView.kActive:
            glFT.glColor3f(0.3, 1.0, 1.0)
        elif status == omui2.M3dView.kLead:
            glFT.glColor3f(1.0, 1.0, 1.0)
        elif status == omui2.M3dView.kDormant:
            glFT.glColor3f(1.0, 1.0, 0.0)

        vPoint1 = om2.MVector(1.0, 0.0, -1.0) * size
        vPoint2 = om2.MVector(-1.0, 0.0, -1.0) * size
        vPoint3 = om2.MVector(-1.0, 0.0, 1.0) * size
        vPoint4 = om2.MVector(1.0, 0.0, 1.0) * size

        glFT.glBegin(omr1.MGL_QUADS)
        glFT.glVertex3f(vPoint1.x, vPoint1.y, vPoint1.z)
        glFT.glVertex3f(vPoint2.x, vPoint2.y, vPoint2.z)
        glFT.glVertex3f(vPoint3.x, vPoint3.y, vPoint3.z)
        glFT.glVertex3f(vPoint4.x, vPoint4.y, vPoint4.z)
        glFT.glEnd()

        glFT.glPopAttrib()

        view.endGL()

    def isBounded(self):
        """isBounded?"""
        return True

    def boundingBox(self):
        """Return the boundingBox"""
        thisMob = self.thisMObject()
        size = om2.MPlug(thisMob, TestLocator.inSize).asDouble()

        corner1 = om2.MPoint(1.0, 0.0, -1.0) * size
        corner2 = om2.MPoint(-1.0, 0.0, 1.0) * size

        return om2.MBoundingBox(corner1, corner2)


class TestLocatorData(om2.MUserData):
    """ Custom user data class. """

    def __init__(self):
        """ Constructor. """
        om2.MUserData.__init__(self, False)  # Don't delete after draw

        self.fDormantColor = om2.MColor()
        self.fActiveColor = om2.MColor()
        self.fLeadColor = om2.MColor()
        self.fQuadList = om2.MPointArray()
        self.fSize = 1.0


class TestLocatorDrawOverride(omr2.MPxDrawOverride):
    """ Drawing override to enable to draw in VP2.0. """

    def __init__(self, obj):
        """ Constructor. """
        omr2.MPxDrawOverride.__init__(self, obj, TestLocatorDrawOverride.draw)

    def supportedDrawAPIs(self):
        """ Select which draw API works. """
        return omr2.MRenderer.kOpenGL | omr2.MRenderer.kDirectX11 | omr2.MRenderer.kOpenGLCoreProfile

    @staticmethod
    def creator(obj):
        """ Maya creator function. """
        return TestLocatorDrawOverride(obj)

    @staticmethod
    def draw(context, data):
        """ Draw method. """
        # pylint: disable=unused-argument
        return

    def isBounded(self, objPath, cameraPath):
        """ isBounded? """
        # pylint: disable=unused-argument
        return True

    def boundingBox(self, objPath, cameraPath):
        """ Return the boundingBox """
        # pylint: disable=unused-argument
        node = objPath.node()
        size = om2.MPlug(node, TestLocator.inSize).asDouble()

        corner1 = om2.MPoint(1.0, 0.0, -1.0) * size
        corner2 = om2.MPoint(-1.0, 0.0, 1.0) * size

        return om2.MBoundingBox(corner1, corner2)

    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        """
        Called by Maya each time the object needs to be drawn.
        Any data needed from the Maya dependency graph must be retrieved and cached in this stage.
        Returns the data to be passed to the draw callback method.
            * objPath [MDagPath] is the path to the object being drawn.
            * cameraPath [MDagPath] is the path to the camera that is being used to draw.
            * frameContext [MFrameContext] is the frame level context information.
            * oldData [MUserData] is the data cached by the previous draw of the instance.
        """
        # pylint: disable=unused-argument
        data = oldData
        if not isinstance(data, TestLocatorData):
            data = TestLocatorData()

        node = objPath.node()
        size = om2.MPlug(node, TestLocator.inSize).asDouble()

        data.fDormantColor = om2.MColor([1.0, 1.0, 0.0])
        data.fActiveColor = om2.MColor([0.3, 1.0, 1.0])
        data.fLeadColor = om2.MColor([1.0, 1.0, 1.0])

        data.fSize = size

        vPoint1 = om2.MVector(1.0, 0.0, -1.0) * size
        vPoint2 = om2.MVector(-1.0, 0.0, -1.0) * size
        vPoint3 = om2.MVector(-1.0, 0.0, 1.0) * size
        vPoint4 = om2.MVector(1.0, 0.0, 1.0) * size

        data.fQuadList.clear()
        data.fQuadList.append(om2.MPoint(vPoint1))
        data.fQuadList.append(om2.MPoint(vPoint2))
        data.fQuadList.append(om2.MPoint(vPoint3))
        data.fQuadList.append(om2.MPoint(vPoint4))
        data.fQuadList.append(om2.MPoint(vPoint1))

        return data

    def hasUIDrawables(self):
        """ Has ui drawables? """
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        """
        Provides access to the MUIDrawManager, which can be used to queue up operations to draw simple UI
        shapes like lines, circles, text, etc.
        It is called after prepareForDraw() and carries the same restrictions on the sorts of operations it
        can perform.
            * objPath [MDagPath] is the path to the object being drawn.
            * drawManager [MUIDrawManager] it can be used to draw some simple geometry including text.
            * frameContext [MFrameContext] is the frame level context information.
            * data [MUserData] is the data cached by the prepareForDraw().
        """
        # pylint: disable=unused-argument
        locatorData = data
        if not isinstance(locatorData, TestLocatorData):
            return

        status = omr2.MGeometryUtilities.displayStatus(objPath)

        drawManager.beginDrawable()

        if status == omr2.MGeometryUtilities.kActive:
            drawManager.setColor(locatorData.fActiveColor)
        elif status == omr2.MGeometryUtilities.kLead:
            drawManager.setColor(locatorData.fLeadColor)
        elif status == omr2.MGeometryUtilities.kDormant:
            drawManager.setColor(locatorData.fDormantColor)

        drawManager.setDepthPriority(5)
        drawManager.mesh(omr2.MUIDrawManager.kTriStrip, locatorData.fQuadList)

        drawManager.endDrawable()


def REGISTER_LOCATOR_NODE(NODE, PLUGIN, DRAWOVERRIDE):
    """ Register a MPxLocatorNode. """
    # pylint: disable=invalid-name
    try:
        PLUGIN.registerNode(NODE.kNodeName, NODE.kNodeID, NODE.creator,
                            NODE.initialize, om2.MPxNode.kLocatorNode, NODE.kNodeClassify)
    except BaseException:
        sys.stderr.write("Failed to register node: %s" % NODE.kNodeName)
        raise

    try:
        omr2.MDrawRegistry.registerDrawOverrideCreator(NODE.kNodeClassify, NODE.kNodeRegistrantID,
                                                       DRAWOVERRIDE.creator)
    except BaseException:
        sys.stderr.write("Failed to register override: %s" % NODE.kNodeName)
        raise

def DEREGISTER_LOCATOR_NODE(NODE, PLUGIN):
    """ Deregister a MPxLocatorNode. """
    # pylint: disable=invalid-name
    try:
        PLUGIN.deregisterNode(NODE.kNodeID)
    except BaseException:
        sys.stderr.write("Failed to deregister node: %s" % NODE.kNodeName)
        raise

    try:
        omr2.MDrawRegistry.deregisterDrawOverrideCreator(NODE.kNodeClassify, NODE.kNodeRegistrantID)
    except BaseException:
        sys.stderr.write("Failed to deregister override: %s" % NODE.kNodeName)
        raise


kAuthor = "Giuliano Franca"
kVersion = "1.0"
kRequiredAPIVersion = "Any"

TestLocator.kNodeName = "gfTestLocator"
TestLocator.kNodeClassify = "drawdb/geometry/locator"
TestLocator.kNodeRegistrantID = "gfTestLocatorNodePlugin"
TestLocator.kNodeID = om2.MTypeId(0x000fff)


def initializePlugin(mobject):
    """ Initializes the plug-in. """
    mPlugin = om2.MFnPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion)

    REGISTER_LOCATOR_NODE(TestLocator, mPlugin, TestLocatorDrawOverride)


def uninitializePlugin(mobject):
    """ Unitializes the plug-in. """
    mPlugin = om2.MFnPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion)

    DEREGISTER_LOCATOR_NODE(TestLocator, mPlugin)
