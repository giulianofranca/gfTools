import math
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om


from gfTools.__OLD.gfTools.gfAutoRig.settings import log
from gfTools.__OLD.gfTools.gfAutoRig.settings import controls as ctrl
reload(log); reload(ctrl)


class buildHumanArm(object):

    def __init__(self, name="", side=""):
        # side, IKFK, AutoPv, StretchFK, StretchIK, Reverse, Ribbon, SpaceSwitch, method, numLegs=2, NumJnts=0
        # self.side = side
        # self.NumLegs = numLegs
        # self.NumJnts = NumJnts
        # self.IKFKSwitch = IKFK
        # self.AutoPv = AutoPv
        # self.StretchFK = StretchFK
        # self.StretchIK = StretchIK
        # self.ReverseFoot = Reverse
        # self.Ribbon = Ribbon
        # self.SpaceSwitch = SpaceSwitch
        # self.method = method
        # self.Features = []
        # self.Features = [IKFK, AutoPv, StretchFK, StretchIK, Reverse, Ribbon, SpaceSwitch]
        # self.build()
        self.name = name
        self.side = side
        self.jntsBnd = []
        self.jntsDrv = []
        self.jntsRib = []
        log.buildLogHumanArm(msg="startBuildHumanArm", btn=self.name, stop=False)
        log.buildLog(msg="whiteLine", stop=False)
        if self.side == "left": self.side = "L"
        elif self.side == "right": self.side = "R"
        else: cmds.error(("Arm ("+name+") side don't recognized"))
        # --------------------------------------------------------------------------------------------------------------
        # READ FEATURES
        log.buildLogHumanArm(msg="readFeatures", btn="Start", stop=False)
        self.haveMultArms = cmds.radioButtonGrp("radMultArmsHArms", q=True, sl=True)
        self.haveStretchFK = cmds.checkBoxGrp("cbxStretchFKHArms", q=True, v1=True)
        self.haveSquashFK = cmds.checkBoxGrp("cbxSquashFKHArms", q=True, v1=True)
        self.haveIK = cmds.optionMenuGrp("optEnIKHArms", q=True, v=True)
        self.haveAutoPv = cmds.checkBoxGrp("cbxAutoManuPvHArms", q=True, v1=True)
        self.haveStretchIK = cmds.checkBoxGrp("cbxStretchIKHArms", q=True, v1=True)
        self.haveStretchMultIK = cmds.checkBoxGrp("cbxStretckIKMultHArms", q=True, v1=True)
        self.haveClampStretchIK = cmds.checkBoxGrp("cbxClampStretchHArms", q=True, v1=True)
        self.haveSquashIK = cmds.checkBoxGrp("cbxHArmSquashIK", q=True, v1=True)
        self.haveSquashMultIK = cmds.checkBoxGrp("cbxSquashIKMultHArms", q=True, v1=True)
        self.haveElbowLockIK = cmds.checkBoxGrp("cbxElbowLockHArms", q=True, v1=True)
        self.haveReverseHand = cmds.checkBoxGrp("cbxReverseHandHArms", q=True, v1=True)
        self.haveRibbon = cmds.optionMenuGrp("optEnRibbonHArms", q=True, v=True)
        self.haveClavicleType = cmds.radioButtonGrp("radClavicleTypeHArms", q=True, sl=True) # 1 = IK/FK | 2 = FK Only | 3 = IK Only
        self.haveBendCtrlsRib = cmds.checkBoxGrp("cbxBendCtrlsHArms", q=True, v1=True)
        self.haveTweakCtrlsRib = cmds.checkBoxGrp("cbxTweakCtrlsHArms", q=True, v1=True)
        self.haveTwistAttrsRib = cmds.checkBoxGrp("cbxTwistAttrsHArms", q=True, v1=True)
        self.haveSineAttrsRib = cmds.checkBoxGrp("cbxSineAttrsHArms", q=True, v1=True)
        self.haveSquashAttrsRib = cmds.checkBoxGrp("cbxSquashAttrsHArms", q=True, v1=True)
        self.haveSpaceSwitch = cmds.optionMenuGrp("optEnSpaceSwitchHArms", q=True, v=True)
        log.buildLogHumanArm(msg="readFeatures", btn="All", stop=False)
        self.gblScaleGuide = cmds.xform("gfARGuides:Ctrl_Global", q=True, r=True, s=True)
        self.gblScale = cmds.checkBoxGrp("cbxGlobalScaleMFeat", q=True, v1=True)
        self.setupFull = cmds.radioButtonGrp("radCompSetupMFeat", q=True, sl=True)
        self.switchType = cmds.radioButtonGrp("radIKFKTypHArms", q=True, sl=True)
        log.buildLog(msg="whiteLine", stop=False)
        # FIND GUIDES TRANSFORMATIONS
        log.buildLogHumanArm(msg="foundGuidesTrans", btn="Start", stop=False)
        if self.haveMultArms == 1:
            if cmds.objExists(("gfARGuides:Ctrl_"+self.side+"_UpperArm")):
                self.posUpperArm = cmds.xform(("gfARGuides:Ctrl_"+self.side+"_UpperArm"), q=True, ws=True, rp=True)
                log.buildLogHumanArm(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.side+"_UpperArm"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.side+"_Forearm")):
                self.posForeArm = cmds.xform(("gfARGuides:Ctrl_"+self.side+"_Forearm"), q=True, ws=True, rp=True)
                log.buildLogHumanArm(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.side+"_Forearm"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.side+"_Wrist")):
                self.posWrist = cmds.xform(("gfARGuides:Ctrl_"+self.side+"_Wrist"), q=True, ws=True, rp=True)
                log.buildLogHumanArm(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.side+"_Wrist"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.side+"_Palm")):
                self.posPalm = cmds.xform(("gfARGuides:Ctrl_"+self.side+"_Palm"), q=True, ws=True, rp=True)
                log.buildLogHumanArm(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.side+"_Palm"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.side+"_ArmEnd")):
                self.posArmEnd = cmds.xform(("gfARGuides:Ctrl_"+self.side+"_ArmEnd"), q=True, ws=True, rp=True)
                log.buildLogHumanArm(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.side+"_ArmEnd"), stop=False)
            else: cmds.error("!!")
        elif self.haveMultArms == 2:
            if cmds.objExists(("gfARGuides:Ctrl_"+self.name+"_UpperArm")):
                self.posUpperArm = cmds.xform(("gfARGuides:Ctrl_"+self.name+"_UpperArm"), q=True, ws=True, rp=True)
                log.buildLogHumanArm(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.name+"_UpperArm"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.name+"_Forearm")):
                self.posForeArm = cmds.xform(("gfARGuides:Ctrl_"+self.name+"_Forearm"), q=True, ws=True, rp=True)
                log.buildLogHumanArm(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.name+"_Forearm"), stop=False)
            else: cmds.error("!!")
            if cmds.objExists(("gfARGuides:Ctrl_"+self.name+"_Wrist")):
                self.posWrist = cmds.xform(("gfARGuides:Ctrl_"+self.name+"_Wrist"), q=True, ws=True, rp=True)
                log.buildLogHumanArm(msg="foundGuidesTrans", btn=("gfARGuides:Ctrl_"+self.name+"_Wrist"), stop=False)
            else: cmds.error("!!")
        log.buildLogHumanArm(msg="foundGuidesTrans", btn="All", stop=False)
        log.buildLog(msg="whiteLine", stop=False)

        self.build()


    def getInfo(self):
        armInfo = [self.name, self.side]
        return self.jntsBnd, self.jntsDrv, self.jntsRib, armInfo

    def build(self):
        cmds.select(cl=True)
        # If method == Maya Nodes
        # Setting Joints Variables
        log.buildLogHumanLeg(msg="settingJntsVariables", stop=False)
        jntsArm = []
        jntsClavicle = []
        if self.haveMultArms == 1:
            if self.haveRibbon == "Enabled":
                upperArmRes = ("JntDrv_"+self.side+"_UpperArm"); foreArmRes = ("JntDrv_"+self.side+"_Forearm")
                wristRes = ("JntBnd_"+self.side+"_Wrist"); palmRes = ("JntBnd_"+self.side+"_Palm")
                handEndRes = ("JntBnd_"+self.side+"_HandEnd")
                jntsArm.append(upperArmRes); jntsArm.append(foreArmRes); jntsArm.append(wristRes); jntsArm.append(palmRes); jntsArm.append(handEndRes)
            elif self.haveRibbon == "Disabled":
                upperArmRes = ("JntBnd_"+self.side+"_UpperArm"); foreArmRes = ("JntBnd_"+self.side+"_Forearm")
                wristRes = ("JntBnd_"+self.side+"_Wrist"); palmRes = ("JntBnd_"+self.side+"_Palm")
                handEndRes = ("JntBnd_"+self.side+"_HandEnd")
                jntsArm.append(upperArmRes); jntsArm.append(foreArmRes); jntsArm.append(wristRes); jntsArm.append(palmRes); jntsArm.append(handEndRes)
            if self.haveIK == "Enabled":
                upperArmFK = ("JntDrv_"+self.side+"_FK_UpperArm"); foreArmFK = ("JntDrv_"+self.side+"_FK_Forearm")
                wristFK = ("JntDrv_"+self.side+"_FK_Wrist"); palmFK = ("JntDrv_"+self.side+"_FK_Palm")
                handEndFK = ("JntDrv_"+self.side+"_FK_HandEnd"); upperArmIK = ("JntDrv_"+self.side+"_IK_UpperArm")
                foreArmIK = ("JntDrv_"+self.side+"_IK_Forearm"); wristIK = ("JntDrv_"+self.side+"_IK_Wrist")
                palmIK = ("JntDrv_"+self.side+"_IK_Palm"); handEndIK = ("JntDrv_"+self.side+"_IK_HandEnd")
                jntsArm.append(upperArmFK); jntsArm.append(foreArmFK); jntsArm.append(wristFK); jntsArm.append(palmFK); jntsArm.append(handEndFK)
                jntsArm.append(upperArmIK); jntsArm.append(foreArmIK); jntsArm.append(wristIK); jntsArm.append(palmIK); jntsArm.append(handEndIK)
            if self.haveAutoPv == True:
                upperArmPv = ("JntDrv_"+self.side+"_Pv_UpperArm"); foreArmPv = ("JntDrv_"+self.side+"_Pv_Forearm")
                wristPv = ("JntDrv_"+self.side+"_Pv_Wrist"); upperArmNoFlip = ("JntDrv_"+self.side+"_NoFlip_UpperArm")
                foreArmNoFlip = ("JntDrv_"+self.side+"_NoFlip_Forearm"); wristNoFlip = ("JntDrv_"+self.side+"_NoFlip_Wrist")
                jntsArm.append(upperArmPv); jntsArm.append(foreArmPv); jntsArm.append(wristPv)
                jntsArm.append(upperArmNoFlip); jntsArm.append(foreArmNoFlip); jntsArm.append(wristNoFlip)
        elif self.haveMultArms == 2:
            if self.haveRibbon == "Enabled":
                upperArmRes = ("JntDrv_"+self.name+"_UpperArm"); foreArmRes = ("JntDrv_"+self.name+"_Forearm")
                wristRes = ("JntDrv_"+self.name+"_Wrist"); palmRes = ("JntDrv_"+self.name+"_Palm")
                handEndRes = ("JntDrv_"+self.name+"_HandEnd")
                jntsArm.append(upperArmRes); jntsArm.append(foreArmRes); jntsArm.append(wristRes); jntsArm.append(palmRes); jntsArm.append(handEndRes)
            elif self.haveRibbon == "Disabled":
                upperArmRes = ("JntBnd_"+self.name+"_UpperArm"); foreArmRes = ("JntBnd_"+self.name+"_Forearm")
                wristRes = ("JntBnd_"+self.name+"_Wrist"); palmRes = ("JntBnd_"+self.name+"_Palm")
                handEndRes = ("JntBnd_"+self.name+"_HandEnd")
                jntsArm.append(upperArmRes); jntsArm.append(foreArmRes); jntsArm.append(wristRes); jntsArm.append(palmRes); jntsArm.append(handEndRes)
            if self.haveIK == "Enabled":
                upperArmFK = ("JntDrv_"+self.name+"_FK_UpperArm"); foreArmFK = ("JntDrv_"+self.name+"_FK_Forearm")
                wristFK = ("JntDrv_"+self.name+"_FK_Wrist"); palmFK = ("JntDrv_"+self.name+"_FK_Palm")
                handEndFK = ("JntDrv_"+self.name+"_FK_HandEnd"); upperArmIK = ("JntDrv_"+self.name+"_IK_UpperArm")
                foreArmIK = ("JntDrv_"+self.name+"_IK_Forearm"); wristIK = ("JntDrv_"+self.name+"_IK_Wrist")
                palmIK = ("JntDrv_"+self.name+"_IK_Palm"); handEndIK = ("JntDrv_"+self.name+"_IK_HandEnd")
                jntsArm.append(upperArmFK); jntsArm.append(foreArmFK); jntsArm.append(wristFK); jntsArm.append(palmFK); jntsArm.append(handEndFK)
                jntsArm.append(upperArmIK); jntsArm.append(foreArmIK); jntsArm.append(wristIK); jntsArm.append(palmIK); jntsArm.append(handEndIK)
            if self.haveAutoPv == True:
                upperArmPv = ("JntDrv_"+self.name+"_Pv_UpperArm"); foreArmPv = ("JntDrv_"+self.name+"_Pv_Forearm")
                wristPv = ("JntDrv_"+self.name+"_Pv_Wrist"); upperArmNoFlip = ("JntDrv_"+self.name+"_NoFlip_UpperArm")
                foreArmNoFlip = ("JntDrv_"+self.name+"_NoFlip_ForeArm"); wristNoFlip = ("JntDrv_"+self.name+"_NoFlip_Wrist")
                jntsArm.append(upperArmPv); jntsArm.append(foreArmPv); jntsArm.append(wristPv)
                jntsArm.append(upperArmNoFlip); jntsArm.append(foreArmNoFlip); jntsArm.append(wristNoFlip)
        log.buildLog(msg="whiteLine", stop=False)


        # Create Joints

        self.createJoints(jntsArm)
        # self.createJoints(jntsFingers)
        for jnt in jntsArm:
            print jnt
        chains = self.connectJntChains(jntsArm)
        self.orientJnts(chains)
        self.setRotOrderJnts(chains)


        # Create Controls

        # if self.side == "L": ctrlColor = "Red"; bendColor = "LightRed"; tweakColor = "DarkRed"
        # elif self.side == "R": ctrlColor = "Blue"; bendColor = "LightBlue"; tweakColor = "DarkBlue"
        ctrlColor = 'Primary'; bendColor = 'Secondary'; tweakColor = 'Tertiary'
        if self.haveMultArms == 1:
            ctrlNames = [("Ctrl_"+self.side+"_FK_UpperArm"), ("Ctrl_"+self.side+"_FK_Forearm"),
                ("Ctrl_"+self.side+"_FK_Wrist")]
        elif self.haveMultArms == 2:
            ctrlNames = [("Ctrl_"+self.name+"_FK_UpperArm"), ("Ctrl_"+self.name+"_FK_Forearm"),
                ("Ctrl_"+self.name+"_FK_Wrist")]
        ctrlSizes = [0.8 * self.gblScaleGuide[0], 0.8 * self.gblScaleGuide[0], 0.7 * self.gblScaleGuide[0]]
        if self.haveIK == "Disabled":
            cmds.select(chains[0][0], r=True)
            grpResJnts = cmds.group(n=("Grp_Jnt_"+self.side+"_Arm_ResultConst"))
            cmds.move(self.posUpperArm[0], self.posUpperArm[1], self.posUpperArm[2], (grpResJnts+".rp"), (grpResJnts+".sp"), rpr=True)
        elif self.haveIK == "Enabled":
            cmds.select(chains[0][0], r=True)
            grpResJnts = cmds.group(n=("Grp_Jnt_"+self.side+"_Arm_ResultConst"))
            cmds.move(self.posUpperArm[0], self.posUpperArm[1], self.posUpperArm[2], (grpResJnts+".rp"), (grpResJnts+".sp"), rpr=True)
            cmds.select(chains[1][0], r=True)
            grpFKArm = cmds.group(n=("Grp_"+chains[1][0][0:6]+"_"+self.side+"_FK_Arm"))
            cmds.move(self.posUpperArm[0], self.posUpperArm[1], self.posUpperArm[2], (grpFKArm+".rotatePivot"), (grpFKArm+".scalePivot"), rpr=True)

        fkControls, grpSettingsCtrls = self.createCtrlsFK(names=ctrlNames, sizes=ctrlSizes, color=[ctrlColor, tweakColor], jnts=chains[0])
        self.adjustCtrlsFK(side=self.side)
        self.manageAttrCtrlsFK()
        grpFKCtrlsConst, grpFKCtrls = self.setHierarchyCtrlsFK()
        self.setRotOrderFK(ctrls=ctrlNames)
        if self.haveIK == "Enabled":
            ctrlsIK, grpIKCtrls = self.createCtrlsIK(color=ctrlColor, jnts=chains)
            pvLoc, pvCtrl, grpPVCtrls, dispLine = self.createPoleVector(jnts=chains[0], color=bendColor)
            self.manageAttrCtrlsIK()
        #     self.setRotOrderIK(("Ctrl_"+self.side+"_IK_Leg"))


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


    def createJoints(self, jnts=[]):
        log.buildLogHumanLeg(msg="createJnts", btn="Start", stop=False)
        x = 0
        y = 0
        pos = [(self.posUpperArm[0], self.posUpperArm[1], self.posUpperArm[2]),
            (self.posForeArm[0], self.posForeArm[1], self.posForeArm[2]),
            (self.posWrist[0], self.posWrist[1], self.posWrist[2]),
            (self.posPalm[0], self.posPalm[1], self.posPalm[2]),
            (self.posArmEnd[0], self.posArmEnd[1], self.posArmEnd[2])]
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

    def createJointsClavicle(self, jnts=[]):
        pos = [(self.posNeck[0], self.posNeck[1], self.posNeck[2]),
            (self.posHead[0], self.posHead[1], self.posHead[2])]
        if self.solverType == 1:
            distNeckHead = [(self.posHead[0] - self.posNeck[0]), (self.posHead[1] - self.posNeck[1]), (self.posHead[2] - self.posNeck[2])]
            percentDist = (100.0 / (self.numberOfIKJnts - 1)) / 100.0
            distJntToJnt = [(distNeckHead[0] * percentDist), (distNeckHead[1] * percentDist), (distNeckHead[2] * percentDist)]
            for x in range(0, self.numberOfIKJnts):
                if x == 0: posIK = [(self.posNeck[0]), (self.posNeck[1]), (self.posNeck[2])]
                else: posIK = [((distJntToJnt[0] * x) + self.posNeck[0]), ((distJntToJnt[1] * x) + self.posNeck[1]), ((distJntToJnt[2] * x) + self.posNeck[2])]
                pos.append(posIK)
        x = 0
        for j in jnts:
            cmds.select(cl=True)
            jnt = cmds.joint(p=(pos[x][0], pos[x][1], pos[x][2]))
            cmds.rename(jnt, j)
            # print ("Jnt #"+str(x)+" | Pos = %s") %(pos[x])
            x += 1

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
            cmds.joint(edit=True, oj="xyz", sao="ydown", ch=True, zso=True)
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
            c = ctrl.Control(n=("Ctrl_"+self.side+"_Arm_Settings"), t="Box", s=(0.1 * self.gblScaleGuide[0]), c=color[1])
            ctrls.append(str(c))
            grp = cmds.group(n=("Grp_Ctrl_"+self.side+"_Arm_Settings"))
            cmds.move(0, 0, 0, (grp+".rotatePivot"), (grp+".scalePivot"))
            cmds.select(loc[0], grp, r=True)
            const = cmds.parentConstraint(weight=1)
            cmds.select(const, r=True)
            cmds.Delete()
            cmds.setAttr((grp+".rz"), 90)
            pos = 15 * self.gblScaleGuide[0]
            cmds.setAttr((grp+".tz"), pos * (-1))
            cmds.select(loc[0], grp, r=True)
            cmds.parentConstraint(weight=1, mo=True)
            cmds.setAttr((loc[0]+".v"), False)
            cmds.rename(loc, ("Loc_Ctrl_"+self.side+"_Arm_Settings"))
        return ctrls, grp

    def adjustCtrlsFK(self, side=""):
        if side == "L":
            # UpperArm
            cmds.select("Ctrl_L_FK_UpperArm.cv[0:7]", r=True)
            cmds.rotate(0, 0, 90, r=True, os=True)
            # Forearm
            cmds.select("Ctrl_L_FK_Forearm.cv[0:7]", r=True)
            cmds.rotate(0, 0, 90, r=True, os=True)
            # Wrist
            cmds.select("Ctrl_L_FK_Wrist.cv[0:7]", r=True)
            cmds.rotate(0, 0, 90, r=True, os=True)
        elif side == "R":
            # UpperArm
            cmds.select("Ctrl_R_FK_UpperArm.cv[0:7]", r=True)
            cmds.rotate(0, 0, -90, r=True, os=True)
            # Forearm
            cmds.select("Ctrl_R_FK_Forearm.cv[0:7]", r=True)
            cmds.rotate(0, 0, -90, r=True, os=True)
            # Wrist
            cmds.select("Ctrl_R_FK_Wrist.cv[0:7]", r=True)
            cmds.rotate(0, 0, -90, r=True, os=True)

    def manageAttrCtrlsFK(self):
        if self.haveMultArms == 1:
            ctrl.Control(n=("Ctrl_"+self.side+"_FK_UpperArm"), t="Lock and Hide", s=["tx", "ty", "tz", "sx", "sy", "sz"])
            ctrl.Control(n=("Ctrl_"+self.side+"_FK_Forearm"), t="Lock and Hide", s=["tx", "ty", "tz", "sx", "sy", "sz"])
            ctrl.Control(n=("Ctrl_"+self.side+"_FK_Wrist"), t="Lock and Hide", s=["tx", "ty", "tz", "sx", "sy", "sz"])
            if self.haveSpaceSwitch == "Enabled" or self.haveStretchFK == True or self.haveSquashFK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_FK_UpperArm|Ctrl_"+self.side+"_FK_UpperArm"), ln="ARM", nn="_____________________ ARM", at="enum", en="__________:")
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_FK_UpperArm|Ctrl_"+self.side+"_FK_UpperArm.ARM"), e=True, channelBox=True)
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_FK_Forearm|Ctrl_"+self.side+"_FK_Forearm"), ln="ARM", nn="_____________________ ARM", at="enum", en="__________:")
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_FK_Forearm|Ctrl_"+self.side+"_FK_Forearm.ARM"), e=True, channelBox=True)
            if self.haveStretchFK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_FK_UpperArm|Ctrl_"+self.side+"_FK_UpperArm"), ln="UpperArmStretch", at="double", min=0.01, dv=1, k=True)
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_FK_Forearm|Ctrl_"+self.side+"_FK_Forearm"), ln="ForearmStretch", at="double", min=0.01, dv=1, k=True)
            if self.haveSquashFK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_FK_UpperArm|Ctrl_"+self.side+"_FK_UpperArm"), ln="UpperArmSquash", at="double", min=0.01, dv=1, k=True)
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_FK_Forearm|Ctrl_"+self.side+"_FK_Forearm"), ln="ForearmSquash", at="double", min=0.01, dv=1, k=True)
            if self.haveSpaceSwitch == "Enabled":
                rawSpaces = cmds.textScrollList("lstArmsSpaceListHArms", q=True, ai=True)
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
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_FK_UpperArm|Ctrl_"+self.side+"_FK_UpperArm"), ln="Follow", at="enum", en=enum, k=True)
            # Settings ctrl
            if self.haveIK == "Enabled" or self.haveBendCtrlsRib == True or self.haveTweakCtrlsRib == True or self.haveSineAttrsRib == True or self.haveTwistAttrsRib == True:
                ctrl.Control(n=("Ctrl_"+self.side+"_Arm_Settings"), t="Lock and Hide", s=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])
                switchAttrs = 0
                if self.haveIK == "Enabled": switchAttrs += 1
                if self.haveAutoPv == True: switchAttrs += 1
                if self.haveBendCtrlsRib == True: switchAttrs += 1
                if self.haveTweakCtrlsRib == True: switchAttrs += 1
                if self.haveIK == "Enabled" or self.haveBendCtrlsRib == True or self.haveTweakCtrlsRib == True:
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SETTINGS", nn="________________ SETTINGS", at="enum", en="__________:")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SwitchSettings", at="compound", nc=switchAttrs)
                if self.haveIK == "Enabled":
                    if self.switchType == 1:
                        cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                            ln="IKFKSwitch", nn="IK/FK Switch", at="enum", en="FK:IK:", p="SwitchSettings", k=True)
                    elif self.switchType == 2:
                        cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                            ln="IKFKSwitch", nn="IK/FK Switch", at="double", min=0, max=1, dv=0, p="SwitchSettings", k=True)
                if self.haveAutoPv == True:
                    if self.switchType == 1:
                        cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                            ln="AutoManualSwitch", nn="Auto/Manual Switch", at="enum", en="Manual:Auto:", p="SwitchSettings", k=True)
                    elif self.switchType == 2:
                        cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                            ln="AutoManualSwitch", nn="Auto/Manual Switch", at="double", min=0, max=1, dv=0, p="SwitchSettings", k=True)
                if self.haveBendCtrlsRib == True:
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SecondaryCtrls", at="bool", p="SwitchSettings", k=True)
                if self.haveTweakCtrlsRib == True:
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="TertiaryCtrls", at="bool", p="SwitchSettings", k=True)
                if self.haveSineAttrsRib == True:
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SINE", nn="____________________ SINE", at="enum", en="__________:")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SineAttrs", at="compound", nc=6)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SineAmplitude", at="double", min=-5, max=5, dv=0, p="SineAttrs", k=True)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SineWavelength", at="double", min=0.1, max=10, dv=2, p="SineAttrs", k=True)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SineOffset", at="double", min=-10, max=10, dv=0, p="SineAttrs", k=True)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SineTwist", at="double", min=-360, max=360, dv=0, p="SineAttrs", k=True)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SinePos", at="double", min=-360, max=360, dv=0, p="SineAttrs", k=True)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SineScale", at="double", min=-360, max=360, dv=0, p="SineAttrs", k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings.SINE"),
                        edit=True, channelBox=True)
                if self.haveTwistAttrsRib == True:
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="TWIST", nn="___________________ TWIST", at="enum", en="__________:")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="TwistAttrs", at="compound", nc=5)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="UpperArmTwistMult", at="double", min=-859, max=859, dv=0, p="TwistAttrs", k=True)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="ElbowTwistMult", at="double", min=-859, max=859, dv=0, p="TwistAttrs", k=True)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="ForearmTwistMult", at="double", min=-859, max=859, dv=0, p="TwistAttrs", k=True)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="Roll", at="double", min=-859, max=859, dv=0, p="TwistAttrs", k=True)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="RollOffset", at="double", min=-859, max=859, dv=0, p="TwistAttrs", k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings.TWIST"),
                        edit=True, channelBox=True)
                if self.haveSquashAttrsRib == True:
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SQUASH", nn="__________________ SQUASH", at="enum", en="__________:")
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SquashAttrs", at="compound", nc=6)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="Squash", at="double", dv=0, p="SquashAttrs", k=True)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SquashMult", at="double", min=-1, max=1, dv=0.3, p="SquashAttrs", k=True)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SquashScale", at="double", dv=0, p="SquashAttrs", k=True)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SquashPos", at="double", dv=0, p="SquashAttrs", k=True)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SquashStartDropoff", at="double", min=0, max=1, dv=0, p="SquashAttrs", k=True)
                    cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings"),
                        ln="SquashEndDropoff", at="double", min=0, max=1, dv=0, p="SquashAttrs", k=True)
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings.SQUASH"),
                        edit=True, channelBox=True)
                if self.haveIK == "Enabled" or self.haveBendCtrlsRib == True or self.haveTweakCtrlsRib == True:
                    cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Arm_Settings|Ctrl_"+self.side+"_Arm_Settings.SETTINGS"),
                        edit=True, channelBox=True)
        elif self.haveMultArms == 2: pass

    def setHierarchyCtrlsFK(self):
        cmds.parent(("Grp_Ctrl_"+self.side+"_FK_Wrist"), ("Ctrl_"+self.side+"_FK_Forearm"))
        cmds.parent(("Grp_Ctrl_"+self.side+"_FK_Forearm"), ("Ctrl_"+self.side+"_FK_UpperArm"))
        cmds.select(("Grp_Ctrl_"+self.side+"_FK_UpperArm"))
        grpFKCtrlsConst = cmds.group(n=("Grp_Ctrl_"+self.side+"_Arm_FKConst"))
        cmds.move(self.posUpperArm[0], self.posUpperArm[1], self.posUpperArm[2], (grpFKCtrlsConst+".rotatePivot"), (grpFKCtrlsConst+".scalePivot"), rpr=True)
        cmds.select(grpFKCtrlsConst)
        grpFKCtrls = cmds.group(n=("Grp_Ctrl_"+self.side+"_FK_Arm"))
        cmds.move(self.posUpperArm[0], self.posUpperArm[1], self.posUpperArm[2], (grpFKCtrls+".rotatePivot"), (grpFKCtrls+".scalePivot"), rpr=True)
        return grpFKCtrlsConst, grpFKCtrls

    def setRotOrderFK(self, ctrls=[]):
        for ctrl in ctrls:
            cmds.setAttr((ctrl+".rotateOrder"), 3)
            # print ("ctrl = %s") %(ctrl)  | All ctrls rot order setted (XZY)

    def createCtrlsIK(self, color="", jnts=[]):
        ctrlNames = []
        c = ctrl.Control(n=("Ctrl_"+self.side+"_IK_Arm"), t="Hand", s=(0.9 * self.gblScaleGuide[0]), c=color)
        ctrlNames.append(str(c))
        if self.side == "L":
            cmds.scale(1, 1, -1, str(c)+'.cv[*]', r=True)
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        pivot = cmds.xform(c, q=True, ws=True, rp=True)
        grpOff = cmds.group(n=("Grp_Ctrl_"+self.side+"_IK_Arm_Off"))
        cmds.select(grpOff, r=True)
        cmds.move(pivot[0], pivot[1], pivot[2], grpOff+'.rp', grpOff+'.sp', rpr=True)
        grpConst = cmds.group(n=("Grp_Ctrl_"+self.side+"_IK_Arm_Const"))
        cmds.select(grpConst, r=True)
        cmds.move(pivot[0], pivot[1], pivot[2], grpConst+'.rp', grpConst+'.sp', rpr=True)
        grp = cmds.group(n=("Grp_Ctrl_"+self.side+"_IK_Arm"))
        cmds.move(pivot[0], pivot[1], pivot[2], grp+'.rp', grp+'.sp', rpr=True)
        cmds.select(jnts[0][2], grp, r=True)
        const = cmds.parentConstraint(weight=1)
        cmds.select(const, r=True)
        cmds.Delete()
        # cmds.setAttr(("Grp_Ctrl_"+self.side+"_IK_Arm.ty"), 0)
        # node = cmds.shadingNode("distanceBetween", asUtility=True)
        # cmds.connectAttr((jnts[0][2]+".tx"), (node+".point1X"), f=True)
        # cmds.connectAttr((jnts[0][3]+".tx"), (node+".point2X"), f=True)
        # dist = cmds.getAttr((node+".distance"))
        # cmds.Delete(node)
        # cmds.select(("Grp_Ctrl_"+self.side+"_IK_Arm"), r=True)
        # midDist = (dist * 0.45) / 2
        # cmds.getAttr(("Grp_Ctrl_"+self.side+"_IK_Arm.tz"))
        # pos = (cmds.getAttr(("Grp_Ctrl_"+self.side+"_IK_Arm.tz"))) - midDist
        # cmds.move(0 * self.gblScaleGuide[0], 0 * self.gblScaleGuide[0], -pos * self.gblScaleGuide[0], ("Ctrl_"+self.side+"_IK_Arm.cv[0:7]"), r=True, os=True, wd=True)
        # cmds.move(self.posAnkle[0], self.posAnkle[1], self.posAnkle[2], ("Ctrl_"+self.side+"_IK_Arm.rotatePivot"), ("Ctrl_"+self.side+"_IK_Arm.scalePivot"))
        # cmds.move(self.posAnkle[0], self.posAnkle[1], self.posAnkle[2], ("Grp_Ctrl_"+self.side+"_IK_Arm_Off.rotatePivot"), ("Grp_Ctrl_"+self.side+"_IK_Arm_Off.scalePivot"))
        # cmds.move(self.posAnkle[0], self.posAnkle[1], self.posAnkle[2], ("Grp_Ctrl_"+self.side+"_IK_Arm_Const.rotatePivot"), ("Grp_Ctrl_"+self.side+"_IK_Arm_Const.scalePivot"))
        # cmds.move(self.posAnkle[0], self.posAnkle[1], self.posAnkle[2], ("Grp_Ctrl_"+self.side+"_IK_Arm.rotatePivot"), ("Grp_Ctrl_"+self.side+"_IK_Arm.scalePivot"))
        return ctrlNames, grp

    def createPoleVector(self, jnts=[], color=""):
        start = cmds.xform(jnts[0], q=True, ws=True, t=True)  # UpperArm
        mid = cmds.xform(jnts[1], q=True, ws=True, t=True)    # Forearm
        end = cmds.xform(jnts[2], q=True, ws=True, t=True)    # Wrist
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
        loc = cmds.spaceLocator(n=("Loc_Ctrl_"+self.side+"_Arm_Pv"))[0]
        cmds.xform(loc, ws=True, t=(finalV.x, finalV.y, finalV.z))
        cmds.xform(loc, ws=True, ro=((rot.x / math.pi * 180.0),
                                     (rot.y / math.pi * 180.0),
                                     (rot.z / math.pi * 180.0)))
        if self.haveMultArms == 1:
            dispLine = []
            c = ctrl.Control(n=("Ctrl_"+self.side+"_Arm_Pv"), t="Diamond", s=(0.3 * self.gblScaleGuide[0]), c=color)
            cmds.select(c, r=True)
            cmds.group(n=("Grp_Ctrl_"+self.side+"_Arm_Pv_Off"))
            cmds.move(finalV.x, finalV.y, finalV.z, r=True)
            cmds.group(n=("Grp_Ctrl_"+self.side+"_Arm_Pv_Const"))
            cmds.CenterPivot()
            grpPV = cmds.group(n=("Grp_Ctrl_"+self.side+"_Arm_Pv"))
            cmds.CenterPivot()
            cmds.parent(loc, c)
            crv = cmds.curve(d=1, p=[(0, 0, 0), (0, 0, -32)], k=[0, 1])
            grpOff = cmds.group(n=("Grp_Crv_"+self.side+"_Arm_Pv_DispLine_Off"))
            grp = cmds.group(n=("Grp_Crv_"+self.side+"_Arm_Pv_DispLine"))
            cmds.select((crv+".cv[0]"), r=True)
            clJnt = cmds.cluster(n=("Cls_"+self.side+"_Arm_Pv_DispLine_Jnt"))
            cmds.select((crv+".cv[1]"), r=True)
            clCtrl = cmds.cluster(n=("Cls_"+self.side+"_Arm_Pv_DispLine_Ctrl"))
            cmds.select(loc, clCtrl, r=True)
            cmds.parentConstraint(weight=1)
            cmds.select(jnts[1], clJnt, r=True)
            cmds.parentConstraint(weight=1)
            cmds.setAttr(crv+".overrideEnabled", True)
            cmds.setAttr(crv+".overrideDisplayType", 2)
            cmds.setAttr((clJnt[0]+"Handle.v"), False)
            cmds.setAttr((clCtrl[0]+"Handle.v"), False)
            cmds.rename(crv, ("Crv_"+self.side+"_Arm_Pv_DispLine"))
            dispLine.append(grp); dispLine.append(clJnt[0]+"Handle"); dispLine.append(clCtrl[0]+"Handle")
            return loc, c, grpPV, dispLine
        elif self.haveMultArms == 2:
            c = ctrl.Control(n=("Ctrl_"+self.side+"_Arm_Pv"), t="Diamond", s=(0.3 * self.gblScaleGuide[0]), c=color)
            cmds.rename(loc, ("Loc_Ctrl_"+self.name+"_Pv"))

    def manageAttrCtrlsIK(self):
        if self.haveMultArms == 1:
            # Freeze controls
            ctrl.Control(n=("Ctrl_"+self.side+"_IK_Arm"), t="Lock and Hide", s=["sx", "sy", "sz"])
            ctrl.Control(n=("Ctrl_"+self.side+"_Arm_Pv"), t="Lock and Hide", s=["rx", "ry", "rz", "sx", "sy", "sz"])
            # Verify compound numbers
            armAttrs = 0
            pvAttrs = 1
            if self.haveAutoPv == True: armAttrs += 1
            if self.haveStretchIK == True: armAttrs += 1
            if self.haveStretchMultIK == True: armAttrs += 2
            if self.haveSquashIK == True: armAttrs += 1
            if self.haveSquashMultIK == True: armAttrs += 2
            if self.haveClampStretchIK == True: armAttrs += 2
            if self.haveElbowLockIK == True: pvAttrs += 1
            if self.haveSpaceSwitch == "Enabled": armAttrs += 1; pvAttrs += 1
            # Add Attrs
            cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Pv|Grp_Ctrl_"+self.side+"_Arm_Pv_Const|Grp_Ctrl_"+self.side+"_Arm_Pv_Off|Ctrl_"+self.side+"_Arm_Pv"),
                ln="ARM", nn="_____________________ ARM", at="enum", en="__________:")
            cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Arm_Pv|Grp_Ctrl_"+self.side+"_Arm_Pv_Const|Grp_Ctrl_"+self.side+"_Arm_Pv_Off|Ctrl_"+self.side+"_Arm_Pv.ARM"),
                edit=True, channelBox=True)
            cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Pv|Grp_Ctrl_"+self.side+"_Arm_Pv_Const|Grp_Ctrl_"+self.side+"_Arm_Pv_Off|Ctrl_"+self.side+"_Arm_Pv"),
                ln="PvSettings", at="compound", nc=pvAttrs)
            cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Pv|Grp_Ctrl_"+self.side+"_Arm_Pv_Const|Grp_Ctrl_"+self.side+"_Arm_Pv_Off|Ctrl_"+self.side+"_Arm_Pv"),
                ln="DisplayLine", at="bool", k=True, p="PvSettings")
            if self.haveAutoPv == True or self.haveStretchIK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
                    ln="ARM", nn="_____________________ ARM", at="enum", en="__________:")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
                    ln="ArmSettings", at="compound", nc=armAttrs)
                cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm.ARM"),
                    edit=True, channelBox=True)
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
                    ln="ElbowTwist", at="double", dv=0, k=True, p="ArmSettings")
            if self.haveStretchIK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
                    ln="Stretch", at="bool", k=True, p="ArmSettings")
            if self.haveStretchMultIK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
                    ln="UpperArmStretchMult", at="double", min=0.01, dv=1, k=True, p="ArmSettings")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
                    ln="ForearmStretchMult", at="double", min=0.01, dv=1, k=True, p="ArmSettings")
            if self.haveSquashIK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
                    ln="Squash", at="bool", k=True, p="ArmSettings")
            if self.haveSquashMultIK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
                    ln="UpperArmSquashMult", at="double", min=0.01, dv=1, k=True, p="ArmSettings")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
                    ln="ForearmSquashMult", at="double", min=0.01, dv=1, k=True, p="ArmSettings")
            if self.haveClampStretchIK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
                    ln="ClampStretch", at="bool", k=True, p="ArmSettings")
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
                    ln="ClampValue", at="double", min=1, dv=1.5, k=True, p="ArmSettings")
            if self.haveElbowLockIK == True:
                cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Pv|Grp_Ctrl_"+self.side+"_Arm_Pv_Const|Grp_Ctrl_"+self.side+"_Arm_Pv_Off|Ctrl_"+self.side+"_Arm_Pv"),
                    ln="ElbowLock", at="double", min=0, max=1, dv=0, k=True, p="PvSettings")
        #     if self.haveSpaceSwitch == "Enabled":
        #         rawSpaces = cmds.textScrollList("lstArmsSpaceListHArms", q=True, ai=True) # lstPvSpaceListHArms
        #         spaces = []
        #         enums = []
        #         y = 0
        #         for rs in rawSpaces:
        #             space = []
        #             for x in range(0, len(rs)):
        #                 if rs[x] == "|": y += 1
        #                 elif y == 1: space.append(rs[x])
        #             if not space == []: spc = ''.join(space)
        #             else: spc = rs
        #             spaces.append(spc)
        #             spc = ''; y = 0
        #         for s in spaces: enums.append(s); enums.append(":")
        #         enum = ''.join(enums)
        #         cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
        #             ln="Follow", at="enum", en=enum, p="ArmSettings")
        #         rawSpaces = cmds.textScrollList("lstPvSpaceListHArms", q=True, ai=True)
        #         spaces = []
        #         enums = []
        #         y = 0
        #         for rs in rawSpaces:
        #             space = []
        #             for x in range(0, len(rs)):
        #                 if rs[x] == "|": y += 1
        #                 elif y == 1: space.append(rs[x])
        #             if not space == []: spc = ''.join(space)
        #             else: spc = rs
        #             spaces.append(spc)
        #             spc = ''; y = 0
        #         for s in spaces: enums.append(s); enums.append(":")
        #         enum = ''.join(enums)
        #         cmds.addAttr(("|Grp_Ctrl_"+self.side+"_Arm_Pv|Grp_Ctrl_"+self.side+"_Arm_Pv_Const|Grp_Ctrl_"+self.side+"_Arm_Pv_Off|Ctrl_"+self.side+"_Arm_Pv"),
        #             ln="Follow", at="enum", en=enum, p="PvSettings")
            # Set Attrs
        #     if self.haveReverseHand == True:
        #         cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
        #             ln="FOOT", nn="____________________ FOOT", at="enum", en="__________:")
        #         cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
        #             ln="ReverseFoot", at="compound", nc=10)
        #         cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
        #             ln="FootRoll", at="double", dv=0, p="ReverseFoot")
        #         cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
        #             ln="FootRollBreak", at="double", dv=45, p="ReverseFoot")
        #         cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
        #             ln="FootRollStraight", at="double", dv=70, p="ReverseFoot")
        #         cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
        #             ln="FootBank", at="double", min=-90, max=90, dv=0, p="ReverseFoot")
        #         cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
        #             ln="FootLean", at="double", dv=0, p="ReverseFoot")
        #         cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
        #             ln="FootSpin", at="double", dv=0, p="ReverseFoot")
        #         cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
        #             ln="ToeSpin", at="double", dv=0, p="ReverseFoot")
        #         cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
        #             ln="ToeBend", at="double", dv=0, p="ReverseFoot")
        #         cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
        #             ln="ToeLean", at="double", dv=0, p="ReverseFoot")
        #         cmds.addAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm"),
        #             ln="HeelSpin", at="double", dv=0, p="ReverseFoot")
        #         cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm.FOOT"),
        #             edit=True, channelBox=True)
        #         cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm.FootRoll"),
        #             edit=True, k=True)
        #         cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm.FootRollBreak"),
        #             edit=True, k=True)
        #         cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm.FootRollStraight"),
        #             edit=True, k=True)
        #         cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm.FootBank"),
        #             edit=True, k=True)
        #         cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm.FootLean"),
        #             edit=True, k=True)
        #         cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm.FootSpin"),
        #             edit=True, k=True)
        #         cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm.ToeSpin"),
        #             edit=True, k=True)
        #         cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm.ToeBend"),
        #             edit=True, k=True)
        #         cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm.ToeLean"),
        #             edit=True, k=True)
        #         cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm.HeelSpin"),
        #             edit=True, k=True)
        #     if self.haveSpaceSwitch == "Enabled":
        #         cmds.setAttr(("|Grp_Ctrl_"+self.side+"_IK_Arm|Grp_Ctrl_"+self.side+"_IK_Arm_Const|Grp_Ctrl_"+self.side+"_IK_Arm_Off|Ctrl_"+self.side+"_IK_Arm.Follow"),
        #             edit=True, k=True)
        #         cmds.setAttr(("|Grp_Ctrl_"+self.side+"_Arm_Pv|Grp_Ctrl_"+self.side+"_Arm_Pv_Const|Grp_Ctrl_"+self.side+"_Arm_Pv_Off|Ctrl_"+self.side+"_Arm_Pv.Follow"),
        #             edit=True, k=True)
        # elif self.haveMultArms == 2: pass
