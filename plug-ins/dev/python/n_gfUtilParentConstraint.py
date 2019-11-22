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
    Custom parent contraint. Parent one object to another. Can be used as point, orient
    or scale constraint.

Attributes:
    * Offset: The matrix offset between the source and target objects.
    * Target World Matrix: The world matrix of the target object.
    * Constraint Parent Inverse Matrix: The world inverse matrix of the parent of the constrainted object.
    * Out Constraint: The output matrix of the constraint.

Todo:
    * Add support to joint orient.
    * Add support to rotation order.
    * Add support to weights.

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


class ParentConstraint(om2.MPxNode):
    """ Main class of gfUtilParentConstraint node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inConstraintJntOri = om2.MObject()
    inConstraintRotOrder = om2.MObject()
    inConstraintParInvMtx = om2.MObject()
    inConstraintParSca = om2.MObject()
    # inTargetJntOri = om2.MObject()
    # inTargetRotOrder = om2.MObject()
    inTargetWorldMatrix = om2.MObject()
    inTargetOffset = om2.MObject()
    inTargetWeight = om2.MObject()
    inTargetList = om2.MObject()
    outConstTrans = om2.MObject()
    outConstRot = om2.MObject()
    outConstSca = om2.MObject()

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
        uAttr = om2.MFnUnitAttribute()
        eAttr = om2.MFnEnumAttribute()
        cAttr = om2.MFnCompoundAttribute()

        constJntOriX = uAttr.create("constraintJointOrientX", "cjorx", om2.MFnUnitAttribute.kAngle, 0.0)
        constJntOriY = uAttr.create("constraintJointOrientY", "cjory", om2.MFnUnitAttribute.kAngle, 0.0)
        constJntOriZ = uAttr.create("constraintJointOrientZ", "cjorz", om2.MFnUnitAttribute.kAngle, 0.0)
        ParentConstraint.inConstraintJntOri = nAttr.create("constraintJointOrient", "cjor", constJntOriX, constJntOriY, constJntOriZ)
        INPUT_ATTR(nAttr)

        ParentConstraint.inConstraintRotOrder = eAttr.create("constraintRotateOrder", "croo", 0)
        eAttr.addField("xyz", 0)
        eAttr.addField("yzx", 1)
        eAttr.addField("zxy", 2)
        eAttr.addField("xzy", 3)
        eAttr.addField("yxz", 4)
        eAttr.addField("zyx", 5)
        INPUT_ATTR(eAttr)

        ParentConstraint.inConstraintParInvMtx = mAttr.create("constraintParentInverseMatrix", "cpim", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        ParentConstraint.inConstraintParSca = nAttr.createPoint("constraintParentScale", "cps")
        nAttr.default = (1.0, 1.0, 1.0)
        INPUT_ATTR(nAttr)

        ParentConstraint.inTargetWorldMatrix = mAttr.create("targetWorldMatrix", "twmtx", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        ParentConstraint.inTargetOffset = mAttr.create("targetOffset", "toff", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        # targetJntOriX = uAttr.create("targetJointOrientX", "tjorx", om2.MFnUnitAttribute.kAngle, 0.0)
        # targetJntOriY = uAttr.create("targetJointOrientY", "tjory", om2.MFnUnitAttribute.kAngle, 0.0)
        # targetJntOriZ = uAttr.create("targetJointOrientZ", "tjorz", om2.MFnUnitAttribute.kAngle, 0.0)
        # ParentConstraint.inTargetJntOri = nAttr.create("targetJointOrient", "tjor", targetJntOriX, targetJntOriY, targetJntOriZ)
        # INPUT_ATTR(nAttr)

        # ParentConstraint.inTargetRotOrder = eAttr.create("targetRotateOrder", "troo", 0)
        # eAttr.addField("xyz", 0)
        # eAttr.addField("yzx", 1)
        # eAttr.addField("zxy", 2)
        # eAttr.addField("xzy", 3)
        # eAttr.addField("yxz", 4)
        # eAttr.addField("zyx", 5)
        # INPUT_ATTR(eAttr)

        ParentConstraint.inTargetWeight = nAttr.create("targetWeight", "twght", om2.MFnNumericData.kFloat, 1.0)
        INPUT_ATTR(nAttr)

        ParentConstraint.inTargetList = cAttr.create("targetList", "tlist")
        cAttr.addChild(ParentConstraint.inTargetWorldMatrix)
        cAttr.addChild(ParentConstraint.inTargetOffset)
        # cAttr.addChild(ParentConstraint.inTargetJntOri)
        # cAttr.addChild(ParentConstraint.inTargetRotOrder)
        cAttr.addChild(ParentConstraint.inTargetWeight)
        cAttr.array = True

        ParentConstraint.outConstTrans = nAttr.createPoint("constraintTranslate", "ctrans")
        OUTPUT_ATTR(nAttr)

        outConstRotX = uAttr.create("constraintRotateX", "crox", om2.MFnUnitAttribute.kAngle, 0.0)
        outConstRotY = uAttr.create("constraintRotateY", "croy", om2.MFnUnitAttribute.kAngle, 0.0)
        outConstRotZ = uAttr.create("constraintRotateZ", "croz", om2.MFnUnitAttribute.kAngle, 0.0)
        ParentConstraint.outConstRot = nAttr.create("constraintRotate", "cro", outConstRotX, outConstRotY, outConstRotZ)
        OUTPUT_ATTR(nAttr)

        ParentConstraint.outConstSca = nAttr.createPoint("constraintScale", "csca")
        nAttr.default = (1.0, 1.0, 1.0)
        OUTPUT_ATTR(nAttr)

        ParentConstraint.addAttribute(ParentConstraint.inConstraintJntOri)
        ParentConstraint.addAttribute(ParentConstraint.inConstraintRotOrder)
        ParentConstraint.addAttribute(ParentConstraint.inConstraintParInvMtx)
        ParentConstraint.addAttribute(ParentConstraint.inConstraintParSca)
        ParentConstraint.addAttribute(ParentConstraint.inTargetList)
        ParentConstraint.addAttribute(ParentConstraint.outConstTrans)
        ParentConstraint.addAttribute(ParentConstraint.outConstRot)
        ParentConstraint.addAttribute(ParentConstraint.outConstSca)
        ParentConstraint.attributeAffects(ParentConstraint.inConstraintJntOri, ParentConstraint.outConstTrans)
        ParentConstraint.attributeAffects(ParentConstraint.inConstraintRotOrder, ParentConstraint.outConstTrans)
        ParentConstraint.attributeAffects(ParentConstraint.inConstraintParInvMtx, ParentConstraint.outConstTrans)
        ParentConstraint.attributeAffects(ParentConstraint.inConstraintParSca, ParentConstraint.outConstTrans)
        ParentConstraint.attributeAffects(ParentConstraint.inTargetWorldMatrix, ParentConstraint.outConstTrans)
        ParentConstraint.attributeAffects(ParentConstraint.inTargetOffset, ParentConstraint.outConstTrans)
        # ParentConstraint.attributeAffects(ParentConstraint.inTargetJntOri, ParentConstraint.outConstTrans)
        # ParentConstraint.attributeAffects(ParentConstraint.inTargetRotOrder, ParentConstraint.outConstTrans)
        ParentConstraint.attributeAffects(ParentConstraint.inTargetWeight, ParentConstraint.outConstTrans)
        ParentConstraint.attributeAffects(ParentConstraint.inConstraintJntOri, ParentConstraint.outConstRot)
        ParentConstraint.attributeAffects(ParentConstraint.inConstraintRotOrder, ParentConstraint.outConstRot)
        ParentConstraint.attributeAffects(ParentConstraint.inConstraintParInvMtx, ParentConstraint.outConstRot)
        ParentConstraint.attributeAffects(ParentConstraint.inConstraintParSca, ParentConstraint.outConstRot)
        ParentConstraint.attributeAffects(ParentConstraint.inTargetWorldMatrix, ParentConstraint.outConstRot)
        ParentConstraint.attributeAffects(ParentConstraint.inTargetOffset, ParentConstraint.outConstRot)
        # ParentConstraint.attributeAffects(ParentConstraint.inTargetJntOri, ParentConstraint.outConstRot)
        # ParentConstraint.attributeAffects(ParentConstraint.inTargetRotOrder, ParentConstraint.outConstRot)
        ParentConstraint.attributeAffects(ParentConstraint.inTargetWeight, ParentConstraint.outConstRot)
        ParentConstraint.attributeAffects(ParentConstraint.inConstraintJntOri, ParentConstraint.outConstSca)
        ParentConstraint.attributeAffects(ParentConstraint.inConstraintRotOrder, ParentConstraint.outConstSca)
        ParentConstraint.attributeAffects(ParentConstraint.inConstraintParInvMtx, ParentConstraint.outConstSca)
        ParentConstraint.attributeAffects(ParentConstraint.inConstraintParSca, ParentConstraint.outConstSca)
        ParentConstraint.attributeAffects(ParentConstraint.inTargetWorldMatrix, ParentConstraint.outConstSca)
        ParentConstraint.attributeAffects(ParentConstraint.inTargetOffset, ParentConstraint.outConstSca)
        # ParentConstraint.attributeAffects(ParentConstraint.inTargetJntOri, ParentConstraint.outConstSca)
        # ParentConstraint.attributeAffects(ParentConstraint.inTargetRotOrder, ParentConstraint.outConstSca)
        ParentConstraint.attributeAffects(ParentConstraint.inTargetWeight, ParentConstraint.outConstSca)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        eConstJntOri = om2.MEulerRotation(dataBlock.inputValue(ParentConstraint.inConstraintJntOri).asDouble3())
        mConstParInv = dataBlock.inputValue(ParentConstraint.inConstraintParInvMtx).asMatrix()
        constRotOrder = dataBlock.inputValue(ParentConstraint.inConstraintRotOrder).asShort()
        constParSca = dataBlock.inputValue(ParentConstraint.inConstraintParSca).asFloat3()
        targetListHandle = dataBlock.inputArrayValue(ParentConstraint.inTargetList)
        mTargetsAdded = om2.MMatrix()
        mtxFn = om2.MTransformationMatrix()
        mtxFn.scaleBy(constParSca, om2.MSpace.kTransform)
        mInvSca = mtxFn.asMatrix()

        for i in range(len(targetListHandle)):
            targetListHandle.jumpToLogicalElement(i)
            targetHandle = targetListHandle.inputValue()
            # targetJntOri = om2.MEulerRotation(targetHandle.child(ParentConstraint.inTargetJntOri).asDouble3())
            # targetRotOrder = targetHandle.child(ParentConstraint.inTargetRotOrder).asShort()
            mTargetW = targetHandle.child(ParentConstraint.inTargetWorldMatrix).asMatrix()
            mOffset = targetHandle.child(ParentConstraint.inTargetOffset).asMatrix()
            targetWeight = targetHandle.child(ParentConstraint.inTargetWeight).asFloat()

            mTarget = mOffset * (mTargetW * targetWeight)
            if mTargetsAdded == om2.MMatrix():
                mTargetsAdded = mTarget
            else:
                mTargetsAdded += mTarget

        mResult = mTargetsAdded * mConstParInv * mInvSca

        if plug == ParentConstraint.outConstTrans:
            outTransHandle = dataBlock.outputValue(ParentConstraint.outConstTrans)
            outTrans = om2.MFloatVector(mResult[12], mResult[13], mResult[14])
            outTransHandle.setMFloatVector(outTrans)
            outTransHandle.setClean()
        if plug == ParentConstraint.outConstRot:
            outRotHandle = dataBlock.outputValue(ParentConstraint.outConstRot)
            mtxFn = om2.MTransformationMatrix(mResult)
            eRotMtx = mtxFn.rotation(asQuaternion=False)
            qRotMtx = eRotMtx.asQuaternion()
            qConstJntOri = eConstJntOri.asQuaternion()
            qOutRot = qRotMtx * qConstJntOri.invertIt()
            outRot = qOutRot.asEulerRotation().reorderIt(constRotOrder)
            outRotHandle.setMVector(outRot.asVector())
            outRotHandle.setClean()
        if plug == ParentConstraint.outConstSca:
            outScaHandle = dataBlock.outputValue(ParentConstraint.outConstSca)
            mtxFn = om2.MTransformationMatrix(mResult)
            outSca = mtxFn.scale(om2.MSpace.kWorld)
            outScaHandle.set3Float(outSca[0], outSca[1], outSca[2])
            outScaHandle.setClean()
