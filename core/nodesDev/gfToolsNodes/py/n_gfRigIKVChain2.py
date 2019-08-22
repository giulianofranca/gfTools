# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfRigIKVChain node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.
    https://www.desmos.com/calculator/wthlznq4aj

Requirements:
    Maya 2017 or above.

Todo:
    * Create and develop the stretchMult attrs.
    * Create and develop the squashMult attrs.
    * Create and develop the slidePv attr.

This code supports Pylint. Rc file in project.
"""
# pylint: disable=E0401
# E0401 = Supress Maya modules import error

import math
import maya.api.OpenMaya as om2


def maya_useNewAPI():
    """ Function to Maya recognize the use of the Python API 2.0. """
    # pylint: disable=C0103, W0107
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


class IKVChain(om2.MPxNode):
    """ Main class of gfRigIKVChain node. """

    kNODE_NAME = ""
    kNODE_CLASSIFY = ""
    kNODE_ID = ""

    inRoot = om2.MObject()
    inHandle = om2.MObject()
    inUpVector = om2.MObject()
    inPreferredAngle = om2.MObject()
    inPvMode = om2.MObject()
    inTwist = om2.MObject()
    inHierarchyMode = om2.MObject()
    inRestLength1 = om2.MObject()
    inRestLength2 = om2.MObject()
    inCompressionLimit = om2.MObject()
    inSoft = om2.MObject()
    inStretch = om2.MObject()
    inClampStretch = om2.MObject()
    inClampValue = om2.MObject()
    inSquash = om2.MObject()
    outChain = om2.MObject()
    debugAngle = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return IKVChain()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to IKVChain class. Instances of IKVChain will use these attributes to create plugs
        for use in the compute() method.
        """
        mAttr = om2.MFnMatrixAttribute()
        nAttr = om2.MFnNumericAttribute()
        uAttr = om2.MFnUnitAttribute()
        eAttr = om2.MFnEnumAttribute()

        IKVChain.inRoot = mAttr.create("root", "root", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        IKVChain.inHandle = mAttr.create("handle", "handle", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        IKVChain.inUpVector = mAttr.create("upVector", "up", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        IKVChain.inPreferredAngle = uAttr.create("preferredAngle", "pa", om2.MFnUnitAttribute.kAngle, 0.0)
        uAttr.setMin(0.0)
        uAttr.setMax(2.0 * math.pi)
        INPUT_ATTR(uAttr)

        IKVChain.inPvMode = eAttr.create("pvMode", "pvm", 0)
        eAttr.addField("Manual", 0)
        eAttr.addField("Auto", 1)
        INPUT_ATTR(eAttr)

        IKVChain.inTwist = uAttr.create("twist", "tw", om2.MFnUnitAttribute.kAngle, 0.0)
        INPUT_ATTR(uAttr)

        IKVChain.inHierarchyMode = nAttr.create("hierarchyMode", "hm", om2.MFnNumericData.kBoolean, True)
        INPUT_ATTR(nAttr)

        IKVChain.inRestLength1 = nAttr.create("restLength1", "rl1", om2.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0.001)
        INPUT_ATTR(nAttr)

        IKVChain.inRestLength2 = nAttr.create("restLength2", "rl2", om2.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0.001)
        INPUT_ATTR(nAttr)

        IKVChain.inCompressionLimit = nAttr.create("compressionLimit", "cl", om2.MFnNumericData.kFloat, 0.1)
        nAttr.setMin(0.001)
        nAttr.setMax(0.4)
        INPUT_ATTR(nAttr)

        IKVChain.inSoft = nAttr.create("soft", "soft", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setSoftMax(0.4)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        IKVChain.inStretch = nAttr.create("stretch", "st", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        IKVChain.inClampStretch = nAttr.create("clampStretch", "cst", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        IKVChain.inClampValue = nAttr.create("clampValue", "cstv", om2.MFnNumericData.kFloat, 1.5)
        nAttr.setMin(1.0)
        nAttr.setSoftMax(1.8)
        INPUT_ATTR(nAttr)

        IKVChain.inSquash = nAttr.create("squash", "sq", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        IKVChain.outChain = mAttr.create("outChain", "oc", om2.MFnMatrixAttribute.kFloat)
        mAttr.array = True
        OUTPUT_ATTR(mAttr)

        IKVChain.debugAngle = uAttr.create("debugAngle", "debugAngle", om2.MFnUnitAttribute.kAngle, 0.0)
        OUTPUT_ATTR(uAttr)

        IKVChain.addAttribute(IKVChain.inRoot)
        IKVChain.addAttribute(IKVChain.inHandle)
        IKVChain.addAttribute(IKVChain.inUpVector)
        IKVChain.addAttribute(IKVChain.inPreferredAngle)
        IKVChain.addAttribute(IKVChain.inPvMode)
        IKVChain.addAttribute(IKVChain.inTwist)
        IKVChain.addAttribute(IKVChain.inHierarchyMode)
        IKVChain.addAttribute(IKVChain.inRestLength1)
        IKVChain.addAttribute(IKVChain.inRestLength2)
        IKVChain.addAttribute(IKVChain.inCompressionLimit)
        IKVChain.addAttribute(IKVChain.inSoft)
        IKVChain.addAttribute(IKVChain.inStretch)
        IKVChain.addAttribute(IKVChain.inClampStretch)
        IKVChain.addAttribute(IKVChain.inClampValue)
        IKVChain.addAttribute(IKVChain.inSquash)
        IKVChain.addAttribute(IKVChain.outChain)
        IKVChain.addAttribute(IKVChain.debugAngle)

        IKVChain.attributeAffects(IKVChain.inRoot, IKVChain.outChain)
        IKVChain.attributeAffects(IKVChain.inHandle, IKVChain.outChain)
        IKVChain.attributeAffects(IKVChain.inUpVector, IKVChain.outChain)
        IKVChain.attributeAffects(IKVChain.inPreferredAngle, IKVChain.outChain)
        IKVChain.attributeAffects(IKVChain.inPvMode, IKVChain.outChain)
        IKVChain.attributeAffects(IKVChain.inTwist, IKVChain.outChain)
        IKVChain.attributeAffects(IKVChain.inHierarchyMode, IKVChain.outChain)
        IKVChain.attributeAffects(IKVChain.inRestLength1, IKVChain.outChain)
        IKVChain.attributeAffects(IKVChain.inRestLength2, IKVChain.outChain)
        IKVChain.attributeAffects(IKVChain.inCompressionLimit, IKVChain.outChain)
        IKVChain.attributeAffects(IKVChain.inSoft, IKVChain.outChain)
        IKVChain.attributeAffects(IKVChain.inStretch, IKVChain.outChain)
        IKVChain.attributeAffects(IKVChain.inClampStretch, IKVChain.outChain)
        IKVChain.attributeAffects(IKVChain.inClampValue, IKVChain.outChain)
        IKVChain.attributeAffects(IKVChain.inSquash, IKVChain.outChain)

        IKVChain.attributeAffects(IKVChain.inRoot, IKVChain.debugAngle)
        IKVChain.attributeAffects(IKVChain.inHandle, IKVChain.debugAngle)
        IKVChain.attributeAffects(IKVChain.inUpVector, IKVChain.debugAngle)
        IKVChain.attributeAffects(IKVChain.inPreferredAngle, IKVChain.debugAngle)
        IKVChain.attributeAffects(IKVChain.inPvMode, IKVChain.debugAngle)
        IKVChain.attributeAffects(IKVChain.inTwist, IKVChain.debugAngle)
        IKVChain.attributeAffects(IKVChain.inHierarchyMode, IKVChain.debugAngle)
        IKVChain.attributeAffects(IKVChain.inRestLength1, IKVChain.debugAngle)
        IKVChain.attributeAffects(IKVChain.inRestLength2, IKVChain.debugAngle)
        IKVChain.attributeAffects(IKVChain.inCompressionLimit, IKVChain.debugAngle)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=R0201

        # Get basis matrix
        pvMode = dataBlock.inputValue(IKVChain.inPvMode).asShort()
        mRoot = dataBlock.inputValue(IKVChain.inRoot).asFloatMatrix()
        mHandle = dataBlock.inputValue(IKVChain.inHandle).asFloatMatrix()
        mUpVector = dataBlock.inputValue(IKVChain.inUpVector).asFloatMatrix()
        prefAngle = dataBlock.inputValue(IKVChain.inPreferredAngle).asAngle().asRadians()
        twist = dataBlock.inputValue(IKVChain.inTwist).asAngle().asRadians()

        vRoot = om2.MFloatVector(mRoot[12], mRoot[13], mRoot[14])
        vHandle = om2.MFloatVector(mHandle[12], mHandle[13], mHandle[14])
        vUpVector = om2.MFloatVector(mUpVector[12], mUpVector[13], mUpVector[14])

        vXDirection = vHandle - vRoot
        xDist = vXDirection.length()
        nXAxis = vXDirection.normal()
        if pvMode == 0:
            vUpDirection = vUpVector - vRoot
            vYDirection = vUpDirection - ((vUpDirection * nXAxis) * nXAxis)
            nYAxis = vYDirection.normal()
        else:
            nYAxis = om2.MFloatVector(math.cos(prefAngle), 0.0, math.sin(prefAngle))
        nZAxis = nXAxis ^ nYAxis

        basis = [nXAxis.x, nXAxis.y, nXAxis.z, 0.0,
                 nYAxis.x, nYAxis.y, nYAxis.z, 0.0,
                 nZAxis.x, nZAxis.y, nZAxis.z, 0.0,
                 vRoot.x, vRoot.y, vRoot.z, 1.0]

        mBasisLocal = om2.MFloatMatrix(basis)
        mTwist = om2.MFloatMatrix()
        mTwist[5] = math.cos(twist)
        mTwist[6] = math.sin(twist)
        mTwist[9] = -math.sin(twist)
        mTwist[10] = math.cos(twist)

        if pvMode == 0:
            mBasis = mBasisLocal
        else:
            mBasis = mTwist * mBasisLocal

        # Solve Triangle
        l1 = dataBlock.inputValue(IKVChain.inRestLength1).asFloat()  # UpperArm
        l2 = dataBlock.inputValue(IKVChain.inRestLength2).asFloat()  # Forearm
        compressionLimit = dataBlock.inputValue(IKVChain.inCompressionLimit).asFloat()  # Rigid
        softValue = dataBlock.inputValue(IKVChain.inSoft).asFloat()

        l1m = l1 # * stretchMult1
        l2m = l2 # * stretchMult2

        chainLength = l1m + l2m

        l3rigid = max(min(xDist, chainLength), chainLength * compressionLimit)
        dc = chainLength
        da = (1.0 - softValue) * dc
        if xDist > da and softValue > 0:
            ds = dc - da
            l3soft = ds * (1.0 - math.pow(math.e, (da - xDist) / ds)) + da
            l3 = l3soft
        else:
            l3 = l3rigid

        # Angle Mesurement
        outDebugAngle = dataBlock.outputValue(IKVChain.debugAngle)
        hierarchyMode = dataBlock.inputValue(IKVChain.inHierarchyMode).asBool()
        # if l1m < 0.001:
        #     betaCos = 0.0
        # else:
        betaCos = (math.pow(l1m, 2.0) + math.pow(l3, 2.0) - math.pow(l2m, 2.0)) / (2.0 * l1m * l3)
        if betaCos < -1.0:
            betaCos = -1.0
        beta = math.acos(betaCos)
        betaSin = math.sin(beta)
        # if l3 < chainLength * compressionLimit + 0.001:
        #     gamma = math.acos(1.0)
        # else:
        gammaCos = (math.pow(l1m, 2.0) + math.pow(l2m, 2.0) - math.pow(l3, 2.0)) / (2.0 * l1m * l2m)
        if gammaCos > 1.0:
            gammaCos = 1.0
        gamma = math.acos(gammaCos)
            # gamma = math.acos((math.pow(l1m, 2.0) + math.pow(l2m, 2.0) - math.pow(l3, 2.0)) / (2.0 * l1m * l2m))
        if hierarchyMode:
            gammaComplement = gamma - math.pi
        else:
            gammaComplement = gamma + beta - math.pi
        gammaComplementCos = math.cos(gammaComplement)
        gammaComplementSin = math.sin(gammaComplement)
        alpha = math.pi - beta - gamma
        alphaCos = math.cos(alpha)
        alphaSin = math.sin(alpha)
        outDebugAngle.setMAngle(om2.MAngle(beta))
        outDebugAngle.setClean()

        # Cartoony features
        stretch = dataBlock.inputValue(IKVChain.inStretch).asFloat()
        if stretch > 0.0:
            clampStretch = dataBlock.inputValue(IKVChain.inClampStretch).asFloat()
            clampStretchValue = dataBlock.inputValue(IKVChain.inClampValue).asFloat()
            squash = dataBlock.inputValue(IKVChain.inSquash).asFloat()
            if xDist > da and softValue > 0:
                scaleFactor = xDist / l3soft
            else:
                scaleFactor = xDist / chainLength
            if xDist >= da:
                clampFactor = (1.0 - clampStretch) * scaleFactor + clampStretch * min(scaleFactor, clampStretchValue)
                stretchFactor = (1.0 - stretch) + stretch * clampFactor
            else:
                stretchFactor = 1.0
            squashFactor = (1.0 - squash) + squash * (1.0 / math.sqrt(stretchFactor))
        else:
            stretchFactor = 1.0
            squashFactor = 1.0

        # Output Transforms
        outChainHdle = dataBlock.outputArrayValue(IKVChain.outChain)
        index = len(outChainHdle)
        srtList = []

        if hierarchyMode:
            mScale = om2.MFloatMatrix()
            mScale[0] = stretchFactor
            mScale[5] = squashFactor
            mScale[10] = squashFactor
            mLocal = om2.MFloatMatrix()
            mLocal[0] = betaCos
            mLocal[1] = betaSin
            mLocal[4] = -betaSin
            mLocal[5] = betaCos
            mResult = mScale * mLocal * mBasis
            srtList.append(mResult)
            mLocal = om2.MFloatMatrix()
            mLocal[0] = gammaComplementCos
            mLocal[1] = gammaComplementSin
            mLocal[4] = -gammaComplementSin
            mLocal[5] = gammaComplementCos
            mResult = mScale * mLocal
            mResult[12] = l1m
            srtList.append(mResult)
            mLocal = om2.MFloatMatrix()
            mLocal[0] = alphaCos
            mLocal[1] = alphaSin
            mLocal[4] = -alphaSin
            mLocal[5] = alphaCos
            mLocal[12] = l2m
            srtList.append(mLocal)
        else:
            mScale = om2.MFloatMatrix()
            mScale[0] = stretchFactor
            mScale[5] = squashFactor
            mScale[10] = squashFactor
            mLocal = om2.MFloatMatrix()
            mLocal[0] = betaCos
            mLocal[1] = betaSin
            mLocal[4] = -betaSin
            mLocal[5] = betaCos
            mResult = mScale * mLocal * mBasis
            srtList.append(mResult)
            mLocal = om2.MFloatMatrix()
            mLocal[0] = gammaComplementCos
            mLocal[1] = gammaComplementSin
            mLocal[4] = -gammaComplementSin
            mLocal[5] = gammaComplementCos
            mLocal[12] = betaCos * l1m * stretchFactor
            mLocal[13] = betaSin * l1m * stretchFactor
            mResult = mScale * mLocal * mBasis
            srtList.append(mResult)
            mLocal = mHandle
            mLocal[12] = mBasis[12] + mBasis[0] * l3 * stretchFactor
            mLocal[13] = mBasis[13] + mBasis[1] * l3 * stretchFactor
            mLocal[14] = mBasis[14] + mBasis[2] * l3 * stretchFactor
            mResult = mScale * mLocal
            srtList.append(mResult)

        for i in range(index):
            outChainHdle.jumpToLogicalElement(i)
            resultHdle = outChainHdle.outputValue()
            if i < index and i < len(srtList):
                resultHdle.setMFloatMatrix(srtList[i])
            else:
                resultHdle.setMFloatMatrix(om2.MFloatMatrix())

        outChainHdle.setAllClean()
