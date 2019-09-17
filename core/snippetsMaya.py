"""
Snippets to use in Maya
"""
# pylint: disable=undefined-variable

import math
import maya.cmds
import maya.api._OpenMaya_py2 as om2
from gfTools.core import snippets
reload(snippets)


# Create Mother rig
snippets.createChar("Mother")
snippets.createComponent("Mother", "leg_L")
snippets.createComponent("Mother", "leg_R")
snippets.createComponent("Mother", "spine_C")
snippets.createComponent("Mother", "head_C")
snippets.createComponent("Mother", "arm_L")
snippets.createComponent("Mother", "arm_R")

snippets.getPoleVectorPosition(distance=4.0)
snippets.createObjectOnTransform("joint")

thigh = [11.641, 152.323, 1.056]
shin = [13.322, 82.643, 0.026]
ankle = [15.011, 12.811, -2.554]
toe = [15.664, 3.892, 19.558]
legEnd = [15.9, 3.892, 28.692]
dist1 = 69.708
dist2 = 69.9

snippets.createAttribute("____________SETTINGS", "SETTINGS", snippets.AttributeTypes.kEnum, enum={"__________":0})
cmds.setAttr("%s.SETTINGS" % om2.MGlobal.getActiveSelectionList().getDagPath(0), 0, l=True)
snippets.createAttribute("FKIKBlend", "FKIKBlend", snippets.AttributeTypes.kFloat, minVal=[0.0], maxVal=[1.0], default=[0.5])
snippets.createAttribute("_______________THIGH", "THIGH", snippets.AttributeTypes.kEnum, enum={"__________":0})
cmds.setAttr("%s.THIGH" % om2.MGlobal.getActiveSelectionList().getDagPath(0), 0, l=True)
snippets.createAttribute("________________SHIN", "SHIN", snippets.AttributeTypes.kEnum, enum={"__________":0})
cmds.setAttr("%s.SHIN" % om2.MGlobal.getActiveSelectionList().getDagPath(0), 0, l=True)
snippets.createAttribute("_________________TOE", "TOE", snippets.AttributeTypes.kEnum, enum={"__________":0})
cmds.setAttr("%s.TOE" % om2.MGlobal.getActiveSelectionList().getDagPath(0), 0, l=True)
snippets.createAttribute("stretch", "stretch", snippets.AttributeTypes.kFloat, minVal=[0.001], default=[1.0])
snippets.createAttribute("squashFB", "squashFB", snippets.AttributeTypes.kFloat, minVal=[0.001], default=[1.0])
snippets.createAttribute("squashLR", "squashLR", snippets.AttributeTypes.kFloat, minVal=[0.001], default=[1.0])


cmds.parent(r=True, s=True)
cmds.setAttr("leg_L_legIK_cNode.pa", cmds.getAttr("leg_L_thighIK_srt.rx"))
cmds.setAttr("multMatrix2.matrixIn[1]", cmds.getAttr("leg_L_ankleIK_srt.worldInverseMatrix"), type="matrix")
cmds.setAttr("multMatrix4.matrixIn[1]", cmds.getAttr("leg_L_toeIK_srt.worldInverseMatrix"), type="matrix")

snippets.createAttribute("angle", "angle", snippets.AttributeTypes.kAngle)
