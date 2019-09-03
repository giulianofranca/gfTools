# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfUtilDoubleToAngle node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.

Requirements:
    Maya 2017 or above.

Todo:
    * Convert angle values to radians.

This code supports Pylint. Rc file in project.
"""
# pylint: disable=import-error
# import-error = Supress Maya modules import error

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


class DoubleToAngle(om2.MPxNode):
    """ Main class of gfUtilDoubleToAngle node. """

    kNODE_NAME = ""
    kNODE_CLASSIFY = ""
    kNODE_ID = ""

    inDouble = om2.MObject()
    outAngle = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return DoubleToAngle()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to DoubleToAngle class. Instances of DoubleToAngle will use these attributes to create plugs
        for use in the compute() method.
        """
        nAttr = om2.MFnNumericAttribute()
        uAttr = om2.MFnUnitAttribute()

        DoubleToAngle.inDouble = nAttr.create("double", "double", om2.MFnNumericData.kDouble, 0.0)
        INPUT_ATTR(nAttr)

        DoubleToAngle.outAngle = uAttr.create("outAngle", "oa", om2.MFnUnitAttribute.kAngle, 0.0)
        OUTPUT_ATTR(uAttr)

        DoubleToAngle.addAttribute(DoubleToAngle.inDouble)
        DoubleToAngle.addAttribute(DoubleToAngle.outAngle)
        DoubleToAngle.attributeAffects(DoubleToAngle.inDouble, DoubleToAngle.outAngle)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != DoubleToAngle.outAngle:
            return om2.kUnknownParameter

        double = dataBlock.inputValue(DoubleToAngle.inDouble).asDouble()
        outAngleHandle = dataBlock.outputValue(DoubleToAngle.outAngle)

        outAngleHandle.setMAngle(om2.MAngle(double, om2.MAngle.kDegrees))
        outAngleHandle.setClean()
