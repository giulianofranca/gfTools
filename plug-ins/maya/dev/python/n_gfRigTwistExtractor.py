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
    * https://en.wikipedia.org/wiki/Quaternion
    * https://learn.foundry.com/modo/content/help/pages/animation/modifiers/matrix_modifiers.html
    * https://bindpose.com/maya-matrix-nodes-part-2-node-based-matrix-twist-calculator/

This code supports Pylint. Rc file in project.
"""
import maya.api._OpenMaya_py2 as om2

kPI = 3.1415926535897932384626433832795


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

    inRotation = om2.MObject()
    inRotationOrder = om2.MObject()
    inUseUpVec = om2.MObject()
    inUpVec = om2.MObject()
    inInvTwist = om2.MObject()
    inRevDist = om2.MObject()
    outTwist = om2.MObject()
    outTwistDist = om2.MObject()

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
        uAttr = om2.MFnUnitAttribute()
        nAttr = om2.MFnNumericAttribute()
        eAttr = om2.MFnEnumAttribute()

        rotX = uAttr.create("rotationX", "rotx", om2.MFnUnitAttribute.kAngle, 0.0)
        rotY = uAttr.create("rotationY", "roty", om2.MFnUnitAttribute.kAngle, 0.0)
        rotZ = uAttr.create("rotationZ", "rotz", om2.MFnUnitAttribute.kAngle, 0.0)
        TwistExtractor.inRotation = nAttr.create("rotation", "rot", rotX, rotY, rotZ)
        INPUT_ATTR(nAttr)

        TwistExtractor.inRotationOrder = eAttr.create("rotationOrder", "roo", 0)
        # eAttr.addField("Twist First (zyx)", 5)
        # eAttr.addField("Twist Last (xyz)", 0)
        # INPUT_ATTR(eAttr)
        eAttr.addField("xyz", 0)
        eAttr.addField("yzx", 1)
        eAttr.addField("zxy", 2)
        eAttr.addField("xzy", 3)
        eAttr.addField("yxz", 4)
        eAttr.addField("zyx", 5)
        INPUT_ATTR(eAttr)

        TwistExtractor.inUseUpVec = nAttr.create("useUpVector", "useup", om2.MFnNumericData.kBoolean, False)
        INPUT_ATTR(nAttr)

        TwistExtractor.inUpVec = nAttr.createPoint("upVector", "upVector")
        nAttr.default = (0.0, 1.0, 0.0)
        INPUT_ATTR(nAttr)

        TwistExtractor.inInvTwist = nAttr.create("inverseTwist", "itwist", om2.MFnNumericData.kBoolean, False)
        INPUT_ATTR(nAttr)

        TwistExtractor.inRevDist = nAttr.create("reverseDistribution", "rdist", om2.MFnNumericData.kBoolean, False)
        INPUT_ATTR(nAttr)

        TwistExtractor.outTwist = uAttr.create("twist", "twist", om2.MFnUnitAttribute.kAngle, 0.0)
        OUTPUT_ATTR(uAttr)

        TwistExtractor.outTwistDist = uAttr.create("twistDistribution", "twistd", om2.MFnUnitAttribute.kAngle, 0.0)
        uAttr.array = True
        OUTPUT_ATTR(uAttr)

        TwistExtractor.addAttribute(TwistExtractor.inRotation)
        TwistExtractor.addAttribute(TwistExtractor.inRotationOrder)
        TwistExtractor.addAttribute(TwistExtractor.inUseUpVec)
        TwistExtractor.addAttribute(TwistExtractor.inUpVec)
        TwistExtractor.addAttribute(TwistExtractor.inInvTwist)
        TwistExtractor.addAttribute(TwistExtractor.inRevDist)
        TwistExtractor.addAttribute(TwistExtractor.outTwist)
        TwistExtractor.addAttribute(TwistExtractor.outTwistDist)
        TwistExtractor.attributeAffects(rotX, TwistExtractor.outTwist)
        TwistExtractor.attributeAffects(rotY, TwistExtractor.outTwist)
        TwistExtractor.attributeAffects(rotZ, TwistExtractor.outTwist)
        TwistExtractor.attributeAffects(TwistExtractor.inRotationOrder, TwistExtractor.outTwist)
        TwistExtractor.attributeAffects(TwistExtractor.inUseUpVec, TwistExtractor.outTwist)
        TwistExtractor.attributeAffects(TwistExtractor.inUpVec, TwistExtractor.outTwist)
        TwistExtractor.attributeAffects(TwistExtractor.inInvTwist, TwistExtractor.outTwist)
        TwistExtractor.attributeAffects(rotX, TwistExtractor.outTwistDist)
        TwistExtractor.attributeAffects(rotY, TwistExtractor.outTwistDist)
        TwistExtractor.attributeAffects(rotZ, TwistExtractor.outTwistDist)
        TwistExtractor.attributeAffects(TwistExtractor.inRotationOrder, TwistExtractor.outTwistDist)
        TwistExtractor.attributeAffects(TwistExtractor.inUseUpVec, TwistExtractor.outTwistDist)
        TwistExtractor.attributeAffects(TwistExtractor.inUpVec, TwistExtractor.outTwistDist)
        TwistExtractor.attributeAffects(TwistExtractor.inInvTwist, TwistExtractor.outTwistDist)
        TwistExtractor.attributeAffects(TwistExtractor.inRevDist, TwistExtractor.outTwistDist)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        rotation = dataBlock.inputValue(TwistExtractor.inRotation).asDouble3()
        rotOrder = dataBlock.inputValue(TwistExtractor.inRotationOrder).asShort()
        eRoll = om2.MEulerRotation(rotation, rotOrder)
        useUpObj = dataBlock.inputValue(TwistExtractor.inUseUpVec).asBool()
        revTwist = dataBlock.inputValue(TwistExtractor.inInvTwist).asBool()

        # Non flip ROO = XYZ
        # Not working = XZY
        twistOrder = om2.MEulerRotation.kXYZ
        eRoll.reorderIt(twistOrder)

        # Non-Roll orientation
        mtxFn = om2.MTransformationMatrix()
        mtxFn.rotateBy(eRoll, om2.MSpace.kWorld)
        mRoll = mtxFn.asMatrix()

        qNonRoll = om2.MQuaternion()

        nAim = om2.MVector(mRoll[0], mRoll[1], mRoll[2])
        nAim.normalize()
        nAimAxis = om2.MVector.kXaxisVector
        qAim = om2.MQuaternion(nAimAxis, nAim)
        qNonRoll *= qAim

        if useUpObj:
            vUp = om2.MVector(dataBlock.inputValue(TwistExtractor.inUpVec).asFloat3())
            nNormal = vUp - ((vUp * nAim) * nAim)
            nNormal.normalize()
            nUp = om2.MVector.kYaxisVector.rotateBy(qAim)
            angle = nUp.angle(nNormal)
            qNormal = om2.MQuaternion(angle, nAim)
            if not nNormal.isEquivalent(nUp.rotateBy(qNormal), 1.0e-5):
                angle = 2.0 * kPI - angle
                qNormal = om2.MQuaternion(angle, nAim)
            qNonRoll *= qNormal
        eNonRoll = qNonRoll.asEulerRotation()
        eNonRoll = om2.MEulerRotation(eNonRoll.x, eNonRoll.y, eNonRoll.z, twistOrder)

        # Extract Twist from orientations
        qRoll = eRoll.asQuaternion()
        qExtract180 = qNonRoll * qRoll.inverse()
        eExtract180 = qExtract180.asEulerRotation()
        twist = -eExtract180.x
        if revTwist:
            twist *= -1.0

        # Output Twist
        if plug == TwistExtractor.outTwist:
            outTwistHdle = dataBlock.outputValue(TwistExtractor.outTwist)
            outTwistHdle.setMAngle(om2.MAngle(twist))
            outTwistHdle.setClean()

        # Output Twist Distribution
        if plug == TwistExtractor.outTwistDist:
            invDist = dataBlock.inputValue(TwistExtractor.inRevDist).asBool()
            outTwistDistHdle = dataBlock.outputArrayValue(TwistExtractor.outTwistDist)
            outputs = len(outTwistDistHdle)
            step = twist / (outputs - 1) if outputs > 1 else twist
            outList = []
            outList.extend(range(outputs))
            if not invDist:
                outList.reverse()
            # pylint: disable=consider-using-enumerate
            for i in range(len(outList)):
                outTwistDistHdle.jumpToLogicalElement(i)
                resultHdle = outTwistDistHdle.outputValue()
                result = step * outList[i] if outputs > 1 else twist
                resultHdle.setMAngle(om2.MAngle(result))
            outTwistDistHdle.setAllClean()

        return


# # Working! To be revised later
# qRollHalf = (eRoll * 0.5).asQuaternion()
# qNonRollHalf = (eNonRoll * 0.5).asQuaternion()
# qExtract360 = (qNonRollHalf * qRollHalf) # * qRoll.inverse()
# eExtract360 = qExtract360.asEulerRotation()
# twist = eExtract360.x * 2.0

# mRollHalf = mRoll * 0.5
# mNonRollHalf = mNonRoll * 0.5
# mExtract360 = mNonRollHalf + mRollHalf
# mExtract360 *= mRoll

# qIdentity = om2.MQuaternion()
# qRollHalf = om2.MQuaternion.slerp(qIdentity, qRoll, 0.5)
# qNonRollHalf = om2.MQuaternion.slerp(qIdentity, qNonRoll, 0.5)
# qExtract360 = (qNonRollHalf * qRollHalf) * qRoll.inverse()
# eExtract360 = qExtract360.asEulerRotation()
# twist = -eExtract360.x * 2.0
