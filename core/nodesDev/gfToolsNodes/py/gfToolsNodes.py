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
# pylint: disable=E0401, C0103, E0602
# E0401 = Supress Maya modules import error
# C0103 = Especial cases of constants (non-camelCase)
# E0602 = Supress Python reload() function error

import sys
import maya.api.OpenMaya as om2

# import n_gfDebugPv as m_PvDebug
import n_gfRigBlendTransform as m_BlendTransform
import n_gfRigBlendMatrix as m_BlendMatrix
import n_gfRigPSD as m_SphericalPSD
import n_gfRigIKVChain as m_IKVChain
import n_gfAimTransform as m_AimTransform
reload(m_BlendMatrix)
reload(m_BlendTransform)
reload(m_IKVChain)
reload(m_AimTransform)


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
kVERSION = "1.0"
kREQUIRED_API_VERSION = "Any"

# m_PvDebug.PvDebug.kNODE_NAME = "gfDebugPv_P"
# m_PvDebug.PvDebug.kNODE_CLASSIFY = "utility/general"
# m_PvDebug.PvDebug.kNODE_ID = om2.MTypeId(0x0012f7c0)
m_BlendTransform.BlendTransform.kNODE_NAME = "gfRigBlendTransform_P"
m_BlendTransform.BlendTransform.kNODE_CLASSIFY = "utility/general"
m_BlendTransform.BlendTransform.kNODE_ID = om2.MTypeId(0x0012f7c1)
m_BlendMatrix.BlendMatrix.kNODE_NAME = "gfRigBlendMatrix_P"
m_BlendMatrix.BlendMatrix.kNODE_CLASSIFY = "utility/general"
m_BlendMatrix.BlendMatrix.kNODE_ID = om2.MTypeId(0x0012f7c2)
m_SphericalPSD.SphericalPSD.kNODE_NAME = "gfRigPSD_P"
m_SphericalPSD.SphericalPSD.kNODE_CLASSIFY = "utility/general"
m_SphericalPSD.SphericalPSD.kNODE_ID = om2.MTypeId(0x0012f7c3)
m_IKVChain.IKVChain.kNODE_NAME = "gfRigIKVChain_P"
m_IKVChain.IKVChain.kNODE_CLASSIFY = "utility/general"
m_IKVChain.IKVChain.kNODE_ID = om2.MTypeId(0x0012f7c4)


def initializePlugin(mobject):
    """ Initializes the plug-in. """
    mplugin2 = om2.MFnPlugin(mobject, kAUTHOR, kVERSION, kREQUIRED_API_VERSION)

    # REGISTER_NODE(m_PvDebug.PvDebug, mplugin2)
    REGISTER_NODE(m_BlendTransform.BlendTransform, mplugin2)
    REGISTER_NODE(m_BlendMatrix.BlendMatrix, mplugin2)
    REGISTER_NODE(m_SphericalPSD.SphericalPSD, mplugin2)
    REGISTER_NODE(m_IKVChain.IKVChain, mplugin2)


def uninitializePlugin(mobject):
    """ Unitializes the plug-in. """
    mplugin2 = om2.MFnPlugin(mobject, kAUTHOR, kVERSION, kREQUIRED_API_VERSION)

    # DEREGISTER_NODE(m_PvDebug.PvDebug, mplugin2)
    DEREGISTER_NODE(m_BlendTransform.BlendTransform, mplugin2)
    DEREGISTER_NODE(m_BlendMatrix.BlendMatrix, mplugin2)
    DEREGISTER_NODE(m_SphericalPSD.SphericalPSD, mplugin2)
    DEREGISTER_NODE(m_IKVChain.IKVChain, mplugin2)
