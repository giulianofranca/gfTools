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
    Extract a twist channel from an Euler Rotation.

Attributes:
    * Target World Matrix: The world matrix of the target object.
    * Target Parent Inverse Matrix: The world inverse matrix of the parent of the target object.
    * Target Joint Orient: The joint orient of the target object.
    * Use Axis as Aim: Use one of the axis of the target object as aim vector.
    * Aim World Matrix: The world matrix of the aim object.
    * Aim Axis: The specific axis of the target object to be used as aim vector.
    * Out Twist: The output twist channel of the target object.

Todo:
    * Add support to 360 degrees twist extraction.

Sources:
    * https://vimeo.com/149066264
    * https://vimeo.com/316148014
    * https://math.stackexchange.com/questions/162863/how-to-get-a-part-of-a-quaternion-e-g-get-half-of-the-rotation-of-a-quaternion
    * https://math.stackexchange.com/questions/939229/unit-quaternion-to-a-scalar-power
    * https://github.com/Kent-H/blue3D/blob/master/Blue3D/src/blue3D/type/QuaternionF.java

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


class TwistExtractor(om2.MPxNode):
    """ Main class of gfTwistExtractor node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inTargetWorldMtx = om2.MObject()
    inTargetParInvMtx = om2.MObject()
    inTargetJointOrient = om2.MObject()
    inUseAxisAsAim = om2.MObject()
    inAimWorldMatrix = om2.MObject()
    inAimAxis = om2.MObject()
    # inAllow360Deg = om2.MObject()
    outTwistAngle = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return TwistExtractor()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to TwistExtractor class. Instances of TwistExtractor will use these attributes to create plugs
        for use in the compute() method.
        """
        mAttr = om2.MFnMatrixAttribute()
        uAttr = om2.MFnUnitAttribute()
        nAttr = om2.MFnNumericAttribute()
        eAttr = om2.MFnEnumAttribute()

        TwistExtractor.inTargetWorldMtx = mAttr.create("targetWorldMatrix", "twmtx", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        TwistExtractor.inTargetParInvMtx = mAttr.create("targetParentInverseMatrix", "tpim", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        tarJntOriX = uAttr.create("targetJointOrientX", "tjox", om2.MFnUnitAttribute.kAngle, 0.0)
        tarJntOriY = uAttr.create("targetJointOrientY", "tjoy", om2.MFnUnitAttribute.kAngle, 0.0)
        tarJntOriZ = uAttr.create("targetJointOrientZ", "tjoz", om2.MFnUnitAttribute.kAngle, 0.0)
        TwistExtractor.inTargetJointOrient = nAttr.create("targetJointOrient", "tjo", tarJntOriX, tarJntOriY, tarJntOriZ)
        INPUT_ATTR(nAttr)

        TwistExtractor.inUseAxisAsAim = nAttr.create("useAxisAsAim", "useAA", om2.MFnNumericData.kBoolean, False)
        INPUT_ATTR(nAttr)

        TwistExtractor.inAimWorldMatrix = mAttr.create("aimWorldMatrix", "awmtx", om2.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        TwistExtractor.inAimAxis = eAttr.create("aimAxis", "aaxis", 0)
        eAttr.addField("Positive X", 0)
        eAttr.addField("Negative X", 1)
        eAttr.addField("Positive Y", 2)
        eAttr.addField("Negative X", 3)
        eAttr.addField("Positive Z", 4)
        eAttr.addField("Negative X", 5)
        INPUT_ATTR(eAttr)

        # TwistExtractor.inAllow360Deg = nAttr.create("allow360Degrees", "a360", om2.MFnNumericData.kBoolean, False)
        # INPUT_ATTR(nAttr)

        TwistExtractor.outTwistAngle = uAttr.create("outTwist", "twist", om2.MFnUnitAttribute.kAngle, 0.0)
        OUTPUT_ATTR(uAttr)

        TwistExtractor.addAttribute(TwistExtractor.inTargetWorldMtx)
        TwistExtractor.addAttribute(TwistExtractor.inTargetParInvMtx)
        TwistExtractor.addAttribute(TwistExtractor.inTargetJointOrient)
        TwistExtractor.addAttribute(TwistExtractor.inUseAxisAsAim)
        TwistExtractor.addAttribute(TwistExtractor.inAimWorldMatrix)
        TwistExtractor.addAttribute(TwistExtractor.inAimAxis)
        # TwistExtractor.addAttribute(TwistExtractor.inAllow360Deg)
        TwistExtractor.addAttribute(TwistExtractor.outTwistAngle)
        TwistExtractor.attributeAffects(TwistExtractor.inTargetWorldMtx, TwistExtractor.outTwistAngle)
        TwistExtractor.attributeAffects(TwistExtractor.inTargetParInvMtx, TwistExtractor.outTwistAngle)
        TwistExtractor.attributeAffects(TwistExtractor.inTargetJointOrient, TwistExtractor.outTwistAngle)
        TwistExtractor.attributeAffects(TwistExtractor.inUseAxisAsAim, TwistExtractor.outTwistAngle)
        TwistExtractor.attributeAffects(TwistExtractor.inAimWorldMatrix, TwistExtractor.outTwistAngle)
        TwistExtractor.attributeAffects(TwistExtractor.inAimAxis, TwistExtractor.outTwistAngle)
        # TwistExtractor.attributeAffects(TwistExtractor.inAllow360Deg, TwistExtractor.outTwistAngle)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        if plug != TwistExtractor.outTwistAngle:
            return om2.kUnknownParameter

        mTargetW = dataBlock.inputValue(TwistExtractor.inTargetWorldMtx).asMatrix()
        mParentInv = dataBlock.inputValue(TwistExtractor.inTargetParInvMtx).asMatrix()
        eTargetJntOri = om2.MEulerRotation(dataBlock.inputValue(TwistExtractor.inTargetJointOrient).asDouble3())
        useAxis = dataBlock.inputValue(TwistExtractor.inUseAxisAsAim).asBool()
        # allow360 = dataBlock.inputValue(TwistExtractor.inAllow360Deg).asBool()
        outTwistHandle = dataBlock.outputValue(TwistExtractor.outTwistAngle)

        mTargetL = mTargetW * mParentInv
        qTargetJntOri = eTargetJntOri.asQuaternion()

        vTargetPos = om2.MVector(mTargetW[12], mTargetW[13], mTargetW[14])
        if useAxis:
            axis = dataBlock.inputValue(TwistExtractor.inAimAxis).asShort()
            if axis == 0:
                nAim = om2.MVector(mTargetW[0], mTargetW[1], mTargetW[2]).normalize()
            elif axis == 1:
                nAim = -om2.MVector(mTargetW[0], mTargetW[1], mTargetW[2]).normalize()
            elif axis == 2:
                nAim = om2.MVector(mTargetW[4], mTargetW[5], mTargetW[6]).normalize()
            elif axis == 3:
                nAim = -om2.MVector(mTargetW[4], mTargetW[5], mTargetW[6]).normalize()
            elif axis == 4:
                nAim = om2.MVector(mTargetW[8], mTargetW[9], mTargetW[10]).normalize()
            else:
                nAim = -om2.MVector(mTargetW[8], mTargetW[9], mTargetW[10]).normalize()
        else:
            mAimW = dataBlock.inputValue(TwistExtractor.inAimWorldMatrix).asMatrix()
            vAimPos = om2.MVector(mAimW[12], mAimW[13], mAimW[14])
            nAim = vAimPos - vTargetPos
            nAim.normalize()
        nAimAxis = om2.MVector(1.0, 0.0, 0.0)
        nRotAxis = nAimAxis ^ nAim
        angle = nAimAxis.angle(nAim)
        qAim = om2.MQuaternion(angle, nRotAxis)

        mtxFn = om2.MTransformationMatrix(mTargetL)
        qTarget = mtxFn.rotation(asQuaternion=True)
        qTarget *= qTargetJntOri.invertIt()
        qExtract = qAim * qTarget.invertIt()
        # if allow360:
        #     qExtract = om2.MQuaternion.slerp(qAim, qTarget, 0.5)

        eExtract = qExtract.asEulerRotation()
        # twist = om2.MAngle(eExtract.x * 2.0) if allow360 else om2.MAngle(eExtract.x)
        twist = om2.MAngle(eExtract.x)
        outTwistHandle.setMAngle(twist)
        outTwistHandle.setClean()
