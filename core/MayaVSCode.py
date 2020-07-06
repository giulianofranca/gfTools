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


import maya.api._OpenMayaUI_py2 as omui2
import maya.api._OpenMaya_py2 as om2
from gfTools.core import snippets
reload(snippets)
# Right arm ori: XYZ+


snippets.createChar("astroman")
snippets.createComponent("astroman", "head_C")
snippets.createMessageAttribute("component", "component")
snippets.createObjectOnTransform()
snippets.unfreezeTransformations()
snippets.createMatrixAttribute("headSpaceWorldMatrix", "headSpaceWorldMatrix", snippets.AttributeTypes.kDoubleMatrix)
snippets.createMatrixAttribute("headSpaceWorldInverseMatrix", "headSpaceWorldInverseMatrix", snippets.AttributeTypes.kDoubleMatrix)
snippets.createMatrixAttribute("jawSpaceWorldMatrix", "jawSpaceWorldMatrix", snippets.AttributeTypes.kDoubleMatrix)
snippets.createMatrixAttribute("jawSpaceWorldInverseMatrix", "jawSpaceWorldInverseMatrix", snippets.AttributeTypes.kDoubleMatrix)
cmds.move(0.0, 0.0, 0.5, r=True, os=True, wd=True)
snippets.mirrorControlShape()
snippets.mirrorControlShape(xAxis=False, yAxis=False)
snippets.createFK(connect=True)


om2.MGlobal.displayInfo(str(((5 - 1) * 2) + 1))
upVec = om2.MVector.kYaxisVector
snippets.curveDistribution("curve1", 5, upVec, "joint", hierarchical=True, nonUniformSegments=False)

snippets.copyCurveShape("arm_L_clavicle_ctrl", "arm_L_clavicle_ctrl1", True)


print(len(cmds.listConnections("leg_R_cmpnt.ikHandles")))
print(len(cmds.listConnections("leg_L_cmpnt.ikHandles")))
snippets.createFK(connect=True)
snippets.mirrorControlShape()
snippets.createComponent("mother", "global_C")
snippets.createComponent("mother", "leg_L")
snippets.createComponent("mother", "leg_R")
snippets.createComponent("mother", "spine_C")
snippets.createComponent("mother", "arm_L")
snippets.createComponent("mother", "arm_R")
snippets.createEnumAttribute("GLOBAL", "GLOBAL", {"__________":0})
cmds.setAttr("global_C_master_ctrl.GLOBAL", 0, l=True)
cmds.setAttr("global_C_masterSub1_ctrl.GLOBAL", 0, l=True)
snippets.createNumericAttribute("globalScale", "globalScale", snippets.AttributeTypes.kFloat, 0.001, default=1.0)
snippets.createEnumAttribute("DISPLAY", "DISPLAY", {"__________":0})
cmds.setAttr("global_C_master_ctrl.DISPLAY", 0, l=True)
snippets.createNumericAttribute("smoothLevel", "smoothLevel", snippets.AttributeTypes.kInt, minVal=0, maxVal=2, default=0, channelBox=True)
snippets.createNumericAttribute("height", "height", snippets.AttributeTypes.kFloat, channelBox=True)
snippets.createNumericAttribute("displayJoints", "displayJoints", snippets.AttributeTypes.kBool)
snippets.createNumericAttribute("displayControls", "displayControls", snippets.AttributeTypes.kBool)
snippets.createNumericAttribute("displayCornea", "displayCornea", snippets.AttributeTypes.kBool)
snippets.createNumericAttribute("displayGlasses", "displayGlasses", snippets.AttributeTypes.kBool)
snippets.createNumericAttribute("displayEarrings", "displayEarrings", snippets.AttributeTypes.kBool)
snippets.createNumericAttribute("displayClothes", "displayClothes", snippets.AttributeTypes.kBool)
snippets.createNumericAttribute("displayBand", "displayBand", snippets.AttributeTypes.kBool)
snippets.createEnumAttribute("displayGeo", "displayGeo", {"Hide":0, "Show":1, "Reference":2})
snippets.createMessageAttribute("component", "component")
snippets.getPoleVectorPosition(12.0)
snippets.createEnumAttribute("SETTINGS", "SETTINGS", {"__________":0})
cmds.setAttr("leg_L_settings_ctrl.SETTINGS", 0, l=True)
snippets.createNumericAttribute("fkikBlend", "fkikBlend", snippets.AttributeTypes.kFloat, 0.0, 1.0)
snippets.createEnumAttribute("LEG", "LEG", {"__________":0})
cmds.setAttr("leg_L_thighFK_ctrl.LEG", 0, l=True)
cmds.setAttr("leg_L_legIK_ctrl.LEG", 0, l=True)
snippets.createEnumAttribute("ARM", "ARM", {"__________":0})
cmds.setAttr("arm_R_upperArmFK_ctrl.ARM", 0, l=True)
cmds.setAttr("arm_R_armIK_ctrl.ARM", 0, l=True)
snippets.createEnumAttribute("spaceSwitch", "spaceSwitch", {"Shoulder":0, "Chest":1, "Hip":2, "Root":3, "Master":4})
snippets.createEnumAttribute("spaceSwitch", "spaceSwitch", {"Pelvis":0, "Hip":1, "Root":2, "Global":3})
snippets.createEnumAttribute("UPPERARM", "UPPERARM", {"__________":0})
cmds.setAttr("arm_R_upperArmFK_ctrl.UPPERARM", 0, l=True)
snippets.createEnumAttribute("FOREARM", "FOREARM", {"__________":0})
cmds.setAttr("arm_R_forearmFK_ctrl.FOREARM", 0, l=True)
snippets.createEnumAttribute("WRIST", "WRIST", {"__________":0})
cmds.setAttr("arm_R_wristFK_ctrl.WRIST", 0, l=True)
snippets.createEnumAttribute("THIGH", "THIGH", {"__________":0})
cmds.setAttr("leg_L_thighFK_ctrl.THIGH", 0, l=True)
snippets.createEnumAttribute("SHIN", "SHIN", {"__________":0})
cmds.setAttr("leg_L_shinFK_ctrl.SHIN", 0, l=True)
snippets.createEnumAttribute("ANKLE", "ANKLE", {"__________":0})
cmds.setAttr("leg_L_ankleFK_ctrl.ANKLE", 0, l=True)
snippets.createEnumAttribute("TOE", "TOE", {"__________":0})
cmds.setAttr("leg_L_toeFK_ctrl.TOE", 0, l=True)
rotOrder = {"xyz":0, "yzx":1, "zxy":2, "xzy":3, "yxz":4, "zyx":5}
snippets.createEnumAttribute("rotationOrder", "rotationOrder", rotOrder)
snippets.createNumericAttribute("showOffsetCtrl", "showOffsetCtrl", snippets.AttributeTypes.kBool, default=True)
snippets.createNumericAttribute("stretch", "stretch", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0)
snippets.createNumericAttribute("squashFB", "squashFB", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0)
snippets.createNumericAttribute("squashLR", "squashLR", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0)
snippets.createEnumAttribute("PV", "PV", {"__________":0})
cmds.setAttr("leg_L_legPv_ctrl.PV", 0, l=True)
snippets.createEnumAttribute("SNAP", "SNAP", {"__________":0})
cmds.setAttr("arm_R_armSnap_ctrl.SNAP", 0, l=True)
snippets.createEnumAttribute("spaceSwitch", "spaceSwitch", {"Arm":0, "Shoulder":1, "Chest":2, "Hip":3, "Root":4, "Master":5})
snippets.createEnumAttribute("spaceSwitch", "spaceSwitch", {"Leg":0, "Pelvis":1, "Hip":2, "Root":3, "Global":4})
snippets.createNumericAttribute("displayPointer", "displayPointer", snippets.AttributeTypes.kBool)
snippets.createNumericAttribute("showSnapCtrl", "showSnapCtrl", snippets.AttributeTypes.kBool, default=True)
snippets.createNumericAttribute("manualAutoPv", "manualAutoPv", snippets.AttributeTypes.kFloat, minVal=0, maxVal=1)
snippets.createUnitAttribute("twistElbow", "twistElbow", snippets.AttributeTypes.kAngle)
snippets.createNumericAttribute("snapPv", "snapPv", snippets.AttributeTypes.kFloat, minVal=0.0, maxVal=1.0)
snippets.createNumericAttribute("softIK", "softIK", snippets.AttributeTypes.kFloat, minVal=0.0, maxVal=0.4)
snippets.createNumericAttribute("stretch", "stretch", snippets.AttributeTypes.kFloat, minVal=0.0, maxVal=1.0)
snippets.createNumericAttribute("clampStretch", "clampStretch", snippets.AttributeTypes.kFloat, minVal=0.0, maxVal=1.0)
snippets.createNumericAttribute("clampValue", "clampValue", snippets.AttributeTypes.kFloat, minVal=1.0, default=1.5)
snippets.createNumericAttribute("currentStretchValue", "currentStretchValue", snippets.AttributeTypes.kFloat, channelBox=True)
snippets.createNumericAttribute("squash", "squash", snippets.AttributeTypes.kFloat, minVal=0.0, maxVal=1.0)
snippets.createNumericAttribute("squashMultUpperArmFB", "squashMultUpperArmFB", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0)
snippets.createNumericAttribute("squashMultUpperArmLR", "squashMultUpperArmLR", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0)
snippets.createNumericAttribute("squashMultForearmFB", "squashMultForearmFB", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0)
snippets.createNumericAttribute("squashMultForearmLR", "squashMultForearmLR", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0)
snippets.createEnumAttribute("FOOT", "FOOT", {"__________":0})
cmds.setAttr("leg_L_footSmart_ctrl.FOOT", 0, l=True)
snippets.findUpVectorPosition(const="leg_L_ankleIK_srt", parent="leg_L_ankleIK_srt", create=True)
snippets.createNumericAttribute("footRollBreak", "footRollBreak", snippets.AttributeTypes.kFloat, default=45)
snippets.createNumericAttribute("footRollStraight", "footRollStraight", snippets.AttributeTypes.kFloat, default=70)
snippets.createUnitAttribute("footRollMaxAngle", "footRollMaxAngle", snippets.AttributeTypes.kAngle, minVal=0)
snippets.createUnitAttribute("footRollMinAngle", "footRollMinAngle", snippets.AttributeTypes.kAngle, minVal=0)
snippets.createUnitAttribute("footBankMaxAngle", "footBankMaxAngle", snippets.AttributeTypes.kAngle, minVal=0)
snippets.createUnitAttribute("footTipLift", "footTipLift", snippets.AttributeTypes.kAngle, default=0, minVal=0)
snippets.createUnitAttribute("footTipSpin", "footTipSpin", snippets.AttributeTypes.kAngle, default=0)
snippets.createUnitAttribute("footHeelSpin", "footHeelSpin", snippets.AttributeTypes.kAngle, default=0)
snippets.createUnitAttribute("ballLift", "ballLift", snippets.AttributeTypes.kAngle, default=0)
snippets.createUnitAttribute("ballSpin", "ballSpin", snippets.AttributeTypes.kAngle, default=0)
snippets.createUnitAttribute("ballLean", "ballLean", snippets.AttributeTypes.kAngle, default=0)
snippets.createUnitAttribute("toeLift", "toeLift", snippets.AttributeTypes.kAngle, default=0)
snippets.createUnitAttribute("toeSpin", "toeSpin", snippets.AttributeTypes.kAngle, default=0)
snippets.createUnitAttribute("toeTwist", "toeTwist", snippets.AttributeTypes.kAngle, default=0)
snippets.createEnumAttribute("TOE", "TOE", {"__________":0})
cmds.setAttr("leg_L_toeSmart_ctrl.TOE", 0, l=True)
snippets.createNumericAttribute("showToeCtrls", "showToeCtrls", snippets.AttributeTypes.kBool)
snippets.createNumericAttribute("globalScale", "globalScale", snippets.AttributeTypes.kFloat)
snippets.createNumericAttribute("globalInverseScale", "globalInverseScale", snippets.AttributeTypes.kFloat)
snippets.createMatrixAttribute("masterSpaceWorldMatrix", "masterSpaceWorldMatrix", snippets.AttributeTypes.kDoubleMatrix)
snippets.createMatrixAttribute("masterSpaceWorldInverseMatrix", "masterSpaceWorldInverseMatrix", snippets.AttributeTypes.kDoubleMatrix)
snippets.createMatrixAttribute("pelvisSpaceWorldMatrix", "pelvisSpaceWorldMatrix", snippets.AttributeTypes.kDoubleMatrix)
snippets.createMatrixAttribute("pelvisSpaceWorldInverseMatrix", "pelvisSpaceWorldInverseMatrix", snippets.AttributeTypes.kDoubleMatrix)
snippets.createMatrixAttribute("hipSpaceWorldMatrix", "hipSpaceWorldMatrix", snippets.AttributeTypes.kDoubleMatrix)
snippets.createMatrixAttribute("hipSpaceWorldInverseMatrix", "hipSpaceWorldInverseMatrix", snippets.AttributeTypes.kDoubleMatrix)
snippets.createMatrixAttribute("rootSpaceWorldMatrix", "rootSpaceWorldMatrix", snippets.AttributeTypes.kDoubleMatrix)
snippets.createMatrixAttribute("rootSpaceWorldInverseMatrix", "rootSpaceWorldInverseMatrix", snippets.AttributeTypes.kDoubleMatrix)
snippets.createMatrixAttribute("chestSpaceWorldMatrix", "chestSpaceWorldMatrix", snippets.AttributeTypes.kDoubleMatrix)
snippets.createMatrixAttribute("chestSpaceWorldInverseMatrix", "chestSpaceWorldInverseMatrix", snippets.AttributeTypes.kDoubleMatrix)
snippets.createUnitAttribute("roll", "roll", snippets.AttributeTypes.kAngle)
snippets.createNumericAttribute("fixedLength", "fixedLength", snippets.AttributeTypes.kFloat, minVal=0.0, maxVal=1.0)
snippets.createNumericAttribute("squash", "squash", snippets.AttributeTypes.kFloat, minVal=0.0, maxVal=1.0)
snippets.createNumericAttribute("squashDistribution", "squashDistribution", snippets.AttributeTypes.kFloat, minVal=0.0, maxVal=1.0)
snippets.createNumericAttribute("squashPos", "squashPos", snippets.AttributeTypes.kFloat, minVal=0.0, maxVal=1.0)
snippets.createNumericAttribute("squashSmooth", "squashSmooth", snippets.AttributeTypes.kFloat, minVal=0.001, default=1.0)
snippets.createNumericAttribute("squashFactor", "squashFactor", snippets.AttributeTypes.kFloat, default=0, minVal=0.0)
snippets.createNumericAttribute("squashMultFB", "squashMultFB", snippets.AttributeTypes.kFloat, default=1.0)
snippets.createNumericAttribute("squashMultLR", "squashMultLR", snippets.AttributeTypes.kFloat, default=1.0)
snippets.createUnitAttribute("thumbCurl", "thumbCurl", snippets.AttributeTypes.kAngle, default=0.0)


selList = om2.MGlobal.getActiveSelectionList()
for i in range(selList.length()):
    curObj = selList.getDependNode(i)
    nodeFn = om2.MFnDependencyNode(curObj)
    rAttr = om2.MRampAttribute()
    attr = rAttr.createCurveRamp("squashRamp", "squashRamp")
    nodeFn.addAttribute(attr)



# Create Mother rig
#======================================================================================================
# Componet Left Leg
#======================================================================================================
snippets.createChar("mother")
snippets.createMessageAttribute("bindGeometry", "bindGeometry", selList=["mother_C_body_geo"])
snippets.connectAttr("geometry_hrc.bindLayer1", "mother_C_body_geo.bindGeometry")
snippets.createComponent("mother", "leg_L")
bndList = ["leg_L_thigh_bnd", "leg_L_shin_bnd", "leg_L_ankle_bnd"]
snippets.createMessageAttribute("bindJoint", "bindJoint", selList=bndList)
ikHdleList = ["leg_L_legIKHandle_srt", "leg_L_ankleIKHandle_srt", "leg_L_toeIKHandle_srt"]
snippets.createMessageAttribute("ikHandle", "ikHandle", selList=ikHdleList)
snippets.getPoleVectorPosition(70.0)
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
snippets.createEnumAttribute("FOOT", "FOOT", {"__________":0}, selList=["leg_L_legIK_ctrl"])
cmds.setAttr("leg_L_legIK_ctrl.FOOT", 0, l=True)
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
snippets.createEnumAttribute("spaceSwitch", "spaceSwitch", {"Leg":0, "Pelvis":1, "Hip":2, "Root":3, "Global":4}, selList=["leg_L_legPv_ctrl"])
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
snippets.createNumericAttribute("currentStretchValue", "currentStretchValue", snippets.AttributeTypes.kFloat, channelBox=True, selList=["leg_L_legIK_ctrl"])
snippets.createNumericAttribute("squash", "squash", snippets.AttributeTypes.kFloat, minVal=0.0, maxVal=1.0, selList=["leg_L_legIK_ctrl"])
snippets.createNumericAttribute("footRoll", "footRoll", snippets.AttributeTypes.kFloat, default=0, selList=["leg_L_legIK_ctrl"])
snippets.createNumericAttribute("footRollBreak", "footRollBreak", snippets.AttributeTypes.kFloat, default=45, selList=["leg_L_legIK_ctrl"])
snippets.createNumericAttribute("footRollStraight", "footRollStraight", snippets.AttributeTypes.kFloat, default=70, selList=["leg_L_legIK_ctrl"])
snippets.createNumericAttribute("footBank", "footBank", snippets.AttributeTypes.kFloat, default=0, selList=["leg_L_legIK_ctrl"])
snippets.createUnitAttribute("footTipLift", "footTipLift", snippets.AttributeTypes.kAngle, default=0, selList=["leg_L_legIK_ctrl"])
snippets.createUnitAttribute("footTipSpin", "footTipSpin", snippets.AttributeTypes.kAngle, default=0, selList=["leg_L_legIK_ctrl"])
snippets.createUnitAttribute("footHeelSpin", "footHeelSpin", snippets.AttributeTypes.kAngle, default=0, selList=["leg_L_legIK_ctrl"])
snippets.createUnitAttribute("ballLift", "ballLift", snippets.AttributeTypes.kAngle, default=0, selList=["leg_L_legIK_ctrl"])
snippets.createUnitAttribute("ballSpin", "ballSpin", snippets.AttributeTypes.kAngle, default=0, selList=["leg_L_legIK_ctrl"])
snippets.createUnitAttribute("ballLean", "ballLean", snippets.AttributeTypes.kAngle, default=0, selList=["leg_L_legIK_ctrl"])
snippets.createUnitAttribute("toeLift", "toeLift", snippets.AttributeTypes.kAngle, default=0, selList=["leg_L_legIK_ctrl"])
snippets.createUnitAttribute("toeSpin", "toeSpin", snippets.AttributeTypes.kAngle, default=0, selList=["leg_L_legIK_ctrl"])
snippets.createUnitAttribute("toeTwist", "toeTwist", snippets.AttributeTypes.kAngle, default=0, selList=["leg_L_legIK_ctrl"])
cmds.setAttr("multMatrix1.matrixIn[0]", cmds.getAttr("offset.matrixSum"), type="matrix")
snippets.createNumericAttribute("showBendCtrls", "showBendCtrls", snippets.AttributeTypes.kBool, selList=["leg_L_settings_ctrl"])
snippets.createNumericAttribute("showRibbonCtrls", "showRibbonCtrls", snippets.AttributeTypes.kBool, selList=["leg_L_settings_ctrl"])

# https://www.youtube.com/watch?v=iOFO-i3F7wY
# https://www.youtube.com/watch?v=naSSzjfPZFs
# https://www.youtube.com/watch?v=yrnpRCwkDf0
# https://github.com/bungnoid/glTools/blob/master/utils/curve.py
om2.MGlobal.displayInfo(str(snippets.findUpVectorPosition("leg_L_toeIK_srt")))
snippets.createMatrixAttribute("pelvisSpaceWorldMatrix", "pelvisSpaceWorldMatrix", snippets.AttributeTypes.kFloatMatrix, selList=["leg_L_settings_io"])
snippets.createMatrixAttribute("pelvisSpaceWorldInverseMatrix", "pelvisSpaceWorldInverseMatrix", snippets.AttributeTypes.kFloatMatrix, selList=["leg_L_settings_io"])
snippets.createMatrixAttribute("hipSpaceWorldMatrix", "hipSpaceWorldMatrix", snippets.AttributeTypes.kFloatMatrix, selList=["leg_L_settings_io"])
snippets.createMatrixAttribute("hipSpaceWorldInverseMatrix", "hipSpaceWorldInverseMatrix", snippets.AttributeTypes.kFloatMatrix, selList=["leg_L_settings_io"])
snippets.createMatrixAttribute("rootSpaceWorldMatrix", "rootSpaceWorldMatrix", snippets.AttributeTypes.kFloatMatrix, selList=["leg_L_settings_io"])
snippets.createMatrixAttribute("rootSpaceWorldInverseMatrix", "rootSpaceWorldInverseMatrix", snippets.AttributeTypes.kFloatMatrix, selList=["leg_L_settings_io"])
#======================================================================================================
# Componet Right Leg
#======================================================================================================
snippets.createComponent("mother", "leg_R")
snippets.createObjectOnTransform()
snippets.mirrorControlShape()
snippets.mirrorControlShape(yAxis=False, zAxis=False)
snippets.getPoleVectorPosition(4.0)
snippets.createMessageAttribute("component", "component")
snippets.createMessageAttribute("bindJoint", "bindJoint")
om2.MGlobal.displayInfo(str(snippets.findUpVectorPosition("leg_R_toeIK_srt")))
#======================================================================================================
# Componet Left Arm
#======================================================================================================
snippets.createComponent("mother", "arm_L")
snippets.createObjectOnTransform()
snippets.getPoleVectorPosition(4.0)















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





# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
draggerContextName = "MyDragger"

def viewToWorld(screenX, screenY):
    """ View to World Position. """
    worldPos = om2.MPoint()     # World position
    worldDir = om2.MVector()    # World direction

    activeView = omui2.M3dView.active3dView()
    activeView.viewToWorld(int(screenX), int(screenY), worldPos, worldDir)

    return (worldPos, worldDir)

def getCameraWorldViewDirection():
    """ Get camera normal. """
    activeView = omui2.M3dView.active3dView()
    cameraPath = activeView.getCamera()
    camFn = om2.MFnCamera(cameraPath)

    return camFn.viewDirection()

om2.MGlobal.displayInfo(str(getCameraWorldViewDirection()))


# Get the vertices normals from selection list
selList = om2.MGlobal.getActiveSelectionList()
itSel = om2.MItSelectionList(selList)
while not itSel.isDone():
    path, cmpnt = itSel.getComponent()
    if not cmpnt.isNull():
        meshFn = om2.MFnMesh(path)
        itVtx = om2.MItMeshVertex(path, cmpnt)
        vtxIndices = om2.MIntArray()
        vtxNormals = om2.MVectorArray()
        vtxPositions = om2.MPointArray()
        while not itVtx.isDone():
            vtxIndices.append(itVtx.index())
            vtxNormals.append(itVtx.getNormal())
            vtxPositions.append(itVtx.position(om2.MSpace.kWorld))
            itVtx.next()
    itSel.next()
