# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfRigHelperJoint node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.

Requirements:
    Maya 2017 or above.

Todo:
    * Get the two sources and their respectives offsets.
    * Add the two matrices blended.
    * Multiply by the target parent inverse matrix.
    * Decompose a euler rotation from this matrix.
    * Get the main source and the respective offset.
    * Multiply by the target parent inverse matrix.
    * Decompose a vector translate from this matrix.

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


class HelperJoint(om2.MPxNode):
    """ Main class of gfRigHelperJoint node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inSource = om2.MObject()                # Source object
    inSourceParent = om2.MObject()          # Parent of source object
    inParInvMtx = om2.MObject()             # The world inverse matrix of the parent of the target obj
    inSourceParSca = om2.MObject()          # The scale of the parent of source object
    inPositionOffset = om2.MObject()        # The position offset of target object
    inRotationOffset = om2.MObject()        # The rotation offset of target object
    inRotAngle = om2.MObject()              # The angle of rotation to evaluate
    inRestAngle = om2.MObject()             # The rest angle of rotation
    inPosMult = om2.MObject()               # The positive angle multiplier of target
    inNegMult = om2.MObject()               # The negative angle multiplier of target
    inTargetList = om2.MObject()            # Compound attribute for all target attributes
    outTransform = om2.MObject()            # The result matrix for the target

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return HelperJoint()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to HelperJoint class. Instances of HelperJoint will use these attributes to create plugs
        for use in the compute() method.
        """
        nAttr = om2.MFnNumericAttribute()
        mAttr = om2.MFnMatrixAttribute()
        uAttr = om2.MFnUnitAttribute()
        cAttr = om2.MFnCompoundAttribute()

        HelperJoint.inSource = mAttr.create("source", "s", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        HelperJoint.inSourceParent = mAttr.create("sourceParent", "sp", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        HelperJoint.inParInvMtx = mAttr.create("targetParentInverseMatrix", "tpimtx", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        HelperJoint.inSourceParSca = nAttr.createPoint("sourceParentScale", "spsca")
        nAttr.default = (1.0, 1.0, 1.0)
        INPUT_ATTR(nAttr)

        HelperJoint.inPositionOffset = nAttr.createPoint("positionOffset", "posoff")
        INPUT_ATTR(nAttr)

        rotOffX = uAttr.create("rotationOffsetX", "rotoffx", om2.MFnUnitAttribute.kAngle, 0.0)
        rotOffY = uAttr.create("rotationOffsetY", "rotoffy", om2.MFnUnitAttribute.kAngle, 0.0)
        rotOffZ = uAttr.create("rotationOffsetZ", "rotoffz", om2.MFnUnitAttribute.kAngle, 0.0)
        HelperJoint.inRotationOffset = nAttr.create("rotationOffset", "rotoff", rotOffX, rotOffY, rotOffZ)
        INPUT_ATTR(nAttr)

        HelperJoint.inRotAngle = uAttr.create("rotationAngle", "rotangle", om2.MFnUnitAttribute.kAngle, 0.0)
        INPUT_ATTR(uAttr)

        HelperJoint.inRestAngle = uAttr.create("restAngle", "rang", om2.MFnUnitAttribute.kAngle, 0.0)
        INPUT_ATTR(uAttr)

        HelperJoint.inPosMult = nAttr.create("positiveMultiplier", "posmult", om2.MFnNumericData.kFloat, 0.0)
        INPUT_ATTR(nAttr)

        HelperJoint.inNegMult = nAttr.create("negativeMultiplier", "negmult", om2.MFnNumericData.kFloat, 0.0)
        INPUT_ATTR(nAttr)

        HelperJoint.inTargetList = cAttr.create("targetList", "tgtl")
        cAttr.addChild(HelperJoint.inPositionOffset)
        cAttr.addChild(HelperJoint.inRotationOffset)
        cAttr.addChild(HelperJoint.inRotAngle)
        cAttr.addChild(HelperJoint.inRestAngle)
        cAttr.addChild(HelperJoint.inPosMult)
        cAttr.addChild(HelperJoint.inNegMult)
        # TODO(rotation interpolation): Rotation interpolation of the weighted add matrix.
        cAttr.array = True

        HelperJoint.outTransform = mAttr.create("outTransform", "outtrans", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        OUTPUT_ATTR(mAttr)

        HelperJoint.addAttribute(HelperJoint.inSource)
        HelperJoint.addAttribute(HelperJoint.inSourceParent)
        HelperJoint.addAttribute(HelperJoint.inParInvMtx)
        HelperJoint.addAttribute(HelperJoint.inSourceParSca)
        HelperJoint.addAttribute(HelperJoint.inTargetList)
        HelperJoint.addAttribute(HelperJoint.outTransform)
        HelperJoint.attributeAffects(HelperJoint.inSource, HelperJoint.outTransform)
        HelperJoint.attributeAffects(HelperJoint.inSourceParent, HelperJoint.outTransform)
        HelperJoint.attributeAffects(HelperJoint.inParInvMtx, HelperJoint.outTransform)
        HelperJoint.attributeAffects(HelperJoint.inSourceParSca, HelperJoint.outTransform)
        HelperJoint.attributeAffects(HelperJoint.inPositionOffset, HelperJoint.outTransform)
        HelperJoint.attributeAffects(HelperJoint.inRotationOffset, HelperJoint.outTransform)
        HelperJoint.attributeAffects(HelperJoint.inRotAngle, HelperJoint.outTransform)
        HelperJoint.attributeAffects(HelperJoint.inRestAngle, HelperJoint.outTransform)
        HelperJoint.attributeAffects(HelperJoint.inPosMult, HelperJoint.outTransform)
        HelperJoint.attributeAffects(HelperJoint.inNegMult, HelperJoint.outTransform)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != HelperJoint.outTransform:
            return om2.kUnknownParameter

        mSource = dataBlock.inputValue(HelperJoint.inSource).asMatrix()
        mtxFn = om2.MTransformationMatrix(mSource)
        mtxFn.setScale([1.0, 1.0, 1.0], om2.MSpace.kTransform)
        mSource = mtxFn.asMatrix()
        mSourceParent = dataBlock.inputValue(HelperJoint.inSourceParent).asMatrix()

        mParInv = dataBlock.inputValue(HelperJoint.inParInvMtx).asMatrix()
        sourceParSca = dataBlock.inputValue(HelperJoint.inSourceParSca).asFloat3()
        mtxFn = om2.MTransformationMatrix()
        mtxFn.scaleBy(sourceParSca, om2.MSpace.kTransform)
        mInvSca = mtxFn.asMatrix()
        targetListHandle = dataBlock.inputArrayValue(HelperJoint.inTargetList)

        outputList = []

        for i in range(len(targetListHandle)):
            targetListHandle.jumpToLogicalElement(i)
            targetHandle = targetListHandle.inputValue()
            vPosOffset = om2.MVector(targetHandle.child(HelperJoint.inPositionOffset).asFloat3())
            eRotOffset = om2.MEulerRotation(targetHandle.child(HelperJoint.inRotationOffset).asDouble3())
            angle = targetHandle.child(HelperJoint.inRotAngle).asAngle().asRadians()
            restAngle = targetHandle.child(HelperJoint.inRestAngle).asAngle().asRadians()
            posMult = targetHandle.child(HelperJoint.inPosMult).asFloat()
            negMult = targetHandle.child(HelperJoint.inNegMult).asFloat()

            mPositionOffset = om2.MMatrix()
            mPositionOffset[12] = vPosOffset.x
            mPositionOffset[13] = vPosOffset.y
            mPositionOffset[14] = vPosOffset.z
            multTranslation = abs(angle) * posMult
            if angle < restAngle:
                multTranslation = abs(angle) * negMult
            vPosOffset.normalize()
            mMultiplier = om2.MMatrix()
            mMultiplier[12] = vPosOffset.x * multTranslation
            mMultiplier[13] = vPosOffset.y * multTranslation
            mMultiplier[14] = vPosOffset.z * multTranslation
            mTargetPoint = mMultiplier * mPositionOffset * mSource
            mTargetOrient = mInvSca * (mSource * 0.5) + (mSourceParent * 0.5)

            vResultPos = om2.MVector(mTargetPoint[12], mTargetPoint[13], mTargetPoint[14])
            mtxFn = om2.MTransformationMatrix(mTargetOrient)
            eResultOri = eRotOffset + mtxFn.rotation(asQuaternion=False)
            mtxFn = om2.MTransformationMatrix()
            mtxFn.setRotation(eResultOri)
            mtxFn.setTranslation(vResultPos, om2.MSpace.kTransform)
            mResult = mtxFn.asMatrix() * mParInv
            outputList.append(mResult)

        outTransHandle = dataBlock.outputArrayValue(HelperJoint.outTransform)
        for i in range(len(outTransHandle)):
            outTransHandle.jumpToLogicalElement(i)
            resultHandle = outTransHandle.outputValue()
            if i < len(outTransHandle) and i < len(outputList):
                resultHandle.setMMatrix(outputList[i])
            else:
                resultHandle.setMMatrix(om2.MMatrix.kIdentity)
