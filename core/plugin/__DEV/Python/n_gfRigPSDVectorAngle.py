# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfRigPSDVectorAngle node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.
    https://www.desmos.com/calculator/nfggjvzpkn

Requirements:
    Maya 2017 or above.

Todo:
    * NDA

This code supports Pylint. Rc file in project.
"""
# pylint: disable=E0401
# E0401 = Supress Maya modules import error

import math
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


class VectorAnglePSD(om2.MPxNode):
    """ Main class of gfRigPSDVectorAngle node. """

    kNODE_NAME = ""
    kNODE_CLASSIFY = ""
    kNODE_ID = ""

    inBase = om2.MObject()
    inSource = om2.MObject()
    inTarget = om2.MObject()
    inTargetEnvelope = om2.MObject()
    inTargetFalloff = om2.MObject()
    inRampWeights = om2.MObject()
    outWeights = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    def postConstructor(self):
        """ Post Constructor. """
        thisMob = self.thisMObject()
        attr = VectorAnglePSD.inRampWeights
        ramp = om2.MRampAttribute(thisMob, attr)
        pos = om2.MFloatArray()
        val = om2.MFloatArray()
        interp = om2.MIntArray()
        pos.append(1.0)
        val.append(1.0)
        interp.append(om2.MRampAttribute.kLinear)
        ramp.addEntries(pos, val, interp)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return VectorAnglePSD()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to IKVChain class. Instances of IKVChain will use these attributes to create plugs
        for use in the compute() method.
        """
        mAttr = om2.MFnMatrixAttribute()
        nAttr = om2.MFnNumericAttribute()
        rAttr = om2.MRampAttribute()

        VectorAnglePSD.inBase = mAttr.create("base", "base", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        VectorAnglePSD.inSource = mAttr.create("source", "source", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        VectorAnglePSD.inTarget = mAttr.create("target", "target", om2.MFnMatrixAttribute.kFloat)
        mAttr.array = True
        INPUT_ATTR(mAttr)

        VectorAnglePSD.inTargetEnvelope = nAttr.create("targetEnvelope", "te", om2.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        nAttr.array = True
        INPUT_ATTR(nAttr)

        VectorAnglePSD.inTargetFalloff = nAttr.create("targetFalloff", "tf", om2.MFnNumericData.kFloat, 90.0)
        nAttr.setMin(0.0)
        nAttr.setMax(180.0)
        nAttr.array = True
        INPUT_ATTR(nAttr)

        VectorAnglePSD.inRampWeights = rAttr.createCurveRamp("rampWeights", "rw")

        VectorAnglePSD.outWeights = nAttr.create("outWeights", "ow", om2.MFnNumericData.kFloat, 0.0)
        nAttr.array = True
        OUTPUT_ATTR(nAttr)

        VectorAnglePSD.addAttribute(VectorAnglePSD.inBase)
        VectorAnglePSD.addAttribute(VectorAnglePSD.inSource)
        VectorAnglePSD.addAttribute(VectorAnglePSD.inTarget)
        VectorAnglePSD.addAttribute(VectorAnglePSD.inTargetEnvelope)
        VectorAnglePSD.addAttribute(VectorAnglePSD.inTargetFalloff)
        VectorAnglePSD.addAttribute(VectorAnglePSD.inRampWeights)
        VectorAnglePSD.addAttribute(VectorAnglePSD.outWeights)
        VectorAnglePSD.attributeAffects(VectorAnglePSD.inBase, VectorAnglePSD.outWeights)
        VectorAnglePSD.attributeAffects(VectorAnglePSD.inSource, VectorAnglePSD.outWeights)
        VectorAnglePSD.attributeAffects(VectorAnglePSD.inTarget, VectorAnglePSD.outWeights)
        VectorAnglePSD.attributeAffects(VectorAnglePSD.inTargetEnvelope, VectorAnglePSD.outWeights)
        VectorAnglePSD.attributeAffects(VectorAnglePSD.inTargetFalloff, VectorAnglePSD.outWeights)
        VectorAnglePSD.attributeAffects(VectorAnglePSD.inRampWeights, VectorAnglePSD.outWeights)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=R0201
        if plug != VectorAnglePSD.outWeights:
            return om2.kUnknownParameter

        mBase = dataBlock.inputValue(VectorAnglePSD.inBase).asFloatMatrix()
        mSource = dataBlock.inputValue(VectorAnglePSD.inSource).asFloatMatrix()

        targetHandle = dataBlock.inputArrayValue(VectorAnglePSD.inTarget)
        targetEnvelopeHandle = dataBlock.inputArrayValue(VectorAnglePSD.inTargetEnvelope)
        targetFalloffHandle = dataBlock.inputArrayValue(VectorAnglePSD.inTargetFalloff)
        outWeightsHandle = dataBlock.outputArrayValue(VectorAnglePSD.outWeights)

        vBase = om2.MFloatVector(mBase[12], mBase[13], mBase[14])
        vSource = om2.MFloatVector(mSource[12], mSource[13], mSource[14])

        vCurPose = vSource - vBase
        nCurPose = vCurPose.normal()

        targetList = []
        envelopeList = []
        falloffList = []

        for i in range(len(targetHandle)):
            targetHandle.jumpToLogicalElement(i)
            mtx = targetHandle.inputValue().asFloatMatrix()
            vec = om2.MFloatVector(mtx[12], mtx[13], mtx[14])
            vTargetPose = vec - vBase
            nTargetPose = vTargetPose.normal()
            targetList.append(nTargetPose)

        for i in range(len(targetEnvelopeHandle)):
            targetEnvelopeHandle.jumpToLogicalElement(i)
            env = targetEnvelopeHandle.inputValue().asFloat()
            envelopeList.append(env)

        for i in range(len(targetFalloffHandle)):
            targetFalloffHandle.jumpToLogicalElement(i)
            fall = targetFalloffHandle.inputValue().asFloat()
            falloffList.append(fall)

        for i in range(len(outWeightsHandle)):
            outWeightsHandle.jumpToLogicalElement(i)
            resultHandle = outWeightsHandle.outputValue()
            if (i < len(outWeightsHandle) and
                    i < len(targetHandle) and
                    i < len(targetEnvelopeHandle) and
                    i < len(targetFalloffHandle)):
                theta = math.acos(targetList[i] * nCurPose)
                ratio = min(max(theta/math.radians(falloffList[i]), -1.0), 1.0)
                if ratio == 0.0:
                    weight = envelopeList[i] * 1.0
                elif ratio > 0.0:
                    weight = envelopeList[i] * (1.0 - ratio)
                elif ratio < 0.0:
                    weight = envelopeList[i] * (1.0 + ratio)

                thisMob = self.thisMObject()
                rampAttr = om2.MRampAttribute(thisMob, VectorAnglePSD.inRampWeights)
                resultWeight = rampAttr.getValueAtPosition(weight)
                resultHandle.setFloat(resultWeight)
            else:
                resultHandle.setFloat(0.0)
