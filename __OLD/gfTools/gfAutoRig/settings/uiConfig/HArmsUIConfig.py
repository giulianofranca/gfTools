import maya.cmds as cmds
import maya.mel as mel
from functools import partial


from gfTools.__OLD.gfTools.gfAutoRig.settings import guides
from gfTools.__OLD.gfTools.gfAutoRig.settings import log
reload(guides); reload(log)


def multipleArmsHArms(*args):
    multArms = cmds.radioButtonGrp("radMultArmsHArms", q=True, sl=True)
    # print ("Radio Button Active: %s") %(multArms)
    if multArms == 1:
        cmds.rowLayout("layMultArmsHArms", edit=True, en=False)
        cmds.textField("txtNumberHArms", edit=True, tx="2")
        cmds.button("btnAddArmHArms", edit=True, en=True)
        cmds.button("btnRemArmHArms", edit=True, en=False)
        childs = cmds.layout("layMultHumanArmsHArms", q=True, ca=True)
        for c in childs:
            cmds.deleteUI(c)
        cmds.rowLayout("layMultLArmHArms", w=310, nc=2, p="layMultHumanArmsHArms")
        cmds.separator(w=5, h=3, st="none")
        cmds.frameLayout("frmLeftArmHArms", w=312, cl=True, cll=True, bgs=True, l="Left Arm")
        cmds.textFieldGrp("txtLArmParentHArms", l="Arm Parent: ", cw2=(110, 120), tx="None", ed=False)
        cmds.checkBoxGrp("cbxLArmHaveClavicleHArms", l="Have clavicle: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(haveClavicleHArms, "LArm"))
        cmds.checkBoxGrp("cbxLArmHaveFingersHArms", l="Have fingers: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(haveFingersHArms, "LArm"))
        cmds.rowLayout("layLArmNumFingersHArms", nc=1, en=False)
        cmds.intSliderGrp("intLArmNumFingersHArms", l="Number of fingers: ", cw=([(1, 110), (2, 40), (3, 130)]), f=True, min=3, max=6, fmn=3, fmx=6, v=5)
        cmds.rowLayout("layMultRArmHArms", w=310, nc=2, p="layMultHumanArmsHArms")
        cmds.separator(w=5, h=3, st="none")
        cmds.frameLayout("frmRightArmHArms", w=310, cl=True, cll=True, bgs=True, l="Right Arm")
        cmds.textFieldGrp("txtRArmParentHArms", l="Arm Parent: ", cw2=(120, 120), tx="None", ed=False)
        cmds.checkBoxGrp("cbxRArmHaveClavicleHArms", l="Have clavicle: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(haveClavicleHArms, "RArm"))
        cmds.checkBoxGrp("cbxRArmHaveFingersHArms", l="Have fingers: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(haveFingersHArms, "RArm"))
        cmds.rowLayout("layRArmNumFingersHArms", nc=1, en=False)
        cmds.intSliderGrp("intRArmNumFingersHArms", l="Number of fingers: ", cw=([(1, 110), (2, 40), (3, 130)]), f=True, min=3, max=6, fmn=3, fmx=6, v=5)
        log.buildLogHumanArm(msg="multArmsPropUI", btn=multArms, stop=False)
    elif multArms == 2:
        cmds.rowLayout("layMultArmsHArms", edit=True, en=True)
        cmds.textField("txtNumberHArms", edit=True, tx="1")
        cmds.button("btnAddArmHArms", edit=True, en=True)
        cmds.button("btnRemArmHArms", edit=True, en=False)
        childs = cmds.layout("layMultHumanArmsHArms", q=True, ca=True)
        for c in childs:
            cmds.deleteUI(c)
        cmds.rowLayout("layMultArm1HArms", w=310, nc=2, p="layMultHumanArmsHArms")
        cmds.separator(w=5, h=3, st="none")
        cmds.frameLayout("frmArm1HArms", w=310, cl=True, cll=True, bgs=True, l="Arm 1")
        cmds.textFieldGrp("txtArm1ParentHArms", l="Arm Parent: ", cw2=(120, 120), tx="None", ed=False)
        cmds.optionMenuGrp("optArm1SideHArms", l="Side: ", cw2=(120, 120))
        cmds.menuItem(l="Left")
        cmds.menuItem(l="Right")
        cmds.checkBoxGrp("cbxArm1HaveClavicleHArms", l="Have clavicle: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(haveClavicleHArms, "Arm1"))
        cmds.checkBoxGrp("cbxArm1HaveFingersHArms", l="Have fingers: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(haveFingersHArms, "Arm1"))
        cmds.rowLayout("layArm1NumFingersHArms", nc=1, en=False)
        cmds.intSliderGrp("intArm1NumFingersHArms", l="Number of fingers: ", cw=([(1, 110), (2, 40), (3, 130)]), f=True, min=3, max=6, fmn=3, fmx=6, v=5)
        log.buildLogHumanArm(msg="multArmsPropUI", btn=multArms, stop=False)
    log.buildLog(msg=None, stop=True)

def addHArms(*args):
    num = cmds.textField("txtNumberHArms", q=True, tx=True)
    newNum = 1
    newNum = int(num) + newNum
    cmds.textField("txtNumberHArms", edit=True, tx=str(newNum))
    if newNum <= 1: cmds.button("btnRemArmHArms", edit=True, en=False)
    elif newNum >= 10: cmds.button("btnAddArmHArms", edit=True, en=False)
    else:
        cmds.button("btnRemArmHArms", edit=True, en=True)
        cmds.button("btnAddArmHArms", edit=True, en=True)
    # Add Layout
    cmds.rowLayout(("layMultArm"+str(newNum)+"HArms"), w=310, nc=2, p="layMultHumanArmsHArms")
    cmds.separator(w=5, h=3, st="none")
    cmds.frameLayout(("frmArm"+str(newNum)+"HArms"), w=310, cl=True, cll=True, bgs=True, l=("Arm "+str(newNum)))
    cmds.textFieldGrp(("txtArm"+str(newNum)+"ParentHArms"), l="Arm Parent: ", cw2=(120, 120), tx="None", ed=False)
    cmds.optionMenuGrp(("optArm"+str(newNum)+"SideHArms"), l="Side: ", cw2=(120, 120))
    cmds.menuItem(l="Left")
    cmds.menuItem(l="Right")
    cmds.checkBoxGrp(("cbxArm"+str(newNum)+"HaveClavicleHArms"), l="Have clavicle: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(haveClavicleHArms, ("Arm"+str(newNum))))
    cmds.checkBoxGrp(("cbxArm"+str(newNum)+"HaveFingersHArms"), l="Have fingers: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(haveFingersHArms, ("Arm"+str(newNum))))
    cmds.rowLayout(("layArm"+str(newNum)+"NumFingersHArms"), nc=1, en=False)
    cmds.intSliderGrp(("intArm"+str(newNum)+"NumFingersHArms"), l="Number of fingers: ", cw=([(1, 110), (2, 40), (3, 130)]), f=True, min=3, max=6, fmn=3, fmx=6, v=5)
    log.buildLogHumanArm(msg="addRemArmsPropUI", btn="add", stop=True)

def remHArms(*args):
    num = cmds.textField("txtNumberHArms", q=True, tx=True)
    newNum = 1
    newNum = int(num) - newNum
    cmds.textField("txtNumberHArms", edit=True, tx=str(newNum))
    if newNum <= 1: cmds.button("btnRemArmHArms", edit=True, en=False)
    elif newNum >= 10: cmds.button("btnAddArmHArms", edit=True, en=False)
    else:
        cmds.button("btnRemArmHArms", edit=True, en=True)
        cmds.button("btnAddArmHArms", edit=True, en=True)
    # Remove Layout
    cmds.deleteUI("layMultArm"+str(num)+"HArms")
    log.buildLogHumanArm(msg="addRemArmsPropUI", btn="rem", stop=True)

def haveFingersHArms(checkbox, *args):
    if checkbox == "LArm": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHArms"), q=True, v1=True)
    elif checkbox == "RArm": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHArms"), q=True, v1=True)
    elif checkbox == "Arm1": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHArms"), q=True, v1=True)
    elif checkbox == "Arm2": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHArms"), q=True, v1=True)
    elif checkbox == "Arm3": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHArms"), q=True, v1=True)
    elif checkbox == "Arm4": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHArms"), q=True, v1=True)
    elif checkbox == "Arm5": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHArms"), q=True, v1=True)
    elif checkbox == "Arm6": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHArms"), q=True, v1=True)
    elif checkbox == "Arm7": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHArms"), q=True, v1=True)
    elif checkbox == "Arm8": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHArms"), q=True, v1=True)
    elif checkbox == "Arm9": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHArms"), q=True, v1=True)
    elif checkbox == "Arm10": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHArms"), q=True, v1=True)
    if check == True:
        cmds.rowLayout(("lay"+checkbox+"NumFingersHArms"), edit=True, en=True)
        """ Load all hand fingers guides. """
        guides.loadGuides().reloadGuides(nameComp="cbxArmHaveFingersHArms", ctrlName=checkbox)
    else:
        cmds.rowLayout(("lay"+checkbox+"NumFingersHArms"), edit=True, en=False)
        """ Delete all hand fingers guides. """
        guides.loadGuides().reloadGuides(nameComp="cbxArmHaveFingersHArms", ctrlName=checkbox)
    log.buildLogHumanArm(msg="haveFingersArmsPropUI", btn=checkbox, stop=True)

def haveClavicleHArms(checkbox, *args):
    if checkbox == "LArm": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveClavicleHArms"), q=True, v1=True)
    elif checkbox == "RArm": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveClavicleHArms"), q=True, v1=True)
    elif checkbox == "Arm1": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveClavicleHArms"), q=True, v1=True)
    elif checkbox == "Arm2": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveClavicleHArms"), q=True, v1=True)
    elif checkbox == "Arm3": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveClavicleHArms"), q=True, v1=True)
    elif checkbox == "Arm4": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveClavicleHArms"), q=True, v1=True)
    elif checkbox == "Arm5": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveClavicleHArms"), q=True, v1=True)
    elif checkbox == "Arm6": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveClavicleHArms"), q=True, v1=True)
    elif checkbox == "Arm7": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveClavicleHArms"), q=True, v1=True)
    elif checkbox == "Arm8": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveClavicleHArms"), q=True, v1=True)
    elif checkbox == "Arm9": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveClavicleHArms"), q=True, v1=True)
    elif checkbox == "Arm10": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveClavicleHArms"), q=True, v1=True)
    if check == True: # Se algum checkBox foi marcado
        """ Load all clavicle guides. """
        guides.loadGuides().reloadGuides(nameComp="cbxArmHaveClavicleHArms", ctrlName=checkbox)
        """ If have any clavicle on unlock clavicle type field """
        multArms = cmds.radioButtonGrp("radMultArmsHArms", q=True, sl=True)
        if multArms == 1:
            limbs = ['LArm', 'RArm']
        else:
            limbs = ['Arm1', 'Arm2', 'Arm3', 'Arm4', 'Arm5', 'Arm6', 'Arm7', 'Arm8', 'Arm9', 'Arm10']
        for l in limbs:
            checkClavicle = cmds.checkBoxGrp(("cbx"+l+"HaveClavicleHArms"), q=True, v1=True)
            if checkClavicle == True:
                if cmds.radioButtonGrp("radClavicleTypeHArms", q=True, en=True) == False:
                    cmds.radioButtonGrp("radClavicleTypeHArms", edit=True, en=True)
    else: # Se algum checkBox foi desmarcado
        """ Delete all hand fingers guides. """
        guides.loadGuides().reloadGuides(nameComp="cbxArmHaveClavicleHArms", ctrlName=checkbox)
        """ If haven't any clavicle on lock clavicle type field """
        multArms = cmds.radioButtonGrp("radMultArmsHArms", q=True, sl=True)
        if multArms == 1:
            limbs = ['LArm', 'RArm']
        else:
            limbs = ['Arm1', 'Arm2', 'Arm3', 'Arm4', 'Arm5', 'Arm6', 'Arm7', 'Arm8', 'Arm9', 'Arm10']
        allOff = True
        for l in limbs:
            checkClavicle = cmds.checkBoxGrp(("cbx"+l+"HaveClavicleHArms"), q=True, v1=True)
            if checkClavicle == True: allOff = False
        if allOff == True:
            if cmds.radioButtonGrp("radClavicleTypeHArms", q=True, en=True) == True:
                cmds.radioButtonGrp("radClavicleTypeHArms", edit=True, en=False)
    log.buildLogHumanArm(msg="haveFingersArmsPropUI", btn=checkbox, stop=True)

def enableIKHArm(*args):
    opt = cmds.optionMenuGrp("optEnIKHArms", q=True, v=True)
    if opt == "Enabled":
        cmds.radioButtonGrp("radIKFKTypHArms", edit=True, en=True)
        # cmds.rowLayout("layDualIKFKSeamHArms", edit=True, en=True)
        cmds.rowLayout("layAutoManuPvHArms", edit=True, en=True)
        cmds.rowLayout("layStretchIKHArms", edit=True, en=True)
        # cmds.rowLayout("laySoftIKHArms", edit=True, en=True)
        # cmds.rowLayout("layScaleIKHArms", edit=True, en=True)
        cmds.rowLayout("layReverseHandHArms", edit=True, en=True)
        cmds.rowLayout("layClavicleIKHArms", edit=True, en=True)
    else:
        cmds.radioButtonGrp("radIKFKTypHArms", edit=True, en=False)
        # cmds.rowLayout("layDualIKFKSeamHArms", edit=True, en=False)
        cmds.rowLayout("layAutoManuPvHArms", edit=True, en=False)
        cmds.rowLayout("layStretchIKHArms", edit=True, en=False)
        # cmds.rowLayout("laySoftIKHArms", edit=True, en=False)
        # cmds.rowLayout("layScaleIKHArms", edit=True, en=False)
        cmds.rowLayout("layReverseHandHArms", edit=True, en=False)
        cmds.rowLayout("layClavicleIKHArms", edit=True, en=False)
        cmds.radioButtonGrp("radClavicleTypeHArms", edit=True, sl=2)

def enableStretchIKHArm(*args):
    checkStretch = cmds.checkBoxGrp("cbxStretchIKHArms", q=True, v1=True)
    checkAutoManual = cmds.checkBoxGrp("cbxAutoManuPvHArms", q=True, v1=True)
    if checkAutoManual == True:
        if checkStretch == True:
            cmds.rowLayout("layStretckIKMultHArms", edit=True, en=True)
    if checkStretch == True:
        cmds.rowLayout("layClampStretchHArms", edit=True, en=True)
        cmds.rowLayout("laySquashIKHArms", edit=True, en=True)
        cmds.rowLayout("laySquashIKMultHArms", edit=True, en=True)
        cmds.rowLayout("layElbowLockHArms", edit=True, en=True)
    else:
        cmds.rowLayout("layStretckIKMultHArms", edit=True, en=False)
        cmds.rowLayout("layClampStretchHArms", edit=True, en=False)
        cmds.rowLayout("laySquashIKHArms", edit=True, en=False)
        cmds.rowLayout("laySquashIKMultHArms", edit=True, en=False)
        cmds.rowLayout("layElbowLockHArms", edit=True, en=False)

def enableStretchIKMultHArm(*args):
    checkStretch = cmds.checkBoxGrp("cbxStretchIKHArms", q=True, v1=True)
    checkAutoManual = cmds.checkBoxGrp("cbxAutoManuPvHArms", q=True, v1=True)
    if checkAutoManual == True:
        if checkStretch == True:
            cmds.rowLayout("layStretckIKMultHArms", edit=True, en=True)
    else:
        cmds.rowLayout("layStretckIKMultHArms", edit=True, en=False)

def enableRibbonHArm(*args):
    opt = cmds.optionMenuGrp("optEnRibbonHArms", q=True, v=True)
    if opt == "Enabled":
        cmds.rowLayout("layNumRibJntsHArms", edit=True, en=True)
        cmds.rowLayout("layBendCtrlsHArms", edit=True, en=True)
        cmds.rowLayout("layTweakCtrlsHArms", edit=True, en=True)
        cmds.rowLayout("layTwistAttrsHArms", edit=True, en=True)
        cmds.rowLayout("laySineAttrsHArms", edit=True, en=True)
        cmds.rowLayout("laySquashAttrsHArms", edit=True, en=True)
        cmds.rowLayout("layExtraFreeSlotsHArms", edit=True, en=True)
    else:
        cmds.rowLayout("layNumRibJntsHArms", edit=True, en=False)
        cmds.rowLayout("layBendCtrlsHArms", edit=True, en=False)
        cmds.rowLayout("layTweakCtrlsHArms", edit=True, en=False)
        cmds.rowLayout("layTwistAttrsHArms", edit=True, en=False)
        cmds.rowLayout("laySineAttrsHArms", edit=True, en=False)
        cmds.rowLayout("laySquashAttrsHArms", edit=True, en=False)
        cmds.rowLayout("layExtraFreeSlotsHArms", edit=True, en=False)

def enableExtraFreeSlotsHArm(*args):
    check = cmds.checkBoxGrp("cbxExtraFreeSlotsHArms", q=True, v1=True)
    if check == True:
        cmds.rowLayout("layNumExtraSlotsHArms", edit=True, en=True)
    else:
        cmds.rowLayout("layNumExtraSlotsHArms", edit=True, en=False)

def enableSpaceSwitchHArm(*args):
    opt = cmds.optionMenuGrp("optEnSpaceSwitchHArms", q=True, v=True)
    if opt == "Enabled":
        # cmds.rowLayout("layMethodHArms", edit=True, en=True)
        cmds.rowLayout("layArmsSpaceHArms", edit=True, en=True)
        cmds.rowLayout("layArmsSpaceListHArms", edit=True, en=True)
        cmds.rowLayout("layPvSpaceHArms", edit=True, en=True)
        cmds.rowLayout("layPvSpaceListHArms", edit=True, en=True)
    else:
        # cmds.rowLayout("layMethodHArms", edit=True, en=False)
        cmds.rowLayout("layArmsSpaceHArms", edit=True, en=False)
        cmds.rowLayout("layArmsSpaceListHArms", edit=True, en=False)
        cmds.rowLayout("layPvSpaceHArms", edit=True, en=False)
        cmds.rowLayout("layPvSpaceListHArms", edit=True, en=False)

def armsSpacesHArms(operation, *args):
    space = cmds.optionMenuGrp("optArmsSpaceHArms", q=True, v=True)
    listed = cmds.textScrollList("lstArmsSpaceListHArms", q=True, ai=True)
    if operation == "add":
        if listed == None:
            cmds.textScrollList("lstArmsSpaceListHArms", edit=True, a=[space])
        else:
            if space in listed:
                cmds.warning("Space already exists")
            else:
                cmds.textScrollList("lstArmsSpaceListHArms", edit=True, a=[space])
    elif operation == "rem":
        sel = cmds.textScrollList("lstArmsSpaceListHArms", q=True, si=True)
        if sel == None:
            cmds.warning("Select at least one space in the list")
        else:
            for s in sel:
                cmds.textScrollList("lstArmsSpaceListHArms", edit=True, ri=s)

def pvSpacesHArms(operation, *args):
    space = cmds.optionMenuGrp("optPvSpaceHArms", q=True, v=True)
    listed = cmds.textScrollList("lstPvSpaceListHArms", q=True, ai=True)
    if operation == "add":
        if listed == None:
            cmds.textScrollList("lstPvSpaceListHArms", edit=True, a=[space])
        else:
            if space in listed:
                cmds.warning("Space already exists")
            else:
                cmds.textScrollList("lstPvSpaceListHArms", edit=True, a=[space])
    elif operation == "rem":
        sel = cmds.textScrollList("lstPvSpaceListHArms", q=True, si=True)
        if sel == None:
            cmds.warning("Select at least one space in the list")
        else:
            for s in sel:
                cmds.textScrollList("lstPvSpaceListHArms", edit=True, ri=s)

def toggleReverseHandGuidesHArms(*args):
    pass
    # mult = cmds.radioButtonGrp("radMultArmsHArms", q=True, sl=True)
    # if mult == 1:
    #     guides.loadGuides().reloadGuides(nameComp="cbxReverseFootHArms", ctrlName="L")
    #     guides.loadGuides().reloadGuides(nameComp="cbxReverseFootHArms", ctrlName="R")
    # elif mult == 2:
    #     pass
