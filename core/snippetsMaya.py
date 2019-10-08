"""
Snippets to use in Maya

* http://www.3dtechart.com/tutorials/book/maya_api_overview_pdf
* https://help.autodesk.com/view/MAYAUL/2016/ENU/?guid=__files_GUID_3F96AF53_A47E_4351_A86A_396E7BFD6665_htm
* https://help.autodesk.com/view/MAYAUL/2017/ENU/?guid=__files_Command_plugins_Attaching_a_plugin_to_a_Maya_menu_htm
* https://www.programcreek.com/python/example/107838/maya.cmds.menu
"""
# pylint: disable=undefined-variable

# import math
# import maya.cmds
# import maya.api._OpenMaya_py2 as om2
from gfTools.core import snippets
reload(snippets)


# Create Mother rig
snippets.createChar("mother")
snippets.createMessageAttribute("bindGeometry", "bindGeometry", selList=["mother_C_body_geo"])
snippets.connectAttr("geometry_hrc.bindLayer1", "mother_C_body_geo.bindGeometry")
snippets.createComponent("mother", "leg_L")
bndList = ["leg_L_thigh_bnd", "leg_L_shin_bnd", "leg_L_ankle_bnd", "leg_L_calcaneus_bnd"]
snippets.createMessageAttribute("bindJoint", "bindJoint", selList=bndList)
snippets.getPoleVectorPosition()
cmds.move(5.0, 0.0, 0.0, r=True, os=True, wd=True)          # Move pole vector




















#=====================================================================================================================
snippets.createComponent("Mother", "leg_L")
snippets.createComponent("Mother", "leg_R")
snippets.createComponent("Mother", "spine_C")
snippets.createComponent("Mother", "head_C")
snippets.createComponent("Mother", "arm_L")
snippets.createComponent("Mother", "arm_R")

snippets.getPoleVectorPosition(distance=4.0)
snippets.createObjectOnTransform("transform")
snippets.createObject("unknownTransform", "Test")

thigh = [11.641, 152.323, 1.056]
shin = [13.322, 82.643, 0.026]
ankle = [15.011, 12.811, -2.554]
toe = [15.664, 3.892, 19.558]
legEnd = [15.9, 3.892, 28.692]
dist1 = 69.708
dist2 = 69.9

# snippets.createAttribute("____________SETTINGS", "SETTINGS", snippets.AttributeTypes.kEnum, enum={"__________":0})
# cmds.setAttr("%s.SETTINGS" % om2.MGlobal.getActiveSelectionList().getDagPath(0), 0, l=True)
# snippets.createAttribute("FKIKBlend", "FKIKBlend", snippets.AttributeTypes.kFloat, minVal=[0.0], maxVal=[1.0], default=[0.5])
# snippets.createAttribute("_______________THIGH", "THIGH", snippets.AttributeTypes.kEnum, enum={"__________":0})
# cmds.setAttr("%s.THIGH" % om2.MGlobal.getActiveSelectionList().getDagPath(0), 0, l=True)
# snippets.createAttribute("________________SHIN", "SHIN", snippets.AttributeTypes.kEnum, enum={"__________":0})
# cmds.setAttr("%s.SHIN" % om2.MGlobal.getActiveSelectionList().getDagPath(0), 0, l=True)
# snippets.createAttribute("_________________TOE", "TOE", snippets.AttributeTypes.kEnum, enum={"__________":0})
# cmds.setAttr("%s.TOE" % om2.MGlobal.getActiveSelectionList().getDagPath(0), 0, l=True)
# snippets.createAttribute("stretch", "stretch", snippets.AttributeTypes.kFloat, minVal=[0.001], default=[1.0])
# snippets.createAttribute("squashFB", "squashFB", snippets.AttributeTypes.kFloat, minVal=[0.001], default=[1.0])
# snippets.createAttribute("squashLR", "squashLR", snippets.AttributeTypes.kFloat, minVal=[0.001], default=[1.0])
enum = {
    "xyz": 0,
    "yzx": 1,
    "zxy": 2,
    "xzy": 3,
    "yxz": 4,
    "zyx": 5
}
# snippets.createAttribute("rotationOrder", "rotationOrder", snippets.AttributeTypes.kEnum, enum=enum)


cmds.parent(r=True, s=True)
cmds.setAttr("leg_L_legIK_cNode.pa", cmds.getAttr("leg_L_thighIK_srt.rx"))
cmds.setAttr("multMatrix2.matrixIn[1]", cmds.getAttr("leg_L_ankleIK_srt.worldInverseMatrix"), type="matrix")
cmds.setAttr("multMatrix4.matrixIn[1]", cmds.getAttr("leg_L_toeIK_srt.worldInverseMatrix"), type="matrix")

# snippets.createAttribute("angle", "angle", snippets.AttributeTypes.kAngle)
