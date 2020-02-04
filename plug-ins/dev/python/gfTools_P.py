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

Nodes:
    * gfDebugVector          (MPxLocatorNode): Node to visualize vectors in the viewport.
    * gfPSDVectorAngle       (MPxNode): Calculate weights based on a pose.
    * gfIKVChain             (MPxNode): IK Solver to VChain type of rig.
    * gfBlendTransform       (MPxNode): Blend transformations (SRT) between an array of objects.
    * gfAimConstraint        (MPxNode): Custom aim constraint.
    * gfParentConstraint     (MPxNode): Custom parent contraint.
    * gfAngleMath            (MPxNode): Basic double angle operations.
    * gfAngleScalarMath      (MPxNode): Basic double angle operations with float scalar.
    * gfAngleTrigMath        (MPxNode): Basic double angle trigonometric operations.
    * gfAngleToDouble        (MPxNode): Convert double angle to double.
    * gfDoubleToAngle        (MPxNode): Convert double to double angle.
    * gfEulerMath            (MPxNode): Basic euler rotation operations.
    * gfEulerScalarMath      (MPxNode): Basic euler rotation operations with float scalar.
    * gfEulerToVector        (MPxNode): Convert euler rotation to vector.
    * gfVectorToEuler        (MPxNode): Convert vector to euler rotation.
    * gfDecompRowMatrix      (MPxNode): Decompose all rows of a matrix as vector3.

Todo:
    * NDA

Sources:
    * https://github.com/bungnoid/glTools

This code supports Pylint. Rc file in project.
"""
# pylint: disable=undefined-variable

import sys
import maya.api._OpenMaya_py2 as om2
import maya.api._OpenMayaRender_py2 as omr2

# gfMenu
import m_gfToolsMenu as m_Menu
# gfDebug
import n_gfDebugVector as n_DebugVector
import n_gfDebugMatrix as n_DebugMatrix
# gfRig
import n_gfRigPSDVectorAngle as n_VectorAnglePSD
import n_gfRigIKVChain as n_IKVChainSolver
import n_gfRigHelperJoint as n_HelperJoint
import n_gfRigDistributeAlongSurface as n_DistributeAlongSurface
import n_gfRigTwistExtractor as n_TwistExtractor
import n_gfRigQuadraticCurve as n_QuadraticCurve
# gfUtil
import n_gfUtilBlendTransform as n_BlendTransform
import n_gfUtilAimConstraint as n_AimConstraint
import n_gfUtilParentConstraint as n_ParentConstraint
import n_gfUtilAngleMath as n_AngularMath
import n_gfUtilAngleScalarMath as n_AngularScalarMath
import n_gfUtilAngleTrigMath as n_AngularTrigMath
import n_gfUtilAngleToDouble as n_AngleToDouble
import n_gfUtilDoubleToAngle as n_DoubleToAngle
import n_gfUtilEulerMath as n_EulerMath
import n_gfUtilEulerScalarMath as n_EulerScalarMath
import n_gfUtilEulerToVector as n_EulerToVector
import n_gfUtilVectorToEuler as n_VectorToEuler
import n_gfUtilDecompRowMatrix as n_DecomposeRowMatrix
# gfMenu
reload(m_Menu)
# gfDebug
reload(n_DebugVector)
reload(n_DebugMatrix)
# gfRig
reload(n_VectorAnglePSD)
reload(n_IKVChainSolver)
reload(n_HelperJoint)
reload(n_DistributeAlongSurface)
reload(n_TwistExtractor)
reload(n_QuadraticCurve)
# gfUtil
reload(n_BlendTransform)
reload(n_AimConstraint)
reload(n_ParentConstraint)
reload(n_AngularMath)
reload(n_AngularScalarMath)
reload(n_AngularTrigMath)
reload(n_AngleToDouble)
reload(n_DoubleToAngle)
reload(n_EulerMath)
reload(n_EulerScalarMath)
reload(n_EulerToVector)
reload(n_VectorToEuler)
reload(n_DecomposeRowMatrix)


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

# gfMenu
m_Menu.MainMenu.kMenuName = "gfTools_PMainMenu"
m_Menu.MainMenu.kMenuLabel = "gfTools_P"
# gfDebug
n_DebugVector.DebugVector.kNodeName = "gfDebugVector_P"
n_DebugVector.DebugVector.kNodeClassify = "drawdb/geometry/locator"
n_DebugVector.DebugVector.kNodeRegistrantID = "gfDebugVector_PNodePlugin"
n_DebugVector.DebugVector.kNodeID = om2.MTypeId(0x0012f7c0)
n_DebugMatrix.DebugMatrix.kNodeName = "gfDebugMatrix_P"
n_DebugMatrix.DebugMatrix.kNodeClassify = "drawdb/geometry/locator"
n_DebugMatrix.DebugMatrix.kNodeRegistrantID = "gfDebugMatrix_PNodePlugin"
n_DebugMatrix.DebugMatrix.kNodeID = om2.MTypeId(0x0012f7c1)
# gfRig
n_VectorAnglePSD.VectorAnglePSD.kNodeName = "gfPSDVectorAngle_P"
n_VectorAnglePSD.VectorAnglePSD.kNodeClassify = "utility/general"
n_VectorAnglePSD.VectorAnglePSD.kNodeID = om2.MTypeId(0x0012f7c2)
n_IKVChainSolver.IKVChainSolver.kNodeName = "gfIKVChain_P"
n_IKVChainSolver.IKVChainSolver.kNodeClassify = "utility/general"
n_IKVChainSolver.IKVChainSolver.kNodeID = om2.MTypeId(0x0012f7c3)
n_HelperJoint.HelperJoint.kNodeName = "gfHelperJoint_P"
n_HelperJoint.HelperJoint.kNodeClassify = "utility/general"
n_HelperJoint.HelperJoint.kNodeID = om2.MTypeId(0x0012f7c4)
n_DistributeAlongSurface.DistributeAlongSurface.kNodeName = "gfDistributeAlongSurface_P" # gfSurfaceDistribute_P
n_DistributeAlongSurface.DistributeAlongSurface.kNodeClassify = "utility/general"
n_DistributeAlongSurface.DistributeAlongSurface.kNodeID = om2.MTypeId(0x0012f7c5)
n_TwistExtractor.TwistExtractor.kNodeName = "gfTwistExtractor_P"
n_TwistExtractor.TwistExtractor.kNodeClassify = "utility/general"
n_TwistExtractor.TwistExtractor.kNodeID = om2.MTypeId(0x0012f7c6)
n_QuadraticCurve.QuadraticCurve.kNodeName = "gfQuadraticCurve_P"
n_QuadraticCurve.QuadraticCurve.kNodeClassify = "utility/general"
n_QuadraticCurve.QuadraticCurve.kNodeID = om2.MTypeId(0x0012f7c7)
# gfUtil
n_BlendTransform.BlendTransform.kNodeName = "gfBlendTransforn_P"
n_BlendTransform.BlendTransform.kNodeClassify = "utility/general"
n_BlendTransform.BlendTransform.kNodeID = om2.MTypeId(0x0012f7c8)
n_AimConstraint.AimConstraint.kNodeName = "gfAimConstraint_P"
n_AimConstraint.AimConstraint.kNodeClassify = "utility/general"
n_AimConstraint.AimConstraint.kNodeID = om2.MTypeId(0x0012f7c9)
n_ParentConstraint.ParentConstraint.kNodeName = "gfParentConstraint_P"
n_ParentConstraint.ParentConstraint.kNodeClassify = "utility/general"
n_ParentConstraint.ParentConstraint.kNodeID = om2.MTypeId(0x0012f7ca)
n_AngularMath.AngularMath.kNodeName = "gfAngleMath_P"
n_AngularMath.AngularMath.kNodeClassify = "utility/general"
n_AngularMath.AngularMath.kNodeID = om2.MTypeId(0x0012f7cb)
n_AngularScalarMath.AngularScalarMath.kNodeName = "gfAngleScalarMath_P"
n_AngularScalarMath.AngularScalarMath.kNodeClassify = "utility/general"
n_AngularScalarMath.AngularScalarMath.kNodeID = om2.MTypeId(0x0012f7cc)
n_AngularTrigMath.AngularTrigMath.kNodeName = "gfAngleTrigMath_P"
n_AngularTrigMath.AngularTrigMath.kNodeClassify = "utility/general"
n_AngularTrigMath.AngularTrigMath.kNodeID = om2.MTypeId(0x0012f7cd)
n_AngleToDouble.AngleToDouble.kNodeName = "gfAngleToDouble_P"
n_AngleToDouble.AngleToDouble.kNodeClassify = "utility/general"
n_AngleToDouble.AngleToDouble.kNodeID = om2.MTypeId(0x0012f7ce)
n_DoubleToAngle.DoubleToAngle.kNodeName = "gfDoubleToAngle_P"
n_DoubleToAngle.DoubleToAngle.kNodeClassify = "utility/general"
n_DoubleToAngle.DoubleToAngle.kNodeID = om2.MTypeId(0x0012f7cf)
n_EulerMath.EulerMath.kNodeName = "gfEulerMath_P"
n_EulerMath.EulerMath.kNodeClassify = "utility/general"
n_EulerMath.EulerMath.kNodeID = om2.MTypeId(0x0012f7d0)
n_EulerScalarMath.EulerScalarMath.kNodeName = "gfEulerScalarMath_P"
n_EulerScalarMath.EulerScalarMath.kNodeClassify = "utility/general"
n_EulerScalarMath.EulerScalarMath.kNodeID = om2.MTypeId(0x0012f7d1)
n_EulerToVector.EulerToVector.kNodeName = "gfEulerToVector_P"
n_EulerToVector.EulerToVector.kNodeClassify = "utility/general"
n_EulerToVector.EulerToVector.kNodeID = om2.MTypeId(0x0012f7d2)
n_VectorToEuler.VectorToEuler.kNodeName = "gfVectorToEuler_P"
n_VectorToEuler.VectorToEuler.kNodeClassify = "utility/general"
n_VectorToEuler.VectorToEuler.kNodeID = om2.MTypeId(0x0012f7d3)
n_DecomposeRowMatrix.DecomposeRowMatrix.kNodeName = "gfDecompRowMtx_P"
n_DecomposeRowMatrix.DecomposeRowMatrix.kNodeClassify = "utility/general"
n_DecomposeRowMatrix.DecomposeRowMatrix.kNodeID = om2.MTypeId(0x0012f7d4)


def initializePlugin(mobject):
    """ Initializes the plug-in. """
    mplugin2 = om2.MFnPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion)

    REGISTER_LOCATOR_NODE(n_DebugVector.DebugVector, mplugin2, n_DebugVector.DebugVectorDrawOverride)
    REGISTER_LOCATOR_NODE(n_DebugMatrix.DebugMatrix, mplugin2, n_DebugMatrix.DebugMatrixDrawOverride)
    REGISTER_NODE(n_VectorAnglePSD.VectorAnglePSD, mplugin2)
    REGISTER_NODE(n_IKVChainSolver.IKVChainSolver, mplugin2)
    REGISTER_NODE(n_HelperJoint.HelperJoint, mplugin2)
    REGISTER_NODE(n_DistributeAlongSurface.DistributeAlongSurface, mplugin2)
    REGISTER_NODE(n_TwistExtractor.TwistExtractor, mplugin2)
    REGISTER_NODE(n_QuadraticCurve.QuadraticCurve, mplugin2)
    REGISTER_NODE(n_BlendTransform.BlendTransform, mplugin2)
    REGISTER_NODE(n_AimConstraint.AimConstraint, mplugin2)
    REGISTER_NODE(n_ParentConstraint.ParentConstraint, mplugin2)
    REGISTER_NODE(n_AngularMath.AngularMath, mplugin2)
    REGISTER_NODE(n_AngularScalarMath.AngularScalarMath, mplugin2)
    REGISTER_NODE(n_AngularTrigMath.AngularTrigMath, mplugin2)
    REGISTER_NODE(n_AngleToDouble.AngleToDouble, mplugin2)
    REGISTER_NODE(n_DoubleToAngle.DoubleToAngle, mplugin2)
    REGISTER_NODE(n_EulerMath.EulerMath, mplugin2)
    REGISTER_NODE(n_EulerScalarMath.EulerScalarMath, mplugin2)
    REGISTER_NODE(n_EulerToVector.EulerToVector, mplugin2)
    REGISTER_NODE(n_VectorToEuler.VectorToEuler, mplugin2)
    REGISTER_NODE(n_DecomposeRowMatrix.DecomposeRowMatrix, mplugin2)
    # m_Menu.MainMenu.loadMenu()


def uninitializePlugin(mobject):
    """ Unitializes the plug-in. """
    mplugin2 = om2.MFnPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion)

    DEREGISTER_LOCATOR_NODE(n_DebugVector.DebugVector, mplugin2)
    DEREGISTER_LOCATOR_NODE(n_DebugMatrix.DebugMatrix, mplugin2)
    DEREGISTER_NODE(n_VectorAnglePSD.VectorAnglePSD, mplugin2)
    DEREGISTER_NODE(n_IKVChainSolver.IKVChainSolver, mplugin2)
    DEREGISTER_NODE(n_HelperJoint.HelperJoint, mplugin2)
    DEREGISTER_NODE(n_DistributeAlongSurface.DistributeAlongSurface, mplugin2)
    DEREGISTER_NODE(n_TwistExtractor.TwistExtractor, mplugin2)
    DEREGISTER_NODE(n_QuadraticCurve.QuadraticCurve, mplugin2)
    DEREGISTER_NODE(n_BlendTransform.BlendTransform, mplugin2)
    DEREGISTER_NODE(n_AimConstraint.AimConstraint, mplugin2)
    DEREGISTER_NODE(n_ParentConstraint.ParentConstraint, mplugin2)
    DEREGISTER_NODE(n_AngularMath.AngularMath, mplugin2)
    DEREGISTER_NODE(n_AngularScalarMath.AngularScalarMath, mplugin2)
    DEREGISTER_NODE(n_AngularTrigMath.AngularTrigMath, mplugin2)
    DEREGISTER_NODE(n_AngleToDouble.AngleToDouble, mplugin2)
    DEREGISTER_NODE(n_DoubleToAngle.DoubleToAngle, mplugin2)
    DEREGISTER_NODE(n_EulerMath.EulerMath, mplugin2)
    DEREGISTER_NODE(n_EulerScalarMath.EulerScalarMath, mplugin2)
    DEREGISTER_NODE(n_EulerToVector.EulerToVector, mplugin2)
    DEREGISTER_NODE(n_VectorToEuler.VectorToEuler, mplugin2)
    DEREGISTER_NODE(n_DecomposeRowMatrix.DecomposeRowMatrix, mplugin2)
    # m_Menu.MainMenu.unloadMenu()
