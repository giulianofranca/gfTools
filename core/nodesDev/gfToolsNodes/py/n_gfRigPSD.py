# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfRigIKVChain node. You should be using the related C++ version.]
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


class SphericalPSD(om2.MPxNode):
    """ Main class of gfRigPSD node. """

    kNODE_NAME = ""
    kNODE_CLASSIFY = ""
    kNODE_ID = ""

    inBase = om2.MObject()
    inPose = om2.MObject()
    inTarget = om2.MObject()
    inTargetEnvelope = om2.MObject()
    inTargetFalloff = om2.MObject()
    outWeight = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return SphericalPSD()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to IKVChain class. Instances of IKVChain will use these attributes to create plugs
        for use in the compute() method.
        """
        nAttr = om2.MFnNumericAttribute()
        mAttr = om2.MFnMatrixAttribute()

        SphericalPSD.inBase = mAttr.create("base", "b", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        SphericalPSD.inPose = mAttr.create("pose", "p", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        SphericalPSD.inTarget = mAttr.create("target", "t", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        INPUT_ATTR(mAttr)

        SphericalPSD.inTargetEnvelope = nAttr.create("targetEnvelope", "te", om2.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        nAttr.array = True
        INPUT_ATTR(nAttr)

        SphericalPSD.inTargetFalloff = nAttr.create("targetFalloff", "tf", om2.MFnNumericData.kFloat, 45.0)
        nAttr.setMin(0.0)
        nAttr.setSoftMax(135.0)
        nAttr.setMax(180.0)
        nAttr.array = True
        INPUT_ATTR(nAttr)

        SphericalPSD.outWeight = nAttr.create("outWeight", "ow", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        nAttr.array = True
        OUTPUT_ATTR(nAttr)

        SphericalPSD.addAttribute(SphericalPSD.inBase)
        SphericalPSD.addAttribute(SphericalPSD.inPose)
        SphericalPSD.addAttribute(SphericalPSD.inTarget)
        SphericalPSD.addAttribute(SphericalPSD.inTargetEnvelope)
        SphericalPSD.addAttribute(SphericalPSD.inTargetFalloff)
        SphericalPSD.addAttribute(SphericalPSD.outWeight)

        SphericalPSD.attributeAffects(SphericalPSD.inBase, SphericalPSD.outWeight)
        SphericalPSD.attributeAffects(SphericalPSD.inPose, SphericalPSD.outWeight)
        SphericalPSD.attributeAffects(SphericalPSD.inTarget, SphericalPSD.outWeight)
        SphericalPSD.attributeAffects(SphericalPSD.inTargetEnvelope, SphericalPSD.outWeight)
        SphericalPSD.attributeAffects(SphericalPSD.inTargetFalloff, SphericalPSD.outWeight)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=R0201
        if plug == SphericalPSD.outWeight:
            baseMtx = dataBlock.inputValue(SphericalPSD.inBase).asMatrix()
            poseMtx = dataBlock.inputValue(SphericalPSD.inPose).asMatrix()
            targetHandle = dataBlock.inputArrayValue(SphericalPSD.inTarget)
            envelopeHandle = dataBlock.inputArrayValue(SphericalPSD.inTargetEnvelope)
            falloffHandle = dataBlock.inputArrayValue(SphericalPSD.inTargetFalloff)
            weightsHandle = dataBlock.outputArrayValue(SphericalPSD.outWeight)

            mtxFn = om2.MTransformationMatrix(baseMtx)
            vBase = mtxFn.translation(om2.MSpace.kWorld)
            mtxFn = om2.MTransformationMatrix(poseMtx)
            vPose = mtxFn.translation(om2.MSpace.kWorld)

            vCurPose = vPose - vBase
            nCurPose = vCurPose.normal()

            targetPoseList = []
            envelopeList = []
            falloffList = []

            index = len(targetHandle)
            for i in range(index):
                targetHandle.jumpToLogicalElement(i)
                mtx = targetHandle.inputValue().asMatrix()
                mtxFn = om2.MTransformationMatrix(mtx)
                vector = mtxFn.translation(om2.MSpace.kWorld)
                vTargetPose = vector - vBase
                nTargetPose = vTargetPose.normal()
                targetPoseList.append(nTargetPose)

            index = len(envelopeHandle)
            for i in range(index):
                envelopeHandle.jumpToLogicalElement(i)
                env = envelopeHandle.inputValue().asFloat()
                envelopeList.append(env)

            index = len(falloffHandle)
            for i in range(index):
                falloffHandle.jumpToLogicalElement(i)
                falloff = math.radians(falloffHandle.inputValue().asFloat())
                falloffList.append(falloff)

            for i in range(len(weightsHandle)):
                weightsHandle.jumpToLogicalElement(i)
                resultHandle = weightsHandle.outputValue()
                if (i < len(weightsHandle) and
                        i < len(targetPoseList) and
                        i < len(falloffList) and
                        i < len(envelopeList)):
                    alpha = math.acos(targetPoseList[i] * nCurPose)
                    ratio = min(max(alpha/falloffList[i], -1.0), 1.0)
                    if ratio == 0.0:
                        resultWeight = envelopeList[i] * 1.0
                    elif ratio > 0.0:
                        resultWeight = envelopeList[i] * (1.0 - ratio)
                    elif ratio < 0.0:
                        resultWeight = envelopeList[i] * (1.0 + ratio)

                    resultHandle.setFloat(resultWeight)
                else:
                    resultHandle.setFloat(0.0)

            weightsHandle.setAllClean()
