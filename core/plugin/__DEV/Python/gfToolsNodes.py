# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Maya IDs:
    Prototypes: 0x0012f7c0 - 0x0012f7ff
    Releases: 0x00130d80 - 0x00130e7f

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfRigIKVChain node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.

How to use:
    * Copy and paste this file to a Maya plugins path, default: "C:/Users/<user>/Documents/maya/<version>/plug-ins".
        You can create a "plug-ins" folder if not exists.
    * Open your Maya (same version).
    * Go to Windows > Settings/Preferences > Plug-in Manager.
    * Mark this file as loaded.

Requirements:
    Maya 2017 or above.

Todo:
    * drawdb/geometry/transform

This code supports Pylint. Rc file in project.
"""
# pylint: disable=undefined-variable

import sys
import maya.api._OpenMaya_py2 as om2
import maya.api._OpenMayaRender_py2 as omr2

# gfDebug
import n_gfDebugVector as m_DebugVector
# gfRig
import n_gfRigPSDVectorAngle as m_VectorAnglePSD
import n_gfRigIKVChain as m_IKVChainSolver
# gfUtil
import n_gfUtilBlendTransform as m_BlendTransform
import n_gfUtilAimConstraint as m_AimConstraint
import n_gfUtilParentConstraint as m_ParentConstraint
import n_gfUtilAngleMath as m_AngularMath
import n_gfUtilAngleScalarMath as m_AngularScalarMath
import n_gfUtilAngleTrigMath as m_AngularTrigMath
import n_gfUtilAngleToDouble as m_AngleToDouble
import n_gfUtilDoubleToAngle as m_DoubleToAngle
import n_gfUtilEulerMath as m_EulerMath
import n_gfUtilEulerScalarMath as m_EulerScalarMath
import n_gfUtilEulerToVector as m_EulerToVector
import n_gfUtilVectorToEuler as m_VectorToEuler
import n_gfUtilDecompRowMatrix as m_DecomposeRowMatrix
# gfDebug
reload(m_DebugVector)
# gfRig
reload(m_VectorAnglePSD)
reload(m_IKVChainSolver)
# gfUtil
reload(m_BlendTransform)
reload(m_AimConstraint)
reload(m_ParentConstraint)
reload(m_AngularMath)
reload(m_AngularScalarMath)
reload(m_AngularTrigMath)
reload(m_AngleToDouble)
reload(m_DoubleToAngle)
reload(m_EulerMath)
reload(m_EulerScalarMath)
reload(m_EulerToVector)
reload(m_VectorToEuler)
reload(m_DecomposeRowMatrix)


def maya_useNewAPI():
    """ Function to Maya recognize the use of the Python API 2.0. """
    # pylint: disable=invalid-name, unnecessary-pass
    pass


def REGISTER_NODE(NODE, PLUGIN):
    """ Register a MPxNode. """
    # pylint: disable=invalid-name
    try:
        PLUGIN.registerNode(NODE.kNodeName, NODE.kNodeID, NODE.creator,
                            NODE.initialize, om2.MPxNode.kDependNode, NODE.kNodeClassify)
    except BaseException:
        sys.stderr.write("Failed to register node: %s" % NODE.kNodeName)
        raise

def DEREGISTER_NODE(NODE, PLUGIN):
    """ Deregister a MPxNode. """
    # pylint: disable=invalid-name
    try:
        PLUGIN.deregisterNode(NODE.kNodeID)
    except BaseException:
        sys.stderr.write("Failed to deregister node: %s" % NODE.kNodeName)
        raise

def REGISTER_LOCATOR_NODE(NODE, PLUGIN, DRAWOVERRIDE):
    """ Register a MPxLocatorNode. """
    # pylint: disable=invalid-name
    try:
        PLUGIN.registerNode(NODE.kNodeName, NODE.kNodeID, NODE.creator,
                            NODE.initialize, om2.MPxNode.kLocatorNode, NODE.kNodeClassify)
    except BaseException:
        sys.stderr.write("Failed to register node: %s" % NODE.kNodeName)
        raise

    try:
        omr2.MDrawRegistry.registerDrawOverrideCreator(NODE.kNodeClassify, NODE.kNodeRegistrantID,
                                                       DRAWOVERRIDE.creator)
    except BaseException:
        sys.stderr.write("Failed to register override: %s" % NODE.kNodeName)
        raise

def DEREGISTER_LOCATOR_NODE(NODE, PLUGIN):
    """ Deregister a MPxLocatorNode. """
    # pylint: disable=invalid-name
    try:
        PLUGIN.deregisterNode(NODE.kNodeID)
    except BaseException:
        sys.stderr.write("Failed to deregister node: %s" % NODE.kNodeName)
        raise

    try:
        omr2.MDrawRegistry.deregisterDrawOverrideCreator(NODE.kNodeClassify, NODE.kNodeRegistrantID)
    except BaseException:
        sys.stderr.write("Failed to deregister override: %s" % NODE.kNodeName)
        raise


kAuthor = "Giuliano Franca"
kVersion = "1.0"
kRequiredAPIVersion = "Any"

# gfDebug
m_DebugVector.DebugVector.kNodeName = "gfDebugVector_P"
m_DebugVector.DebugVector.kNodeClassify = "drawdb/geometry/locator"
m_DebugVector.DebugVector.kNodeRegistrantID = "gfDebugVector_PNodePlugin"
m_DebugVector.DebugVector.kNodeID = om2.MTypeId(0x0012f7c0)
# gfRig
m_VectorAnglePSD.VectorAnglePSD.kNodeName = "gfRigPSDVectorAngle_P"
m_VectorAnglePSD.VectorAnglePSD.kNodeClassify = "utility/general"
m_VectorAnglePSD.VectorAnglePSD.kNodeID = om2.MTypeId(0x0012f7c1)
m_IKVChainSolver.IKVChainSolver.kNodeName = "gfRigIKVChain_P"
m_IKVChainSolver.IKVChainSolver.kNodeClassify = "utility/general"
m_IKVChainSolver.IKVChainSolver.kNodeID = om2.MTypeId(0x0012f7c2)
# gfUtil
m_BlendTransform.BlendTransform.kNodeName = "gfUtilBlendTransform_P"
m_BlendTransform.BlendTransform.kNodeClassify = "utility/general"
m_BlendTransform.BlendTransform.kNodeID = om2.MTypeId(0x0012f7c3)
m_AimConstraint.AimConstraint.kNodeName = "gfUtilAimConstraint_P"
m_AimConstraint.AimConstraint.kNodeClassify = "utility/general"
m_AimConstraint.AimConstraint.kNodeID = om2.MTypeId(0x0012f7c4)
m_ParentConstraint.ParentConstraint.kNodeName = "gfUtilParentConstraint_P"
m_ParentConstraint.ParentConstraint.kNodeClassify = "utility/general"
m_ParentConstraint.ParentConstraint.kNodeID = om2.MTypeId(0x0012f7c5)
m_AngularMath.AngularMath.kNodeName = "gfUtilAngleMath_P"
m_AngularMath.AngularMath.kNodeClassify = "utility/general"
m_AngularMath.AngularMath.kNodeID = om2.MTypeId(0x0012f7c6)
m_AngularScalarMath.AngularScalarMath.kNodeName = "gfUtilAngleScalarMath_P"
m_AngularScalarMath.AngularScalarMath.kNodeClassify = "utility/general"
m_AngularScalarMath.AngularScalarMath.kNodeID = om2.MTypeId(0x0012f7c7)
m_AngularTrigMath.AngularTrigMath.kNodeName = "gfUtilAngleTrigMath_P"
m_AngularTrigMath.AngularTrigMath.kNodeClassify = "utility/general"
m_AngularTrigMath.AngularTrigMath.kNodeID = om2.MTypeId(0x0012f7c8)
m_AngleToDouble.AngleToDouble.kNodeName = "gfUtilAngleToDouble_P"
m_AngleToDouble.AngleToDouble.kNodeClassify = "utility/general"
m_AngleToDouble.AngleToDouble.kNodeID = om2.MTypeId(0x0012f7c9)
m_DoubleToAngle.DoubleToAngle.kNodeName = "gfUtilDoubleToAngle_P"
m_DoubleToAngle.DoubleToAngle.kNodeClassify = "utility/general"
m_DoubleToAngle.DoubleToAngle.kNodeID = om2.MTypeId(0x0012f7ca)
m_EulerMath.EulerMath.kNodeName = "gfUtilEulerMath_P"
m_EulerMath.EulerMath.kNodeClassify = "utility/general"
m_EulerMath.EulerMath.kNodeID = om2.MTypeId(0x0012f7cb)
m_EulerScalarMath.EulerScalarMath.kNodeName = "gfUtilEulerScalarMath_P"
m_EulerScalarMath.EulerScalarMath.kNodeClassify = "utility/general"
m_EulerScalarMath.EulerScalarMath.kNodeID = om2.MTypeId(0x0012f7cc)
m_EulerToVector.EulerToVector.kNodeName = "gfUtilEulerToVector_P"
m_EulerToVector.EulerToVector.kNodeClassify = "utility/general"
m_EulerToVector.EulerToVector.kNodeID = om2.MTypeId(0x0012f7cd)
m_VectorToEuler.VectorToEuler.kNodeName = "gfUtilVectorToEuler_P"
m_VectorToEuler.VectorToEuler.kNodeClassify = "utility/general"
m_VectorToEuler.VectorToEuler.kNodeID = om2.MTypeId(0x0012f7ce)
m_DecomposeRowMatrix.DecomposeRowMatrix.kNodeName = "gfUtilDecompRowMtx_P"
m_DecomposeRowMatrix.DecomposeRowMatrix.kNodeClassify = "utility/general"
m_DecomposeRowMatrix.DecomposeRowMatrix.kNodeID = om2.MTypeId(0x0012f7cf)


def initializePlugin(mobject):
    """ Initializes the plug-in. """
    mplugin2 = om2.MFnPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion)

    REGISTER_LOCATOR_NODE(m_DebugVector.DebugVector, mplugin2, m_DebugVector.DebugVectorDrawOverride)
    REGISTER_NODE(m_VectorAnglePSD.VectorAnglePSD, mplugin2)
    REGISTER_NODE(m_IKVChainSolver.IKVChainSolver, mplugin2)
    REGISTER_NODE(m_BlendTransform.BlendTransform, mplugin2)
    REGISTER_NODE(m_AimConstraint.AimConstraint, mplugin2)
    REGISTER_NODE(m_ParentConstraint.ParentConstraint, mplugin2)
    REGISTER_NODE(m_AngularMath.AngularMath, mplugin2)
    REGISTER_NODE(m_AngularScalarMath.AngularScalarMath, mplugin2)
    REGISTER_NODE(m_AngularTrigMath.AngularTrigMath, mplugin2)
    REGISTER_NODE(m_AngleToDouble.AngleToDouble, mplugin2)
    REGISTER_NODE(m_DoubleToAngle.DoubleToAngle, mplugin2)
    REGISTER_NODE(m_EulerMath.EulerMath, mplugin2)
    REGISTER_NODE(m_EulerScalarMath.EulerScalarMath, mplugin2)
    REGISTER_NODE(m_EulerToVector.EulerToVector, mplugin2)
    REGISTER_NODE(m_VectorToEuler.VectorToEuler, mplugin2)
    REGISTER_NODE(m_DecomposeRowMatrix.DecomposeRowMatrix, mplugin2)


def uninitializePlugin(mobject):
    """ Unitializes the plug-in. """
    mplugin2 = om2.MFnPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion)

    DEREGISTER_LOCATOR_NODE(m_DebugVector.DebugVector, mplugin2)
    DEREGISTER_NODE(m_VectorAnglePSD.VectorAnglePSD, mplugin2)
    DEREGISTER_NODE(m_IKVChainSolver.IKVChainSolver, mplugin2)
    DEREGISTER_NODE(m_BlendTransform.BlendTransform, mplugin2)
    DEREGISTER_NODE(m_AimConstraint.AimConstraint, mplugin2)
    DEREGISTER_NODE(m_ParentConstraint.ParentConstraint, mplugin2)
    DEREGISTER_NODE(m_AngularMath.AngularMath, mplugin2)
    DEREGISTER_NODE(m_AngularScalarMath.AngularScalarMath, mplugin2)
    DEREGISTER_NODE(m_AngularTrigMath.AngularTrigMath, mplugin2)
    DEREGISTER_NODE(m_AngleToDouble.AngleToDouble, mplugin2)
    DEREGISTER_NODE(m_DoubleToAngle.DoubleToAngle, mplugin2)
    DEREGISTER_NODE(m_EulerMath.EulerMath, mplugin2)
    DEREGISTER_NODE(m_EulerScalarMath.EulerScalarMath, mplugin2)
    DEREGISTER_NODE(m_EulerToVector.EulerToVector, mplugin2)
    DEREGISTER_NODE(m_VectorToEuler.VectorToEuler, mplugin2)
    DEREGISTER_NODE(m_DecomposeRowMatrix.DecomposeRowMatrix, mplugin2)
