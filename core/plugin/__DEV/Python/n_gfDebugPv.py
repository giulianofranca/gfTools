# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfDebugPv node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.

Requirements:
    Maya 2017 or above.

Todo:
    * NDA

This code supports Pylint. Rc file in project.
"""
# pylint: disable=E0401
# E0401 = Supress Maya modules import error

import math
import colorsys
import maya.api.OpenMaya as om2


def maya_useNewAPI():
    """ Function to Maya recognize the use of the Python API 2.0. """
    # pylint: disable=C0103, w0107
    pass


def INPUT_ATTR(FNATTR):
    """ Configure a input attribute. """
    # pylint: disable=C0103
    FNATTR.writable = True
    FNATTR.readable = True
    FNATTR.storable = True
    FNATTR.keyable = True


def OUTPUT_ATTR(FNATTR):
    """ Configure a output attribute. """
    # pylint: disable=C0103
    FNATTR.writable = False
    FNATTR.readable = True
    FNATTR.storable = False
    FNATTR.keyable = False


class PvDebug(om2.MPxNode):
    """ Main class of gfDebugPv node. """

    kNODE_NAME = ""
    kNODE_CLASSIFY = ""
    kNODE_ID = ""

    inStartPos = om2.MObject()
    inMidPos = om2.MObject()
    inEndPos = om2.MObject()
    outPos = om2.MObject()
    outRot = om2.MObject()
    outRotX = om2.MObject()
    outRotY = om2.MObject()
    outRotZ = om2.MObject()
    result = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return PvDebug()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to IKVChain class. Instances of IKVChain will use these attributes to create plugs
        for use in the compute() method.
        """
        startPosAttr = om2.MFnNumericAttribute()
        PvDebug.inStartPos = startPosAttr.createPoint("startPos", "sp")
        startPosAttr.writable = True
        startPosAttr.storable = True
        startPosAttr.keyable = True

        midPosAttr = om2.MFnNumericAttribute()
        PvDebug.inMidPos = midPosAttr.createPoint("midPos", "mp")
        midPosAttr.writable = True
        midPosAttr.storable = True
        midPosAttr.keyable = True

        endPosAttr = om2.MFnNumericAttribute()
        PvDebug.inEndPos = endPosAttr.createPoint("endPos", "ep")
        endPosAttr.writable = True
        endPosAttr.storable = True
        endPosAttr.keyable = True

        # Create outputs
        outPosAttr = om2.MFnNumericAttribute()
        PvDebug.outPos = outPosAttr.createPoint("outPos", "op")
        outPosAttr.writable = False
        outPosAttr.storable = True

        outRotAttr = om2.MFnUnitAttribute()
        PvDebug.outRotX = outRotAttr.create("outRotX", "orox", om2.MFnUnitAttribute.kAngle, 0.0)
        PvDebug.outRotY = outRotAttr.create("outRotY", "oroy", om2.MFnUnitAttribute.kAngle, 0.0)
        PvDebug.outRotZ = outRotAttr.create("outRotZ", "oroz", om2.MFnUnitAttribute.kAngle, 0.0)
        outRotAttr = om2.MFnNumericAttribute()
        PvDebug.outRot = outRotAttr.create("outRot", "oro", PvDebug.outRotX, PvDebug.outRotY, PvDebug.outRotZ)
        outRotAttr.writable = False
        outRotAttr.storable = True

        resultAttr = om2.MFnNumericAttribute()
        PvDebug.result = resultAttr.createColor("result", "or")
        resultAttr.writable = False
        resultAttr.storable = True
        resultAttr.usedAsColor = True

        # Add attributes
        PvDebug.addAttribute(PvDebug.inStartPos)
        PvDebug.addAttribute(PvDebug.inMidPos)
        PvDebug.addAttribute(PvDebug.inEndPos)
        PvDebug.addAttribute(PvDebug.outPos)
        PvDebug.addAttribute(PvDebug.outRot)
        PvDebug.addAttribute(PvDebug.result)
        PvDebug.attributeAffects(PvDebug.inStartPos, PvDebug.outPos)
        PvDebug.attributeAffects(PvDebug.inMidPos, PvDebug.outPos)
        PvDebug.attributeAffects(PvDebug.inEndPos, PvDebug.outPos)
        PvDebug.attributeAffects(PvDebug.inStartPos, PvDebug.outRot)
        PvDebug.attributeAffects(PvDebug.inMidPos, PvDebug.outRot)
        PvDebug.attributeAffects(PvDebug.inEndPos, PvDebug.outRot)
        PvDebug.attributeAffects(PvDebug.inStartPos, PvDebug.result)
        PvDebug.attributeAffects(PvDebug.inMidPos, PvDebug.result)
        PvDebug.attributeAffects(PvDebug.inEndPos, PvDebug.result)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=R0201
        startPos = dataBlock.inputValue(PvDebug.inStartPos).asFloat3()
        midPos = dataBlock.inputValue(PvDebug.inMidPos).asFloat3()
        endPos = dataBlock.inputValue(PvDebug.inEndPos).asFloat3()

        resTrans, resRot = PvDebug.retrieveLocation(startPos, midPos, endPos)

        if plug == PvDebug.outPos:
            outPosHandle = dataBlock.outputValue(PvDebug.outPos).set3Float(resTrans[0], resTrans[1], resTrans[2])
            outPosHandle.setClean()

        elif plug == PvDebug.outRot:
            outRotHandle = dataBlock.outputValue(PvDebug.outRot)
            outRotXHandle = outRotHandle.child(PvDebug.outRotX)
            outRotYHandle = outRotHandle.child(PvDebug.outRotY)
            outRotZHandle = outRotHandle.child(PvDebug.outRotZ)
            outRotXHandle.setMAngle(om2.MAngle(resRot.x))
            outRotYHandle.setMAngle(om2.MAngle(resRot.y))
            outRotZHandle.setMAngle(om2.MAngle(resRot.z))
            outRotXHandle.setClean()
            outRotYHandle.setClean()
            outRotZHandle.setClean()
            outRotHandle.setClean()

        elif plug == PvDebug.result:
            color = PvDebug.pvLocationRatioColor(startPos, midPos, resTrans)

            outColorHandle = dataBlock.outputValue(PvDebug.result)
            outColorHandle.setMFloatVector(color)
            outColorHandle.setClean()

    @staticmethod
    def retrieveLocation(start, mid, end):
        """ Retrieve exact location of the pv. """
        vStart = om2.MVector(start[0], start[1], start[2])
        vMid = om2.MVector(mid[0], mid[1], mid[2])
        vEnd = om2.MVector(end[0], end[1], end[2])
        vStartEnd = vEnd - vStart
        vStartMid = vMid - vStart
        dotP = vStartMid * vStartEnd
        proj = float(dotP) / float(vStartEnd.length())
        nStartEnd = vStartEnd.normal()
        vProj = nStartEnd * proj
        vArrow = vStartMid - vProj
        vArrow *= 1  # Multiplier
        vFinal = vArrow + vMid
        vCross1 = vStartEnd ^ vStartMid
        vCross1.normalize()
        vCross2 = vCross1 ^ vArrow
        vCross2.normalize()
        vArrow.normalize()
        matrix = [vArrow.x, vArrow.y, vArrow.z, 0.0,
                  vCross1.x, vCross1.y, vCross1.z, 0.0,
                  vCross2.x, vCross2.y, vCross2.z, 0.0,
                  0.0, 0.0, 0.0, 1.0]
        mMatrix = om2.MMatrix(matrix)
        matrixFn = om2.MTransformationMatrix(mMatrix)
        eRot = matrixFn.rotation(asQuaternion=False)
        resTranslate = [vFinal.x, vFinal.y, vFinal.z]
        return resTranslate, eRot

    @staticmethod
    def pvLocationRatioColor(startPos, midPos, pvPos):
        """
        Get the distances of startPos-midPos and midPos-pvPos, calculate a ratio between
        these distance to get a HSV color.
        Ratio math: midPos-pvPos >= (startPos-midPos / 4)
        """
        startToMidPosDist = math.sqrt(math.pow(startPos[0] - midPos[0], 2) +
                                      math.pow(startPos[1] - midPos[1], 2) +
                                      math.pow(startPos[2] - midPos[2], 2))
        midToPvPosDist = math.sqrt(math.pow(midPos[0] - pvPos[0], 2) +
                                   math.pow(midPos[1] - pvPos[1], 2) +
                                   math.pow(midPos[2] - pvPos[2], 2))
        okRatio = startToMidPosDist / 4
        badRatio = 0.0
        okHColor = 180.0
        badHColor = 0.0
        colorH = PvDebug.fit(midToPvPosDist, badRatio, okRatio, badHColor, okHColor)
        colorH = PvDebug.fit(colorH, 0.0, 360.0, 0.0, 1.0)
        colorS = 1.0
        colorV = 1.0
        rgb = colorsys.hsv_to_rgb(colorH, colorS, colorV)
        color = om2.MFloatVector(rgb[0], rgb[1], rgb[2])
        return color

    @staticmethod
    def fit(value, oldMin, oldMax, newMin, newMax):
        """
        Fit function: (((value-oldMin)*(newMax-newMin))/(oldMax-oldMin))+newMin
        """
        oldRange = oldMax - oldMin
        newRange = newMax - newMin
        newValue = (((value - oldMin) * newRange) / oldRange) + newMin
        if value >= oldMax:
            newValue = newMax
        elif value <= oldMin:
            newValue = newMin
        return newValue
