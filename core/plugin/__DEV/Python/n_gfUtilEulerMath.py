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
    * Convert angle values to radians.

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
    inEuler2 = om2.MObject()
    inRotOrder = om2.MObject()
    outEuler = om2.MObject()

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
        eAttr.addField("Power", 3)
        eAttr.addField("Max", 4)
        eAttr.addField("Min", 5)
        INPUT_ATTR(eAttr)

        euler1X = uAttr.create("euler1X", "e1x", om2.MFnUnitAttribute.kAngle, 0.0)
        euler1Y = uAttr.create("euler1Y", "e1y", om2.MFnUnitAttribute.kAngle, 0.0)
        euler1Z = uAttr.create("euler1Z", "e1z", om2.MFnUnitAttribute.kAngle, 0.0)
        EulerMath.inEuler1 = nAttr.create("euler1", "e1", euler1X, euler1Y, euler1Z)
        INPUT_ATTR(nAttr)

        euler2X = uAttr.create("euler2X", "e2x", om2.MFnUnitAttribute.kAngle, 0.0)
        euler2Y = uAttr.create("euler2Y", "e2y", om2.MFnUnitAttribute.kAngle, 0.0)
        euler2Z = uAttr.create("euler2Z", "e2z", om2.MFnUnitAttribute.kAngle, 0.0)
        EulerMath.inEuler2 = nAttr.create("euler2", "e2", euler2X, euler2Y, euler2Z)
        INPUT_ATTR(nAttr)

        EulerMath.inRotOrder = eAttr.create("rotationOrder", "ro", 0)
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
        EulerMath.outEuler = nAttr.create("outEuler", "oe", outEulerX, outEulerY, outEulerZ)
        OUTPUT_ATTR(nAttr)

        EulerMath.addAttribute(EulerMath.inOperation)
        EulerMath.addAttribute(EulerMath.inEuler1)
        EulerMath.addAttribute(EulerMath.inEuler2)
        EulerMath.addAttribute(EulerMath.inRotOrder)
        EulerMath.addAttribute(EulerMath.outEuler)
        EulerMath.attributeAffects(EulerMath.inOperation, EulerMath.outEuler)
        EulerMath.attributeAffects(EulerMath.inEuler1, EulerMath.outEuler)
        EulerMath.attributeAffects(EulerMath.inEuler2, EulerMath.outEuler)
        EulerMath.attributeAffects(EulerMath.inRotOrder, EulerMath.outEuler)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != EulerMath.outEuler:
            return om2.kUnknownParameter

        rotOrder = dataBlock.inputValue(EulerMath.inRotOrder).asShort()
        operation = dataBlock.inputValue(EulerMath.inOperation).asShort()
        qEuler1 = om2.MEulerRotation(dataBlock.inputValue(EulerMath.inEuler1).asDouble3()).asQuaternion()
        qEuler2 = om2.MEulerRotation(dataBlock.inputValue(EulerMath.inEuler2).asDouble3()).asQuaternion()

        outEulerHandle = dataBlock.outputValue(EulerMath.outEuler)

        if operation == 0:
            vResult = qEuler1.asEulerRotation().asVector()
            outEulerHandle.setMVector(vResult)
        elif operation == 1:
            vEuler1 = qEuler1.asEulerRotation().asVector()
            vEuler2 = qEuler2.asEulerRotation().asVector()
            vResult = vEuler1 + vEuler2
            outEulerHandle.setMVector(vResult)
        elif operation == 2:
            vEuler1 = qEuler1.asEulerRotation().asVector()
            vEuler2 = qEuler2.asEulerRotation().asVector()
            vResult = vEuler1 - vEuler2
            outEulerHandle.setMVector(vResult)
        elif operation == 3:
            pass

        outEulerHandle.setClean()
