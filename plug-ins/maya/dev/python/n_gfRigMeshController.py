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

Sources:
    * https://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__cpp_ref_ui_draw_manager_2ui_draw_manager_8cpp_example_html

This code supports Pylint. Rc file in project.
"""
# pylint: disable=no-name-in-module

import time
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

    ctrlVertices = []
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

        MeshController.addAttribute(MeshController.inIndexList)
        MeshController.addAttribute(MeshController.inOffset)
        MeshController.addAttribute(MeshController.inMesh)
        MeshController.addAttribute(MeshController.inColor)

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
    def getGeometryPoints(meshMob, indexStr, offset, transform):
        """ Find the info of the geometry who will be drawed. """
        # vtxNormals = []
        # vtxPositions = []

        # if not meshMob.isNull():
        #     polyIndexList = MeshController.listToMIntArray(indexStr.split(","))
        #     itPoly = om2.MItMeshPolygon(meshMob)
        #     while not itPoly.isDone():
        #         if itPoly.index() in polyIndexList:
        #             vtxNormals.append(itPoly.getNormals())
        #             vtxPositions.append(itPoly.getPoints(om2.MSpace.kWorld))
        #         itPoly.next(None)

        # return [vtxNormals, vtxPositions]

        #==============================================================================
        # # 47 FPS AVERAGE WITH NO EDGES | 27 FPS AVERAGE WITH EDGES
        # vtxNormals = []
        # vtxPositions = []

        # if not meshMob.isNull():
        #     polyIndexList = MeshController.listToMIntArray(indexStr.split(","))
        #     itPoly = om2.MItMeshPolygon(meshMob)
        #     for index in polyIndexList:
        #         itPoly.setIndex(index)
        #         vtxNormals.append(itPoly.getNormals())
        #         vtxPositions.append(itPoly.getPoints(om2.MSpace.kWorld))

        # return [vtxNormals, vtxPositions]

        #==============================================================================
        # # 45 FPS AVERAGE WITH NO EDGES | 25 FPS AVERAGE WITH EDGES
        # meshVtxPos = om2.MPointArray()
        # vtxIndexList = []
        # vtxPositions = []

        # if not meshMob.isNull():
        #     polyIndexList = MeshController.listToMIntArray(indexStr.split(","))
        #     meshFn = om2.MFnMesh(meshMob)
        #     meshVtxPos = meshFn.getPoints(om2.MSpace.kWorld)
        #     for index in polyIndexList:
        #         vtxIndexList.append(meshFn.getPolygonVertices(index))
        #     for poly in vtxIndexList:
        #         pntArray = om2.MPointArray()
        #         for pnt in poly:
        #             pntArray.append(meshVtxPos[pnt])
        #         vtxPositions.append(pntArray)

        # return [[], vtxPositions]

        #==============================================================================
        # 47 FPS AVERAGE WITH NO EDGES | 27 FPS AVERAGE WITH EDGES
        outPnts = []

        pntOffTolerance = 0.01
        tolerance = offset + pntOffTolerance
        bBox = om2.MBoundingBox()

        if not meshMob.isNull():
            polyIndexList = MeshController.listToMIntArray(indexStr.split(","))
            itPoly = om2.MItMeshPolygon(meshMob)
            for index in polyIndexList:
                itPoly.setIndex(index)
                polyVtxNormals = itPoly.getNormals()
                polyVtxPos = itPoly.getPoints(om2.MSpace.kWorld)
                outPolyVtxPos = om2.MPointArray()
                for i, pnt in enumerate(polyVtxPos):
                    curPnt = pnt
                    curNormal = polyVtxNormals[i]
                    outPnt = (curPnt + (curNormal * tolerance)) * transform
                    bBox.expand(outPnt)
                    outPolyVtxPos.append(outPnt)
                outPnts.append(outPolyVtxPos)

        MeshController.ctrlVertices = outPnts
        MeshController.bBox = bBox

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=unused-argument
        return

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
        # thisMob = self.thisMObject()
        # mWorldInv = path.inclusiveMatrixInverse()
        # indexStr = om2.MPlug(thisMob, MeshController.inIndexList).asString()
        # offset = om2.MPlug(thisMob, MeshController.inOffset).asFloat()
        # mesh = om2.MPlug(thisMob, MeshController.inMesh).asMDataHandle().asMesh()
        # color = om2.MPlug(thisMob, MeshController.inColor).asMDataHandle().asFloatVector()

        # # If plugs are dirty calculate the geometry points
        # MeshController.getGeometryPoints(mesh, indexStr, offset, mWorldInv)

        # view.beginGL()

        # glRenderer = omr1.MHardwareRenderer.theRenderer()
        # glFT = glRenderer.glFunctionTable()

        # glFT.glPushAttrib(omr1.MGL_CURRENT_BIT)
        # glFT.glDisable(omr1.MGL_CULL_FACE)
        # glFT.glEnable(omr1.MGL_BLEND)
        # glFT.glBlendFunc(omr1.MGL_SRC_ALPHA, omr1.MGL_ONE_MINUS_SRC_ALPHA)

        # color = om2.MFloatVector(color.x, color.y, color.z)
        # if status == view.kDormant:
        #     # Not selected
        #     alpha = 0.25
        # elif status == view.kActive:
        #     # Multiselection
        #     alpha = 0.65
        # elif status == view.kLead:
        #     # Selected
        #     alpha = 0.5

        # if style == view.kFlatShaded or style == view.kGouraudShaded:
        #     glFT.glColor4f(color.x, color.y, color.z, alpha)
        #     for poly in MeshController.ctrlVertices:
        #         glFT.glBegin(omr1.MGL_POLYGON)
        #         for pnt in poly:
        #             glFT.glVertex3f(pnt.x, pnt.y, pnt.z)
        #         glFT.glEnd()

        # if style == view.kWireFrame:
        #     glFT.glColor4f(color.x, color.y, color.z, 1.0)
        #     glFT.glBegin(omr1.MGL_LINES)
        #     for poly in MeshController.ctrlVertices:
        #         for i, pnt in enumerate(poly):
        #             glFT.glVertex3f(pnt.x, pnt.y, pnt.z)
        #             if i == len(poly) - 1:
        #                 glFT.glVertex3f(poly[0].x, poly[0].y, poly[0].z)
        #             else:
        #                 glFT.glVertex3f(poly[i+1].x, poly[i+1].y, poly[i+1].z)
        #     glFT.glEnd()

        # glFT.glPopAttrib()

        # view.endGL()
        return

    def isBounded(self):
        """isBounded?"""
        return True

    def isTransparent(self):
        """isTransparent?"""
        return True

    def boundingBox(self):
        """Return the boundingBox"""
        if not MeshController.ctrlVertices:
            thisMob = self.thisMObject()
            thisPath = om2.MDagPath.getAPathTo(thisMob)
            transformPath = om2.MDagPath.getAPathTo(om2.MFnDagNode(thisPath).parent(0))
            mWorldInv = transformPath.inclusiveMatrixInverse()
            indexStr = om2.MPlug(thisMob, MeshController.inIndexList).asString()
            offset = om2.MPlug(thisMob, MeshController.inOffset).asFloat()
            mesh = om2.MPlug(thisMob, MeshController.inMesh).asMDataHandle().asMesh()
            MeshController.getGeometryPoints(mesh, indexStr, offset, mWorldInv)
        return MeshController.bBox

    def preEvaluation(self, context, evaluationNode):
        """ Called before this node is evaluated by Evaluation Manager.
            * context [MDGContext] is the context which the evaluation is happening.
            * evaluationNode [MEvaluationNode] the evaluation node which contains information
                about the dirty plugs that are about to be evaluated for the context.
                Should be only used to query information.
        """
        if context.isNormal():
            if evaluationNode.dirtyPlugExists(MeshController.inOffset):
                omr2.MRenderer.setGeometryDrawDirty(self.thisMObject())
            elif evaluationNode.dirtyPlugExists(MeshController.inIndexList):
                omr2.MRenderer.setGeometryDrawDirty(self.thisMObject())
            elif evaluationNode.dirtyPlugExists(MeshController.inMesh):
                omr2.MRenderer.setGeometryDrawDirty(self.thisMObject())


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
        if not MeshController.ctrlVertices:
            thisMob = objPath.node()
            thisPath = om2.MDagPath.getAPathTo(thisMob)
            transformPath = om2.MDagPath.getAPathTo(om2.MFnDagNode(thisPath).parent(0))
            mWorldInv = transformPath.inclusiveMatrixInverse()
            indexStr = om2.MPlug(thisMob, MeshController.inIndexList).asString()
            offset = om2.MPlug(thisMob, MeshController.inOffset).asFloat()
            mesh = om2.MPlug(thisMob, MeshController.inMesh).asMDataHandle().asMesh()
            MeshController.getGeometryPoints(mesh, indexStr, offset, mWorldInv)
        return MeshController.bBox

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
        startTime = time.time()
        data = oldData
        if not isinstance(data, MeshControllerData):
            data = MeshControllerData()

        node = objPath.node()
        transformPath = om2.MDagPath.getAPathTo(om2.MFnDagNode(objPath).parent(0))
        mWorldInv = transformPath.inclusiveMatrixInverse()
        indexStr = om2.MPlug(node, MeshController.inIndexList).asString()
        offset = om2.MPlug(node, MeshController.inOffset).asFloat()
        mesh = om2.MPlug(node, MeshController.inMesh).asMDataHandle().asMesh()
        color = om2.MPlug(node, MeshController.inColor).asMDataHandle().asFloatVector()

        # If plugs are dirty calculate the geometry points
        MeshController.getGeometryPoints(mesh, indexStr, offset, mWorldInv)

        data.fVtxPositions = MeshController.ctrlVertices

        status = omr2.MGeometryUtilities.displayStatus(objPath)
        if status == omr2.MGeometryUtilities.kDormant:
            # Not selected
            alpha = 0.25
        elif status == omr2.MGeometryUtilities.kActive:
            # Multiselection
            alpha = 0.65
        elif status == omr2.MGeometryUtilities.kLead:
            # Selected
            alpha = 0.5
        data.fColor = om2.MColor([color.x, color.y, color.z, alpha])

        runTime = round((time.time() - startTime) * 1000, 5)
        om2.MGlobal.displayInfo("prepareForDraw time: %s ms" % str(runTime))
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
        # ========================================
        # RUNTIME DEBUG 1250 FACES
        # With VP1.0 implementation
        #     25 ms to prepare and 50 ms to draw
        # Without VP1.0 implementation
        #     20 ms to prepare and 40 ms to draw
        # With only one mesh call instead of one per poly
        #     NDA
        # ========================================
        startTime = time.time()
        locatorData = data
        if not isinstance(locatorData, MeshControllerData):
            return

        drawManager.beginDrawable(omr2.MUIDrawManager.kSelectable)
        mode = omr2.MUIDrawManager.kTriStrip
        index = om2.MUintArray([0, 1, 3, 2])

        drawManager.setColor(locatorData.fColor)

        drawManager.setDepthPriority(omr2.MRenderItem.sSelectionDepthPriority)
        for poly in locatorData.fVtxPositions:
            drawManager.mesh(mode, poly, None, None, index)

        drawManager.endDrawable()
        runTime = round((time.time() - startTime) * 1000, 5)
        om2.MGlobal.displayInfo("draw time: %s ms" % str(runTime))
        return
