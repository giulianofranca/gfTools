# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfRigBlendMatrix node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.

Requirements:
    Maya 2017 or above.

Todo:
    * Fix the scale compensation of the joints.
    * Dev the switch attr for the calculation of the scale compensation.
    * Multiply the vSca1 and vSca2 to the scale compensation before doing the blend.
    * https://forums.autodesk.com/t5/maya-animation-and-rigging/quot-bake-quot-segment-scale-compensate-result/td-p/8524752
    * https://sites.google.com/site/mayariggingwiki/rigging-notes/rig-fundamentals/rotation-order
    * https://talk.bindpose.com/entry/63
    * https://talk.bindpose.com/entry/64
    * https://talk.bindpose.com/entry/55
    * https://groups.google.com/forum/#!topic/python_inside_maya/MT2kKRzL2Ys (X-ray OpenGL)
    * Scale = xAxis.length()
    *
    * Fix Euler Lerp rotation interpolation by converting negation quaternions to negation eulers.
    * Fix parents inverse scale with no use of MVector. (Cause of Dot Product).

This code supports Pylint. Rc file in project.
"""
# pylint: disable=E0401
# E0401 = Supress Maya modules import error

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


class BlendMatrix(om2.MPxNode):
    """ Main class of gfBlendMatrix node. """

    kNODE_NAME = ""
    kNODE_CLASSIFY = ""
    kNODE_ID = ""

    inBlender = om2.MObject()
    inRotInterp = om2.MObject()
    inScaleComp = om2.MObject()
    inMtx1 = om2.MObject()
    inMtx2 = om2.MObject()
    inOri1 = om2.MObject()
    inOri2 = om2.MObject()
    outChain = om2.MObject()
    outVis = om2.MObject()
    outRevVis = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return BlendMatrix()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to BlendMatrix class. Instances of BlendMatrix will use these attributes to create plugs
        for use in the compute() method.
        """
        mAttr = om2.MFnMatrixAttribute()
        nAttr = om2.MFnNumericAttribute()
        uAttr = om2.MFnUnitAttribute()
        eAttr = om2.MFnEnumAttribute()

        BlendMatrix.inBlender = nAttr.create("blender", "blender", om2.MFnNumericData.kFloat, 0.5)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        BlendMatrix.inRotInterp = eAttr.create("rotationInterpolation", "roti", 0)
        eAttr.addField("Euler Lerp", 0)
        eAttr.addField("Quaternion Slerp", 1)
        INPUT_ATTR(eAttr)

        BlendMatrix.inScaleComp = nAttr.create("scaleCompensation", "sc", om2.MFnNumericData.kBoolean, True)
        INPUT_ATTR(nAttr)

        BlendMatrix.inMtx1 = mAttr.create("matrix1", "mtx1", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        INPUT_ATTR(mAttr)

        BlendMatrix.inMtx2 = mAttr.create("matrix2", "mtx2", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        INPUT_ATTR(mAttr)

        ori1X = uAttr.create("orient1X", "or1x", om2.MFnUnitAttribute.kAngle, 0.0)
        ori1Y = uAttr.create("orient1Y", "or1y", om2.MFnUnitAttribute.kAngle, 0.0)
        ori1Z = uAttr.create("orient1Z", "or1z", om2.MFnUnitAttribute.kAngle, 0.0)
        BlendMatrix.inOri1 = nAttr.create("orient1", "or1", ori1X, ori1Y, ori1Z)
        nAttr.array = True
        INPUT_ATTR(nAttr)

        ori2X = uAttr.create("orient2X", "or2x", om2.MFnUnitAttribute.kAngle, 0.0)
        ori2Y = uAttr.create("orient2Y", "or2y", om2.MFnUnitAttribute.kAngle, 0.0)
        ori2Z = uAttr.create("orient2Z", "or2z", om2.MFnUnitAttribute.kAngle, 0.0)
        BlendMatrix.inOri2 = nAttr.create("orient2", "or2", ori2X, ori2Y, ori2Z)
        nAttr.array = True
        INPUT_ATTR(nAttr)

        BlendMatrix.outChain = mAttr.create("outChain", "oc", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        OUTPUT_ATTR(mAttr)

        BlendMatrix.outVis = nAttr.create("visibility", "vis", om2.MFnNumericData.kBoolean, True)
        OUTPUT_ATTR(nAttr)

        BlendMatrix.outRevVis = nAttr.create("reverseVisibility", "rvis", om2.MFnNumericData.kBoolean, False)
        OUTPUT_ATTR(nAttr)

        BlendMatrix.addAttribute(BlendMatrix.inBlender)
        BlendMatrix.addAttribute(BlendMatrix.inRotInterp)
        BlendMatrix.addAttribute(BlendMatrix.inScaleComp)
        BlendMatrix.addAttribute(BlendMatrix.inMtx1)
        BlendMatrix.addAttribute(BlendMatrix.inMtx2)
        BlendMatrix.addAttribute(BlendMatrix.inOri1)
        BlendMatrix.addAttribute(BlendMatrix.inOri2)
        BlendMatrix.addAttribute(BlendMatrix.outChain)
        BlendMatrix.addAttribute(BlendMatrix.outVis)
        BlendMatrix.addAttribute(BlendMatrix.outRevVis)

        BlendMatrix.attributeAffects(BlendMatrix.inBlender, BlendMatrix.outChain)
        BlendMatrix.attributeAffects(BlendMatrix.inRotInterp, BlendMatrix.outChain)
        BlendMatrix.attributeAffects(BlendMatrix.inScaleComp, BlendMatrix.outChain)
        BlendMatrix.attributeAffects(BlendMatrix.inMtx1, BlendMatrix.outChain)
        BlendMatrix.attributeAffects(BlendMatrix.inMtx2, BlendMatrix.outChain)
        BlendMatrix.attributeAffects(BlendMatrix.inOri1, BlendMatrix.outChain)
        BlendMatrix.attributeAffects(BlendMatrix.inOri2, BlendMatrix.outChain)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=R0201

        # Get Transformation Data
        mtx1Handle = dataBlock.inputArrayValue(BlendMatrix.inMtx1)
        mtx2Handle = dataBlock.inputArrayValue(BlendMatrix.inMtx2)
        ori1Handle = dataBlock.inputArrayValue(BlendMatrix.inOri1)
        ori2Handle = dataBlock.inputArrayValue(BlendMatrix.inOri2)
        mtx1List = []
        mtx2List = []
        ori1List = []
        ori2List = []
        index = len(mtx1Handle)
        for i in range(index):
            mtx1Handle.jumpToLogicalElement(i)
            mMtx = mtx1Handle.inputValue().asMatrix()
            mtx1List.append(mMtx)
        index = len(mtx2Handle)
        for i in range(index):
            mtx2Handle.jumpToLogicalElement(i)
            mMtx = mtx2Handle.inputValue().asMatrix()
            mtx2List.append(mMtx)
        index = len(ori1Handle)
        for i in range(index):
            ori1Handle.jumpToLogicalElement(i)
            eOri1 = om2.MEulerRotation(ori1Handle.inputValue().asVector())
            ori1List.append(eOri1)
        index = len(ori2Handle)
        for i in range(index):
            ori2Handle.jumpToLogicalElement(i)
            eOri2 = om2.MEulerRotation(ori2Handle.inputValue().asVector())
            ori2List.append(eOri2)

        # Perform Blend
        blender = dataBlock.inputValue(BlendMatrix.inBlender).asFloat()
        rotInterp = dataBlock.inputValue(BlendMatrix.inRotInterp).asShort()
        scaleComp = dataBlock.inputValue(BlendMatrix.inScaleComp).asBool()
        outList = []
        minPlug = min(min(len(mtx1List), len(mtx2List)), len(ori1List), len(ori2List))
        for i in range(minPlug):
            mtxFn1 = om2.MTransformationMatrix(mtx1List[i])
            mtxFn2 = om2.MTransformationMatrix(mtx2List[i])

            # Scale
            vSca1 = om2.MVector(mtxFn1.scale(om2.MSpace.kTransform))
            vSca2 = om2.MVector(mtxFn2.scale(om2.MSpace.kTransform))
            vOutSca = (1.0 - blender) * vSca1 + blender * vSca2
            mOutSca = om2.MMatrix()
            mOutSca[0] = vOutSca.x
            mOutSca[5] = vOutSca.y
            mOutSca[10] = vOutSca.z

            # Scale Compensation
            parInvSca1 = [1.0, 1.0, 1.0]
            parInvSca2 = [1.0, 1.0, 1.0]
            if scaleComp is True:
                if i > 0:
                    mParSca1 = om2.MTransformationMatrix(mtx1List[i-1])
                    mParSca2 = om2.MTransformationMatrix(mtx2List[i-1])
                    parSca1 = mParSca1.scale(om2.MSpace.kTransform)
                    parSca2 = mParSca2.scale(om2.MSpace.kTransform)
                    parInvSca1 = [1.0 / parSca1[0], 1.0 / parSca1[1], 1.0 / parSca1[2]]
                    parInvSca2 = [1.0 / parSca2[0], 1.0 / parSca2[1], 1.0 / parSca2[2]]

            # Rotation
            eOri1 = ori1List[i].invertIt()
            mtxFn1.rotateBy(eOri1, om2.MSpace.kTransform)
            eRot1 = mtxFn1.rotation(asQuaternion=False)
            eOri2 = ori2List[i].invertIt()
            mtxFn2.rotateBy(eOri2, om2.MSpace.kTransform)
            eRot2 = mtxFn2.rotation(asQuaternion=False)

            vRot1 = om2.MVector(eRot1.x * parInvSca1[0], eRot1.y * parInvSca1[1], eRot1.z * parInvSca1[2])
            vRot2 = om2.MVector(eRot2.x * parInvSca2[0], eRot2.y * parInvSca2[1], eRot2.z * parInvSca2[2])
            if rotInterp == 0:
                vOutRot = (1.0 - blender) * vRot1 + blender * vRot2
                eRot = om2.MEulerRotation(vOutRot.x, vOutRot.y, vOutRot.z)
            else:
                qRot1 = eRot1.asQuaternion().normalizeIt()
                qRot2 = eRot2.asQuaternion().normalizeIt()
                eRot = om2.MQuaternion.slerp(qRot1, qRot2, blender).asEulerRotation()
            mtxFn = om2.MTransformationMatrix(om2.MMatrix())
            mtxFn.setRotation(eRot)
            mOutRot = mtxFn.asMatrix()

            # Translation
            vTrans1 = om2.MVector(mtx1List[i][12], mtx1List[i][13], mtx1List[i][14])
            vTrans2 = om2.MVector(mtx2List[i][12], mtx2List[i][13], mtx2List[i][14])
            vOutTrans = (1.0 - blender) * vTrans1 + blender * vTrans2
            mOutTrans = om2.MMatrix()
            mOutTrans[12] = vOutTrans.x
            mOutTrans[13] = vOutTrans.y
            mOutTrans[14] = vOutTrans.z

            # Output Matrix
            mOut = mOutSca * mOutRot * mOutTrans
            outList.append(mOut)

        # Output Transforms
        outChainHandle = dataBlock.outputArrayValue(BlendMatrix.outChain)
        index = len(outChainHandle)
        for i in range(index):
            outChainHandle.jumpToLogicalElement(i)
            resultHdle = outChainHandle.outputValue()
            if i < index and i < len(outList):
                resultHdle.setMMatrix(outList[i])
            else:
                resultHdle.setMMatrix(om2.MMatrix())

        outChainHandle.setAllClean()
