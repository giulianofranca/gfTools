# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França
Redistribution:
    Something here.
Maya Node:
    [This is a prototype version of the gfUtilAimConstraint node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.
Requirements:
    Maya 2017 or above.
Todo:
    * Fix only works with X Primary and Y Secondary
    * Add maintain offset funcionality
    * Add manual twist functionality
This code supports Pylint. Rc file in project.
"""
# import math
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


class AimConstraint(om2.MPxNode):
    """ Main class of gfUtilAimConstraint node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inUpVecType = om2.MObject()
    inOffset = om2.MObject()
    inWorldUpVector = om2.MObject()
    inWorldUpMtx = om2.MObject()
    inTargetWMtx = om2.MObject()
    inTargetWeight = om2.MObject()
    inConstWMtx = om2.MObject()
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
        return AimConstraint()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to AimConstraint class. Instances of AimConstraint will use these attributes to create plugs
        for use in the compute() method.
        """
        eAttr = om2.MFnEnumAttribute()
        mAttr = om2.MFnMatrixAttribute()
        nAttr = om2.MFnNumericAttribute()
        uAttr = om2.MFnUnitAttribute()

        AimConstraint.inUpVecType = eAttr.create("upVectorType", "upt", 0)
        eAttr.addField("World Up", 0)
        eAttr.addField("Object Up", 1)
        INPUT_ATTR(eAttr)

        offsetX = uAttr.create("offsetX", "offsetX", om2.MFnUnitAttribute.kAngle, 0.0)
        offsetY = uAttr.create("offsetY", "offsetY", om2.MFnUnitAttribute.kAngle, 0.0)
        offsetZ = uAttr.create("offsetZ", "offsetZ", om2.MFnUnitAttribute.kAngle, 0.0)
        AimConstraint.inOffset = nAttr.create("offset", "offset", offsetX, offsetY, offsetZ)
        INPUT_ATTR(nAttr)

        AimConstraint.inWorldUpVector = nAttr.createPoint("worldUpVector", "wuv")
        nAttr.default = (0.0, 1.0, 0.0)
        INPUT_ATTR(nAttr)

        AimConstraint.inWorldUpMtx = mAttr.create("worldUpMatrix", "wum", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        AimConstraint.inTargetWMtx = mAttr.create("targetWorldMatrix", "twmtx", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        AimConstraint.inTargetWeight = nAttr.create("targetWeight", "tw", om2.MFnNumericData.kDouble, 1.0)
        INPUT_ATTR(nAttr)

        AimConstraint.inConstWMtx = mAttr.create("constraintWorldMatrix", "cwmtx", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        AimConstraint.inConstParInvMtx = mAttr.create("constraintParentInverseMatrix", "cpim", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        jntOriX = uAttr.create("constraintJointOrientX", "cjorx", om2.MFnUnitAttribute.kAngle, 0.0)
        jntOriY = uAttr.create("constraintJointOrientY", "cjory", om2.MFnUnitAttribute.kAngle, 0.0)
        jntOriZ = uAttr.create("constraintJointOrientZ", "cjorz", om2.MFnUnitAttribute.kAngle, 0.0)
        AimConstraint.inConstJntOri = nAttr.create("constraintJointOrient", "cjor", jntOriX, jntOriY, jntOriZ)
        INPUT_ATTR(nAttr)

        AimConstraint.inConstRotOrder = eAttr.create("constraintRotateOrder", "cro", 0)
        eAttr.addField("xyz", 0)
        eAttr.addField("yzx", 1)
        eAttr.addField("zxy", 2)
        eAttr.addField("xzy", 3)
        eAttr.addField("yxz", 4)
        eAttr.addField("zyx", 5)
        INPUT_ATTR(eAttr)

        outConstraintX = uAttr.create("constraintX", "cx", om2.MFnUnitAttribute.kAngle, 0.0)
        outConstraintY = uAttr.create("constraintY", "cy", om2.MFnUnitAttribute.kAngle, 0.0)
        outConstraintZ = uAttr.create("constraintZ", "cz", om2.MFnUnitAttribute.kAngle, 0.0)
        AimConstraint.outConstraint = nAttr.create("constraint", "const", outConstraintX, outConstraintY, outConstraintZ)
        OUTPUT_ATTR(nAttr)

        AimConstraint.addAttribute(AimConstraint.inUpVecType)
        AimConstraint.addAttribute(AimConstraint.inOffset)
        AimConstraint.addAttribute(AimConstraint.inWorldUpVector)
        AimConstraint.addAttribute(AimConstraint.inWorldUpMtx)
        AimConstraint.addAttribute(AimConstraint.inTargetWMtx)
        AimConstraint.addAttribute(AimConstraint.inTargetWeight)
        AimConstraint.addAttribute(AimConstraint.inConstWMtx)
        AimConstraint.addAttribute(AimConstraint.inConstParInvMtx)
        AimConstraint.addAttribute(AimConstraint.inConstJntOri)
        AimConstraint.addAttribute(AimConstraint.inConstRotOrder)
        AimConstraint.addAttribute(AimConstraint.outConstraint)
        AimConstraint.attributeAffects(AimConstraint.inUpVecType, AimConstraint.outConstraint)
        AimConstraint.attributeAffects(AimConstraint.inOffset, AimConstraint.outConstraint)
        AimConstraint.attributeAffects(AimConstraint.inWorldUpVector, AimConstraint.outConstraint)
        AimConstraint.attributeAffects(AimConstraint.inWorldUpMtx, AimConstraint.outConstraint)
        AimConstraint.attributeAffects(AimConstraint.inTargetWMtx, AimConstraint.outConstraint)
        AimConstraint.attributeAffects(AimConstraint.inTargetWeight, AimConstraint.outConstraint)
        AimConstraint.attributeAffects(AimConstraint.inConstWMtx, AimConstraint.outConstraint)
        AimConstraint.attributeAffects(AimConstraint.inConstParInvMtx, AimConstraint.outConstraint)
        AimConstraint.attributeAffects(AimConstraint.inConstJntOri, AimConstraint.outConstraint)
        AimConstraint.attributeAffects(AimConstraint.inConstRotOrder, AimConstraint.outConstraint)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != AimConstraint.outConstraint:
            return om2.kUnknownParameter
        upVecType = dataBlock.inputValue(AimConstraint.inUpVecType).asShort()
        eOffset = om2.MEulerRotation(dataBlock.inputValue(AimConstraint.inOffset).asDouble3())
        mTargetWorld = dataBlock.inputValue(AimConstraint.inTargetWMtx).asFloatMatrix()
        targetWeight = dataBlock.inputValue(AimConstraint.inTargetWeight).asDouble()
        mConstWorld = dataBlock.inputValue(AimConstraint.inConstWMtx).asFloatMatrix()
        mConstParInv = dataBlock.inputValue(AimConstraint.inConstParInvMtx).asMatrix()
        eConstJntOri = om2.MEulerRotation(dataBlock.inputValue(AimConstraint.inConstJntOri).asDouble3())
        constRotOrder = dataBlock.inputValue(AimConstraint.inConstRotOrder).asShort()

        vTargetPos = om2.MFloatVector(mTargetWorld[12], mTargetWorld[13], mTargetWorld[14])
        vConstPos = om2.MFloatVector(mConstWorld[12], mConstWorld[13], mConstWorld[14])
        nAim = vTargetPos - vConstPos
        nAim.normalize()
        if upVecType == 0:
            nWorldUp = dataBlock.inputValue(AimConstraint.inWorldUpVector).asFloatVector()
            nWorldUp.normalize()
            nBinormal = nWorldUp ^ nAim
            nBinormal.normalize()
            nNormal = nAim ^ nBinormal
            nNormal.normalize()
        elif upVecType == 1:
            mWorldUp = dataBlock.inputValue(AimConstraint.inWorldUpMtx).asFloatMatrix()
            vWorldUp = om2.MFloatVector(mWorldUp[12], mWorldUp[13], mWorldUp[14])
            nNormal = vWorldUp - vConstPos
            nNormal.normalize()
            nBinormal = nAim ^ nNormal
            nBinormal.normalize()
        aim = [
            nAim.x, nAim.y, nAim.z, 0.0,
            nNormal.x, nNormal.y, nNormal.z, 0.0,
            nBinormal.x, nBinormal.y, nBinormal.z, 0.0,
            0.0, 0.0, 0.0, 1.0
        ]
        mAim = om2.MMatrix(aim)
        mtxFn = om2.MTransformationMatrix()
        mtxFn.rotateBy(eConstJntOri, om2.MSpace.kTransform)
        mConstJntOri = mtxFn.asMatrix()
        mtxFn = om2.MTransformationMatrix()
        mtxFn.rotateBy(eOffset.invertIt(), om2.MSpace.kTransform)
        mOffset = mtxFn.asMatrix()
        mResult = mOffset * mAim * mConstParInv * mConstJntOri.inverse()
        eConstraint = om2.MEulerRotation.decompose(mResult, om2.MEulerRotation.kXYZ)
        eConstraint.reorderIt(constRotOrder)
        eConstraint *= targetWeight
        vConstraint = eConstraint.asVector()
        outConstraintHandle = dataBlock.outputValue(AimConstraint.outConstraint)
        outConstraintHandle.setMVector(vConstraint)
        outConstraintHandle.setClean()
