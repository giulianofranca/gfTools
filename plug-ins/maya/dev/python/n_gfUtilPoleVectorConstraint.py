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
    Custom aim constraint. Aim an object to another.

Attributes:
    * Up Vector Type: The type of calculation of the up vector.
    * Offset: The matrix offset between the source and target objects.
    * World Up Vector: The scene world up vector.
    * World Up Matrix: The world matrix of the up object.
    * Target World Matrix: The world matrix of the target object.
    * Target Weight: The weight of calculation.
    * Constraint World Matrix: The world matrix of the constrainted object.
    * Constraint Parent Inverse Matrix: The world inverse matrix of the parent of the constrainted object.
    * Constraint Joint Orient: The joint orient of the constrainted object (if exists).
    * Constraint Rotate Order: The rotate order of the constrainted object.
    * Constraint Parent Scale: The local scale of the parent of the constrainted object.
    * Out Constraint: The result euler rotation of the constraint.

Todo:
    * NDA

Sources:
    * NDA

This code supports Pylint. Rc file in project.
"""
import maya.api._OpenMaya_py2 as om2


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


class PoleVectorConstraint(om2.MPxNode):
    """ Main class of gfUtilPoleVectorConstraint node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inRootWMtx = om2.MObject()
    inTargetWMtx = om2.MObject()
    inTargetWeight = om2.MObject()
    inConstParInvMtx = om2.MObject()
    inRestPosition = om2.MObject()
    inNormalizeOutput = om2.MObject()
    outConstraint = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return PoleVectorConstraint()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to PoleVectorConstraint class. Instances of PoleVectorConstraint will use these attributes to create plugs
        for use in the compute() method.
        """
        mAttr = om2.MFnMatrixAttribute()
        nAttr = om2.MFnNumericAttribute()

        PoleVectorConstraint.inRootWMtx = mAttr.create("rootWorldMatrix", "rootm", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        PoleVectorConstraint.inTargetWMtx = mAttr.create("targetWorldMatrix", "tgtm", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        PoleVectorConstraint.inTargetWeight = nAttr.create("targetWeight", "tw", om2.MFnNumericData.kDouble, 1.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        PoleVectorConstraint.inConstParInvMtx = mAttr.create("constraintParentInverseMatrix", "cpim", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        PoleVectorConstraint.inRestPosition = nAttr.createPoint("restPosition", "rest")
        nAttr.writable = True
        nAttr.readable = True
        nAttr.storable = True
        nAttr.keyable = False

        PoleVectorConstraint.inNormalizeOutput = nAttr.create("normalizeOutput", "normalize", om2.MFnNumericData.kBoolean, False)
        INPUT_ATTR(nAttr)

        PoleVectorConstraint.outConstraint = nAttr.createPoint("constraint", "const")
        OUTPUT_ATTR(nAttr)

        PoleVectorConstraint.addAttribute(PoleVectorConstraint.inRootWMtx)
        PoleVectorConstraint.addAttribute(PoleVectorConstraint.inTargetWMtx)
        PoleVectorConstraint.addAttribute(PoleVectorConstraint.inTargetWeight)
        PoleVectorConstraint.addAttribute(PoleVectorConstraint.inConstParInvMtx)
        PoleVectorConstraint.addAttribute(PoleVectorConstraint.inRestPosition)
        PoleVectorConstraint.addAttribute(PoleVectorConstraint.inNormalizeOutput)
        PoleVectorConstraint.addAttribute(PoleVectorConstraint.outConstraint)
        PoleVectorConstraint.attributeAffects(PoleVectorConstraint.inRootWMtx, PoleVectorConstraint.outConstraint)
        PoleVectorConstraint.attributeAffects(PoleVectorConstraint.inTargetWMtx, PoleVectorConstraint.outConstraint)
        PoleVectorConstraint.attributeAffects(PoleVectorConstraint.inTargetWeight, PoleVectorConstraint.outConstraint)
        PoleVectorConstraint.attributeAffects(PoleVectorConstraint.inConstParInvMtx, PoleVectorConstraint.outConstraint)
        PoleVectorConstraint.attributeAffects(PoleVectorConstraint.inRestPosition, PoleVectorConstraint.outConstraint)
        PoleVectorConstraint.attributeAffects(PoleVectorConstraint.inNormalizeOutput, PoleVectorConstraint.outConstraint)

    def connectionMade(self, plug, otherPlug, asSrc):
        """This method gets called when connections are made to attributes of this node.
            * plug (MPlug) is the attribute on this node.
            * otherPlug (MPlug) is the attribute on the other node.
            * asSrc (bool) is this plug a source of the connection.
        """
        if plug == PoleVectorConstraint.inTargetWMtx:
            thisMob = self.thisMObject()
            restPosPlug = om2.MPlug(thisMob, PoleVectorConstraint.inRestPosition)
            targetMob = otherPlug.asMObject()
            mtxDataFn = om2.MFnMatrixData(targetMob)
            mTarget = mtxDataFn.matrix()
            vTarget = om2.MFloatVector(mTarget[12], mTarget[13], mTarget[14])
            restPosHdle = restPosPlug.asMDataHandle()
            restPosHdle.setMFloatVector(vTarget)
            restPosPlug.setMDataHandle(restPosHdle)
        return om2.MPxNode.connectionMade(self, plug, otherPlug, asSrc)


    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != PoleVectorConstraint.outConstraint:
            return om2.kUnknownParameter

        mRoot = dataBlock.inputValue(PoleVectorConstraint.inRootWMtx).asMatrix()
        mTarget = dataBlock.inputValue(PoleVectorConstraint.inTargetWMtx).asMatrix()
        mConstParInv = dataBlock.inputValue(PoleVectorConstraint.inConstParInvMtx).asMatrix()
        targetWeight = dataBlock.inputValue(PoleVectorConstraint.inTargetWeight).asDouble()
        vRest = om2.MVector(dataBlock.inputValue(PoleVectorConstraint.inRestPosition).asFloat3())
        normalize = dataBlock.inputValue(PoleVectorConstraint.inNormalizeOutput).asBool()

        vRoot = om2.MVector(mRoot[12], mRoot[13], mRoot[14])
        vTarget = om2.MVector(mTarget[12], mTarget[13], mTarget[14])

        vPoleDirection = (vTarget - vRoot) * mConstParInv
        vRestDirection = (vRest - vRoot) * mConstParInv
        vPole = (1.0 - targetWeight) * vRestDirection + targetWeight * vPoleDirection

        vResult = om2.MFloatVector(vPole)
        if normalize:
            vResult.normalize()
        outConstHdle = dataBlock.outputValue(PoleVectorConstraint.outConstraint)
        outConstHdle.setMFloatVector(vResult)
        outConstHdle.setClean()
