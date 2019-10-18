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
    IK Solver to VChain type of rig. Can be used to replace the default Maya
    IKRPSolver with the plus of some cartoony options.

Attributes:
    * Root: The world matrix of the root object.
    * Handle: The world matrix of the handle object.
    * Up Vector: The world matrix of the up vector object.
    * Parent Inverse Matrix: The world inverse matrix of the parent of the output chain.
    * Joint Orient: The array of joint orient sorted by output.
    * Preferred Angle: The preferred angle to be used to calculate the automatic pole vector.
    * Pv Mode: The type of calculation of the pole vector.
    * Twist: Twist the pole vector in automatic mode.
    * Hierarchy Mode: Solve IK in hierarchy mode. (Used by joint chains.)
    * Rest Length 1: The length of the first object.
    * Rest Length 2: The length of the second object.
    * Compression Limit: Limit compression of the solver.
    * Softness: Soft the solver to avoid pops in pole vector.
    * Snap Up Vector: Snap the pole vector to the snap object.
    * Snap Obj: The world matrix of the snap object.
    * Stretch: Enable stretch of the output chain.
    * Clamp Stretch: Clamp the stretch at certain value.
    * Clamp Value: Clamp value of the stretch clamp.
    * Squash: Enable automatic squash of the output chain.
    * Out Chain: The output matrices of the output chain.

Todo:
    * Create and develop the stretchMult attr.
    * Create and develop the squashMult attr.
    * Create and develop the slidePv attr.

Sources:
    * https://www.desmos.com/calculator/wthlznq4aj

This code supports Pylint. Rc file in project.
"""

import math
import maya.api._OpenMaya_py2 as om2


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


class IKVChainSolver(om2.MPxNode):
    """ Main class of gfRigIKVChainSolver node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inRoot = om2.MObject()
    inHandle = om2.MObject()
    inUpVector = om2.MObject()
    inParInvMtx = om2.MObject()
    inJointOrient = om2.MObject()
    inPreferredAngle = om2.MObject()
    inPvMode = om2.MObject()
    inTwist = om2.MObject()
    inHierarchyMode = om2.MObject()
    inRestLength1 = om2.MObject()
    inRestLength2 = om2.MObject()
    inCompressionLimit = om2.MObject()
    inSoftness = om2.MObject()
    inSnapUpVector = om2.MObject()
    inSnapObj = om2.MObject()
    inStretch = om2.MObject()
    inClampStretch = om2.MObject()
    inClampValue = om2.MObject()
    inSquash = om2.MObject()
    outChain = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return IKVChainSolver()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to IKVChainSolver class. Instances of IKVChainSolver will use these attributes to create plugs
        for use in the compute() method.
        """
        mAttr = om2.MFnMatrixAttribute()
        nAttr = om2.MFnNumericAttribute()
        uAttr = om2.MFnUnitAttribute()
        eAttr = om2.MFnEnumAttribute()

        IKVChainSolver.inRoot = mAttr.create("root", "root", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inHandle = mAttr.create("handle", "handle", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inUpVector = mAttr.create("upVector", "up", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inParInvMtx = mAttr.create("parentInverseMatrix", "pim", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        jntOriX = uAttr.create("jointOrientX", "jox", om2.MFnUnitAttribute.kAngle, 0.0)
        jntOriY = uAttr.create("jointOrientY", "joy", om2.MFnUnitAttribute.kAngle, 0.0)
        jntOriZ = uAttr.create("jointOrientZ", "joz", om2.MFnUnitAttribute.kAngle, 0.0)
        IKVChainSolver.inJointOrient = nAttr.create("jointOrient", "jo", jntOriX, jntOriY, jntOriZ)
        nAttr.array = True
        INPUT_ATTR(nAttr)

        IKVChainSolver.inPreferredAngle = uAttr.create("preferredAngle", "pa", om2.MFnUnitAttribute.kAngle, 0.0)
        uAttr.setMin(0.0)
        uAttr.setMax(2.0 * math.pi)
        INPUT_ATTR(uAttr)

        IKVChainSolver.inPvMode = eAttr.create("pvMode", "pvm", 0)
        eAttr.addField("Manual", 0)
        eAttr.addField("Auto", 1)
        INPUT_ATTR(eAttr)

        IKVChainSolver.inTwist = uAttr.create("twist", "tw", om2.MFnUnitAttribute.kAngle, 0.0)
        INPUT_ATTR(uAttr)

        IKVChainSolver.inHierarchyMode = nAttr.create("hierarchyMode", "hm", om2.MFnNumericData.kBoolean, True)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inRestLength1 = nAttr.create("restLength1", "rl1", om2.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0.001)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inRestLength2 = nAttr.create("restLength2", "rl2", om2.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0.001)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inCompressionLimit = nAttr.create("compressionLimit", "cl", om2.MFnNumericData.kFloat, 0.1)
        nAttr.setMin(0.001)
        nAttr.setMax(0.4)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inSoftness = nAttr.create("softness", "soft", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setSoftMax(0.4)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inSnapUpVector = nAttr.create("snapPoleVector", "snap", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inSnapObj = mAttr.create("snapObject", "sobj", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inStretch = nAttr.create("stretch", "st", om2.MFnNumericData.kDouble, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inClampStretch = nAttr.create("clampStretch", "cst", om2.MFnNumericData.kDouble, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inClampValue = nAttr.create("clampValue", "cstv", om2.MFnNumericData.kDouble, 1.5)
        nAttr.setMin(1.0)
        nAttr.setSoftMax(1.8)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inSquash = nAttr.create("squash", "sq", om2.MFnNumericData.kDouble, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        IKVChainSolver.outChain = mAttr.create("outChain", "oc", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        OUTPUT_ATTR(mAttr)

        IKVChainSolver.addAttribute(IKVChainSolver.inRoot)
        IKVChainSolver.addAttribute(IKVChainSolver.inHandle)
        IKVChainSolver.addAttribute(IKVChainSolver.inUpVector)
        IKVChainSolver.addAttribute(IKVChainSolver.inParInvMtx)
        IKVChainSolver.addAttribute(IKVChainSolver.inJointOrient)
        IKVChainSolver.addAttribute(IKVChainSolver.inPreferredAngle)
        IKVChainSolver.addAttribute(IKVChainSolver.inPvMode)
        IKVChainSolver.addAttribute(IKVChainSolver.inTwist)
        IKVChainSolver.addAttribute(IKVChainSolver.inHierarchyMode)
        IKVChainSolver.addAttribute(IKVChainSolver.inRestLength1)
        IKVChainSolver.addAttribute(IKVChainSolver.inRestLength2)
        IKVChainSolver.addAttribute(IKVChainSolver.inCompressionLimit)
        IKVChainSolver.addAttribute(IKVChainSolver.inSoftness)
        IKVChainSolver.addAttribute(IKVChainSolver.inSnapUpVector)
        IKVChainSolver.addAttribute(IKVChainSolver.inSnapObj)
        IKVChainSolver.addAttribute(IKVChainSolver.inStretch)
        IKVChainSolver.addAttribute(IKVChainSolver.inClampStretch)
        IKVChainSolver.addAttribute(IKVChainSolver.inClampValue)
        IKVChainSolver.addAttribute(IKVChainSolver.inSquash)
        IKVChainSolver.addAttribute(IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inRoot, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inHandle, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inUpVector, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inParInvMtx, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inJointOrient, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inPreferredAngle, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inPvMode, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inTwist, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inHierarchyMode, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inRestLength1, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inRestLength2, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inCompressionLimit, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inSoftness, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inSnapUpVector, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inSnapObj, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inStretch, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inClampStretch, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inClampValue, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inSquash, IKVChainSolver.outChain)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=R0201
        if plug != IKVChainSolver.outChain:
            return om2.kUnknownParameter

        # Get basis matrix
        snap = dataBlock.inputValue(IKVChainSolver.inSnapUpVector).asFloat()
        pvMode = dataBlock.inputValue(IKVChainSolver.inPvMode).asShort()
        mRoot = dataBlock.inputValue(IKVChainSolver.inRoot).asMatrix()
        mHandle = dataBlock.inputValue(IKVChainSolver.inHandle).asMatrix()
        mUpVector = dataBlock.inputValue(IKVChainSolver.inUpVector).asMatrix()
        mSnap = dataBlock.inputValue(IKVChainSolver.inSnapObj).asMatrix()
        prefAngle = dataBlock.inputValue(IKVChainSolver.inPreferredAngle).asAngle().asRadians()
        twist = dataBlock.inputValue(IKVChainSolver.inTwist).asAngle().asRadians()
        vRoot = om2.MVector(mRoot[12], mRoot[13], mRoot[14])
        vHandle = om2.MVector(mHandle[12], mHandle[13], mHandle[14])
        vUpVector = om2.MVector(mUpVector[12], mUpVector[13], mUpVector[14])
        vSnap = om2.MVector(mSnap[12], mSnap[13], mSnap[14])
        vXDirection = vHandle - vRoot
        xDist = vXDirection.length()
        nXAxis = vXDirection.normal()
        vL1Snap = vSnap - vRoot
        vL2Snap = vSnap - vHandle
        if pvMode == 0:
            vUpDirection = vUpVector - vRoot
            vYDirection = vUpDirection - ((vUpDirection * nXAxis) * nXAxis)
            nYAxis = vYDirection.normal()
        else:
            vAutoPosWorld = vRoot + om2.MVector(math.cos(twist + prefAngle), 0.0, math.sin(twist + prefAngle))
            vAutoPosLocal = vAutoPosWorld - vRoot
            vYDirection = vAutoPosLocal - ((vAutoPosLocal * nXAxis) * nXAxis)
            nYAxis = vYDirection.normal()
        if snap > 0.0:
            vSnapDirection = vL1Snap - ((vL1Snap * nXAxis) * nXAxis)
            nSnapDirection = vSnapDirection.normal()
            nYAxisSnap = (1.0 - snap) * nYAxis + snap * nSnapDirection
        else:
            nYAxisSnap = nYAxis
        nZAxis = nXAxis ^ nYAxisSnap
        basis = [nXAxis.x, nXAxis.y, nXAxis.z, 0.0,
                 nYAxisSnap.x, nYAxisSnap.y, nYAxisSnap.z, 0.0,
                 nZAxis.x, nZAxis.y, nZAxis.z, 0.0,
                 vRoot.x, vRoot.y, vRoot.z, 1.0]
        mBasis = om2.MMatrix(basis)

        # Solve triangle
        l1 = dataBlock.inputValue(IKVChainSolver.inRestLength1).asFloat()  # UpperArm
        l2 = dataBlock.inputValue(IKVChainSolver.inRestLength2).asFloat()  # Forearm
        compressionLimit = dataBlock.inputValue(IKVChainSolver.inCompressionLimit).asFloat()  # Rigid
        softValue = dataBlock.inputValue(IKVChainSolver.inSoftness).asFloat()
        l1m = l1 # * stretchMult1
        l2m = l2 # * stretchMult2
        l1Snap = vL1Snap.length()
        l2Snap = vL2Snap.length()
        length1 = (1.0 - snap) * l1m + snap * l1Snap
        length2 = (1.0 - snap) * l2m + snap * l2Snap
        chainLength = (1.0 - snap) * (l1m + l2m) + snap * (l1Snap + l2Snap)
        l3rigid = max(min(xDist, chainLength), chainLength * compressionLimit)
        dc = chainLength
        da = (1.0 - softValue) * dc
        if xDist > da and softValue > 0:
            ds = dc - da
            l3soft = ds * (1.0 - math.pow(math.e, (da - xDist) / ds)) + da
            l3SnapSoft = (1.0 - snap) * l3soft + snap * l3rigid
            l3 = l3SnapSoft
        else:
            l3 = l3rigid

        # Angle mesurement
        hierarchyMode = dataBlock.inputValue(IKVChainSolver.inHierarchyMode).asBool()
        betaCos = (math.pow(length1, 2.0) + math.pow(l3, 2.0) - math.pow(length2, 2.0)) / (2.0 * length1 * l3)
        if betaCos < -1.0:
            betaCos = -1.0
        beta = math.acos(betaCos)
        betaSin = math.sin(beta)
        gammaCos = (math.pow(length1, 2.0) + math.pow(length2, 2.0) - math.pow(l3, 2.0)) / (2.0 * length1 * length2)
        if gammaCos > 1.0:
            gammaCos = 1.0
        gamma = math.acos(gammaCos)
        if hierarchyMode:
            gammaComplement = gamma - math.pi
        else:
            gammaComplement = gamma + beta - math.pi
        gammaComplementCos = math.cos(gammaComplement)
        gammaComplementSin = math.sin(gammaComplement)
        alpha = math.pi - beta - gamma
        alphaCos = math.cos(alpha)
        alphaSin = math.sin(alpha)

        # Cartoony features
        stretch = dataBlock.inputValue(IKVChainSolver.inStretch).asDouble()
        if stretch > 0.0:
            clampStretch = dataBlock.inputValue(IKVChainSolver.inClampStretch).asDouble()
            clampStretchValue = dataBlock.inputValue(IKVChainSolver.inClampValue).asDouble()
            squash = dataBlock.inputValue(IKVChainSolver.inSquash).asDouble()
            if xDist > da and softValue > 0:
                scaleFactor = xDist / l3SnapSoft
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

        # Output transforms
        outChainHdle = dataBlock.outputArrayValue(IKVChainSolver.outChain)
        srtList = []
        jntOriList = []
        jntOriHandle = dataBlock.inputArrayValue(IKVChainSolver.inJointOrient)
        for i in range(len(jntOriHandle)):
            jntOriHandle.jumpToLogicalElement(i)
            eOri = om2.MEulerRotation(jntOriHandle.inputValue().asDouble3())
            mtxFn = om2.MTransformationMatrix()
            mtxFn.rotateBy(eOri, om2.MSpace.kTransform)
            mOri = mtxFn.asMatrix()
            jntOriList.append(mOri)
        if hierarchyMode:
            mParInv = dataBlock.inputValue(IKVChainSolver.inParInvMtx).asMatrix()
            mScale = om2.MMatrix()
            mScale[0] = stretchFactor
            mScale[5] = squashFactor
            mScale[10] = squashFactor
            mLocal = om2.MMatrix()
            mLocal[0] = betaCos
            mLocal[1] = betaSin
            mLocal[4] = -betaSin
            mLocal[5] = betaCos
            if len(jntOriList) >= 1:
                mResult = mScale * mLocal * mBasis * mParInv * jntOriList[0].inverse()
            else:
                mResult = mScale * mLocal * mBasis * mParInv
            srtList.append(mResult)
            mLocal = om2.MMatrix()
            mLocal[0] = gammaComplementCos
            mLocal[1] = gammaComplementSin
            mLocal[4] = -gammaComplementSin
            mLocal[5] = gammaComplementCos
            if len(jntOriList) >= 2:
                mResult = mScale * mLocal * jntOriList[1].inverse()
            else:
                mResult = mScale * mLocal
            mResult[12] = length1
            srtList.append(mResult)
            mLocal = om2.MMatrix()
            mLocal[0] = alphaCos
            mLocal[1] = alphaSin
            mLocal[4] = -alphaSin
            mLocal[5] = alphaCos
            mLocal[12] = length2
            srtList.append(mLocal)
        else:
            mScale = om2.MMatrix()
            mScale[0] = stretchFactor
            mScale[5] = squashFactor
            mScale[10] = squashFactor
            mLocal = om2.MMatrix()
            mLocal[0] = betaCos
            mLocal[1] = betaSin
            mLocal[4] = -betaSin
            mLocal[5] = betaCos
            mResult = mScale * mLocal * mBasis
            srtList.append(mResult)
            mLocal = om2.MMatrix()
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
        for i in range(len(outChainHdle)):
            outChainHdle.jumpToLogicalElement(i)
            resultHdle = outChainHdle.outputValue()
            if i < len(outChainHdle) and i < len(srtList):
                resultHdle.setMMatrix(srtList[i])
            else:
                resultHdle.setMMatrix(om2.MFloatMatrix())
        outChainHdle.setAllClean()
