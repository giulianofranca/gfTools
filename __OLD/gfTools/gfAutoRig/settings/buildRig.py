import maya.cmds as cmds
import maya.mel as mel
from functools import partial


from gfTools.__OLD.gfTools.gfAutoRig.settings import log
from gfTools.__OLD.gfTools.gfAutoRig.settings.uiConfig import masterUIConfig
from gfTools.__OLD.gfTools.gfAutoRig.components import humanLegs as HLegs
from gfTools.__OLD.gfTools.gfAutoRig.components import humanArms as HArms
from gfTools.__OLD.gfTools.gfAutoRig.components import humanSpine as HSpine
from gfTools.__OLD.gfTools.gfAutoRig.components import humanHeads as HHeads
from gfTools.__OLD.gfTools.gfAutoRig.settings import controls as ctrl
reload(log); reload(masterUIConfig); reload(HLegs); reload(HSpine); reload(HHeads); reload(ctrl)


class buildRig(object):

    def __init__(self, path="", *args):
        cmds.select(cl=True)
        # Char name already exists. You want to merge components?
        self.jntsBnd = []
        self.jntsDrv = []
        self.jntsRib = []
        self.charInfo = []
        self.scriptPath = path
        # self.slotGblSca = False
        self.charName = cmds.textFieldGrp("txtCharName", q=True, tx=True)
        self.charType = cmds.optionMenu("optCharType", q=True, v=True)
        # if self.charName != "":
        #     if self.charType != "Select Type":
        # Block All Buttons
        ''' PARA FAZER'''
        # Lock Master Features Transformations
        cmds.select("gfARGuides:Ctrl_Global")
        cmds.CenterPivot()
        self.setupFull = cmds.radioButtonGrp("radCompSetupMFeat", q=True, sl=True)
        if self.setupFull == 1:
            setupGbl()
        # View Log
        cmds.tabLayout("tabChar", edit=True, st="layLog")
        # Build Components
        components = self._verifyComponents()
        for c in components:
            self._build(c)
            cmds.scrollLayout("promptLog", edit=True, sp=("down"))

        # Setup Spaces

        # Document Guides History in Node
        ''' PARA FAZER '''
        # Delete Guides
        masterUIConfig.config().reloadCharField("", True, "NDA", False)
        cmds.frameLayout("frmGlobalControlMFeat", edit=True, cl=True, en=False)
        cmds.frameLayout("frmMasterControlMFeat", edit=True, cl=True, en=False)
        cmds.frameLayout("frmExtraSettingsMFeat", edit=True, cl=True, en=False)
        cmds.frameLayout("frmOutputSettingsMFeat", edit=True, cl=False, en=True)
        # cmds.rowLayout("layJntBndSizeMFeat", edit=True, en=True)
        # cmds.rowLayout("layFinishRigMFeat", edit=True, en=True)
        # Output Settings
        commandList = []
        for j in self.jntsBnd: commandList.append((', "'+j+'.radius"'))
        command = ''.join(commandList)
        finalCommand = ('cmds.connectControl("fltJntBndSizeMFeat"'+command+')')
        cmds.rowLayout("layJntBndSizeMFeat", nc=1, en=True, parent="frmOutputSettingsMFeat")
        cmds.floatSliderGrp("fltJntBndSizeMFeat", l="JntBnd Size: ", cw=([(1, 110), (2, 50), (3, 130)]), f=True, min=0, max=5, fmn=0, fmx=50, v=1) #0.4
        cmds.setParent('..')
        exec(finalCommand)
        if self.jntsDrv != []:
            commandList = []
            for j in self.jntsDrv: commandList.append((', "'+j+'.radius"'))
            command = ''.join(commandList)
            finalCommand = ('cmds.connectControl("fltJntDrvSizeMFeat"'+command+')')
            cmds.rowLayout("layJntDrvSizeMFeat", nc=1, en=True, parent="frmOutputSettingsMFeat")
            cmds.floatSliderGrp("fltJntDrvSizeMFeat", l="JntDrv Size: ", cw=([(1, 110), (2, 50), (3, 130)]), f=True, min=0, max=5, fmn=0, fmx=50, v=1) #0.2
            cmds.setParent('..')
            exec(finalCommand)
        if self.jntsRib != []:
            commandList = []
            for j in self.jntsRib: commandList.append((', "'+j+'.radius"'))
            command = ''.join(commandList)
            finalCommand = ('cmds.connectControl("fltJntRibSizeMFeat"'+command+')')
            cmds.rowLayout("layJntRibSizeMFeat", nc=1, en=True, parent="frmOutputSettingsMFeat")
            cmds.floatSliderGrp("fltJntRibSizeMFeat", l="JntRib Size: ", cw=([(1, 110), (2, 50), (3, 130)]), f=True, min=0, max=5, fmn=0, fmx=50, v=1) #0.5
            cmds.setParent('..')
            exec(finalCommand)
        cmds.scrollLayout("promptLog", edit=True, sp=("down"))
        cmds.rowLayout("layFinishRigMFeat", nc=2, en=True)
        cmds.separator(w=40, h=3, st="none")
        cmds.button(l="Finish Rig", w=230, h=25, c=finishRig)
        cmds.setParent('..')
        #     else: cmds.warning("Select the type of your character!")
        # else: cmds.warning("Type the name of your character!")




    def _verifyComponents(self):
        Childs = cmds.layout("scrOutputs", q=True, ca=True)
        return Childs

    def _build(self, comp):
        jBnd = []
        jDrv = []
        jRib = []
        if comp == "compHumanSpine":
            bnd, drv, rib, HumanSpine = HSpine.buildHumanSpine().getInfo()
            print ("\nJntBnd = %s") %(bnd), ("\nJntDrv = %s") %(drv), ("\nJntRib = %s") %(rib), ("\nSpine info = %s") %(HumanSpine)
            self.jntsBnd.extend(bnd)
            self.jntsDrv.extend(drv)
            self.jntsRib.extend(rib)
            # self.charInfo.append(HumanSpine)
        elif comp == "compHumanLegs":
            log.buildLogHumanLeg(msg="startBuildHumanLeg", btn="All", stop=False)
            haveMultLegs = cmds.radioButtonGrp("radMultLegsHLegs", q=True, sl=True)
            if haveMultLegs == 1:
                bnd, drv, rib, HumanLLeg = HLegs.buildHumanLeg(name="LLeg", side="left", path=self.scriptPath).getInfo()
                print ("\nJntBnd = %s") %(bnd), ("\nJntDrv = %s") %(drv), ("\nJntRib = %s") %(rib), ("\nLeg name = %s | Leg side = %s") %(HumanLLeg[0], HumanLLeg[1])
                self.jntsBnd.extend(bnd)
                self.jntsDrv.extend(drv)
                self.jntsRib.extend(rib)
                bnd, drv, rib, HumanRLeg = HLegs.buildHumanLeg(name="RLeg", side="right", path=self.scriptPath).getInfo()
                print ("\nJntBnd = %s") %(bnd), ("\nJntDrv = %s") %(drv), ("\nJntRib = %s") %(rib), ("\nLeg name = %s | Leg side = %s") %(HumanRLeg[0], HumanRLeg[1])
                self.jntsBnd.extend(bnd)
                self.jntsDrv.extend(drv)
                self.jntsRib.extend(rib)
            elif haveMultLegs == 2:
                pass
        elif comp == "compHumanArms":
            haveMultArms = cmds.radioButtonGrp("radMultArmsHArms", q=True, sl=True)
            if haveMultArms == 1:
                bnd, drv, rib, HumanLArm = HArms.buildHumanArm(name="LArm", side="left").getInfo()
                print ("\nJntBnd = %s") %(bnd), ("\nJntDrv = %s") %(drv), ("\nJntRib = %s") %(rib), ("\nArm name = %s | Arm side = %s") %(HumanLArm[0], HumanLArm[1])
                self.jntsBnd.extend(bnd)
                self.jntsDrv.extend(drv)
                self.jntsRib.extend(rib)
                bnd, drv, rib, HumanRArm = HArms.buildHumanArm(name="RArm", side="right").getInfo()
                print ("\nJntBnd = %s") %(bnd), ("\nJntDrv = %s") %(drv), ("\nJntRib = %s") %(rib), ("\nArm name = %s | Arm side = %s") %(HumanRArm[0], HumanRArm[1])
                self.jntsBnd.extend(bnd)
                self.jntsDrv.extend(drv)
                self.jntsRib.extend(rib)
            elif haveMultArms == 2:
                pass
        elif comp == "compHumanHead":
            bnd, drv, rib, HumanHeads = HHeads.buildHumanHeads().getInfo()
            print ("\nJntBnd = %s") %(bnd), ("\nJntDrv = %s") %(drv), ("\nJntRib = %s") %(rib), ("\nHeads info = %s") %(HumanHeads)
            self.jntsBnd.extend(bnd)
            self.jntsDrv.extend(drv)
            self.jntsRib.extend(rib)
            # self.charInfo.append(HumanHeads)

class finishRig(object):

    def __init__(self, *args):
        cmds.tabLayout("tabChar", edit=True, st="layRig")
        cmds.frameLayout("frmGlobalControlMFeat", edit=True, cl=False, en=True)
        cmds.frameLayout("frmMasterControlMFeat", edit=True, cl=False, en=True)
        cmds.frameLayout("frmExtraSettingsMFeat", edit=True, cl=True, en=True)
        cmds.frameLayout("frmOutputSettingsMFeat", edit=True, cl=True, en=False)
        cmds.deleteUI("layJntBndSizeMFeat")
        if cmds.rowLayout("layJntDrvSizeMFeat", q=True, ex=True):
            cmds.deleteUI("layJntDrvSizeMFeat")
        if cmds.rowLayout("layJntRibSizeMFeat", q=True, ex=True):
            cmds.deleteUI("layJntRibSizeMFeat")
        cmds.deleteUI("layFinishRigMFeat")
        cmds.textFieldGrp("txtCharName", edit=True, tx="")
        cmds.optionMenu("optCharType", edit=True, v="Select Type")
        # jntsDrivers = cmds.ls("*JntDrv*", type="joint")
        # for jnt in jntsDrivers:
        #     cmds.setAttr((jnt+".drawStyle"), 2)

class setupGbl(object):

    def __init__(self, *args):
        self.charName = cmds.textFieldGrp("txtCharName", q=True, tx=True)
        self.haveTrack = cmds.checkBoxGrp("cbxTrackingCtrlMFeat", q=True, v1=True)
        self.haveMaster = cmds.optionMenuGrp("optEnMasterCtrlMFeat", q=True, v=True)
        self.haveGblSca = cmds.checkBoxGrp("cbxGlobalScaleMFeat", q=True, v1=True)
        self.gblCtrlSca = cmds.floatSliderGrp("fltGblCtrlScaMFeat", q=True, v=True)
        self.gblCtrlPos = cmds.xform("gfARGuides:Ctrl_Global", q=True, ws=True, rp=True)
        self.gblScaleGuide = cmds.xform("gfARGuides:Ctrl_Global", q=True, r=True, s=True)
        # Criar atributo draw style em alguns grupos
        self._setup()

    def _setup(self):
        grps = self.createHierarchy()
        ctrlGbl = ctrl.Control(n="Ctrl_Global", t="Global", s=3.6, c="Global") # LightYellow
        if self.haveGblSca == True:
            cmds.addAttr(("|"+str(ctrlGbl)), ln="GLOBAL", nn="__________________ GLOBAL", at="enum", en="__________:")
            cmds.addAttr(("|"+str(ctrlGbl)), ln="GlobalScale", at="double", min=0.01, dv=1)
            cmds.setAttr(("|"+str(ctrlGbl)+".GLOBAL"), edit=True, channelBox=True)
            cmds.setAttr(("|"+str(ctrlGbl)+".GlobalScale"), edit=True, k=True)
            cmds.connectAttr((str(ctrlGbl)+".GlobalScale"), (str(ctrlGbl)+".sx"))
            cmds.connectAttr((str(ctrlGbl)+".GlobalScale"), (str(ctrlGbl)+".sy"))
            cmds.connectAttr((str(ctrlGbl)+".GlobalScale"), (str(ctrlGbl)+".sz"))
        ctrl.Control(n=str(ctrlGbl), t="Lock and Hide", s=["sx", "sy", "sz", "v"])
        grpGbl = cmds.group(n="Grp_Ctrl_Global")
        cmds.scale((self.gblCtrlSca * self.gblScaleGuide[0]), (self.gblCtrlSca * self.gblScaleGuide[0]), (self.gblCtrlSca * self.gblScaleGuide[0]), r=True)
        cmds.move(self.gblCtrlPos[0], self.gblCtrlPos[1], self.gblCtrlPos[2], r=True)
        if self.haveTrack == True:
            ctrlTrack1 = ctrl.Control(n="Ctrl_Track_1", t="Track", s=3.8, c="Extra") # Magenta
            grpTrack1 = cmds.group(n="Grp_Ctrl_Track_1")
            cmds.scale((self.gblCtrlSca * self.gblScaleGuide[0]), (self.gblCtrlSca * self.gblScaleGuide[0]), (self.gblCtrlSca * self.gblScaleGuide[0]), r=True)
            cmds.move(self.gblCtrlPos[0], self.gblCtrlPos[1], self.gblCtrlPos[2], r=True)
            ctrlTrack2 = ctrl.Control(n="Ctrl_Track_2", t="Track", s=3.2, c="Extra") # Purple
            grpTrack2 = cmds.group(n="Grp_Ctrl_Track_2")
            cmds.scale((self.gblCtrlSca * self.gblScaleGuide[0]), (self.gblCtrlSca * self.gblScaleGuide[0]), (self.gblCtrlSca * self.gblScaleGuide[0]), r=True)
            cmds.move(self.gblCtrlPos[0], self.gblCtrlPos[1], self.gblCtrlPos[2], r=True)
            cmds.addAttr(("|"+str(grpGbl)+"|"+str(ctrlGbl)), ln="XtraControls", at="bool")
            cmds.setAttr(("|"+str(grpGbl)+"|"+str(ctrlGbl)+".XtraControls"), edit=True, k=True)
            cmds.setAttr((str(ctrlGbl)+".XtraControls"), True)
            ctrlTrack1Shape = cmds.listRelatives(str(ctrlTrack1), s=True)[0]
            ctrlTrack2Shape = cmds.listRelatives(str(ctrlTrack2), s=True)[0]
            cmds.connectAttr((str(ctrlGbl)+".XtraControls"), (ctrlTrack1Shape+".visibility"))
            cmds.connectAttr((str(ctrlGbl)+".XtraControls"), (ctrlTrack2Shape+".visibility"))
            cmds.parent(grpTrack2, ctrlTrack1)
            cmds.parent(grpGbl, ctrlTrack2)
            cmds.parent(grpTrack1, "Grp_Ctrl_Gbl")
            ctrl.Control(n=str(ctrlTrack1), t="Lock and Hide", s=["sx", "sy", "sz", "v"])
            ctrl.Control(n=str(ctrlTrack2), t="Lock and Hide", s=["sx", "sy", "sz", "v"])
        else: cmds.parent(grpGbl, "Grp_Ctrl_Gbl")
        cmds.select(str(ctrlGbl), "Grp_Gbl", r=True)
        cmds.parentConstraint(weight=1, mo=True)
        if self.haveGblSca == True: cmds.scaleConstraint(weight=1, mo=True)
        for grp in grps:
            ctrl.Control(n=grp, t="Lock and Hide", s=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])


    def createHierarchy(self):
        grpsHierarchy = []
        charNameFiltered = ""
        for char in self.charName:
            if char == " ": charNameFiltered += "_"
            else: charNameFiltered += char
        grpChar = cmds.group(empty=True, n=("Grp_"+charNameFiltered))
        grpsHierarchy.append(grpChar)
        cmds.setAttr((grpChar+".useOutlinerColor"), 1)
        cmds.setAttr((grpChar+".outlinerColorR"), 0.18039)
        cmds.setAttr((grpChar+".outlinerColorG"), 0.80000)
        cmds.setAttr((grpChar+".outlinerColorB"), 0.44314)
        grpGbl = cmds.group(empty=True, n="Grp_Gbl")
        grpsHierarchy.append(grpGbl)
        grpSktn = cmds.group(empty=True, n="Grp_Sktn")
        grpsHierarchy.append(grpSktn)
        grpCtrl = cmds.group(empty=True, n="Grp_Ctrl")
        grpsHierarchy.append(grpCtrl)
        grpIk = cmds.group(empty=True, n="Grp_ikHdle")
        grpsHierarchy.append(grpIk)
        grpCtrlGbl = cmds.group(empty=True, n="Grp_Ctrl_Gbl")
        grpsHierarchy.append(grpCtrlGbl)
        grpGeo = cmds.group(empty=True, n="Grp_Geo")
        grpsHierarchy.append(grpGeo)
        grpPSD = cmds.group(empty=True, n="Grp_PSD")
        grpsHierarchy.append(grpPSD)
        grpXtra = cmds.group(empty=True, n="Grp_Xtra")
        grpsHierarchy.append(grpXtra)
        grpXtraShow = cmds.group(empty=True, n="Grp_Xtra_ToShow")
        grpsHierarchy.append(grpXtraShow)
        grpXtraHide = cmds.group(empty=True, n="Grp_Xtra_ToHide")
        grpsHierarchy.append(grpXtraHide)
        cmds.parent(grpSktn, grpGbl)
        cmds.parent(grpCtrl, grpGbl)
        cmds.parent(grpIk, grpGbl)
        cmds.parent(grpXtraShow, grpXtra)
        cmds.parent(grpXtraHide, grpXtra)
        cmds.parent(grpGbl, grpChar)
        cmds.parent(grpCtrlGbl, grpChar)
        cmds.parent(grpGeo, grpChar)
        cmds.parent(grpPSD, grpChar)
        cmds.parent(grpXtra, grpChar)
        cmds.select(cl=True)
        cmds.setAttr((grpIk+".v"), False)
        cmds.setAttr((grpIk+".overrideEnabled"), True)
        cmds.setAttr((grpIk+".overrideDisplayType"), 2)
        cmds.setAttr((grpGeo+".overrideEnabled"), True)
        cmds.setAttr((grpGeo+".overrideDisplayType"), 2)
        cmds.setAttr((grpPSD+".v"), False)
        cmds.setAttr((grpPSD+".overrideEnabled"), True)
        cmds.setAttr((grpPSD+".overrideDisplayType"), 2)
        cmds.setAttr((grpXtraHide+".v"), False)
        cmds.setAttr((grpXtraHide+".overrideEnabled"), True)
        cmds.setAttr((grpXtraHide+".overrideDisplayType"), 2)
        return grpsHierarchy
