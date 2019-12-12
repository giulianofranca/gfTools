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
    * Fix lock length
    * Fix aim orientation

Sources:
    * NDA

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


class QuadraticCurve(om2.MPxNode):
    """ Main class of gfQuadraticCurve node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inControlPoints = om2.MObject()
    inEnableTwist = om2.MObject()
    inStartUpObj = om2.MObject()
    inEndUpObj = om2.MObject()
    inLockLength = om2.MObject()
    inRestLength = om2.MObject()
    inPreferredAngle = om2.MObject()
    outTransforms = om2.MObject()
    outCurve = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return QuadraticCurve()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to QuadraticCurve class. Instances of QuadraticCurve will use these attributes to create plugs
        for use in the compute() method.
        """
        mAttr = om2.MFnMatrixAttribute()
        nAttr = om2.MFnNumericAttribute()
        uAttr = om2.MFnUnitAttribute()
        tAttr = om2.MFnTypedAttribute()

        QuadraticCurve.inControlPoints = mAttr.create("controlPoints", "cp", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        INPUT_ATTR(mAttr)

        QuadraticCurve.inEnableTwist = nAttr.create("enableTwist", "etw", om2.MFnNumericData.kBoolean, False)
        INPUT_ATTR(nAttr)

        QuadraticCurve.inStartUpObj = mAttr.create("startUpObjectMatrix", "suom", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        QuadraticCurve.inEndUpObj = mAttr.create("endUpObjectMatrix", "euom", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        QuadraticCurve.inLockLength = nAttr.create("lockLength", "locklen", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        QuadraticCurve.inRestLength = nAttr.create("restLength", "rlength", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        INPUT_ATTR(nAttr)

        QuadraticCurve.inPreferredAngle = uAttr.create("preferredAngle", "pangle", om2.MFnUnitAttribute.kAngle)
        uAttr.setMin(0.0)
        uAttr.setMax(om2.MAngle(360.0, om2.MAngle.kDegrees).asRadians())
        INPUT_ATTR(uAttr)

        QuadraticCurve.outTransforms = mAttr.create("outTransforms", "otrans", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        OUTPUT_ATTR(mAttr)

        QuadraticCurve.outCurve = tAttr.create("outCurve", "ocrv", om2.MFnData.kNurbsCurve)
        OUTPUT_ATTR(tAttr)

        QuadraticCurve.addAttribute(QuadraticCurve.inControlPoints)
        QuadraticCurve.addAttribute(QuadraticCurve.inEnableTwist)
        QuadraticCurve.addAttribute(QuadraticCurve.inStartUpObj)
        QuadraticCurve.addAttribute(QuadraticCurve.inEndUpObj)
        QuadraticCurve.addAttribute(QuadraticCurve.inLockLength)
        QuadraticCurve.addAttribute(QuadraticCurve.inRestLength)
        QuadraticCurve.addAttribute(QuadraticCurve.inPreferredAngle)
        QuadraticCurve.addAttribute(QuadraticCurve.outTransforms)
        QuadraticCurve.addAttribute(QuadraticCurve.outCurve)
        QuadraticCurve.attributeAffects(QuadraticCurve.inControlPoints, QuadraticCurve.outCurve)
        QuadraticCurve.attributeAffects(QuadraticCurve.inControlPoints, QuadraticCurve.outTransforms)
        QuadraticCurve.attributeAffects(QuadraticCurve.inEnableTwist, QuadraticCurve.outTransforms)
        QuadraticCurve.attributeAffects(QuadraticCurve.inStartUpObj, QuadraticCurve.outTransforms)
        QuadraticCurve.attributeAffects(QuadraticCurve.inEndUpObj, QuadraticCurve.outTransforms)
        QuadraticCurve.attributeAffects(QuadraticCurve.inLockLength, QuadraticCurve.outTransforms)
        QuadraticCurve.attributeAffects(QuadraticCurve.inRestLength, QuadraticCurve.outTransforms)
        QuadraticCurve.attributeAffects(QuadraticCurve.inPreferredAngle, QuadraticCurve.outTransforms)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        ctrlPntsHandle = dataBlock.inputArrayValue(QuadraticCurve.inControlPoints)
        ctrlPnts = om2.MPointArray()

        for i in range(3):
            ctrlPntsHandle.jumpToLogicalElement(i)
            mCtrlPnt = ctrlPntsHandle.inputValue().asMatrix()
            ctrlPnt = om2.MPoint(mCtrlPnt[12], mCtrlPnt[13], mCtrlPnt[14])
            ctrlPnts.append(ctrlPnt)

        # spans = numCVs - degree. (3 - 2 = 1)
        # knots = spans + 2 * degree - 1. (1 + 4 - 1 = 4)
        # degree = N
        # numSpans = M
        crvKnots = om2.MDoubleArray([0, 0, 1, 1])
        crvDegree = 2
        crvForm = om2.MFnNurbsCurve.kOpen
        crvIs2d = False
        crvRational = False
        crvData = om2.MFnNurbsCurveData().create()
        crvFn = om2.MFnNurbsCurve(crvData)

        crvFn.create(ctrlPnts, crvKnots, crvDegree, crvForm, crvIs2d, crvRational, crvData)
        crvFn.updateCurve()

        if plug == QuadraticCurve.outCurve:
            outCurveHandle = dataBlock.outputValue(QuadraticCurve.outCurve)
            outCurveHandle.setMObject(crvData)
            outCurveHandle.setClean()

        elif plug == QuadraticCurve.outTransforms:
            outTransHandle = dataBlock.outputArrayValue(QuadraticCurve.outTransforms)
            lockLength = dataBlock.inputValue(QuadraticCurve.inLockLength).asFloat()
            restLength = dataBlock.inputValue(QuadraticCurve.inRestLength).asFloat()
            crvLength = crvFn.length()
            numOutputs = len(outTransHandle)
            stepFull = 1.0 / (numOutputs - 1) if numOutputs > 1 else 0.0
            stepLock = (min(restLength, crvLength) / crvLength) / (numOutputs - 1) if numOutputs > 1 else 0.0
            step = (1.0 - lockLength) * stepFull + lockLength * stepLock
            for i in range(numOutputs):
                parameter = step * i
                pos = crvFn.getPointAtParam(parameter, om2.MSpace.kObject)
                vPos = om2.MVector(pos.x, pos.y, pos.z)
                mtx = [
                    1.0, 0.0, 0.0, 0.0,
                    0.0, 1.0, 0.0, 0.0,
                    0.0, 0.0, 1.0, 0.0,
                    vPos.x, vPos.y, vPos.z, 1.0
                ]
                mOut = om2.MMatrix(mtx)
                outTransHandle.jumpToLogicalElement(i)
                resultHandle = outTransHandle.outputValue()
                resultHandle.setMMatrix(mOut)
            outTransHandle.setAllClean()
            # prefAngle = dataBlock.inputValue(QuadraticCurve.inPreferredAngle).asAngle().asRadians()
            # enableTwist = dataBlock.inputValue(QuadraticCurve.inEnableTwist).asBool()
            # mStartUp = dataBlock.inputValue(QuadraticCurve.inStartUpObj).asMatrix()
            # outTransHandle = dataBlock.outputArrayValue(QuadraticCurve.outTransforms)
            # numOutputs = len(outTransHandle)
            # step = 1.0 / (numOutputs - 1) if numOutputs > 1 else 0.0
            # startUp = om2.MPoint(mStartUp[12], mStartUp[13], mStartUp[14])
            # for i in range(numOutputs):
            #     parameter = step * i
            #     pos = crvFn.getPointAtParam(parameter, om2.MSpace.kObject)
            #     if i == numOutputs - 1:
            #         nextPos = crvFn.getPointAtParam(step * (i - 1), om2.MSpace.kObject)
            #         nAim = -(nextPos - pos)
            #     else:
            #         nextPos = crvFn.getPointAtParam(step * (i + 1), om2.MSpace.kObject)
            #         nAim = nextPos - pos
            #     nAim.normalize()
            #     nNormal = startUp - pos
            #     nNormal.normalize()
            #     nBinormal = nAim ^ nNormal
            #     nBinormal.normalize()
            #     # up = (pos + om2.MVector(math.cos(prefAngle), 0.0, math.sin(prefAngle))) - pos
            #     # nNormal = up - ((up * nAim) * nAim)
            #     # nNormal.normalize()
            #     # nBinormal = nAim ^ nNormal
            #     mtx = [
            #         nAim.x, nAim.y, nAim.z, 0.0,
            #         nNormal.x, nNormal.y, nNormal.z, 0.0,
            #         nBinormal.x, nBinormal.y, nBinormal.z, 0.0,
            #         pos.x, pos.y, pos.z, 1.0
            #     ]
            #     mOut = om2.MMatrix(mtx)
            #     outTransHandle.jumpToLogicalElement(i)
            #     resultHandle = outTransHandle.outputValue()
            #     resultHandle.setMMatrix(mOut)
            # outTransHandle.setAllClean()
