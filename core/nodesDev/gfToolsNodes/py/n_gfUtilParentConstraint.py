# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfUtilParentConstraint node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.

Requirements:
    Maya 2017 or above.

Todo:
    * NDA
    * https://math.stackexchange.com/questions/1099390/billinear-interpolation-of-3-points
    * https://en.wikipedia.org/wiki/Bilinear_interpolation

This code supports Pylint. Rc file in project.
"""
# pylint: disable=import-error
# import-error = Supress Maya modules import error

import maya.api.OpenMaya as om2


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


class ParentConstraint(om2.MPxNode):
    """ Main class of gfUtilParentConstraint node. """

    kNODE_NAME = ""
    kNODE_CLASSIFY = ""
    kNODE_ID = ""

    inTarget = om2.MObject()
    inOffset = om2.MObject()
    inWeight = om2.MObject()
    outConstraint = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return ParentConstraint()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to ParentConstraint class. Instances of ParentConstraint will use these attributes to create plugs
        for use in the compute() method.
        """
        mAttr = om2.MFnMatrixAttribute()
        nAttr = om2.MFnNumericAttribute()

        ParentConstraint.inTarget = mAttr.create("target", "target", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        INPUT_ATTR(mAttr)

        ParentConstraint.inOffset = mAttr.create("offset", "offset", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        INPUT_ATTR(mAttr)

        ParentConstraint.inWeight = nAttr.create("weight", "weight", om2.MFnNumericData.kFloat, 1.0)
        nAttr.array = True
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        ParentConstraint.outConstraint = mAttr.create("constraint", "const", om2.MFnMatrixAttribute.kDouble)
        OUTPUT_ATTR(mAttr)

        ParentConstraint.addAttribute(ParentConstraint.inTarget)
        ParentConstraint.addAttribute(ParentConstraint.inOffset)
        ParentConstraint.addAttribute(ParentConstraint.inWeight)
        ParentConstraint.addAttribute(ParentConstraint.outConstraint)
        ParentConstraint.attributeAffects(ParentConstraint.inTarget, ParentConstraint.outConstraint)
        ParentConstraint.attributeAffects(ParentConstraint.inOffset, ParentConstraint.outConstraint)
        ParentConstraint.attributeAffects(ParentConstraint.inWeight, ParentConstraint.outConstraint)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != ParentConstraint.outConstraint:
            return om2.kUnknownParameter

        targetHandle = dataBlock.inputArrayValue(ParentConstraint.inTarget)
        offsetHandle = dataBlock.inputArrayValue(ParentConstraint.inOffset)
        weightHandle = dataBlock.inputArrayValue(ParentConstraint.inWeight)

        targetList = []

        for i in range(min(len(targetHandle), len(offsetHandle), len(weightHandle))):
            targetHandle.jumpToLogicalElement(i)
            offsetHandle.jumpToLogicalElement(i)
            weightHandle.jumpToLogicalElement(i)
            mTarget = targetHandle.inputValue().asMatrix()
            mOffset = offsetHandle.inputValue().asMatrix()
            weight = weightHandle.inputValue().asFloat()
            targetList.append((mOffset * mTarget) * weight)

        mAdd = om2.MMatrix()
        for i in targetList:
            mAdd += i

        mConstraint = mAdd * om2.MMatrix() # Parent Inverse Matrix
        outConstraintHandle = dataBlock.outputValue(ParentConstraint.outConstraint)
        outConstraintHandle.setMMatrix(mConstraint)
        outConstraintHandle.setClean()
