import maya.cmds as cmds
import maya.mel as mel
from functools import partial


from gfTools.gfAutoRig.settings import guides
from gfTools.gfAutoRig.settings import log
reload(guides); reload(log)


def enableIKSplineHSpine(self, *args):
    opt = cmds.optionMenuGrp("optEnIKSplineHSpine", q=True, v=True)
    if opt == "Enabled":
        cmds.rowLayout("layNumIKSplineJntsHSpine", edit=True, en=True)
        cmds.rowLayout("layTwistIKHSpine", edit=True, en=True)
        cmds.rowLayout("layStretchIKHSpine", edit=True, en=True)
        cmds.rowLayout("layTweakIKHSpine", edit=True, en=True)
    else:
        cmds.rowLayout("layNumIKSplineJntsHSpine", edit=True, en=False)
        cmds.rowLayout("layTwistIKHSpine", edit=True, en=False)
        cmds.rowLayout("layStretchIKHSpine", edit=True, en=False)
        cmds.rowLayout("layTweakIKHSpine", edit=True, en=False)

def enableRibbonHSpine(self, *args):
    opt = cmds.optionMenuGrp("optEnRibbonHSpine", q=True, v=True)
    if opt == "Enabled":
        cmds.rowLayout("layNumRibJntsHSpine", edit=True, en=True)
        cmds.rowLayout("layBendCtrlsHSpine", edit=True, en=True)
        cmds.rowLayout("layTweakCtrlsHSpine", edit=True, en=True)
        cmds.rowLayout("layTwistAttrsHSpine", edit=True, en=True)
        cmds.rowLayout("laySineAttrsHSpine", edit=True, en=True)
        # cmds.rowLayout("layStretchAttrsHSpine", edit=True, en=True)
        cmds.rowLayout("layExtraFreeSlotsHSpine", edit=True, en=True)
    else:
        cmds.rowLayout("layNumRibJntsHSpine", edit=True, en=False)
        cmds.rowLayout("layBendCtrlsHSpine", edit=True, en=False)
        cmds.rowLayout("layTweakCtrlsHSpine", edit=True, en=False)
        cmds.rowLayout("layTwistAttrsHSpine", edit=True, en=False)
        cmds.rowLayout("laySineAttrsHSpine", edit=True, en=False)
        # cmds.rowLayout("layStretchAttrsHSpine", edit=True, en=False)
        cmds.rowLayout("layExtraFreeSlotsHSpine", edit=True, en=False)

def enableStretchIKHSpine(self, *args):
    check = cmds.checkBoxGrp("cbxStretchIKHSpine", q=True, v1=True)
    if check == True:
        cmds.rowLayout("layStretckIKMultHSpine", edit=True, en=True)
        cmds.rowLayout("layClampStretchHSpine", edit=True, en=True)
        cmds.rowLayout("laySquashIKHSpine", edit=True, en=True)
        cmds.rowLayout("laySquashIKMultHSpine", edit=True, en=True)
    else:
        cmds.rowLayout("layStretckIKMultHSpine", edit=True, en=False)
        cmds.rowLayout("layClampStretchHSpine", edit=True, en=False)
        cmds.rowLayout("laySquashIKHSpine", edit=True, en=False)
        cmds.rowLayout("laySquashIKMultHSpine", edit=True, en=False)

def setHybridTypeHSpine(self, *args):
    typ = cmds.radioButtonGrp("radHybridTypeHSpine", q=True, sl=True)
    if typ == 1:
        cmds.frameLayout("frmIKSplineSettingsHSpine", edit=True, en=True)
        cmds.frameLayout("frmRibbonSettingsHSpine", edit=True, cl=True, en=False)
    elif typ == 2:
        cmds.frameLayout("frmIKSplineSettingsHSpine", edit=True, cl=True, en=False)
        cmds.frameLayout("frmRibbonSettingsHSpine", edit=True, en=True)
