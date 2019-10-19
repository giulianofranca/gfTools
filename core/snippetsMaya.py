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
#======================================================================================================
# Componet Left Leg
#======================================================================================================
snippets.createChar("mother")
snippets.createMessageAttribute("bindGeometry", "bindGeometry", selList=["mother_C_body_geo"])
snippets.connectAttr("geometry_hrc.bindLayer1", "mother_C_body_geo.bindGeometry")
snippets.createComponent("mother", "leg_L")
bndList = ["leg_L_thigh_bnd", "leg_L_shin_bnd", "leg_L_ankle_bnd", "leg_L_calcaneus_bnd"]
snippets.createMessageAttribute("bindJoint", "bindJoint", selList=bndList)
snippets.getPoleVectorPosition()
cmds.move(5.0, 0.0, 0.0, r=True, os=True, wd=True)          # Move pole vector
cmds.select("leg_L_thighFK_srt", "leg_L_shinFK_srt", "leg_L_ankleFK_srt", "leg_L_toeFK_srt")
snippets.createObjectOnTransform()
fkControls = ["leg_L_thighFK_ctrl", "leg_L_shinFK_ctrl", "leg_L_ankleFK_ctrl", "leg_L_toeFK_ctrl"]
pvControls = ["leg_L_legPv_ctrl", "leg_L_legSnapPv_ctrl"]
settingsControl = ["leg_L_settings_ctrl"]
snippets.lockAndHideAttributes(fkControls, ["translate", "scale", "shear"])
snippets.lockAndHideAttributes(pvControls, ["rotate", "scale", "shear"])
snippets.lockAndHideAttributes(settingsControl, ["translate", "rotate", "scale", "shear"])
cmds.scale(0.95, 0.95, 0.95, r=True, p=(1.73, 13.6, 0.38))
cmds.scale(1.05, 1.05, 1.05, r=True, p=(1.73, 13.6, 0.38))
snippets.createMessageAttribute("component", "component")
cmds.select("leg_L_legPvPointer_ctrlShape", "leg_L_legPv_ctrl")
cmds.parent(r=True, s=True)
# Create attributes
snippets.createEnumAttribute("LEG", "LEG", {"__________":0}, selList=["leg_L_thighFK_ctrl"])
cmds.setAttr("leg_L_thighFK_ctrl.LEG", 0, l=True)
snippets.createEnumAttribute("THIGH", "THIGH", {"__________":0}, selList=["leg_L_thighFK_ctrl"])
cmds.setAttr("leg_L_thighFK_ctrl.THIGH", 0, l=True)
snippets.createEnumAttribute("SHIN", "SHIN", {"__________":0}, selList=["leg_L_shinFK_ctrl"])
cmds.setAttr("leg_L_shinFK_ctrl.SHIN", 0, l=True)
snippets.createEnumAttribute("FOOT", "FOOT", {"__________":0}, selList=["leg_L_ankleFK_ctrl"])
cmds.setAttr("leg_L_ankleFK_ctrl.FOOT", 0, l=True)
snippets.createEnumAttribute("ANKLE", "ANKLE", {"__________":0}, selList=["leg_L_ankleFK_ctrl"])
cmds.setAttr("leg_L_ankleFK_ctrl.ANKLE", 0, l=True)
snippets.createEnumAttribute("TOE", "TOE", {"__________":0}, selList=["leg_L_toeFK_ctrl"])
cmds.setAttr("leg_L_toeFK_ctrl.TOE", 0, l=True)
snippets.createEnumAttribute("SETTINGS", "SETTINGS", {"__________":0}, selList=["leg_L_settings_ctrl"])
cmds.setAttr("leg_L_settings_ctrl.SETTINGS", 0, l=True)
snippets.createEnumAttribute("PV", "PV", {"__________":0}, selList=["leg_L_legPv_ctrl"])
cmds.setAttr("leg_L_legPv_ctrl.PV", 0, l=True)
snippets.createEnumAttribute("LEG", "LEG", {"__________":0}, selList=["leg_L_legIK_ctrl"])
cmds.setAttr("leg_L_legIK_ctrl.LEG", 0, l=True)
rotOrder = {"xyz":0, "yzx":1, "zxy":2, "xzy":3, "yxz":4, "zyx":5}
snippets.createEnumAttribute("rotateOrderFK", "rotateOrderFK", rotOrder, selList=["leg_L_thighFK_ctrl"])
snippets.createEnumAttribute("rotateOrderIK", "rotateOrderIK", rotOrder, selList=["leg_L_legIK_ctrl"])
snippets.createNumericAttribute("fkikBlend", "fkikBlend", snippets.AttributeTypes.kFloat, 0.0, 1.0, selList=["leg_L_settings_ctrl"])
snippets.createEnumAttribute("spaceSwitch", "spaceSwitch", {"Pelvis":0, "Hip":1, "Root":2, "Global":3}, selList=["leg_L_thighFK_ctrl"])
snippets.createEnumAttribute("spaceSwitch", "spaceSwitch", {"Pelvis":0, "Hip":1, "Root":2, "Global":3}, selList=["leg_L_legIK_ctrl"])
snippets.createNumericAttribute("showGimbalCtrl", "showGimbalCtrl", snippets.AttributeTypes.kBool, selList=["leg_L_thighFK_ctrl"])
snippets.createNumericAttribute("showGimbalCtrl", "showGimbalCtrl", snippets.AttributeTypes.kBool, selList=["leg_L_shinFK_ctrl"])
snippets.createNumericAttribute("showGimbalCtrl", "showGimbalCtrl", snippets.AttributeTypes.kBool, selList=["leg_L_ankleFK_ctrl"])
snippets.createNumericAttribute("showGimbalCtrl", "showGimbalCtrl", snippets.AttributeTypes.kBool, selList=["leg_L_toeFK_ctrl"])
snippets.createNumericAttribute("showGimbalCtrl", "showGimbalCtrl", snippets.AttributeTypes.kBool, selList=["leg_L_legIK_ctrl"])
snippets.createNumericAttribute("stretch", "stretch", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0, selList=["leg_L_thighFK_ctrl"])
snippets.createNumericAttribute("squashFB", "squashFB", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0, selList=["leg_L_thighFK_ctrl"])
snippets.createNumericAttribute("squashLR", "squashLR", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0, selList=["leg_L_thighFK_ctrl"])
snippets.createNumericAttribute("stretch", "stretch", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0, selList=["leg_L_shinFK_ctrl"])
snippets.createNumericAttribute("squashFB", "squashFB", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0, selList=["leg_L_shinFK_ctrl"])
snippets.createNumericAttribute("squashLR", "squashLR", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0, selList=["leg_L_shinFK_ctrl"])
snippets.createNumericAttribute("stretch", "stretch", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0, selList=["leg_L_ankleFK_ctrl"])
snippets.createNumericAttribute("squashFB", "squashFB", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0, selList=["leg_L_ankleFK_ctrl"])
snippets.createNumericAttribute("squashLR", "squashLR", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0, selList=["leg_L_ankleFK_ctrl"])
snippets.createNumericAttribute("displayPointer", "displayPointer", snippets.AttributeTypes.kBool, selList=["leg_L_legPv_ctrl"])
snippets.createNumericAttribute("showSnapCtrl", "showSnapCtrl", snippets.AttributeTypes.kBool, selList=["leg_L_legIK_ctrl"])
snippets.createEnumAttribute("pvMode", "pvMode", {"Manual":0, "Auto":1}, selList=["leg_L_legIK_ctrl"])
snippets.createUnitAttribute("twistKnee", "twistKnee", snippets.AttributeTypes.kAngle, selList=["leg_L_legIK_ctrl"])
snippets.createNumericAttribute("snapPv", "snapPv", snippets.AttributeTypes.kFloat, minVal=0.0, maxVal=1.0, selList=["leg_L_legIK_ctrl"])
snippets.createNumericAttribute("softIK", "softIK", snippets.AttributeTypes.kFloat, minVal=0.0, maxVal=0.4, selList=["leg_L_legIK_ctrl"])
snippets.createNumericAttribute("stretch", "stretch", snippets.AttributeTypes.kFloat, minVal=0.0, maxVal=1.0, selList=["leg_L_legIK_ctrl"])
snippets.createNumericAttribute("clampStretch", "clampStretch", snippets.AttributeTypes.kFloat, minVal=0.0, maxVal=1.0, selList=["leg_L_legIK_ctrl"])
snippets.createNumericAttribute("clampValue", "clampValue", snippets.AttributeTypes.kFloat, minVal=1.0, default=1.5, selList=["leg_L_legIK_ctrl"])
snippets.createNumericAttribute("stretchValue", "stretchValue", snippets.AttributeTypes.kFloat, channelBox=True, selList=["leg_L_legIK_ctrl"])
snippets.createNumericAttribute("squash", "squash", snippets.AttributeTypes.kFloat, minVal=0.0, maxVal=1.0, selList=["leg_L_legIK_ctrl"])
cmds.setAttr("leg_L_ankleIKUpWMtx_fNode.matrixIn[0]", cmds.getAttr("composeMatrix3.outputMatrix"), type="matrix")
print(snippets.findUpVectorPosition("leg_L_toeIK_srt"))




















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
