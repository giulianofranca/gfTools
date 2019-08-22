# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfUtilAngleToDouble node. You should be using the related C++ version.]
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


class AngleToDouble(om2.MPxNode):
    """ Main class of gfUtilAngleToDouble node. """

    kNODE_NAME = ""
    kNODE_CLASSIFY = ""
    kNODE_ID = ""

    inAngle = om2.MObject()
    outDouble = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return AngleToDouble()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to AngleToDouble class. Instances of AngleToDouble will use these attributes to create plugs
        for use in the compute() method.
        """
        uAttr = om2.MFnUnitAttribute()
        nAttr = om2.MFnNumericAttribute()

        AngleToDouble.inAngle = uAttr.create("angle", "angle", om2.MFnUnitAttribute.kAngle, 0.0)
        INPUT_ATTR(uAttr)

        AngleToDouble.outDouble = nAttr.create("outDouble", "od", om2.MFnNumericData.kDouble, 0.0)
        OUTPUT_ATTR(nAttr)

        AngleToDouble.addAttribute(AngleToDouble.inAngle)
        AngleToDouble.addAttribute(AngleToDouble.outDouble)
        AngleToDouble.attributeAffects(AngleToDouble.inAngle, AngleToDouble.outDouble)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != AngleToDouble.outDouble:
            return om2.kUnknownParameter

        angle = dataBlock.inputValue(AngleToDouble.inAngle).asAngle().asDegrees()
        outDoubleHandle = dataBlock.outputValue(AngleToDouble.outDouble)

        outDoubleHandle.setDouble(angle)
        outDoubleHandle.setClean()
