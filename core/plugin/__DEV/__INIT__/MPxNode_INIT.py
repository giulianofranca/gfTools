# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Maya IDs:
    Prototypes: 0x0012f7c0 - 0x0012f7ff
    Releases: 0x00130d80 - 0x00130e7f

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfTestNode node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.

How to use:
    * Copy and paste this file to a Maya plugins path, default: "C:/Users/<user>/Documents/maya/<version>/plug-ins".
        You can create a "plug-ins" folder if not exists.
    * Open your Maya (same version).
    * Go to Windows > Settings/Preferences > Plug-in Manager.
    * Mark this file as loaded.

Requirements:
    Maya 2017 or above.

Todo:
    * NDA

This code supports Pylint. Rc file in project.
"""

import sys
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


class TestNode(om2.MPxNode):
    """ Main class of gfTestNode node. """

    kNodeName = "gfTestNode"
    kNodeClassify = "utility/general"
    kNodeID = om2.MTypeId(0x0012f7c2)

    inAttr = om2.MObject()
    outAttr = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return TestNode()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to TestNode class. Instances of TestNode will use these attributes to create plugs
        for use in the compute() method.
        """
        nAttr = om2.MFnNumericAttribute()

        TestNode.inAttr = nAttr.createPoint("inAttr", "ina")
        INPUT_ATTR(nAttr)

        TestNode.outAttr = nAttr.createPoint("outAttr", "outa")
        OUTPUT_ATTR(nAttr)

        TestNode.addAttribute(TestNode.inAttr)
        TestNode.addAttribute(TestNode.outAttr)
        TestNode.attributeAffects(TestNode.inAttr, TestNode.outAttr)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug == TestNode.outAttr:
            inAttrValue = dataBlock.inputValue(TestNode.inAttr).asFloat3()

            outAttrHandle = dataBlock.outputValue(TestNode.outAttr)
            outAttrHandle.set3Float(inAttrValue[0], inAttrValue[1], inAttrValue[2])
            outAttrHandle.setClean()


def initializePlugin(mobject):
    """ Initializes the plug-in. """
    mplugin = om2.MFnPlugin(mobject)
    try:
        mplugin.registerNode(TestNode.kNodeName, TestNode.kNodeID, TestNode.creator,
                             TestNode.initialize, om2.MPxNode.kDependNode, TestNode.kNodeClassify)
    except:
        sys.stderr.write("Failed to register node: " + TestNode.kNodeName)
        raise


def uninitializePlugin(mobject):
    """ Unitializes the plug-in. """
    mplugin = om2.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(TestNode.kNodeID)
    except:
        sys.stderr.write("Failed to deregister node: " + TestNode.kNodeName)
        raise
