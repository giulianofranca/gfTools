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
    inTarget = om2.MObject()
    inWorldUp = om2.MObject()
    inUpObj = om2.MObject()
    inPivot = om2.MObject()
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

        AimConstraint.inTarget = mAttr.create("target", "target", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        AimConstraint.inUpObj = mAttr.create("up", "up", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        AimConstraint.inWorldUp = nAttr.createPoint("worldUp", "wu")
        nAttr.default = (0.0, 1.0, 0.0)
        INPUT_ATTR(nAttr)

        AimConstraint.inPivot = mAttr.create("pivot", "pivot", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        outConstraintX = uAttr.create("constraintX", "cx", om2.MFnUnitAttribute.kAngle, 0.0)
        outConstraintY = uAttr.create("constraintY", "cy", om2.MFnUnitAttribute.kAngle, 0.0)
        outConstraintZ = uAttr.create("constraintZ", "cz", om2.MFnUnitAttribute.kAngle, 0.0)
        AimConstraint.outConstraint = nAttr.create("constraint", "const", outConstraintX, outConstraintY, outConstraintZ)
        OUTPUT_ATTR(nAttr)

        AimConstraint.addAttribute(AimConstraint.inUpVecType)
        AimConstraint.addAttribute(AimConstraint.inTarget)
        AimConstraint.addAttribute(AimConstraint.inUpObj)
        AimConstraint.addAttribute(AimConstraint.inWorldUp)
        AimConstraint.addAttribute(AimConstraint.inPivot)
        AimConstraint.addAttribute(AimConstraint.outConstraint)
        AimConstraint.attributeAffects(AimConstraint.inUpVecType, AimConstraint.outConstraint)
        AimConstraint.attributeAffects(AimConstraint.inTarget, AimConstraint.outConstraint)
        AimConstraint.attributeAffects(AimConstraint.inUpObj, AimConstraint.outConstraint)
        AimConstraint.attributeAffects(AimConstraint.inWorldUp, AimConstraint.outConstraint)
        AimConstraint.attributeAffects(AimConstraint.inPivot, AimConstraint.outConstraint)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != AimConstraint.outConstraint:
            return om2.kUnknownParameter
        upType = dataBlock.inputValue(AimConstraint.inUpVecType).asShort()
        mTarget = dataBlock.inputValue(AimConstraint.inTarget).asFloatMatrix()
        mPivot = dataBlock.inputValue(AimConstraint.inPivot).asFloatMatrix()
        vTarget = om2.MFloatVector(mTarget[12], mTarget[13], mTarget[14])
        vPivot = om2.MFloatVector(mPivot[12], mPivot[13], mPivot[14])
        vAim = vTarget - vPivot
        nAim = vAim.normal()
        if upType == 0:
            vWorldUp = dataBlock.inputValue(AimConstraint.inWorldUp).asFloatVector()
            nWorldUp = vWorldUp.normal()
            nBinormal = nAim ^ -nWorldUp
            nNormal = nAim ^ nBinormal
        elif upType == 1:
            mUpObj = dataBlock.inputValue(AimConstraint.inUpObj).asFloatMatrix()
            vUpObj = om2.MFloatVector(mUpObj[12], mUpObj[13], mUpObj[14])
            vNormal = vUpObj - vPivot
            nNormal = vNormal.normal()
            nBinormal = nAim ^ nNormal
        aim = [nAim.x, nAim.y, nAim.z, 0.0,
               nNormal.x, nNormal.y, nNormal.z, 0.0,
               nBinormal.x, nBinormal.y, nBinormal.z, 0.0,
               0.0, 0.0, 0.0, 1.0]
        mAim = om2.MMatrix(aim)
        mtxFn = om2.MTransformationMatrix(mAim)
        eAim = mtxFn.rotation(asQuaternion=True).asEulerRotation().asVector()
        outConstraintHandle = dataBlock.outputValue(AimConstraint.outConstraint)
        outConstraintHandle.setMVector(eAim)
        outConstraintHandle.setClean()
