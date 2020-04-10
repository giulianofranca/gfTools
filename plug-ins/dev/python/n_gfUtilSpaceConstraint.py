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
    Custom aim constraint. Aim an object to another.

Attributes:
    * Up Vector Type: The type of calculation of the up vector.
    * Offset: The matrix offset between the source and target objects.
    * World Up Vector: The scene world up vector.
    * World Up Matrix: The world matrix of the up object.
    * Target World Matrix: The world matrix of the target object.
    * Target Weight: The weight of calculation.
    * Constraint World Matrix: The world matrix of the constrainted object.
    * Constraint Parent Inverse Matrix: The world inverse matrix of the parent of the constrainted object.
    * Constraint Joint Orient: The joint orient of the constrainted object (if exists).
    * Constraint Rotate Order: The rotate order of the constrainted object.
    * Constraint Parent Scale: The local scale of the parent of the constrainted object.
    * Out Constraint: The result euler rotation of the constraint.

Todo:
    * NDA

Sources:
    * NDA

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


class SpaceConstraint(om2.MPxNode):
    """ Main class of gfUtilSpaceConstraint node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""
    kCallbackIDs = om2.MCallbackIdArray()
    kCallbackNodes = om2.MObjectArray()

    inSpace = om2.MObject()
    inOffset = om2.MObject()
    inOffsetMatches = om2.MObject()
    inTarget = om2.MObject()
    inAutoFillOff = om2.MObject()
    inSpaceMatch = om2.MObject()
    outConstTrans = om2.MObject()
    outConstRot = om2.MObject()
    outConstSca = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)
        self.lastSpace = 0
        self.constraintObject = None

    @staticmethod
    def creator():
        """ Maya creator function. """
        return SpaceConstraint()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to SpaceConstraint class. Instances of SpaceConstraint will use these attributes to create plugs
        for use in the compute() method.
        """
        mAttr = om2.MFnMatrixAttribute()
        nAttr = om2.MFnNumericAttribute()
        uAttr = om2.MFnUnitAttribute()

        SpaceConstraint.inSpace = nAttr.create("space", "space", om2.MFnNumericData.kShort, 0)
        nAttr.setMin(0)
        INPUT_ATTR(nAttr)

        SpaceConstraint.inOffset = mAttr.create("offset", "offset", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        INPUT_ATTR(mAttr)

        SpaceConstraint.inOffsetMatches = mAttr.create("offsetMatch", "offm", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        INPUT_ATTR(mAttr)
        mAttr.keyable = False

        SpaceConstraint.inTarget = mAttr.create("target", "target", om2.MFnMatrixAttribute.kDouble)
        mAttr.array = True
        INPUT_ATTR(mAttr)

        SpaceConstraint.inAutoFillOff = nAttr.create("autoFillOffsets", "afoff", om2.MFnNumericData.kBoolean, True)
        INPUT_ATTR(nAttr)

        SpaceConstraint.inSpaceMatch = nAttr.create("spaceMatch", "spaceMatch", om2.MFnNumericData.kBoolean, True)
        INPUT_ATTR(nAttr)

        SpaceConstraint.outConstTrans = nAttr.createPoint("constraintTranslate", "ctrans")
        OUTPUT_ATTR(nAttr)

        rotX = uAttr.create("constraintRotateX", "crotx", om2.MFnUnitAttribute.kAngle, 0.0)
        rotY = uAttr.create("constraintRotateY", "croty", om2.MFnUnitAttribute.kAngle, 0.0)
        rotZ = uAttr.create("constraintRotateZ", "crotz", om2.MFnUnitAttribute.kAngle, 0.0)
        SpaceConstraint.outConstRot = nAttr.create("constraintRotate", "crot", rotX, rotY, rotZ)
        OUTPUT_ATTR(nAttr)

        SpaceConstraint.outConstSca = nAttr.createPoint("constraintScale", "csca")
        nAttr.default = (1.0, 1.0, 1.0)
        OUTPUT_ATTR(nAttr)

        SpaceConstraint.addAttribute(SpaceConstraint.inSpace)
        SpaceConstraint.addAttribute(SpaceConstraint.inAutoFillOff)
        SpaceConstraint.addAttribute(SpaceConstraint.inSpaceMatch)
        SpaceConstraint.addAttribute(SpaceConstraint.inOffset)
        SpaceConstraint.addAttribute(SpaceConstraint.inOffsetMatches)
        SpaceConstraint.addAttribute(SpaceConstraint.inTarget)
        SpaceConstraint.addAttribute(SpaceConstraint.outConstTrans)
        SpaceConstraint.addAttribute(SpaceConstraint.outConstRot)
        SpaceConstraint.addAttribute(SpaceConstraint.outConstSca)
        SpaceConstraint.attributeAffects(SpaceConstraint.inSpace, SpaceConstraint.outConstTrans)
        SpaceConstraint.attributeAffects(SpaceConstraint.inOffset, SpaceConstraint.outConstTrans)
        SpaceConstraint.attributeAffects(SpaceConstraint.inOffsetMatches, SpaceConstraint.outConstTrans)
        SpaceConstraint.attributeAffects(SpaceConstraint.inTarget, SpaceConstraint.outConstTrans)
        SpaceConstraint.attributeAffects(SpaceConstraint.inSpace, SpaceConstraint.outConstRot)
        SpaceConstraint.attributeAffects(SpaceConstraint.inOffset, SpaceConstraint.outConstRot)
        SpaceConstraint.attributeAffects(SpaceConstraint.inOffsetMatches, SpaceConstraint.outConstRot)
        SpaceConstraint.attributeAffects(SpaceConstraint.inTarget, SpaceConstraint.outConstRot)
        SpaceConstraint.attributeAffects(SpaceConstraint.inSpace, rotX)
        SpaceConstraint.attributeAffects(SpaceConstraint.inOffset, rotX)
        SpaceConstraint.attributeAffects(SpaceConstraint.inOffsetMatches, rotX)
        SpaceConstraint.attributeAffects(SpaceConstraint.inTarget, rotX)
        SpaceConstraint.attributeAffects(SpaceConstraint.inSpace, rotY)
        SpaceConstraint.attributeAffects(SpaceConstraint.inOffset, rotY)
        SpaceConstraint.attributeAffects(SpaceConstraint.inOffsetMatches, rotY)
        SpaceConstraint.attributeAffects(SpaceConstraint.inTarget, rotY)
        SpaceConstraint.attributeAffects(SpaceConstraint.inSpace, rotZ)
        SpaceConstraint.attributeAffects(SpaceConstraint.inOffset, rotZ)
        SpaceConstraint.attributeAffects(SpaceConstraint.inOffsetMatches, rotZ)
        SpaceConstraint.attributeAffects(SpaceConstraint.inTarget, rotZ)
        SpaceConstraint.attributeAffects(SpaceConstraint.inSpace, SpaceConstraint.outConstSca)
        SpaceConstraint.attributeAffects(SpaceConstraint.inOffset, SpaceConstraint.outConstSca)
        SpaceConstraint.attributeAffects(SpaceConstraint.inOffsetMatches, SpaceConstraint.outConstSca)
        SpaceConstraint.attributeAffects(SpaceConstraint.inTarget, SpaceConstraint.outConstSca)

    def postConstructor(self):
        """ Post Constructor. """
        thisMob = self.thisMObject()

        # Add space match callback
        callback = om2.MNodeMessage.addAttributeChangedCallback(thisMob, SpaceConstraint.spaceMatchCallback, self)
        SpaceConstraint.kCallbackIDs.append(callback)
        SpaceConstraint.kCallbackNodes.append(thisMob)
        om2.MGlobal.displayInfo("Node callback: %s" % str(callback))
        om2.MGlobal.displayInfo("All callbacks: %s" % str(SpaceConstraint.kCallbackIDs))

    @staticmethod
    def spaceMatchCallback(msg, plug, otherPlug, clientData):
        """
        The callback function.
        Note: Attribute Changed messages will not be generated while Maya is either in playback or scrubbing modes.
        If you need to do something during playback or scrubbing you will have to register a callback for the
        timeChanged message which is the only message that is sent during those modes.
            * msg [MNodeMessage::AttributeMessage] is the kind of attribute change triggering the callback.
            * plug [MPlug] is the node's plug where the connection changed.
            * otherPlug [MPlug] is the plug opposite the node's plug where the connection changed.
            * clientData [void*] is the user defined data passed to this callback function.
        """
        # pylint: disable=unused-argument
        # 6144 = create input array element.
        # 16385 = connecting output.
        # 16386 = disconnecting output.
        # 2052 = change output in compute method.
        # 2056 = set attribute.
        # 10240 = delete element plug from array attribute.
        # 18434 = disconnect input plug.
        # 18433 = connect input plug.

        thisMob = clientData.thisMObject()
        if not isinstance(clientData, SpaceConstraint):
            # SpaceConstraint *pMesh = static_cast<SpaceConstraint *>(clientData);
            om2.MGlobal.displayError("[gfTools] gfSpaceConstraint don't recognize the clientData for space match callback. Callback functionality skiped.")
            return
        match = om2.MPlug(thisMob, SpaceConstraint.inSpaceMatch).asBool()
        if not match:
            return
        if msg == 2056:
            if plug == SpaceConstraint.inSpace:
                lastValue = clientData.lastSpace
                curValue = plug.asShort()
                # 1- Get the output plug
                allClear = clientData.checkOutputConnections(thisMob)
                # 2- Check if the curValue is valid. If it is not, get the last valid.
                targetPlug = om2.MPlug(thisMob, SpaceConstraint.inTarget)
                offsetPlug = om2.MPlug(thisMob, SpaceConstraint.inOffset)
                offsetMatchPlug = om2.MPlug(thisMob, SpaceConstraint.inOffsetMatches)
                numTarget = targetPlug.numElements() - 1
                if curValue > numTarget:
                    curValue = numTarget
                # 3- If the node have necessary connections...
                if not allClear and (numTarget + 1) > 0:
                    outObj = clientData.constraintObject
                    if outObj.hasFn(om2.MFn.kDagNode):
                        # 4- Get the last world matrix of the target
                        lastOffsetMatchPlug = offsetMatchPlug.elementByLogicalIndex(lastValue)
                        lastOffsetMatchObj = lastOffsetMatchPlug.asMObject()
                        mtxDataFn = om2.MFnMatrixData(lastOffsetMatchObj)
                        mOffsetMatch = mtxDataFn.matrix()
                        lastOffsetPlug = offsetPlug.elementByLogicalIndex(lastValue)
                        lastOffsetObj = lastOffsetPlug.asMObject()
                        mtxDataFn = om2.MFnMatrixData(lastOffsetObj)
                        mOffset = mtxDataFn.matrix()
                        lastTargetPlug = targetPlug.elementByLogicalIndex(lastValue)
                        lastTargetObj = lastTargetPlug.asMObject()
                        mtxDataFn = om2.MFnMatrixData(lastTargetObj)
                        mTarget = mtxDataFn.matrix()
                        mLastOutputW = mOffsetMatch * mOffset * mTarget
                        # 5- Get the current world matrix of the target
                        curTargetPlug = targetPlug.elementByLogicalIndex(curValue)
                        curTargetObj = curTargetPlug.asMObject()
                        mtxDataFn = om2.MFnMatrixData(curTargetObj)
                        mTarget = mtxDataFn.matrix()
                        curOffsetPlug = offsetPlug.elementByLogicalIndex(curValue)
                        curOffsetObj = curOffsetPlug.asMObject()
                        mtxDataFn = om2.MFnMatrixData(curOffsetObj)
                        mOffset = mtxDataFn.matrix()
                        mCurOutputW = mOffset * mTarget
                        # 6- Get the result of the match and set it into the plug
                        mResult = mLastOutputW * mCurOutputW.inverse()
                        curOffsetMatchPlug = offsetMatchPlug.elementByLogicalIndex(curValue)
                        curOffsetMatchHdle = curOffsetMatchPlug.asMDataHandle()
                        curOffsetMatchHdle.setMMatrix(mResult)
                        curOffsetMatchPlug.setMDataHandle(curOffsetMatchHdle)
                        # 7- Clean the offset match plug from last value
                        lastOffsetMatchHdle = lastOffsetMatchPlug.asMDataHandle()
                        lastOffsetMatchHdle.setMMatrix(om2.MMatrix())
                        lastOffsetMatchPlug.setMDataHandle(lastOffsetMatchHdle)
                clientData.lastSpace = curValue

    def checkOutputConnections(self, thisMob):
        """
        Check if any output plug is connected.
        If it have connections, return False and the object connected.
        """
        outPlugArray = om2.MPlugArray([
            om2.MPlug(thisMob, SpaceConstraint.outConstTrans),
            om2.MPlug(thisMob, SpaceConstraint.outConstRot),
            om2.MPlug(thisMob, SpaceConstraint.outConstSca)
        ])
        allClear = True
        for plug in outPlugArray:
            if plug.isConnected:
                allClear = False
                objPlugs = plug.connectedTo(False, True)
                obj = objPlugs[0].node()
                for outPlug in objPlugs:
                    outNode = outPlug.node()
                    if self.constraintObject is not None:
                        if outNode == self.constraintObject:
                            obj = self.constraintObject
                            break
                break
        self.constraintObject = None if allClear else obj
        return allClear

    def autoFillOffset(self, thisMob, index):
        """Auto fill offsets attributes."""
        allClear = self.checkOutputConnections(thisMob)
        obj = self.constraintObject
        if not allClear:
            if obj.hasFn(om2.MFn.kDagNode):
                objPath = om2.MFnDagNode(obj).getPath()
                mOut = objPath.inclusiveMatrix()
                targetPlug = om2.MPlug(thisMob, SpaceConstraint.inTarget)
                curTargetPlug = targetPlug.elementByLogicalIndex(index)
                curTargetObj = curTargetPlug.asMObject()
                mtxDataFn = om2.MFnMatrixData(curTargetObj)
                mTarget = mtxDataFn.matrix()
                mOffset = mOut * mTarget.inverse()
                offsetPlug = om2.MPlug(thisMob, SpaceConstraint.inOffset)
                curOffsetPlug = offsetPlug.elementByLogicalIndex(index)
                curOffsetHdle = curOffsetPlug.asMDataHandle()
                mCurOffset = curOffsetHdle.asMatrix()
                if mCurOffset == om2.MMatrix():
                    curOffsetHdle.setMMatrix(mOffset)
                    curOffsetPlug.setMDataHandle(curOffsetHdle)

    def connectionMade(self, plug, otherPlug, asSrc):
        """This method gets called when connections are made to attributes of this node.
            * plug (MPlug) is the attribute on this node.
            * otherPlug (MPlug) is the attribute on the other node.
            * asSrc (bool) is this plug a source of the connection.
        """
        thisMob = self.thisMObject()
        autoFill = om2.MPlug(thisMob, SpaceConstraint.inAutoFillOff).asBool()
        self.checkOutputConnections(thisMob)
        if plug == SpaceConstraint.inTarget:
            # Create empty slots in offset and offset match attributes if they don't exists.
            targetIndex = plug.logicalIndex()
            offsetPlug = om2.MPlug(thisMob, SpaceConstraint.inOffset)
            curOffPlug = offsetPlug.elementByLogicalIndex(targetIndex)
            curOffPlug.asMDataHandle()
            offsetMatchPlug = om2.MPlug(thisMob, SpaceConstraint.inOffsetMatches)
            curOffMatchPlug = offsetMatchPlug.elementByLogicalIndex(targetIndex)
            curOffMatchPlug.asMDataHandle()
            # Auto fill offset if it has a connected output
            if autoFill:
                self.autoFillOffset(thisMob, targetIndex)
        elif (plug == SpaceConstraint.outConstTrans or
              plug == SpaceConstraint.outConstRot or
              plug == SpaceConstraint.outConstSca):
            # Check if it has a target input connection. If true autoFill the offsets.
            targetPlug = om2.MPlug(thisMob, SpaceConstraint.inTarget)
            numTarget = targetPlug.numElements()
            if numTarget > 0 and autoFill:
                for targetIndex in range(numTarget):
                    self.autoFillOffset(thisMob, targetIndex)
        return om2.MPxNode.connectionMade(self, plug, otherPlug, asSrc)

    def connectionBroken(self, plug, otherPlug, asSrc):
        """This method gets called when connections of this node are broken.
            * plug (MPlug) is the attribute on this node.
            * otherPlug (MPlug) is the attribute on the other node.
            * asSrc (bool) is this plug a source of the connection.
        """
        thisMob = self.thisMObject()
        self.checkOutputConnections(thisMob)
        if plug == SpaceConstraint.outConstTrans:
            pass
        elif plug == SpaceConstraint.outConstRot:
            pass
        elif plug == SpaceConstraint.outConstSca:
            pass
        return om2.MPxNode.connectionBroken(self, plug, otherPlug, asSrc)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        curSpace = dataBlock.inputValue(SpaceConstraint.inSpace).asShort()

        offsetMatchHdle = dataBlock.inputArrayValue(SpaceConstraint.inOffsetMatches)
        offsetHdle = dataBlock.inputArrayValue(SpaceConstraint.inOffset)
        targetHdle = dataBlock.inputArrayValue(SpaceConstraint.inTarget)
        offsetMatchList = []
        offsetList = []
        targetList = []

        for i in range(len(offsetMatchHdle)):
            offsetMatchHdle.jumpToLogicalElement(i)
            mOffMatch = offsetMatchHdle.inputValue().asMatrix()
            offsetMatchList.append(mOffMatch)

        for i in range(len(offsetHdle)):
            offsetHdle.jumpToLogicalElement(i)
            mOff = offsetHdle.inputValue().asMatrix()
            offsetList.append(mOff)

        for i in range(len(targetHdle)):
            targetHdle.jumpToLogicalElement(i)
            mTgt = targetHdle.inputValue().asMatrix()
            targetList.append(mTgt)

        if len(offsetList) == 0 or len(targetList) == 0:
            mResult = om2.MMatrix()
        else:
            minRequired = min(len(offsetList), len(targetList)) - 1
            if curSpace > minRequired:
                curSpace = minRequired
            mResult = offsetMatchList[curSpace] * offsetList[curSpace] * targetList[curSpace]

        mtxFn = om2.MTransformationMatrix(mResult)

        if plug == SpaceConstraint.outConstTrans:
            vTransD = om2.MVector(mResult[12], mResult[13], mResult[14])
            vTrans = om2.MFloatVector(vTransD)
            outTransHdle = dataBlock.outputValue(SpaceConstraint.outConstTrans)
            outTransHdle.setMFloatVector(vTrans)
            outTransHdle.setClean()

        if plug == SpaceConstraint.outConstRot:
            eRot = mtxFn.rotation(asQuaternion=False)
            outRotHdle = dataBlock.outputValue(SpaceConstraint.outConstRot)
            outRotHdle.setMVector(eRot.asVector())
            outRotHdle.setClean()

        if plug == SpaceConstraint.outConstSca:
            outSca = mtxFn.scale(om2.MSpace.kWorld)
            outScaHdle = dataBlock.outputValue(SpaceConstraint.outConstSca)
            outScaHdle.set3Float(outSca[0], outSca[1], outSca[2])
            outScaHdle.setClean()
