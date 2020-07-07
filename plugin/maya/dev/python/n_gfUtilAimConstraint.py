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
import math
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
    inAngleUp = om2.MObject()
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
        eAttr.addField("None", 0)
        eAttr.addField("World Up", 1)
        eAttr.addField("Object Up", 2)
        eAttr.addField("Angle Up", 3)
        INPUT_ATTR(eAttr)
        eAttr.channelBox = True

        offsetX = uAttr.create("offsetX", "offsetX", om2.MFnUnitAttribute.kAngle, 0.0)
        offsetY = uAttr.create("offsetY", "offsetY", om2.MFnUnitAttribute.kAngle, 0.0)
        offsetZ = uAttr.create("offsetZ", "offsetZ", om2.MFnUnitAttribute.kAngle, 0.0)
        AimConstraint.inOffset = nAttr.create("offset", "offset", offsetX, offsetY, offsetZ)
        INPUT_ATTR(nAttr)

        AimConstraint.inWorldUpVector = nAttr.createPoint("worldUpVector", "wuv")
        nAttr.default = (0.0, 1.0, 0.0)
        INPUT_ATTR(nAttr)

        AimConstraint.inWorldUpMtx = mAttr.create("worldUpMatrix", "wum", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        AimConstraint.inAngleUp = uAttr.create("angleUp", "angle", om2.MFnUnitAttribute.kAngle, 0.0)
        uAttr.setMin(0.0)
        uAttr.setMax(2.0 * math.pi)
        INPUT_ATTR(uAttr)

        AimConstraint.inTargetWMtx = mAttr.create("targetWorldMatrix", "twmtx", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        AimConstraint.inTargetWeight = nAttr.create("targetWeight", "tw", om2.MFnNumericData.kDouble, 1.0)
        INPUT_ATTR(nAttr)

        AimConstraint.inConstWMtx = mAttr.create("constraintWorldMatrix", "cwmtx", om2.MFnMatrixAttribute.kDouble)
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
        AimConstraint.addAttribute(AimConstraint.inAngleUp)
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
        AimConstraint.attributeAffects(AimConstraint.inAngleUp, AimConstraint.outConstraint)
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
        qOffset = eOffset.asQuaternion()
        mTargetW = dataBlock.inputValue(AimConstraint.inTargetWMtx).asMatrix()
        targetWeight = dataBlock.inputValue(AimConstraint.inTargetWeight).asDouble()
        mConstW = dataBlock.inputValue(AimConstraint.inConstWMtx).asMatrix()
        mConstParInv = dataBlock.inputValue(AimConstraint.inConstParInvMtx).asMatrix()
        eConstJntOri = om2.MEulerRotation(dataBlock.inputValue(AimConstraint.inConstJntOri).asDouble3())
        qConstJntOri = eConstJntOri.asQuaternion()
        constRotOrder = dataBlock.inputValue(AimConstraint.inConstRotOrder).asShort()

        vTarget = om2.MVector(mTargetW[12], mTargetW[13], mTargetW[14])
        vConst = om2.MVector(mConstW[12], mConstW[13], mConstW[14])
        mtxFn = om2.MTransformationMatrix(mConstParInv)
        qConstParInv = mtxFn.rotation(asQuaternion=True)

        primAxis = om2.MVector.kXaxisVector
        secAxis = om2.MVector.kYaxisVector
        qAimConst = om2.MQuaternion()

        nAim = vTarget - vConst
        nAim.normalize()
        qAim = om2.MQuaternion(primAxis, nAim)
        qAimConst *= qAim

        if upVecType != 0:
            if upVecType == 1:
                # World Up
                nWorldUp = om2.MVector(dataBlock.inputValue(AimConstraint.inWorldUpVector).asFloat3())
                nWorldUp.normalize()
                vUp = nWorldUp
            elif upVecType == 2:
                # Object Up
                mWorldUp = dataBlock.inputValue(AimConstraint.inWorldUpMtx).asMatrix()
                vWorldUp = om2.MVector(mWorldUp[12], mWorldUp[13], mWorldUp[14])
                vUp = vWorldUp - vConst
            elif upVecType == 3:
                # Angle Up
                angleUp = dataBlock.inputValue(AimConstraint.inAngleUp).asAngle().asRadians()
                qTwist = om2.MQuaternion(angleUp, nAim)
                vUp = secAxis.rotateBy(qTwist)
            nNormal = vUp - ((vUp * nAim) * nAim)
            nNormal.normalize()

            nUp = secAxis.rotateBy(qAim)
            angle = nUp.angle(nNormal)
            qNormal = om2.MQuaternion(angle, nAim)
            if not nNormal.isEquivalent(nUp.rotateBy(qNormal), 1.0e-5):
                angle = 2.0 * math.pi - angle
                qNormal = om2.MQuaternion(angle, nAim)
            qAimConst *= qNormal

        qResult = om2.MQuaternion()
        qResult *= qOffset.invertIt()
        qResult *= qAimConst
        qResult *= qConstParInv
        qResult *= qConstJntOri.invertIt()
        eResult = qResult.asEulerRotation()
        eResult.reorderIt(constRotOrder)
        eResult *= targetWeight
        vResult = eResult.asVector()
        outConstraintHandle = dataBlock.outputValue(AimConstraint.outConstraint)
        outConstraintHandle.setMVector(vResult)
        outConstraintHandle.setClean()
