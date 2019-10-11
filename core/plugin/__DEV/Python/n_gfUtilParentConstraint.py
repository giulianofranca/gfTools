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


class ParentConstraint(om2.MPxNode):
    """ Main class of gfUtilParentConstraint node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inOffset = om2.MObject()
    inTargetWMtx = om2.MObject()
    inTargetRotOrder = om2.MObject()
    inTargetWeight = om2.MObject()
    inConstParInvMtx = om2.MObject()
    inConstJntOri = om2.MObject()
    inConstRotOrder = om2.MObject()
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
        eAttr = om2.MFnEnumAttribute()
        mAttr = om2.MFnMatrixAttribute()
        nAttr = om2.MFnNumericAttribute()
        uAttr = om2.MFnUnitAttribute()
        cAttr = om2.MFnCompoundAttribute()

        ParentConstraint.inOffset = mAttr.create("offset", "offset", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        ParentConstraint.inTargetWMtx = mAttr.create("targetWorldMatrix", "twmtx", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        ParentConstraint.inTargetRotOrder = eAttr.create("targetRotateOrder", "tro", 0)
        eAttr.addField("xyz", 0)
        eAttr.addField("yzx", 1)
        eAttr.addField("zxy", 2)
        eAttr.addField("xzy", 3)
        eAttr.addField("yxz", 4)
        eAttr.addField("zyx", 5)
        INPUT_ATTR(eAttr)

        ParentConstraint.inTargetWeight = nAttr.create("targetWeight", "tw", om2.MFnNumericData.kDouble, 1.0)
        INPUT_ATTR(nAttr)

        ParentConstraint.inConstParInvMtx = mAttr.create("constraintParentInverseMatrix", "cpim", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        constJntOriX = uAttr.create("constraintJointOrientX", "cjorx", om2.MFnUnitAttribute.kAngle, 0.0)
        constJntOriY = uAttr.create("constraintJointOrientY", "cjory", om2.MFnUnitAttribute.kAngle, 0.0)
        constJntOriZ = uAttr.create("constraintJointOrientZ", "cjorz", om2.MFnUnitAttribute.kAngle, 0.0)
        ParentConstraint.inConstJntOri = nAttr.create("constraintJointOrient", "cjor", constJntOriX, constJntOriY, constJntOriZ)
        INPUT_ATTR(nAttr)

        ParentConstraint.inConstRotOrder = eAttr.create("constraintRotateOrder", "cro", 0)
        eAttr.addField("xyz", 0)
        eAttr.addField("yzx", 1)
        eAttr.addField("zxy", 2)
        eAttr.addField("xzy", 3)
        eAttr.addField("yxz", 4)
        eAttr.addField("zyx", 5)
        INPUT_ATTR(eAttr)

        ParentConstraint.outConstraint = mAttr.create("constraint", "const", om2.MFnMatrixAttribute.kDouble)
        OUTPUT_ATTR(mAttr)

        ParentConstraint.addAttribute(ParentConstraint.inOffset)
        ParentConstraint.addAttribute(ParentConstraint.inTargetWMtx)
        ParentConstraint.addAttribute(ParentConstraint.inTargetRotOrder)
        ParentConstraint.addAttribute(ParentConstraint.inTargetWeight)
        ParentConstraint.addAttribute(ParentConstraint.inConstParInvMtx)
        ParentConstraint.addAttribute(ParentConstraint.inConstJntOri)
        ParentConstraint.addAttribute(ParentConstraint.inConstRotOrder)
        ParentConstraint.addAttribute(ParentConstraint.outConstraint)
        ParentConstraint.attributeAffects(ParentConstraint.inOffset, ParentConstraint.outConstraint)
        ParentConstraint.attributeAffects(ParentConstraint.inTargetWMtx, ParentConstraint.outConstraint)
        ParentConstraint.attributeAffects(ParentConstraint.inTargetRotOrder, ParentConstraint.outConstraint)
        ParentConstraint.attributeAffects(ParentConstraint.inTargetWeight, ParentConstraint.outConstraint)
        ParentConstraint.attributeAffects(ParentConstraint.inConstParInvMtx, ParentConstraint.outConstraint)
        ParentConstraint.attributeAffects(ParentConstraint.inConstJntOri, ParentConstraint.outConstraint)
        ParentConstraint.attributeAffects(ParentConstraint.inConstRotOrder, ParentConstraint.outConstraint)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != ParentConstraint.outConstraint:
            return om2.kUnknownParameter

        mOffset = dataBlock.inputValue(ParentConstraint.inOffset).asMatrix()
        mTargetWorld = dataBlock.inputValue(ParentConstraint.inTargetWMtx).asMatrix()
        targetRotOrder = dataBlock.inputValue(ParentConstraint.inTargetRotOrder).asShort()
        targetWeight = dataBlock.inputValue(ParentConstraint.inTargetWeight).asDouble()
        mConstParInv = dataBlock.inputValue(ParentConstraint.inConstParInvMtx).asMatrix()
        eConstJntOri = om2.MEulerRotation(dataBlock.inputValue(ParentConstraint.inConstJntOri).asDouble3())
        constRotOrder = dataBlock.inputValue(ParentConstraint.inConstRotOrder).asShort()

        mtxFn = om2.MTransformationMatrix()
        mtxFn.rotateBy(eConstJntOri, om2.MSpace.kTransform)
        mConstJntOri = mtxFn.asMatrix()

        # TODO(matrix multiplication order): Separate SRT Multiplication order?
        mResult = mOffset * mTargetWorld * mConstParInv * mConstJntOri.inverse()

        vResultTrans = om2.MVector(mResult[12], mResult[13], mResult[14])
        eResultRot = om2.MEulerRotation.decompose(mResult, targetRotOrder)
        eResultRot.reorderIt(constRotOrder)
        resultScale = om2.MTransformationMatrix(mResult).scale(om2.MSpace.kTransform)

        mtxFn = om2.MTransformationMatrix()
        mtxFn.scaleBy(resultScale, om2.MSpace.kTransform)
        mtxFn.rotateBy(eResultRot, om2.MSpace.kTransform)
        mtxFn.translateBy(vResultTrans, om2.MSpace.kTransform)

        mConstraint = mtxFn.asMatrix()
        mConstraint *= targetWeight

        outConstraintHandle = dataBlock.outputValue(ParentConstraint.outConstraint)
        outConstraintHandle.setMMatrix(mConstraint)
        outConstraintHandle.setClean()

        # targetHandle = dataBlock.inputArrayValue(ParentConstraint.inTarget)
        # offsetHandle = dataBlock.inputArrayValue(ParentConstraint.inOffset)
        # weightHandle = dataBlock.inputArrayValue(ParentConstraint.inWeight)

        # targetList = []

        # for i in range(min(len(targetHandle), len(offsetHandle), len(weightHandle))):
        #     targetHandle.jumpToLogicalElement(i)
        #     offsetHandle.jumpToLogicalElement(i)
        #     weightHandle.jumpToLogicalElement(i)
        #     mTarget = targetHandle.inputValue().asMatrix()
        #     mOffset = offsetHandle.inputValue().asMatrix()
        #     weight = weightHandle.inputValue().asFloat()
        #     targetList.append((mOffset * mTarget) * weight)

        # mAdd = om2.MMatrix()
        # for i in targetList:
        #     mAdd += i

        # mConstraint = mAdd * om2.MMatrix() # Parent Inverse Matrix
        # outConstraintHandle = dataBlock.outputValue(ParentConstraint.outConstraint)
        # outConstraintHandle.setMMatrix(mConstraint)
        # outConstraintHandle.setClean()
