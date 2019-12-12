import maya.cmds as cmds
import maya.mel as mel
from functools import partial


from gfTools.__OLD.gfTools.gfAutoRig.settings import guides
from gfTools.__OLD.gfTools.gfAutoRig.settings import log
reload(guides); reload(log)


def enableIKSplineHHeads(self, *args):
    opt = cmds.optionMenuGrp("optEnIKSplineHHeads", q=True, v=True)
    if opt == "Enabled":
        cmds.rowLayout("layNumIKSplineJntsHHeads", edit=True, en=True)
        cmds.rowLayout("layStretchIKHHeads", edit=True, en=True)
        cmds.rowLayout("layTweakIKHHeads", edit=True, en=True)
    else:
        cmds.rowLayout("layNumIKSplineJntsHHeads", edit=True, en=False)
        cmds.rowLayout("layStretchIKHHeads", edit=True, en=False)
        cmds.rowLayout("layTweakIKHHeads", edit=True, en=False)

def enableRibbonHHeads(self, *args):
    opt = cmds.optionMenuGrp("optEnRibbonHHeads", q=True, v=True)
    if opt == "Enabled":
        cmds.rowLayout("layNumRibJntsHHeads", edit=True, en=True)
        cmds.rowLayout("layBendCtrlsHHeads", edit=True, en=True)
        cmds.rowLayout("layTweakCtrlsHHeads", edit=True, en=True)
        cmds.rowLayout("layTwistAttrsHHeads", edit=True, en=True)
        cmds.rowLayout("laySineAttrsHHeads", edit=True, en=True)
        # cmds.rowLayout("layStretchAttrsHHeads", edit=True, en=True)
        cmds.rowLayout("layExtraFreeSlotsHHeads", edit=True, en=True)
    else:
        cmds.rowLayout("layNumRibJntsHHeads", edit=True, en=False)
        cmds.rowLayout("layBendCtrlsHHeads", edit=True, en=False)
        cmds.rowLayout("layTweakCtrlsHHeads", edit=True, en=False)
        cmds.rowLayout("layTwistAttrsHHeads", edit=True, en=False)
        cmds.rowLayout("laySineAttrsHHeads", edit=True, en=False)
        # cmds.rowLayout("layStretchAttrsHHeads", edit=True, en=False)
        cmds.rowLayout("layExtraFreeSlotsHHeads", edit=True, en=False)

def enableStretchIKHHeads(self, *args):
    check = cmds.checkBoxGrp("cbxStretchIKHHeads", q=True, v1=True)
    if check == True:
        cmds.rowLayout("layStretckIKMultHHeads", edit=True, en=True)
        cmds.rowLayout("layClampStretchHHeads", edit=True, en=True)
        cmds.rowLayout("laySquashIKHHeads", edit=True, en=True)
        cmds.rowLayout("laySquashIKMultHHeads", edit=True, en=True)
    else:
        cmds.rowLayout("layStretckIKMultHHeads", edit=True, en=False)
        cmds.rowLayout("layClampStretchHHeads", edit=True, en=False)
        cmds.rowLayout("laySquashIKHHeads", edit=True, en=False)
        cmds.rowLayout("laySquashIKMultHHeads", edit=True, en=False)

def enableEyesHHeads(self, *args):
    check = cmds.checkBoxGrp("cbxHead1CreateEyesHHeads", q=True, v1=True)
    if check == True:
        cmds.rowLayout("layHead1NumEyesHHeads", edit=True, en=True)
    else:
        cmds.rowLayout("layHead1NumEyesHHeads", edit=True, en=False)

def setHybridTypeHHeads(self, *args):
    typ = cmds.radioButtonGrp("radHybridTypeHHeads", q=True, sl=True)
    if typ == 1:
        cmds.frameLayout("frmIKSplineSettingsHHeads", edit=True, en=True)
        cmds.frameLayout("frmRibbonSettingsHHeads", edit=True, cl=True, en=False)
    elif typ == 2:
        cmds.frameLayout("frmIKSplineSettingsHHeads", edit=True, cl=True, en=False)
        cmds.frameLayout("frmRibbonSettingsHHeads", edit=True, en=True)

def enableSpaceSwitchHHeads(*args):
    opt = cmds.optionMenuGrp("optEnSpaceSwitchHHeads", q=True, v=True)
    if opt == "Enabled":
        # cmds.rowLayout("layMethodHHeads", edit=True, en=True)
        cmds.rowLayout("layHeadsSpaceHHeads", edit=True, en=True)
        cmds.rowLayout("layHeadsSpaceListHHeads", edit=True, en=True)
    else:
        # cmds.rowLayout("layMethodHHeads", edit=True, en=False)
        cmds.rowLayout("layHeadsSpaceHHeads", edit=True, en=False)
        cmds.rowLayout("layHeadsSpaceListHHeads", edit=True, en=False)

def legsSpacesHHeads(operation, *args):
    space = cmds.optionMenuGrp("optHeadsSpaceHHeads", q=True, v=True)
    listed = cmds.textScrollList("lstHeadsSpaceListHHeads", q=True, ai=True)
    if operation == "add":
        if listed == None:
            cmds.textScrollList("lstHeadsSpaceListHHeads", edit=True, a=[space])
        else:
            if space in listed:
                cmds.warning("Space already exists")
            else:
                cmds.textScrollList("lstHeadsSpaceListHHeads", edit=True, a=[space])
    elif operation == "rem":
        sel = cmds.textScrollList("lstHeadsSpaceListHHeads", q=True, si=True)
        if sel == None:
            cmds.warning("Select at least one space in the list")
        else:
            for s in sel:
                cmds.textScrollList("lstHeadsSpaceListHHeads", edit=True, ri=s)
