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


class DebugGeometry(om2.MPxSurfaceShape):
    """ Main class of gfDebugGeometry node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeRegistrantID = ""
    kNodeID = ""

    kPnts = om2.MPointArray([
        om2.MPoint(0.0, 0.0, 0.0),
        om2.MPoint(0.0, 0.0, -4.0),
        om2.MPoint(-4.0, 0.0, -4.0),
        om2.MPoint(-4.0, 0.0, 0.0)
    ])

    def __init__(self):
        """ Constructor. """
        om2.MPxSurfaceShape.__init__(self)

    def postConstructor(self):
        """ Post Constructor. """
        thisMob = self.thisMObject()
        om2.MFnDependencyNode(thisMob).setName("%sShape#" % DebugGeometry.kNodeName)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return DebugGeometry()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to DebugGeometry class. Instances of DebugGeometry will use these attributes to create plugs
        for use in the compute() method.
        """
        return True

    def isBounded(self):
        """isBounded?"""
        return True

    def boundingBox(self):
        """Return the boundingBox"""
        bBox = om2.MBoundingBox()
        for i in range(len(DebugGeometry.kPnts)):
            bBox.expand(DebugGeometry.kPnts[i])
        return bBox

    def getShapeSelectionMask(self):
        """Returns the selection mask of the shape."""
        mask = om2.MSelectionMask(om2.MSelectionMask.kSelectIkHandles)
        return mask


class DebugGeometryUI(omui2.MPxSurfaceShapeUI):
    """ UI class of gfDebugGeometry node. """

    def __init__(self):
        """ Constructor. """
        omui2.MPxSurfaceShapeUI.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return DebugGeometryUI()


class DebugGeometryOverride(omr2.MPxGeometryOverride):
    """ Geometry override to enable to draw in VP2.0. """

    def __init__(self, obj):
        """ Constructor. """
        omr2.MPxGeometryOverride.__init__(self, obj)

    def supportedDrawAPIs(self):
        """ Select which draw API works. """
        return omr2.MRenderer.kOpenGL | omr2.MRenderer.kDirectX11 | omr2.MRenderer.kOpenGLCoreProfile

    @staticmethod
    def creator(obj):
        """ Maya creator function. """
        return DebugGeometryOverride(obj)

    def updateDG(self):
        """ Perform any work required to translate the geometry data that needs to get
        information from the dependency graph. """ 
        return

    def updateRenderItems(self, path, list):
        """
        This method is called for each instance of the associated DAG object whenever the object changes.
        The method is passed the path to the instance and the current list of render items associated with that
        instance. By default the list will contain one render item for each shader assigned to the instance.
        Implementations of this method may add, remove or modify items in the list. Note that removal of items
        created by Maya for assigned shaders is not allowed and will fail. As an alternative this method can
        disable those items so that they do not draw.
            * path [MDagPath] is the path to the instance to update render items for.
            * list [MRenderItemList] is the current render item list, items may be modified, added or removed.
        """
        # pylint: disable=unused-argument
        return

    def populateGeometry(self, requirements, renderItems, data):
        """
        Implementations of this method should create and populate vertex and index buffers on the MGeometry
        instance 'data' in order to fulfill all of the geometry requirements defined by the 'requirements'
        parameter. Failure to do so will result in the object either drawing incorrectly or not drawing at all.
        The geometry requirements will ask for index buffers on demand. Implementations can force the geometry
        requirements to update index buffers by calling MHWRender::MRenderer::setGeometryDrawDirty() with
        topologyChanged setting to true.
            * requirements [MGeometryRequirements] is the requirements that need to be satisfied.
            * renderItems [MRenderItemList] is the list of render items that need to be updated.
            * data [MGeometry] is the container for the geometry data.
        """
        # pylint: disable=unused-argument
        return

    def cleanUp(self):
        """ Called after all other stages are completed. Clean up any cached data stored from the updateDG()
        phase. """
        return

    def hasUIDrawables(self):
        """ Has ui drawables? """
        return True

    def addUIDrawables(self, path, drawManager, frameContext):
        """
        For each instance of the object, besides the render items updated in updateRenderItems() there is also
        a render item list for rendering simple UI elements. This stage gives the plugin access to MUIDrawManager
        which aids in drawing simple geometry like line, circle, rectangle, text, etc. If you are not going to
        override this function, please don't make 'hasUIDrawables()' return True or there may be some wasted
        performance overhead.
            * path [MDagPath] is the path to the instance to update auxiliary items for (this shape node).
            * drawManager [MUIDrawManager] is the draw manager used to draw simple geometry.
            * frameContext [MFrameContext] is the frame level context information.
        """
        displayStyle = frameContext.getDisplayStyle()

        activeView = omui2.M3dView.active3dView()
        displayXRay = activeView.xrayJoints()

        drawManager.beginDrawable(omr2.MUIDrawManager.kSelectable)
        if (displayStyle & omr2.MFrameContext.kXrayActiveComponents):
            om2.MGlobal.displayInfo("Opa! Xray on!!! [%s]" % displayStyle)
            drawManager.beginDrawInXray()

        drawManager.setColor(om2.MColor([1.0, 0.0, 0.0, 0.3]))
        drawManager.mesh(
            omr2.MUIDrawManager.kTriStrip,
            DebugGeometry.kPnts,
            None,
            None,
            om2.MUintArray([0, 1, 3, 2])
        )

        if (displayStyle & omr2.MFrameContext.kXrayActiveComponents):
            drawManager.endDrawInXray()
        drawManager.endDrawable()
