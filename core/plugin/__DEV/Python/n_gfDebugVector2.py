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
    * glFT.glEnable(omr1.MGL_BLEND); glFT.glBlendFunc(omr1.MGL_SRC_ALPHA, omr1.MGL_ONE_MINUS_SRC_ALPHA)

This code supports Pylint. Rc file in project.
"""
# pylint: disable=import-error
# import-error = Supress Maya modules import error

import math
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
        uAttr = om2.MFnUnitAttribute()

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

        DebugVector.inSize = uAttr.create("size", "size", om2.MFnUnitAttribute.kDistance)
        uAttr.default = om2.MDistance(0.0)
        INPUT_ATTR(uAttr)

        DebugVector.addAttribute(DebugVector.inLineWidth)
        DebugVector.addAttribute(DebugVector.inColor)
        DebugVector.addAttribute(DebugVector.inRadius)
        DebugVector.addAttribute(DebugVector.inXRay)
        DebugVector.addAttribute(DebugVector.inOperation)
        DebugVector.addAttribute(DebugVector.inVec1)
        DebugVector.addAttribute(DebugVector.inVec2)
        DebugVector.addAttribute(DebugVector.inSize)

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
        radius = om2.MPlug(thisMob, DebugVector.inRadius).asFloat()
        xray = om2.MPlug(thisMob, DebugVector.inXRay).asBool()
        vVec1 = om2.MPlug(thisMob, DebugVector.inVec1).asMDataHandle().asFloatVector()
        vVec2 = om2.MPlug(thisMob, DebugVector.inVec2).asMDataHandle().asFloatVector()

        vAim = vVec2 - vVec1
        nAim = vAim.normal()
        nBinormal = nAim ^ -om2.MFloatVector(0.0, 1.0, 0.0)
        nNormal = nAim ^ nBinormal

        aim = [nAim.x, nAim.y, nAim.z, 0.0,
               nNormal.x, nNormal.y, nNormal.z, 0.0,
               nBinormal.x, nBinormal.y, nBinormal.z, 0.0,
               0.0, 0.0, 0.0, 1.0]
        mAim = om2.MMatrix(aim)
        mTrans = om2.MMatrix()
        mTrans[12] = vVec1.x
        mTrans[13] = vVec1.y
        mTrans[14] = vVec1.z
        mBase = mAim * mTrans
        mBaseArrowL = om2.MMatrix()
        mBaseArrowL[12] = vAim.length() * 0.9
        mBaseArrowW = mBaseArrowL * mBase
        # length = om2.MFloatVector(vAim * 0.9).length()
        # mArrow = om2.MMatrix()
        # mArrow[12] = length
        # mArrowBase = mBase * mArrow


        # vDist += vVec1

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
            glFT.glColor3f(0.5, 1.0, 1.0)
        elif status == omui2.M3dView.kLead:
            glFT.glColor3f(1.0, 1.0, 1.0)
        elif status == omui2.M3dView.kDormant:
            glFT.glColor3f(colorLoc.x, colorLoc.y, colorLoc.z)

        glFT.glLineWidth(lineW)
        glFT.glBegin(omr1.MGL_LINES)
        glFT.glVertex3f(vVec1.x, vVec1.y, vVec1.z)
        glFT.glVertex3f(vVec2.x, vVec2.y, vVec2.z)
        arrowSubd = 4
        step = 2.0 * math.pi / float(arrowSubd)
        for i in range(arrowSubd):
            theta = step * i
            mPointL = om2.MMatrix()
            mPointL[13] = -math.sin(theta) * radius
            mPointL[14] = math.cos(theta) * radius
            mPoint = mPointL * mBaseArrowW
            glFT.glVertex3f(mBaseArrowW[12], mBaseArrowW[13], mBaseArrowW[14])
            glFT.glVertex3f(mPoint[12], mPoint[13], mPoint[14])
            glFT.glVertex3f(mPoint[12], mPoint[13], mPoint[14])
            glFT.glVertex3f(vVec2.x, vVec2.y, vVec2.z)
        # arrowSubd = 4
        # step = 2.0 * math.pi / float(arrowSubd)
        # for i in range(arrowSubd):
        #     theta = step * i
        #     mDist = om2.MMatrix()
        #     mDist[13] = math.cos(theta) * radius
        #     mDist[14] = math.sin(theta) * radius
        #     mPoint = mDist * mArrowBase
        #     glFT.glVertex3f(mArrowBase[12], mArrowBase[13], mArrowBase[14])
        #     glFT.glVertex3f(mPoint[12], mPoint[13], mPoint[14])
        #     glFT.glVertex3f(mPoint[12], mPoint[13], mPoint[14])
        #     glFT.glVertex3f(vVec2.x, vVec2.y, vVec2.z)
        glFT.glEnd()

        # glFT.glDisable(omr1.MGL_BLEND)
        if xray:
            glFT.glDisable(omr1.MGL_DEPTH_TEST)
        glFT.glPopAttrib()
        glFT.glLineWidth(1.0)

        view.endGL()

    def isBounded(self):
        """ isBounded? """
        return True

    def boundingBox(self):
        """ Return the boundingBox """
        # Get the size
        thisMob = self.thisMObject()
        plug = om2.MPlug(thisMob, DebugVector.inSize)
        sizeVal = plug.asMDistance()
        multiplier = sizeVal.asCentimeters()

        corner1 = om2.MPoint(-0.17, 0.0, -0.7)
        corner2 = om2.MPoint(0.17, 0.0, 0.3)

        corner1 *= multiplier
        corner2 *= multiplier

        return om2.MBoundingBox(corner1, corner2)


# class DebugVectorData(om2.MUserData):
#     """ Custom user data class. """

#     def __init__(self):
#         """ Constructor. """
#         om2.MUserData.__init__(self, False)  # Don't delete after draw

#         self.fColor = om2.MColor()
#         self.fSoleLineList = om2.MPointArray()
#         self.fSoleTriangleList = om2.MPointArray()
#         self.fHeelLineList = om2.MPointArray()
#         self.fHeelTriangleList = om2.MPointArray()


# class DebugVectorDrawOverride(omr2.MPxDrawOverride):
#     """ Drawing override to enable to draw in VP2.0. """

#     def __init__(self, obj):
#         """ Constructor. """
#         omr2.MPxDrawOverride.__init__(self, obj, DebugVectorDrawOverride.draw)

#         # We want to perform custom bounding box drawing so return True so that the
#         # internal rendering code will not draw it for us.
#         self.mCustomBoxDraw = True
#         self.mCurrentBoundingBox = om2.MBoundingBox()

#     def supportedDrawAPIs(self):
#         """ Select which draw API works. """
#         return omr2.MRenderer.kOpenGL | omr2.MRenderer.kDirectX11 | omr2.MRenderer.kOpenGLCoreProfile

#     @staticmethod
#     def creator(obj):
#         """ Maya creator function. """
#         return DebugVectorDrawOverride(obj)

#     @staticmethod
#     def draw(context, data):
#         """ Draw method. """
#         # pylint: disable=unused-argument
#         return

#     def isBounded(self, objPath, cameraPath):
#         """ isBounded? """
#         # pylint: disable=unused-argument
#         return True

#     def boundingBox(self, objPath, cameraPath):
#         """ Return the boundingBox """
#         # pylint: disable=unused-argument
#         corner1 = om2.MPoint(-0.17, 0.0, -0.7)
#         corner2 = om2.MPoint(0.17, 0.0, 0.3)

#         multiplier = self.getMultiplier(objPath)
#         corner1 *= multiplier
#         corner2 *= multiplier

#         self.mCurrentBoundingBox.clear()
#         self.mCurrentBoundingBox.expand(corner1)
#         self.mCurrentBoundingBox.expand(corner2)

#         return self.mCurrentBoundingBox

#     def disableInternalBoundingBoxDraw(self):
#         """ Disable internal bounding box draw. """
#         return self.mCustomBoxDraw

#     def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
#         """ Append new data to the MUserData. """
#         # pylint: disable=unused-argument
#         # Retrieve data cache (create if does not exist)
#         data = oldData
#         if not isinstance(data, DebugVectorData):
#             data = DebugVectorData()

#         # Compute data and cache it

#         fMultiplier = self.getMultiplier(objPath)

#         data.fSoleLineList.clear()
#         for i in range(soleCount):
#             data.fSoleLineList.append(om2.MPoint(sole[i][0] * fMultiplier, sole[i][1] * fMultiplier, sole[i][2] * fMultiplier))

#         data.fHeelLineList.clear()
#         for i in range(heelCount):
#             data.fHeelLineList.append(om2.MPoint(heel[i][0] * fMultiplier, heel[i][1] * fMultiplier, heel[i][2] * fMultiplier))

#         data.fSoleTriangleList.clear()
#         for i in range(1, soleCount - 1):
#             data.fSoleTriangleList.append(om2.MPoint(sole[0][0] * fMultiplier, sole[0][1] * fMultiplier, sole[0][2] * fMultiplier))
#             data.fSoleTriangleList.append(om2.MPoint(sole[i][0] * fMultiplier, sole[i][1] * fMultiplier, sole[i][2] * fMultiplier))
#             data.fSoleTriangleList.append(om2.MPoint(sole[i + 1][0] * fMultiplier, sole[i + 1][1] * fMultiplier, sole[i + 1][2] * fMultiplier))

#         data.fHeelTriangleList.clear()
#         for i in range(1, heelCount - 1):
#             data.fHeelTriangleList.append(om2.MPoint(heel[0][0] * fMultiplier, heel[0][1] * fMultiplier, heel[0][2] * fMultiplier))
#             data.fHeelTriangleList.append(om2.MPoint(heel[i][0] * fMultiplier, heel[i][1] * fMultiplier, heel[i][2] * fMultiplier))
#             data.fHeelTriangleList.append(om2.MPoint(heel[i + 1][0] * fMultiplier, heel[i + 1][1] * fMultiplier, heel[i + 1][2] * fMultiplier))

#         data.fColor = omr2.MGeometryUtilities.wireframeColor(objPath)

#         return data

#     def hasUIDrawables(self):
#         """ Has ui drawables? """
#         return True

#     def addUIDrawables(self, objPath, drawManager, frameContext, data):
#         """ Add UI Drawables. """
#         # pylint: disable=unused-argument
#         locatorData = data
#         if not isinstance(locatorData, DebugVectorData):
#             return

#         drawManager.beginDrawable()

#         # Draw the quad solid/wireframe
#         drawManager.setColor(locatorData.fColor)
#         drawManager.setDepthPriority(5)

#         if frameContext.getDisplayStyle() & omr2.MFrameContext.kGouraudShaded:
#             drawManager.mesh(omr2.MGeometry.kTriangles, locatorData.fSoleTriangleList)
#             drawManager.mesh(omr2.MGeometry.kTriangles, locatorData.fHeelTriangleList)

#         drawManager.mesh(omr2.MUIDrawManager.kClosedLine, locatorData.fSoleLineList)
#         drawManager.mesh(omr2.MUIDrawManager.kClosedLine, locatorData.fHeelLineList)

#         # Draw a text
#         pos = om2.MPoint(0.0, 0.0, 0.0)
#         textColor = om2.MColor((0.1, 0.8, 0.8, 1.0))

#         drawManager.setColor(textColor)
#         drawManager.setFontSize(omr2.MUIDrawManager.kSmallFontSize)
#         drawManager.text(pos, "Custom Locator", omr2.MUIDrawManager.kCenter)

#         drawManager.endDrawable()

#     def getMultiplier(self, objPath):
#         """ Return the multiplier size value. """
#         node = objPath.node()
#         plug = om2.MPlug(node, DebugVector.inSize)
#         if not plug.isNull:
#             sizeVal = plug.asMDistance()
#             return sizeVal.asCentimeters()
#         return 1.0
