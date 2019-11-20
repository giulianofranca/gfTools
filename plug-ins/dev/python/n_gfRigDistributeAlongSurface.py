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


class DistributeAlongSurface(om2.MPxNode):
    """ Main class of gfDistributeAlongSurface node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inSurface = om2.MObject()
    inDistributeAlong = om2.MObject()
    inDisplace = om2.MObject()
    inAlwaysUniform = om2.MObject()
    outTransform = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return DistributeAlongSurface()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to DistributeAlongSurface class. Instances of DistributeAlongSurface will use these attributes to create plugs
        for use in the compute() method.
        """
        tAttr = om2.MFnTypedAttribute()
        eAttr = om2.MFnEnumAttribute()
        nAttr = om2.MFnNumericAttribute()
        mAttr = om2.MFnMatrixAttribute()

        DistributeAlongSurface.inSurface = tAttr.create("inputSurface", "isurf", om2.MFnData.kNurbsSurface)
        INPUT_ATTR(tAttr)

        DistributeAlongSurface.inDistributeAlong = eAttr.create("distributeAlong", "da", 0)
        eAttr.addField("U", 0)
        eAttr.addField("V", 1)
        INPUT_ATTR(eAttr)

        DistributeAlongSurface.inDisplace = nAttr.create("displaceTangent", "dtan", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        DistributeAlongSurface.inAlwaysUniform = nAttr.create("alwaysUniform", "auni", om2.MFnNumericData.kBoolean, False)
        INPUT_ATTR(nAttr)

        DistributeAlongSurface.outTransform = mAttr.create("outputTransform", "ot", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        OUTPUT_ATTR(mAttr)

        DistributeAlongSurface.addAttribute(DistributeAlongSurface.inSurface)
        DistributeAlongSurface.addAttribute(DistributeAlongSurface.inDistributeAlong)
        DistributeAlongSurface.addAttribute(DistributeAlongSurface.inDisplace)
        DistributeAlongSurface.addAttribute(DistributeAlongSurface.inAlwaysUniform)
        DistributeAlongSurface.addAttribute(DistributeAlongSurface.outTransform)
        DistributeAlongSurface.attributeAffects(DistributeAlongSurface.inSurface, DistributeAlongSurface.outTransform)
        DistributeAlongSurface.attributeAffects(DistributeAlongSurface.inDistributeAlong, DistributeAlongSurface.outTransform)
        DistributeAlongSurface.attributeAffects(DistributeAlongSurface.inDisplace, DistributeAlongSurface.outTransform)
        DistributeAlongSurface.attributeAffects(DistributeAlongSurface.inAlwaysUniform, DistributeAlongSurface.outTransform)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != DistributeAlongSurface.outTransform:
            return om2.kUnknownParameter

        surfaceHandle = dataBlock.inputValue(DistributeAlongSurface.inSurface)
        surface = surfaceHandle.asNurbsSurface()
        distAlong = dataBlock.inputValue(DistributeAlongSurface.inDistributeAlong).asShort()
        displace = dataBlock.inputValue(DistributeAlongSurface.inDisplace).asFloat()
        alwaysUniform = dataBlock.inputValue(DistributeAlongSurface.inAlwaysUniform).asBool()
        outTransHandle = dataBlock.outputArrayValue(DistributeAlongSurface.outTransform)

        numOutputs = len(outTransHandle)
        surfaceFn = om2.MFnNurbsSurface(surface)
        step = 1.0 / (numOutputs - 1) if numOutputs > 1 else 0.0
        curveData = om2.MFnNurbsCurveData().create()
        curveFn = om2.MFnNurbsCurve(curveData)

        if alwaysUniform:
            numCVs = surfaceFn.numCVsInU if distAlong == 0 else surfaceFn.numCVsInV
            curvePnts = om2.MPointArray()
            curveKnots = surfaceFn.knotsInU() if distAlong == 0 else surfaceFn.knotsInV()
            curveDegree = surfaceFn.degreeInU if distAlong == 0 else surfaceFn.degreeInV
            curveForm = surfaceFn.formInU if distAlong == 0 else surfaceFn.formInV
            curveIs2d = False
            curveRational = False
            for i in range(numCVs):
                if distAlong == 0:
                    curvePnts.append(surfaceFn.cvPosition(i, int(displace)))
                else:
                    curvePnts.append(surfaceFn.cvPosition(int(displace), i))
            curveFn.create(curvePnts, curveKnots, curveDegree, curveForm, curveIs2d, curveRational, curveData)
            curveLength = curveFn.length()

        for i in range(numOutputs):
            if alwaysUniform:
                parU = curveFn.findParamFromLength(curveLength * step * i) if distAlong == 0 else displace
                parV = displace if distAlong == 0 else curveFn.findParamFromLength(curveLength * step * i)
            else:
                parU = step * i if distAlong == 0 else displace
                parV = displace if distAlong == 0 else step * i
            pos = surfaceFn.getPointAtParam(parU, parV, om2.MSpace.kWorld)
            tangents = surfaceFn.tangents(parU, parV, om2.MSpace.kWorld)
            aim = tangents[0].normalize() if distAlong == 0 else tangents[1].normalize()
            normal = surfaceFn.normal(parU, parV, om2.MSpace.kWorld).normalize()
            binormal = tangents[1].normalize() if distAlong == 0 else tangents[0].normalize()
            mtx = [
                aim.x, aim.y, aim.z, 0.0,
                normal.x, normal.y, normal.z, 0.0,
                binormal.x, binormal.y, binormal.z, 0.0,
                pos.x, pos.y, pos.z, 1.0
            ]
            mOut = om2.MMatrix(mtx)
            outTransHandle.jumpToLogicalElement(i)
            resultHandle = outTransHandle.outputValue()
            resultHandle.setMMatrix(mOut)

        surfaceHandle.setClean()
        outTransHandle.setAllClean()
