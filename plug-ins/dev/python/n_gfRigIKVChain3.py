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
    inRestLenStart = om2.MObject()
    inRestLenEnd = om2.MObject()
    inCompressionLimit = om2.MObject()
    inSoftness = om2.MObject()
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

        IKVChainSolver.inRoot = mAttr.create("root", "root", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inHandle = mAttr.create("handle", "handle", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inPoleVector = mAttr.create("poleVector", "pole", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inOffset = mAttr.create("offset", "offset", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        INPUT_ATTR(mAttr)

        IKVChainSolver.inRestLenStart = nAttr.create("restLengthStart", "rls", om2.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0.001)
        INPUT_ATTR(nAttr)
        nAttr.keyable = False
        nAttr.channelBox = True

        IKVChainSolver.inRestLenEnd = nAttr.create("restLengthEnd", "rle", om2.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0.001)
        INPUT_ATTR(nAttr)
        nAttr.keyable = False
        nAttr.channelBox = True

        IKVChainSolver.inCompressionLimit = nAttr.create("compressionLimit", "cl", om2.MFnNumericData.kFloat, 0.1)
        nAttr.setMin(0.001)
        nAttr.setMax(0.4)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inSoftness = nAttr.create("softness", "soft", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setSoftMax(0.2)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        IKVChainSolver.outChain = mAttr.create("outChain", "oc", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        OUTPUT_ATTR(mAttr)

        IKVChainSolver.addAttribute(IKVChainSolver.inRoot)
        IKVChainSolver.addAttribute(IKVChainSolver.inHandle)
        IKVChainSolver.addAttribute(IKVChainSolver.inPoleVector)
        IKVChainSolver.addAttribute(IKVChainSolver.inOffset)
        IKVChainSolver.addAttribute(IKVChainSolver.inRestLenStart)
        IKVChainSolver.addAttribute(IKVChainSolver.inRestLenEnd)
        IKVChainSolver.addAttribute(IKVChainSolver.inCompressionLimit)
        IKVChainSolver.addAttribute(IKVChainSolver.inSoftness)
        IKVChainSolver.addAttribute(IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inRoot, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inHandle, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inPoleVector, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inOffset, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inRestLenStart, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inRestLenEnd, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inCompressionLimit, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inSoftness, IKVChainSolver.outChain)

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

        # Get basis transformation
        mRoot = dataBlock.inputValue(IKVChainSolver.inRoot).asMatrix()
        mHandle = dataBlock.inputValue(IKVChainSolver.inHandle).asMatrix()
        mPoleVector = dataBlock.inputValue(IKVChainSolver.inPoleVector).asMatrix()

        vRoot = om2.MVector(mRoot[12], mRoot[13], mRoot[14])
        vHandle = om2.MVector(mHandle[12], mHandle[13], mHandle[14])
        vPoleVector = om2.MVector(mPoleVector[12], mPoleVector[13], mPoleVector[14])

        vBasis = vRoot
        qBasis = om2.MQuaternion()

        vAim = vHandle - vRoot
        nAim = vAim.normal()
        qAim = om2.MQuaternion(om2.MVector.kXaxisVector, nAim)
        qBasis *= qAim

        vPole = vPoleVector - vRoot
        nNormal = vPole - ((vPole * nAim) * nAim)
        nNormal.normalize()
        nUp = om2.MVector.kYaxisVector.rotateBy(qAim)
        angle = nUp.angle(nNormal)
        qNormal = om2.MQuaternion(angle, nAim)
        if not nNormal.isEquivalent(nUp.rotateBy(qNormal), 1.0e-5):
            angle = 2.0 * math.pi - angle
            qNormal = om2.MQuaternion(angle, nAim)
        qBasis *= qNormal


        # Solve triangle
        restLenStart = dataBlock.inputValue(IKVChainSolver.inRestLenStart).asFloat()
        restLenEnd = dataBlock.inputValue(IKVChainSolver.inRestLenEnd).asFloat()
        compressionLimit = dataBlock.inputValue(IKVChainSolver.inCompressionLimit).asFloat()
        softVal = dataBlock.inputValue(IKVChainSolver.inSoftness).asFloat()

        startLen = restLenStart
        endLen = restLenEnd
        chainLen = startLen + endLen
        handleLen = vAim.length()

        rigidLen = max(min(handleLen, chainLen), chainLen * compressionLimit)
        dc = chainLen
        da = (1.0 - softVal) * dc
        if handleLen > da and softVal > 0.0:
            ds = dc - da
            softLenPole = ds * (1.0 - math.pow(math.e, (da - handleLen) / ds)) + da
            solverLen = softLenPole
        solverLen = rigidLen


        # Pre calculations
        startLenSquared = math.pow(startLen, 2.0)
        endLenSquared = math.pow(endLen, 2.0)
        solverLenSquared = math.pow(solverLen, 2.0)
        outChainHandle = dataBlock.outputArrayValue(IKVChainSolver.outChain)
        srtList = []


        # First Output
        vFirstPos = vBasis
        betaCosPure = (startLenSquared + solverLenSquared - endLenSquared) / (2.0 * startLen * solverLen)
        betaCos = min(max(betaCosPure, -1.0), 1.0)
        beta = math.acos(betaCos)
        qBeta = om2.MQuaternion(beta, om2.MVector.kZaxisVector)
        qFirstRot = qBeta * qBasis
        firstSca = [1.0, 1.0, 1.0]
        mtxFn = om2.MTransformationMatrix()
        mtxFn.setScale(firstSca, om2.MSpace.kTransform)
        mtxFn.setRotation(qFirstRot)
        mtxFn.setTranslation(vFirstPos, om2.MSpace.kTransform)
        mFirst = mtxFn.asMatrix()
        srtList.append(mFirst)


        # Second Output
        vSecondOri = nAim.rotateBy(om2.MQuaternion(beta, nAim ^ nNormal)) * startLen
        vSecondPos = vBasis + vSecondOri
        gammaCosPure = (startLenSquared + endLenSquared - solverLenSquared) / (2.0 * startLen * endLen)
        gammaCos = min(max(gammaCosPure, -1.0), 1.0)
        gamma = math.acos(gammaCos)
        gammaCmp = gamma + beta - math.pi
        qGamma = om2.MQuaternion(gammaCmp, om2.MVector.kZaxisVector)
        qSecondRot = qGamma * qBasis
        secondSca = [1.0, 1.0, 1.0]
        mtxFn = om2.MTransformationMatrix()
        mtxFn.setScale(secondSca, om2.MSpace.kTransform)
        mtxFn.setRotation(qSecondRot)
        mtxFn.setTranslation(vSecondPos, om2.MSpace.kTransform)
        mSecond = mtxFn.asMatrix()
        srtList.append(mSecond)


        # Third Output
        vThirdPos = vBasis + nAim * solverLen
        qThirdRot = qBasis
        thidSca = [1.0, 1.0, 1.0]
        mtxFn = om2.MTransformationMatrix()
        mtxFn.setScale(thidSca, om2.MSpace.kTransform)
        mtxFn.setRotation(qThirdRot)
        mtxFn.setTranslation(vThirdPos, om2.MSpace.kTransform)
        mThird = mtxFn.asMatrix()
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
