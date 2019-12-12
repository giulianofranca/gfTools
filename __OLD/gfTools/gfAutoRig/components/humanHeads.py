import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import math


from gfTools.__OLD.gfTools.gfAutoRig.settings import log
from gfTools.__OLD.gfTools.gfAutoRig.settings import controls as ctrl
reload(log); reload(ctrl)


class buildHumanHeads(object):

    def __init__(self):
        self.jntsBnd = []
        self.jntsDrv = []
        self.jntsRib = []
        # --------------------------------------------------------------------------------------------------------------
        # READ FEATURES                        | CheckBox = True/False | RadioBtn = 1/2 | OptionMenu = Enabled/Disabled
        self.numberOfJnts = cmds.intSliderGrp("intNumJntsHHeads", q=True, v=True)
        self.solverType = cmds.radioButtonGrp("radHybridTypeHHeads", q=True, sl=1)
        self.haveScale = cmds.checkBoxGrp("cbxScaleHeadsHHeads", q=True, v1=True)
        self.haveIK = cmds.optionMenuGrp("optEnIKSplineHHeads", q=True, v=True)
        self.numberOfIKJnts = cmds.intSliderGrp("intNumIKSplineJntsHHeads", q=True, v=True)
        self.haveStretchIK = cmds.checkBoxGrp("cbxStretchIKHHeads", q=True, v1=True)
        self.haveStretchMultIK = cmds.checkBoxGrp("cbxStretckIKMultHHeads", q=True, v1=True)
        self.haveClampStretchIK = cmds.checkBoxGrp("cbxClampStretchHHeads", q=True, v1=True)
        self.haveSquashIK = cmds.checkBoxGrp("cbxSquashIKHHeads", q=True, v1=True)
        self.haveSquashMultIK = cmds.checkBoxGrp("cbxSquashIKMultHHeads", q=True, v1=True)
        self.haveBendIK = cmds.checkBoxGrp("cbxBendIKHHeads", q=True, v1=True)
        self.haveRibbon = cmds.optionMenuGrp("optEnRibbonHHeads", q=True, v=True)
        self.haveBendCtrlsRib = cmds.checkBoxGrp("cbxBendCtrlsHHeads", q=True, v1=True)
        self.haveTweakCtrlsRib = cmds.checkBoxGrp("cbxTweakCtrlsHHeads", q=True, v1=True)
        self.haveTwistAttrsRib = cmds.checkBoxGrp("cbxTwistAttrsHHeads", q=True, v1=True)
        self.haveSineAttrsRib = cmds.checkBoxGrp("cbxSineAttrsHHeads", q=True, v1=True)
        # <<<------------------- PARA FAZER: Ribbon Squash Attributes
        self.haveExtraFreeSlotsRib = cmds.checkBoxGrp("cbxExtraFreeSlotsHHeads", q=True, v1=True)
        self.numberOfFreeSlotsRib = cmds.intSliderGrp("intNumExtraSlotsHHeads", q=True, v=True)
        self.haveSpaceSwitch = cmds.optionMenuGrp("optEnSpaceSwitchHHeads", q=True, v=True)
        # --------------------------------------------------------------------------------------------------------------
        # FIND GUIDES TRANSFORMATIONS
        self.gblScaleGuide = cmds.xform("gfARGuides:Ctrl_Global", q=True, r=True, s=True)
        self.gblScale = cmds.checkBoxGrp("cbxGlobalScaleMFeat", q=True, v1=True)
        self.setupFull = cmds.radioButtonGrp("radCompSetupMFeat", q=True, sl=True)
        if cmds.objExists(("gfARGuides:Ctrl_Neck")):
            self.posNeck = cmds.xform(("gfARGuides:Ctrl_Neck"), q=True, ws=True, rp=True)
        else: cmds.error("Cannot find Neck Guide"); return False
        if cmds.objExists(("gfARGuides:Ctrl_Head")):
            self.posHead = cmds.xform(("gfARGuides:Ctrl_Head"), q=True, ws=True, rp=True)
        else: cmds.error("Cannot find Head Guide"); return False
        if cmds.objExists(("gfARGuides:Ctrl_HeadEnd")):
            self.posHeadEnd = cmds.xform(("gfARGuides:Ctrl_HeadEnd"), q=True, ws=True, rp=True)
        else: cmds.error("Cannot find HeadEnd Guide"); return False
        if cmds.objExists(("gfARGuides:Ctrl_Jaw")):
            self.posJaw = cmds.xform(("gfARGuides:Ctrl_Jaw"), q=True, ws=True, rp=True)
        else: cmds.error("Cannot find Jaw Guide"); return False
        if cmds.objExists(("gfARGuides:Ctrl_JawPivot")):
            self.posJawPivot = cmds.xform(("gfARGuides:Ctrl_JawPivot"), q=True, ws=True, rp=True)
        else: cmds.error("Cannot find JawPivot Guide"); return False
        if cmds.objExists(("gfARGuides:Ctrl_JawEnd")):
            self.posJawEnd = cmds.xform(("gfARGuides:Ctrl_JawEnd"), q=True, ws=True, rp=True)
        else: cmds.error("Cannot find JawEnd Guide"); return False
        self.build()

    def getInfo(self):
        headsInfo = "Minhas cabecas"
        '''
        Info exports the parent location to put the locators on
        Ex: Neck Space = JntDrv_FK_Head | Chest Space = JntDrv_Crv_IK_Chest
        '''
        return self.jntsBnd, self.jntsDrv, self.jntsRib, headsInfo

    def build(self):
        cmds.select(cl=True)
        # Setting Joints Variables
        jntsNeck = []
        jntsHead = []
        neckIK = []
        if self.haveIK == "Enabled":
            neckRes = "JntDrv_FK_Neck"; headRes = "JntDrv_FK_Head"
            jntsNeck.append(neckRes); jntsNeck.append(headRes)
            for x in range(1, (self.numberOfIKJnts + 1)):
                neckIK.append(("JntBnd_IK_Neck_"+str(x)))
            jntsNeck.extend(neckIK)
        else:
            neckRes = "JntBnd_Neck"; headRes = "JntBnd_Head"
            jntsNeck.append(neckRes); jntsNeck.append(headRes)
        headRes = "JntDrv_Head"; headEndRes = "JntBnd_HeadEnd"; jawRes = "JntBnd_Jaw"; jawPivotRes = "JntBnd_JawPivot"; jawEndRes = "JntBnd_JawEnd"
        jntsHead.append(headRes); jntsHead.append(headEndRes); jntsHead.append(jawRes); jntsHead.append(jawPivotRes); jntsHead.append(jawEndRes)

        # print ("My Neck Joints = %s | My Head Joints = %s") %(jntsNeck, jntsHead)


        # Create Joints

        self.createJointsNeck(jntsNeck)
        self.createJointsHead(jntsHead)
        chainsNeck = self.connectJntChainsNeck(jntsNeck)
        chainsHead = self.connectJntChainsHead(jntsHead)
        self.orientJntsNeck(chainsNeck)
        self.orientJntsHead(chainsHead)
        self.setRotOrderJntsNeck(chainsNeck)
        self.setRotOrderJntsHead(chainsHead)
        # print ("\nCORRENTE HEAD = %s") %(chainsHead)


        # Create Controls

        # ctrlColor = "Yellow"; ctrlMainColor = "DarkYellow"; tweakColor = "DarkGreen"
        ctrlColor = 'Primary'; ctrlMainColor = 'Secondary'; tweakColor = 'Tertiary'
        ctrlNames = []
        ctrlSizes = []
        if self.haveIK == "Disabled":
            ctrlNames.append("Ctrl_FK_Neck")
            ctrlSizes.append(1 * self.gblScaleGuide[0])
            ctrlNames.append("Ctrl_FK_Head")
            ctrlSizes.append(0.8 * self.gblScaleGuide[0])
            self.createCtrls(names=ctrlNames, sizes=ctrlSizes, color=ctrlColor, jnts=chainsNeck[0])
            self.manageAttrCtrls(ctrls=ctrlNames)
            grpHeadCtrls, grpCtrlsFKConst = self.setHierarchyCtrlsFK(ctrls=ctrlNames)
            self.setRotOrderFK(ctrls=ctrlNames[0])
        elif self.haveIK == "Enabled":
            ctrlNames.append("Ctrl_FK_Neck")
            ctrlSizes.append(1 * self.gblScaleGuide[0])
            ctrlNames.append("Ctrl_IK_Head")
            ctrlSizes.append(0.8 * self.gblScaleGuide[0])
            # ctrlNames.append("Loc_IK_Neck")
            self.createCtrls(names=ctrlNames, sizes=ctrlSizes, color=ctrlColor, jnts=chainsNeck[0])
            grpHeadCtrls, grpCtrlsFKConst = self.setHierarchyCtrlsFK(ctrls=ctrlNames)
            self.setRotOrderFK(ctrls=ctrlNames[0])
            if self.haveBendIK == True:
                ctrlNames.append("Ctrl_IK_Neck_Bend")
                ctrlBend = self.createCtrlIKBend(name=ctrlNames[-1], jnts=chainsNeck[1], color=tweakColor)
            self.manageAttrCtrls(ctrls=ctrlNames)
            self.setRotOrderIK(ctrls=ctrlNames[1:len(ctrlNames)])


        # Create Setup

        if self.haveIK == "Enabled":
            fkJnts = []
            fkJnts.extend(chainsNeck[0][0:(len(chainsNeck[0]) - 1)])
            fkJnts.append(chainsHead[0])
            print ("\n FK JOINTS = %s") %(fkJnts)
            print ("\n CTRL NAMES = %s") %(ctrlNames[0:2])
            jntsCrv, ikNeck, crvNeck = self.associateIK(jnts=chainsNeck[1], ctrls=ctrlNames[1:3])
            self.associateFK(jnts=fkJnts, ctrls=ctrlNames[0:2], jntsNeck=chainsNeck[0])
            if self.haveBendIK == True:
                self.setupBendIK(ctrls=ctrlNames[1:len(ctrlNames)], jnt=jntsCrv[1])
                jntBend = jntsCrv[1]
            else: jntBend = jntsCrv[0]
            self.createTwistIK(jnts=jntsCrv, ctrlHead=ctrlNames[1], ctrlNeck=jntBend, ikHandle=ikNeck)
            if self.haveStretchIK == True:
                self.createStretchIK(crvIK=crvNeck, ctrlHead=ctrlNames[1], jnts=chainsNeck[1])
        else:
            fkJnts = []
            fkJnts.append(chainsNeck[0][0])
            fkJnts.append(chainsHead[0])
            print ("\n FK JOINTS = %s") %(chainsNeck[0])
            self.associateFK(jnts=chainsHead, ctrls=ctrlNames, jntsNeck=chainsNeck[0])


        # Clean Up Component
        cmds.select(chainsNeck[0][0], r=True)
        if self.haveIK == "Enabled": grpFKJnts = cmds.group(n=("Grp_JntDrv_Neck_FKConst"))
        else: grpFKJnts = cmds.group(n=("Grp_JntBnd_Neck_FKConst"))
        cmds.move(self.posNeck[0], self.posNeck[1], self.posNeck[2], (grpFKJnts+".rotatePivot"), (grpFKJnts+".scalePivot"), rpr=True)
        cmds.select(chainsHead[0], r=True)
        grpFKJntsHead = cmds.group(n=("Grp_JntBnd_Head_FKConst"))
        cmds.move(self.posHead[0], self.posHead[1], self.posHead[2], (grpFKJntsHead+".rotatePivot"), (grpFKJntsHead+".scalePivot"), rpr=True)
        if self.haveIK == "Enabled":
            cmds.select(chainsNeck[1][0], jntsCrv, r=True)
            grpIKJnts = cmds.group(n="Grp_JntBnd_Neck_IKConst")
            cmds.move(self.posNeck[0], self.posNeck[1], self.posNeck[2], (grpIKJnts+".rotatePivot"), (grpIKJnts+".scalePivot"), rpr=True)
            cmds.select(jntsCrv, r=True)
            grpIKCrvJnts = cmds.group(n="Grp_JntDrv_Neck_CrvJnts_IKConst")
            cmds.move(self.posNeck[0], self.posNeck[1], self.posNeck[2], (grpIKCrvJnts+".rotatePivot"), (grpIKCrvJnts+".scalePivot"), rpr=True)
            cmds.select(grpIKJnts, grpIKCrvJnts, r=True)
            grpJntsDONOTTOUCH = cmds.group(n="DO_NOT_TOUCH")
            cmds.move(self.posNeck[0], self.posNeck[1], self.posNeck[2], (grpJntsDONOTTOUCH+".rotatePivot"), (grpJntsDONOTTOUCH+".scalePivot"), rpr=True)
            cmds.setAttr((grpJntsDONOTTOUCH+".useOutlinerColor"), 1)
            cmds.setAttr((grpJntsDONOTTOUCH+".outlinerColorR"), 0.9372)
            cmds.setAttr((grpJntsDONOTTOUCH+".outlinerColorG"), 0.2823)
            cmds.setAttr((grpJntsDONOTTOUCH+".outlinerColorB"), 0.2117)
            cmds.select(grpFKJnts, grpFKJntsHead, grpJntsDONOTTOUCH, r=True)
            grpHeadJnts = cmds.group(n="Grp_JntBnd_Head")
            cmds.move(self.posNeck[0], self.posNeck[1], self.posNeck[2], (grpHeadJnts+".rotatePivot"), (grpHeadJnts+".scalePivot"), rpr=True)
            grpCtrlsIKConst = cmds.group(n=("Grp_Ctrl_Head_IKConst"), em=True)
            for c in ctrlNames[1:len(ctrlNames)]:
                cmds.parent(("Grp_"+str(c)), grpCtrlsIKConst)
            cmds.move(self.posNeck[0], self.posNeck[1], self.posNeck[2], (grpCtrlsIKConst+".rotatePivot"), (grpCtrlsIKConst+".scalePivot"), rpr=True)
            cmds.parent(grpCtrlsIKConst, grpHeadCtrls)
            # Connect Root Ctrl
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
            # Hide Attrs
            # attrs = []
            # attrs.append(grpFKJnts); attrs.append(grpIKJnts); attrs.append(grpIKCrvJnts); attrs.append(grpCtrlsFKConst); attrs.append(grpCtrlsIKConst)
            # attrs.append(grpJntsDONOTTOUCH); attrs.append(grpHeadCtrls); attrs.append(grpSpineJnts)
        #     for a in attrs:
        #         ctrl.Control(n=a, t="Lock and Hide", s=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])
            # Create Component hierarchy
            if self.setupFull == 1:
                cmds.parent(grpHeadJnts, "Grp_Sktn")
                cmds.parent(grpHeadCtrls, "Grp_Ctrl")
                cmds.parent(ikNeck, "Grp_ikHdle")
                cmds.parent(crvNeck, "Grp_Xtra_ToHide")
            elif self.setupFull == 2:
                cmds.select(grpHeadJnts, grpHeadCtrls, ikNeck, crvNeck, r=True)
                grpHead = cmds.group(n="Grp_HumanHeads")
        else:
            cmds.select(grpFKJnts, grpFKJntsHead, r=True)
            grpHeadJnts = cmds.group(n="Grp_JntBnd_Head")
            cmds.move(self.posNeck[0], self.posNeck[1], self.posNeck[2], (grpHeadJnts+".rotatePivot"), (grpHeadJnts+".scalePivot"), rpr=True)
        #     # Connect Root Ctrl
        #     cmds.select(rootCtrl, grpFKJnts, r=True)
        #     const = cmds.parentConstraint(weight=1, mo=True)
        #     cmds.select(rootCtrl, grpCtrlsFKConst, r=True)
        #     const = cmds.parentConstraint(weight=1, mo=True)
        #     # Hide Attrs
        #     attrs = []
        #     attrs.append(grpFKJnts); attrs.append(grpCtrlsFKConst); attrs.append(grpHeadCtrls); attrs.append(grpHeadJnts)
        #     for a in attrs:
        #         ctrl.Control(n=a, t="Lock and Hide", s=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])
            # Create Component hierarchy
            if self.setupFull == 1:
                cmds.parent(grpHeadJnts, "Grp_Sktn")
                cmds.parent(grpHeadCtrls, "Grp_Ctrl")
            elif self.setupFull == 2:
                cmds.select(grpHeadJnts, grpHeadCtrls, r=True)
                grpHead = cmds.group(n="Grp_HumanHeads")


        # Return Features

        if self.haveIK == "Enabled":
            self.jntsBnd.extend(chainsNeck[1])
            self.jntsBnd.extend(chainsHead[1:len(chainsHead)])
            self.jntsDrv.extend(chainsNeck[0])
            self.jntsDrv.append(chainsHead[0])
        elif self.haveRibbon == "Enabled":
            pass
        else:
            self.jntsBnd.extend(chainsNeck[0])
            self.jntsBnd.extend(chainsHead[1:len(chainsHead)])
            self.jntsDrv.append(chainsHead[0])



    def createJointsNeck(self, jnts=[]):
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

    def createJointsHead(self, jnts=[]):
        pos = [(self.posHead[0], self.posHead[1], self.posHead[2]),
            (self.posHeadEnd[0], self.posHeadEnd[1], self.posHeadEnd[2]),
            (self.posJaw[0], self.posJaw[1], self.posJaw[2]),
            (self.posJawPivot[0], self.posJawPivot[1], self.posJawPivot[2]),
            (self.posJawEnd[0], self.posJawEnd[1], self.posJawEnd[2])]
        x = 0
        for j in jnts:
            cmds.select(cl=True)
            jnt = cmds.joint(p=(pos[x][0], pos[x][1], pos[x][2]))
            cmds.rename(jnt, j)
            # print ("Jnt #"+str(x)+" | Pos = %s") %(pos[x])
            x += 1

    def connectJntChainsNeck(self, jnts=[]):
        chains = []
        for x in range(0, (self.numberOfJnts - 1)):
            try:
                cmds.parent(jnts[x+1], jnts[x])
            except IndexError:
                cmds.warning(("Index "+str(x)+" ignored"))
        # print ("Chain 1 = %s") %(jnts[0:self.numberOfJnts])
        chains.append(jnts[0:self.numberOfJnts])
        if self.haveIK == "Enabled":
            jntsFK = self.numberOfJnts
            totalJnts = self.numberOfIKJnts + self.numberOfJnts
            for x in range(jntsFK, (totalJnts - 1)):
                try:
                    cmds.parent(jnts[x+1], jnts[x])
                except IndexError:
                    cmds.warning(("Index "+str(x)+" ignored"))
                # print ("Parent "+str(x+1)+", "+str(x))
            # print ("\nChain 2 = %s") %(jnts[jntsFK:(totalJnts+2)])
            chains.append(jnts[jntsFK:(totalJnts+2)])
        return chains

    def connectJntChainsHead(self, jnts=[]):
        chains = []
        cmds.parent(jnts[1], jnts[0])
        cmds.parent(jnts[2], jnts[0])
        cmds.parent(jnts[3], jnts[2])
        cmds.parent(jnts[4], jnts[3])
        # print ("Chain 3 = %s") %(jnts)
        chains.extend(jnts)
        return chains

    def orientJntsNeck(self, chains=[]):
        count = len(chains)
        for x in range(0, count):
            cmds.select(chains[x][0], r=True)
            cmds.joint(edit=True, oj="xyz", sao="zup", ch=True, zso=True) # XYZ
            cmds.select(chains[x][-1], r=True)
            cmds.joint(edit=True, oj="none", zso=True)

    def orientJntsHead(self, chains=[]):
        cmds.select(chains[0], r=True)
        cmds.joint(edit=True, oj="xyz", sao="zup", zso=True) # XYZ
        cmds.select(chains[1], r=True)
        cmds.joint(edit=True, oj="none", zso=True)
        cmds.select(chains[2:len(chains)], r=True)
        cmds.joint(edit=True, oj="xyz", sao="ydown", ch=True, zso=True) # XYY
        cmds.select(chains[-1], r=True)
        cmds.joint(edit=True, oj="none", zso=True)

    def setRotOrderJntsNeck(self, chains=[]):
        for c in chains:
            for jnt in c:
                cmds.setAttr((jnt+".rotateOrder"), 3) # XZY

    def setRotOrderJntsHead(self, chains=[]):
        for x in range(0, 2):
            cmds.setAttr((chains[x]+".rotateOrder"), 3) # XZY
        for x in range(2, len(chains)):
            cmds.setAttr((chains[x]+".rotateOrder"), 2) # ZXY

    def createCtrls(self, names=[], sizes=[], color="", jnts=[]):
        c = ctrl.Control(n=names[0], t="Circle", s=sizes[0], c=color)
        grp = cmds.group(n=("Grp_"+names[0]))
        cmds.select(jnts[0], r=True)
        cmds.select(grp, add=True)
        const = cmds.parentConstraint(weight=1)
        cmds.select(const, r=True)
        cmds.Delete()
        cmds.select((str(c)+".cv[0:7]"), r=True)
        cmds.rotate(0, 0, 90, r=True, os=True)
        c = ctrl.Control(n=names[1], t="Head", s=sizes[1], c=color)
        grp = cmds.group(n=("Grp_"+names[1]))
        cmds.move(0, 0, 0, (grp+".rotatePivot"), (grp+".scalePivot"), rpr=True)
        cmds.select(jnts[1], r=True)
        cmds.select(grp, add=True)
        const = cmds.parentConstraint(weight=1)
        cmds.select(const, r=True)
        cmds.Delete()
        # if self.haveIK == "Enabled":
        #     loc = cmds.spaceLocator(n=names[2])
        #     grp = cmds.group(n=("Grp_"+names[2]))
        #     cmds.select(jnts[0], grp, r=True)
        #     parConst = cmds.parentConstraint(weight=1)
        #     cmds.select(parConst, r=True)
        #     cmds.Delete()

    def manageAttrCtrls(self, ctrls=[]):
        ctrl.Control(n=ctrls[0], t="Lock and Hide", s=["tx", "ty", "tz", "sx", "sy", "sz"])
        if self.haveStretchIK == True: ctrl.Control(n=ctrls[1], t="Lock and Hide", s=["sx", "sy", "sz"])
        else: ctrl.Control(n=ctrls[1], t="Lock and Hide", s=["tx", "ty", "tz", "sx", "sy", "sz"])
        if self.haveBendIK == True:
            ctrl.Control(n=ctrls[2], t="Lock and Hide", s=["sx", "sy", "sz"])
        # Neck | Head | Loc | Bend
        neckAttrs = 2 # Twists
        if self.haveBendIK == True: neckAttrs += 1
        if self.haveStretchIK == True: neckAttrs += 1
        if self.haveStretchMultIK == True: neckAttrs += 1
        if self.haveClampStretchIK == True: neckAttrs += 2
        if self.haveSquashIK == True: neckAttrs += 1
        if self.haveSquashMultIK == True: neckAttrs += 1
        # Add Attrs
        if self.haveBendIK == True:
            cmds.addAttr(("|Grp_"+str(ctrls[2])+"|"+str(ctrls[2])), ln="HEAD", nn="____________________ HEAD", at="enum", en="__________:")
            cmds.setAttr(("|Grp_"+str(ctrls[2])+"|"+str(ctrls[2])+".HEAD"), edit=True, channelBox=True)
            cmds.addAttr(("|Grp_"+str(ctrls[2])+"|"+str(ctrls[2])), ln="FollowHead", at="bool")
            cmds.setAttr(("|Grp_"+str(ctrls[2])+"|"+str(ctrls[2])+".FollowHead"), edit=True, k=True)
        if self.haveIK == "Enabled":
            cmds.addAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])), ln="NECK", nn="____________________ NECK", at="enum", en="__________:")
            cmds.setAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])+".NECK"), edit=True, channelBox=True)
            cmds.addAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])), ln="NeckSettings", at="compound", nc=neckAttrs)
            if self.haveBendIK == True:
                cmds.addAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])), ln="SecondaryCtrls", at="bool", p="NeckSettings")
            cmds.addAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])), ln="NeckTwistMult", at="double", dv=0, p="NeckSettings")
            cmds.addAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])), ln="HeadTwistMult", at="double", dv=0, p="NeckSettings")
        if self.haveStretchIK == True:
            cmds.addAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])), ln="NeckStretch", at="bool", p="NeckSettings")
        if self.haveStretchMultIK == True:
            cmds.addAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])), ln="NeckStretchMult", at="double", min=0.01, dv=1, p="NeckSettings")
        if self.haveClampStretchIK == True:
            cmds.addAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])), ln="ClampStretch", at="bool", p="NeckSettings")
            cmds.addAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])), ln="ClampValue", at="double", min=1, dv=1.5, p="NeckSettings")
        if self.haveSquashIK == True:
            cmds.addAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])), ln="NeckSquash", at="bool", p="NeckSettings")
        if self.haveSquashMultIK == True:
            cmds.addAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])), ln="NeckSquashMult", at="double", min=0.01, dv=1, p="NeckSettings")
        if self.haveSpaceSwitch == "Enabled":
            cmds.addAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])), ln="HEAD", nn="____________________ HEAD", at="enum", en="__________:")
            cmds.setAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])+".HEAD"), edit=True, channelBox=True)
            rawSpaces = cmds.textScrollList("lstHeadsSpaceListHHeads", q=True, ai=True)
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
            cmds.addAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])), ln="Follow", at="enum", en=enum)
        cmds.addAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])), ln="FACIAL", nn="__________________ FACIAL", at="enum", en="__________:")
        cmds.setAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])+".FACIAL"), edit=True, channelBox=True)
        # Set Attrs
        if self.haveIK == "Enabled":
            if self.haveBendIK == True:
                cmds.setAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])+".SecondaryCtrls"), edit=True, k=True)
                cmds.connectAttr((str(ctrls[1])+".SecondaryCtrls"), (str(ctrls[2]+".v")))
                ctrl.Control(n=ctrls[2], t="Lock and Hide", s=["v"])
            cmds.setAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])+".NeckTwistMult"), edit=True, k=True)
            cmds.setAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])+".HeadTwistMult"), edit=True, k=True)
        if self.haveStretchIK == True:
            cmds.setAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])+".NeckStretch"), edit=True, k=True)
        if self.haveStretchMultIK == True:
            cmds.setAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])+".NeckStretchMult"), edit=True, k=True)
        if self.haveClampStretchIK == True:
            cmds.setAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])+".ClampStretch"), edit=True, k=True)
            cmds.setAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])+".ClampValue"), edit=True, k=True)
        if self.haveSquashIK == True:
            cmds.setAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])+".NeckSquash"), edit=True, k=True)
        if self.haveSquashMultIK == True:
            cmds.setAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])+".NeckSquashMult"), edit=True, k=True)
        if self.haveSpaceSwitch == "Enabled":
            cmds.setAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])+".Follow"), edit=True, k=True)

    def setHierarchyCtrlsFK(self, ctrls=[]):
        # FK MODE: Neck | Head
        cmds.select(("Grp_"+ctrls[0]), r=True)
        grpCtrlsFKConst = cmds.group(n=("Grp_Ctrl_Head_FKConst"))
        cmds.move(self.posNeck[0], self.posNeck[1], self.posNeck[2], (grpCtrlsFKConst+".rotatePivot"), (grpCtrlsFKConst+".scalePivot"), rpr=True)
        cmds.select(grpCtrlsFKConst, r=True)
        grpCtrlsFK = cmds.group(n=("Grp_Ctrl_Head"))
        cmds.move(self.posNeck[0], self.posNeck[1], self.posNeck[2], (grpCtrlsFK+".rotatePivot"), (grpCtrlsFK+".scalePivot"), rpr=True)
        if self.haveIK != "Enabled": cmds.parent(("Grp_"+ctrls[1]), ctrls[0])
        return grpCtrlsFK, grpCtrlsFKConst

    def setRotOrderFK(self, ctrls=[]):
        # for ctrl in ctrls:                                    REFAZER QUANDO TIVER MAIS PESCOCOS
        #     cmds.setAttr((ctrl+".rotateOrder"), 3) # XZY
        cmds.setAttr((ctrls+".rotateOrder"), 3) # XZY

    def setRotOrderIK(self, ctrls=[]):
        for c in ctrls:
            cmds.setAttr((c+".rotateOrder"), 2) # ZXY

    def associateFK(self, jnts=[], ctrls=[], jntsNeck=[]):
        if self.haveIK == "Enabled":
            cmds.connectAttr((ctrls[0]+".r"), (jnts[0]+".r"))
            print ("\n TEST JNTS = %s") %(jnts)
            print ("\n TEST CTRLS = %s") %(ctrls)
            print ("\n TEST NECK = %s") %(jntsNeck)
            if self.haveSpaceSwitch != "Enabled":
                cmds.select(jntsNeck[1], ("Grp_"+ctrls[1]), r=True)
                cmds.parentConstraint(weight=1, mo=True)
            cmds.select(ctrls[1], jnts[1], r=True)
            cmds.parentConstraint(weight=1, mo=True)
        else:
            for x in range(0, len(ctrls)):
                cmds.connectAttr((ctrls[x]+".r"), (jntsNeck[x]+".r"))
            cmds.select(jntsNeck[-1], jnts[0], r=True)
            cmds.parentConstraint(weight=1, mo=True)

    def createCtrlIKBend(self, name="", jnts=[], color=""):
        ctrlBend = []
        dist = [(self.posHead[0] - self.posNeck[0]), (self.posHead[1] - self.posNeck[1]), (self.posHead[2] - self.posNeck[2])]
        pos = [(dist[0] * 0.5), (dist[1] * 0.5), (dist[2] * 0.5)]
        finalPos = [(self.posNeck[0] + pos[0]), (self.posNeck[1] + pos[1]), (self.posNeck[2] + pos[2])]
        cmds.select(cl=True)
        loc = cmds.joint(p=(finalPos[0], finalPos[1], finalPos[2]))
        cmds.select(cl=True)
        c = ctrl.Control(n=name, t="Gear Smooth", s=(0.8 * self.gblScaleGuide[0]), c=color)
        grp = cmds.group(n=("Grp_"+str(c)))
        cmds.move(0, 0, 0, (grp+".rotatePivot"), (grp+".scalePivot"), rpr=True)
        cmds.select(loc, grp, r=True)
        pntConst = cmds.pointConstraint(weight=1)
        cmds.select(jnts[0], grp, r=True)
        oriConst = cmds.orientConstraint(weight=1)
        ctrlBend.append(c)
        cmds.select(pntConst, oriConst, loc, r=True)
        cmds.Delete()
        cmds.select((str(c)+".cv[*]"), r=True)
        cmds.rotate(0, 0, 90, r=True, os=True)
        return ctrlBend

    def associateIK(self, jnts=[], ctrls=[]):
        jntsCrv = []
        ikNeck, effNeck, crvNeck = cmds.ikHandle(n="ikHdle_Neck", sol="ikSplineSolver", sj=jnts[0], ee=jnts[-1])
        cmds.select(jnts[0], r=True)
        jntNeck = cmds.duplicate(rr=True)
        jntNeckChildren = cmds.listRelatives(ad=True, f=True)
        cmds.select(jntNeckChildren[0], r=True)
        jntHead = cmds.duplicate(rr=True)
        cmds.parent(w=True)
        for x in range(0, len(jntNeckChildren)):
            cmds.select(jntNeckChildren[x], r=True)
            cmds.Delete()
        if self.haveBendIK == True:
            cmds.select(cl=True)
            jntBend = cmds.joint()
            cmds.select(str(ctrls[-1]), jntBend, r=True)
            pntConst = cmds.pointConstraint(weight=1)
            cmds.select(pntConst, r=True)
            cmds.Delete()
            cmds.parent(jntBend, jntNeck)
            cmds.select(jntBend, r=True)
            cmds.joint(edit=True, oj="none", zso=True)
            cmds.parent(w=True)
        cmds.rename(jntNeck, "JntDrv_Crv_IK_Neck")
        cmds.rename(jntHead, "JntDrv_Crv_IK_Head")
        if self.haveBendIK == True:
            cmds.rename(jntBend, "JntDrv_Crv_IK_Neck_Bend")
            jntsCrv.append("JntDrv_Crv_IK_Neck_Bend")
        jntsCrv.append("JntDrv_Crv_IK_Neck")
        jntsCrv.append("JntDrv_Crv_IK_Head")
        cmds.skinCluster(jntsCrv, crvNeck, tsb=True, sm=0, nw=1, mi=len(jntsCrv), rui=True, omi=True, dr=4.0)
        cmds.rename(effNeck, "Eff_Neck")
        cmds.rename(crvNeck, "Crv_Neck")
        for jnt in jntsCrv:
            cmds.setAttr((jnt+".rotateOrder"), 2) # ZXY
        for ctrl in ctrls:
            cmds.setAttr((str(ctrl)+".rotateOrder"), 2) # ZXY
        # Head | Neck | Bend
        # cmds.select(str(ctrls[1]), jntsCrv[-2], r=True)
        # cmds.parentConstraint(weight=1)
        cmds.select(str(ctrls[0]), jntsCrv[-1], r=True)
        cmds.parentConstraint(weight=1)
        if self.haveBendIK == True:
            cmds.select(str(ctrls[1]), jntsCrv[0], r=True)
            cmds.parentConstraint(weight=1)
        return jntsCrv, ikNeck, "Crv_Neck"

    def setupBendIK(self, ctrls=[], jnt=""):
        # Head | Bend || Neck
        cmds.select(str(ctrls[0]), jnt, ("Grp_"+str(ctrls[1])), r=True)
        const = cmds.parentConstraint(weight=1, mo=True)
        bcBendFollow = cmds.shadingNode("blendColors", asUtility=True, n="Bc_Neck_Bend_Follow")
        cmds.connectAttr((str(ctrls[1])+".FollowHead"), (bcBendFollow+".blender"))
        cmds.connectAttr((bcBendFollow+".outputR"), (str(const[0])+"."+str(ctrls[0])+"W0"))
        cmds.connectAttr((bcBendFollow+".outputR"), (str(const[0])+"."+jnt+"W1"))
        cmds.setAttr(((str(ctrls[1])+".FollowHead")), True)

    def createTwistIK(self, jnts=[], ctrlHead="", ctrlNeck="", ikHandle=""):
        pmaTwistOffsetHead = cmds.shadingNode("plusMinusAverage", asUtility=True, n="Pma_Neck_Head_TwistOffset")
        pmaTwistOffsetNeck = cmds.shadingNode("plusMinusAverage", asUtility=True, n="Pma_Neck_Neck_TwistOffset")
        pmaCounterTwist = cmds.shadingNode("plusMinusAverage", asUtility=True, n="Pma_Neck_CounterTwist")
        cmds.connectAttr((str(ctrlHead)+".rx"), (pmaTwistOffsetHead+".input1D[0]"))
        cmds.connectAttr((str(ctrlHead)+".HeadTwistMult"), (pmaTwistOffsetHead+".input1D[1]"))
        cmds.connectAttr((str(ctrlNeck)+".rx"), (pmaTwistOffsetNeck+".input1D[0]"))
        cmds.connectAttr((str(ctrlHead)+".NeckTwistMult"), (pmaTwistOffsetNeck+".input1D[1]"))
        cmds.connectAttr((pmaTwistOffsetNeck+".output1D"), (ikHandle+".roll"))
        cmds.connectAttr((pmaTwistOffsetHead+".output1D"), (pmaCounterTwist+".input1D[0]"))
        cmds.connectAttr((pmaTwistOffsetNeck+".output1D"), (pmaCounterTwist+".input1D[1]"))
        cmds.setAttr((pmaCounterTwist+".operation"), 2)
        cmds.connectAttr((pmaCounterTwist+".output1D"), (ikHandle+".twist"))

    def createStretchIK(self, crvIK="", ctrlHead="", jnts=[]):
        cmds.select(crvIK, r=True)
        crvIKShape = cmds.listRelatives(s=True)
        info = cmds.shadingNode("curveInfo", asUtility=True, n="Cinf_Neck_Info")
        mdStretch = cmds.shadingNode("multiplyDivide", asUtility=True, n="Md_Neck_Stretch_Div")
        bcStretchSwitch = cmds.shadingNode("blendColors", asUtility=True, n="Bc_Neck_Stretch_Switch")
        if self.gblScale == True:
            mdGblScaleStretch = cmds.shadingNode("multiplyDivide", asUtility=True, n="Md_Neck_Stretch_GblScale_Div")
        if self.haveStretchMultIK == True:
            mdStretchMult = cmds.shadingNode("multiplyDivide", asUtility=True, n="Md_Neck_StretchMult_Mult")
        if self.haveClampStretchIK == True:
            cmpClampStretch = cmds.shadingNode("clamp", asUtility=True, n="Cmp_Neck_Stretch")
            bcClampStretchSwitch = cmds.shadingNode("blendColors", asUtility=True, n="Bc_Neck_ClampStretch_Switch")
        if self.haveSquashIK == True:
            mdSqrtStretch = cmds.shadingNode("multiplyDivide", asUtility=True, n="Md_Neck_SqrtStretch_Pow")
            mdSquash = cmds.shadingNode("multiplyDivide", asUtility=True, n="Md_Neck_Squash_Div")
            bcSquashSwitch = cmds.shadingNode("blendColors", asUtility=True, n="Bc_Neck_Squash_Switch")
        if self.haveSquashMultIK == True:
            mdSquashMult = cmds.shadingNode("multiplyDivide", asUtility=True, n="Md_Neck_SquashMult_Mult")
        cmds.connectAttr((crvIKShape[0]+".worldSpace"), (info+".inputCurve"))
        if self.gblScale == True:
            cmds.connectAttr((info+".arcLength"), (mdGblScaleStretch+".input1X"))
            if self.setupFull == 1: cmds.connectAttr(("Ctrl_Global.sy"), (mdGblScaleStretch+".input2X"))
            cmds.setAttr((mdGblScaleStretch+".operation"), 2)
            cmds.connectAttr((mdGblScaleStretch+".outputX"), (mdStretch+".input1X"))
        else:
            cmds.connectAttr((info+".arcLength"), (mdStretch+".input1X"))
        cmds.setAttr((mdStretch+".input2X"), cmds.arclen(crvIKShape[0]))
        cmds.setAttr((mdStretch+".operation"), 2)
        if self.haveStretchMultIK == True:
            cmds.connectAttr((mdStretch+".outputX"), (mdStretchMult+".input1X"))
            cmds.connectAttr((str(ctrlHead)+".NeckStretchMult"), (mdStretchMult+".input2X"))
            cmds.connectAttr((mdStretchMult+".outputX"), (bcStretchSwitch+".color1R"))
            cmds.setAttr((bcStretchSwitch+".color2R"), 1)
            cmds.connectAttr((str(ctrlHead)+".NeckStretch"), (bcStretchSwitch+".blender"))
        else:
            cmds.connectAttr((mdStretch+".outputX"), (bcStretchSwitch+".color1R"))
            cmds.setAttr((bcStretchSwitch+".color2R"), 1)
            cmds.connectAttr((str(ctrlHead)+".NeckStretch"), (bcStretchSwitch+".blender"))
        if self.haveClampStretchIK == True:
            cmds.connectAttr((bcStretchSwitch+".outputR"), (cmpClampStretch+".inputR"))
            cmds.connectAttr((str(ctrlHead)+".ClampValue"), (cmpClampStretch+".maxR"))
            cmds.connectAttr((cmpClampStretch+".outputR"), (bcClampStretchSwitch+".color1R"))
            cmds.connectAttr((bcStretchSwitch+".outputR"), (bcClampStretchSwitch+".color2R"))
            cmds.connectAttr((str(ctrlHead)+".ClampStretch"), (bcClampStretchSwitch+".blender"))
        for x in range(0, (self.numberOfIKJnts - 1)):
            if self.haveClampStretchIK == True:
                cmds.connectAttr((bcClampStretchSwitch+".outputR"), (jnts[x]+".sx"))
            else:
                cmds.connectAttr((bcStretchSwitch+".outputR"), (jnts[x]+".sx"))
        if self.haveSquashIK == True:
            cmds.connectAttr((bcStretchSwitch+".outputR"), (mdSqrtStretch+".input1X"))
            cmds.setAttr((mdSqrtStretch+".operation"), 3)
            cmds.setAttr((mdSqrtStretch+".input2X"), 0.5)
            cmds.connectAttr((mdSqrtStretch+".outputX"), (mdSquash+".input2X"))
            cmds.setAttr((mdSquash+".operation"), 2)
            cmds.setAttr((mdSquash+".input1X"), 1)
            if self.haveSquashMultIK == True:
                cmds.connectAttr((mdSquash+".outputX"), (mdSquashMult+".input1X"))
                cmds.connectAttr((str(ctrlHead)+".NeckSquashMult"), (mdSquashMult+".input2X"))
                cmds.connectAttr((mdSquashMult+".outputX"), (bcSquashSwitch+".color1R"))
                cmds.setAttr((bcSquashSwitch+".color2R"), 1)
                cmds.connectAttr((str(ctrlHead)+".NeckSquash"), (bcSquashSwitch+".blender"))
            else:
                cmds.connectAttr((mdSquash+".outputX"), (bcSquashSwitch+".color1R"))
                cmds.setAttr((bcSquashSwitch+".color2R"), 1)
                cmds.connectAttr((str(ctrlHead)+".NeckSquash"), (bcSquashSwitch+".blender"))
            for x in range(0, (self.numberOfIKJnts - 1)):
                cmds.connectAttr((bcSquashSwitch+".outputR"), (jnts[x]+".sy"))
                cmds.connectAttr((bcSquashSwitch+".outputR"), (jnts[x]+".sz"))
