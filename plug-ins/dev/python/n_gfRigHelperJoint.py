# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfRigHelperJoint node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.

Requirements:
    Maya 2017 or above.

Todo:
    * Get the two sources and their respectives offsets.
    * Add the two matrices blended.
    * Multiply by the target parent inverse matrix.
    * Decompose a euler rotation from this matrix.
    * Get the main source and the respective offset.
    * Multiply by the target parent inverse matrix.
    * Decompose a vector translate from this matrix.

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


class HelperJoint(om2.MPxNode):
    """ Main class of gfRigHelperJoint node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inSourceMtx1 = om2.MObject()            # Shin
    inSourceMtx2 = om2.MObject()            # Thigh
    inSource1Offset = om2.MObject()         # Jnt to Shin offset
    inSource2Offset = om2.MObject()         # Jnt to Thigh offset
    inParentInverseMtx = om2.MObject()      # Parent inverse matrix
    inPositiveMult = om2.MObject()          # Positive multiplier
    inNegativeMult = om2.MObject()          # Negative multiplier
    outMtx = om2.MObject()                  # The result joint matrix in worldSpace

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return HelperJoint()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to HelperJoint class. Instances of HelperJoint will use these attributes to create plugs
        for use in the compute() method.
        """
        nAttr = om2.MFnNumericAttribute()
        mAttr = om2.MFnMatrixAttribute()

        HelperJoint.inSourceMtx1 = mAttr.create("sourceMtx1", "smtx1", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        HelperJoint.inSourceMtx2 = mAttr.create("sourceMtx2", "smtx2", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        HelperJoint.inSource1Offset = mAttr.create("sourceOffset1", "so1", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        HelperJoint.inSource2Offset = mAttr.create("sourceOffset2", "so2", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        HelperJoint.inParentInverseMtx = mAttr.create("parentInverseMatrix", "pim", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        HelperJoint.inPositiveMult = nAttr.create("positiveMultiplier", "posm", om2.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0.0)
        INPUT_ATTR(nAttr)

        HelperJoint.inNegativeMult = nAttr.create("negativeMultiplier", "negm", om2.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0.0)
        INPUT_ATTR(nAttr)

        HelperJoint.outMtx = mAttr.create("outMatrix", "omtx", om2.MFnMatrixAttribute.kDouble)
        OUTPUT_ATTR(mAttr)

        HelperJoint.addAttribute(HelperJoint.inSourceMtx1)
        HelperJoint.addAttribute(HelperJoint.inSourceMtx2)
        HelperJoint.addAttribute(HelperJoint.inSource1Offset)
        HelperJoint.addAttribute(HelperJoint.inSource2Offset)
        HelperJoint.addAttribute(HelperJoint.inParentInverseMtx)
        HelperJoint.addAttribute(HelperJoint.inPositiveMult)
        HelperJoint.addAttribute(HelperJoint.inNegativeMult)
        HelperJoint.addAttribute(HelperJoint.outMtx)
        HelperJoint.attributeAffects(HelperJoint.inSourceMtx1, HelperJoint.outMtx)
        HelperJoint.attributeAffects(HelperJoint.inSourceMtx2, HelperJoint.outMtx)
        HelperJoint.attributeAffects(HelperJoint.inSource1Offset, HelperJoint.outMtx)
        HelperJoint.attributeAffects(HelperJoint.inSource2Offset, HelperJoint.outMtx)
        HelperJoint.attributeAffects(HelperJoint.inParentInverseMtx, HelperJoint.outMtx)
        HelperJoint.attributeAffects(HelperJoint.inPositiveMult, HelperJoint.outMtx)
        HelperJoint.attributeAffects(HelperJoint.inNegativeMult, HelperJoint.outMtx)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != HelperJoint.outMtx:
            return om2.kUnknownParameter

        mSource1 = dataBlock.inputValue(HelperJoint.inSourceMtx1).asMatrix()
        mSource2 = dataBlock.inputValue(HelperJoint.inSourceMtx2).asMatrix()
        mSource1Offset = dataBlock.inputValue(HelperJoint.inSource1Offset).asMatrix()
        mSource2Offset = dataBlock.inputValue(HelperJoint.inSource2Offset).asMatrix()
        mParentInv = dataBlock.inputValue(HelperJoint.inParentInverseMtx).asMatrix()
        posMult = dataBlock.inputValue(HelperJoint.inPositiveMult).asFloat()
        negMult = dataBlock.inputValue(HelperJoint.inNegativeMult).asFloat()

        mSource1Local = mSource1Offset * mSource1
        mSource2Local = mSource2Offset * mSource2

        mOutT = mSource1Local * mParentInv
        # mOutR = (((mSource1Offset * mSource1) * 0.5) + ((mSource2Offset * mSource2) * 0.5)) * mParentInv
        eOri1 = om2.MTransformationMatrix(mSource1Local).rotation(asQuaternion=False)
        eOri1 *= -0.5
        eOri2 = om2.MTransformationMatrix(mSource2Local).rotation(asQuaternion=False)
        eOri2 *= -0.5
        mSource1LocalOri = om2.MTransformationMatrix(mSource1Local).rotateBy(eOri1, om2.MSpace.kTransform).asMatrix()
        mSource2LocalOri = om2.MTransformationMatrix(mSource2Local).rotateBy(eOri2, om2.MSpace.kTransform).asMatrix()
        mOutRLocal = mSource2LocalOri + mSource1LocalOri
        mOutR = mOutRLocal * mParentInv
        mtxFn = om2.MTransformationMatrix(mOutR)
        eRot = mtxFn.rotation(asQuaternion=False)
        mtxFn = om2.MTransformationMatrix(mOutT)
        vTrans = mtxFn.translation(om2.MSpace.kWorld)
        scale = mtxFn.scale(om2.MSpace.kTransform)
        mtxFn = om2.MTransformationMatrix()
        mtxFn.scaleBy(scale, om2.MSpace.kTransform)
        mtxFn.rotateBy(eRot, om2.MSpace.kWorld)
        mtxFn.translateBy(vTrans, om2.MSpace.kWorld)
        mOut = mtxFn.asMatrix()

        outMtxHandle = dataBlock.outputValue(HelperJoint.outMtx)
        outMtxHandle.setMMatrix(mOut)
        outMtxHandle.setClean()
