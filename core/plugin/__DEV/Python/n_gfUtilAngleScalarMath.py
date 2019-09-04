# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfUtilAngularScalarMath node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.

Requirements:
    Maya 2017 or above.

Todo:
    * Convert angle values to radians.

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


class AngularScalarMath(om2.MPxNode):
    """ Main class of gfUtilAngularScalarMath node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inAngle = om2.MObject()
    inScalar = om2.MObject()
    inOperation = om2.MObject()
    outAngle = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return AngularScalarMath()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to AngularScalarMath class. Instances of AngularScalarMath will use these attributes to create plugs
        for use in the compute() method.
        """
        uAttr = om2.MFnUnitAttribute()
        nAttr = om2.MFnNumericAttribute()
        eAttr = om2.MFnEnumAttribute()

        AngularScalarMath.inAngle = uAttr.create("angle", "angle", om2.MFnUnitAttribute.kAngle, 0.0)
        INPUT_ATTR(uAttr)

        AngularScalarMath.inScalar = nAttr.create("scalar", "scalar", om2.MFnNumericData.kDouble, 0.0)
        INPUT_ATTR(nAttr)

        AngularScalarMath.inOperation = eAttr.create("operation", "operation", 0)
        eAttr.addField("No Operation", 0)
        eAttr.addField("Add", 1)
        eAttr.addField("Subtract", 2)
        eAttr.addField("Multiply", 3)
        eAttr.addField("Divide", 4)
        eAttr.addField("Power", 5)
        eAttr.addField("Min", 6)
        eAttr.addField("Max", 7)
        INPUT_ATTR(eAttr)

        AngularScalarMath.outAngle = uAttr.create("outAngle", "oa", om2.MFnUnitAttribute.kAngle, 0.0)
        OUTPUT_ATTR(uAttr)

        AngularScalarMath.addAttribute(AngularScalarMath.inOperation)
        AngularScalarMath.addAttribute(AngularScalarMath.inAngle)
        AngularScalarMath.addAttribute(AngularScalarMath.inScalar)
        AngularScalarMath.addAttribute(AngularScalarMath.outAngle)
        AngularScalarMath.attributeAffects(AngularScalarMath.inAngle, AngularScalarMath.outAngle)
        AngularScalarMath.attributeAffects(AngularScalarMath.inScalar, AngularScalarMath.outAngle)
        AngularScalarMath.attributeAffects(AngularScalarMath.inOperation, AngularScalarMath.outAngle)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != AngularScalarMath.outAngle:
            return om2.kUnknownParameter

        angle = dataBlock.inputValue(AngularScalarMath.inAngle).asAngle().asDegrees()
        scalar = dataBlock.inputValue(AngularScalarMath.inScalar).asDouble()
        operation = dataBlock.inputValue(AngularScalarMath.inOperation).asShort()

        outAngleHandle = dataBlock.outputValue(AngularScalarMath.outAngle)

        if operation == 0:
            outAngleHandle.setMAngle(om2.MAngle(angle, om2.MAngle.kDegrees))
        elif operation == 1:
            outAngle = angle + scalar
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))
        elif operation == 2:
            outAngle = angle - scalar
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))
        elif operation == 3:
            outAngle = angle * scalar
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))
        elif operation == 4:
            if scalar != 0.0:
                outAngle = angle / scalar
            else:
                outAngle = 9999.999
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))
        elif operation == 5:
            outAngle = math.pow(angle, scalar)
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))
        elif operation == 6:
            outAngle = min(angle, scalar)
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))
        elif operation == 7:
            outAngle = max(angle, scalar)
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))

        outAngleHandle.setClean()
