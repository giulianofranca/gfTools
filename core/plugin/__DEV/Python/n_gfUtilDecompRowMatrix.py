# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfUtilAngularMath node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.

Requirements:
    Maya 2017 or above.

Todo:
    * NDA.

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


class DecomposeRowMatrix(om2.MPxNode):
    """ Main class of gfUtilDecompRowMtx node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inMatrix = om2.MObject()
    inNormalizeOutput = om2.MObject()
    outRow1 = om2.MObject()
    outRow2 = om2.MObject()
    outRow3 = om2.MObject()
    outRow4 = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return DecomposeRowMatrix()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to DecomposeRowMatrix class. Instances of DecomposeRowMatrix will use these attributes to create plugs
        for use in the compute() method.
        """
        nAttr = om2.MFnNumericAttribute()
        mAttr = om2.MFnMatrixAttribute()

        DecomposeRowMatrix.inMatrix = mAttr.create("inputMatrix", "im", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        DecomposeRowMatrix.inNormalizeOutput = nAttr.create("normalizeOutput", "no", om2.MFnNumericData.kBoolean, False)
        INPUT_ATTR(nAttr)

        DecomposeRowMatrix.outRow1 = nAttr.createPoint("row1", "r1")
        OUTPUT_ATTR(nAttr)

        DecomposeRowMatrix.outRow2 = nAttr.createPoint("row2", "r2")
        OUTPUT_ATTR(nAttr)

        DecomposeRowMatrix.outRow3 = nAttr.createPoint("row3", "r3")
        OUTPUT_ATTR(nAttr)

        DecomposeRowMatrix.outRow4 = nAttr.createPoint("row4", "r4")
        OUTPUT_ATTR(nAttr)

        DecomposeRowMatrix.addAttribute(DecomposeRowMatrix.inMatrix)
        DecomposeRowMatrix.addAttribute(DecomposeRowMatrix.inNormalizeOutput)
        DecomposeRowMatrix.addAttribute(DecomposeRowMatrix.outRow1)
        DecomposeRowMatrix.addAttribute(DecomposeRowMatrix.outRow2)
        DecomposeRowMatrix.addAttribute(DecomposeRowMatrix.outRow3)
        DecomposeRowMatrix.addAttribute(DecomposeRowMatrix.outRow4)
        DecomposeRowMatrix.attributeAffects(DecomposeRowMatrix.inMatrix, DecomposeRowMatrix.outRow1)
        DecomposeRowMatrix.attributeAffects(DecomposeRowMatrix.inNormalizeOutput, DecomposeRowMatrix.outRow1)
        DecomposeRowMatrix.attributeAffects(DecomposeRowMatrix.inMatrix, DecomposeRowMatrix.outRow2)
        DecomposeRowMatrix.attributeAffects(DecomposeRowMatrix.inNormalizeOutput, DecomposeRowMatrix.outRow2)
        DecomposeRowMatrix.attributeAffects(DecomposeRowMatrix.inMatrix, DecomposeRowMatrix.outRow3)
        DecomposeRowMatrix.attributeAffects(DecomposeRowMatrix.inNormalizeOutput, DecomposeRowMatrix.outRow3)
        DecomposeRowMatrix.attributeAffects(DecomposeRowMatrix.inMatrix, DecomposeRowMatrix.outRow4)
        DecomposeRowMatrix.attributeAffects(DecomposeRowMatrix.inNormalizeOutput, DecomposeRowMatrix.outRow4)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        mInput = dataBlock.inputValue(DecomposeRowMatrix.inMatrix).asFloatMatrix()
        normalize = dataBlock.inputValue(DecomposeRowMatrix.inNormalizeOutput).asBool()

        if plug == DecomposeRowMatrix.outRow1:
            vRow1 = om2.MFloatVector(mInput[0], mInput[1], mInput[2])
            if normalize:
                vRow1.normalize()
            outRow1Handle = dataBlock.outputValue(DecomposeRowMatrix.outRow1)
            outRow1Handle.setMFloatVector(vRow1)
            outRow1Handle.setClean()
        elif plug == DecomposeRowMatrix.outRow2:
            vRow2 = om2.MFloatVector(mInput[4], mInput[5], mInput[6])
            if normalize:
                vRow2.normalize()
            outRow2Handle = dataBlock.outputValue(DecomposeRowMatrix.outRow2)
            outRow2Handle.setMFloatVector(vRow2)
            outRow2Handle.setClean()
        elif plug == DecomposeRowMatrix.outRow3:
            vRow3 = om2.MFloatVector(mInput[8], mInput[9], mInput[10])
            if normalize:
                vRow3.normalize()
            outRow3Handle = dataBlock.outputValue(DecomposeRowMatrix.outRow3)
            outRow3Handle.setMFloatVector(vRow3)
            outRow3Handle.setClean()
        elif plug == DecomposeRowMatrix.outRow4:
            vRow4 = om2.MFloatVector(mInput[12], mInput[13], mInput[14])
            if normalize:
                vRow4.normalize()
            outRow4Handle = dataBlock.outputValue(DecomposeRowMatrix.outRow4)
            outRow4Handle.setMFloatVector(vRow4)
            outRow4Handle.setClean()
        else:
            return om2.kUnknownParameter
