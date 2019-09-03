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
    * NDA

This code supports Pylint. Rc file in project.
"""
# pylint: disable=import-error
# import-error = Supress Maya modules import error

import sys
import maya.OpenMaya as om1
import maya.OpenMayaMPx as ompx


def INPUT_ATTR(FNATTR):
    """ Configure a input attribute. """
    # pylint: disable=invalid-name
    FNATTR.setWritable(True)
    FNATTR.setReadable(True)
    FNATTR.setStorable(True)
    FNATTR.setConnectable(True)
    FNATTR.setAffectsWorldSpace(True)


def OUTPUT_ATTR(FNATTR):
    """ Configure a output attribute. """
    # pylint: disable=invalid-name
    FNATTR.setWritable(False)
    FNATTR.setReadable(True)
    FNATTR.setStorable(False)
    FNATTR.setKeyable(False)


class AimTransformMatrix(ompx.MPxTransformationMatrix):
    """ Main class of gfAimTransformMatrix. """
    kMATRIX_ID = om1.MTypeId(0x0012f7c6)

    def __init__(self):
        """ Constructor. """
        ompx.MPxTransformationMatrix.__init__(self)
        self.mInverseParentSpace = om1.MMatrix()
        self.vPos = om1.MFloatVector()
        self.vAim = om1.MFloatVector()
        self.vUp = om1.MFloatVector()

    @staticmethod
    def creator():
        """ Maya creator function. """
        return ompx.asMPxPtr(AimTransformMatrix())

    def asMatrix(self, percent=None):
        """ Find the new object matrix and returns it. """
        # pylint: disable=no-self-use
        if percent is None:
            # return self.matrixFromInternals()
            return om1.MMatrix()
        else:
            # return self.matrixFromInternals()
            return om1.MMatrix()

    def matrixFromInternals(self):
        """ Calculates and returns the result aim matrix. """
        vAt = self.vAim - self.vPos
        vAt.normalize()
        vBinormal = vAt ^ (self.vUp - self.vPos)
        vBinormal.normalize()
        vNormal = vBinormal ^ vAt
        mtx = [vAt.x, vAt.y, vAt.z, 0.0,
               vNormal.x, vNormal.y, vNormal.z, 0.0,
               vBinormal.x, vBinormal.y, vBinormal.z, 0.0,
               self.vPos.x, self.vPos.y, self.vPos.z, 1.0]
        return om1.MMatrix(mtx) * self.mInverseParentSpace


class AimTransform(ompx.MPxTransform):
    """ Main class of gfAimTransform node. """

    kNODE_NAME = "gfTestAimTransform_P"
    kNODE_CLASSIFY = "drawdb/transform"
    kNODE_ID = om1.MTypeId(0x0012f7c5)

    inInvParSpace = om1.MObject()
    inDriverPos = om1.MObject()
    inDriverAt = om1.MObject()
    inDriverUp = om1.MObject()

    def __init__(self, transform=None):
        """ Constructor. """
        if transform is None:
            ompx.MPxTransform.__init__(self)
        else:
            ompx.MPxTransform.__init__(self, transform)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return ompx.asMPxPtr(AimTransform())

    def createTransformationMatrix(self):
        """ Point the result MPxTransformationMatrix. """
        # pylint: disable=no-self-use
        return ompx.asMPxPtr(AimTransformMatrix())

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to AimTransform class. Instances of AimTransform will use these attributes to create plugs
        for use in the compute() method.
        """
        mAttr = om1.MFnMatrixAttribute()

        AimTransform.inInvParSpace = mAttr.create("inverseParentWorldSpace", "ipws", om1.MFnMatrixAttribute.kDouble)
        INPUT_ATTR(mAttr)

        AimTransform.inDriverPos = mAttr.create("driverWorldPosition", "dwp", om1.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        AimTransform.inDriverAt = mAttr.create("driverWorldAt", "dwat", om1.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        AimTransform.inDriverUp = mAttr.create("driverWorldUp", "dwup", om1.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        AimTransform.addAttribute(AimTransform.inInvParSpace)
        AimTransform.addAttribute(AimTransform.inDriverPos)
        AimTransform.addAttribute(AimTransform.inDriverAt)
        AimTransform.addAttribute(AimTransform.inDriverUp)

        AimTransform.attributeAffects(AimTransform.inInvParSpace, AimTransform.matrix)
        AimTransform.attributeAffects(AimTransform.inDriverPos, AimTransform.matrix)
        AimTransform.attributeAffects(AimTransform.inDriverAt, AimTransform.matrix)
        AimTransform.attributeAffects(AimTransform.inDriverUp, AimTransform.matrix)

        AimTransform.mustCallValidateAndSet(AimTransform.inInvParSpace)
        AimTransform.mustCallValidateAndSet(AimTransform.inDriverPos)
        AimTransform.mustCallValidateAndSet(AimTransform.inDriverAt)
        AimTransform.mustCallValidateAndSet(AimTransform.inDriverUp)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use, unused-argument
        return True

    def validateAndSetValue(self, plug, handle, context):
        """
        Method to validate attributes for MPxTransformationMatrix.
        This method will only be called by mustCallValidateAndSet setted attributes.
        Context argument is obsolete in C++.
        """
        # pylint: disable=unused-argument
        aimMtxFn = self.transformationMatrixPtr()
        if plug == AimTransform.inDriverPos:
            mDriverPos = handle.asFloatMatrix()
            vDriverPos = om1.MFloatVector(mDriverPos[12], mDriverPos[13], mDriverPos[14])
            aimMtxFn.vPos = vDriverPos
        elif plug in (AimTransform.inDriverAt, AimTransform.inDriverUp):
            dataBlock = self.forceCache()
            mDriverAt = dataBlock.inputValue(AimTransform.inDriverAt).asFloatMatrix()
            mDriverUp = dataBlock.inputValue(AimTransform.inDriverUp).asFloatMatrix()
            vDriverAt = om1.MFloatVector(mDriverAt[12], mDriverAt[13], mDriverAt[14])
            vDriverUp = om1.MFloatVector(mDriverUp[12], mDriverUp[13], mDriverUp[14])
            aimMtxFn.vAim = vDriverAt
            aimMtxFn.vUp = vDriverUp
        elif plug == AimTransform.inInvParSpace:
            aimMtxFn.mInverseParentSpace = handle.asMatrix()
        return True


def initializePlugin(mobject):
    """ Initializes the plug-in. """
    mplugin = ompx.MFnPlugin(mobject)
    try:
        mplugin.registerTransform(AimTransform.kNODE_NAME, AimTransform.kNODE_ID, AimTransform.creator,
                                  AimTransform.initialize, AimTransformMatrix.creator, AimTransformMatrix.kMATRIX_ID,
                                  AimTransform.kNODE_CLASSIFY)
    except:
        sys.stderr.write("Failed to register transform: " +
                         AimTransform.kNODE_NAME)
        raise


def uninitializePlugin(mobject):
    """ Unitializes the plug-in. """
    mplugin = ompx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(AimTransform.kNODE_ID)
    except:
        sys.stderr.write("Failed to register transform: " +
                         AimTransform.kNODE_NAME)
        raise
