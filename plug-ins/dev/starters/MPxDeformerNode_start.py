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
    * cmds.deformer(type="gfTestDeformer")

Requirements:
    * Maya 2017 or above.

Todo:
    * NDA

Sources:
    * http://www.chadvernon.com/blog/resources/maya-api-programming/deformers/
    * http://rodolphe-vaillant.fr/?e=99
    * https://vimeo.com/263594559
    * https://github.com/gbarlier/relax_node/blob/master/python/relax_node.py

This code supports Pylint. Rc file in project.
"""
# pylint: disable=no-name-in-module

import sys
import math
import maya.cmds as cmds
import maya.OpenMaya as om1
import maya.OpenMayaMPx as ompx


def INPUT_ATTR(FNATTR):
    """ Configure a input attribute. """
    # pylint: disable=invalid-name
    FNATTR.setWritable(True)
    FNATTR.setReadable(True)
    FNATTR.setStorable(True)
    FNATTR.setKeyable(True)


def OUTPUT_ATTR(FNATTR):
    """ Configure a output attribute. """
    # pylint: disable=invalid-name
    FNATTR.setWritable(False)
    FNATTR.setReadable(True)
    FNATTR.setStorable(False)
    FNATTR.setKeyable(False)


class TestDeformer(ompx.MPxDeformerNode):
    """ Main class of gfDeformer node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inAmplitude = om1.MObject()
    inDisplace = om1.MObject()
    inMatrix = om1.MObject()

    def __init__(self):
        """ Constructor. """
        ompx.MPxDeformerNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return ompx.asMPxPtr(TestDeformer())

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to TestNode class. Instances of TestNode will use these attributes to create plugs
        for use in the compute() method.
        """
        nAttr = om1.MFnNumericAttribute()
        mAttr = om1.MFnMatrixAttribute()

        TestDeformer.inAmplitude = nAttr.create("amplitude", "amplitude", om1.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        TestDeformer.inDisplace = nAttr.create("displace", "displace", om1.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(10.0)
        INPUT_ATTR(nAttr)

        TestDeformer.inMatrix = mAttr.create("matrix", "matrix")
        INPUT_ATTR(mAttr)

        TestDeformer.addAttribute(TestDeformer.inAmplitude)
        TestDeformer.addAttribute(TestDeformer.inDisplace)
        TestDeformer.addAttribute(TestDeformer.inMatrix)

        TestDeformer.attributeAffects(TestDeformer.inAmplitude, ompx.cvar.MPxGeometryFilter_outputGeom)
        TestDeformer.attributeAffects(TestDeformer.inDisplace, ompx.cvar.MPxGeometryFilter_outputGeom)
        TestDeformer.attributeAffects(TestDeformer.inMatrix, ompx.cvar.MPxGeometryFilter_outputGeom)

        cmds.makePaintable(TestDeformer.kNodeName, "weights", at="multiFloat", sm="deformer")

    def deform(self, dataBlock, geoIter, mtx, multiIndex):
        """This method performs the deformation algorithm.
        The geometry iterator passed to this method is in local space and not world space. To convert
        points to world space use the matrix that is suppied.
            * dataBlock [MDataBlock] is the node's datablock.
            * geoIter [MItGeometry] is an iterator for the current geometry being deformed.
            * mtx [MMatrix] is the geometry's world space transformation matrix.
            * multiIndex [int] is the index corresponding to the requested output geometry.
        """
        # pylint: disable=unused-argument
        envelope = dataBlock.inputValue(ompx.cvar.MPxGeometryFilter_envelope).asFloat()
        amplitude = dataBlock.inputValue(TestDeformer.inAmplitude).asFloat()
        displace = dataBlock.inputValue(TestDeformer.inDisplace).asFloat()
        inputArrayHandle = dataBlock.outputArrayValue(ompx.cvar.MPxGeometryFilter_input)
        inputArrayHandle.jumpToElement(multiIndex)
        inputElement = inputArrayHandle.outputValue()
        inMesh = inputElement.child(ompx.cvar.MPxGeometryFilter_inputGeom).asMesh()
        mMatrix = dataBlock.inputValue(TestDeformer.inMatrix).asMatrix()

        vTrans = om1.MVector(mMatrix(3, 0), mMatrix(3, 1), mMatrix(3, 2))

        meshFn = om1.MFnMesh(inMesh)
        normalsArray = om1.MFloatVectorArray()
        meshFn.getVertexNormals(False, normalsArray, om1.MSpace.kObject)
        verticesArray = om1.MPointArray()

        while not geoIter.isDone():
            index = geoIter.index()
            pntPos = geoIter.position()
            weight = self.weightValue(dataBlock, multiIndex, index)
            if weight != 0:
                pntPos.x = pntPos.x + math.sin(index + displace - vTrans[0]) * amplitude * normalsArray[index].x * weight * envelope
                pntPos.y = pntPos.y + math.sin(index + displace - vTrans[0]) * amplitude * normalsArray[index].y * weight * envelope
                pntPos.z = pntPos.z + math.sin(index + displace - vTrans[0]) * amplitude * normalsArray[index].z * weight * envelope
            verticesArray.append(pntPos)
            geoIter.next()
        geoIter.setAllPositions(verticesArray)

    def accessoryNodeSetup(self, dagMod):
        """This method is called by the "deformer -type" command when your node is specified.
        This method can be used to create and attach accessory nodes if your plugin node requires
        them. To do so, override this method, and provide the creation and attachment commands to
        the MDagModifier that is passed as input to the method.
            * dagMod [MDagModifier] is the dag modifier to which the method will add commands.
        """
        locMob = dagMod.createNode("locator")
        dagMod.renameNode(locMob, "%sHandle#" % TestDeformer.kNodeName)
        nodeFn = om1.MFnDependencyNode(locMob)
        mtxWPlug = nodeFn.findPlug("worldMatrix")
        wMtxAttr = mtxWPlug.attribute()

        status = dagMod.connect(locMob, wMtxAttr, self.thisMObject(), TestDeformer.inMatrix)
        return status

    def accessoryAttribute(self):
        """This method returns an MObject for the attribute to which an accessory shape is connected.
        If the accessory shape is deleted, the deformer node will automatically be deleted.
        """
        return TestDeformer.inMatrix


def REGISTER_NODE(NODE, PLUGIN):
    """ Register a MPxNode. """
    # pylint: disable=invalid-name
    try:
        PLUGIN.registerNode(NODE.kNodeName, NODE.kNodeID, NODE.creator,
                            NODE.initialize, ompx.MPxNode.kDeformerNode, NODE.kNodeClassify) #, NODE.kNodeClassify)
    except BaseException:
        sys.stderr.write("Failed to register node: %s" % NODE.kNodeName)
        raise

def DEREGISTER_NODE(NODE, PLUGIN):
    """ Deregister a MPxNode. """
    # pylint: disable=invalid-name
    try:
        PLUGIN.deregisterNode(NODE.kNodeID)
    except BaseException:
        sys.stderr.write("Failed to deregister node: %s" % NODE.kNodeName)
        raise


kAuthor = "Giuliano Franca"
kVersion = "1.0"
kRequiredAPIVersion = "Any"

TestDeformer.kNodeName = "gfTestDeformer"
TestDeformer.kNodeClassify = "deformer/geoemtry"
TestDeformer.kNodeID = om1.MTypeId(0x000fff)


def initializePlugin(mobject):
    """ Initializes the plug-in. """
    mPlugin = ompx.MFnPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion)

    REGISTER_NODE(TestDeformer, mPlugin)


def uninitializePlugin(mobject):
    """ Unitializes the plug-in. """
    mPlugin = ompx.MFnPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion)

    DEREGISTER_NODE(TestDeformer, mPlugin)
