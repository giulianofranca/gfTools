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
    * Figure out how to select priority the control.
    * Fix the evaluation of the node.
    * Create MouseHover event with custom ray-tracing algorithm.
    * Review mesh iteration. It is necessary to iterate all the geometry?
    * Add the ability to calculate using GPU (OpenCL)
    * Learn more about Evaluation Manager and Dependency Graph on Maya to optimize the node.
    * Template and reference types of drawing.
    * Create mesh using triangles

Sources:
    * https://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__cpp_ref_ui_draw_manager_2ui_draw_manager_8cpp_example_html
    * https://github.com/PixarAnimationStudios/OpenSubdiv/blob/master/regression/far_regression/example_createMesh.py
    * https://github.com/alicevision/mayaAPI/blob/master/2016.sp1/linux/devkit/plug-ins/scripted/pyApiMeshShape.py
    * https://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__cpp_ref__abc_export_2_maya_mesh_writer_8cpp_example_html
    * https://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__cpp_ref_squares_node_no_depth_test_2squares_node_no_depth_test_8cpp_example_html

This code supports Pylint. Rc file in project.
"""
# pylint: disable=no-name-in-module

import time
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


class MeshController(omui2.MPxLocatorNode):
    """ Main class of gfMeshController node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeRegistrantID = ""
    kNodeID = ""

    inIndexList = om2.MObject()
    inOffset = om2.MObject()
    inMesh = om2.MObject()
    inColor = om2.MObject()
    inXray = om2.MObject()

    meshVtxPositions = om2.MPointArray()
    meshVtxIndices = om2.MUintArray()
    meshVtxNormals = om2.MVectorArray()
    bBox = om2.MBoundingBox()

    def __init__(self):
        """ Constructor. """
        omui2.MPxLocatorNode.__init__(self)

    def postConstructor(self):
        """ Post Constructor. """
        thisMob = self.thisMObject()
        om2.MFnDependencyNode(thisMob).setName("%sShape#" % MeshController.kNodeName)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return MeshController()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to MeshController class. Instances of MeshController will use these attributes to create plugs
        for use in the compute() method.
        """
        tAttr = om2.MFnTypedAttribute()
        nAttr = om2.MFnNumericAttribute()

        MeshController.inIndexList = tAttr.create("indexList", "index", om2.MFnData.kString)
        INPUT_ATTR(tAttr)

        MeshController.inOffset = nAttr.create("offset", "offset", om2.MFnNumericData.kFloat, 0.0)
        INPUT_ATTR(nAttr)

        MeshController.inMesh = tAttr.create("controlMesh", "controlMesh", om2.MFnData.kMesh)
        INPUT_ATTR(tAttr)

        MeshController.inColor = nAttr.createColor("color", "color")
        nAttr.default = (1.0, 0.455, 0.086)
        INPUT_ATTR(nAttr)

        MeshController.inXray = nAttr.create("xray", "xray", om2.MFnNumericData.kBoolean, False)
        INPUT_ATTR(nAttr)

        MeshController.addAttribute(MeshController.inIndexList)
        MeshController.addAttribute(MeshController.inMesh)
        MeshController.addAttribute(MeshController.inOffset)
        MeshController.addAttribute(MeshController.inColor)
        MeshController.addAttribute(MeshController.inXray)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=unused-argument
        return

    def connectionMade(self, plug, otherPlug, asSrc):
        """
        This method gets called when connections are made to attributes of this node.
            * plug (MPlug) is the attribute on this node.
            * otherPlug (MPlug) is the attribute on the other node.
            * asSrc (bool) is this plug a source of the connection.
        """
        # generate mesh points here initially
        return om2.MPxNode.connectionMade(self, plug, otherPlug, asSrc)

    def connectionBroken(self, plug, otherPlug, asSrc):
        """This method gets called when connections are made to attributes of this node.
            * plug (MPlug) is the attribute on this node.
            * otherPlug (MPlug) is the attribute on the other node.
            * asSrc (bool) is this plug a source of the connection.
        """
        return om2.MPxNode.connectionBroken(self, plug, otherPlug, asSrc)

    def setDependentsDirty(self, plugBeingDirtied, affectedPlugs):
        """
        This method can be overridden in user defined nodes to specify which plugs should be set dirty based
        upon an input plug {plugBeingDirtied} which Maya is marking dirty.
        The list of plugs for Maya to mark dirty is returned by the plug array {affectedPlugs}.
        You must not cause any dependency graph computations.
            * plugBeingDirtied [MPlug] is the plug being dirtied.
            * affectedPlugs [MPlugArray] is the list of dirty plugs returned by Maya.
        """
        # pylint: disable=unused-argument
        if (plugBeingDirtied == MeshController.inIndexList or
                plugBeingDirtied == MeshController.inMesh):
            self.signalDirtyToViewport()

    def preEvaluation(self, context, evaluationNode):
        """ Called before this node is evaluated by Evaluation Manager.
            * context [MDGContext] is the context which the evaluation is happening.
            * evaluationNode [MEvaluationNode] the evaluation node which contains information
                about the dirty plugs that are about to be evaluated for the context.
                Should be only used to query information.
        """
        if not context.isNormal():
            return
        if (evaluationNode.dirtyPlugExists(MeshController.inMesh) or
                evaluationNode.dirtyPlugExists(MeshController.inIndexList) or
                evaluationNode.dirtyPlugExists(MeshController.inOffset)):
            omr2.MRenderer.setGeometryDrawDirty(self.thisMObject())

    @staticmethod
    def listToMIntArray(strList):
        """ Convert a list of int to a MIntArray instance. """
        # pylint: disable=undefined-variable
        instance = om2.MIntArray()
        for i in strList:
            try:
                instance.append(int(i))
            except ValueError:
                pass
        return instance

    @staticmethod
    def generateMesh(meshMob, faceIndicesStr):
        """ Find the info of the geometry who will be drawed. """
        meshFn = om2.MFnMesh(meshMob)

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
        # NO DRAWING IN VIEWPORT 1.0, JUST RETURN
        return

    def isBounded(self):
        """isBounded?"""
        return False


class MeshControllerData(om2.MUserData):
    """ Custom user data class. """

    def __init__(self):
        """ Constructor. """
        om2.MUserData.__init__(self, False)  # Don't delete after draw

        self.fColor = om2.MColor()
        self.fVtxPositions = []
        # self.fVtxPositions = om2.MPointArray()


class MeshControllerDrawOverride(omr2.MPxDrawOverride):
    """ Drawing override to enable to draw in VP2.0. """

    def __init__(self, obj):
        """ Constructor. """
        omr2.MPxDrawOverride.__init__(self, obj, MeshControllerDrawOverride.draw)

    def supportedDrawAPIs(self):
        """ Select which draw API works. """
        return omr2.MRenderer.kOpenGL | omr2.MRenderer.kDirectX11 | omr2.MRenderer.kOpenGLCoreProfile

    @staticmethod
    def creator(obj):
        """ Maya creator function. """
        return MeshControllerDrawOverride(obj)

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
        return om2.MBoundingBox()

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
        return om2.MUserData()

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
        return
