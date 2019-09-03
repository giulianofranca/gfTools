# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfDebugVector node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.

Requirements:
    Maya 2017 or above.

Todo:
    * Lock the SRT controls in post-constructor
    * https://en.wikibooks.org/wiki/OpenGL_Programming/GLStart/Tut3
    * https://community.khronos.org/t/fyi-c-code-for-drawing-a-line-3d-arrow-head/70602
    * glFT.glEnable(omr1.MGL_BLEND); glFT.glBlendFunc(omr1.MGL_SRC_ALPHA, omr1.MGL_ONE_MINUS_SRC_ALPHA)
    * Fix can't select in xray mode

This code supports Pylint. Rc file in project.
"""
# pylint: disable=import-error
# import-error = Supress Maya modules import error

import maya.api.OpenMaya as om2
import maya.api.OpenMayaUI as omui2
import maya.api.OpenMayaRender as omr2


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


class DebugVector(omui2.MPxLocatorNode):
    """ Main class of gfDebugVector node. """

    kNODE_NAME = ""
    kNODE_CLASSIFY = ""
    kNODE_REGISTRANT_ID = ""
    kNODE_ID = ""

    inLineWidth = om2.MObject()
    inColor = om2.MObject()
    inRadius = om2.MObject()
    inXRay = om2.MObject()
    inVec1 = om2.MObject()
    inVec2 = om2.MObject()
    inOperation = om2.MObject()

    inSize = om2.MObject()

    def __init__(self):
        """ Constructor. """
        omui2.MPxLocatorNode.__init__(self)

    def postConstructor(self):
        """ Post Constructor. """
        thisMob = self.thisMObject()
        om2.MFnDependencyNode(thisMob).setName("gfDebugVector_PShape#")

    @staticmethod
    def creator():
        """ Maya creator function. """
        return DebugVector()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to DebugVector class. Instances of DebugVector will use these attributes to create plugs
        for use in the compute() method.
        """
        eAttr = om2.MFnEnumAttribute()
        nAttr = om2.MFnNumericAttribute()

        DebugVector.inLineWidth = nAttr.create("lineWidth", "lw", om2.MFnNumericData.kFloat, 3.0)
        nAttr.setMin(1.0)
        nAttr.setSoftMax(5.0)
        INPUT_ATTR(nAttr)

        DebugVector.inColor = nAttr.createColor("color", "color")
        nAttr.default = (1.0, 1.0, 0.0)
        INPUT_ATTR(nAttr)

        DebugVector.inRadius = nAttr.create("radius", "radius", om2.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0.0)
        nAttr.setSoftMax(2.0)
        INPUT_ATTR(nAttr)

        DebugVector.inXRay = nAttr.create("XRay", "xray", om2.MFnNumericData.kBoolean, False)
        INPUT_ATTR(nAttr)

        DebugVector.inOperation = eAttr.create("operation", "op", 1)
        eAttr.addField("No operation", 0)
        eAttr.addField("Add", 1)
        eAttr.addField("Subtract", 2)
        INPUT_ATTR(eAttr)

        DebugVector.inVec1 = nAttr.createPoint("vector1", "v1")
        INPUT_ATTR(nAttr)

        DebugVector.inVec2 = nAttr.createPoint("vector2", "v2")
        INPUT_ATTR(nAttr)

        DebugVector.addAttribute(DebugVector.inLineWidth)
        DebugVector.addAttribute(DebugVector.inColor)
        DebugVector.addAttribute(DebugVector.inRadius)
        DebugVector.addAttribute(DebugVector.inXRay)
        DebugVector.addAttribute(DebugVector.inOperation)
        DebugVector.addAttribute(DebugVector.inVec1)
        DebugVector.addAttribute(DebugVector.inVec2)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use, unused-argument
        return None

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
        lineW = om2.MPlug(thisMob, DebugVector.inLineWidth).asFloat()
        colorLoc = om2.MPlug(thisMob, DebugVector.inColor).asMDataHandle().asFloatVector()
        # radius = om2.MPlug(thisMob, DebugVector.inRadius).asFloat()
        xray = om2.MPlug(thisMob, DebugVector.inXRay).asBool()
        vVec1 = om2.MPlug(thisMob, DebugVector.inVec1).asMDataHandle().asFloatVector()
        vVec2 = om2.MPlug(thisMob, DebugVector.inVec2).asMDataHandle().asFloatVector()

        view.beginGL()

        # Drawing in VP1 views will be done using Python API 1.0
        import maya.OpenMayaRender as omr1
        glRenderer = omr1.MHardwareRenderer.theRenderer()
        glFT = glRenderer.glFunctionTable()

        glFT.glPushAttrib(omr1.MGL_CURRENT_BIT)
        glFT.glDisable(omr1.MGL_CULL_FACE)
        if xray:
            glFT.glEnable(omr1.MGL_DEPTH_TEST)
            glFT.glClear(omr1.MGL_DEPTH_BUFFER_BIT)

        if status == omui2.M3dView.kActive:
            glFT.glColor3f(0.3, 1.0, 1.0)
        elif status == omui2.M3dView.kLead:
            glFT.glColor3f(1.0, 1.0, 1.0)
        elif status == omui2.M3dView.kDormant:
            glFT.glColor3f(colorLoc.x, colorLoc.y, colorLoc.z)

        glFT.glLineWidth(lineW)
        glFT.glBegin(omr1.MGL_LINES)
        glFT.glVertex3f(vVec1.x, vVec1.y, vVec1.z)
        glFT.glVertex3f(vVec2.x, vVec2.y, vVec2.z)
        glFT.glEnd()
        if xray:
            glFT.glDisable(omr1.MGL_DEPTH_TEST)
        glFT.glPopAttrib()
        glFT.glLineWidth(1.0)

        view.endGL()


class DebugVectorData(om2.MUserData):
    """ Custom user data class. """

    def __init__(self):
        """ Constructor. """
        om2.MUserData.__init__(self, False)  # Don't delete after draw

        self.fDormantColor = om2.MColor()
        self.fActiveColor = om2.MColor()
        self.fLeadColor = om2.MColor()
        self.fLineList = om2.MPointArray()
        self.fLineWidth = 1.0
        self.fXRay = 5


class DebugVectorDrawOverride(omr2.MPxDrawOverride):
    """ Drawing override to enable to draw in VP2.0. """

    def __init__(self, obj):
        """ Constructor. """
        omr2.MPxDrawOverride.__init__(self, obj, DebugVectorDrawOverride.draw)

        # We want to perform custom bounding box drawing so return True so that the
        # internal rendering code will not draw it for us.
        self.mCustomBoxDraw = True
        self.mCurrentBoundingBox = om2.MBoundingBox()

    def supportedDrawAPIs(self):
        """ Select which draw API works. """
        return omr2.MRenderer.kOpenGL | omr2.MRenderer.kDirectX11 | omr2.MRenderer.kOpenGLCoreProfile

    @staticmethod
    def creator(obj):
        """ Maya creator function. """
        return DebugVectorDrawOverride(obj)

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
        vVec1 = om2.MPlug(node, DebugVector.inVec1).asMDataHandle().asFloatVector()
        vVec2 = om2.MPlug(node, DebugVector.inVec2).asMDataHandle().asFloatVector()
        corner1 = om2.MPoint(vVec1.x, vVec1.y, vVec1.z)
        corner2 = om2.MPoint(vVec2.x, vVec2.y, vVec2.z)

        self.mCurrentBoundingBox.clear()
        self.mCurrentBoundingBox.expand(corner1)
        self.mCurrentBoundingBox.expand(corner2)

        return self.mCurrentBoundingBox

    def disableInternalBoundingBoxDraw(self):
        """ Disable internal bounding box draw. """
        return self.mCustomBoxDraw

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
        if not isinstance(data, DebugVectorData):
            data = DebugVectorData()

        node = objPath.node()
        lineW = om2.MPlug(node, DebugVector.inLineWidth).asFloat()
        colorLoc = om2.MPlug(node, DebugVector.inColor).asMDataHandle().asFloatVector()
        xray = om2.MPlug(node, DebugVector.inXRay).asBool()
        vVec1 = om2.MPlug(node, DebugVector.inVec1).asMDataHandle().asFloatVector()
        vVec2 = om2.MPlug(node, DebugVector.inVec2).asMDataHandle().asFloatVector()

        data.fLineList.clear()
        data.fLineList.append(om2.MPoint(vVec1.x, vVec1.y, vVec1.z))
        data.fLineList.append(om2.MPoint(vVec2.x, vVec2.y, vVec2.z))
        data.fDormantColor = om2.MColor([colorLoc.x, colorLoc.y, colorLoc.z])
        data.fActiveColor = om2.MColor([0.3, 1.0, 1.0])
        data.fLeadColor = om2.MColor([1.0, 1.0, 1.0])
        data.fLineWidth = lineW
        if xray:
            data.fXRay = True
        else:
            data.fXRay = False

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
        if not isinstance(locatorData, DebugVectorData):
            return

        # status = omui2.M3dView.displayStatus(objPath)
        status = omr2.MGeometryUtilities.displayStatus(objPath)

        if locatorData.fXRay:
            drawManager.beginDrawInXray()
        else:
            drawManager.beginDrawable()

        if status == omr2.MGeometryUtilities.kActive:
            drawManager.setColor(locatorData.fActiveColor)
        elif status == omr2.MGeometryUtilities.kLead:
            drawManager.setColor(locatorData.fLeadColor)
        elif status == omr2.MGeometryUtilities.kDormant:
            drawManager.setColor(locatorData.fDormantColor)

        drawManager.setDepthPriority(5)

        drawManager.setLineWidth(locatorData.fLineWidth)
        drawManager.mesh(omr2.MUIDrawManager.kLines, locatorData.fLineList)

        if locatorData.fXRay:
            drawManager.endDrawInXray()
        else:
            drawManager.endDrawable()
