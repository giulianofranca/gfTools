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
# pylint: disable=import-error
# import-error = Supress Maya modules import error

import math
import maya.api.OpenMaya as om2


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


class AngularMath(om2.MPxNode):
    """ Main class of gfUtilAngularMath node. """

    kNODE_NAME = ""
    kNODE_CLASSIFY = ""
    kNODE_ID = ""

    inAngle1 = om2.MObject()
    inAngle2 = om2.MObject()
    inOperation = om2.MObject()
    outAngle = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return AngularMath()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to AngularMath class. Instances of AngularMath will use these attributes to create plugs
        for use in the compute() method.
        """
        uAttr = om2.MFnUnitAttribute()
        eAttr = om2.MFnEnumAttribute()

        AngularMath.inAngle1 = uAttr.create("angle1", "a1", om2.MFnUnitAttribute.kAngle, 0.0)
        INPUT_ATTR(uAttr)

        AngularMath.inAngle2 = uAttr.create("angle2", "a2", om2.MFnUnitAttribute.kAngle, 0.0)
        INPUT_ATTR(uAttr)

        AngularMath.inOperation = eAttr.create("operation", "operation", 0)
        eAttr.addField("No Operation", 0)
        eAttr.addField("Add", 1)
        eAttr.addField("Subtract", 2)
        eAttr.addField("Multiply", 3)
        eAttr.addField("Divide", 4)
        eAttr.addField("Power", 5)
        eAttr.addField("Min", 6)
        eAttr.addField("Max", 7)
        INPUT_ATTR(eAttr)

        AngularMath.outAngle = uAttr.create("outAngle", "oa", om2.MFnUnitAttribute.kAngle, 0.0)
        OUTPUT_ATTR(uAttr)

        AngularMath.addAttribute(AngularMath.inOperation)
        AngularMath.addAttribute(AngularMath.inAngle1)
        AngularMath.addAttribute(AngularMath.inAngle2)
        AngularMath.addAttribute(AngularMath.outAngle)
        AngularMath.attributeAffects(AngularMath.inAngle1, AngularMath.outAngle)
        AngularMath.attributeAffects(AngularMath.inAngle2, AngularMath.outAngle)
        AngularMath.attributeAffects(AngularMath.inOperation, AngularMath.outAngle)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != AngularMath.outAngle:
            return om2.kUnknownParameter

        angle1 = dataBlock.inputValue(AngularMath.inAngle1).asAngle().asDegrees()
        angle2 = dataBlock.inputValue(AngularMath.inAngle2).asAngle().asDegrees()
        operation = dataBlock.inputValue(AngularMath.inOperation).asShort()

        outAngleHandle = dataBlock.outputValue(AngularMath.outAngle)

        if operation == 0:
            outAngleHandle.setMAngle(om2.MAngle(angle1, om2.MAngle.kDegrees))
        elif operation == 1:
            outAngle = angle1 + angle2
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))
        elif operation == 2:
            outAngle = angle1 - angle2
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))
        elif operation == 3:
            outAngle = angle1 * angle2
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))
        elif operation == 4:
            if angle2 != 0.0:
                outAngle = angle1 / angle2
            else:
                outAngle = 9999.999
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))
        elif operation == 5:
            outAngle = math.pow(angle1, angle2)
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))
        elif operation == 6:
            outAngle = min(angle1, angle2)
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))
        elif operation == 7:
            outAngle = max(angle1, angle2)
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))

        outAngleHandle.setClean()
