# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the testLocatorNode node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.

Requirements:
    Maya 2017 or above.

Todo:
    * NDA

This code supports Pylint. Rc file in project.
"""
# pylint: disable=import-error
# import-error = Supress Maya modules import error

import sys
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


sole = [[0.00, 0.0, -0.70],
        [0.04, 0.0, -0.69],
        [0.09, 0.0, -0.65],
        [0.13, 0.0, -0.61],
        [0.16, 0.0, -0.54],
        [0.17, 0.0, -0.46],
        [0.17, 0.0, -0.35],
        [0.16, 0.0, -0.25],
        [0.15, 0.0, -0.14],
        [0.13, 0.0, 0.00],
        [0.00, 0.0, 0.00],
        [-0.13, 0.0, 0.00],
        [-0.15, 0.0, -0.14],
        [-0.16, 0.0, -0.25],
        [-0.17, 0.0, -0.35],
        [-0.17, 0.0, -0.46],
        [-0.16, 0.0, -0.54],
        [-0.13, 0.0, -0.61],
        [-0.09, 0.0, -0.65],
        [-0.04, 0.0, -0.69],
        [-0.00, 0.0, -0.70]]
heel = [[0.00, 0.0, 0.06],
        [0.13, 0.0, 0.06],
        [0.14, 0.0, 0.15],
        [0.14, 0.0, 0.21],
        [0.13, 0.0, 0.25],
        [0.11, 0.0, 0.28],
        [0.09, 0.0, 0.29],
        [0.04, 0.0, 0.30],
        [0.00, 0.0, 0.30],
        [-0.04, 0.0, 0.30],
        [-0.09, 0.0, 0.29],
        [-0.11, 0.0, 0.28],
        [-0.13, 0.0, 0.25],
        [-0.14, 0.0, 0.21],
        [-0.14, 0.0, 0.15],
        [-0.13, 0.0, 0.06],
        [-0.00, 0.0, 0.06]]
soleCount = 21
heelCount = 17


class TestLocator(omui2.MPxLocatorNode):
    """ Main class of testLocatorNode node. """

    kNODE_NAME = "TestLocator"
    kNODE_CLASSIFY = "drawdb/geometry/footPrint"
    kNODE_REGISTRANT_ID = "TestLocatorNodePlugin"
    kNODE_ID = om2.MTypeId(0x0012f7c2)

    inSize = om2.MObject()

    def __init__(self):
        """ Constructor. """
        omui2.MPxLocatorNode.__init__(self)

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
        uAttr = om2.MFnUnitAttribute()

        TestLocator.inSize = uAttr.create("size", "sz", om2.MFnUnitAttribute.kDistance)
        uAttr.default = om2.MDistance(1.0)
        # INPUT_ATTR(uAttr)

        TestLocator.addAttribute(TestLocator.inSize)

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
        # Get the size
        thisMob = self.thisMObject()
        plug = om2.MPlug(thisMob, TestLocator.inSize)
        sizeVal = plug.asMDistance()
        multiplier = sizeVal.asCentimeters()

        view.beginGL()

        # Drawing in VP1 views will be done using Python API 1.0
        import maya.OpenMayaRender as omr1
        glRenderer = omr1.MHardwareRenderer.theRenderer()
        glFT = glRenderer.glFunctionTable()

        if style in (omui2.M3dView.kFlatShaded, omui2.M3dView.kGouraudShaded):
            # Push the color settings
            glFT.glPushAttrib(omr1.MGL_CURRENT_BIT)
            # Show both faces
            glFT.glDisable(omr1.MGL_CULL_FACE)

            if status == omui2.M3dView.kActive:
                view.setDrawColor(13, omui2.M3dView.kActiveColors)
            else:
                view.setDrawColor(13, omui2.M3dView.kDormantColors)

            glFT.glBegin(omr1.MGL_TRIANGLE_FAN)
            for i in range(soleCount - 1):
                glFT.glVertex3f(sole[i][0] * multiplier, sole[i][1] * multiplier, sole[i][2] * multiplier)
            glFT.glEnd()

            glFT.glBegin(omr1.MGL_TRIANGLE_FAN)
            for i in range(heelCount - 1):
                glFT.glVertex3f(heel[i][0] * multiplier, heel[i][1] * multiplier, heel[i][2] * multiplier)
            glFT.glEnd()

            glFT.glPopAttrib()

        # Draw the outline
        glFT.glBegin(omr1.MGL_LINES)
        for i in range(soleCount - 1):
            glFT.glVertex3f(sole[i][0] * multiplier, sole[i][1] * multiplier, sole[i][2] * multiplier)
            glFT.glVertex3f(sole[i + 1][0] * multiplier, sole[i + 1][1] * multiplier, sole[i + 1][2] * multiplier)
        glFT.glEnd()

        for i in range(heelCount - 1):
            glFT.glVertex3f(heel[i][0] * multiplier, heel[i][1] * multiplier, heel[i][2] * multiplier)
            glFT.glVertex3f(heel[i + 1][0] * multiplier, heel[i + 1][1] * multiplier, heel[i + 1][2] * multiplier)
        glFT.glEnd()

        view.endGL()

        # Draw the name of the badword
        view.setDrawColor(om2.MColor((0.1, 0.8, 0.8, 1.0)))
        view.drawText("Custom Locator", om2.MPoint(0.0, 0.0, 0.0), omui2.M3dView.kCenter)

    def isBounded(self):
        """ isBounded? """
        return True

    def boundingBox(self):
        """ Return the boundingBox """
        # Get the size
        thisMob = self.thisMObject()
        plug = om2.MPlug(thisMob, TestLocator.inSize)
        sizeVal = plug.asMDistance()
        multiplier = sizeVal.asCentimeters()

        corner1 = om2.MPoint(-0.17, 0.0, -0.7)
        corner2 = om2.MPoint(0.17, 0.0, 0.3)

        corner1 *= multiplier
        corner2 *= multiplier

        return om2.MBoundingBox(corner1, corner2)


class DebugPoleVectorData(om2.MUserData):
    """ Custom user data class. """

    def __init__(self):
        """ Constructor. """
        om2.MUserData.__init__(self, False)  # Don't delete after draw

        self.fColor = om2.MColor()
        self.fSoleLineList = om2.MPointArray()
        self.fSoleTriangleList = om2.MPointArray()
        self.fHeelLineList = om2.MPointArray()
        self.fHeelTriangleList = om2.MPointArray()


class DebugPoleVectorDrawOverride(omr2.MPxDrawOverride):
    """ Drawing override to enable to draw in VP2.0. """

    def __init__(self, obj):
        """ Constructor. """
        omr2.MPxDrawOverride.__init__(self, obj, DebugPoleVectorDrawOverride.draw)

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
        return DebugPoleVectorDrawOverride(obj)

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
        corner1 = om2.MPoint(-0.17, 0.0, -0.7)
        corner2 = om2.MPoint(0.17, 0.0, 0.3)

        multiplier = self.getMultiplier(objPath)
        corner1 *= multiplier
        corner2 *= multiplier

        self.mCurrentBoundingBox.clear()
        self.mCurrentBoundingBox.expand(corner1)
        self.mCurrentBoundingBox.expand(corner2)

        return self.mCurrentBoundingBox

    def disableInternalBoundingBoxDraw(self):
        """ Disable internal bounding box draw. """
        return self.mCustomBoxDraw

    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        """ Append new data to the MUserData. """
        # pylint: disable=unused-argument
        # Retrieve data cache (create if does not exist)
        data = oldData
        if not isinstance(data, DebugPoleVectorData):
            data = DebugPoleVectorData()

        # Compute data and cache it

        fMultiplier = self.getMultiplier(objPath)

        data.fSoleLineList.clear()
        for i in range(soleCount):
            data.fSoleLineList.append(om2.MPoint(sole[i][0] * fMultiplier, sole[i][1] * fMultiplier, sole[i][2] * fMultiplier))

        data.fHeelLineList.clear()
        for i in range(heelCount):
            data.fHeelLineList.append(om2.MPoint(heel[i][0] * fMultiplier, heel[i][1] * fMultiplier, heel[i][2] * fMultiplier))

        data.fSoleTriangleList.clear()
        for i in range(1, soleCount - 1):
            data.fSoleTriangleList.append(om2.MPoint(sole[0][0] * fMultiplier, sole[0][1] * fMultiplier, sole[0][2] * fMultiplier))
            data.fSoleTriangleList.append(om2.MPoint(sole[i][0] * fMultiplier, sole[i][1] * fMultiplier, sole[i][2] * fMultiplier))
            data.fSoleTriangleList.append(om2.MPoint(sole[i + 1][0] * fMultiplier, sole[i + 1][1] * fMultiplier, sole[i + 1][2] * fMultiplier))

        data.fHeelTriangleList.clear()
        for i in range(1, heelCount - 1):
            data.fHeelTriangleList.append(om2.MPoint(heel[0][0] * fMultiplier, heel[0][1] * fMultiplier, heel[0][2] * fMultiplier))
            data.fHeelTriangleList.append(om2.MPoint(heel[i][0] * fMultiplier, heel[i][1] * fMultiplier, heel[i][2] * fMultiplier))
            data.fHeelTriangleList.append(om2.MPoint(heel[i + 1][0] * fMultiplier, heel[i + 1][1] * fMultiplier, heel[i + 1][2] * fMultiplier))

        data.fColor = omr2.MGeometryUtilities.wireframeColor(objPath)

        return data

    def hasUIDrawables(self):
        """ Has ui drawables? """
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        """ Add UI Drawables. """
        # pylint: disable=unused-argument
        locatorData = data
        if not isinstance(locatorData, DebugPoleVectorData):
            return

        drawManager.beginDrawable()

        # Draw the quad solid/wireframe
        drawManager.setColor(locatorData.fColor)
        drawManager.setDepthPriority(5)

        if frameContext.getDisplayStyle() & omr2.MFrameContext.kGouraudShaded:
            drawManager.mesh(omr2.MGeometry.kTriangles, locatorData.fSoleTriangleList)
            drawManager.mesh(omr2.MGeometry.kTriangles, locatorData.fHeelTriangleList)

        drawManager.mesh(omr2.MUIDrawManager.kClosedLine, locatorData.fSoleLineList)
        drawManager.mesh(omr2.MUIDrawManager.kClosedLine, locatorData.fHeelLineList)

        # Draw a text
        pos = om2.MPoint(0.0, 0.0, 0.0)
        textColor = om2.MColor((0.1, 0.8, 0.8, 1.0))

        drawManager.setColor(textColor)
        drawManager.setFontSize(omr2.MUIDrawManager.kSmallFontSize)
        drawManager.text(pos, "Custom Locator", omr2.MUIDrawManager.kCenter)

        drawManager.endDrawable()

    def getMultiplier(self, objPath):
        """ Return the multiplier size value. """
        node = objPath.node()
        plug = om2.MPlug(node, TestLocator.inSize)
        if not plug.isNull:
            sizeVal = plug.asMDistance()
            return sizeVal.asCentimeters()
        return 1.0


def initializePlugin(obj):
    """ Initialize Plugin function. """
    plugin = om2.MFnPlugin(obj, "Autodesk", "3.0", "Any")

    try:
        plugin.registerNode(TestLocator.kNODE_NAME, TestLocator.kNODE_ID, TestLocator.creator,
                            TestLocator.initialize, om2.MPxNode.kLocatorNode, TestLocator.kNODE_CLASSIFY)
    except BaseException:
        sys.stderr.write("Failed to register node\n")
        raise

    try:
        omr2.MDrawRegistry.registerDrawOverrideCreator(TestLocator.kNODE_CLASSIFY, TestLocator.kNODE_REGISTRANT_ID,
                                                       DebugPoleVectorDrawOverride.creator)
    except BaseException:
        sys.stderr.write("Failed to register override\n")
        raise


def uninitializePlugin(obj):
    """ Uninitialize Plugin function. """
    plugin = om2.MFnPlugin(obj)

    try:
        plugin.deregisterNode(TestLocator.kNODE_ID)
    except BaseException:
        sys.stderr.write("Failed to deregister node\n")
        raise

    try:
        omr2.MDrawRegistry.deregisterDrawOverrideCreator(TestLocator.kNODE_CLASSIFY, TestLocator.kNODE_REGISTRANT_ID)
    except BaseException:
        sys.stderr.write("Failed to deregister override\n")
        raise
