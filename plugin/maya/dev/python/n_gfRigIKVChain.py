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
    inPoleVector = om2.MObject()
    inOffset = om2.MObject()
    inJntOri = om2.MObject()
    inParInvMtx = om2.MObject()
    inRestLenStart = om2.MObject()
    inRestLenEnd = om2.MObject()
    inPreferredAngle = om2.MObject()
    inTwist = om2.MObject()
    inPvMode = om2.MObject()
    inHierarchyMode = om2.MObject()
    inFlip = om2.MObject()
    inUseScale = om2.MObject()
    inCompressionLimit = om2.MObject()
    inSnapUpVector = om2.MObject()
    inSnap = om2.MObject()
    inSoftness = om2.MObject()
    inStretch = om2.MObject()
    inClampStretch = om2.MObject()
    inClampValue = om2.MObject()
    # inStretchMultStart = om2.MObject()
    # inStretchMultEnd = om2.MObject()
    inSquash = om2.MObject()
    inSquashMultStart = om2.MObject()
    inSquashMultEnd = om2.MObject()
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
        eAttr = om2.MFnEnumAttribute()
        uAttr = om2.MFnUnitAttribute()

        IKVChainSolver.inRoot = mAttr.create("root", "root", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inHandle = mAttr.create("handle", "handle", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inPoleVector = mAttr.create("poleVector", "pole", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        offX = uAttr.create("offsetX", "offx", om2.MFnUnitAttribute.kAngle, 0.0)
        offY = uAttr.create("offsetY", "offy", om2.MFnUnitAttribute.kAngle, 0.0)
        offZ = uAttr.create("offsetZ", "offz", om2.MFnUnitAttribute.kAngle, 0.0)
        IKVChainSolver.inOffset = nAttr.create("offset", "off", offX, offY, offZ)
        nAttr.array = True
        INPUT_ATTR(nAttr)

        jntOriX = uAttr.create("jointOrientX", "jox", om2.MFnUnitAttribute.kAngle, 0.0)
        jntOriY = uAttr.create("jointOrientY", "joy", om2.MFnUnitAttribute.kAngle, 0.0)
        jntOriZ = uAttr.create("jointOrientZ", "joz", om2.MFnUnitAttribute.kAngle, 0.0)
        IKVChainSolver.inJntOri = nAttr.create("jointOrient", "jo", jntOriX, jntOriY, jntOriZ)
        nAttr.array = True
        INPUT_ATTR(nAttr)

        IKVChainSolver.inParInvMtx = mAttr.create("parentInverseMatrix", "pim", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inRestLenStart = nAttr.create("restLengthStart", "rls", om2.MFnNumericData.kFloat, 1.0)
        # nAttr.setMin(0.001)
        INPUT_ATTR(nAttr)
        nAttr.channelBox = True

        IKVChainSolver.inRestLenEnd = nAttr.create("restLengthEnd", "rle", om2.MFnNumericData.kFloat, 1.0)
        # nAttr.setMin(0.001)
        INPUT_ATTR(nAttr)
        nAttr.channelBox = True

        IKVChainSolver.inPreferredAngle = uAttr.create("preferredAngle", "pa", om2.MFnUnitAttribute.kAngle, 0.0)
        uAttr.setMin(0.0)
        uAttr.setMax(2.0 * math.pi)
        INPUT_ATTR(uAttr)
        uAttr.channelBox = True

        IKVChainSolver.inTwist = uAttr.create("twist", "twist", om2.MFnUnitAttribute.kAngle, 0.0)
        INPUT_ATTR(uAttr)

        IKVChainSolver.inPvMode = eAttr.create("pvMode", "pvm", 0)
        eAttr.addField("Manual", 0)
        eAttr.addField("Auto", 1)
        INPUT_ATTR(eAttr)

        IKVChainSolver.inHierarchyMode = nAttr.create("hierarchyMode", "hm", om2.MFnNumericData.kBoolean, True)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inFlip = nAttr.create("flipOrientation", "fori", om2.MFnNumericData.kBoolean, False)
        INPUT_ATTR(nAttr)
        nAttr.channelBox = True

        IKVChainSolver.inUseScale = nAttr.create("useStretchAsScale", "usca", om2.MFnNumericData.kBoolean, False)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inCompressionLimit = nAttr.create("compressionLimit", "cl", om2.MFnNumericData.kFloat, 0.1)
        nAttr.setMin(0.001)
        nAttr.setMax(0.4)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inSnapUpVector = nAttr.create("snapUpVector", "supv", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inSnap = mAttr.create("snap", "snap", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inSoftness = nAttr.create("softness", "soft", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setSoftMax(0.2)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

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

        # IKVChainSolver.inStretchMultStart = nAttr.create("stretchMultStart", "stms", om2.MFnNumericData.kFloat, 1.0)
        # nAttr.setMin(0.001)
        # INPUT_ATTR(nAttr)

        # IKVChainSolver.inStretchMultEnd = nAttr.create("stretchMultEnd", "stme", om2.MFnNumericData.kFloat, 1.0)
        # nAttr.setMin(0.001)
        # INPUT_ATTR(nAttr)

        IKVChainSolver.inSquash = nAttr.create("squash", "sq", om2.MFnNumericData.kDouble, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        startSqX = nAttr.create("squashMultStartX", "sqmsx", om2.MFnNumericData.kFloat, 1.0)
        startSqY = nAttr.create("squashMultStartY", "sqmsy", om2.MFnNumericData.kFloat, 1.0)
        IKVChainSolver.inSquashMultStart = nAttr.create("squashMultStart", "sqms", startSqX, startSqY)
        nAttr.setMin([0.001, 0.001])
        INPUT_ATTR(nAttr)

        endSqX = nAttr.create("squashMultEndX", "sqmex", om2.MFnNumericData.kFloat, 1.0)
        endSqY = nAttr.create("squashMultEndY", "sqmey", om2.MFnNumericData.kFloat, 1.0)
        IKVChainSolver.inSquashMultEnd = nAttr.create("squashMultEnd", "sqme", endSqX, endSqY)
        nAttr.setMin([0.001, 0.001])
        INPUT_ATTR(nAttr)

        IKVChainSolver.outChain = mAttr.create("outChain", "oc", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        OUTPUT_ATTR(mAttr)

        IKVChainSolver.addAttribute(IKVChainSolver.inRoot)
        IKVChainSolver.addAttribute(IKVChainSolver.inHandle)
        IKVChainSolver.addAttribute(IKVChainSolver.inPoleVector)
        IKVChainSolver.addAttribute(IKVChainSolver.inOffset)
        IKVChainSolver.addAttribute(IKVChainSolver.inJntOri)
        IKVChainSolver.addAttribute(IKVChainSolver.inParInvMtx)
        IKVChainSolver.addAttribute(IKVChainSolver.inRestLenStart)
        IKVChainSolver.addAttribute(IKVChainSolver.inRestLenEnd)
        IKVChainSolver.addAttribute(IKVChainSolver.inPreferredAngle)
        IKVChainSolver.addAttribute(IKVChainSolver.inTwist)
        IKVChainSolver.addAttribute(IKVChainSolver.inPvMode)
        IKVChainSolver.addAttribute(IKVChainSolver.inHierarchyMode)
        IKVChainSolver.addAttribute(IKVChainSolver.inFlip)
        IKVChainSolver.addAttribute(IKVChainSolver.inUseScale)
        IKVChainSolver.addAttribute(IKVChainSolver.inCompressionLimit)
        IKVChainSolver.addAttribute(IKVChainSolver.inSnapUpVector)
        IKVChainSolver.addAttribute(IKVChainSolver.inSnap)
        IKVChainSolver.addAttribute(IKVChainSolver.inSoftness)
        IKVChainSolver.addAttribute(IKVChainSolver.inStretch)
        IKVChainSolver.addAttribute(IKVChainSolver.inClampStretch)
        IKVChainSolver.addAttribute(IKVChainSolver.inClampValue)
        # IKVChainSolver.addAttribute(IKVChainSolver.inStretchMultStart)
        # IKVChainSolver.addAttribute(IKVChainSolver.inStretchMultEnd)
        IKVChainSolver.addAttribute(IKVChainSolver.inSquash)
        IKVChainSolver.addAttribute(IKVChainSolver.inSquashMultStart)
        IKVChainSolver.addAttribute(IKVChainSolver.inSquashMultEnd)
        IKVChainSolver.addAttribute(IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inRoot, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inHandle, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inPoleVector, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inOffset, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inJntOri, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inParInvMtx, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inRestLenStart, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inRestLenEnd, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inPreferredAngle, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inTwist, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inPvMode, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inHierarchyMode, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inFlip, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inUseScale, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inCompressionLimit, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inSnapUpVector, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inSnap, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inSoftness, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inStretch, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inClampStretch, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inClampValue, IKVChainSolver.outChain)
        # IKVChainSolver.attributeAffects(IKVChainSolver.inStretchMultStart, IKVChainSolver.outChain)
        # IKVChainSolver.attributeAffects(IKVChainSolver.inStretchMultEnd, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inSquash, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inSquashMultStart, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inSquashMultEnd, IKVChainSolver.outChain)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        if plug != IKVChainSolver.outChain:
            return om2.kUnknownParameter

        # Get Basis Quaternion
        mRoot = dataBlock.inputValue(IKVChainSolver.inRoot).asMatrix()
        mHandle = dataBlock.inputValue(IKVChainSolver.inHandle).asMatrix()
        mPoleVector = dataBlock.inputValue(IKVChainSolver.inPoleVector).asMatrix()
        pvMode = dataBlock.inputValue(IKVChainSolver.inPvMode).asShort()
        prefAngle = dataBlock.inputValue(IKVChainSolver.inPreferredAngle).asAngle().asRadians()
        twist = dataBlock.inputValue(IKVChainSolver.inTwist).asAngle().asRadians()
        snap = dataBlock.inputValue(IKVChainSolver.inSnapUpVector).asFloat()
        mSnap = dataBlock.inputValue(IKVChainSolver.inSnap).asMatrix()
        flip = dataBlock.inputValue(IKVChainSolver.inFlip).asBool()

        vRoot = om2.MVector(mRoot[12], mRoot[13], mRoot[14])
        vHandle = om2.MVector(mHandle[12], mHandle[13], mHandle[14])
        vPoleVector = om2.MVector(mPoleVector[12], mPoleVector[13], mPoleVector[14])
        vSnap = om2.MVector(mSnap[12], mSnap[13], mSnap[14])

        primAxis = om2.MVector.kXaxisVector
        secAxis = om2.MVector.kYaxisVector
        if flip:
            primAxis = -om2.MVector.kXaxisVector
            secAxis = -om2.MVector.kYaxisVector
        binAxis = primAxis ^ secAxis
        qBasis = om2.MQuaternion()

        vAim = vHandle - vRoot
        nAim = vAim.normal()
        qAim = om2.MQuaternion(primAxis, nAim)
        qBasis *= qAim

        vStartSnap = vSnap - vRoot
        vEndSnap = vSnap - vHandle

        if pvMode == 0:
            vUp = vPoleVector - vRoot
        else:
            qTwist = om2.MQuaternion(prefAngle + twist, nAim)
            vUp = secAxis.rotateBy(qTwist)
        nNormalPole = vUp - ((vUp * nAim) * nAim)
        nNormalPole.normalize()
        if snap > 0.0:
            nNormalSnap = vStartSnap - ((vStartSnap * nAim) * nAim)
            nNormalSnap.normalize()
            nNormal = (1.0 - snap) * nNormalPole + snap * nNormalSnap
        else:
            nNormal = nNormalPole

        nUp = secAxis.rotateBy(qAim)
        angle = nUp.angle(nNormal)
        qNormal = om2.MQuaternion(angle, nAim)
        if not nNormal.isEquivalent(nUp.rotateBy(qNormal), 1.0e-5):
            angle = 2.0 * math.pi - angle
            qNormal = om2.MQuaternion(angle, nAim)
        qBasis *= qNormal


        # Solver Triangle
        restStartLen = dataBlock.inputValue(IKVChainSolver.inRestLenStart).asFloat()
        restEndLen = dataBlock.inputValue(IKVChainSolver.inRestLenEnd).asFloat()
        compressionLimit = dataBlock.inputValue(IKVChainSolver.inCompressionLimit).asFloat()
        softVal = dataBlock.inputValue(IKVChainSolver.inSoftness).asFloat()

        startSnapLen = vStartSnap.length()
        endSnapLen = vEndSnap.length()

        startLen = (1.0 - snap) * restStartLen + snap * startSnapLen
        endLen = (1.0 - snap) * restEndLen + snap * endSnapLen
        chainLen = (1.0 - snap) * (restStartLen + restEndLen) + snap * (startSnapLen + endSnapLen)
        handleLen = vAim.length()

        rigidLen = max(min(handleLen, chainLen), chainLen * compressionLimit)
        dc = chainLen
        da = (1.0 - softVal) * dc
        if handleLen > da and softVal > 0.0:
            ds = dc - da
            softLen = ds * (1.0 - math.pow(math.e, (da - handleLen) / ds)) + da
            solverLen = (1.0 - snap) * softLen + snap * rigidLen
        else:
            solverLen = rigidLen


        # Pre Calculations
        startLenSquared = math.pow(startLen, 2.0)
        endLenSquared = math.pow(endLen, 2.0)
        solverLenSquared = math.pow(solverLen, 2.0)
        stretch = dataBlock.inputValue(IKVChainSolver.inStretch).asDouble()
        squashMultStart = dataBlock.inputValue(IKVChainSolver.inSquashMultStart).asFloat2()
        squashMultEnd = dataBlock.inputValue(IKVChainSolver.inSquashMultEnd).asFloat2()
        if stretch > 0.0:
            clampStretch = dataBlock.inputValue(IKVChainSolver.inClampStretch).asDouble()
            clampValue = dataBlock.inputValue(IKVChainSolver.inClampValue).asDouble()
            squash = dataBlock.inputValue(IKVChainSolver.inSquash).asDouble()
            if handleLen > da and softVal > 0.0:
                scaleFactor = handleLen / solverLen
            else:
                scaleFactor = handleLen / chainLen
            if handleLen >= da:
                clampFactor = (1.0 - clampStretch) * scaleFactor + clampStretch * min(scaleFactor, clampValue)
                stretchFactor = (1.0 - stretch) + stretch * clampFactor
            else:
                stretchFactor = 1.0
            squashFactor = (1.0 - squash) + squash * (1.0 / math.sqrt(stretchFactor))
        else:
            stretchFactor = 1.0
            squashFactor = 1.0

        hierarchyMode = dataBlock.inputValue(IKVChainSolver.inHierarchyMode).asBool()
        useScale = dataBlock.inputValue(IKVChainSolver.inUseScale).asBool()
        outChainHandle = dataBlock.outputArrayValue(IKVChainSolver.outChain)
        offsetHandle = dataBlock.inputArrayValue(IKVChainSolver.inOffset)
        jntOriHandle = dataBlock.inputArrayValue(IKVChainSolver.inJntOri)
        mParInv = dataBlock.inputValue(IKVChainSolver.inParInvMtx).asMatrix()
        srtList = []
        offsetList = []
        jntOriList = []

        for i in range(len(offsetHandle)):
            offsetHandle.jumpToLogicalElement(i)
            eOff = om2.MEulerRotation(offsetHandle.inputValue().asDouble3())
            qOff = eOff.asQuaternion()
            offsetList.append(qOff)

        for i in range(len(jntOriHandle)):
            jntOriHandle.jumpToLogicalElement(i)
            eOri = om2.MEulerRotation(jntOriHandle.inputValue().asDouble3())
            qOri = eOri.asQuaternion()
            jntOriList.append(qOri)


        # First Output
        # Scale
        firstStretch = stretchFactor
        firstScaX = firstStretch
        if not useScale:
            firstStretch = 1.0
        firstSquash = [squashFactor * squashMultStart[0], squashFactor * squashMultStart[1]]
        firstSca = [firstStretch, firstSquash[0], firstSquash[1]]
        # Rotation
        betaCosPure = (startLenSquared + solverLenSquared - endLenSquared) / (2.0 * startLen * solverLen)
        betaCos = min(max(betaCosPure, -1.0), 1.0)
        beta = math.acos(betaCos)
        qBeta = om2.MQuaternion(beta, binAxis)
        qFirstRotW = qBeta * qBasis
        qFirstRot = om2.MQuaternion()
        if len(offsetList) >= 1:
            qFirstRot *= offsetList[0].invertIt()
        qFirstRot *= qFirstRotW
        if len(jntOriList) >= 1:
            qFirstRot *= jntOriList[0].invertIt()
        # Translation
        vFirstPos = vRoot
        # Matrix Output
        mtxFn = om2.MTransformationMatrix()
        mtxFn.setScale(firstSca, om2.MSpace.kTransform)
        mtxFn.setRotation(qFirstRot)
        mtxFn.setTranslation(vFirstPos, om2.MSpace.kTransform)
        mFirst = mtxFn.asMatrix()
        mFirst *= mParInv
        srtList.append(mFirst)


        # Second Output
        # Scale
        secondStretch = stretchFactor
        secondScaX = secondStretch
        if not useScale:
            secondStretch = 1.0
        secondSquash = [squashFactor * squashMultEnd[0], squashFactor * squashMultEnd[1]]
        secondSca = [secondStretch, secondSquash[0], secondSquash[1]]
        # Rotation
        gammaCosPure = (startLenSquared + endLenSquared - solverLenSquared) / (2.0 * startLen * endLen)
        gammaCos = min(max(gammaCosPure, -1.0), 1.0)
        gamma = math.acos(gammaCos)
        gammaCmp = gamma + beta - math.pi
        qGamma = om2.MQuaternion(gammaCmp, binAxis)
        qSecondRotW = qGamma * qBasis
        qSecondRot = om2.MQuaternion()
        if len(offsetList) >= 2:
            qSecondRot *= offsetList[1].invertIt()
        qSecondRot *= qSecondRotW
        if hierarchyMode:
            qSecondRot *= qFirstRotW.invertIt()
            if len(offsetList) >= 1:
                qSecondRot *= offsetList[0].invertIt()
        if len(jntOriList) >= 2:
            qSecondRot *= jntOriList[1].invertIt()
        # Translation
        if hierarchyMode:
            vSecondPos = primAxis * startLen
            if not useScale:
                vSecondPos *= firstScaX
        else:
            vSecondOri = nAim.rotateBy(om2.MQuaternion(beta, nAim ^ nNormal)) * startLen
            if not useScale:
                vSecondOri *= firstScaX
            vSecondPos = vRoot + vSecondOri
        # Matrix Output
        mtxFn = om2.MTransformationMatrix()
        mtxFn.setScale(secondSca, om2.MSpace.kTransform)
        mtxFn.setRotation(qSecondRot)
        mtxFn.setTranslation(vSecondPos, om2.MSpace.kTransform)
        mSecond = mtxFn.asMatrix()
        if not hierarchyMode:
            mSecond *= mParInv
        srtList.append(mSecond)


        # Third Output
        # Rotation
        qThirdRot = qBasis
        if hierarchyMode:
            qThirdRot *= qSecondRotW.invertIt()
            if len(offsetList) >= 2:
                qThirdRot *= offsetList[1].invertIt()
        # Translation
        if hierarchyMode:
            vThirdPos = primAxis * endLen
            if not useScale:
                vThirdPos *= secondScaX
        else:
            vThirdPos = vRoot + nAim * solverLen
            if not useScale:
                vThirdPos = vRoot + nAim * solverLen * stretchFactor
        # Matrix Output
        mtxFn = om2.MTransformationMatrix()
        mtxFn.setRotation(qThirdRot)
        mtxFn.setTranslation(vThirdPos, om2.MSpace.kTransform)
        mThird = mtxFn.asMatrix()
        if not hierarchyMode:
            mThird *= mParInv
        srtList.append(mThird)


        # Set outputs
        for i in range(len(outChainHandle)):
            outChainHandle.jumpToLogicalElement(i)
            resultHandle = outChainHandle.outputValue()
            if i < len(outChainHandle) and i < len(srtList):
                resultHandle.setMMatrix(srtList[i])
            else:
                resultHandle.setMMatrix(om2.MMatrix.kIdentity)

        outChainHandle.setAllClean()
