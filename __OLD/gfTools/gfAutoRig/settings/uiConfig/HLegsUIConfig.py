import maya.cmds as cmds
import maya.mel as mel
from functools import partial


from gfTools.__OLD.gfTools.gfAutoRig.settings import guides
from gfTools.__OLD.gfTools.gfAutoRig.settings import log
reload(guides); reload(log)


def multipleLegsHLegs(*args):
    multLegs = cmds.radioButtonGrp("radMultLegsHLegs", q=True, sl=True)
    # print ("Radio Button Active: %s") %(multLegs)
    if multLegs == 1:
        cmds.rowLayout("layMultLegsHLegs", edit=True, en=False)
        cmds.textField("txtNumberHLegs", edit=True, tx="2")
        cmds.button("btnAddLegHLegs", edit=True, en=True)
        cmds.button("btnRemLegHLegs", edit=True, en=False)
        childs = cmds.layout("layMultHumanLegsHLegs", q=True, ca=True)
        for c in childs:
            cmds.deleteUI(c)
        cmds.rowLayout("layMultLLegHLegs", w=310, nc=2, p="layMultHumanLegsHLegs")
        cmds.separator(w=5, h=3, st="none")
        cmds.frameLayout("frmLeftLegHLegs", w=312, cl=True, cll=True, bgs=True, l="Left Leg")
        cmds.textFieldGrp("txtLLegParentHLegs", l="Leg Parent: ", cw2=(110, 120), tx="None", ed=False)
        cmds.checkBoxGrp("cbxLLegHaveFingersHLegs", l="Have fingers: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(haveFingersHLegs, "LLeg"))
        cmds.rowLayout("layLLegNumFingersHLegs", nc=1, en=False)
        cmds.intSliderGrp("intLLegNumFingersHLegs", l="Number of fingers: ", cw=([(1, 110), (2, 40), (3, 130)]), f=True, min=3, max=6, fmn=3, fmx=6, v=5)
        cmds.rowLayout("layMultRLegHLegs", w=310, nc=2, p="layMultHumanLegsHLegs")
        cmds.separator(w=5, h=3, st="none")
        cmds.frameLayout("frmRightLegHLegs", w=310, cl=True, cll=True, bgs=True, l="Right Leg")
        cmds.textFieldGrp("txtRLegParentHLegs", l="Leg Parent: ", cw2=(120, 120), tx="None", ed=False)
        cmds.checkBoxGrp("cbxRLegHaveFingersHLegs", l="Have fingers: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(haveFingersHLegs, "RLeg"))
        cmds.rowLayout("layRLegNumFingersHLegs", nc=1, en=False)
        cmds.intSliderGrp("intRLegNumFingersHLegs", l="Number of fingers: ", cw=([(1, 110), (2, 40), (3, 130)]), f=True, min=3, max=6, fmn=3, fmx=6, v=5)
        log.buildLogHumanLeg(msg="multLegsPropUI", btn=multLegs, stop=False)
    elif multLegs == 2:
        cmds.rowLayout("layMultLegsHLegs", edit=True, en=True)
        cmds.textField("txtNumberHLegs", edit=True, tx="1")
        cmds.button("btnAddLegHLegs", edit=True, en=True)
        cmds.button("btnRemLegHLegs", edit=True, en=False)
        childs = cmds.layout("layMultHumanLegsHLegs", q=True, ca=True)
        for c in childs:
            cmds.deleteUI(c)
        cmds.rowLayout("layMultLeg1HLegs", w=310, nc=2, p="layMultHumanLegsHLegs")
        cmds.separator(w=5, h=3, st="none")
        cmds.frameLayout("frmLeg1HLegs", w=310, cl=True, cll=True, bgs=True, l="Leg 1")
        cmds.textFieldGrp("txtLeg1ParentHLegs", l="Leg Parent: ", cw2=(120, 120), tx="None", ed=False)
        cmds.optionMenuGrp("optLeg1SideHLegs", l="Side: ", cw2=(120, 120))
        cmds.menuItem(l="Left")
        cmds.menuItem(l="Right")
        cmds.checkBoxGrp("cbxLeg1HaveFingersHLegs", l="Have fingers: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(haveFingersHLegs, "Leg1"))
        cmds.rowLayout("layLeg1NumFingersHLegs", nc=1, en=False)
        cmds.intSliderGrp("intLeg1NumFingersHLegs", l="Number of fingers: ", cw=([(1, 110), (2, 40), (3, 130)]), f=True, min=3, max=6, fmn=3, fmx=6, v=5)
        log.buildLogHumanLeg(msg="multLegsPropUI", btn=multLegs, stop=False)
    log.buildLog(msg=None, stop=True)

def addHLegs(*args):
    num = cmds.textField("txtNumberHLegs", q=True, tx=True)
    newNum = 1
    newNum = int(num) + newNum
    cmds.textField("txtNumberHLegs", edit=True, tx=str(newNum))
    if newNum <= 1: cmds.button("btnRemLegHLegs", edit=True, en=False)
    elif newNum >= 10: cmds.button("btnAddLegHLegs", edit=True, en=False)
    else:
        cmds.button("btnRemLegHLegs", edit=True, en=True)
        cmds.button("btnAddLegHLegs", edit=True, en=True)
    # Add Layout
    cmds.rowLayout(("layMultLeg"+str(newNum)+"HLegs"), w=310, nc=2, p="layMultHumanLegsHLegs")
    cmds.separator(w=5, h=3, st="none")
    cmds.frameLayout(("frmLeg"+str(newNum)+"HLegs"), w=310, cl=True, cll=True, bgs=True, l=("Leg "+str(newNum)))
    cmds.textFieldGrp(("txtLeg"+str(newNum)+"ParentHLegs"), l="Leg Parent: ", cw2=(120, 120), tx="None", ed=False)
    cmds.optionMenuGrp(("optLeg"+str(newNum)+"SideHLegs"), l="Side: ", cw2=(120, 120))
    cmds.menuItem(l="Left")
    cmds.menuItem(l="Right")
    cmds.checkBoxGrp(("cbxLeg"+str(newNum)+"HaveFingersHLegs"), l="Have fingers: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(haveFingersHLegs, ("Leg"+str(newNum))))
    cmds.rowLayout(("layLeg"+str(newNum)+"NumFingersHLegs"), nc=1, en=False)
    cmds.intSliderGrp(("intLeg"+str(newNum)+"NumFingersHLegs"), l="Number of fingers: ", cw=([(1, 110), (2, 40), (3, 130)]), f=True, min=3, max=6, fmn=3, fmx=6, v=5)
    log.buildLogHumanLeg(msg="addRemLegsPropUI", btn="add", stop=True)

def remHLegs(*args):
    num = cmds.textField("txtNumberHLegs", q=True, tx=True)
    newNum = 1
    newNum = int(num) - newNum
    cmds.textField("txtNumberHLegs", edit=True, tx=str(newNum))
    if newNum <= 1: cmds.button("btnRemLegHLegs", edit=True, en=False)
    elif newNum >= 10: cmds.button("btnAddLegHLegs", edit=True, en=False)
    else:
        cmds.button("btnRemLegHLegs", edit=True, en=True)
        cmds.button("btnAddLegHLegs", edit=True, en=True)
    # Remove Layout
    cmds.deleteUI("layMultLeg"+str(num)+"HLegs")
    log.buildLogHumanLeg(msg="addRemLegsPropUI", btn="rem", stop=True)

def haveFingersHLegs(checkbox, *args):
    if checkbox == "LLeg": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHLegs"), q=True, v1=True)
    elif checkbox == "RLeg": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHLegs"), q=True, v1=True)
    elif checkbox == "Leg1": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHLegs"), q=True, v1=True)
    elif checkbox == "Leg2": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHLegs"), q=True, v1=True)
    elif checkbox == "Leg3": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHLegs"), q=True, v1=True)
    elif checkbox == "Leg4": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHLegs"), q=True, v1=True)
    elif checkbox == "Leg5": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHLegs"), q=True, v1=True)
    elif checkbox == "Leg6": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHLegs"), q=True, v1=True)
    elif checkbox == "Leg7": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHLegs"), q=True, v1=True)
    elif checkbox == "Leg8": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHLegs"), q=True, v1=True)
    elif checkbox == "Leg9": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHLegs"), q=True, v1=True)
    elif checkbox == "Leg10": check = cmds.checkBoxGrp(("cbx"+checkbox+"HaveFingersHLegs"), q=True, v1=True)
    if check == True:
        cmds.rowLayout(("lay"+checkbox+"NumFingersHLegs"), edit=True, en=True)
    else:
        cmds.rowLayout(("lay"+checkbox+"NumFingersHLegs"), edit=True, en=False)
    log.buildLogHumanLeg(msg="haveFingersLegsPropUI", btn=checkbox, stop=True)

def enableIKHLeg(*args):
    opt = cmds.optionMenuGrp("optEnIKHLegs", q=True, v=True)
    if opt == "Enabled":
        cmds.radioButtonGrp("radIKFKTypHLegs", edit=True, en=True)
        # cmds.rowLayout("layDualIKFKSeamHLegs", edit=True, en=True)
        cmds.rowLayout("layAutoManuPvHLegs", edit=True, en=True)
        cmds.rowLayout("layStretchIKHLegs", edit=True, en=True)
        # cmds.rowLayout("laySoftIKHLegs", edit=True, en=True)
        # cmds.rowLayout("layScaleIKHLegs", edit=True, en=True)
        cmds.rowLayout("layReverseFootHLegs", edit=True, en=True)
    else:
        cmds.radioButtonGrp("radIKFKTypHLegs", edit=True, en=False)
        # cmds.rowLayout("layDualIKFKSeamHLegs", edit=True, en=False)
        cmds.rowLayout("layAutoManuPvHLegs", edit=True, en=False)
        cmds.rowLayout("layStretchIKHLegs", edit=True, en=False)
        # cmds.rowLayout("laySoftIKHLegs", edit=True, en=False)
        # cmds.rowLayout("layScaleIKHLegs", edit=True, en=False)
        cmds.rowLayout("layReverseFootHLegs", edit=True, en=False)

def enableStretchIKHLeg(*args):
    checkStretch = cmds.checkBoxGrp("cbxStretchIKHLegs", q=True, v1=True)
    checkAutoManual = cmds.checkBoxGrp("cbxAutoManuPvHLegs", q=True, v1=True)
    if checkAutoManual == True:
        if checkStretch == True:
            cmds.rowLayout("layStretckIKMultHLegs", edit=True, en=True)
    if checkStretch == True:
        cmds.rowLayout("layClampStretchHLegs", edit=True, en=True)
        cmds.rowLayout("laySquashIKHLegs", edit=True, en=True)
        cmds.rowLayout("laySquashIKMultHLegs", edit=True, en=True)
        cmds.rowLayout("layKneeLockHLegs", edit=True, en=True)
    else:
        cmds.rowLayout("layStretckIKMultHLegs", edit=True, en=False)
        cmds.rowLayout("layClampStretchHLegs", edit=True, en=False)
        cmds.rowLayout("laySquashIKHLegs", edit=True, en=False)
        cmds.rowLayout("laySquashIKMultHLegs", edit=True, en=False)
        cmds.rowLayout("layKneeLockHLegs", edit=True, en=False)

def enableStretchIKMultHLeg(*args):
    checkStretch = cmds.checkBoxGrp("cbxStretchIKHLegs", q=True, v1=True)
    checkAutoManual = cmds.checkBoxGrp("cbxAutoManuPvHLegs", q=True, v1=True)
    if checkAutoManual == True:
        if checkStretch == True:
            cmds.rowLayout("layStretckIKMultHLegs", edit=True, en=True)
    else:
        cmds.rowLayout("layStretckIKMultHLegs", edit=True, en=False)

def enableRibbonHLeg(*args):
    opt = cmds.optionMenuGrp("optEnRibbonHLegs", q=True, v=True)
    if opt == "Enabled":
        cmds.rowLayout("layNumRibJntsHLegs", edit=True, en=True)
        cmds.rowLayout("layBendCtrlsHLegs", edit=True, en=True)
        cmds.rowLayout("layTweakCtrlsHLegs", edit=True, en=True)
        cmds.rowLayout("layTwistAttrsHLegs", edit=True, en=True)
        cmds.rowLayout("laySineAttrsHLegs", edit=True, en=True)
        cmds.rowLayout("laySquashAttrsHLegs", edit=True, en=True)
        cmds.rowLayout("layExtraFreeSlotsHLegs", edit=True, en=True)
    else:
        cmds.rowLayout("layNumRibJntsHLegs", edit=True, en=False)
        cmds.rowLayout("layBendCtrlsHLegs", edit=True, en=False)
        cmds.rowLayout("layTweakCtrlsHLegs", edit=True, en=False)
        cmds.rowLayout("layTwistAttrsHLegs", edit=True, en=False)
        cmds.rowLayout("laySineAttrsHLegs", edit=True, en=False)
        cmds.rowLayout("laySquashAttrsHLegs", edit=True, en=False)
        cmds.rowLayout("layExtraFreeSlotsHLegs", edit=True, en=False)

def enableExtraFreeSlotsHLeg(*args):
    check = cmds.checkBoxGrp("cbxExtraFreeSlotsHLegs", q=True, v1=True)
    if check == True:
        cmds.rowLayout("layNumExtraSlotsHLegs", edit=True, en=True)
    else:
        cmds.rowLayout("layNumExtraSlotsHLegs", edit=True, en=False)

def enableSpaceSwitchHLeg(*args):
    opt = cmds.optionMenuGrp("optEnSpaceSwitchHLegs", q=True, v=True)
    if opt == "Enabled":
        # cmds.rowLayout("layMethodHLegs", edit=True, en=True)
        cmds.rowLayout("layLegsSpaceHLegs", edit=True, en=True)
        cmds.rowLayout("layLegsSpaceListHLegs", edit=True, en=True)
        cmds.rowLayout("layPvSpaceHLegs", edit=True, en=True)
        cmds.rowLayout("layPvSpaceListHLegs", edit=True, en=True)
    else:
        # cmds.rowLayout("layMethodHLegs", edit=True, en=False)
        cmds.rowLayout("layLegsSpaceHLegs", edit=True, en=False)
        cmds.rowLayout("layLegsSpaceListHLegs", edit=True, en=False)
        cmds.rowLayout("layPvSpaceHLegs", edit=True, en=False)
        cmds.rowLayout("layPvSpaceListHLegs", edit=True, en=False)

def legsSpacesHLegs(operation, *args):
    space = cmds.optionMenuGrp("optLegsSpaceHLegs", q=True, v=True)
    listed = cmds.textScrollList("lstLegsSpaceListHLegs", q=True, ai=True)
    if operation == "add":
        if listed == None:
            cmds.textScrollList("lstLegsSpaceListHLegs", edit=True, a=[space])
        else:
            if space in listed:
                cmds.warning("Space already exists")
            else:
                cmds.textScrollList("lstLegsSpaceListHLegs", edit=True, a=[space])
    elif operation == "rem":
        sel = cmds.textScrollList("lstLegsSpaceListHLegs", q=True, si=True)
        if sel == None:
            cmds.warning("Select at least one space in the list")
        else:
            for s in sel:
                cmds.textScrollList("lstLegsSpaceListHLegs", edit=True, ri=s)

def pvSpacesHLegs(operation, *args):
    space = cmds.optionMenuGrp("optPvSpaceHLegs", q=True, v=True)
    listed = cmds.textScrollList("lstPvSpaceListHLegs", q=True, ai=True)
    if operation == "add":
        if listed == None:
            cmds.textScrollList("lstPvSpaceListHLegs", edit=True, a=[space])
        else:
            if space in listed:
                cmds.warning("Space already exists")
            else:
                cmds.textScrollList("lstPvSpaceListHLegs", edit=True, a=[space])
    elif operation == "rem":
        sel = cmds.textScrollList("lstPvSpaceListHLegs", q=True, si=True)
        if sel == None:
            cmds.warning("Select at least one space in the list")
        else:
            for s in sel:
                cmds.textScrollList("lstPvSpaceListHLegs", edit=True, ri=s)
                
def toggleReverseFootGuidesHLegs(*args):
    mult = cmds.radioButtonGrp("radMultLegsHLegs", q=True, sl=True)
    if mult == 1:
        guides.loadGuides().reloadGuides(nameComp="cbxReverseFootHLegs", ctrlName="L")
        guides.loadGuides().reloadGuides(nameComp="cbxReverseFootHLegs", ctrlName="R")
    elif mult == 2:
        pass
