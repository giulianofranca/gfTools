# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfUtilAngularTrigMath node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.

Requirements:
    Maya 2017 or above.

Todo:
    * https://en.wikipedia.org/wiki/Inverse_trigonometric_functions

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


class AngularTrigMath(om2.MPxNode):
    """ Main class of gfUtilAngularTrigMath node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

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
        return AngularTrigMath()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to AngularTrigMath class. Instances of AngularTrigMath will use these attributes to create plugs
        for use in the compute() method.
        """
        uAttr = om2.MFnUnitAttribute()
        eAttr = om2.MFnEnumAttribute()

        AngularTrigMath.inAngle1 = uAttr.create("angle1", "a1", om2.MFnUnitAttribute.kAngle, 0.0)
        INPUT_ATTR(uAttr)

        AngularTrigMath.inAngle2 = uAttr.create("angle2", "a2", om2.MFnUnitAttribute.kAngle, 0.0)
        INPUT_ATTR(uAttr)

        AngularTrigMath.inOperation = eAttr.create("operation", "operation", 0)
        eAttr.addField("No Operation", 0)
        eAttr.addField("Cosine", 1)
        eAttr.addField("Sine", 2)
        eAttr.addField("Tangent", 3)
        eAttr.addField("Arccos", 4)
        eAttr.addField("Arcsin", 5)
        eAttr.addField("Arctan", 6)
        eAttr.addField("Arctan2", 7)
        INPUT_ATTR(eAttr)

        AngularTrigMath.outAngle = uAttr.create("outAngle", "oa", om2.MFnUnitAttribute.kAngle, 0.0)
        OUTPUT_ATTR(uAttr)

        AngularTrigMath.addAttribute(AngularTrigMath.inOperation)
        AngularTrigMath.addAttribute(AngularTrigMath.inAngle1)
        AngularTrigMath.addAttribute(AngularTrigMath.inAngle2)
        AngularTrigMath.addAttribute(AngularTrigMath.outAngle)
        AngularTrigMath.attributeAffects(AngularTrigMath.inAngle1, AngularTrigMath.outAngle)
        AngularTrigMath.attributeAffects(AngularTrigMath.inAngle2, AngularTrigMath.outAngle)
        AngularTrigMath.attributeAffects(AngularTrigMath.inOperation, AngularTrigMath.outAngle)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != AngularTrigMath.outAngle:
            return om2.kUnknownParameter

        angle1 = dataBlock.inputValue(AngularTrigMath.inAngle1).asAngle()
        operation = dataBlock.inputValue(AngularTrigMath.inOperation).asShort()

        outAngleHandle = dataBlock.outputValue(AngularTrigMath.outAngle)

        if operation == 0:
            outAngleHandle.setMAngle(angle1)
        elif operation == 1:
            outAngle = math.cos(angle1.asRadians())
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))
        elif operation == 2:
            outAngle = math.sin(angle1.asRadians())
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))
        elif operation == 3:
            outAngle = math.tan(angle1.asRadians())
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kDegrees))
        elif operation == 4:
            resAngle = angle1.asDegrees()
            if resAngle > 1.0:
                resAngle = 1.0
            elif resAngle < -1.0:
                resAngle = -1.0
            outAngle = math.acos(resAngle)
            outAngleHandle.setMAngle(om2.MAngle(outAngle))
        elif operation == 5:
            resAngle = angle1.asDegrees()
            if resAngle > 1.0:
                resAngle = 1.0
            elif resAngle < -1.0:
                resAngle = -1.0
            outAngle = math.asin(resAngle)
            outAngleHandle.setMAngle(om2.MAngle(outAngle))
        elif operation == 6:
            outAngle = math.atan(angle1.asRadians())
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kRadians))
        elif operation == 7:
            angle2 = dataBlock.inputValue(AngularTrigMath.inAngle2).asAngle()
            outAngle = math.atan2(angle1.asRadians(), angle2.asRadians())
            outAngleHandle.setMAngle(om2.MAngle(outAngle, om2.MAngle.kRadians))

        outAngleHandle.setClean()
