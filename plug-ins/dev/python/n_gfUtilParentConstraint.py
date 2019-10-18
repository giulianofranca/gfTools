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

    inOffset = om2.MObject()
    inTargetWMtx = om2.MObject()
    # inTargetRotOrder = om2.MObject()
    # inTargetWeight = om2.MObject()
    inConstParInvMtx = om2.MObject()
    # inConstJntOri = om2.MObject()
    # inConstRotOrder = om2.MObject()
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

        ParentConstraint.inOffset = mAttr.create("offset", "offset", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        ParentConstraint.inTargetWMtx = mAttr.create("targetWorldMatrix", "twmtx", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        # ParentConstraint.inTargetRotOrder = eAttr.create("targetRotateOrder", "tro", 0)
        # eAttr.addField("xyz", 0)
        # eAttr.addField("yzx", 1)
        # eAttr.addField("zxy", 2)
        # eAttr.addField("xzy", 3)
        # eAttr.addField("yxz", 4)
        # eAttr.addField("zyx", 5)
        # INPUT_ATTR(eAttr)

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
        # ParentConstraint.addAttribute(ParentConstraint.inTargetRotOrder)
        ParentConstraint.addAttribute(ParentConstraint.inTargetWeight)
        ParentConstraint.addAttribute(ParentConstraint.inConstParInvMtx)
        ParentConstraint.addAttribute(ParentConstraint.inConstJntOri)
        ParentConstraint.addAttribute(ParentConstraint.inConstRotOrder)
        ParentConstraint.addAttribute(ParentConstraint.outConstraint)
        ParentConstraint.attributeAffects(ParentConstraint.inOffset, ParentConstraint.outConstraint)
        ParentConstraint.attributeAffects(ParentConstraint.inTargetWMtx, ParentConstraint.outConstraint)
        # ParentConstraint.attributeAffects(ParentConstraint.inTargetRotOrder, ParentConstraint.outConstraint)
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
        # targetRotOrder = dataBlock.inputValue(ParentConstraint.inTargetRotOrder).asShort()
        # targetWeight = dataBlock.inputValue(ParentConstraint.inTargetWeight).asDouble()
        mConstParInv = dataBlock.inputValue(ParentConstraint.inConstParInvMtx).asMatrix()
        eConstJntOri = om2.MEulerRotation(dataBlock.inputValue(ParentConstraint.inConstJntOri).asDouble3())
        constRotOrder = dataBlock.inputValue(ParentConstraint.inConstRotOrder).asShort()

        # mtxFn = om2.MTransformationMatrix()
        # mtxFn.rotateBy(eConstJntOri.invertIt(), om2.MSpace.kTransform)
        # mConstJntOri = mtxFn.asMatrix()

        mResult = mOffset * mTargetWorld * mConstParInv

        vResult = om2.MVector(mResult[12], mResult[13], mResult[14])
        eResult = om2.MEulerRotation.decompose(mResult, om2.MEulerRotation.kXYZ)
        eResult.reorderIt(constRotOrder)
        eResult += eConstJntOri.invertIt()
        result = om2.MTransformationMatrix(mResult).scale(om2.MSpace.kTransform)
        mtxFn = om2.MTransformationMatrix()
        mtxFn.scaleBy(result, om2.MSpace.kTransform)
        mtxFn.rotateBy(eResult, om2.MSpace.kTransform)
        mtxFn.translateBy(vResult, om2.MSpace.kTransform)

        mConstraint = mtxFn.asMatrix()
        # mConstraint *= targetWeight

        outConstraintHandle = dataBlock.outputValue(ParentConstraint.outConstraint)
        outConstraintHandle.setMMatrix(mConstraint)
        outConstraintHandle.setClean()
