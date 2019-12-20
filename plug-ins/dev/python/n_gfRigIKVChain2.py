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
    inParInvMtx = om2.MObject()
    inJntOrient = om2.MObject()
    inRestLengthStart = om2.MObject()
    inRestLengthEnd = om2.MObject()
    inCompressionLimit = om2.MObject()
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
        uAttr = om2.MFnUnitAttribute()
        nAttr = om2.MFnNumericAttribute()

        IKVChainSolver.inRoot = mAttr.create("root", "root", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inHandle = mAttr.create("handle", "handle", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inPoleVector = mAttr.create("poleVector", "pole", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inOffset = mAttr.create("offset", "offset", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        INPUT_ATTR(mAttr)

        IKVChainSolver.inParInvMtx = mAttr.create("parentInverseMatrix", "pim", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        jntOriX = uAttr.create("jointOrientX", "jox", om2.MFnUnitAttribute.kAngle, 0.0)
        jntOriY = uAttr.create("jointOrientY", "joy", om2.MFnUnitAttribute.kAngle, 0.0)
        jntOriZ = uAttr.create("jointOrientZ", "joz", om2.MFnUnitAttribute.kAngle, 0.0)
        IKVChainSolver.inJntOrient = nAttr.create("jointOrient", "jo", jntOriX, jntOriY, jntOriZ)
        nAttr.array = True
        INPUT_ATTR(nAttr)

        IKVChainSolver.inRestLengthStart = nAttr.create("restLengthStart", "rls", om2.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0.001)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inRestLengthEnd = nAttr.create("restLengthEnd", "rle", om2.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0.001)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inCompressionLimit = nAttr.create("compressionLimit", "cl", om2.MFnNumericData.kFloat, 0.1)
        nAttr.setMin(0.001)
        nAttr.setMax(0.4)
        INPUT_ATTR(nAttr)

        IKVChainSolver.outChain = mAttr.create("outChain", "oc", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        OUTPUT_ATTR(mAttr)

        IKVChainSolver.addAttribute(IKVChainSolver.inRoot)
        IKVChainSolver.addAttribute(IKVChainSolver.inHandle)
        IKVChainSolver.addAttribute(IKVChainSolver.inPoleVector)
        IKVChainSolver.addAttribute(IKVChainSolver.inOffset)
        IKVChainSolver.addAttribute(IKVChainSolver.inParInvMtx)
        IKVChainSolver.addAttribute(IKVChainSolver.inJntOrient)
        IKVChainSolver.addAttribute(IKVChainSolver.inRestLengthStart)
        IKVChainSolver.addAttribute(IKVChainSolver.inRestLengthEnd)
        IKVChainSolver.addAttribute(IKVChainSolver.inCompressionLimit)
        IKVChainSolver.addAttribute(IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inRoot, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inHandle, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inPoleVector, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inOffset, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inParInvMtx, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inJntOrient, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inRestLengthStart, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inRestLengthEnd, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inCompressionLimit, IKVChainSolver.outChain)

    @staticmethod
    def negateOrientation(mtx, orient):
        """
        Receive a matrix and return a new matrix with given orientation negated.

        Args:
            * Mtx (MMatrix): The given matrix.
            * Orient (MQuaternion): The given orientation.

        Returns:
            * MMatrix: A new matrix with new orientation.
        """
        mtxFn = om2.MTransformationMatrix(mtx)
        vTrans = mtxFn.translation(om2.MSpace.kWorld)
        qRot = mtxFn.rotation(asQuaternion=True)
        qRot *= orient
        sca = mtxFn.scale(om2.MSpace.kTransform)
        mtxFn = om2.MTransformationMatrix()
        mtxFn.translateBy(vTrans, om2.MSpace.kTransform)
        mtxFn.rotateBy(qRot, om2.MSpace.kTransform)
        mtxFn.scaleBy(sca, om2.MSpace.kTransform)
        return mtxFn.asMatrix()

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        if plug != IKVChainSolver.outChain:
            return om2.kUnknownParameter

        # Get basis matrix
        mRoot = dataBlock.inputValue(IKVChainSolver.inRoot).asMatrix()
        mHandle = dataBlock.inputValue(IKVChainSolver.inHandle).asMatrix()
        mPoleVector = dataBlock.inputValue(IKVChainSolver.inPoleVector).asMatrix()

        vRoot = om2.MVector(mRoot[12], mRoot[13], mRoot[14])
        vHandle = om2.MVector(mHandle[12], mHandle[13], mHandle[14])
        vPoleVector = om2.MVector(mPoleVector[12], mPoleVector[13], mPoleVector[14])

        vAim = vHandle - vRoot
        nAim = vAim.normal()
        vUp = vPoleVector - vRoot
        nNormal = vUp - ((vUp * nAim) * nAim)
        nNormal.normalize()
        nBinormal = nAim ^ nNormal
        nBinormal.normalize()
        basis = [
            nAim.x, nAim.y, nAim.z, 0.0,
            nNormal.x, nNormal.y, nNormal.z, 0.0,
            nBinormal.x, nBinormal.y, nBinormal.z, 0.0,
            vRoot.x, vRoot.y, vRoot.z, 1.0
        ]
        mBasis = om2.MMatrix(basis)


        # Solve triangle
        startRestLength = dataBlock.inputValue(IKVChainSolver.inRestLengthStart).asFloat()
        endRestLength = dataBlock.inputValue(IKVChainSolver.inRestLengthEnd).asFloat()
        compressionLimit = dataBlock.inputValue(IKVChainSolver.inCompressionLimit).asFloat()

        startLen = startRestLength
        endLen = endRestLength
        handleLen = vAim.length()
        chainLen = startLen + endLen

        rigidLen = max(min(handleLen, chainLen), chainLen * compressionLimit)
        solverLen = rigidLen


        # Angle mesurement
        startLenSquared = math.pow(startLen, 2.0)
        endLenSquared = math.pow(endLen, 2.0)
        solverLenSquared = math.pow(solverLen, 2.0)

        betaCosPure = (startLenSquared + solverLenSquared - endLenSquared) / (2.0 * startLen * solverLen)
        betaCos = min(max(betaCosPure, -1.0), 1.0)
        beta = math.acos(betaCos)
        betaSin = math.sin(beta)
        gammaCosPure = (startLenSquared + endLenSquared - solverLenSquared) / (2.0 * startLen * endLen)
        gammaCos = min(max(gammaCosPure, -1.0), 1.0)
        gamma = math.acos(gammaCos)
        gammaComplement = gamma - math.pi
        gammaComplementCos = math.cos(gammaComplement)
        gammaComplementSin = math.sin(gammaComplement)
        alpha = math.pi - beta - gamma
        alphaCos = math.cos(alpha)
        alphaSin = math.sin(alpha)


        # Output transforms
        offsetHandle = dataBlock.inputArrayValue(IKVChainSolver.inOffset)
        jntOriHandle = dataBlock.inputArrayValue(IKVChainSolver.inJntOrient)
        outChainHandle = dataBlock.outputArrayValue(IKVChainSolver.outChain)
        srtList = []
        offsetList = []
        jntOriList = []

        for i in range(len(offsetHandle)):
            offsetHandle.jumpToLogicalElement(i)
            mOff = offsetHandle.inputValue().asMatrix()
            offsetList.append(mOff)
        for i in range(len(jntOriHandle)):
            jntOriHandle.jumpToLogicalElement(i)
            eOri = om2.MEulerRotation(jntOriHandle.inputValue().asDouble3())
            qOri = eOri.asQuaternion()
            qOri.invertIt()
            jntOriList.append(qOri)

        offsetLen = len(offsetList)
        orientLen = len(jntOriList)

        mLocal = om2.MMatrix()
        mLocal[0] = betaCos
        mLocal[1] = betaSin
        mLocal[4] = -betaSin
        mLocal[5] = betaCos
        mResult = mLocal * mBasis
        if offsetLen >= 1:
            mResult = offsetList[0] * mLocal * mBasis
        if orientLen >= 1:
            mResult = IKVChainSolver.negateOrientation(mResult, jntOriList[0])
        srtList.append(mResult)
        mLocal = om2.MMatrix()
        mLocal[0] = gammaComplementCos
        mLocal[1] = gammaComplementSin
        mLocal[4] = -gammaComplementSin
        mLocal[5] = gammaComplementCos
        mLocal[12] = startLen
        mResult = mLocal
        if offsetLen >= 2:
            mResult = offsetList[1] * mLocal
        if orientLen >= 2:
            mResult = IKVChainSolver.negateOrientation(mResult, jntOriList[1])
        srtList.append(mResult)
        mLocal = om2.MMatrix()
        mLocal[0] = alphaCos
        mLocal[1] = alphaSin
        mLocal[4] = -alphaSin
        mLocal[5] = alphaCos
        mLocal[12] = endLen
        mResult = mLocal
        srtList.append(mResult)

        for i in range(len(outChainHandle)):
            outChainHandle.jumpToLogicalElement(i)
            resultHandle = outChainHandle.outputValue()
            if i < len(outChainHandle) and i < len(srtList):
                resultHandle.setMMatrix(srtList[i])
            else:
                resultHandle.setMMatrix(om2.MMatrix())

        outChainHandle.setAllClean()
