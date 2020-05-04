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
    Basic euler rotation operations. No operation value returns the first euler.
    Support addition, subtraction and multiply.

Attributes:
    * Operation: The math operation. Can be add, subtract or multiply.
    * Euler 1: The first euler rotation of the operation.
    * Euler 1 Rotate Order: The rotation order of the first euler rotation.
    * Euler 2: The second euler rotation of the operation.
    * Euler 2 Rotate Order: The rotation order of the second euler rotation.
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


class EulerMath(om2.MPxNode):
    """ Main class of gfUtilEulerMath node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inOperation = om2.MObject()
    inEuler1 = om2.MObject()
    inEuler1X = om2.MObject()
    inEuler1Y = om2.MObject()
    inEuler1Z = om2.MObject()
    inEuler1RotOrder = om2.MObject()
    inEuler2 = om2.MObject()
    inEuler2X = om2.MObject()
    inEuler2Y = om2.MObject()
    inEuler2Z = om2.MObject()
    inEuler2RotOrder = om2.MObject()
    inResRotOrder = om2.MObject()
    outEuler = om2.MObject()
    outEulerX = om2.MObject()
    outEulerY = om2.MObject()
    outEulerZ = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return EulerMath()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to EulerMath class. Instances of EulerMath will use these attributes to create plugs
        for use in the compute() method.
        """
        eAttr = om2.MFnEnumAttribute()
        uAttr = om2.MFnUnitAttribute()
        nAttr = om2.MFnNumericAttribute()

        EulerMath.inOperation = eAttr.create("operation", "operation", 0)
        eAttr.addField("No Operation", 0)
        eAttr.addField("Add", 1)
        eAttr.addField("Subtract", 2)
        eAttr.addField("Multiply", 3)
        INPUT_ATTR(eAttr)

        EulerMath.inEuler1X = uAttr.create("euler1X", "e1x", om2.MFnUnitAttribute.kAngle, 0.0)
        EulerMath.inEuler1Y = uAttr.create("euler1Y", "e1y", om2.MFnUnitAttribute.kAngle, 0.0)
        EulerMath.inEuler1Z = uAttr.create("euler1Z", "e1z", om2.MFnUnitAttribute.kAngle, 0.0)
        EulerMath.inEuler1 = nAttr.create("euler1", "e1", EulerMath.inEuler1X, EulerMath.inEuler1Y, EulerMath.inEuler1Z)
        INPUT_ATTR(nAttr)

        EulerMath.inEuler1RotOrder = eAttr.create("rotateOrderEuler1", "roe1", 0)
        eAttr.addField("xyz", 0)
        eAttr.addField("yzx", 1)
        eAttr.addField("zxy", 2)
        eAttr.addField("xzy", 3)
        eAttr.addField("yxz", 4)
        eAttr.addField("zyx", 5)
        INPUT_ATTR(eAttr)

        EulerMath.inEuler2X = uAttr.create("euler2X", "e2x", om2.MFnUnitAttribute.kAngle, 0.0)
        EulerMath.inEuler2Y = uAttr.create("euler2Y", "e2y", om2.MFnUnitAttribute.kAngle, 0.0)
        EulerMath.inEuler2Z = uAttr.create("euler2Z", "e2z", om2.MFnUnitAttribute.kAngle, 0.0)
        EulerMath.inEuler2 = nAttr.create("euler2", "e2", EulerMath.inEuler2X, EulerMath.inEuler2Y, EulerMath.inEuler2Z)
        INPUT_ATTR(nAttr)

        EulerMath.inEuler2RotOrder = eAttr.create("rotateOrderEuler2", "roe2", 0)
        eAttr.addField("xyz", 0)
        eAttr.addField("yzx", 1)
        eAttr.addField("zxy", 2)
        eAttr.addField("xzy", 3)
        eAttr.addField("yxz", 4)
        eAttr.addField("zyx", 5)
        INPUT_ATTR(eAttr)

        EulerMath.outEulerX = uAttr.create("outEulerX", "oex", om2.MFnUnitAttribute.kAngle, 0.0)
        EulerMath.outEulerY = uAttr.create("outEulerY", "oey", om2.MFnUnitAttribute.kAngle, 0.0)
        EulerMath.outEulerZ = uAttr.create("outEulerZ", "oez", om2.MFnUnitAttribute.kAngle, 0.0)
        EulerMath.outEuler = nAttr.create("outEuler", "oe", EulerMath.outEulerX, EulerMath.outEulerY, EulerMath.outEulerZ)
        OUTPUT_ATTR(nAttr)

        EulerMath.inResRotOrder = eAttr.create("rotateOrderOutEuler", "rooe", 0)
        eAttr.addField("xyz", 0)
        eAttr.addField("yzx", 1)
        eAttr.addField("zxy", 2)
        eAttr.addField("xzy", 3)
        eAttr.addField("yxz", 4)
        eAttr.addField("zyx", 5)
        INPUT_ATTR(eAttr)

        EulerMath.addAttribute(EulerMath.inOperation)
        EulerMath.addAttribute(EulerMath.inEuler1)
        EulerMath.addAttribute(EulerMath.inEuler1RotOrder)
        EulerMath.addAttribute(EulerMath.inEuler2)
        EulerMath.addAttribute(EulerMath.inEuler2RotOrder)
        EulerMath.addAttribute(EulerMath.inResRotOrder)
        EulerMath.addAttribute(EulerMath.outEuler)
        EulerMath.attributeAffects(EulerMath.inOperation, EulerMath.outEuler)
        EulerMath.attributeAffects(EulerMath.inEuler1, EulerMath.outEuler)
        EulerMath.attributeAffects(EulerMath.inEuler1RotOrder, EulerMath.outEuler)
        EulerMath.attributeAffects(EulerMath.inEuler2, EulerMath.outEuler)
        EulerMath.attributeAffects(EulerMath.inEuler2RotOrder, EulerMath.outEuler)
        EulerMath.attributeAffects(EulerMath.inResRotOrder, EulerMath.outEuler)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if (plug != EulerMath.outEuler and
            plug != EulerMath.outEulerX and
            plug != EulerMath.outEulerY and
            plug != EulerMath.outEulerZ):
            return om2.kUnknownParameter

        operation = dataBlock.inputValue(EulerMath.inOperation).asShort()
        euler1 = dataBlock.inputValue(EulerMath.inEuler1).asDouble3()
        euler2 = dataBlock.inputValue(EulerMath.inEuler2).asDouble3()
        euler1RotOrder = dataBlock.inputValue(EulerMath.inEuler1RotOrder).asShort()
        euler2RotOrder = dataBlock.inputValue(EulerMath.inEuler2RotOrder).asShort()
        outRotOrder = dataBlock.inputValue(EulerMath.inResRotOrder).asShort()

        eEuler1 = om2.MEulerRotation(euler1, euler1RotOrder)
        eEuler2 = om2.MEulerRotation(euler2, euler2RotOrder)

        outEulerHdle = dataBlock.outputValue(EulerMath.outEuler)

        if operation == 0:
            eEuler1.reorderIt(outRotOrder)
            outEulerHdle.set3Double(eEuler1.x, eEuler1.y, eEuler1.z)
        elif operation == 1:
            eEuler1.reorderIt(outRotOrder)
            eEuler2.reorderIt(outRotOrder)
            eOutEuler = eEuler1 + eEuler2
            outEulerHdle.set3Double(eOutEuler.x, eOutEuler.y, eOutEuler.z)
        elif operation == 2:
            eEuler1.reorderIt(outRotOrder)
            eEuler2.reorderIt(outRotOrder)
            eOutEuler = eEuler1 - eEuler2
            outEulerHdle.set3Double(eOutEuler.x, eOutEuler.y, eOutEuler.z)
        elif operation == 3:
            eEuler1.reorderIt(outRotOrder)
            eEuler2.reorderIt(outRotOrder)
            eOutEuler = eEuler1 * eEuler2
            outEulerHdle.set3Double(eOutEuler.x, eOutEuler.y, eOutEuler.z)

        outEulerHdle.setClean()
