import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import math, os


from gfTools.__OLD.gfTools.gfAutoRig.settings import log
from gfTools.__OLD.gfTools.gfAutoRig.settings import controls as ctrl
reload(log); reload(ctrl)


class buildHumanLeg(object):
    # numInst = 0

    def __init__(self, name="", side="", path=""):
        self.name = name
        self.side = side
        self.jntsBnd = []
        self.jntsDrv = []
        self.jntsRib = []
        self.scriptPath = path
        log.buildLogHumanLeg(msg="startBuildHumanLeg", btn=self.name, stop=False)
        log.buildLog(msg="whiteLine", stop=False)
        if self.side == "left": self.side = "L"
        elif self.side == "right": self.side = "R"
        else: cmds.error(("Leg ("+name+") side don't recognized"))
        # --------------------------------------------------------------------------------------------------------------
        # READ FEATURES                        | CheckBox = True/False | RadioBtn = 1/2 | OptionMenu = Enabled/Disabled
        log.buildLogHumanLeg(msg="readFeatures", btn="Start", stop=False)
        # <<<------------------- PARA FAZER: Unique Hip
        self.haveMultLegs = cmds.radioButtonGrp("radMultLegsHLegs", q=True, sl=True)
        self.haveStretchFK = cmds.checkBoxGrp("cbxStretchFKHLegs", q=True, v1=True)
        self.haveSquashFK = cmds.checkBoxGrp("cbxSquashFKHLegs", q=True, v1=True)
        # <<<------------------- PARA FAZER: Scale Legs FK
        self.haveIK = cmds.optionMenuGrp("optEnIKHLegs", q=True, v=True)
        self.switchType = cmds.radioButtonGrp("radIKFKTypHLegs", q=True, sl=True)
        self.haveAutoPv = cmds.checkBoxGrp("cbxAutoManuPvHLegs", q=True, v1=True)
        # <<<------------------- PARA FAZER: Dual IK/FK seamless
        self.haveStretchIK = cmds.checkBoxGrp("cbxStretchIKHLegs", q=True, v1=True)
        self.haveStretchMultIK = cmds.checkBoxGrp("cbxStretckIKMultHLegs", q=True, v1=True)
        self.haveClampStretchIK = cmds.checkBoxGrp("cbxClampStretchHLegs", q=True, v1=True)
        self.haveSquashIK = cmds.checkBoxGrp("cbxHLegSquashIK", q=True, v1=True)
        self.haveSquashMultIK = cmds.checkBoxGrp("cbxSquashIKMultHLegs", q=True, v1=True)
        self.haveKneeLockIK = cmds.checkBoxGrp("cbxKneeLockHLegs", q=True, v1=True)
        # <<<------------------- PARA FAZER: Soft IK
        # <<<------------------- PARA FAZER: Scale Legs IK
        self.haveReverseFoot = cmds.checkBoxGrp("cbxReverseFootHLegs", q=True, v1=True)
        self.haveRibbon = cmds.optionMenuGrp("optEnRibbonHLegs", q=True, v=True)
        self.numberOfJntsRib = cmds.intSliderGrp("intNumRibJntsHLegs", q=True, v=True)
        self.haveBendCtrlsRib = cmds.checkBoxGrp("cbxBendCtrlsHLegs", q=True, v1=True)
        self.haveTweakCtrlsRib = cmds.checkBoxGrp("cbxTweakCtrlsHLegs", q=True, v1=True)
        self.haveTwistAttrsRib = cmds.checkBoxGrp("cbxTwistAttrsHLegs", q=True, v1=True)
        self.haveSineAttrsRib = cmds.checkBoxGrp("cbxSineAttrsHLegs", q=True, v1=True)
        self.haveSquashAttrsRib = cmds.checkBoxGrp("cbxSquashAttrsHLegs", q=True, v1=True)
        self.haveExtraFreeSlotsRib = cmds.checkBoxGrp("cbxExtraFreeSlotsHLegs", q=True, v1=True)
        self.numberOfFreeSlotsRib = cmds.intSliderGrp("intNumExtraSlotsHLegs", q=True, v=True)
        self.haveSpaceSwitch = cmds.optionMenuGrp("optEnSpaceSwitchHLegs", q=True, v=True)
        log.buildLogHumanLeg(msg="readFeatures", btn="All", stop=False)
        log.buildLog(msg="whiteLine", stop=False)
        # --------------------------------------------------------------------------------------------------------------
        # FIND GUIDES TRANSFORMATIONS
        log.buildLogHumanLeg(msg="foundGuidesTrans", btn="Start", stop=False)
        self.gblScaleGuide = cmds.xform("gfARGuides:Ctrl_Global", q=True, r=True, s=True)
        self.gblScale = cmds.checkBoxGrp("cbxGlobalScaleMFeat", q=True, v1=True)
        self.setupFull = cmds.radioButtonGrp("radCompSetupMFeat", q=True, sl=True)
        if self.haveMultLegs == 1:
            if cmds.objExists(("gfARGuides:Ctrl_"+self.side+"_Thigh")):
                self.posThigh = cmds.xform(("gfARGuides:Ctrl_"+self.side+"_Thigh"), q=True, ws=True, rp=True)
                log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.side+"_Thigh"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.side+"_Shin")):
                self.posShin = cmds.xform(("gfARGuides:Ctrl_"+self.side+"_Shin"), q=True, ws=True, rp=True)
                log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.side+"_Shin"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.side+"_Ankle")):
                self.posAnkle = cmds.xform(("gfARGuides:Ctrl_"+self.side+"_Ankle"), q=True, ws=True, rp=True)
                log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.side+"_Ankle"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.side+"_Toe")):
                self.posToe = cmds.xform(("gfARGuides:Ctrl_"+self.side+"_Toe"), q=True, ws=True, rp=True)
                log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.side+"_Toe"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.side+"_LegEnd")):
                self.posLegEnd = cmds.xform(("gfARGuides:Ctrl_"+self.side+"_LegEnd"), q=True, ws=True, rp=True)
                log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.side+"_LegEnd"), stop=False)
            else: cmds.error("!!")
            if self.haveReverseFoot == True:
                if cmds.objExists(("gfARGuides:Ctrl_"+self.side+"_TipHeel")):
                    self.posTipHeel = cmds.xform(("gfARGuides:Ctrl_"+self.side+"_TipHeel"), q=True, ws=True, rp=True)
                    log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.side+"_TipHeel"), stop=False)
                else: cmds.error("!!")
                if cmds.objExists(("gfARGuides:Ctrl_"+self.side+"_InFoot")):
                    self.posInFoot = cmds.xform(("gfARGuides:Ctrl_"+self.side+"_InFoot"), q=True, ws=True, rp=True)
                    log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.side+"_InFoot"), stop=False)
                else: cmds.error("!!")
                if cmds.objExists(("gfARGuides:Ctrl_"+self.side+"_OutFoot")):
                    self.posOutFoot = cmds.xform(("gfARGuides:Ctrl_"+self.side+"_OutFoot"), q=True, ws=True, rp=True)
                    log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.side+"_OutFoot"), stop=False)
                else: cmds.error("!!")
                if cmds.objExists(("gfARGuides:Ctrl_"+self.side+"_TipFoot")):
                    self.posTipFoot = cmds.xform(("gfARGuides:Ctrl_"+self.side+"_TipFoot"), q=True, ws=True, rp=True)
                    log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.side+"_TipFoot"), stop=False)
                else: cmds.error("!!")
        elif self.haveMultLegs == 2:
            if cmds.objExists(("gfARGuides:Ctrl_"+self.name+"_Thigh")):
                self.posThigh = cmds.xform(("gfARGuides:Ctrl_"+self.name+"_Thigh"), q=True, ws=True, rp=True)
                log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.name+"_Thigh"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.name+"_Shin")):
                self.posShin = cmds.xform(("gfARGuides:Ctrl_"+self.name+"_Shin"), q=True, ws=True, rp=True)
                log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.name+"_Shin"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.name+"_Ankle")):
                self.posAnkle = cmds.xform(("gfARGuides:Ctrl_"+self.name+"_Ankle"), q=True, ws=True, rp=True)
                log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.name+"_Ankle"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.name+"_Toe")):
                self.posToe = cmds.xform(("gfARGuides:Ctrl_"+self.name+"_Toe"), q=True, ws=True, rp=True)
                log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.name+"_Toe"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.name+"_LegEnd")):
                self.posLegEnd = cmds.xform(("gfARGuides:Ctrl_"+self.name+"_LegEnd"), q=True, ws=True, rp=True)
                log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.name+"_LegEnd"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.name+"_TipHeel")):
                self.posTipHeel = cmds.xform(("gfARGuides:Ctrl_"+self.name+"_TipHeel"), q=True, ws=True, rp=True)
                log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.name+"_TipHeel"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.name+"_InFoot")):
                self.posInFoot = cmds.xform(("gfARGuides:Ctrl_"+self.name+"_InFoot"), q=True, ws=True, rp=True)
                log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.name+"_InFoot"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.name+"_OutFoot")):
                self.posOutFoot = cmds.xform(("gfARGuides:Ctrl_"+self.name+"_OutFoot"), q=True, ws=True, rp=True)
                log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.name+"_OutFoot"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.name+"_TipFoot")):
                self.posTipFoot = cmds.xform(("gfARGuides:Ctrl_"+self.name+"_TipFoot"), q=True, ws=True, rp=True)
                log.buildLogHumanLeg(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.name+"_TipFoot"), stop=False)
            else: cmds.error("!!")
        log.buildLogHumanLeg(msg="foundGuidesTrans", btn="All", stop=False)
        log.buildLog(msg="whiteLine", stop=False)

        self.build()
        # print ("\nGlobal scale: %s") %(self.gblScaleGuide)

    # def __new__(cls, *args):
    #     pass

    def __del__(self): # Deletar a perna
        pass

    def __len__(self):pass
        #return numLegs

    def __repr__(self):
        return 'buildHumanLeg({}, {})'.format(self.name, self.side)

    def __str__(self):
        return 'Leg name: {} | Leg side: {}'.format(self.name, self.side)

    def getInfo(self):
        legInfo = [self.name, self.side]
        return self.jntsBnd, self.jntsDrv, self.jntsRib, legInfo

    def build(self):
        cmds.select(cl=True)
        # If method == Maya Nodes
        # Setting Joints Variables
        log.buildLogHumanLeg(msg="settingJntsVariables", stop=False)
        jnts = []
        if self.haveMultLegs == 1:
            if self.haveRibbon == "Enabled":
                thighRes = ("JntDrv_"+self.side+"_Thigh"); shinRes = ("JntDrv_"+self.side+"_Shin")
                ankleRes = ("JntBnd_"+self.side+"_Ankle"); toeRes = ("JntBnd_"+self.side+"_Toe")
                legEndRes = ("JntBnd_"+self.side+"_LegEnd")
                jnts.append(thighRes); jnts.append(shinRes); jnts.append(ankleRes); jnts.append(toeRes); jnts.append(legEndRes)
            elif self.haveRibbon == "Disabled":
                thighRes = ("JntBnd_"+self.side+"_Thigh"); shinRes = ("JntBnd_"+self.side+"_Shin")
                ankleRes = ("JntBnd_"+self.side+"_Ankle"); toeRes = ("JntBnd_"+self.side+"_Toe")
                legEndRes = ("JntBnd_"+self.side+"_LegEnd")
                jnts.append(thighRes); jnts.append(shinRes); jnts.append(ankleRes); jnts.append(toeRes); jnts.append(legEndRes)
            if self.haveIK == "Enabled":
                thighFK = ("JntDrv_"+self.side+"_FK_Thigh"); shinFK = ("JntDrv_"+self.side+"_FK_Shin")
                ankleFK = ("JntDrv_"+self.side+"_FK_Ankle"); toeFK = ("JntDrv_"+self.side+"_FK_Toe")
                legEndFK = ("JntDrv_"+self.side+"_FK_LegEnd"); thighIK = ("JntDrv_"+self.side+"_IK_Thigh")
                shinIK = ("JntDrv_"+self.side+"_IK_Shin"); ankleIK = ("JntDrv_"+self.side+"_IK_Ankle")
                toeIK = ("JntDrv_"+self.side+"_IK_Toe"); legEndIK = ("JntDrv_"+self.side+"_IK_LegEnd")
                jnts.append(thighFK); jnts.append(shinFK); jnts.append(ankleFK); jnts.append(toeFK); jnts.append(legEndFK)
                jnts.append(thighIK); jnts.append(shinIK); jnts.append(ankleIK); jnts.append(toeIK); jnts.append(legEndIK)
            if self.haveAutoPv == True:
                thighPv = ("JntDrv_"+self.side+"_Pv_Thigh"); shinPv = ("JntDrv_"+self.side+"_Pv_Shin")
                anklePv = ("JntDrv_"+self.side+"_Pv_Ankle"); thighNoFlip = ("JntDrv_"+self.side+"_NoFlip_Thigh")
                shinNoFlip = ("JntDrv_"+self.side+"_NoFlip_Shin"); ankleNoFlip = ("JntDrv_"+self.side+"_NoFlip_Ankle")
                jnts.append(thighPv); jnts.append(shinPv); jnts.append(anklePv)
                jnts.append(thighNoFlip); jnts.append(shinNoFlip); jnts.append(ankleNoFlip)
        elif self.haveMultLegs == 2:
            if self.haveRibbon == "Enabled":
                thighRes = ("JntDrv_"+self.name+"_Thigh"); shinRes = ("JntDrv_"+self.name+"_Shin")
                ankleRes = ("JntDrv_"+self.name+"_Ankle"); toeRes = ("JntDrv_"+self.name+"_Toe")
                legEndRes = ("JntDrv_"+self.name+"_LegEnd")
                jnts.append(thighRes); jnts.append(shinRes); jnts.append(ankleRes); jnts.append(toeRes); jnts.append(legEndRes)
            elif self.haveRibbon == "Disabled":
                thighRes = ("JntBnd_"+self.name+"_Thigh"); shinRes = ("JntBnd_"+self.name+"_Shin")
                ankleRes = ("JntBnd_"+self.name+"_Ankle"); toeRes = ("JntBnd_"+self.name+"_Toe")
                legEndRes = ("JntBnd_"+self.name+"_LegEnd")
                jnts.append(thighRes); jnts.append(shinRes); jnts.append(ankleRes); jnts.append(toeRes); jnts.append(legEndRes)
            if self.haveIK == "Enabled":
                thighFK = ("JntDrv_"+self.name+"_FK_Thigh"); shinFK = ("JntDrv_"+self.name+"_FK_Shin")
                ankleFK = ("JntDrv_"+self.name+"_FK_Ankle"); toeFK = ("JntDrv_"+self.name+"_FK_Toe")
                legEndFK = ("JntDrv_"+self.name+"_FK_LegEnd"); thighIK = ("JntDrv_"+self.name+"_IK_Thigh")
                shinIK = ("JntDrv_"+self.name+"_IK_Shin"); ankleIK = ("JntDrv_"+self.name+"_IK_Ankle")
                toeIK = ("JntDrv_"+self.name+"_IK_Toe"); legEndIK = ("JntDrv_"+self.name+"_IK_LegEnd")
                jnts.append(thighFK); jnts.append(shinFK); jnts.append(ankleFK); jnts.append(toeFK); jnts.append(legEndFK)
                jnts.append(thighIK); jnts.append(shinIK); jnts.append(ankleIK); jnts.append(toeIK); jnts.append(legEndIK)
            if self.haveAutoPv == True:
                thighPv = ("JntDrv_"+self.name+"_Pv_Thigh"); shinPv = ("JntDrv_"+self.name+"_Pv_Shin")
                anklePv = ("JntDrv_"+self.name+"_Pv_Ankle"); thighNoFlip = ("JntDrv_"+self.name+"_NoFlip_Thigh")
                shinNoFlip = ("JntDrv_"+self.name+"_NoFlip_Shin"); ankleNoFlip = ("JntDrv_"+self.name+"_NoFlip_Ankle")
                jnts.append(thighPv); jnts.append(shinPv); jnts.append(anklePv)
                jnts.append(thighNoFlip); jnts.append(shinNoFlip); jnts.append(ankleNoFlip)
        log.buildLog(msg="whiteLine", stop=False)

        # Create Joints

        self.createJoints(jnts)
        for jnt in jnts:
            print jnt
        chains = self.connectJntChains(jnts)
        self.orientJnts(chains)
        self.setRotOrderJnts(chains)


        # Create Controls

        # if self.side == "L": ctrlColor = "Red"; bendColor = "LightRed"; tweakColor = "DarkRed"
        # elif self.side == "R": ctrlColor = "Blue"; bendColor = "LightBlue"; tweakColor = "DarkBlue"
        ctrlColor = 'Primary'; bendColor = 'Secondary'; tweakColor = 'Tertiary'
        if self.haveMultLegs == 1:
            ctrlNames = [("Ctrl_"+self.side+"_FK_Thigh"), ("Ctrl_"+self.side+"_FK_Shin"),
                ("Ctrl_"+self.side+"_FK_Ankle"), ("Ctrl_"+self.side+"_FK_Toe")]
        elif self.haveMultLegs == 2:
            ctrlNames = [("Ctrl_"+self.name+"_FK_Thigh"), ("Ctrl_"+self.name+"_FK_Shin"),
                ("Ctrl_"+self.name+"_FK_Ankle"), ("Ctrl_"+self.name+"_FK_Toe")]
        ctrlSizes = [1 * self.gblScaleGuide[0], 0.85 * self.gblScaleGuide[0], 0.8 * self.gblScaleGuide[0], 0.6 * self.gblScaleGuide[0]]
        if self.haveIK == "Disabled":
            cmds.select(chains[0][0], r=True)
            grpResJnts = cmds.group(n=("Grp_Jnt_"+self.side+"_Leg_ResultConst"))
            cmds.move(self.posThigh[0], self.posThigh[1], self.posThigh[2], (grpResJnts+".rp"), (grpResJnts+".sp"), rpr=True)
        elif self.haveIK == "Enabled":
            cmds.select(chains[0][0], r=True)
            grpResJnts = cmds.group(n=("Grp_Jnt_"+self.side+"_Leg_ResultConst"))
            cmds.move(self.posThigh[0], self.posThigh[1], self.posThigh[2], (grpResJnts+".rp"), (grpResJnts+".sp"), rpr=True)
            cmds.select(chains[1][0], r=True)
            grpFKLeg = cmds.group(n=("Grp_"+chains[1][0][0:6]+"_"+self.side+"_FK_Leg"))
            cmds.move(self.posThigh[0], self.posThigh[1], self.posThigh[2], (grpFKLeg+".rotatePivot"), (grpFKLeg+".scalePivot"), rpr=True)

        fkControls, grpSettingsCtrls = self.createCtrlsFK(names=ctrlNames, sizes=ctrlSizes, color=[ctrlColor, tweakColor], jnts=chains[0])
        self.adjustCtrlsFK(side=self.side)
        self.manageAttrCtrlsFK()
        grpFKCtrlsConst, grpFKCtrls = self.setHierarchyCtrlsFK()
        self.setRotOrderFK(ctrls=ctrlNames)
        if self.haveIK == "Enabled":
            ctrlsIK, grpIKCtrls = self.createCtrlsIK(color=ctrlColor, jnts=chains)
            pvLoc, pvCtrl, grpPVCtrls, dispLine = self.createPoleVector(jnts=chains[0], color=bendColor)
            self.manageAttrCtrlsIK()
            self.setRotOrderIK(("Ctrl_"+self.side+"_IK_Leg"))


        # Create Setup

        if self.haveIK == "Enabled":
            FKJnts = self.associateFK(ctrls=ctrlNames, jnts=chains[1])
        elif self.haveIK == "Disabled":
            FKJnts = self.associateFK(ctrls=ctrlNames, jnts=chains[0])
        if self.haveStretchFK == True: self.setupStretchFK(ctrls=ctrlNames, jnts=FKJnts)
        if self.haveSquashFK == True: self.setupSquashFK(ctrls=ctrlNames, jnts=FKJnts)
        if self.haveIK == "Enabled":
            # Create Switchs
            if self.switchType == 1:
                ikfksChains = []
                ikfksChains.append(chains[1])
                ikfksChains.append(chains[2])
                ikfksChains.append(chains[0])
                self.createMultSwitch(ikfksChains, "IKFKSwitch")
                if self.haveAutoPv == True:
                    autoPvChains = []
                    autoPvChains.append(chains[3])
                    autoPvChains.append(chains[4])
                    autoPvChains.append(chains[2])
                    self.createMultSwitch(autoPvChains, "AutoManualSwitch")
            elif self.switchType == 2:
                self.createIKFKSwitch(chains)
                if self.haveAutoPv == True:
                    self.createAutoMSwitch(chains)
            # Create IK
            '''
            # Result
            # FK
            # IK
            # PV
            # No Flip
            '''
            ikHdls, grpIKS = self.associateIK(jnts=chains, ctrlLeg=ctrlsIK[0])
            if self.haveStretchIK == True: stretchLocs = self.setupStretchIK(ctrls=ctrlsIK, pvLoc=pvLoc, pvCtrl=pvCtrl, chains=chains[2:len(chains)])
            if self.haveReverseFoot == True:
                self.createReverseFoot(ikHandles=ikHdls)
            self.connectIKFKSwitchVis(settingsCtrl=fkControls[-1])
        # Create Ribbon Setup
        if self.haveRibbon == "Enabled":
            oldSfc = self.createRibbon()
            newSfc, ribJnts, thighRot, shinRot, grpRibCtrls, grpRibFol = self.rebuildRibbon(oldRib=oldSfc, colors=[ctrlColor, bendColor, tweakColor],
                settingsCtrl=fkControls[-1])
            blends = []
            if self.haveBendCtrlsRib == True: blends.append("Bend")
            if self.haveTwistAttrsRib == True: blends.append("Twist")
            if self.haveSineAttrsRib == True: blends.append("Sine")
            if self.haveSquashAttrsRib == True: blends.append("Squash")
            if self.haveExtraFreeSlotsRib == True:
                slots = ["Extra"]
                slots.append(self.numberOfFreeSlotsRib)
                blends.append(slots)
            blendSfc = self.createBsRibbons(mainSfc=newSfc, bs=blends, jnts=chains[0][0:3])
            if "Bend" in blends:
                grpBends, grpCtrls, wireCrvs = self.createBendRibbon(mainSfc=("Sfc_Rib_"+self.side+"_Leg"), sfc=("Sfc_Bs_Rib_"+self.side+"_Leg_Bend"), color=bendColor,
                    jntsRes=chains[0][0:3], thighRot=thighRot, shinRot=shinRot, settingsCtrl=fkControls[-1])
            if "Sine" in blends: nlSine = self.createSineRibbon(sfc=("Sfc_Bs_Rib_"+self.side+"_Leg_Sine"), settingsCtrl=fkControls[-1])
            if "Twist" in blends: nlTwist = self.createTwistRibbon(sfc=("Sfc_Bs_Rib_"+self.side+"_Leg_Twist"), thighRot=thighRot, shinRot=shinRot, settingsCtrl=fkControls[-1])
            if "Squash" in blends: nlSquash, grpFolSquash = self.createSquashRibbon(sfc=("Sfc_Bs_Rib_"+self.side+"_Leg_Squash"), settingsCtrl=fkControls[-1],
                ctrlJntsGrp=grpRibCtrls)
        # Create Space Switchs


        # Return Features

        self.jntsBnd.extend(chains[0])
        if self.haveIK == "Enabled":
            self.jntsDrv.extend(chains[1])
            self.jntsDrv.extend(chains[2])
            if self.haveAutoPv == True:
                self.jntsDrv.extend(chains[3])
                self.jntsDrv.extend(chains[4])
        if self.haveRibbon == "Enabled":
            self.jntsRib.extend(ribJnts)


        # Clean Up Component
        if self.haveIK == "Enabled":
            cmds.select(chains[2][0], r=True)
            if self.haveAutoPv == True: cmds.select(chains[3][0], chains[4][0], add=True)
            if self.haveStretchIK == True: cmds.select(stretchLocs[0:2], add=True)
            grpIKConst = cmds.group(n=("Grp_Jnt_"+self.side+"_Leg_IKConst"))
            cmds.move(self.posThigh[0], self.posThigh[1], self.posThigh[2], (grpIKConst+".rp"), (grpIKConst+".sp"), rpr=True)
        if self.haveIK == "Enabled":
            cmds.select(grpFKLeg, r=True);
            grpFKConst = cmds.group(n=("Grp_Jnt_"+self.side+"_Leg_FKConst"))
            cmds.move(self.posThigh[0], self.posThigh[1], self.posThigh[2], (grpFKConst+".rp"), (grpFKConst+".sp"), rpr=True)
            cmds.connectAttr((grpFKConst+".t"), (grpFKCtrlsConst+".t"))
            cmds.connectAttr((grpFKConst+".r"), (grpFKCtrlsConst+".r"))
            cmds.select(grpIKConst, grpResJnts, r=True)
            grpDONOTTOUCH = cmds.group(n=("Grp_DO_NOT_TOUCH"))
            cmds.select(grpFKConst, grpDONOTTOUCH, r=True)
            if self.haveRibbon == "Enabled": grpLegJnts = cmds.group(n=("Grp_JntDrv_"+self.side+"_Leg"))
            else: grpLegJnts = cmds.group(n=("Grp_JntBnd_"+self.side+"_Leg"))
            cmds.move(self.posThigh[0], self.posThigh[1], self.posThigh[2], (grpLegJnts+".rp"), (grpLegJnts+".sp"), rpr=True)
            cmds.setAttr("|"+grpLegJnts+"|"+grpDONOTTOUCH+".useOutlinerColor", True)
            cmds.setAttr("|"+grpLegJnts+"|"+grpDONOTTOUCH+".outlinerColorR", 0.9372)
            cmds.setAttr("|"+grpLegJnts+"|"+grpDONOTTOUCH+".outlinerColorG", 0.2823)
            cmds.setAttr("|"+grpLegJnts+"|"+grpDONOTTOUCH+".outlinerColorB", 0.2117)
            # Ctrls
            if self.haveBendCtrlsRib == True:
                cmds.select(grpBends, r=True)
                grpBends = cmds.group(n=("Grp_Ctrl_Rib_"+self.side+"_Leg"))
                cmds.select(grpCtrls, r=True)
                grpCtrls = cmds.group(n=("Grp_Ctrl_Bend_"+self.side+"_Leg"))
            cmds.select(grpFKCtrls, grpIKCtrls, grpPVCtrls, grpSettingsCtrls, r=True)
            if self.haveBendCtrlsRib == True: cmds.select(grpCtrls, add=True)
            grpLegCtrls = cmds.group(n=("Grp_Ctrls_"+self.side+"_Leg"))
            # Blendshapes
            if self.haveRibbon == "Enabled":
                if blendSfc != []:
                    cmds.select(blendSfc, r=True)
                    grpBsRib = cmds.group(n=("Grp_Bs_Rib_"+self.side+"_Leg"))
            # Xtra
            if self.haveRibbon == "Enabled":
                cmds.select(newSfc, r=True)
                if self.haveSineAttrsRib == True: cmds.select(nlSine, add=True)
                if self.haveTwistAttrsRib == True: cmds.select(nlTwist, add=True)
                if self.haveSquashAttrsRib == True: cmds.select(nlSquash, grpFolSquash, add=True)
                if self.haveBendCtrlsRib == True: cmds.select(wireCrvs, grpBends, add=True)
                grpXtraHide = cmds.group(n=("Grp_Xtra_ToHide_"+self.side+"_Leg"))
            if self.haveRibbon == "Enabled" or self.haveIK == "Enabled":
                grpXtraShow = cmds.group(n=("Grp_Xtra_ToShow_"+self.side+"_Leg"), empty=True)
                if self.haveRibbon == "Enabled": cmds.parent(grpRibFol, grpXtraShow, r=True)
                if self.haveIK == "Enabled": cmds.parent(dispLine, grpXtraShow, r=True)
            # Global group
            if self.setupFull == 1:
                cmds.parent(grpLegJnts, "Grp_Sktn")
                cmds.parent(grpLegCtrls, "Grp_Ctrl")
                cmds.parent(grpIKS, "Grp_ikHdle")
                if self.haveRibbon == "Enabled" or self.haveIK == "Enabled":
                    if self.haveRibbon == "Enabled":
                        if blendSfc != []: cmds.parent(grpBsRib, "Grp_PSD")
                        cmds.parent(grpXtraHide, "Grp_Xtra_ToHide")
                    cmds.parent(grpXtraShow, "Grp_Xtra_ToShow")
            else:
                grpLeg = cmds.group(n=("Grp_"+self.side+"_HumanLeg"), empty=True)
                cmds.parent(grpLegJnts, grpLegCtrls, grpIKS, grpLeg, r=True)
                if self.haveRibbon == "Enabled":
                    if blendSfc != []:
                        cmds.select(grpBsRib, r=True)
                        grpBs = cmds.group(n=("Grp_Bs_"+self.side+"_Leg"))
                        cmds.parent(grpBs, grpLeg, r=True)
                cmds.parent(grpXtraShow, grpXtraHide, grpLeg, r=True)
        else:
            cmds.select(grpResJnts, r=True)
            if self.haveRibbon == "Enabled": grpLegJnts = cmds.group(n=("Grp_JntDrv_"+self.side+"_Leg"))
            else: grpLegJnts = cmds.group(n=("Grp_JntBnd_"+self.side+"_Leg"))
            cmds.move(self.posThigh[0], self.posThigh[1], self.posThigh[2], (grpLegJnts+".rp"), (grpLegJnts+".sp"), rpr=True)
            cmds.connectAttr((grpResJnts+".t"), (grpFKCtrlsConst+".t"))
            cmds.connectAttr((grpResJnts+".r"), (grpFKCtrlsConst+".r"))
            # Ctrls
            if self.haveBendCtrlsRib == True:
                cmds.select(grpBends, r=True)
                grpBends = cmds.group(n=("Grp_Ctrl_Rib_"+self.side+"_Leg"))
                cmds.select(grpCtrls, r=True)
                grpCtrls = cmds.group(n=("Grp_Ctrl_Bend_"+self.side+"_Leg"))
            cmds.select(grpFKCtrls, r=True)
            if self.haveRibbon == "Enabled": cmds.select(grpSettingsCtrls, add=True)
            if self.haveBendCtrlsRib == True: cmds.select(grpCtrls, add=True)
            grpLegCtrls = cmds.group(n=("Grp_Ctrls_"+self.side+"_Leg"))
            # Blendshapes
            if self.haveRibbon == "Enabled":
                if blendSfc != []:
                    cmds.select(blendSfc, r=True)
                    grpBsRib = cmds.group(n=("Grp_Bs_Rib_"+self.side+"_Leg"))
            # Xtra
            if self.haveRibbon == "Enabled":
                cmds.select(newSfc, r=True)
                if self.haveSineAttrsRib == True: cmds.select(nlSine, add=True)
                if self.haveTwistAttrsRib == True: cmds.select(nlTwist, add=True)
                if self.haveSquashAttrsRib == True: cmds.select(nlSquash, grpFolSquash, add=True)
                if self.haveBendCtrlsRib == True: cmds.select(wireCrvs, grpBends, add=True)
                grpXtraHide = cmds.group(n=("Grp_Xtra_ToHide_"+self.side+"_Leg"))
            if self.haveRibbon == "Enabled":
                cmds.select(grpRibFol, add=True)
                grpXtraShow = cmds.group(n=("Grp_Xtra_ToShow_"+self.side+"_Leg"))
            # Global group
            if self.setupFull == 1:
                cmds.parent(grpLegJnts, "Grp_Sktn")
                cmds.parent(grpLegCtrls, "Grp_Ctrl")
                if self.haveRibbon == "Enabled":
                    if blendSfc != []: cmds.parent(grpBsRib, "Grp_PSD")
                    cmds.parent(grpXtraShow, "Grp_Xtra_ToShow")
                    cmds.parent(grpXtraHide, "Grp_Xtra_ToHide")
            else:
                grpLeg = cmds.group(n=("Grp_"+self.side+"_HumanLeg"), empty=True)
                cmds.parent(grpLegJnts, grpLegCtrls, grpLeg, r=True)
                if self.haveRibbon == "Enabled":
                    if blendSfc != []:
                        cmds.select(grpBsRib, r=True)
                        grpBs = cmds.group(n=("Grp_Bs_"+self.side+"_Leg"))
                        cmds.parent(grpBs, grpLeg, r=True)
                    cmds.parent(grpXtraShow, grpXtraHide, grpLeg, r=True)


        # cmds.select(chains[0][0], r=True)
        # if self.haveIK == "Enabled": grpFKJnts = cmds.group(n=("Grp_JntDrv_Spine_FKConst"))
        # else: grpFKJnts = cmds.group(n=("Grp_JntBnd_Spine_FKConst"))
        # cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], (grpFKJnts+".rotatePivot"), (grpFKJnts+".scalePivot"), rpr=True)
        # if self.haveIK == "Enabled":
        #     cmds.select(chains[1][0], jntsCrv, r=True)
        #     grpIKJnts = cmds.group(n="Grp_JntBnd_Spine_IKConst")
        #     cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], (grpIKJnts+".rotatePivot"), (grpIKJnts+".scalePivot"), rpr=True)
        #     cmds.select(jntsCrv, r=True)
        #     grpIKCrvJnts = cmds.group(n="Grp_JntDrv_Spine_CrvJnts_IKConst")
        #     cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], (grpIKCrvJnts+".rotatePivot"), (grpIKCrvJnts+".scalePivot"), rpr=True)
        #     cmds.select(grpIKJnts, grpIKCrvJnts, r=True)
        #     grpJntsDONOTTOUCH = cmds.group(n="DO_NOT_TOUCH")
        #     cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], (grpJntsDONOTTOUCH+".rotatePivot"), (grpJntsDONOTTOUCH+".scalePivot"), rpr=True)
        #     cmds.setAttr((grpJntsDONOTTOUCH+".useOutlinerColor"), 1)
        #     cmds.setAttr((grpJntsDONOTTOUCH+".outlinerColorR"), 0.9372)
        #     cmds.setAttr((grpJntsDONOTTOUCH+".outlinerColorG"), 0.2823)
        #     cmds.setAttr((grpJntsDONOTTOUCH+".outlinerColorB"), 0.2117)
        #     cmds.select(grpFKJnts, grpJntsDONOTTOUCH, r=True)
        #     grpSpineJnts = cmds.group(n="Grp_JntBnd_Spine")
        #     cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], (grpSpineJnts+".rotatePivot"), (grpSpineJnts+".scalePivot"), rpr=True)
        #     grpCtrlsIKConst = cmds.group(n=("Grp_Ctrl_Spine_IKConst"), em=True)
        #     for c in ctrlsIK:
        #         cmds.parent(("Grp_"+str(c)), grpCtrlsIKConst)
        #     cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], (grpCtrlsIKConst+".rotatePivot"), (grpCtrlsIKConst+".scalePivot"), rpr=True)
        #     cmds.parent(grpCtrlsIKConst, grpSpineCtrls)
        #     # Connect Root Ctrl
        #     cmds.select(rootCtrl, grpFKJnts, r=True)
        #     const = cmds.parentConstraint(weight=1, mo=True)
        #     cmds.select(rootCtrl, grpIKJnts, r=True)
        #     const = cmds.parentConstraint(weight=1, mo=True)
        #     cmds.select(rootCtrl, grpIKCrvJnts, r=True)
        #     const = cmds.parentConstraint(weight=1, mo=True)
        #     cmds.select(rootCtrl, grpCtrlsFKConst, r=True)
        #     const = cmds.parentConstraint(weight=1, mo=True)
        #     cmds.select(rootCtrl, grpCtrlsIKConst, r=True)
        #     const = cmds.parentConstraint(weight=1, mo=True)
        #     # Hide Attrs
        #     attrs = []
        #     attrs.append(grpFKJnts); attrs.append(grpIKJnts); attrs.append(grpIKCrvJnts); attrs.append(grpCtrlsFKConst); attrs.append(grpCtrlsIKConst)
        #     attrs.append(grpJntsDONOTTOUCH); attrs.append(grpSpineCtrls); attrs.append(grpSpineJnts)
        #     for a in attrs:
        #         ctrl.Control(n=a, t="Lock and Hide", s=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])
        #     # Create Component hierarchy
        #     if self.setupFull == 1:
        #         cmds.parent(grpSpineJnts, "Grp_Sktn")
        #         cmds.parent(("Grp_"+str(rootCtrl)), "Grp_Ctrl")
        #         cmds.parent(grpSpineCtrls, "Grp_Ctrl")
        #         cmds.parent(ikSpine, "Grp_ikHdle")
        #         cmds.parent(crvSpine, "Grp_Xtra_ToHide")
        #     elif self.setupFull == 2:
        #         cmds.select(grpSpineJnts, grpSpineCtrls, ("Grp_"+str(rootCtrl)), ikSpine, crvSpine, r=True)
        #         grpSpine = cmds.group(n="Grp_HumanSpine")
        # else:
        #     cmds.select(grpFKJnts, r=True)
        #     grpSpineJnts = cmds.group(n="Grp_JntBnd_Spine")
        #     cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], (grpSpineJnts+".rotatePivot"), (grpSpineJnts+".scalePivot"), rpr=True)
        #     # Connect Root Ctrl
        #     cmds.select(rootCtrl, grpFKJnts, r=True)
        #     const = cmds.parentConstraint(weight=1, mo=True)
        #     cmds.select(rootCtrl, grpCtrlsFKConst, r=True)
        #     const = cmds.parentConstraint(weight=1, mo=True)
        #     # Hide Attrs
        #     attrs = []
        #     attrs.append(grpFKJnts); attrs.append(grpCtrlsFKConst); attrs.append(grpSpineCtrls); attrs.append(grpSpineJnts)
        #     for a in attrs:
        #         ctrl.Control(n=a, t="Lock and Hide", s=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])
        #     # Create Component hierarchy
        #     if self.setupFull == 1:
        #         cmds.parent(grpSpineJnts, "Grp_Sktn")
        #         cmds.parent(("Grp_"+str(rootCtrl)), "Grp_Ctrl")
        #         cmds.parent(grpSpineCtrls, "Grp_Ctrl")
        #     elif self.setupFull == 2:
        #         cmds.select(grpSpineJnts, grpSpineCtrls, ("Grp_"+str(rootCtrl)), r=True)
        #         grpSpine = cmds.group(n="Grp_HumanSpine")




    def createJoints(self, jnts=[]):
        log.buildLogHumanLeg(msg="createJnts", btn="Start", stop=False)
        x = 0
        y = 0
        pos = [(self.posThigh[0], self.posThigh[1], self.posThigh[2]),
            (self.posShin[0], self.posShin[1], self.posShin[2]),
            (self.posAnkle[0], self.posAnkle[1], self.posAnkle[2]),
            (self.posToe[0], self.posToe[1], self.posToe[2]),
            (self.posLegEnd[0], self.posLegEnd[1], self.posLegEnd[2])]
        for j in jnts:
            if x >= 3:
                if y >= 3: x = 0
                elif x >= 5: x = 0; y += 1
            cmds.select(cl=True)
            jnt = cmds.joint(p=(pos[x][0], pos[x][1], pos[x][2]))
            cmds.rename(jnt, j)
            x += 1
            log.buildLogHumanLeg(msg="createJnts", btn=[j, x], stop=False)
        log.buildLogHumanLeg(msg="createJnts", btn="All", stop=False)
        log.buildLog(msg="whiteLine", stop=False)

    def connectJntChains(self, jnts=[]):
        chains = []
        count = len(jnts)
        if count == 21:
            cmds.parent(jnts[4], jnts[3]); cmds.parent(jnts[3], jnts[2]); cmds.parent(jnts[2], jnts[1]); cmds.parent(jnts[1], jnts[0])
            cmds.parent(jnts[9], jnts[8]); cmds.parent(jnts[8], jnts[7]); cmds.parent(jnts[7], jnts[6]); cmds.parent(jnts[6], jnts[5])
            cmds.parent(jnts[14], jnts[13]); cmds.parent(jnts[13], jnts[12]); cmds.parent(jnts[12], jnts[11]); cmds.parent(jnts[11], jnts[10])
            cmds.parent(jnts[17], jnts[16]); cmds.parent(jnts[16], jnts[15])
            cmds.parent(jnts[20], jnts[19]); cmds.parent(jnts[19], jnts[18])
            log.buildLogHumanLeg(msg="connectJnts", btn=str(count), stop=False)
            chains.append(jnts[0:5])   # Result
            chains.append(jnts[5:10])  # FK
            chains.append(jnts[10:15]) # IK
            chains.append(jnts[15:18]) # PV
            chains.append(jnts[18:21]) # No Flip
            for c in chains:
                log.buildLogHumanLeg(msg="jntChainsCreated", btn=c, stop=False)
            return chains
        elif count == 15:
            cmds.parent(jnts[4], jnts[3]); cmds.parent(jnts[3], jnts[2]); cmds.parent(jnts[2], jnts[1]); cmds.parent(jnts[1], jnts[0])
            cmds.parent(jnts[9], jnts[8]); cmds.parent(jnts[8], jnts[7]); cmds.parent(jnts[7], jnts[6]); cmds.parent(jnts[6], jnts[5])
            cmds.parent(jnts[14], jnts[13]); cmds.parent(jnts[13], jnts[12]); cmds.parent(jnts[12], jnts[11]); cmds.parent(jnts[11], jnts[10])
            log.buildLogHumanLeg(msg="connectJnts", btn=str(count), stop=False)
            chains.append(jnts[0:5])   # Result
            chains.append(jnts[5:10])  # FK
            chains.append(jnts[10:15]) # IK
            for c in chains:
                log.buildLogHumanLeg(msg="jntChainsCreated", btn=c, stop=False)
            return chains
        elif count == 5:
            cmds.parent(jnts[4], jnts[3]); cmds.parent(jnts[3], jnts[2]); cmds.parent(jnts[2], jnts[1]); cmds.parent(jnts[1], jnts[0])
            log.buildLogHumanLeg(msg="connectJnts", btn=str(count), stop=False)
            chains.append(jnts[0:5])   # Result
            for c in chains:
                log.buildLogHumanLeg(msg="jntChainsCreated", btn=c, stop=False)
            return chains

    def orientJnts(self, chains=[]):
        log.buildLog(msg="whiteLine", stop=False)
        count = len(chains)
        x = 0
        log.buildLogHumanLeg(msg="orientJnts", btn=["Start", str(count)], stop=False)
        while x < count:
            cmds.select(chains[x][0])
            cmds.joint(edit=True, oj="xyz", sao="xup", ch=True, zso=True)
            cmds.select(chains[x][-1])
            cmds.joint(edit=True, oj="none", zso=True)
            x += 1
        log.buildLogHumanLeg(msg="orientJnts", btn=["Run", str(count)], stop=False)
        log.buildLog(msg="whiteLine", stop=False)

    def setRotOrderJnts(self, chains=[]):
        # print ("\n chains = %s") %(chains)  | All chains
        for c in chains:
            # print ("\n chain(c) = %s") %(c)  | Chain selected
            for jnt in c:
                cmds.setAttr((jnt+".rotateOrder"), 3)
                # print ("jnt = %s") %(jnt)  | All joints rot order setted (XZY)

    def createCtrlsFK(self, names=[], sizes=[], color="", jnts=[]):
        x = 0
        ctrls = []
        for name in names:
            ctrls.append(ctrl.Control(n=name, t="Circle", s=sizes[x], c=color[0]))
            grp = cmds.group(n=("Grp_"+name))
            cmds.select(jnts[x], r=True)
            cmds.select(grp, add=True)
            const = cmds.parentConstraint(weight=1)
            cmds.select(const, r=True)
            cmds.Delete()
            x += 1
        if self.haveIK == "Enabled" or self.haveBendCtrlsRib == True or self.haveTweakCtrlsRib == True or self.haveSineAttrsRib == True or self.haveTwistAttrsRib == True:
            loc = cmds.spaceLocator(p=(0, 0, 0))
            cmds.parent(loc, jnts[2])
            attr = ['tx', 'tz', 'ty']
            for a in attr:
                cmds.setAttr((loc[0]+"."+a), 0)
            c = ctrl.Control(n=("Ctrl_"+self.side+"_Leg_Settings"), t="Box", s=(0.1 * self.gblScaleGuide[0]), c=color[1])
            ctrls.append(str(c))
            grp = cmds.group(n=("Grp_Ctrl_"+self.side+"_Leg_Settings"))
            cmds.move(0, 0, 0, (grp+".rotatePivot"), (grp+".scalePivot"))
            cmds.select(loc[0], grp, r=True)
            const = cmds.parentConstraint(weight=1)
            cmds.select(const, r=True)
            cmds.Delete()
            cmds.setAttr((grp+".rz"), 90)
            pos = 12 * self.gblScaleGuide[0]
            cmds.setAttr((grp+".tz"), pos * (-1))
            cmds.select(loc[0], grp, r=True)
            cmds.parentConstraint(weight=1, mo=True)
            cmds.setAttr((loc[0]+".v"), False)
            cmds.rename(loc, ("Loc_Ctrl_"+self.side+"_Leg_Settings"))
        return ctrls, grp

    def adjustCtrlsFK(self, side=""):
        if side == "L":
            # Thigh
            cmds.select("Ctrl_L_FK_Thigh.cv[0:7]", r=True)
            cmds.rotate(0, 0, -50, r=True, os=True)
            cmds.move(0.4 * self.gblScaleGuide[0], -0.4 * self.gblScaleGuide[0], 0 * self.gblScaleGuide[0], r=True, os=True)
            # Shin
            cmds.select("Ctrl_L_FK_Shin.cv[0:7]", r=True)
            cmds.rotate(0, 0, 90, r=True, os=True)
            cmds.move(0 * self.gblScaleGuide[0], 0.2 * self.gblScaleGuide[0], -0.2 * self.gblScaleGuide[0], r=True, os=True)
            # Ankle
            cmds.select("Ctrl_L_FK_Ankle.cv[0:7]", r=True)
            cmds.rotate(30, 0, 90, r=True, os=True)
            cmds.move(0 * self.gblScaleGuide[0], 0.6 * self.gblScaleGuide[0], 0.2 * self.gblScaleGuide[0], r=True, os=True)
            cmds.select("Ctrl_L_FK_Ankle.cv[0:2]", r=True)
            cmds.move(-2 * self.gblScaleGuide[0], 0 * self.gblScaleGuide[0], 2 * self.gblScaleGuide[0], r=True, os=True)
            cmds.select("Ctrl_L_FK_Ankle.cv[1]", r=True)
            cmds.move(0 * self.gblScaleGuide[0], 0 * self.gblScaleGuide[0], 1.2 * self.gblScaleGuide[0], r=True, os=True)
            # Toe
            cmds.select("Ctrl_L_FK_Toe.cv[0:7]", r=True)
            cmds.rotate(0, 0, 90, r=True, os=True)
            cmds.move(-0.1 * self.gblScaleGuide[0], 0.6 * self.gblScaleGuide[0], 0.6 * self.gblScaleGuide[0], r=True, os=True)
            cmds.select("Ctrl_L_FK_Toe.cv[0:2]", r=True)
            cmds.move(0 * self.gblScaleGuide[0], 0 * self.gblScaleGuide[0], 1.9 * self.gblScaleGuide[0], r=True, os=True)
            cmds.select("Ctrl_L_FK_Toe.cv[1]", r=True)
            cmds.move(0 * self.gblScaleGuide[0], 0 * self.gblScaleGuide[0], 1.9 * self.gblScaleGuide[0], r=True, os=True)
        elif side == "R":
            # Thigh
            cmds.select("Ctrl_R_FK_Thigh.cv[0:7]", r=True)
            cmds.rotate(0, 0, 50, r=True, os=True)
            cmds.move(0.4 * self.gblScaleGuide[0], -0.4 * self.gblScaleGuide[0], 0 * self.gblScaleGuide[0], r=True, os=True)
            # Shin
            cmds.select("Ctrl_R_FK_Shin.cv[0:7]", r=True)
            cmds.rotate(0, 0, -90, r=True, os=True)
            cmds.move(0 * self.gblScaleGuide[0], 0.2 * self.gblScaleGuide[0], -0.2 * self.gblScaleGuide[0], r=True, os=True)
            # Ankle
            cmds.select("Ctrl_R_FK_Ankle.cv[0:7]", r=True)
            cmds.rotate(30, 0, 90, r=True, os=True)
            cmds.move(0 * self.gblScaleGuide[0], 0.6 * self.gblScaleGuide[0], 0.2 * self.gblScaleGuide[0], r=True, os=True)
            cmds.select("Ctrl_R_FK_Ankle.cv[0:2]", r=True)
            cmds.move(-2 * self.gblScaleGuide[0], 0 * self.gblScaleGuide[0], 2 * self.gblScaleGuide[0], r=True, os=True)
            cmds.select("Ctrl_R_FK_Ankle.cv[1]", r=True)
            cmds.move(0 * self.gblScaleGuide[0], 0 * self.gblScaleGuide[0], 1.2 * self.gblScaleGuide[0], r=True, os=True)
            # Toe
            cmds.select("Ctrl_R_FK_Toe.cv[0:7]", r=True)
            cmds.rotate(0, 0, -90, r=True, os=True)
            cmds.move(-0.1 * self.gblScaleGuide[0], 0.6 * self.gblScaleGuide[0], 0.6 * self.gblScaleGuide[0], r=True, os=True)
            cmds.select("Ctrl_R_FK_Toe.cv[0:2]", r=True)
            cmds.move(0 * self.gblScaleGuide[0], 0 * self.gblScaleGuide[0], 1.9 * self.gblScaleGuide[0], r=True, os=True)
            cmds.select("Ctrl_R_FK_Toe.cv[1]", r=True)
            cmds.move(0 * self.gblScaleGuide[0], 0 * self.gblScaleGuide[0], 1.9 * self.gblScaleGuide[0], r=True, os=True)

    def manageAttrCtrlsFK(self):
        if self.haveMultLegs == 1:
            ctrl.Control(n=("Ctrl_"+self.side+"_FK_Thigh"), t="Lock and Hide", s=["tx", "ty", "tz", "sx", "sy", "sz"])
            ctrl.Control(n=("Ctrl_"+self.side+"_FK_Shin"), t="Lock and Hide", s=["tx", "ty", "tz", "sx", "sy", "sz"])
            ctrl.Control(n=("Ctrl_"+self.side+"_FK_Ankle"), t="Lock and Hide", s=["tx", "ty", "tz", "sx", "sy", "sz"])
            ctrl.Control(n=("Ctrl_"+self.side+"_FK_Toe"), t="Lock and Hide", s=["tx", "ty", "tz", "sx", "sy", "sz"])
            if self.haveSpaceSwitch == "Enabled" or self.haveStretchFK == True or self.haveSquashFK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_FK_Thigh|Ctrl_"+self.side+"_FK_Thigh"), ln="LEG", nn="_____________________ LEG", at="enum", en="__________:")
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_FK_Thigh|Ctrl_"+self.side+"_FK_Thigh.LEG"), edit=True, channelBox=True)
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_FK_Shin|Ctrl_"+self.side+"_FK_Shin"), ln="LEG", nn="_____________________ LEG", at="enum", en="__________:")
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_FK_Shin|Ctrl_"+self.side+"_FK_Shin.LEG"), edit=True, channelBox=True)
            if self.haveStretchFK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_FK_Thigh|Ctrl_"+self.side+"_FK_Thigh"), ln="ThighStretch", at="double", min=0, dv=1)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_FK_Thigh|Ctrl_"+self.side+"_FK_Thigh.ThighStretch"), edit=True, k=True)
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_FK_Shin|Ctrl_"+self.side+"_FK_Shin"), ln="ShinStretch", at="double", min=0, dv=1)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_FK_Shin|Ctrl_"+self.side+"_FK_Shin.ShinStretch"), edit=True, k=True)
            if self.haveSquashFK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_FK_Thigh|Ctrl_"+self.side+"_FK_Thigh"), ln="ThighSquash", at="double", min=0, dv=1)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_FK_Thigh|Ctrl_"+self.side+"_FK_Thigh.ThighSquash"), edit=True, k=True)
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_FK_Shin|Ctrl_"+self.side+"_FK_Shin"), ln="ShinSquash", at="double", min=0, dv=1)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_FK_Shin|Ctrl_"+self.side+"_FK_Shin.ShinSquash"), edit=True, k=True)
            if self.haveSpaceSwitch == "Enabled":
                rawSpaces = cmds.textScrollList("lstLegsSpaceListHLegs", q=True, ai=True)
                spaces = []
                enums = []
                y = 0
                for rs in rawSpaces:
                    space = []
                    for x in range(0, len(rs)):
                        if rs[x] == "|": y += 1
                        elif y == 1: space.append(rs[x])
                    if not space == []: spc = ''.join(space)
                    else: spc = rs
                    spaces.append(spc)
                    spc = ''; y = 0
                for s in spaces: enums.append(s); enums.append(":")
                enum = ''.join(enums)
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_FK_Thigh|Ctrl_"+self.side+"_FK_Thigh"), ln="Follow", at="enum", en=enum)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_FK_Thigh|Ctrl_"+self.side+"_FK_Thigh.Follow"), edit=True, k=True)
            # Settings ctrl
            if self.haveIK == "Enabled" or self.haveBendCtrlsRib == True or self.haveTweakCtrlsRib == True or self.haveSineAttrsRib == True or self.haveTwistAttrsRib == True:
                ctrl.Control(n=("Ctrl_"+self.side+"_Leg_Settings"), t="Lock and Hide", s=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])
                switchAttrs = 0
                if self.haveIK == "Enabled": switchAttrs += 1
                if self.haveAutoPv == True: switchAttrs += 1
                if self.haveBendCtrlsRib == True: switchAttrs += 1
                if self.haveTweakCtrlsRib == True: switchAttrs += 1
                if self.haveIK == "Enabled" or self.haveBendCtrlsRib == True or self.haveTweakCtrlsRib == True:
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SETTINGS", nn="________________ SETTINGS", at="enum", en="__________:")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SwitchSettings", at="compound", nc=switchAttrs)
                if self.haveIK == "Enabled":
                    if self.switchType == 1:
                        cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                            ln="IKFKSwitch", nn="IK/FK Switch", at="enum", en="FK:IK:", p="SwitchSettings")
                    elif self.switchType == 2:
                        cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                            ln="IKFKSwitch", nn="IK/FK Switch", at="double", min=0, max=1, dv=0, p="SwitchSettings")
                if self.haveAutoPv == True:
                    if self.switchType == 1:
                        cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                            ln="AutoManualSwitch", nn="Auto/Manual Switch", at="enum", en="Manual:Auto:", p="SwitchSettings")
                    elif self.switchType == 2:
                        cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                            ln="AutoManualSwitch", nn="Auto/Manual Switch", at="double", min=0, max=1, dv=0, p="SwitchSettings")
                if self.haveBendCtrlsRib == True:
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SecondaryCtrls", at="bool", p="SwitchSettings")
                if self.haveTweakCtrlsRib == True:
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="TertiaryCtrls", at="bool", p="SwitchSettings")
                if self.haveSineAttrsRib == True:
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SINE", nn="____________________ SINE", at="enum", en="__________:")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SineAttrs", at="compound", nc=6)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SineAmplitude", at="double", min=-5, max=5, dv=0, p="SineAttrs")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SineWavelength", at="double", min=0.1, max=10, dv=2, p="SineAttrs")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SineOffset", at="double", min=-10, max=10, dv=0, p="SineAttrs")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SineTwist", at="double", min=-360, max=360, dv=0, p="SineAttrs")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SinePos", at="double", min=-360, max=360, dv=0, p="SineAttrs")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SineScale", at="double", min=-360, max=360, dv=0, p="SineAttrs")
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.SINE"),
                        edit=True, channelBox=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.SineAmplitude"),
                        edit=True, k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.SineWavelength"),
                        edit=True, k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.SineOffset"),
                        edit=True, k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.SineTwist"),
                        edit=True, k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.SinePos"),
                        edit=True, k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.SineScale"),
                        edit=True, k=True)
                if self.haveTwistAttrsRib == True:
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="TWIST", nn="___________________ TWIST", at="enum", en="__________:")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="TwistAttrs", at="compound", nc=5)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="ThighTwistMult", at="double", min=-859, max=859, dv=0, p="TwistAttrs")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="KneeTwistMult", at="double", min=-859, max=859, dv=0, p="TwistAttrs")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="ShinTwistMult", at="double", min=-859, max=859, dv=0, p="TwistAttrs")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="Roll", at="double", min=-859, max=859, dv=0, p="TwistAttrs")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="RollOffset", at="double", min=-859, max=859, dv=0, p="TwistAttrs")
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.TWIST"),
                        edit=True, channelBox=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.ThighTwistMult"),
                        edit=True, k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.KneeTwistMult"),
                        edit=True, k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.ShinTwistMult"),
                        edit=True, k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.Roll"),
                        edit=True, k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.RollOffset"),
                        edit=True, k=True)
                if self.haveSquashAttrsRib == True:
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SQUASH", nn="__________________ SQUASH", at="enum", en="__________:")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SquashAttrs", at="compound", nc=6)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="Squash", at="double", dv=0, p="SquashAttrs")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SquashMult", at="double", min=-1, max=1, dv=0.3, p="SquashAttrs")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SquashScale", at="double", dv=0, p="SquashAttrs")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SquashPos", at="double", dv=0, p="SquashAttrs")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SquashStartDropoff", at="double", min=0, max=1, dv=0, p="SquashAttrs")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings"),
                        ln="SquashEndDropoff", at="double", min=0, max=1, dv=0, p="SquashAttrs")
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.SQUASH"),
                        edit=True, channelBox=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.Squash"),
                        edit=True, k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.SquashMult"),
                        edit=True, k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.SquashScale"),
                        edit=True, k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.SquashPos"),
                        edit=True, k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.SquashStartDropoff"),
                        edit=True, k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.SquashEndDropoff"),
                        edit=True, k=True)
                if self.haveIK == "Enabled" or self.haveBendCtrlsRib == True or self.haveTweakCtrlsRib == True:
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.SETTINGS"),
                        edit=True, channelBox=True)
                if self.haveIK == "Enabled":
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.IKFKSwitch"),
                        edit=True, k=True)
                if self.haveAutoPv == True:
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.AutoManualSwitch"),
                        edit=True, k=True)
                if self.haveBendCtrlsRib == True:
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.SecondaryCtrls"),
                        edit=True, k=True)
                if self.haveTweakCtrlsRib == True:
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Settings|Ctrl_"+self.side+"_Leg_Settings.TertiaryCtrls"),
                        edit=True, k=True)
        elif self.haveMultLegs == 2: pass

    def setHierarchyCtrlsFK(self):
        cmds.parent(("Grp_Ctrl_"+self.side+"_FK_Toe"), ("Ctrl_"+self.side+"_FK_Ankle"))
        cmds.parent(("Grp_Ctrl_"+self.side+"_FK_Ankle"), ("Ctrl_"+self.side+"_FK_Shin"))
        cmds.parent(("Grp_Ctrl_"+self.side+"_FK_Shin"), ("Ctrl_"+self.side+"_FK_Thigh"))
        cmds.select(("Grp_Ctrl_"+self.side+"_FK_Thigh"))
        grpFKCtrlsConst = cmds.group(n=("Grp_Ctrl_"+self.side+"_Leg_FKConst"))
        cmds.move(self.posThigh[0], self.posThigh[1], self.posThigh[2], (grpFKCtrlsConst+".rotatePivot"), (grpFKCtrlsConst+".scalePivot"), rpr=True)
        cmds.select(grpFKCtrlsConst)
        grpFKCtrls = cmds.group(n=("Grp_Ctrl_"+self.side+"_FK_Leg"))
        cmds.move(self.posThigh[0], self.posThigh[1], self.posThigh[2], (grpFKCtrls+".rotatePivot"), (grpFKCtrls+".scalePivot"), rpr=True)
        return grpFKCtrlsConst, grpFKCtrls

    def setRotOrderFK(self, ctrls=[]):
        for ctrl in ctrls:
            cmds.setAttr((ctrl+".rotateOrder"), 3)
            # print ("ctrl = %s") %(ctrl)  | All ctrls rot order setted (XZY)

    def createCtrlsIK(self, color="", jnts=[]):
        ctrlNames = []
        c = ctrl.Control(n=("Ctrl_"+self.side+"_IK_Leg"), t="Foot", s=(0.9 * self.gblScaleGuide[0]), c=color)
        ctrlNames.append(str(c))
        if self.side == "R":
            cmds.scale(-1, 1, 1, c, r=True)
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        grpOff = cmds.group(n=("Grp_Ctrl_"+self.side+"_IK_Leg_Off"))
        cmds.select(grpOff, r=True)
        grpConst = cmds.group(n=("Grp_Ctrl_"+self.side+"_IK_Leg_Const"))
        cmds.select(grpConst, r=True)
        grp = cmds.group(n=("Grp_Ctrl_"+self.side+"_IK_Leg"))
        cmds.select(jnts[0][3], grp, r=True)
        const = cmds.pointConstraint(weight=1)
        cmds.select(const, r=True)
        cmds.Delete()
        cmds.setAttr(("Grp_Ctrl_"+self.side+"_IK_Leg.ty"), 0)
        node = cmds.shadingNode("distanceBetween", asUtility=True)
        cmds.connectAttr((jnts[0][2]+".tx"), (node+".point1X"), f=True)
        cmds.connectAttr((jnts[0][3]+".tx"), (node+".point2X"), f=True)
        dist = cmds.getAttr((node+".distance"))
        cmds.select(node, r=True)
        cmds.Delete()
        cmds.select(("Grp_Ctrl_"+self.side+"_IK_Leg"), r=True)
        midDist = (dist * 0.45) / 2
        cmds.getAttr(("Grp_Ctrl_"+self.side+"_IK_Leg.tz"))
        pos = (cmds.getAttr(("Grp_Ctrl_"+self.side+"_IK_Leg.tz"))) - midDist
        cmds.move(0 * self.gblScaleGuide[0], 0 * self.gblScaleGuide[0], -pos * self.gblScaleGuide[0], ("Ctrl_"+self.side+"_IK_Leg.cv[0:7]"), r=True, os=True, wd=True)
        cmds.move(self.posAnkle[0], self.posAnkle[1], self.posAnkle[2], ("Ctrl_"+self.side+"_IK_Leg.rotatePivot"), ("Ctrl_"+self.side+"_IK_Leg.scalePivot"))
        cmds.move(self.posAnkle[0], self.posAnkle[1], self.posAnkle[2], ("Grp_Ctrl_"+self.side+"_IK_Leg_Off.rotatePivot"), ("Grp_Ctrl_"+self.side+"_IK_Leg_Off.scalePivot"))
        cmds.move(self.posAnkle[0], self.posAnkle[1], self.posAnkle[2], ("Grp_Ctrl_"+self.side+"_IK_Leg_Const.rotatePivot"), ("Grp_Ctrl_"+self.side+"_IK_Leg_Const.scalePivot"))
        cmds.move(self.posAnkle[0], self.posAnkle[1], self.posAnkle[2], ("Grp_Ctrl_"+self.side+"_IK_Leg.rotatePivot"), ("Grp_Ctrl_"+self.side+"_IK_Leg.scalePivot"))
        return ctrlNames, grp

    def createPoleVector(self, jnts=[], color=""):
        start = cmds.xform(jnts[0], q=True, ws=True, t=True)  # Thigh
        mid = cmds.xform(jnts[1], q=True, ws=True, t=True)    # Shin
        end = cmds.xform(jnts[2], q=True, ws=True, t=True)    # Ankle
        startV = om.MVector(start[0], start[1], start[2])
        midV = om.MVector(mid[0], mid[1], mid[2])
        endV = om.MVector(end[0], end[1], end[2])
        startEnd = endV - startV
        startMid = midV - startV
        dotP = startMid * startEnd
        proj = float(dotP) / float(startEnd.length())
        startEndN = startEnd.normal()
        projV = startEndN * proj
        arrowV = startMid - projV
        arrowV *= 4                 # Multiplier distance
        finalV = arrowV + midV
        cross1 = startEnd ^ startMid
        cross1.normalize()
        cross2 = cross1 ^ arrowV
        cross2.normalize()
        arrowV.normalize()
        matrixV = [arrowV.x, arrowV.y, arrowV.z, 0,
                   cross1.x, cross1.y, cross1.z, 0,
                   cross2.x, cross2.y, cross2.z, 0,
                   0, 0, 0, 1]
        matrixM = om.MMatrix()
        om.MScriptUtil.createMatrixFromList(matrixV, matrixM)
        matrixFn = om.MTransformationMatrix(matrixM)
        rot = matrixFn.eulerRotation()
        loc = cmds.spaceLocator(n=("Loc_Ctrl_"+self.side+"_Leg_Pv"))[0]
        cmds.xform(loc, ws=True, t=(finalV.x, finalV.y, finalV.z))
        cmds.xform(loc, ws=True, ro=((rot.x / math.pi * 180.0),
                                     (rot.y / math.pi * 180.0),
                                     (rot.z / math.pi * 180.0)))
        if self.haveMultLegs == 1:
            dispLine = []
            c = ctrl.Control(n=("Ctrl_"+self.side+"_Leg_Pv"), t="Diamond", s=(0.3 * self.gblScaleGuide[0]), c=color)
            cmds.select(c, r=True)
            cmds.group(n=("Grp_Ctrl_"+self.side+"_Leg_Pv_Off"))
            cmds.move(finalV.x, finalV.y, finalV.z, r=True)
            cmds.group(n=("Grp_Ctrl_"+self.side+"_Leg_Pv_Const"))
            cmds.CenterPivot()
            grpPV = cmds.group(n=("Grp_Ctrl_"+self.side+"_Leg_Pv"))
            cmds.CenterPivot()
            cmds.parent(loc, c)
            crv = cmds.curve(d=1, p=[(0, 0, 0), (0, 0, -32)], k=[0, 1])
            grpOff = cmds.group(n=("Grp_Crv_"+self.side+"_Leg_Pv_DispLine_Off"))
            grp = cmds.group(n=("Grp_Crv_"+self.side+"_Leg_Pv_DispLine"))
            cmds.select((crv+".cv[0]"), r=True)
            clJnt = cmds.cluster(n=("Cls_"+self.side+"_Leg_Pv_DispLine_Jnt"))
            cmds.select((crv+".cv[1]"), r=True)
            clCtrl = cmds.cluster(n=("Cls_"+self.side+"_Leg_Pv_DispLine_Ctrl"))
            cmds.select(loc, clCtrl, r=True)
            cmds.parentConstraint(weight=1)
            cmds.select(jnts[1], clJnt, r=True)
            cmds.parentConstraint(weight=1)
            cmds.setAttr(crv+".overrideEnabled", True)
            cmds.setAttr(crv+".overrideDisplayType", 2)
            cmds.setAttr((clJnt[0]+"Handle.v"), False)
            cmds.setAttr((clCtrl[0]+"Handle.v"), False)
            cmds.rename(crv, ("Crv_"+self.side+"_Leg_Pv_DispLine"))
            dispLine.append(grp); dispLine.append(clJnt[0]+"Handle"); dispLine.append(clCtrl[0]+"Handle")
            print("\n\n\n\n\nDISPLAY LINE: %s") %(dispLine)
            return loc, c, grpPV, dispLine
        elif self.haveMultLegs == 2:
            c = ctrl.Control(n=("Ctrl_"+self.side+"_Leg_Pv"), t="Diamond", s=(0.3 * self.gblScaleGuide[0]), c=color)
            cmds.rename(loc, ("Loc_Ctrl_"+self.name+"_Pv"))

    def manageAttrCtrlsIK(self):
        if self.haveMultLegs == 1:
            # Freeze controls
            ctrl.Control(n=("Ctrl_"+self.side+"_IK_Leg"), t="Lock and Hide", s=["sx", "sy", "sz"])
            ctrl.Control(n=("Ctrl_"+self.side+"_Leg_Pv"), t="Lock and Hide", s=["rx", "ry", "rz", "sx", "sy", "sz"])
            # Verify compound numbers
            legAttrs = 0
            pvAttrs = 1
            if self.haveAutoPv == True: legAttrs += 1;
            if self.haveStretchIK == True: legAttrs += 1
            if self.haveStretchMultIK == True: legAttrs += 2
            if self.haveSquashIK == True: legAttrs += 1
            if self.haveSquashMultIK == True: legAttrs += 2
            if self.haveClampStretchIK == True: legAttrs += 2
            if self.haveKneeLockIK == True: pvAttrs += 1
            if self.haveSpaceSwitch == "Enabled": legAttrs += 1; pvAttrs += 1
            # Add Attrs
            cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Pv|Grp_Ctrl_"+self.side+"_Leg_Pv_Const|Grp_Ctrl_"+self.side+"_Leg_Pv_Off|Ctrl_"+self.side+"_Leg_Pv"),
                ln="LEG", nn="_____________________ LEG", at="enum", en="__________:")
            cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Pv|Grp_Ctrl_"+self.side+"_Leg_Pv_Const|Grp_Ctrl_"+self.side+"_Leg_Pv_Off|Ctrl_"+self.side+"_Leg_Pv.LEG"),
                edit=True, channelBox=True)
            cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Pv|Grp_Ctrl_"+self.side+"_Leg_Pv_Const|Grp_Ctrl_"+self.side+"_Leg_Pv_Off|Ctrl_"+self.side+"_Leg_Pv"),
                ln="PvSettings", at="compound", nc=pvAttrs)
            cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Pv|Grp_Ctrl_"+self.side+"_Leg_Pv_Const|Grp_Ctrl_"+self.side+"_Leg_Pv_Off|Ctrl_"+self.side+"_Leg_Pv"),
                ln="DisplayLine", at="bool", p="PvSettings")
            if self.haveAutoPv == True or self.haveStretchIK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="LEG", nn="_____________________ LEG", at="enum", en="__________:")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="LegSettings", at="compound", nc=legAttrs)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.LEG"),
                    edit=True, channelBox=True)
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="KneeTwist", at="double", dv=0, p="LegSettings")
            if self.haveStretchIK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="Stretch", at="bool", p="LegSettings")
            if self.haveStretchMultIK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="ThighStretchMult", at="double", min=0.01, dv=1, p="LegSettings")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="ShinStretchMult", at="double", min=0.01, dv=1, p="LegSettings")
            if self.haveSquashIK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="Squash", at="bool", p="LegSettings")
            if self.haveSquashMultIK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="ThighSquashMult", at="double", min=0.01, dv=1, p="LegSettings")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="ShinSquashMult", at="double", min=0.01, dv=1, p="LegSettings")
            if self.haveClampStretchIK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="ClampStretch", at="bool", p="LegSettings")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="ClampValue", at="double", min=1, dv=1.5, p="LegSettings")
            if self.haveKneeLockIK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Pv|Grp_Ctrl_"+self.side+"_Leg_Pv_Const|Grp_Ctrl_"+self.side+"_Leg_Pv_Off|Ctrl_"+self.side+"_Leg_Pv"),
                    ln="KneeLock", at="double", min=0, max=1, dv=0, p="PvSettings")
            if self.haveSpaceSwitch == "Enabled":
                rawSpaces = cmds.textScrollList("lstLegsSpaceListHLegs", q=True, ai=True) # lstPvSpaceListHLegs
                spaces = []
                enums = []
                y = 0
                for rs in rawSpaces:
                    space = []
                    for x in range(0, len(rs)):
                        if rs[x] == "|": y += 1
                        elif y == 1: space.append(rs[x])
                    if not space == []: spc = ''.join(space)
                    else: spc = rs
                    spaces.append(spc)
                    spc = ''; y = 0
                for s in spaces: enums.append(s); enums.append(":")
                enum = ''.join(enums)
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="Follow", at="enum", en=enum, p="LegSettings")
                rawSpaces = cmds.textScrollList("lstPvSpaceListHLegs", q=True, ai=True)
                spaces = []
                enums = []
                y = 0
                for rs in rawSpaces:
                    space = []
                    for x in range(0, len(rs)):
                        if rs[x] == "|": y += 1
                        elif y == 1: space.append(rs[x])
                    if not space == []: spc = ''.join(space)
                    else: spc = rs
                    spaces.append(spc)
                    spc = ''; y = 0
                for s in spaces: enums.append(s); enums.append(":")
                enum = ''.join(enums)
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Leg_Pv|Grp_Ctrl_"+self.side+"_Leg_Pv_Const|Grp_Ctrl_"+self.side+"_Leg_Pv_Off|Ctrl_"+self.side+"_Leg_Pv"),
                    ln="Follow", at="enum", en=enum, p="PvSettings")
            # Set Attrs
            cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Pv|Grp_Ctrl_"+self.side+"_Leg_Pv_Const|Grp_Ctrl_"+self.side+"_Leg_Pv_Off|Ctrl_"+self.side+"_Leg_Pv.DisplayLine"),
                edit=True, k=True)
            if self.haveAutoPv == True:
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.KneeTwist"),
                    edit=True, k=True)
            if self.haveStretchIK == True:
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.Stretch"),
                    edit=True, k=True)
            if self.haveStretchMultIK == True:
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.ThighStretchMult"),
                    edit=True, k=True)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.ShinStretchMult"),
                    edit=True, k=True)
            if self.haveSquashIK == True:
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.Squash"),
                    edit=True, k=True)
            if self.haveSquashMultIK == True:
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.ThighSquashMult"),
                    edit=True, k=True)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.ShinSquashMult"),
                    edit=True, k=True)
            if self.haveClampStretchIK == True:
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.ClampStretch"),
                    edit=True, k=True)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.ClampValue"),
                    edit=True, k=True)
            if self.haveKneeLockIK == True:
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Pv|Grp_Ctrl_"+self.side+"_Leg_Pv_Const|Grp_Ctrl_"+self.side+"_Leg_Pv_Off|Ctrl_"+self.side+"_Leg_Pv.KneeLock"),
                    edit=True, k=True)
            if self.haveReverseFoot == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="FOOT", nn="____________________ FOOT", at="enum", en="__________:")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="ReverseFoot", at="compound", nc=10)
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="FootRoll", at="double", dv=0, p="ReverseFoot")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="FootRollBreak", at="double", dv=45, p="ReverseFoot")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="FootRollStraight", at="double", dv=70, p="ReverseFoot")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="FootBank", at="double", min=-90, max=90, dv=0, p="ReverseFoot")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="FootLean", at="double", dv=0, p="ReverseFoot")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="FootSpin", at="double", dv=0, p="ReverseFoot")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="ToeSpin", at="double", dv=0, p="ReverseFoot")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="ToeBend", at="double", dv=0, p="ReverseFoot")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="ToeLean", at="double", dv=0, p="ReverseFoot")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg"),
                    ln="HeelSpin", at="double", dv=0, p="ReverseFoot")
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.FOOT"),
                    edit=True, channelBox=True)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.FootRoll"),
                    edit=True, k=True)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.FootRollBreak"),
                    edit=True, k=True)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.FootRollStraight"),
                    edit=True, k=True)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.FootBank"),
                    edit=True, k=True)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.FootLean"),
                    edit=True, k=True)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.FootSpin"),
                    edit=True, k=True)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.ToeSpin"),
                    edit=True, k=True)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.ToeBend"),
                    edit=True, k=True)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.ToeLean"),
                    edit=True, k=True)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.HeelSpin"),
                    edit=True, k=True)
            if self.haveSpaceSwitch == "Enabled":
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Leg|Grp_Ctrl_"+self.side+"_IK_Leg_Const|Grp_Ctrl_"+self.side+"_IK_Leg_Off|Ctrl_"+self.side+"_IK_Leg.Follow"),
                    edit=True, k=True)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Leg_Pv|Grp_Ctrl_"+self.side+"_Leg_Pv_Const|Grp_Ctrl_"+self.side+"_Leg_Pv_Off|Ctrl_"+self.side+"_Leg_Pv.Follow"),
                    edit=True, k=True)
        elif self.haveMultLegs == 2: pass

    def setRotOrderIK(self, ikControl=""):
        cmds.setAttr((ikControl+".rotateOrder"), 5)
        # print ("ctrl = %s") %(ctrl)  | All ctrls rot order setted (ZYX)

    def associateFK(self, ctrls=[], jnts=[]):
        x = 0
        for ctrl in ctrls:
            cmds.connectAttr((ctrl+".r"), (jnts[x]+".r"))
            x += 1
        return jnts

    def setupStretchFK(self, ctrls=[], jnts=[]):
        mdShinFollow = cmds.shadingNode("multiplyDivide", asUtility=True)
        mdAnkleFollow = cmds.shadingNode("multiplyDivide", asUtility=True)
        shinFollowVal = cmds.xform(jnts[1], q=True, t=True)[0]
        ankleFollowVal = cmds.xform(jnts[2], q=True, t=True)[0]
        cmds.setAttr((mdShinFollow+".input1X"), shinFollowVal)
        cmds.setAttr((mdAnkleFollow+".input1X"), ankleFollowVal)
        cmds.connectAttr((ctrls[0]+".ThighStretch"), (mdShinFollow+".input2X"))
        cmds.connectAttr((ctrls[1]+".ShinStretch"), (mdAnkleFollow+".input2X"))
        cmds.connectAttr((mdShinFollow+".outputX"), ("Grp_"+ctrls[1]+".tx"))
        cmds.connectAttr((mdAnkleFollow+".outputX"), ("Grp_"+ctrls[2]+".tx"))
        cmds.connectAttr((ctrls[0]+".ThighStretch"), (jnts[0]+".sx"))
        cmds.connectAttr((ctrls[1]+".ShinStretch"), (jnts[1]+".sx"))
        cmds.rename(mdShinFollow, ("Md_"+self.side+"_FK_Leg_Shin_StretchFollow"))
        cmds.rename(mdAnkleFollow, ("Md_"+self.side+"_FK_Leg_Ankle_StretchFollow"))

    def setupSquashFK(self, ctrls=[], jnts=[]):
        cmds.connectAttr((ctrls[0]+".ThighSquash"), (jnts[0]+".sy"))
        cmds.connectAttr((ctrls[0]+".ThighSquash"), (jnts[0]+".sz"))
        cmds.connectAttr((ctrls[1]+".ShinSquash"), (jnts[1]+".sy"))
        cmds.connectAttr((ctrls[1]+".ShinSquash"), (jnts[1]+".sz"))

    def createIKFKSwitch(self, chains=[]):
        cmds.select(cl=True)
        numNodes = len(chains[0])
        lc = []
        for s in chains[0]: lc.append(len(s))
        x = 0
        for n in range((numNodes - 1)):
            bcT = cmds.shadingNode("blendColors", asUtility=True)
            bcR = cmds.shadingNode("blendColors", asUtility=True)
            bcS = cmds.shadingNode("blendColors", asUtility=True)
            cmds.connectAttr((chains[1][x]+".t"), (bcT+".color1"))
            cmds.connectAttr((chains[1][x]+".r"), (bcR+".color1"))
            cmds.connectAttr((chains[1][x]+".s"), (bcS+".color1"))
            cmds.connectAttr((chains[2][x]+".t"), (bcT+".color2"))
            cmds.connectAttr((chains[2][x]+".r"), (bcR+".color2"))
            cmds.connectAttr((chains[2][x]+".s"), (bcS+".color2"))
            cmds.connectAttr((bcT+".output"), (chains[0][x]+".t"))
            cmds.connectAttr((bcR+".output"), (chains[0][x]+".r"))
            cmds.connectAttr((bcS+".output"), (chains[0][x]+".s"))
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings.IKFKSwitch"), (bcT+".blender"))
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings.IKFKSwitch"), (bcR+".blender"))
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings.IKFKSwitch"), (bcS+".blender"))
            cmds.rename(bcT, ("Bc_"+chains[0][x][7:lc[x]]+"_IKFKSwitch_Trans"))
            cmds.rename(bcR, ("Bc_"+chains[0][x][7:lc[x]]+"_IKFKSwitch_Rot"))
            cmds.rename(bcS, ("Bc_"+chains[0][x][7:lc[x]]+"_IKFKSwitch_Sca"))
            x += 1

    def createAutoMSwitch(self, chains=[]):
        cmds.select(cl=True)
        numNodes = len(chains[3])
        lc = []
        for s in chains[0]: lc.append(len(s))
        x = 0
        for n in range((numNodes - 1)):
            bcT = cmds.shadingNode("blendColors", asUtility=True)
            bcR = cmds.shadingNode("blendColors", asUtility=True)
            bcS = cmds.shadingNode("blendColors", asUtility=True)
            cmds.connectAttr((chains[3][x]+".t"), (bcT+".color1"))
            cmds.connectAttr((chains[3][x]+".r"), (bcR+".color1"))
            cmds.connectAttr((chains[3][x]+".s"), (bcS+".color1"))
            cmds.connectAttr((chains[4][x]+".t"), (bcT+".color2"))
            cmds.connectAttr((chains[4][x]+".r"), (bcR+".color2"))
            cmds.connectAttr((chains[4][x]+".s"), (bcS+".color2"))
            cmds.connectAttr((bcT+".output"), (chains[2][x]+".t"))
            cmds.connectAttr((bcR+".output"), (chains[2][x]+".r"))
            cmds.connectAttr((bcS+".output"), (chains[2][x]+".s"))
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings.AutoManualSwitch"), (bcT+".blender"))
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings.AutoManualSwitch"), (bcR+".blender"))
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings.AutoManualSwitch"), (bcS+".blender"))
            cmds.rename(bcT, ("Bc_"+chains[0][x][7:lc[x]]+"_AutoManualSwitch_Trans"))
            cmds.rename(bcR, ("Bc_"+chains[0][x][7:lc[x]]+"_AutoManualSwitch_Rot"))
            cmds.rename(bcS, ("Bc_"+chains[0][x][7:lc[x]]+"_AutoManualSwitch_Sca"))
            x += 1

    def createMultSwitch(self, chains=[], name=""):
        cmds.select(cl=True)
        numChains = len(chains)
        numNodes = len(chains[0])
        lc = []
        for s in chains[0]: lc.append(len(s))
        x = 0
        for n in range((numNodes - 1)):
            chTX = cmds.shadingNode("choice", asUtility=True)
            chTY = cmds.shadingNode("choice", asUtility=True)
            chTZ = cmds.shadingNode("choice", asUtility=True)
            chRX = cmds.shadingNode("choice", asUtility=True)
            chRY = cmds.shadingNode("choice", asUtility=True)
            chRZ = cmds.shadingNode("choice", asUtility=True)
            chSX = cmds.shadingNode("choice", asUtility=True)
            chSY = cmds.shadingNode("choice", asUtility=True)
            chSZ = cmds.shadingNode("choice", asUtility=True)
            for c in range((numChains - 1)):
                cmds.connectAttr((chains[c][n]+".tx"), (chTX+".input["+str(c)+"]"))
                cmds.connectAttr((chains[c][n]+".ty"), (chTY+".input["+str(c)+"]"))
                cmds.connectAttr((chains[c][n]+".tz"), (chTZ+".input["+str(c)+"]"))
                cmds.connectAttr((chains[c][n]+".rx"), (chRX+".input["+str(c)+"]"))
                cmds.connectAttr((chains[c][n]+".ry"), (chRY+".input["+str(c)+"]"))
                cmds.connectAttr((chains[c][n]+".rz"), (chRZ+".input["+str(c)+"]"))
                cmds.connectAttr((chains[c][n]+".sx"), (chSX+".input["+str(c)+"]"))
                cmds.connectAttr((chains[c][n]+".sy"), (chSY+".input["+str(c)+"]"))
                cmds.connectAttr((chains[c][n]+".sz"), (chSZ+".input["+str(c)+"]"))
            cmds.connectAttr((chTX+".output"), (chains[-1][n]+".tx"))
            cmds.connectAttr((chTY+".output"), (chains[-1][n]+".ty"))
            cmds.connectAttr((chTZ+".output"), (chains[-1][n]+".tz"))
            cmds.connectAttr((chRX+".output"), (chains[-1][n]+".rx"))
            cmds.connectAttr((chRY+".output"), (chains[-1][n]+".ry"))
            cmds.connectAttr((chRZ+".output"), (chains[-1][n]+".rz"))
            cmds.connectAttr((chSX+".output"), (chains[-1][n]+".sx"))
            cmds.connectAttr((chSY+".output"), (chains[-1][n]+".sy"))
            cmds.connectAttr((chSZ+".output"), (chains[-1][n]+".sz"))
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings."+name), (chTX+".selector"))
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings."+name), (chTY+".selector"))
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings."+name), (chTZ+".selector"))
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings."+name), (chRX+".selector"))
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings."+name), (chRY+".selector"))
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings."+name), (chRZ+".selector"))
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings."+name), (chSX+".selector"))
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings."+name), (chSY+".selector"))
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings."+name), (chSZ+".selector"))
            cmds.rename(chTX, ("Ch_"+chains[-1][x][7:lc[x]]+"_"+name+"_tx"))
            cmds.rename(chTY, ("Ch_"+chains[-1][x][7:lc[x]]+"_"+name+"_ty"))
            cmds.rename(chTZ, ("Ch_"+chains[-1][x][7:lc[x]]+"_"+name+"_tz"))
            cmds.rename(chRX, ("Ch_"+chains[-1][x][7:lc[x]]+"_"+name+"_rx"))
            cmds.rename(chRY, ("Ch_"+chains[-1][x][7:lc[x]]+"_"+name+"_ry"))
            cmds.rename(chRZ, ("Ch_"+chains[-1][x][7:lc[x]]+"_"+name+"_rz"))
            cmds.rename(chSX, ("Ch_"+chains[-1][x][7:lc[x]]+"_"+name+"_sx"))
            cmds.rename(chSY, ("Ch_"+chains[-1][x][7:lc[x]]+"_"+name+"_sy"))
            cmds.rename(chSZ, ("Ch_"+chains[-1][x][7:lc[x]]+"_"+name+"_sz"))
            x += 1

    def connectIKFKSwitchVis(self, settingsCtrl=""):
        rev = cmds.shadingNode("reverse", asUtility=True, n=("Rev_"+self.side+"_IK_Leg_IKFKSwitch_Vis"))
        cmds.connectAttr((settingsCtrl+".IKFKSwitch"), (rev+".inputX"))
        cmds.connectAttr((rev+".outputX"), ("Grp_Ctrl_"+self.side+"_IK_Leg.v"))
        cmds.connectAttr((rev+".outputX"), ("Grp_Ctrl_"+self.side+"_Leg_Pv.v"))
        cmds.connectAttr((rev+".outputX"), ("Grp_Crv_"+self.side+"_Leg_Pv_DispLine.v"))
        cmds.connectAttr((settingsCtrl+".IKFKSwitch"), ("Grp_Ctrl_"+self.side+"_FK_Leg.v"))
        if self.haveAutoPv == True:
            cmds.connectAttr((settingsCtrl+".AutoManualSwitch"), ("Ctrl_"+self.side+"_Leg_Pv.v"))
            cmds.connectAttr((settingsCtrl+".AutoManualSwitch"), ("Grp_Crv_"+self.side+"_Leg_Pv_DispLine_Off.v"))
        # else:
        #     cmds.connectAttr((settingsCtrl+".IKFKSwitch"), ("Ctrl_"+self.side+"_Leg_Pv.v"))
        #     cmds.connectAttr((settingsCtrl+".IKFKSwitch"), ("Grp_Crv_"+self.side+"_Leg_Pv_DispLine_Off.v"))

    def associateIK(self, ctrlLeg="", jnts=[]):
        iks = []
        # IK Ball
        ikBall = cmds.ikHandle(n=("ikHdle_"+self.side+"_IK_Ball"), sol="ikRPsolver", sj=jnts[2][2], ee=jnts[2][3])
        cmds.rename(ikBall[1], ("Eff_"+self.side+"_IK_Ball"))
        iks.append(ikBall[0])
        # IK Toe
        ikToe = cmds.ikHandle(n=("ikHdle_"+self.side+"_IK_Toe"), sol="ikRPsolver", sj=jnts[2][3], ee=jnts[2][4])
        cmds.rename(ikToe[1], ("Eff_"+self.side+"_IK_Toe"))
        iks.append(ikToe[0])
        if self.haveAutoPv == True:
            # IK Pv
            ikPv = cmds.ikHandle(n=("ikHdle_"+self.side+"_Pv_Leg"), sol="ikRPsolver", sj=jnts[3][0], ee=jnts[3][2])
            cmds.rename(ikPv[1], ("Eff_"+self.side+"_Pv_Leg"))
            cmds.select(("Ctrl_"+self.side+"_Leg_Pv"), ikPv[0], r=True)
            cmds.poleVectorConstraint(weight=1)
            iks.append(ikPv[0])
            # IK NoFlip
            ikNoFlip = cmds.ikHandle(n=("ikHdle_"+self.side+"_NoFlip_Leg"), sol="ikRPsolver", sj=jnts[4][0], ee=jnts[4][2])
            cmds.rename(ikNoFlip[1], ("Eff_"+self.side+"_NoFlip_Leg"))
            loc = cmds.spaceLocator(p=(0, 0, 0))
            cmds.move(self.posAnkle[0], self.posAnkle[1], self.posAnkle[2], loc, r=True)
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
            if self.side == "L": cmds.move((5 * self.gblScaleGuide[0]), 0, 0, loc, r=True)
            elif self.side == "R": cmds.move((-5 * self.gblScaleGuide[0]), 0, 0, loc, r=True)
            cmds.select(loc, ikNoFlip[0], r=True)
            cmds.poleVectorConstraint(weight=1)
            if self.side == "L": cmds.setAttr((ikNoFlip[0]+".twist"), 90)
            elif self.side == "R": cmds.setAttr((ikNoFlip[0]+".twist"), -90)
            cmds.select(loc, r=True)
            grp = cmds.group(n=("Grp_Loc_"+self.side+"_NoFlip_Knee"))
            cmds.move(self.posAnkle[0], self.posAnkle[1], self.posAnkle[2], (grp+".rotatePivot"), (grp+".scalePivot"))
            if self.haveReverseFoot == False:
                cmds.select(ctrlLeg, grp, r=True)
                pntConst = cmds.pointConstraint(weight=1)
            cmds.connectAttr(("Ctrl_"+self.side+"_IK_Leg.KneeTwist"), (grp+".ry"))
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Pv.DisplayLine"), ("Crv_"+self.side+"_Leg_Pv_DispLine.v"))
            cmds.setAttr((loc[0]+".visibility"), False)
            cmds.setAttr(("Ctrl_"+self.side+"_Leg_Pv.DisplayLine"), 1)
            cmds.rename(loc, ("Loc_"+self.side+"_NoFlip_Knee"))
            iks.append(ikNoFlip[0])
        else:
            # IK Leg
            ikLeg = cmds.ikHandle(n=("ikHdle_"+self.side+"_IK_Leg"), sol="ikRPsolver", sj=jnts[2][0], ee=jnts[2][2])
            cmds.rename(ikLeg[1], ("Eff_"+self.side+"_IK_Leg"))
            cmds.select(("Ctrl_"+self.side+"_Leg_Pv"), ikLeg[0], r=True)
            cmds.poleVectorConstraint(weight=1)
            cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Pv.DisplayLine"), ("Crv_"+self.side+"_Leg_Pv_DispLine.v"))
            cmds.setAttr(("Ctrl_"+self.side+"_Leg_Pv.DisplayLine"), 1)
            iks.append(ikLeg[0])
        cmds.select(iks, r=True)
        grp = cmds.group(n=("Grp_ikHdle_"+self.side+"_Leg"))
        cmds.move(self.posAnkle[0], self.posAnkle[1], self.posAnkle[2], (grp+".rotatePivot"), (grp+".scalePivot"))
        cmds.select(("Ctrl_"+self.side+"_IK_Leg"), grp, r=True)
        cmds.parentConstraint(weight=1)
        return iks, grp

    def createReverseFoot(self, ikHandles=[]):
        loc1 = cmds.spaceLocator(p=(0, 0, 0))
        loc2 = cmds.spaceLocator(p=(0, 0, 0))
        loc3 = cmds.spaceLocator(p=(0, 0, 0))
        loc4 = cmds.spaceLocator(p=(0, 0, 0))
        loc5 = cmds.spaceLocator(p=(0, 0, 0))
        clampHeelRot = cmds.shadingNode("clamp", asUtility=True)
        clampZeroToBend = cmds.shadingNode("clamp", asUtility=True)
        rangeZeroToBend = cmds.shadingNode("setRange", asUtility=True)
        clampBendToStraight = cmds.shadingNode("clamp", asUtility=True)
        rangeBendToStraight = cmds.shadingNode("setRange", asUtility=True)
        mdRollMult = cmds.shadingNode("multiplyDivide", asUtility=True)
        pmaInvert = cmds.shadingNode("plusMinusAverage", asUtility=True)
        mdPercentMult = cmds.shadingNode("multiplyDivide", asUtility=True)
        mdBallRollMult = cmds.shadingNode("multiplyDivide", asUtility=True)
        cmds.move(self.posTipHeel[0], self.posTipHeel[1], self.posTipHeel[2], loc1, r=True)
        cmds.move(self.posToe[0], self.posToe[1], self.posToe[2], loc2, r=True)
        cmds.move(self.posLegEnd[0], self.posLegEnd[1], self.posLegEnd[2], loc3, r=True)
        cmds.move(self.posInFoot[0], self.posInFoot[1], self.posInFoot[2], loc4, r=True)
        cmds.move(self.posOutFoot[0], self.posOutFoot[1], self.posOutFoot[2], loc5, r=True)
        cmds.parent(loc1, loc2, loc3, ("Grp_ikHdle_"+self.side+"_Leg"))
        cmds.parent(loc4, loc5)
        cmds.parent(loc5, loc1)
        cmds.parent(ikHandles[0:4], loc2, loc3, loc1)
        cmds.parent(ikHandles[0], ikHandles[2:4], loc2)
        cmds.parent(loc2, loc3)
        if cmds.objExists(("Grp_Loc_"+self.side+"_NoFlip_Knee")):
            cmds.parent(("Grp_Loc_"+self.side+"_NoFlip_Knee"), loc2)
        # Smart Foot Roll
        cmds.connectAttr(("Ctrl_"+self.side+"_IK_Leg.FootRoll"), (clampHeelRot+".inputR"))
        cmds.setAttr((clampHeelRot+".minR"), -90)
        cmds.connectAttr((clampHeelRot+".outputR"), (loc1[0]+".rx"))
        cmds.connectAttr(("Ctrl_"+self.side+"_IK_Leg.FootRoll"), (clampZeroToBend+".inputR"))
        cmds.connectAttr(("Ctrl_"+self.side+"_IK_Leg.FootRollBreak"), (clampZeroToBend+".maxR"))
        cmds.connectAttr((clampZeroToBend+".minR"), (rangeZeroToBend+".oldMinX"))
        cmds.connectAttr((clampZeroToBend+".maxR"), (rangeZeroToBend+".oldMaxX"))
        cmds.connectAttr((clampZeroToBend+".inputR"), (rangeZeroToBend+".valueX"))
        cmds.setAttr((rangeZeroToBend+".maxX"), 1)
        cmds.connectAttr(("Ctrl_"+self.side+"_IK_Leg.FootRollBreak"), (clampBendToStraight+".minR"))
        cmds.connectAttr(("Ctrl_"+self.side+"_IK_Leg.FootRollStraight"), (clampBendToStraight+".maxR"))
        cmds.connectAttr(("Ctrl_"+self.side+"_IK_Leg.FootRoll"), (clampBendToStraight+".inputR"))
        cmds.connectAttr((clampBendToStraight+".minR"), (rangeBendToStraight+".oldMinX"))
        cmds.connectAttr((clampBendToStraight+".maxR"), (rangeBendToStraight+".oldMaxX"))
        cmds.setAttr((rangeBendToStraight+".maxX"), 1)
        cmds.connectAttr((clampBendToStraight+".inputR"), (rangeBendToStraight+".valueX"))
        cmds.connectAttr((rangeBendToStraight+".outValueX"), (mdRollMult+".input1X"))
        cmds.connectAttr((clampBendToStraight+".inputR"), (mdRollMult+".input2X"))
        cmds.connectAttr((mdRollMult+".outputX"), (loc3[0]+".rx"))
        cmds.setAttr((pmaInvert+".input1D[0]"), 1)
        cmds.connectAttr((rangeBendToStraight+".outValueX"), (pmaInvert+".input1D[1]"))
        cmds.setAttr((pmaInvert+".operation"), 2)
        cmds.connectAttr((rangeZeroToBend+".outValueX"), (mdPercentMult+".input1X"))
        cmds.connectAttr((pmaInvert+".output1D"), (mdPercentMult+".input2X"))
        cmds.connectAttr((mdPercentMult+".outputX"), (mdBallRollMult+".input1X"))
        cmds.connectAttr(("Ctrl_"+self.side+"_IK_Leg.FootRoll"), (mdBallRollMult+".input2X"))
        cmds.connectAttr((mdBallRollMult+".outputX"), (loc2[0]+".rx"))
        cmds.parent(loc3, ikHandles[1], loc4)
        cmds.select(ikHandles[1], r=True)
        grp = cmds.group(n=("Grp_"+self.side+"_ToeBend_Pivot"))
        cmds.move(self.posToe[0], self.posToe[1], self.posToe[2], (grp+".rotatePivot"), (grp+".scalePivot"))
        cmds.parent(grp, loc3)
        cmds.connectAttr(("Ctrl_"+self.side+"_IK_Leg.FootLean"), (loc2[0]+".rz"))
        cmds.connectAttr(("Ctrl_"+self.side+"_IK_Leg.FootSpin"), (loc2[0]+".ry"))
        cmds.connectAttr(("Ctrl_"+self.side+"_IK_Leg.ToeSpin"), (loc3[0]+".ry"))
        cmds.connectAttr(("Ctrl_"+self.side+"_IK_Leg.ToeBend"), (grp+".rx"))
        cmds.connectAttr(("Ctrl_"+self.side+"_IK_Leg.ToeLean"), (grp+".rz"))
        cmds.connectAttr(("Ctrl_"+self.side+"_IK_Leg.HeelSpin"), (loc1[0]+".ry"))
        cmds.setAttr((loc3[0]+".rotateOrder"), 2)
        cmds.setAttr((grp+".v"), False)
        cmds.setAttr((loc1[0]+".v"), False)
        cmds.rename(loc1, ("Loc_"+self.side+"_Foot_Heel"))
        cmds.setAttr((loc2[0]+".v"), False)
        cmds.rename(loc2, ("Loc_"+self.side+"_Foot_Ball"))
        cmds.setAttr((loc3[0]+".v"), False)
        cmds.rename(loc3, ("Loc_"+self.side+"_Foot_Toe"))
        cmds.setAttr((loc4[0]+".v"), False)
        cmds.rename(loc4, ("Loc_"+self.side+"_Inner_Foot"))
        cmds.setAttr((loc5[0]+".v"), False)
        cmds.rename(loc5, ("Loc_"+self.side+"_Outer_Foot"))
        if self.side == "L":
            cmds.expression(s="Loc_L_Inner_Foot.rz=clamp(0,90,Ctrl_L_IK_Leg.FootBank);\nLoc_L_Outer_Foot.rz=clamp(-90,0,Ctrl_L_IK_Leg.FootBank)", n="Exp_L_Foot_Bank", ae=1)
        elif self.side == "R":
            cmds.expression(s="Loc_R_Inner_Foot.rz=clamp(-90,0,Ctrl_R_IK_Leg.FootBank);\nLoc_R_Outer_Foot.rz=clamp(0,90,Ctrl_R_IK_Leg.FootBank)", n="Exp_R_Foot_Bank", ae=1)
        cmds.rename(clampHeelRot, ("Cmp_"+self.side+"_Foot_Heel_Rot"))
        cmds.rename(clampZeroToBend, ("Cmp_"+self.side+"_Foot_Ball_ZeroToBend"))
        cmds.rename(rangeZeroToBend, ("Srg_"+self.side+"_Foot_Ball_ZeroToBend_Percent"))
        cmds.rename(clampBendToStraight, ("Cmp_"+self.side+"_Foot_BendToStraight"))
        cmds.rename(rangeBendToStraight, ("Srg_"+self.side+"_Foot_BendToStraight_Percent"))
        cmds.rename(mdRollMult, ("Md_"+self.side+"_Foot_Roll_Mult"))
        cmds.rename(pmaInvert, ("Pma_"+self.side+"_Foot_Ball_Invert_Percentage"))
        cmds.rename(mdPercentMult, ("Md_"+self.side+"_Foot_Ball_Percent_Mult"))
        cmds.rename(mdBallRollMult, ("Md_"+self.side+"_Foot_Ball_Roll_Mult"))

    def setupStretchIK(self, ctrls=[], pvLoc="", pvCtrl="", chains=[]):
        locs = []
        locThigh = cmds.spaceLocator(p=(0, 0, 0), n=("Loc_"+self.side+"_Thigh"))
        locShin = cmds.spaceLocator(p=(0, 0, 0), n=("Loc_"+self.side+"_Shin"))
        locAnkle = cmds.spaceLocator(p=(0, 0, 0), n=("Loc_"+self.side+"_Ankle"))
        locs.append(locThigh[0]); locs.append(locShin[0]); locs.append(locAnkle[0])
        dbThighLength = cmds.shadingNode("distanceBetween", asUtility=True, n=("Db_"+self.side+"_Thigh_Length"))
        dbShinLength = cmds.shadingNode("distanceBetween", asUtility=True, n=("Db_"+self.side+"_Shin_Length"))
        dbLegLength = cmds.shadingNode("distanceBetween", asUtility=True, n=("Db_"+self.side+"_Leg_Length"))
        pmaSumDistance = cmds.shadingNode("plusMinusAverage", asUtility=True, n=("Pma_"+self.side+"_IK_Leg_Stretch_SumInfo"))
        mdSumDistance = cmds.shadingNode("multiplyDivide", asUtility=True, n=("Md_"+self.side+"_IK_Leg_Stretch_SumInfo"))
        mdStretch = cmds.shadingNode("multiplyDivide", asUtility=True, n=("Md_"+self.side+"_IK_Leg_Stretch_Div"))
        cndStretch = cmds.shadingNode("condition", asUtility=True, n=("Cnd_"+self.side+"_IK_Leg_Stretch"))
        cndStretchSwitch = cmds.shadingNode("condition", asUtility=True, n=("Cnd_"+self.side+"_IK_Leg_Stretch_Switch"))
        ucStretch = cmds.shadingNode("unitConversion", asUtility=True, n=("Uc_"+self.side+"_IK_Leg_Stretch"))
        if self.haveStretchMultIK == True:
            cndStretchMultSwitch = cmds.shadingNode("condition", asUtility=True, n=("Cnd_"+self.side+"_IK_Leg_StretchMult_Switch"))
            mdThighStretchMult = cmds.shadingNode("multiplyDivide", asUtility=True, n=("Md_"+self.side+"_IK_Leg_ThighStretch_Mult"))
            mdShinStretchMult = cmds.shadingNode("multiplyDivide", asUtility=True, n=("Md_"+self.side+"_IK_Leg_ShinStretch_Mult"))
        if self.haveClampStretchIK == True:
            cmpClampStretch = cmds.shadingNode("clamp", asUtility=True, n=("Cmp_"+self.side+"_IK_Leg_Stretch"))
            bcClampStretchSwitch = cmds.shadingNode("blendColors", asUtility=True, n=("Bc_"+self.side+"_IK_Leg_Stretch_ClampSwitch"))
        if self.haveSquashIK == True:
            mdSquashPow = cmds.shadingNode("multiplyDivide", asUtility=True, n=("Md_"+self.side+"_IK_Leg_Squash_Pow"))
            mdSquashInv = cmds.shadingNode("multiplyDivide", asUtility=True, n=("Md_"+self.side+"_IK_Leg_SquashInv_Div"))
            ucSquash = cmds.shadingNode("unitConversion", asUtility=True, n=("Uc_"+self.side+"_IK_Leg_Squash"))
            ucSquashSwitch = cmds.shadingNode("unitConversion", asUtility=True, n=("Uc_"+self.side+"_IK_Leg_SquashSwitch"))
        if self.haveSquashMultIK == True:
            cndSquashMultSwitch = cmds.shadingNode("condition", asUtility=True, n=("Cnd_"+self.side+"_IK_Leg_SquashMult_Switch"))
            mdThighSquashMult = cmds.shadingNode("multiplyDivide", asUtility=True, n=("Md_"+self.side+"_IK_Leg_ThighSquash_Mult"))
            mdShinSquashMult = cmds.shadingNode("multiplyDivide", asUtility=True, n=("Md_"+self.side+"_IK_Leg_ShinSquash_Mult"))
        if self.haveKneeLockIK == True:
            dbThighToKneeLength = cmds.shadingNode("distanceBetween", asUtility=True, n=("Db_"+self.side+"_ThighToKnee_Length"))
            dbKneeToAnkleLength = cmds.shadingNode("distanceBetween", asUtility=True, n=("Db_"+self.side+"_KneeToAnkle_Length"))
            mdKneeLock = cmds.shadingNode("multiplyDivide", asUtility=True, n=("Md_"+self.side+"_IK_Leg_KneeLock_Div"))
            b2aThighKneeLock = cmds.shadingNode("blendTwoAttr", asUtility=True, n=("B2a_"+self.side+"_IK_Leg_Thigh_KneeLock"))
            b2aShinKneeLock =cmds.shadingNode("blendTwoAttr", asUtility=True, n=("B2a_"+self.side+"_IK_Leg_Shin_KneeLock"))
        if self.gblScale == True: mdStretchGblSca = cmds.shadingNode("multiplyDivide", asUtility=True, n=("Md_"+self.side+"_IK_Leg_Stretch_GlobalScale_Mult"))
        cmds.move(self.posThigh[0], self.posThigh[1], self.posThigh[2], locThigh, r=True)
        cmds.move(self.posShin[0], self.posShin[1], self.posShin[2], locShin, r=True)
        cmds.move(self.posAnkle[0], self.posAnkle[1], self.posAnkle[2], locAnkle, r=True)
        cmds.parent(locAnkle, ctrls[0])
        cmds.select(locThigh, r=True)
        locThighShape = cmds.listRelatives(s=True)
        cmds.setAttr((locThigh[0]+".v"), False)
        cmds.select(locShin, r=True)
        locShinShape = cmds.listRelatives(s=True)
        cmds.setAttr((locShin[0]+".v"), False)
        cmds.select(locAnkle, r=True)
        locAnkleShape = cmds.listRelatives(s=True)
        cmds.setAttr((locAnkle[0]+".v"), False)
        cmds.select(pvLoc, r=True)
        pvLocShape = cmds.listRelatives(s=True)
        cmds.setAttr((pvLoc+".v"), False)
        cmds.connectAttr((locThighShape[0]+".worldPosition[0]"), (dbThighLength+".point1"))
        cmds.connectAttr((locShinShape[0]+".worldPosition[0]"), (dbThighLength+".point2"))
        cmds.connectAttr((locShinShape[0]+".worldPosition[0]"), (dbShinLength+".point1"))
        cmds.connectAttr((locAnkleShape[0]+".worldPosition[0]"), (dbShinLength+".point2"))
        cmds.connectAttr((locThighShape[0]+".worldPosition[0]"), (dbLegLength+".point1"))
        cmds.connectAttr((locAnkleShape[0]+".worldPosition[0]"), (dbLegLength+".point2"))
        cmds.connectAttr((dbThighLength+".distance"), (pmaSumDistance+".input1D[0]"))
        cmds.connectAttr((dbShinLength+".distance"), (pmaSumDistance+".input1D[1]"))
        cmds.connectAttr((pmaSumDistance+".output1D"), (mdSumDistance+".input1X"))
        if self.gblScale == True:
            cmds.setAttr((mdStretchGblSca+".input1X"), cmds.getAttr(mdSumDistance+".input1X"), lock=True)
            if self.setupFull == 1: cmds.connectAttr("Ctrl_Global.sy", (mdStretchGblSca+".input2X"))
            cmds.connectAttr((mdStretchGblSca+".outputX"), (mdStretch+".input2X"))
        else: cmds.setAttr((mdStretch+".input2X"), cmds.getAttr(mdSumDistance+".input1X"), lock=True)
        cmds.setAttr((mdStretch+".operation"), 2)
        cmds.connectAttr((dbLegLength+".distance"), (mdStretch+".input1X"))
        cmds.connectAttr((mdStretch+".outputX"), (cndStretch+".firstTerm"))
        cmds.setAttr((cndStretch+".secondTerm"), 1)
        cmds.setAttr((cndStretch+".operation"), 3)
        cmds.connectAttr((cndStretch+".outColorR"), (ucStretch+".input"))
        cmds.connectAttr((ctrls[0]+".Stretch"), (cndStretchSwitch+".firstTerm"))
        cmds.setAttr((cndStretchSwitch+".secondTerm"), 1)
        cmds.connectAttr((cndStretchSwitch+".outColorR"), (cndStretch+".colorIfTrueR"))
        if self.haveClampStretchIK == True:
            cmds.connectAttr((mdStretch+".outputX"), (cmpClampStretch+".inputR"))
            cmds.connectAttr((ctrls[0]+".ClampValue"), (cmpClampStretch+".maxR"))
            cmds.connectAttr((cmpClampStretch+".outputR"), (bcClampStretchSwitch+".color1R"))
            cmds.connectAttr((mdStretch+".outputX"), (bcClampStretchSwitch+".color2R"))
            cmds.connectAttr((ctrls[0]+".ClampStretch"), (bcClampStretchSwitch+".blender"))
            cmds.connectAttr((bcClampStretchSwitch+".outputR"), (cndStretchSwitch+".colorIfTrueR"))
        else: cmds.connectAttr((mdStretch+".outputX"), (cndStretchSwitch+".colorIfTrueR"))
        if self.haveStretchMultIK == True:
            cmds.connectAttr((ctrls[0]+".Stretch"), (cndStretchMultSwitch+".firstTerm"))
            cmds.setAttr((cndStretchMultSwitch+".secondTerm"), 1)
            cmds.connectAttr((ucStretch+".output"), (cndStretchMultSwitch+".colorIfTrueR"))
            cmds.connectAttr((ctrls[0]+".ThighStretchMult"), (cndStretchMultSwitch+".colorIfTrueG"))
            cmds.connectAttr((ctrls[0]+".ShinStretchMult"), (cndStretchMultSwitch+".colorIfTrueB"))
            cmds.connectAttr((cndStretchMultSwitch+".outColorR"), (mdThighStretchMult+".input2X"))
            cmds.connectAttr((cndStretchMultSwitch+".outColorR"), (mdShinStretchMult+".input2X"))
            cmds.connectAttr((cndStretchMultSwitch+".outColorG"), (mdThighStretchMult+".input1X"))
            cmds.connectAttr((cndStretchMultSwitch+".outColorB"), (mdShinStretchMult+".input1X"))
        if self.haveSquashIK == True:
            cmds.setAttr((mdSquashPow+".operation"), 3)
            cmds.connectAttr((cndStretch+".outColorR"), (mdSquashPow+".input1X"))
            cmds.setAttr((mdSquashPow+".input2X"), 0.5)
            cmds.setAttr((mdSquashInv+".operation"), 2)
            cmds.connectAttr((mdSquashPow+".outputX"), (mdSquashInv+".input2X"))
            cmds.setAttr((mdSquashInv+".input1X"), 1)
            cmds.connectAttr((mdSquashInv+".outputX"), (ucSquash+".input"))
            cmds.connectAttr((ctrls[0]+".Squash"), (ucSquashSwitch+".input"))
            cmds.setAttr((ucSquashSwitch+".conversionFactor"), 2)
            cmds.connectAttr((ucSquashSwitch+".output"), (mdSquashInv+".operation"))
            if self.haveSquashMultIK == True:
                cmds.connectAttr((ctrls[0]+".Squash"), (cndSquashMultSwitch+".firstTerm"))
                cmds.setAttr((cndSquashMultSwitch+".secondTerm"), 1)
                cmds.connectAttr((ucSquash+".output"), (cndSquashMultSwitch+".colorIfTrueR"))
                cmds.connectAttr((ctrls[0]+".ThighSquashMult"), (cndSquashMultSwitch+".colorIfTrueG"))
                cmds.connectAttr((ctrls[0]+".ShinSquashMult"), (cndSquashMultSwitch+".colorIfTrueB"))
                cmds.connectAttr((cndSquashMultSwitch+".outColorR"), (mdThighSquashMult+".input2X"))
                cmds.connectAttr((cndSquashMultSwitch+".outColorR"), (mdShinSquashMult+".input2X"))
                cmds.connectAttr((cndSquashMultSwitch+".outColorG"), (mdThighSquashMult+".input1X"))
                cmds.connectAttr((cndSquashMultSwitch+".outColorB"), (mdShinSquashMult+".input1X"))
        if self.haveKneeLockIK == True:
            cmds.connectAttr((locThighShape[0]+".worldPosition[0]"), (dbThighToKneeLength+".point1"))
            cmds.connectAttr((pvLocShape[0]+".worldPosition[0]"), (dbThighToKneeLength+".point2"))
            cmds.connectAttr((pvLocShape[0]+".worldPosition[0]"), (dbKneeToAnkleLength+".point1"))
            cmds.connectAttr((locAnkleShape[0]+".worldPosition[0]"), (dbKneeToAnkleLength+".point2"))
            cmds.setAttr((mdKneeLock+".operation"), 2)
            cmds.connectAttr((dbThighToKneeLength+".distance"), (mdKneeLock+".input1X"))
            cmds.connectAttr((dbKneeToAnkleLength+".distance"), (mdKneeLock+".input1Y"))
            cmds.setAttr((mdKneeLock+".input2X"), cmds.getAttr(dbThighLength+".distance"))
            cmds.setAttr((mdKneeLock+".input2Y"), cmds.getAttr(dbShinLength+".distance"))
            cmds.connectAttr((str(pvCtrl)+".KneeLock"), (b2aThighKneeLock+".attributesBlender"))
            cmds.connectAttr((cndStretch+".outColorR"), (b2aThighKneeLock+".input[0]"))
            cmds.connectAttr((mdKneeLock+".outputX"), (b2aThighKneeLock+".input[1]"))
            cmds.connectAttr((str(pvCtrl)+".KneeLock"), (b2aShinKneeLock+".attributesBlender"))
            cmds.connectAttr((cndStretch+".outColorR"), (b2aShinKneeLock+".input[0]"))
            cmds.connectAttr((mdKneeLock+".outputY"), (b2aShinKneeLock+".input[1]"))
        # IK | PV | NoFlip
        # Stretch
        if self.haveKneeLockIK == True:
            if self.haveAutoPv == True:
                cmds.connectAttr((b2aThighKneeLock+".output"), (chains[1][0]+".sx"))
                cmds.connectAttr((b2aShinKneeLock+".output"), (chains[1][1]+".sx"))
                cmds.connectAttr((mdThighStretchMult+".outputX"), (chains[2][0]+".sx"))
                cmds.connectAttr((mdShinStretchMult+".outputX"), (chains[2][1]+".sx"))
            else:
                for chain in chains:
                    cmds.connectAttr((b2aThighKneeLock+".output"), (chain[0]+".sx"))
                    cmds.connectAttr((b2aShinKneeLock+".output"), (chain[1]+".sx"))
        else:
            if self.haveAutoPv == True:
                for chain in chains[1:len(chains)]:
                    cmds.connectAttr((mdThighStretchMult+".outputX"), (chain[0]+".sx"))
                    cmds.connectAttr((mdShinStretchMult+".outputX"), (chain[1]+".sx"))
            else:
                for chain in chains:
                    cmds.connectAttr((mdThighStretchMult+".outputX"), (chain[0]+".sx"))
                    cmds.connectAttr((mdShinStretchMult+".outputX"), (chain[1]+".sx"))
        # Squash
        if self.haveAutoPv == True:
            for chain in chains[1:len(chains)]:
                cmds.connectAttr((mdThighSquashMult+".outputX"), (chain[0]+".sy"))
                cmds.connectAttr((mdThighSquashMult+".outputX"), (chain[0]+".sz"))
                cmds.connectAttr((mdShinSquashMult+".outputX"), (chain[1]+".sy"))
                cmds.connectAttr((mdShinSquashMult+".outputX"), (chain[1]+".sz"))
        else:
            for chain in chains:
                cmds.connectAttr((mdThighSquashMult+".outputX"), (chain[0]+".sy"))
                cmds.connectAttr((mdThighSquashMult+".outputX"), (chain[0]+".sz"))
                cmds.connectAttr((mdShinSquashMult+".outputX"), (chain[1]+".sy"))
                cmds.connectAttr((mdShinSquashMult+".outputX"), (chain[1]+".sz"))
        return locs

    def createRibbon(self):
        rib = cmds.nurbsPlane(p=(0, 0, 0), ax=(0, 1, 0), w=1, lr=1, d=1, u=1, v=2, ch=1)
        cmds.CenterPivot()
        cmds.scale((2.5 * self.gblScaleGuide[0]), 1, 1, r=True)
        cmds.DeleteHistory()
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.select((rib[0]+".cv[0:1][2]"))
        clThighTEMP = cmds.cluster(n=("Cls_Rib_TEMP_Thigh"))
        cmds.select((rib[0]+".cv[0:1][1]"))
        clShinTEMP = cmds.cluster(n=("Cls_Rib_TEMP_Shin"))
        cmds.select((rib[0]+".cv[0:1][0]"))
        clAnkleTEMP = cmds.cluster(n=("Cls_Rib_TEMP_Ankle"))
        if not cmds.objExists(("Loc_"+self.side+"_Thigh")):
            locTEMP = cmds.spaceLocator(p=(self.posThigh[0], self.posThigh[1], self.posThigh[2]))
            cmds.CenterPivot()
            cmds.select(locTEMP, clThighTEMP, r=True)
            const = cmds.parentConstraint(weight=1)
            cmds.select(locTEMP, r=True)
            cmds.Delete()
        else:
            cmds.select(("Loc_"+self.side+"_Thigh"), clThighTEMP, r=True)
            const = cmds.parentConstraint(weight=1)
        if not cmds.objExists(("Loc_"+self.side+"_Shin")):
            locTEMP = cmds.spaceLocator(p=(self.posShin[0], self.posShin[1], self.posShin[2]))
            cmds.CenterPivot()
            cmds.select(locTEMP, clShinTEMP, r=True)
            const = cmds.parentConstraint(weight=1)
            cmds.select(locTEMP, r=True)
            cmds.Delete()
        else:
            cmds.select(("Loc_"+self.side+"_Shin"), clShinTEMP, r=True)
            const = cmds.parentConstraint(weight=1)
        if not cmds.objExists(("Loc_"+self.side+"_Ankle")):
            locTEMP = cmds.spaceLocator(p=(self.posAnkle[0], self.posAnkle[1], self.posAnkle[2]))
            cmds.CenterPivot()
            cmds.select(locTEMP, clAnkleTEMP, r=True)
            const = cmds.parentConstraint(weight=1)
            cmds.select(locTEMP, r=True)
            cmds.Delete()
        else:
            cmds.select(("Loc_"+self.side+"_Ankle"), clAnkleTEMP, r=True)
            const = cmds.parentConstraint(weight=1)
        cmds.select(rib[0], r=True)
        cmds.DeleteHistory()
        if cmds.objExists(clThighTEMP[0]+"Handle"):
            cmds.select(clThighTEMP[0]+"Handle", r=True)
            cmds.Delete()
        if cmds.objExists(clShinTEMP[0]+"Handle"):
            cmds.select(clShinTEMP[0]+"Handle", r=True)
            cmds.Delete()
        if cmds.objExists(clAnkleTEMP[0]+"Handle"):
            cmds.select(clAnkleTEMP[0]+"Handle", r=True)
            cmds.Delete()
        return rib[0]

    def rebuildRibbon(self, oldRib="", colors=[], settingsCtrl=""):
        jntsRib = []
        numFol = self.numberOfJntsRib - 1
        newRib = cmds.rebuildSurface(oldRib, ch=False, rpo=0, rt=0, end=1, kr=0, kcp=0, kc=0, su=1, du=1, sv=self.numberOfJntsRib, dv=3, tol=0.01, fr=0, dir=2)
        cmds.select(oldRib, r=True)
        cmds.Delete()
        if cmds.objExists("hairSystem1"): cmds.select("hairSystem1", r=True); cmds.Delete()
        if cmds.objExists("pfxHair1"): cmds.select("pfxHair1", r=True); cmds.Delete()
        if cmds.objExists("nucleus1"): cmds.select("nucleus1", r=True); cmds.Delete()
        if cmds.objExists("hairSystem1Follicles"): cmds.select("hairSystem1Follicles", r=True); cmds.Delete()
        cmds.select(newRib, r=True)
        mel.eval("createHair 1 {0} 10 0 0 0 0 5 0 2 2 1;".format(self.numberOfJntsRib))
        cmds.select("hairSystem1", "hairSystem1OutputCurves", "nucleus1", r=True)
        cmds.Delete()
        grpFol = cmds.rename("hairSystem1Follicles", ("Grp_Fol_"+self.side+"_Leg"))
        newRib = cmds.rename(newRib, ("Sfc_Rib_"+self.side+"_Leg"))
        fol = cmds.listRelatives(grpFol, c=True)
        newFol = []
        ctrlJntsGrp = []
        for x in range(0, len(fol)):
            folCrv = cmds.listRelatives(fol[x], c=True)
            cmds.select(folCrv[1], r=True)
            cmds.Delete()
            if self.haveTweakCtrlsRib == True:
                c = ctrl.Control(n=("Ctrl_Rib_"+self.side+"_Leg_"+str(len(fol) - x)), t="Circle", s=(0.5 * self.gblScaleGuide[0]), c=colors[2])
                ctrlJntsGrp.append(cmds.group(n=("Grp_"+str(c))))
                ctrl.Control(n=str(c), t="Lock and Hide", s=["v"])
                cShapes = cmds.listRelatives(str(c), s=True)
                for shape in cShapes:
                    cmds.connectAttr((settingsCtrl+".TertiaryCtrls"), (shape+".v"))
                cmds.parent(ctrlJntsGrp[x], fol[x])
                cmds.move(0, 0, 0, os=True)
                cmds.rotate(0, 0, 0, os=True)
                cmds.select(str(c), r=True)
                jntsRib.append(cmds.joint(n=("JntBnd_"+self.side+"_Leg_"+str(len(fol) - x))))
                grpJnt = cmds.group(n=("Grp_"+jntsRib[x]))
            elif self.haveTweakCtrlsRib == False:
                cmds.select(fol[x], r=True)
                jntsRib.append(cmds.joint(n=("JntBnd_"+self.side+"_Leg_"+str(len(fol) - x))))
                ctrlJntsGrp.append(cmds.group(n=("Grp_"+jntsRib[x])))
            newFol.append(cmds.rename(fol[x], ("Fol_Rib_"+self.side+"_Leg_"+str(len(fol) - x))))
            newFolShape = cmds.listRelatives(newFol[x], c=True)
            if self.setupFull == 1 and self.gblScale == True:
                cmds.select("Ctrl_Global", newFol[x], r=True)
                cmds.scaleConstraint(weight=1, mo=True)
            cmds.setAttr((newFolShape[0]+".v"), False)
        thighRot = cmds.xform(newFol[-1], q=True, ro=True)
        shinRot = cmds.xform(newFol[0], q=True, ro=True)
        return newRib, jntsRib, thighRot, shinRot, ctrlJntsGrp, grpFol

    def createBsRibbons(self, mainSfc="", bs=[], jnts=[]):
        blendSfc = []
        squashSfc = []
        if bs != []:
            if "Bend" in bs:
                cmds.select(mainSfc, r=True)
                sfc = cmds.duplicate(rr=True)
                newRib = cmds.rename(sfc, ("Sfc_Bs_Rib_"+self.side+"_Leg_Bend"))
                blendSfc.append(newRib)
            if "Twist" in bs:
                cmds.select(mainSfc, r=True)
                sfc = cmds.duplicate(rr=True)
                newRib = cmds.rename(sfc, ("Sfc_Bs_Rib_"+self.side+"_Leg_Twist"))
                blendSfc.append(newRib)
            if "Sine" in bs:
                cmds.select(mainSfc, r=True)
                sfc = cmds.duplicate(rr=True)
                newRib = cmds.rename(sfc, ("Sfc_Bs_Rib_"+self.side+"_Leg_Sine"))
                blendSfc.append(newRib)
            if "Squash" in bs:
                cmds.select(mainSfc, r=True)
                sfc = cmds.duplicate(rr=True)
                newRib = cmds.rename(sfc, ("Sfc_Bs_Rib_"+self.side+"_Leg_Squash"))
                squashSfc.append(newRib)
            if "Extra" in bs[-1]:
                for new in range(1, (bs[-1][1] + 1)):
                    cmds.select(mainSfc, r=True)
                    sfc = cmds.duplicate(rr=True)
                    newRib = cmds.rename(sfc, ("Sfc_Bs_Rib_"+self.side+"_Leg_Extra_"+str(new)))
                    blendSfc.append(newRib)
        # Attach BS
        skin = cmds.skinCluster(jnts, mainSfc, tsb=True, mi=5, rui=True, omi=False, dr=4.0)
        cmds.select(blendSfc, mainSfc, r=True)
        bs = cmds.blendShape(n=("Bs_Rib_"+self.side+"_Leg"))
        for sfc in blendSfc: cmds.setAttr((bs[0]+"."+sfc), 1)
        cmds.reorderDeformers(skin[0], bs[0], mainSfc)
        blendSfc.extend(squashSfc)
        return blendSfc

    def createBendRibbon(self, mainSfc="", sfc="", color="", jntsRes=[], thighRot=[], shinRot=[], settingsCtrl=""):
        grpBends = []
        grpCtrls = []
        wireCrvs = []
        cmds.cycleCheck(e=False)
        ctrlBendLegStart = cmds.spaceLocator(n=("Ctrl_Rib_"+self.side+"_Leg_LegStart"))
        grpCtrlBendLegStart = cmds.group(n=("Grp_"+ctrlBendLegStart[0]))
        cmds.move(self.posThigh[0], self.posThigh[1], self.posThigh[2], r=True)
        cmds.rotate(thighRot[0], thighRot[1], thighRot[2], r=True)
        ctrlBendThigh = cmds.spaceLocator(n=("Ctrl_Rib_"+self.side+"_Leg_Thigh"))
        grpCtrlBendThigh = cmds.group(n=("Grp_"+ctrlBendThigh[0]))
        ctrlBendKnee = cmds.spaceLocator(n=("Ctrl_Rib_"+self.side+"_Leg_Knee"))
        grpCtrlBendKnee = cmds.group(n=("Grp_"+ctrlBendKnee[0]))
        cmds.move(self.posShin[0], self.posShin[1], self.posShin[2], r=True)
        cmds.rotate(shinRot[0], shinRot[1], shinRot[2], r=True)
        cmds.select(ctrlBendLegStart, ctrlBendKnee, grpCtrlBendThigh, r=True)
        pntConst = cmds.pointConstraint(weight=1)
        cmds.rotate(thighRot[0], thighRot[1], thighRot[2], grpCtrlBendThigh, r=True)
        ctrlBendShin = cmds.spaceLocator(n=("Ctrl_Rib_"+self.side+"_Leg_Shin"))
        grpCtrlBendShin = cmds.group(n=("Grp_"+ctrlBendShin[0]))
        ctrlBendLegEnd = cmds.spaceLocator(n=("Ctrl_Rib_"+self.side+"_Leg_LegEnd"))
        grpCtrlBendLegEnd = cmds.group(n=("Grp_"+ctrlBendLegEnd[0]))
        cmds.move(self.posAnkle[0], self.posAnkle[1], self.posAnkle[2], r=True)
        cmds.rotate(shinRot[0], shinRot[1], shinRot[2], r=True)
        cmds.select(ctrlBendKnee, ctrlBendLegEnd, grpCtrlBendShin, r=True)
        pntConst = cmds.pointConstraint(weight=1)
        cmds.rotate(shinRot[0], shinRot[1], shinRot[2], grpCtrlBendShin, r=True)
        grpBends.append(grpCtrlBendLegStart); grpBends.append(grpCtrlBendThigh); grpBends.append(grpCtrlBendKnee);
        grpBends.append(grpCtrlBendShin); grpBends.append(grpCtrlBendLegEnd)
        ctrlLegStart = cmds.spaceLocator(n=("Ctrl_"+self.side+"_Leg_LegStart_Bend")) # <-------------------------------------------------------- REVER!!!!
        grpCtrlLegStart = cmds.group(n=("Grp_"+ctrlLegStart[0]))
        cmds.connectAttr((settingsCtrl+".SecondaryCtrls"), (ctrlLegStart[0]+".v"))
        ctrl.Control(n=ctrlLegStart[0], t="Lock and Hide", s=["v"])
        cmds.move(self.posThigh[0], self.posThigh[1], self.posThigh[2], r=True)
        cmds.rotate(thighRot[0], thighRot[1], thighRot[2], r=True)
        ctrlThigh = ctrl.Control(n=("Ctrl_"+self.side+"_Leg_Thigh_Bend"), t="Gear Smooth", s=(0.75 * self.gblScaleGuide[0]), c=color)
        grpCtrlThigh = cmds.group(n=("Grp_"+str(ctrlThigh)))
        cmds.connectAttr((settingsCtrl+".SecondaryCtrls"), (str(ctrlThigh)+".v"))
        ctrl.Control(n=str(ctrlThigh), t="Lock and Hide", s=["v"])
        ctrlKnee = ctrl.Control(n=("Ctrl_"+self.side+"_Leg_Knee_Bend"), t="Gear Smooth", s=(0.75 * self.gblScaleGuide[0]), c=color)
        grpCtrlKnee = cmds.group(n=("Grp_"+str(ctrlKnee)))
        cmds.connectAttr((settingsCtrl+".SecondaryCtrls"), (str(ctrlKnee)+".v"))
        ctrl.Control(n=str(ctrlKnee), t="Lock and Hide", s=["v"])
        cmds.move(self.posShin[0], self.posShin[1], self.posShin[2], r=True)
        cmds.rotate(shinRot[0], shinRot[1], shinRot[2], r=True)
        cmds.select(ctrlLegStart, ctrlKnee, grpCtrlThigh, r=True)
        pntConst = cmds.pointConstraint(weight=1)
        cmds.rotate(thighRot[0], thighRot[1], thighRot[2], grpCtrlThigh, r=True)
        ctrlShin = ctrl.Control(n=("Ctrl_"+self.side+"_Leg_Shin_Bend"), t="Gear Smooth", s=(0.75 * self.gblScaleGuide[0]), c=color)
        grpCtrlShin = cmds.group(n=("Grp_"+str(ctrlShin)))
        cmds.connectAttr((settingsCtrl+".SecondaryCtrls"), (str(ctrlShin)+".v"))
        ctrl.Control(n=str(ctrlShin), t="Lock and Hide", s=["v"])
        ctrlLegEnd = cmds.spaceLocator(n=("Ctrl_"+self.side+"_Leg_LegEnd_Bend"))
        grpCtrlLegEnd = cmds.group(n=("Grp_"+ctrlLegEnd[0]))
        grpCtrls.append(grpCtrlLegStart); grpCtrls.append(grpCtrlThigh); grpCtrls.append(grpCtrlKnee);
        grpCtrls.append(grpCtrlShin); grpCtrls.append(grpCtrlLegEnd)
        cmds.connectAttr((settingsCtrl+".SecondaryCtrls"), (ctrlLegEnd[0]+".v"))
        ctrl.Control(n=ctrlLegEnd[0], t="Lock and Hide", s=["v"])
        cmds.move(self.posAnkle[0], self.posAnkle[1], self.posAnkle[2], r=True)
        cmds.rotate(shinRot[0], shinRot[1], shinRot[2], r=True)
        cmds.select(ctrlKnee, ctrlLegEnd, grpCtrlShin, r=True)
        pntConst = cmds.pointConstraint(weight=1)
        cmds.rotate(shinRot[0], shinRot[1], shinRot[2], grpCtrlShin, r=True)
        thighMidPos = [((self.posThigh[0] + self.posShin[0]) / 2), ((self.posThigh[1] + self.posShin[1]) / 2), ((self.posThigh[2] + self.posShin[2]) / 2)]
        shinMidPos = [((self.posShin[0] + self.posAnkle[0]) / 2), ((self.posShin[1] + self.posAnkle[1]) / 2), ((self.posShin[2] + self.posAnkle[2]) / 2)]
        wireCrvThigh = cmds.curve(d=2, p=[self.posThigh, thighMidPos, self.posShin], k=[0, 0, 1, 1], n=("Crv_"+self.side+"_Thigh_Bend"))
        wireCrvs.append(wireCrvThigh)
        wireCrvs.append(wireCrvThigh+"BaseWire")
        wireCrvShin = cmds.curve(d=2, p=[self.posShin, shinMidPos, self.posAnkle], k=[0, 0, 1, 1], n=("Crv_"+self.side+"_Shin_Bend"))
        wireCrvs.append(wireCrvShin)
        wireCrvs.append(wireCrvShin+"BaseWire")
        cmds.select(wireCrvThigh+".cv[0:1]", r=True)
        clsThighTop = cmds.cluster(n=("Cls_"+self.side+"_Thigh_Top_Wire"))
        clsThighTopShape = cmds.listRelatives(clsThighTop[1], s=True)
        cmds.cluster(clsThighTop[0], e=True, bs=1, wn=(ctrlBendLegStart[0], ctrlBendLegStart[0]))
        cmds.select(clsThighTop[1], r=True)
        cmds.Delete()
        cmds.setAttr(clsThighTopShape[0]+".visibility", False)
        cmds.select(wireCrvThigh+".cv[1:2]", r=True)
        clsThighBot = cmds.cluster(n=("Cls_"+self.side+"_Thigh_Bot_Wire"))
        clsThighBotShape = cmds.listRelatives(clsThighBot[1], s=True)
        cmds.cluster(clsThighBot[0], e=True, bs=1, wn=(ctrlBendKnee[0], ctrlBendKnee[0]))
        cmds.select(clsThighBot[1], r=True)
        cmds.Delete()
        cmds.setAttr(clsThighBotShape[0]+".visibility", False)
        cmds.select(wireCrvThigh+".cv[1]", r=True)
        clsThighMid = cmds.cluster(n=("Cls_"+self.side+"_Thigh_Mid_Wire"))
        clsThighMidShape = cmds.listRelatives(clsThighMid[1], s=True)
        cmds.cluster(clsThighMid[0], e=True, bs=1, wn=(ctrlBendThigh[0], ctrlBendThigh[0]))
        cmds.select(clsThighMid[1], r=True)
        cmds.Delete()
        cmds.setAttr(clsThighMidShape[0]+".visibility", False)
        cmds.percent(clsThighTop[0], (wireCrvThigh+".cv[1]"), v=0)
        cmds.percent(clsThighBot[0], (wireCrvThigh+".cv[1]"), v=0)
        cmds.select(wireCrvShin+".cv[0:1]", r=True)
        clsShinTop = cmds.cluster(n=("Cls_"+self.side+"_Shin_Top_Wire"))
        clsShinTopShape = cmds.listRelatives(clsShinTop[1], s=True)
        cmds.cluster(clsShinTop[0], e=True, bs=1, wn=(ctrlBendKnee[0], ctrlBendKnee[0]))
        cmds.select(clsShinTop[1], r=True)
        cmds.Delete()
        cmds.setAttr(clsShinTopShape[0]+".visibility", False)
        cmds.select(wireCrvShin+".cv[1:2]", r=True)
        clsShinBot = cmds.cluster(n=("Cls_"+self.side+"_Shin_Bot_Wire"))
        clsShinBotShape = cmds.listRelatives(clsShinBot[1], s=True)
        cmds.cluster(clsShinBot[0], e=True, bs=1, wn=(ctrlBendLegEnd[0], ctrlBendLegEnd[0]))
        cmds.select(clsShinBot[1], r=True)
        cmds.Delete()
        cmds.setAttr(clsShinBotShape[0]+".visibility", False)
        cmds.select(wireCrvShin+".cv[1]", r=True)
        clsShinMid = cmds.cluster(n=("Cls_"+self.side+"_Shin_Mid_Wire"))
        clsShinMidShape = cmds.listRelatives(clsShinMid[1], s=True)
        cmds.cluster(clsShinMid[0], e=True, bs=1, wn=(ctrlBendShin[0], ctrlBendShin[0]))
        cmds.select(clsShinMid[1], r=True)
        cmds.Delete()
        cmds.setAttr(clsShinMidShape[0]+".visibility", False)
        cmds.percent(clsShinTop[0], (wireCrvShin+".cv[1]"), v=0)
        cmds.percent(clsShinBot[0], (wireCrvShin+".cv[1]"), v=0)
        spansU = cmds.getAttr((sfc+".spansU"))
        degreeU = cmds.getAttr((sfc+".degreeU"))
        spansV = cmds.getAttr((sfc+".spansV"))
        degreeV = cmds.getAttr((sfc+".degreeV"))
        formU = cmds.getAttr((sfc+".formU"))
        formV = cmds.getAttr((sfc+".formV"))
        numCvsU = spansU + degreeU
        if formU == 2: numCvsU -= degreeU
        numCvsV = spansV + degreeV
        if formV == 2: numCvsV -= degreeV
        wireDefThigh = cmds.wire(sfc, w=wireCrvThigh, gw=False, en=1.000000, li=0.000000, ce=0.000000)
        cmds.setAttr(wireDefThigh[0]+".dropoffDistance[0]", 100)
        cmds.percent(wireDefThigh[0], (sfc+".cv[0:1][0:"+str((numCvsV - 1) / 2)+"]"), v=0)
        wireDefShin = cmds.wire(sfc, w=wireCrvShin, gw=False, en=1.000000, li=0.000000, ce=0.000000)
        cmds.setAttr(wireDefShin[0]+".dropoffDistance[0]", 100)
        cmds.percent(wireDefShin[0], (sfc+".cv[0:1]["+str(numCvsV / 2)+":"+str(numCvsV - 1)+"]"), v=0)
        cmds.connectAttr((ctrlLegStart[0]+".t"), (ctrlBendLegStart[0]+".t"))
        cmds.connectAttr((ctrlLegStart[0]+".r"), (ctrlBendLegStart[0]+".r"))
        cmds.connectAttr((str(ctrlThigh)+".t"), (ctrlBendThigh[0]+".t"))
        cmds.connectAttr((str(ctrlThigh)+".r"), (ctrlBendThigh[0]+".r"))
        cmds.connectAttr((str(ctrlKnee)+".t"), (ctrlBendKnee[0]+".t"))
        cmds.connectAttr((str(ctrlKnee)+".r"), (ctrlBendKnee[0]+".r"))
        cmds.connectAttr((str(ctrlShin)+".t"), (ctrlBendShin[0]+".t"))
        cmds.connectAttr((str(ctrlShin)+".r"), (ctrlBendShin[0]+".r"))
        cmds.connectAttr((ctrlLegEnd[0]+".t"), (ctrlBendLegEnd[0]+".t"))
        cmds.connectAttr((ctrlLegEnd[0]+".r"), (ctrlBendLegEnd[0]+".r"))
        cmds.rename(wireDefThigh[0], ("Def_"+self.side+"_Thigh_Wire"))
        cmds.rename(wireDefShin[0], ("Def_"+self.side+"_Shin_Wire"))
        cmds.setAttr(ctrlBendLegStart[0]+".v", False)
        cmds.setAttr(ctrlBendThigh[0]+".v", False)
        cmds.setAttr(ctrlBendKnee[0]+".v", False)
        cmds.setAttr(ctrlBendShin[0]+".v", False)
        cmds.setAttr(ctrlBendLegEnd[0]+".v", False)
        cmds.select(jntsRes[0], ("Grp_"+ctrlLegStart[0]), r=True)
        cmds.parentConstraint(weight=1, mo=True)
        cmds.select(jntsRes[1], ("Grp_"+str(ctrlKnee)), r=True)
        cmds.parentConstraint(weight=1, mo=True)
        cmds.select(jntsRes[2], ("Grp_"+ctrlLegEnd[0]), r=True)
        cmds.parentConstraint(weight=1, mo=True)
        cmds.cycleCheck(e=True)
        # cmds.cycleCheck(e=False)
        # cmds.select((sfc+".cv[1][*]"), r=True)
        # crv = self.convertCVtoCurve()
        # loc = cmds.spaceLocator(p=(0, 0, 0), n="gfAutoRig_TEMPLOC")
        # path = cmds.pathAnimation(loc[0], c=crv[1], fm=True, f=True, fa='x', ua='z', wut='vector', wu=(0, 0, 1), iu=False, inverseFront=True, b=False)
        # pathCon = cmds.listConnections(path)
        # try:
        #     for p in pathCon:
        #         if cmds.nodeType(p) == "animCurveTL":
        #             cmds.select(p, r=True)
        #             cmds.Delete()
        # except: pass
        # pos = [1, 0.75, 0.5, 0.25, 0]
        # names = [('JntDrv_Rib_'+self.side+'_Leg_LegStart'), ('JntDrv_Rib_'+self.side+'_Leg_Thigh'), ('JntDrv_Rib_'+self.side+'_Leg_Knee'),
        #     ('JntDrv_Rib_'+self.side+'_Leg_Shin'), ('JntDrv_Rib_'+self.side+'_Leg_LegEnd')]
        # jnts = []
        # ctrlsSfc = []
        # for x in range(0, 5):
        #     cmds.setAttr((path+".uValue"), pos[x])
        #     c = ctrl.Control(n=("Ctrl_"+names[x][7:len(names[x])]), t="Gear", s=(0.4 * self.gblScaleGuide[0]))
        #     ctrlsSfc.append(str(c))
        #     grpCtrlOff = cmds.group(n=("Grp_Ctrl_"+names[x][7:len(names[x])]+"_Off"))
        #     grpCtrl = cmds.group(n=("Grp_Ctrl_"+names[x][7:len(names[x])]))
        #     cmds.select(cl=True)
        #     jnt = cmds.joint(n=names[x])
        #     jnts.append(jnt)
        #     grpJnt = cmds.group(n=("Grp_"+names[x]))
        #     cmds.parent(grpJnt, str(c))
        #     cmds.select(loc[0], grpCtrl, r=True)
        #     parConst = cmds.parentConstraint(weight=1)
        #     cmds.select(parConst, r=True)
        #     cmds.Delete()
        #     cmds.select((str(c)+".cv[*]"), r=True)
        #     cmds.rotate(0, 0, 90, r=True, os=True)
        # for p in pathCon:
        #     try:
        #         cmds.select(p, r=True)
        #         cmds.Delete()
        #     except: pass
        # cmds.cycleCheck(e=True)
        # # Skin to surface
        # skin = cmds.skinCluster(names[0:5], sfc, tsb=True, mi=5, rui=True, omi=False, dr=4.0)
        # # cmds.deformerWeights("HLegs_Bend_Rib.xml", im=True, m="index", ig=True, df=skin[0], p=(self.scriptPath+"/skin"))
        # Create controls
        # cmds.cycleCheck(e=False)
        # cmds.select((mainSfc+".cv[1][*]"), r=True)
        # crv = self.convertCVtoCurve()
        # loc = cmds.spaceLocator(p=(0, 0, 0), n="gfAutoRig_TEMPLOC")
        # path = cmds.pathAnimation(loc[0], c=crv[1], fm=True, f=True, fa='x', ua='z', wut='vector', wu=(0, 0, 1), iu=False, inverseFront=True, b=False)
        # pathCon = cmds.listConnections(path)
        # try:
        #     for p in pathCon:
        #         if cmds.nodeType(p) == "animCurveTL":
        #             cmds.select(p, r=True)
        #             cmds.Delete()
        # except: pass
        # pos = [0.75, 0.5, 0.25]
        # ctrlsBnd = []
        # names = ['Thigh', 'Knee', 'Shin']
        # for x in range(0, 3):
        #     cmds.setAttr((path+".uValue"), pos[x])
        #     c = ctrl.Control(n=("Ctrl_"+self.side+"_"+names[x]+"_Bend"), t="Gear Smooth", s=(0.75 * self.gblScaleGuide[0]), c=color)
        #     ctrlsBnd.append(str(c))
        #     cmds.select(str(c), r=True)
        #     grpCtrlOff = cmds.group(n=("Grp_"+str(c)+"_Off"))
        #     grpCtrl = cmds.group(n=("Grp_"+str(c)))
        #     cmds.select(loc[0], grpCtrl, r=True)
        #     parConst = cmds.parentConstraint(weight=1)
        #     cmds.select(parConst, r=True)
        #     cmds.Delete()
        #     cmds.select((str(c)+".cv[*]"), r=True)
        #     cmds.rotate(0, 0, 90, r=True, os=True)
        # for p in pathCon:
        #     try:
        #         cmds.select(p, r=True)
        #         cmds.Delete()
        #     except: pass
        # cmds.cycleCheck(e=True)
        # # Create attrs
        # # Bug tip: Ctrls Bend directly connected (parent) to result joints
        # # Bug tip: Ctrls Bend don't follow in middle position of the leg (follow res jnts)
        # cmds.select(jntsRes[0], ("Grp_"+ctrlsBnd[0]), r=True)
        # cmds.parentConstraint(weight=1, mo=True)
        # cmds.select(jntsRes[1], ("Grp_"+ctrlsBnd[1]), r=True)
        # cmds.parentConstraint(weight=1, mo=True)
        # cmds.select(jntsRes[1], ("Grp_"+ctrlsBnd[2]), r=True)
        # cmds.parentConstraint(weight=1, mo=True)
        # '''
        # cmds.addAttr(("|Grp_"+ctrlsBnd[1]+"|Grp_"+ctrlsBnd[1]+"_Off|"+ctrlsBnd[1]), ln="BEND", nn="____________________ BEND", at="enum", en="__________:")
        # cmds.setAttr(("|Grp_"+ctrlsBnd[1]+"|Grp_"+ctrlsBnd[1]+"_Off|"+ctrlsBnd[1]+".BEND"), edit=True, channelBox=True)
        # cmds.addAttr(("|Grp_"+ctrlsBnd[1]+"|Grp_"+ctrlsBnd[1]+"_Off|"+ctrlsBnd[1]), ln="BendFollowPercent", at="double", min=0, max=1, dv=1)
        # cmds.setAttr(("|Grp_"+ctrlsBnd[1]+"|Grp_"+ctrlsBnd[1]+"_Off|"+ctrlsBnd[1]+".BendFollowPercent"), edit=True, k=True)
        # bsSfcFollow = cmds.shadingNode('blendColors', asUtility=True, n=("Bs_"+self.side+"_Thigh_Bend_Sfc_FollowPercent"))
        # bsCtrlFollow = cmds.shadingNode('blendColors', asUtility=True, n=("Bs_"+self.side+"_Thigh_Bend_Ctrl_FollowPercent"))
        # cmds.connectAttr((str(ctrlsBnd[1])+".t"), (bsSfcFollow+".color1"))
        # cmds.setAttr((bsSfcFollow+".color2"), 0, 0, 0)
        # cmds.connectAttr((bsSfcFollow+".output"), ("Grp_"+ctrlsSfc[1]+"_Off.t"))
        # cmds.connectAttr((str(ctrlsBnd[1])+".BendFollowPercent"), (bsSfcFollow+".blender"))
        # cmds.select(str(ctrlsBnd[1]), ("Grp_"+str(ctrlsBnd[0])+"_Off"), r=True)
        # pntConst = cmds.pointConstraint(weight=1, mo=True)
        # cmds.connectAttr((pntConst[0]+".constraintTranslate"), (bsCtrlFollow+".color1"))
        # cmds.setAttr((bsCtrlFollow+".color2"), 0, 0, 0)
        # cmds.connectAttr((bsCtrlFollow+".output"), ("Grp_"+str(ctrlsBnd[0])+"_Off.t"))
        # cmds.disconnectAttr((pntConst[0]+".constraintTranslateX"), ("Grp_"+str(ctrlsBnd[0])+"_Off.tx"))
        # cmds.disconnectAttr((pntConst[0]+".constraintTranslateY"), ("Grp_"+str(ctrlsBnd[0])+"_Off.ty"))
        # cmds.disconnectAttr((pntConst[0]+".constraintTranslateZ"), ("Grp_"+str(ctrlsBnd[0])+"_Off.tz"))
        # cmds.connectAttr((str(ctrlsBnd[1])+".BendFollowPercent"), (bsCtrlFollow+".blender"))
        # bsSfcFollow = cmds.shadingNode('blendColors', asUtility=True, n=("Bs_"+self.side+"_Shin_Bend_Sfc_FollowPercent"))
        # bsCtrlFollow = cmds.shadingNode('blendColors', asUtility=True, n=("Bs_"+self.side+"_Shin_Bend_Ctrl_FollowPercent"))
        # cmds.connectAttr((str(ctrlsBnd[1])+".t"), (bsSfcFollow+".color1"))
        # cmds.setAttr((bsSfcFollow+".color2"), 0, 0, 0)
        # cmds.connectAttr((bsSfcFollow+".output"), ("Grp_"+ctrlsSfc[3]+"_Off.t"))
        # cmds.connectAttr((str(ctrlsBnd[1])+".BendFollowPercent"), (bsSfcFollow+".blender"))
        # cmds.select(str(ctrlsBnd[1]), ("Grp_"+str(ctrlsBnd[2])+"_Off"), r=True)
        # pntConst = cmds.pointConstraint(weight=1, mo=True)
        # cmds.connectAttr((pntConst[0]+".constraintTranslate"), (bsCtrlFollow+".color1"))
        # cmds.setAttr((bsCtrlFollow+".color2"), 0, 0, 0)
        # cmds.connectAttr((bsCtrlFollow+".output"), ("Grp_"+str(ctrlsBnd[2])+"_Off.t"))
        # cmds.disconnectAttr((pntConst[0]+".constraintTranslateX"), ("Grp_"+str(ctrlsBnd[2])+"_Off.tx"))
        # cmds.disconnectAttr((pntConst[0]+".constraintTranslateY"), ("Grp_"+str(ctrlsBnd[2])+"_Off.ty"))
        # cmds.disconnectAttr((pntConst[0]+".constraintTranslateZ"), ("Grp_"+str(ctrlsBnd[2])+"_Off.tz"))
        # cmds.connectAttr((str(ctrlsBnd[1])+".BendFollowPercent"), (bsCtrlFollow+".blender"))
        # '''
        # # Connect controls
        # for x in range(0, (len(ctrlsSfc) - 1)):
        #     if x == 0 or x == (len(ctrlsSfc) - 1): pass
        #     else:
        #         cmds.connectAttr((ctrlsBnd[x-1]+".t"), (ctrlsSfc[x]+".t"))
        #         cmds.connectAttr((ctrlsBnd[x-1]+".r"), (ctrlsSfc[x]+".r"))
        #         cmds.connectAttr((ctrlsBnd[x-1]+".s"), (ctrlsSfc[x]+".s"))
        # for c in ctrlsBnd:
        #     cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings.SecondaryCtrls"), (str(c)+".v"))
        #     ctrl.Control(n=str(c), t="Lock and Hide", s=["v"])
        # # Template joints
        # for c in ctrlsSfc:
        #     cmds.setAttr((c+".template"), True)
        return grpBends, grpCtrls, wireCrvs

    def createSineRibbon(self, sfc="", settingsCtrl=""):
        cmds.select(sfc, r=True)
        nlSine = cmds.nonLinear(typ="sine")
        cmds.setAttr((nlSine[0]+".dropoff"), 1)
        cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings.SineAmplitude"), (nlSine[0]+".amplitude"))
        cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings.SineWavelength"), (nlSine[0]+".wavelength"))
        cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings.SineOffset"), (nlSine[0]+".offset"))
        cmds.connectAttr(("Ctrl_"+self.side+"_Leg_Settings.SineTwist"), (nlSine[1]+".ry"))
        pmaSinePosNormalizer = cmds.shadingNode('plusMinusAverage', asUtility=True, n=("Pma_"+self.side+"_Leg_Sine_PosNormalizer"))
        cmds.connectAttr((settingsCtrl+".SinePos"), (pmaSinePosNormalizer+".input1D[0]"))
        cmds.setAttr(pmaSinePosNormalizer+".input1D[1]", cmds.getAttr(nlSine[1]+".ty"), lock=True)
        cmds.connectAttr((pmaSinePosNormalizer+".output1D"), (nlSine[1]+".ty"))
        pmaSineScaleNormalizer = cmds.shadingNode('plusMinusAverage', asUtility=True, n=("Pma_"+self.side+"_Sine_ScaleNormalizer"))
        cmds.connectAttr((settingsCtrl+".SineScale"), (pmaSineScaleNormalizer+".input1D[0]"))
        cmds.setAttr(pmaSineScaleNormalizer+".input1D[1]", cmds.getAttr(nlSine[1]+".sy"), lock=True)
        cmds.connectAttr((pmaSineScaleNormalizer+".output1D"), (nlSine[1]+".sy"))
        cmds.rename(nlSine[0], ("Nl_Rib_"+self.side+"_Leg_Sine"))
        nlSine = cmds.rename(nlSine[1], ("Nl_Rib_"+self.side+"_Leg_SineHandle"))
        return nlSine

    def createTwistRibbon(self, sfc="", thighRot=[], shinRot=[], settingsCtrl=""):
        cmds.select(sfc, r=True)
        spansU = cmds.getAttr((sfc+".spansU"))
        degreeU = cmds.getAttr((sfc+".degreeU"))
        spansV = cmds.getAttr((sfc+".spansV"))
        degreeV = cmds.getAttr((sfc+".degreeV"))
        formU = cmds.getAttr((sfc+".formU"))
        formV = cmds.getAttr((sfc+".formV"))
        numCvsU = spansU + degreeU
        if formU == 2: numCvsU -= degreeU
        numCvsV = spansV + degreeV
        if formV == 2: numCvsV -= degreeV
        cmds.select((sfc+".cv[0:1]["+str(numCvsV / 2)+":"+str(numCvsV - 1)+"]"), r=True)
        nlThighTwist = cmds.nonLinear(type="twist")
        cmds.rotate(thighRot[0], thighRot[1], thighRot[2], nlThighTwist[1], r=True)
        cmds.select((sfc+".cv[0:1][0:"+str((numCvsV - 1) / 2)+"]"), r=True)
        nlShinTwist = cmds.nonLinear(type="twist")
        cmds.rotate(shinRot[0], shinRot[1], shinRot[2], nlShinTwist[1], r=True)
        pmaThighTwistStartSum = cmds.shadingNode('plusMinusAverage', asUtility=True, n=("Pma_"+self.side+"_Thigh_Twist_StartSum"))
        pmaThighTwistEndSum = cmds.shadingNode('plusMinusAverage', asUtility=True, n=("Pma_"+self.side+"_Thigh_Twist_EndSum"))
        mdlThighReverseStartTwist = cmds.shadingNode('multDoubleLinear', asUtility=True, n=("Mdl_"+self.side+"_Thigh_Twist_ReverseStart"))
        mdlThighReverseEndTwist = cmds.shadingNode('multDoubleLinear', asUtility=True, n=("Mdl_"+self.side+"_Thigh_Twist_ReverseEnd"))
        cmds.connectAttr((settingsCtrl+".KneeTwistMult"), (pmaThighTwistStartSum+".input1D[0]"))
        cmds.connectAttr((settingsCtrl+".Roll"), (pmaThighTwistStartSum+".input1D[1]"))
        cmds.connectAttr((settingsCtrl+".RollOffset"), (pmaThighTwistStartSum+".input1D[2]"))
        cmds.connectAttr((pmaThighTwistStartSum+".output1D"), (mdlThighReverseStartTwist+".input1"))
        cmds.setAttr(mdlThighReverseStartTwist+".input2", -1)
        cmds.connectAttr((mdlThighReverseStartTwist+".output"), (nlThighTwist[0]+".startAngle"))
        cmds.connectAttr((settingsCtrl+".ThighTwistMult"), (pmaThighTwistEndSum+".input1D[0]"))
        cmds.connectAttr((settingsCtrl+".Roll"), (pmaThighTwistEndSum+".input1D[1]"))
        cmds.connectAttr((settingsCtrl+".RollOffset"), (pmaThighTwistEndSum+".input1D[2]"))
        cmds.connectAttr((pmaThighTwistEndSum+".output1D"), (mdlThighReverseEndTwist+".input1"))
        cmds.setAttr(mdlThighReverseEndTwist+".input2", -1)
        cmds.connectAttr((mdlThighReverseEndTwist+".output"), (nlThighTwist[0]+".endAngle"))
        pmaShinTwistStartSum = cmds.shadingNode('plusMinusAverage', asUtility=True, n=("Pma_"+self.side+"_Shin_Twist_StartSum"))
        pmaShinTwistEndSum = cmds.shadingNode('plusMinusAverage', asUtility=True, n=("Pma_"+self.side+"_Shin_Twist_EndSum"))
        mdlShinReverseStartTwist = cmds.shadingNode('multDoubleLinear', asUtility=True, n=("Mdl_"+self.side+"_Shin_Twist_ReverseStart"))
        mdlShinReverseEndTwist = cmds.shadingNode('multDoubleLinear', asUtility=True, n=("Mdl_"+self.side+"_Shin_Twist_ReverseEnd"))
        cmds.connectAttr((settingsCtrl+".ShinTwistMult"), (pmaShinTwistStartSum+".input1D[0]"))
        cmds.connectAttr((settingsCtrl+".Roll"), (pmaShinTwistStartSum+".input1D[1]"))
        cmds.connectAttr((settingsCtrl+".RollOffset"), (pmaShinTwistStartSum+".input1D[2]"))
        cmds.connectAttr((pmaShinTwistStartSum+".output1D"), (mdlShinReverseStartTwist+".input1"))
        cmds.setAttr(mdlShinReverseStartTwist+".input2", -1)
        cmds.connectAttr((mdlShinReverseStartTwist+".output"), (nlShinTwist[0]+".startAngle"))
        cmds.connectAttr((settingsCtrl+".KneeTwistMult"), (pmaShinTwistEndSum+".input1D[0]"))
        cmds.connectAttr((settingsCtrl+".Roll"), (pmaShinTwistEndSum+".input1D[1]"))
        cmds.connectAttr((settingsCtrl+".RollOffset"), (pmaShinTwistEndSum+".input1D[2]"))
        cmds.connectAttr((pmaShinTwistEndSum+".output1D"), (mdlShinReverseEndTwist+".input1"))
        cmds.setAttr(mdlShinReverseEndTwist+".input2", -1)
        cmds.connectAttr((mdlShinReverseEndTwist+".output"), (nlShinTwist[0]+".endAngle"))
        cmds.rename(nlThighTwist[0], ("Def_"+self.side+"_Thigh_Twist"))
        cmds.rename(nlShinTwist[0], ("Def_"+self.side+"_Shin_Twist"))
        nlThighTwist = cmds.rename(nlThighTwist[1], ("Def_"+self.side+"_Thigh_TwistHandle"))
        nlShinTwist = cmds.rename(nlShinTwist[1], ("Def_"+self.side+"_Shin_TwistHandle"))
        nlTwist = []
        nlTwist.append(nlThighTwist); nlTwist.append(nlShinTwist)
        return nlTwist

    def createSquashRibbon(self, sfc="", settingsCtrl="", ctrlJntsGrp=[]):
        cmds.select(sfc, r=True)
        if cmds.objExists("hairSystem1"): cmds.select("hairSystem1", r=True); cmds.Delete()
        if cmds.objExists("hairSystem1OutputCurves"): cmds.select("hairSystem1OutputCurves", r=True); cmds.Delete()
        if cmds.objExists("hairSystem1Follicles"): cmds.select("hairSystem1Follicles", r=True); cmds.Delete()
        if cmds.objExists("nucleus1"): cmds.select("nucleus1", r=True); cmds.Delete()
        cmds.select(sfc, r=True)
        nlSquash = cmds.nonLinear(type='squash')
        cmds.select(sfc, r=True)
        mel.eval("createHair 1 {0} 10 0 0 0 0 5 0 2 2 1;".format(self.numberOfJntsRib))
        cmds.select("hairSystem1", "hairSystem1OutputCurves", "nucleus1", r=True)
        cmds.Delete()
        fol = cmds.listRelatives('hairSystem1Follicles', c=True)
        newFol = []
        jnts = []
        for x in range(0, len(fol)):
            grp = cmds.listRelatives(fol[x], c=True)
            cmds.setAttr(fol[x]+".parameterU", 1)
            cmds.select(grp[1], r=True)
            cmds.Delete()
            mdlSquashMult = cmds.shadingNode('multDoubleLinear', asUtility=True, n=("Mdl_SquashMult_"+self.side+"_Leg_Rib_"+str(len(fol) - x)))
            pmaSquashMult = cmds.shadingNode('plusMinusAverage', asUtility=True, n=("Pma_SquashMult_Sum_"+self.side+"_Leg_Rib_"+str(len(fol) - x)))
            cmds.connectAttr((settingsCtrl+".SquashMult"), (mdlSquashMult+".input1"))
            cmds.connectAttr((fol[x]+".tx"), (mdlSquashMult+".input2")) # TranslateX do fol tem que ser igual a 0
            cmds.setAttr(pmaSquashMult+".input1D[0]", 1)
            cmds.connectAttr((mdlSquashMult+".output"), (pmaSquashMult+".input1D[1]"))
            cmds.connectAttr((pmaSquashMult+".output1D"), (ctrlJntsGrp[x]+".sx"))
            cmds.connectAttr((pmaSquashMult+".output1D"), (ctrlJntsGrp[x]+".sz"))
            newFol.append(cmds.rename(fol[x], ("Fol_Squash_"+self.side+"_"+str(len(fol) - x))))
        cmds.move(-(cmds.getAttr(newFol[0]+".tx")), 0, 0, sfc, r=True)
        cmds.select(nlSquash[1], r=True)
        cmds.move(cmds.getAttr(sfc+".tx"), 0, 0, r=True)
        mdlReverseVolume = cmds.shadingNode('multDoubleLinear', asUtility=True, n=("Mdl_Reverse_Squash_"+self.side))
        cmds.connectAttr((settingsCtrl+".Squash"), (mdlReverseVolume+".input1"))
        cmds.setAttr(mdlReverseVolume+".input2", -1)
        cmds.connectAttr((mdlReverseVolume+".output"), (nlSquash[0]+".factor"))
        pmaSquashScaleNormalizer = cmds.shadingNode('plusMinusAverage', asUtility=True, n=("Pma_SquashScale_Normalizer_"+self.side))
        cmds.connectAttr((settingsCtrl+".SquashScale"), (pmaSquashScaleNormalizer+".input1D[0]"))
        cmds.setAttr(pmaSquashScaleNormalizer+".input1D[1]", cmds.getAttr(nlSquash[1]+".sy"), lock=True)
        cmds.connectAttr((pmaSquashScaleNormalizer+".output1D"), (nlSquash[1]+".sy"))
        pmaSquashPosNormalizer = cmds.shadingNode('plusMinusAverage', asUtility=True, n=("Pma_SquashPos_Normalizer_"+self.side))
        cmds.connectAttr((settingsCtrl+".SquashPos"), (pmaSquashPosNormalizer+".input1D[0]"))
        cmds.setAttr(pmaSquashPosNormalizer+".input1D[1]", cmds.getAttr(nlSquash[1]+".ty"), lock=True)
        cmds.connectAttr((pmaSquashPosNormalizer+".output1D"), (nlSquash[1]+".ty"))
        cmds.connectAttr((settingsCtrl+".SquashStartDropoff"), (nlSquash[0]+".startSmoothness"))
        cmds.connectAttr((settingsCtrl+".SquashEndDropoff"), (nlSquash[0]+".endSmoothness"))
        grpFolSquash = cmds.rename("hairSystem1Follicles", ("Grp_Fol_Squash_"+self.side+"_Leg"))
        cmds.rename(nlSquash[0], ("Def_"+self.side+"_Leg_Squash"))
        nlSquash = cmds.rename(nlSquash[1], ("Def_"+self.side+"_Leg_SquashHandle"))
        return nlSquash, grpFolSquash

    def createSpaceSwitch(self):
        pass

    def convertCVtoCurve(self):
        curveCmd = "cmds.curve(d=3, p=["
        vertices = cmds.ls(sl=True, fl=True)
        positions = []
        for vtx in vertices:
            pos = cmds.pointPosition(vtx, w=True)
            positions.append(("("+str(pos[0])+", "+str(pos[1])+", "+str(pos[2])+")"))
        for x in range(0, len(positions)):
            curveCmd += positions[x]
            if x < (len(positions) - 1): curveCmd += ", "
            else: curveCmd += "], k=["
        numPnts = len(vertices)
        numDegrees = 3
        lastKnot = numPnts - 3
        numKnots = numPnts + numDegrees - 1
        knots = [0, 0, 0]
        for x in range(1, (lastKnot + 1)):
            knots.append(x)
            if x >= lastKnot: knots.append(x); knots.append(x)
        for x in range(0, len(knots)):
            curveCmd += str(knots[x])
            if x < (len(knots) - 1): curveCmd += ", "
            else: curveCmd += "], n='gfAutoRig_TEMPCRV')"
        exec(curveCmd)
        crvShape = cmds.listRelatives(c=True)
        cmds.rename(crvShape[0], 'gfAutoRig_TEMPCRV_SHAPE')
        return 'gfAutoRig_TEMPCRV', 'gfAutoRig_TEMPCRV_SHAPE'
