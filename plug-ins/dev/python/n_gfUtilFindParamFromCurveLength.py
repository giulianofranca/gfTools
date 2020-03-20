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
    Distribute objects along a line in surface. The distribution is uniform and based
    on a number of outputs.

Attributes:
    * Input Surface: The input Nurbs Surface shape to be used.
    * Distribute Along: The direction of the distribution line.
    * Displace Tangent: Displace the line tangent along the surface.
    * Always Uniform: Asure that the distribution is always uniform. (Affect performance).
    * Output Transform: The world matrix of each output object.

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


class FindParamFromLength(om2.MPxNode):
    """ Main class of gfFindParamFromLength node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inCurve = om2.MObject()
    inArcLength = om2.MObject()
    outParam = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return FindParamFromLength()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to DistributeAlongSurface class. Instances of DistributeAlongSurface will use these attributes to create plugs
        for use in the compute() method.
        """
        tAttr = om2.MFnTypedAttribute()
        nAttr = om2.MFnNumericAttribute()
        uAttr = om2.MFnUnitAttribute()

        FindParamFromLength.inCurve = tAttr.create("inputCurve", "icrv", om2.MFnData.kNurbsCurve)
        INPUT_ATTR(tAttr)

        FindParamFromLength.inArcLength = uAttr.create("arcLength", "length", om2.MFnUnitAttribute.kDistance, 0.0)
        INPUT_ATTR(uAttr)

        FindParamFromLength.outParam = nAttr.create("outParam", "param", om2.MFnNumericData.kFloat, 0.0)
        OUTPUT_ATTR(nAttr)

        FindParamFromLength.addAttribute(FindParamFromLength.inCurve)
        FindParamFromLength.addAttribute(FindParamFromLength.inArcLength)
        FindParamFromLength.addAttribute(FindParamFromLength.outParam)
        FindParamFromLength.attributeAffects(FindParamFromLength.inCurve, FindParamFromLength.outParam)
        FindParamFromLength.attributeAffects(FindParamFromLength.inArcLength, FindParamFromLength.outParam)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug == FindParamFromLength.outParam:
            curveHandle = dataBlock.inputValue(FindParamFromLength.inCurve)
            curveMob = curveHandle.asNurbsCurve()
            arcLen = dataBlock.inputValue(FindParamFromLength.inArcLength).asDouble()

            curveFn = om2.MFnNurbsCurve(curveMob)
            param = curveFn.findParamFromLength(arcLen)

            outParamHandle = dataBlock.outputValue(FindParamFromLength.outParam)
            outParamHandle.setFloat(param)
            outParamHandle.setClean()
