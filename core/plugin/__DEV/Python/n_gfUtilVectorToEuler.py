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


class VectorToEuler(om2.MPxNode):
    """ Main class of gfUtilVectorToEuler node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inVector = om2.MObject()
    outEuler = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return VectorToEuler()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to VectorToEuler class. Instances of VectorToEuler will use these attributes to create plugs
        for use in the compute() method.
        """
        uAttr = om2.MFnUnitAttribute()
        nAttr = om2.MFnNumericAttribute()

        vectorX = nAttr.create("vectorX", "vecx", om2.MFnNumericData.kDouble, 0.0)
        vectorY = nAttr.create("vectorY", "vecy", om2.MFnNumericData.kDouble, 0.0)
        vectorZ = nAttr.create("vectorZ", "vecz", om2.MFnNumericData.kDouble, 0.0)
        VectorToEuler.inVector = nAttr.create("vector", "vec", vectorX, vectorY, vectorZ)
        INPUT_ATTR(nAttr)

        outEulerX = uAttr.create("outEulerX", "oex", om2.MFnUnitAttribute.kAngle, 0.0)
        outEulerY = uAttr.create("outEulerY", "oey", om2.MFnUnitAttribute.kAngle, 0.0)
        outEulerZ = uAttr.create("outEulerZ", "oez", om2.MFnUnitAttribute.kAngle, 0.0)
        VectorToEuler.outEuler = nAttr.create("outEuler", "oe", outEulerX, outEulerY, outEulerZ)
        OUTPUT_ATTR(nAttr)

        VectorToEuler.addAttribute(VectorToEuler.inVector)
        VectorToEuler.addAttribute(VectorToEuler.outEuler)
        VectorToEuler.attributeAffects(VectorToEuler.inVector, VectorToEuler.outEuler)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != VectorToEuler.outEuler:
            return om2.kUnknownParameter

        vVector = dataBlock.inputValue(VectorToEuler.inVector).asVector()
        eEuler = om2.MEulerRotation(
            om2.MAngle(vVector.x, om2.MAngle.kDegrees).asRadians(),
            om2.MAngle(vVector.y, om2.MAngle.kDegrees).asRadians(),
            om2.MAngle(vVector.z, om2.MAngle.kDegrees).asRadians(),
            om2.MEulerRotation.kXYZ
        )

        outEulerHandle = dataBlock.outputValue(VectorToEuler.outEuler)
        outEulerHandle.setMVector(eEuler.asVector())
        outEulerHandle.setClean()
