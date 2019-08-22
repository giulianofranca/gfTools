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
# pylint: disable=E0401, C0103, undefined-variable
# E0401 = Supress Maya modules import error
# C0103 = Especial cases of constants (non-camelCase)

import sys
import maya.api.OpenMaya as om2

# gfDebug
# import n_gfDebugPv as m_PvDebug
# import n_gfRigBlendMatrix as m_BlendMatrix
# reload(m_BlendMatrix)
# gfRig
import n_gfRigPSDVectorAngle as m_VectorAnglePSD
import n_gfRigIKVChain as m_IKVChainSolver
# gfUtil
import n_gfUtilBlendTransform as m_BlendTransform
import n_gfUtilAimConstraint as m_AimConstraint
import n_gfUtilAngleMath as m_AngularMath
import n_gfUtilAngleScalarMath as m_AngularScalarMath
import n_gfUtilAngleTrigMath as m_AngularTrigMath
import n_gfUtilAngleToDouble as m_AngleToDouble
import n_gfUtilDoubleToAngle as m_DoubleToAngle
# gfRig
reload(m_VectorAnglePSD)
reload(m_IKVChainSolver)
# gfUtil
reload(m_BlendTransform)
reload(m_AimConstraint)
reload(m_AngularMath)
reload(m_AngularScalarMath)
reload(m_AngularTrigMath)
reload(m_AngleToDouble)
reload(m_DoubleToAngle)


def maya_useNewAPI():
    """ Function to Maya recognize the use of the Python API 2.0. """
    # pylint: disable=invalid-name, unnecessary-pass
    pass


def REGISTER_NODE(NODE, PLUGIN):
    """ Register a MPxNode. """
    try:
        PLUGIN.registerNode(NODE.kNODE_NAME, NODE.kNODE_ID, NODE.creator,
                            NODE.initialize, om2.MPxNode.kDependNode, NODE.kNODE_CLASSIFY)
    except:
        sys.stderr.write("Failed to register node: " + NODE.kNODE_NAME)
        raise


def DEREGISTER_NODE(NODE, PLUGIN):
    """ Deregister a MPxNode. """
    try:
        PLUGIN.deregisterNode(NODE.kNODE_ID)
    except:
        sys.stderr.write("Failed to deregister node: " + NODE.kNODE_NAME)
        raise


kAUTHOR = "Giuliano Franca"
kVERSION = "1.0 Pro"
kREQUIRED_API_VERSION = "Any"

# gfDebug
# m_PvDebug.PvDebug.kNODE_NAME = "gfDebugPv_P"
# m_PvDebug.PvDebug.kNODE_CLASSIFY = "utility/general"
# m_PvDebug.PvDebug.kNODE_ID = om2.MTypeId(0x0012f7c0)
# gfRig
# m_BlendMatrix.BlendMatrix.kNODE_NAME = "gfRigBlendMatrix_P"
# m_BlendMatrix.BlendMatrix.kNODE_CLASSIFY = "utility/general"
# m_BlendMatrix.BlendMatrix.kNODE_ID = om2.MTypeId(0x0012f7c2)
m_VectorAnglePSD.VectorAnglePSD.kNODE_NAME = "gfRigPSDVectorAngle_P"
m_VectorAnglePSD.VectorAnglePSD.kNODE_CLASSIFY = "utility/general"
m_VectorAnglePSD.VectorAnglePSD.kNODE_ID = om2.MTypeId(0x0012f7c1)
m_IKVChainSolver.IKVChainSolver.kNODE_NAME = "gfRigIKVChain_P"
m_IKVChainSolver.IKVChainSolver.kNODE_CLASSIFY = "utility/general"
m_IKVChainSolver.IKVChainSolver.kNODE_ID = om2.MTypeId(0x0012f7c2)
# gfUtil
m_BlendTransform.BlendTransform.kNODE_NAME = "gfUtilBlendTransform_P"
m_BlendTransform.BlendTransform.kNODE_CLASSIFY = "utility/general"
m_BlendTransform.BlendTransform.kNODE_ID = om2.MTypeId(0x0012f7c3)
m_AimConstraint.AimConstraint.kNODE_NAME = "gfUtilAimConstraint_P"
m_AimConstraint.AimConstraint.kNODE_CLASSIFY = "utility/general"
m_AimConstraint.AimConstraint.kNODE_ID = om2.MTypeId(0x0012f7c4)
m_AngularMath.AngularMath.kNODE_NAME = "gfUtilAngleMath_P"
m_AngularMath.AngularMath.kNODE_CLASSIFY = "utility/general"
m_AngularMath.AngularMath.kNODE_ID = om2.MTypeId(0x0012f7c5)
m_AngularScalarMath.AngularScalarMath.kNODE_NAME = "gfUtilAngleScalarMath_P"
m_AngularScalarMath.AngularScalarMath.kNODE_CLASSIFY = "utility/general"
m_AngularScalarMath.AngularScalarMath.kNODE_ID = om2.MTypeId(0x0012f7c6)
m_AngularTrigMath.AngularTrigMath.kNODE_NAME = "gfUtilAngleTrigMath_P"
m_AngularTrigMath.AngularTrigMath.kNODE_CLASSIFY = "utility/general"
m_AngularTrigMath.AngularTrigMath.kNODE_ID = om2.MTypeId(0x0012f7c7)
m_AngleToDouble.AngleToDouble.kNODE_NAME = "gfUtilAngleToDouble_P"
m_AngleToDouble.AngleToDouble.kNODE_CLASSIFY = "utility/general"
m_AngleToDouble.AngleToDouble.kNODE_ID = om2.MTypeId(0x0012f7c8)
m_DoubleToAngle.DoubleToAngle.kNODE_NAME = "gfUtilDoubleToAngle_P"
m_DoubleToAngle.DoubleToAngle.kNODE_CLASSIFY = "utility/general"
m_DoubleToAngle.DoubleToAngle.kNODE_ID = om2.MTypeId(0x0012f7c9)


def initializePlugin(mobject):
    """ Initializes the plug-in. """
    mplugin2 = om2.MFnPlugin(mobject, kAUTHOR, kVERSION, kREQUIRED_API_VERSION)

    # REGISTER_NODE(m_PvDebug.PvDebug, mplugin2)
    # REGISTER_NODE(m_BlendMatrix.BlendMatrix, mplugin2)
    REGISTER_NODE(m_VectorAnglePSD.VectorAnglePSD, mplugin2)
    REGISTER_NODE(m_IKVChainSolver.IKVChainSolver, mplugin2)
    REGISTER_NODE(m_BlendTransform.BlendTransform, mplugin2)
    REGISTER_NODE(m_AimConstraint.AimConstraint, mplugin2)
    REGISTER_NODE(m_AngularMath.AngularMath, mplugin2)
    REGISTER_NODE(m_AngularScalarMath.AngularScalarMath, mplugin2)
    REGISTER_NODE(m_AngularTrigMath.AngularTrigMath, mplugin2)
    REGISTER_NODE(m_AngleToDouble.AngleToDouble, mplugin2)
    REGISTER_NODE(m_DoubleToAngle.DoubleToAngle, mplugin2)


def uninitializePlugin(mobject):
    """ Unitializes the plug-in. """
    mplugin2 = om2.MFnPlugin(mobject, kAUTHOR, kVERSION, kREQUIRED_API_VERSION)

    # DEREGISTER_NODE(m_PvDebug.PvDebug, mplugin2)
    # DEREGISTER_NODE(m_BlendMatrix.BlendMatrix, mplugin2)
    DEREGISTER_NODE(m_VectorAnglePSD.VectorAnglePSD, mplugin2)
    DEREGISTER_NODE(m_IKVChainSolver.IKVChainSolver, mplugin2)
    DEREGISTER_NODE(m_BlendTransform.BlendTransform, mplugin2)
    DEREGISTER_NODE(m_AimConstraint.AimConstraint, mplugin2)
    DEREGISTER_NODE(m_AngularMath.AngularMath, mplugin2)
    DEREGISTER_NODE(m_AngularScalarMath.AngularScalarMath, mplugin2)
    DEREGISTER_NODE(m_AngularTrigMath.AngularTrigMath, mplugin2)
    DEREGISTER_NODE(m_AngleToDouble.AngleToDouble, mplugin2)
    DEREGISTER_NODE(m_DoubleToAngle.DoubleToAngle, mplugin2)
