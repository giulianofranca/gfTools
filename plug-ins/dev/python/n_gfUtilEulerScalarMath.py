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
    Basic euler rotation operations with float scalar. No operation value returns the euler rotation.
    Support addition, subtraction and multiply.

Attributes:
    * Operation: The math operation. Can be add, subtract or multiply.
    * Euler: The euler rotation of the operation.
    * Euler Rotate Order: The rotation order of the euler rotation.
    * Scalar: The scalar value of the operation.
    * Rotate Order Out Euler: The rotation order of the output euler rotation.
    * Out Euler: The output euler rotation.

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


class EulerScalarMath(om2.MPxNode):
    """ Main class of gfUtilEulerScalarMath node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inOperation = om2.MObject()
    inEuler = om2.MObject()
    inEulerRotOrder = om2.MObject()
    inScalar = om2.MObject()
    inResRotOrder = om2.MObject()
    outEuler = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return EulerScalarMath()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to EulerScalarMath class. Instances of EulerScalarMath will use these attributes to create plugs
        for use in the compute() method.
        """
        eAttr = om2.MFnEnumAttribute()
        uAttr = om2.MFnUnitAttribute()
        nAttr = om2.MFnNumericAttribute()

        EulerScalarMath.inOperation = eAttr.create("operation", "operation", 0)
        eAttr.addField("No Operation", 0)
        eAttr.addField("Add", 1)
        eAttr.addField("Subtract", 2)
        eAttr.addField("Multiply", 3)
        INPUT_ATTR(eAttr)

        eulerX = uAttr.create("eulerX", "ex", om2.MFnUnitAttribute.kAngle, 0.0)
        eulerY = uAttr.create("eulerY", "ey", om2.MFnUnitAttribute.kAngle, 0.0)
        eulerZ = uAttr.create("eulerZ", "ez", om2.MFnUnitAttribute.kAngle, 0.0)
        EulerScalarMath.inEuler = nAttr.create("euler", "e", eulerX, eulerY, eulerZ)
        INPUT_ATTR(nAttr)

        EulerScalarMath.inEulerRotOrder = eAttr.create("rotateOrderEuler", "roe", 0)
        eAttr.addField("xyz", 0)
        eAttr.addField("yzx", 1)
        eAttr.addField("zxy", 2)
        eAttr.addField("xzy", 3)
        eAttr.addField("yxz", 4)
        eAttr.addField("zyx", 5)
        INPUT_ATTR(eAttr)

        EulerScalarMath.inScalar = nAttr.create("scalar", "scalar", om2.MFnNumericData.kDouble, 0.0)
        INPUT_ATTR(nAttr)

        EulerScalarMath.inResRotOrder = eAttr.create("rotateOrderOutEuler", "rooe", 0)
        eAttr.addField("xyz", 0)
        eAttr.addField("yzx", 1)
        eAttr.addField("zxy", 2)
        eAttr.addField("xzy", 3)
        eAttr.addField("yxz", 4)
        eAttr.addField("zyx", 5)
        INPUT_ATTR(eAttr)

        outEulerX = uAttr.create("outEulerX", "oex", om2.MFnUnitAttribute.kAngle, 0.0)
        outEulerY = uAttr.create("outEulerY", "oey", om2.MFnUnitAttribute.kAngle, 0.0)
        outEulerZ = uAttr.create("outEulerZ", "oez", om2.MFnUnitAttribute.kAngle, 0.0)
        EulerScalarMath.outEuler = nAttr.create("outEuler", "oe", outEulerX, outEulerY, outEulerZ)
        OUTPUT_ATTR(nAttr)

        EulerScalarMath.addAttribute(EulerScalarMath.inOperation)
        EulerScalarMath.addAttribute(EulerScalarMath.inEuler)
        EulerScalarMath.addAttribute(EulerScalarMath.inEulerRotOrder)
        EulerScalarMath.addAttribute(EulerScalarMath.inScalar)
        EulerScalarMath.addAttribute(EulerScalarMath.inResRotOrder)
        EulerScalarMath.addAttribute(EulerScalarMath.outEuler)
        EulerScalarMath.attributeAffects(EulerScalarMath.inOperation, EulerScalarMath.outEuler)
        EulerScalarMath.attributeAffects(EulerScalarMath.inEuler, EulerScalarMath.outEuler)
        EulerScalarMath.attributeAffects(EulerScalarMath.inEulerRotOrder, EulerScalarMath.outEuler)
        EulerScalarMath.attributeAffects(EulerScalarMath.inScalar, EulerScalarMath.outEuler)
        EulerScalarMath.attributeAffects(EulerScalarMath.inResRotOrder, EulerScalarMath.outEuler)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != EulerScalarMath.outEuler:
            return om2.kUnknownParameter

        operation = dataBlock.inputValue(EulerScalarMath.inOperation).asShort()
        vEuler = dataBlock.inputValue(EulerScalarMath.inEuler).asVector()
        scalar = dataBlock.inputValue(EulerScalarMath.inScalar).asDouble()
        eulerRotOder = dataBlock.inputValue(EulerScalarMath.inEulerRotOrder).asShort()
        outRotOrder = dataBlock.inputValue(EulerScalarMath.inResRotOrder).asShort()

        eEuler = om2.MEulerRotation(vEuler, eulerRotOder)

        outEulerHandle = dataBlock.outputValue(EulerScalarMath.outEuler)

        if operation == 0:
            eEuler.reorderIt(outRotOrder)
            vResult = eEuler.asVector()
            outEulerHandle.setMVector(vResult)
        elif operation == 1:
            eEuler.reorderIt(outRotOrder)
            vScalar = om2.MVector(
                om2.MAngle(scalar, om2.MAngle.kDegrees).asRadians(),
                om2.MAngle(scalar, om2.MAngle.kDegrees).asRadians(),
                om2.MAngle(scalar, om2.MAngle.kDegrees).asRadians(),
            )
            vResult = eEuler.asVector() + vScalar
            outEulerHandle.setMVector(vResult)
        elif operation == 2:
            eEuler.reorderIt(outRotOrder)
            vScalar = om2.MVector(
                om2.MAngle(scalar, om2.MAngle.kDegrees).asRadians(),
                om2.MAngle(scalar, om2.MAngle.kDegrees).asRadians(),
                om2.MAngle(scalar, om2.MAngle.kDegrees).asRadians(),
            )
            vResult = eEuler.asVector() - vScalar
            outEulerHandle.setMVector(vResult)
        elif operation == 3:
            eEuler.reorderIt(outRotOrder)
            eOutEuler = eEuler * scalar
            vResult = eOutEuler.asVector()
            outEulerHandle.setMVector(vResult)

        outEulerHandle.setClean()
