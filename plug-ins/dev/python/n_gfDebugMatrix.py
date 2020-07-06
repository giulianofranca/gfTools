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
    "gfTools > plug-ins > release"

How to use:
    * Copy the parent folder to the MAYA_SCRIPT_PATH.
    * To find MAYA_SCRIPT_PATH paste this command in a Python tab:
        import os; os.environ["MAYA_SCRIPT_PATH"].split(";")
    * In Maya, go to Windows > Settings/Preferences > Plug-in Manager.
    * Browse for "gfTools > plug-ins > dev > python"
    * Find gfTools_P.py and import it.

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

This code supports Pylint. Rc file in project.
"""
# pylint: disable=no-name-in-module

import math
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
    FNATTR.channelBox = True


def OUTPUT_ATTR(FNATTR):
    """ Configure a output attribute. """
    # pylint: disable=invalid-name
    FNATTR.writable = False
    FNATTR.readable = True
    FNATTR.storable = False
    FNATTR.keyable = False


class DebugMatrix(omui2.MPxLocatorNode):
    """ Main class of gfDebugMatrix node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeRegistrantID = ""
    kNodeID = ""

    inMatrix = om2.MObject()
    inNameColor = om2.MObject()
    inMtxColor = om2.MObject()
    inDistance = om2.MObject()
    inLineHeight = om2.MObject()

    fNameColor = om2.MColor([0.90588, 0.41961, 0.41961])
    fMtxColor = om2.MColor([0.93725, 0.87843, 0.69412])

    def __init__(self):
        """ Constructor. """
        omui2.MPxLocatorNode.__init__(self)

    def postConstructor(self):
        """ Post Constructor. """
        thisMob = self.thisMObject()
        nodeFn = om2.MFnDependencyNode(thisMob)
        nodeFn.setName("%sShape#" % DebugMatrix.kNodeName)
        # localPosPlug = nodeFn.findPlug("localPosition", False)
        # localPosPlug.isChannelBox = False
        # localPosPlug

    @staticmethod
    def creator():
        """ Maya creator function. """
        return DebugMatrix()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to DebugMatrix class. Instances of DebugMatrix will use these attributes to create plugs
        for use in the compute() method.
        """
        mAttr = om2.MFnMatrixAttribute()
        nAttr = om2.MFnNumericAttribute()

        DebugMatrix.inMatrix = mAttr.create("matrixInput", "mtxi", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)
        mAttr.storable = False
        mAttr.keyable = True

        DebugMatrix.inNameColor = nAttr.createColor("nameColor", "nColor")
        nAttr.default = (DebugMatrix.fNameColor.r, DebugMatrix.fNameColor.g, DebugMatrix.fNameColor.b)
        INPUT_ATTR(nAttr)

        DebugMatrix.inMtxColor = nAttr.createColor("matrixColor", "mColor")
        nAttr.default = (DebugMatrix.fMtxColor.r, DebugMatrix.fMtxColor.g, DebugMatrix.fMtxColor.b)
        INPUT_ATTR(nAttr)

        DebugMatrix.inDistance = nAttr.create("distance", "dist", om2.MFnNumericData.kFloat, 0.0)
        INPUT_ATTR(nAttr)

        DebugMatrix.inLineHeight = nAttr.create("lineHeight", "lHeight", om2.MFnNumericData.kFloat, 0.7)
        nAttr.setMin(0.001)
        nAttr.setMax(2.0)
        INPUT_ATTR(nAttr)

        DebugMatrix.addAttribute(DebugMatrix.inMatrix)
        DebugMatrix.addAttribute(DebugMatrix.inNameColor)
        DebugMatrix.addAttribute(DebugMatrix.inMtxColor)
        DebugMatrix.addAttribute(DebugMatrix.inDistance)
        DebugMatrix.addAttribute(DebugMatrix.inLineHeight)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=unused-argument
        return None

    def connectionMade(self, plug, otherPlug, asSrc):
        """This method gets called when connections are made to attributes of this node.
            * plug (MPlug) is the attribute on this node.
            * otherPlug (MPlug) is the attribute on the other node.
            * asSrc (bool) is this plug a source of the connection.
        """
        if plug == DebugMatrix.inMatrix:
            thisMob = self.thisMObject()
            distancePlug = om2.MPlug(thisMob, DebugMatrix.inDistance)
            dagFn = om2.MFnDagNode(otherPlug.node())
            bBox = dagFn.boundingBox
            offset = bBox.width / 2.0
            distancePlug.setFloat(offset + 2.0)
        return omui2.MPxLocatorNode.connectionMade(self, plug, otherPlug, asSrc)

    def connectionBroken(self, plug, otherPlug, asSrc):
        """This method gets called when connections are broken with attributes of this node.
            * plug (MPlug) is the attribute on this node.
            * otherPlug (MPlug) is the attribute on the other node.
            * asSrc (bool) is this plug a source of the connection.
        """
        if plug == DebugMatrix.inMatrix:
            thisMob = self.thisMObject()
            distancePlug = om2.MPlug(thisMob, DebugMatrix.inDistance)
            distancePlug.setFloat(0.0)
        return omui2.MPxLocatorNode.connectionBroken(self, plug, otherPlug, asSrc)

    def drawText(self, mtx, dist, colorList, status, cameraPath, lineH, view=None,
                 drawManager=None):
        """Draw the matrix text.
        """
        mCamera = cameraPath.inclusiveMatrix()
        camFn = om2.MFnCamera(cameraPath)
        thisMob = self.thisMObject()
        worldMtxPlug = om2.MPlug(thisMob, DebugMatrix.inMatrix)
        destPlugList = worldMtxPlug.connectedTo(True, False)
        if len(destPlugList) >= 1:
            node = destPlugList[0].node()
            attr = destPlugList[0].attribute()
            dagFn = om2.MFnDagNode(node)
            name = dagFn.name()
            attrName = "%s   (%s)" % ("  "*len(name), om2.MFnAttribute(attr).name)
            bBox = dagFn.boundingBox
        else:
            attrName = ""
            name = "NO MATRIX INPUT"
            bBox = om2.MBoundingBox()

        offsetY = bBox.height / 2.0

        pntCamera = om2.MPoint(mCamera[12], mCamera[13], mCamera[14])
        pntPos = om2.MPoint(mtx[12] + dist, mtx[13] + offsetY, mtx[14])
        vCamera = pntCamera - pntPos
        distFromCamera = vCamera.length()
        pntLineOffset = om2.MPoint(0.0, (distFromCamera / camFn.focalLength) * lineH, 0.0)
        rowList = []

        pntRow1 = om2.MPoint(mtx[0], mtx[1], mtx[2], mtx[3])
        row1 = "%s | %s | %s | %s" % ("%.3f" % pntRow1.x, "%.3f" % pntRow1.y,
                                      "%.3f" % pntRow1.z, "%.3f" % pntRow1.w)
        rowList.append(row1)
        pntRow2 = om2.MPoint(mtx[4], mtx[5], mtx[6], mtx[7])
        row2 = "%s | %s | %s | %s" % ("%.3f" % pntRow2.x, "%.3f" % pntRow2.y,
                                      "%.3f" % pntRow2.z, "%.3f" % pntRow2.w)
        rowList.append(row2)
        pntRow3 = om2.MPoint(mtx[8], mtx[9], mtx[10], mtx[11])
        row3 = "%s | %s | %s | %s" % ("%.3f" % pntRow3.x, "%.3f" % pntRow3.y,
                                      "%.3f" % pntRow3.z, "%.3f" % pntRow3.w)
        rowList.append(row3)
        pntRow4 = om2.MPoint(mtx[12], mtx[13], mtx[14], mtx[15])
        row4 = "%s | %s | %s | %s" % ("%.3f" % pntRow4.x, "%.3f" % pntRow4.y,
                                      "%.3f" % pntRow4.z, "%.3f" % pntRow4.w)
        rowList.append(row4)

        if status == omui2.M3dView.kActive:
            view.setDrawColor(om2.MColor([0.3, 1.0, 1.0]))
        elif status == omui2.M3dView.kLead:
            view.setDrawColor(om2.MColor([1.0, 1.0, 1.0]))

        if status == omui2.M3dView.kDormant:
            view.setDrawColor(colorList[0])
        view.drawText(name, pntPos, omui2.M3dView.kLeft)

        if status == omui2.M3dView.kDormant:
            view.setDrawColor(colorList[1])
        view.drawText(attrName, pntPos, omui2.M3dView.kLeft)
        if worldMtxPlug.isConnected:
            for i in range(1, 5):
                pos = om2.MPoint(pntPos - (pntLineOffset * i))
                view.drawText(rowList[i-1], pos, omui2.M3dView.kLeft)

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
        mInput = om2.MPlug(thisMob, DebugMatrix.inMatrix).asMDataHandle().asMatrix()
        nameColor = om2.MPlug(thisMob, DebugMatrix.inNameColor).asMDataHandle().asFloatVector()
        mtxColor = om2.MPlug(thisMob, DebugMatrix.inMtxColor).asMDataHandle().asFloatVector()
        dist = om2.MPlug(thisMob, DebugMatrix.inDistance).asFloat()
        lineHeight = om2.MPlug(thisMob, DebugMatrix.inLineHeight).asFloat()
        colorList = om2.MColorArray()
        colorList.append(om2.MColor([nameColor.x, nameColor.y, nameColor.z]))
        colorList.append(om2.MColor([mtxColor.x, mtxColor.y, mtxColor.z]))
        cameraPath = view.getCamera()

        view.beginGL()

        glRenderer = omr1.MHardwareRenderer.theRenderer()
        glFT = glRenderer.glFunctionTable()

        glFT.glPushAttrib(omr1.MGL_CURRENT_BIT)
        glFT.glDisable(omr1.MGL_CULL_FACE)

        self.drawText(mInput, dist, colorList, status, cameraPath, lineHeight, view)

        view.endGL()
        return None


class DebugMatrixData(om2.MUserData):
    """ Custom user data class. """

    def __init__(self):
        """ Constructor. """
        om2.MUserData.__init__(self, False)  # Don't delete after draw

        self.fDormantColor = om2.MColor()
        self.fActiveColor = om2.MColor()
        self.fLeadColor = om2.MColor()
        self.fPntPos = om2.MPoint()
        self.fRow0 = ""
        self.fRow1 = ""
        self.fRow2 = ""
        self.fRow3 = ""
        self.fRow4 = ""
        self.fDist = 2.0


class DebugMatrixDrawOverride(omr2.MPxDrawOverride):
    """ Drawing override to enable to draw in VP2.0. """

    def __init__(self, obj):
        """ Constructor. """
        omr2.MPxDrawOverride.__init__(self, obj, DebugMatrixDrawOverride.draw)

    def supportedDrawAPIs(self):
        """ Select which draw API works. """
        return omr2.MRenderer.kOpenGL | omr2.MRenderer.kDirectX11 | omr2.MRenderer.kOpenGLCoreProfile

    @staticmethod
    def creator(obj):
        """ Maya creator function. """
        return DebugMatrixDrawOverride(obj)

    @staticmethod
    def draw(context, data):
        """ Draw method. """
        # pylint: disable=unused-argument
        return

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
        if not isinstance(data, DebugMatrixData):
            data = DebugMatrixData()

        node = objPath.node()
        mInput = om2.MPlug(node, DebugMatrix.inMatrix).asMDataHandle().asMatrix()
        color = om2.MPlug(node, DebugMatrix.inNameColor).asMDataHandle().asFloatVector()
        dist = om2.MPlug(node, DebugMatrix.inDistance).asFloat()

        pntPos = om2.MPoint(mInput[12], mInput[13], mInput[14])

        pntRow1 = om2.MPoint(mInput[0], mInput[1], mInput[2], mInput[3])
        row1 = "%s | %s | %s | %s" % (str(pntRow1.x), str(pntRow1.y),
                                      str(pntRow1.z), str(pntRow1.w))

        data.fDormantColor = om2.MColor([color.x, color.y, color.z])
        data.fActiveColor = om2.MColor([0.3, 1.0, 1.0])
        data.fLeadColor = om2.MColor([1.0, 1.0, 1.0])

        data.fDist = dist
        data.fPntPos = pntPos
        data.fRow1 = row1

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

        # view.drawText(row1, pntPos, omui2.M3dView.kLeft)
        locatorData = data
        if not isinstance(locatorData, DebugMatrixData):
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

        drawManager.text(locatorData.fPntPos, locatorData.fRow1, omr2.MUIDrawManager.kLeft, dynamic=True)
        # drawManager.mesh(omr2.MUIDrawManager.kTriStrip, locatorData.fQuadList)

        drawManager.endDrawable()
