# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfUtilBlendTransform node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.

Requirements:
    Maya 2017 or above.

Todo:
    * NDA

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


class BlendTransform(om2.MPxNode):
    """ Main class of gfUtilBlendTransform node. """

    kNODE_NAME = ""
    kNODE_CLASSIFY = ""
    kNODE_ID = ""

    inBlender = om2.MObject()
    inRotInterp = om2.MObject()
    inTrans1 = om2.MObject()
    inRot1 = om2.MObject()
    inSca1 = om2.MObject()
    inTransform1 = om2.MObject()
    inTrans2 = om2.MObject()
    inRot2 = om2.MObject()
    inSca2 = om2.MObject()
    inTransform2 = om2.MObject()
    outTrans = om2.MObject()
    outRot = om2.MObject()
    outSca = om2.MObject()
    outVis = om2.MObject()
    outRevVis = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return BlendTransform()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to BlendTransform class. Instances of BlendTransform will use these attributes to create plugs
        for use in the compute() method.
        """
        nAttr = om2.MFnNumericAttribute()
        uAttr = om2.MFnUnitAttribute()
        cAttr = om2.MFnCompoundAttribute()
        eAttr = om2.MFnEnumAttribute()

        BlendTransform.inBlender = nAttr.create("blender", "blender", om2.MFnNumericData.kFloat, 0.5)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        BlendTransform.inRotInterp = eAttr.create("rotationInterpolation", "roti", 0)
        eAttr.addField("Euler Lerp", 0)
        eAttr.addField("Quaternion Slerp", 1)
        INPUT_ATTR(eAttr)

        BlendTransform.inTrans1 = nAttr.createPoint("translate1", "t1")
        nAttr.array = True
        INPUT_ATTR(nAttr)

        rot1X = uAttr.create("rotate1X", "ro1x", om2.MFnUnitAttribute.kAngle, 0.0)
        rot1Y = uAttr.create("rotate1Y", "ro1y", om2.MFnUnitAttribute.kAngle, 0.0)
        rot1Z = uAttr.create("rotate1Z", "ro1z", om2.MFnUnitAttribute.kAngle, 0.0)
        BlendTransform.inRot1 = nAttr.create("rotate1", "ro1", rot1X, rot1Y, rot1Z)
        nAttr.array = True
        INPUT_ATTR(nAttr)

        BlendTransform.inSca1 = nAttr.createPoint("scale1", "sca1")
        nAttr.array = True
        INPUT_ATTR(nAttr)

        BlendTransform.inTransform1 = cAttr.create("transform1", "tr1")
        cAttr.addChild(BlendTransform.inTrans1)
        cAttr.addChild(BlendTransform.inRot1)
        cAttr.addChild(BlendTransform.inSca1)

        BlendTransform.inTrans2 = nAttr.createPoint("translate2", "t2")
        nAttr.array = True
        INPUT_ATTR(nAttr)

        rot2X = uAttr.create("rotate2X", "ro2x", om2.MFnUnitAttribute.kAngle, 0.0)
        rot2Y = uAttr.create("rotate2Y", "ro2y", om2.MFnUnitAttribute.kAngle, 0.0)
        rot2Z = uAttr.create("rotate2Z", "ro2z", om2.MFnUnitAttribute.kAngle, 0.0)
        BlendTransform.inRot2 = nAttr.create("rotate2", "ro2", rot2X, rot2Y, rot2Z)
        nAttr.array = True
        INPUT_ATTR(nAttr)

        BlendTransform.inSca2 = nAttr.createPoint("scale2", "sca2")
        nAttr.array = True
        INPUT_ATTR(nAttr)

        BlendTransform.inTransform2 = cAttr.create("transform2", "tr2")
        cAttr.addChild(BlendTransform.inTrans2)
        cAttr.addChild(BlendTransform.inRot2)
        cAttr.addChild(BlendTransform.inSca2)

        BlendTransform.outTrans = nAttr.createPoint("outTranslate", "ot")
        nAttr.array = True
        OUTPUT_ATTR(nAttr)

        oRotX = uAttr.create("outRotateX", "orox", om2.MFnUnitAttribute.kAngle, 0.0)
        oRotY = uAttr.create("outRotateY", "oroy", om2.MFnUnitAttribute.kAngle, 0.0)
        oRotZ = uAttr.create("outRotateZ", "oroz", om2.MFnUnitAttribute.kAngle, 0.0)
        BlendTransform.outRot = nAttr.create("outRotate", "oro", oRotX, oRotY, oRotZ)
        nAttr.array = True
        OUTPUT_ATTR(nAttr)

        BlendTransform.outSca = nAttr.createPoint("outScale", "osca")
        nAttr.array = True
        OUTPUT_ATTR(nAttr)

        BlendTransform.outVis = nAttr.create("visibility", "vis", om2.MFnNumericData.kBoolean, True)
        OUTPUT_ATTR(nAttr)

        BlendTransform.outRevVis = nAttr.create("reverseVisibility", "rvis", om2.MFnNumericData.kBoolean, False)
        OUTPUT_ATTR(nAttr)

        BlendTransform.addAttribute(BlendTransform.inBlender)
        BlendTransform.addAttribute(BlendTransform.inRotInterp)
        BlendTransform.addAttribute(BlendTransform.inTransform1)
        BlendTransform.addAttribute(BlendTransform.inTransform2)
        BlendTransform.addAttribute(BlendTransform.outTrans)
        BlendTransform.addAttribute(BlendTransform.outRot)
        BlendTransform.addAttribute(BlendTransform.outSca)
        BlendTransform.addAttribute(BlendTransform.outVis)
        BlendTransform.addAttribute(BlendTransform.outRevVis)

        BlendTransform.attributeAffects(BlendTransform.inBlender, BlendTransform.outTrans)
        BlendTransform.attributeAffects(BlendTransform.inTrans1, BlendTransform.outTrans)
        BlendTransform.attributeAffects(BlendTransform.inTrans2, BlendTransform.outTrans)
        BlendTransform.attributeAffects(BlendTransform.inBlender, BlendTransform.outRot)
        BlendTransform.attributeAffects(BlendTransform.inRotInterp, BlendTransform.outRot)
        BlendTransform.attributeAffects(BlendTransform.inRot1, BlendTransform.outRot)
        BlendTransform.attributeAffects(BlendTransform.inRot2, BlendTransform.outRot)
        BlendTransform.attributeAffects(BlendTransform.inBlender, BlendTransform.outSca)
        BlendTransform.attributeAffects(BlendTransform.inSca1, BlendTransform.outSca)
        BlendTransform.attributeAffects(BlendTransform.inSca2, BlendTransform.outSca)
        BlendTransform.attributeAffects(BlendTransform.inBlender, BlendTransform.outVis)
        BlendTransform.attributeAffects(BlendTransform.inBlender, BlendTransform.outRevVis)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=R0201
        blender = dataBlock.inputValue(BlendTransform.inBlender).asFloat()
        if plug == BlendTransform.outTrans:
            trans1Handle = dataBlock.inputArrayValue(BlendTransform.inTrans1)
            trans2Handle = dataBlock.inputArrayValue(BlendTransform.inTrans2)
            outTransHandle = dataBlock.outputArrayValue(BlendTransform.outTrans)
            outList = []
            for i in range(min(len(trans1Handle), len(trans2Handle))):
                trans1Handle.jumpToLogicalElement(i)
                trans2Handle.jumpToLogicalElement(i)
                vTrans1 = trans1Handle.inputValue().asFloatVector()
                vTrans2 = trans2Handle.inputValue().asFloatVector()
                vOut = (1.0 - blender) * vTrans1 + blender * vTrans2
                outList.append(vOut)
            for i in range(len(outTransHandle)):
                outTransHandle.jumpToLogicalElement(i)
                resultHandle = outTransHandle.outputValue()
                if i < len(outTransHandle) and i < len(outList):
                    resultHandle.setMFloatVector(outList[i])
                else:
                    resultHandle.setMFloatVector(om2.MFloatVector())
            outTransHandle.setAllClean()

        elif plug == BlendTransform.outRot:
            rotInterp = dataBlock.inputValue(BlendTransform.inRotInterp).asShort()
            rot1Handle = dataBlock.inputArrayValue(BlendTransform.inRot1)
            rot2Handle = dataBlock.inputArrayValue(BlendTransform.inRot2)
            outRotHandle = dataBlock.outputArrayValue(BlendTransform.outRot)
            outList = []
            for i in range(min(len(rot1Handle), len(rot2Handle))):
                rot1Handle.jumpToLogicalElement(i)
                rot2Handle.jumpToLogicalElement(i)
                vRot1 = rot1Handle.inputValue().asVector()
                vRot2 = rot2Handle.inputValue().asVector()
                if rotInterp == 0:
                    vOut = (1.0 - blender) * vRot1 + blender * vRot2
                else:
                    qRot1 = om2.MEulerRotation(vRot1).asQuaternion()
                    qRot2 = om2.MEulerRotation(vRot2).asQuaternion()
                    vOut = om2.MQuaternion.slerp(qRot1, qRot2, blender).asEulerRotation().asVector()
                outList.append(vOut)
            for i in range(len(outRotHandle)):
                outRotHandle.jumpToLogicalElement(i)
                resultHandle = outRotHandle.outputValue()
                if i < len(outRotHandle) and i < len(outList):
                    resultHandle.setMVector(outList[i])
                else:
                    resultHandle.setMVector(om2.MVector())
            outRotHandle.setAllClean()

        elif plug == BlendTransform.outSca:
            sca1Handle = dataBlock.inputArrayValue(BlendTransform.inSca1)
            sca2Handle = dataBlock.inputArrayValue(BlendTransform.inSca2)
            outScaHandle = dataBlock.outputArrayValue(BlendTransform.outSca)
            outList = []
            for i in range(min(len(sca1Handle), len(sca2Handle))):
                sca1Handle.jumpToLogicalElement(i)
                sca2Handle.jumpToLogicalElement(i)
                vSca1 = sca1Handle.inputValue().asFloatVector()
                vSca2 = sca2Handle.inputValue().asFloatVector()
                vOut = (1.0 - blender) * vSca1 + blender * vSca2
                outList.append(vOut)
            for i in range(len(outScaHandle)):
                outScaHandle.jumpToLogicalElement(i)
                resultHandle = outScaHandle.outputValue()
                if i < len(outScaHandle) and i < len(outList):
                    resultHandle.setMFloatVector(outList[i])
                else:
                    resultHandle.setMFloatVector(om2.MFloatVector())
            outScaHandle.setAllClean()

        elif plug in (BlendTransform.outVis, BlendTransform.outRevVis):
            outVisHandle = dataBlock.outputValue(BlendTransform.outVis)
            outRevVisHandle = dataBlock.outputValue(BlendTransform.outRevVis)
            vis, revVis = BlendTransform.visibilityCalculation(blender)
            outVisHandle.setBool(vis)
            outRevVisHandle.setBool(revVis)
            outVisHandle.setClean()
            outRevVisHandle.setClean()

    @staticmethod
    def visibilityCalculation(blender):
        """
        Calculate the visibility of the objects based on blender value. Threshold can be changed
        in code to affect the calculation.
        """
        threshold = 0.25
        vis = True
        revVis = False
        if blender <= 0.0 + threshold:
            vis = False
            revVis = True
        elif blender >= 1.0 - threshold:
            vis = True
            revVis = False
        else:
            vis = True
            revVis = True

        return vis, revVis
