import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import math


from gfTools.gfAutoRig.settings import log
from gfTools.gfAutoRig.settings import controls as ctrl
reload(log); reload(ctrl)


class buildHumanSpine(object):

    def __init__(self):
        self.jntsBnd = []
        self.jntsDrv = []
        self.jntsRib = []
        # self.slotGblSca = False
        # --------------------------------------------------------------------------------------------------------------
        # READ FEATURES                        | CheckBox = True/False | RadioBtn = 1/2 | OptionMenu = Enabled/Disabled
        self.numberOfJnts = cmds.intSliderGrp("intNumJntsHSpine", q=True, v=True)
        self.solverType = cmds.radioButtonGrp("radHybridTypeHSpine", q=True, sl=1)
        self.haveTangent = cmds.checkBoxGrp("cbxTangentCtrlsHSpine", q=True, v1=True)
        self.haveScale = cmds.checkBoxGrp("cbxScaleSpineHSpine", q=True, v1=True)
        self.haveIK = cmds.optionMenuGrp("optEnIKSplineHSpine", q=True, v=True)
        self.numberOfIKJnts = cmds.intSliderGrp("intNumIKSplineJntsHSpine", q=True, v=True)
        self.haveTwistIK = cmds.checkBoxGrp("cbxTwistIKHSpine", q=True, v1=True)
        self.haveStretchIK = cmds.checkBoxGrp("cbxStretchIKHSpine", q=True, v1=True)
        self.haveStretchMultIK = cmds.checkBoxGrp("cbxStretckIKMultHSpine", q=True, v1=True)
        self.haveClampStretchIK = cmds.checkBoxGrp("cbxClampStretchHSpine", q=True, v1=True)
        self.haveSquashIK = cmds.checkBoxGrp("cbxSquashIKHSpine", q=True, v1=True)
        self.haveSquashMultIK = cmds.checkBoxGrp("cbxSquashIKMultHSpine", q=True, v1=True)
        self.haveBendIK = cmds.checkBoxGrp("cbxBendIKHSpine", q=True, v1=True)
        self.haveRibbon = cmds.optionMenuGrp("optEnRibbonHSpine", q=True, v=True)
        self.haveBendCtrlsRib = cmds.checkBoxGrp("cbxBendCtrlsHSpine", q=True, v1=True)
        self.haveTweakCtrlsRib = cmds.checkBoxGrp("cbxTweakCtrlsHSpine", q=True, v1=True)
        self.haveTwistAttrsRib = cmds.checkBoxGrp("cbxTwistAttrsHSpine", q=True, v1=True)
        self.haveSineAttrsRib = cmds.checkBoxGrp("cbxSineAttrsHSpine", q=True, v1=True)
        # <<<------------------- PARA FAZER: Ribbon Squash Attributes
        self.haveExtraFreeSlotsRib = cmds.checkBoxGrp("cbxExtraFreeSlotsHSpine", q=True, v1=True)
        self.numberOfFreeSlotsRib = cmds.intSliderGrp("intNumExtraSlotsHSpine", q=True, v=True)
        # --------------------------------------------------------------------------------------------------------------
        # FIND GUIDES TRANSFORMATIONS
        self.gblScaleGuide = cmds.xform("gfARGuides:Ctrl_Global", q=True, r=True, s=True)
        self.gblScale = cmds.checkBoxGrp("cbxGlobalScaleMFeat", q=True, v1=True)
        self.setupFull = cmds.radioButtonGrp("radCompSetupMFeat", q=True, sl=True)
        if cmds.objExists(("gfARGuides:Ctrl_Hip")):
            self.posHip = cmds.xform(("gfARGuides:Ctrl_Hip"), q=True, ws=True, rp=True)
        else: cmds.error("Cannot find Hip Guide"); return False
        if cmds.objExists(("gfARGuides:Ctrl_Chest")):
            self.posChest = cmds.xform(("gfARGuides:Ctrl_Chest"), q=True, ws=True, rp=True)
        else: cmds.error("Cannot find Chest Guide"); return False
        for x in range(1, (self.numberOfJnts + 1)):
            if cmds.objExists(("gfARGuides:Ctrl_Spine"+str(x))):
                toExec = (r"self.posSpine"+str(x)+" = cmds.xform(('gfARGuides:Ctrl_Spine"+str(x)+"'), q=True, ws=True, rp=True)")
                exec(toExec)
                # Result: self.posSpine1 | self.posSpine2 | self.posSpine3 | self.posSpine4 | self.posSpine5
            else: cmds.error("Cannot find Spine "+str(x)+" Guide"); return False

        self.build()

    def getInfo(self):
        # if self.gblScale == True:
        #     if self.setupFull == 2:
        #         self.slotGblSca == True
        # spineInfo = [self.slotGblSca]
        spineInfo = ""
        return self.jntsBnd, self.jntsDrv, self.jntsRib, spineInfo


    def build(self):
        cmds.select(cl=True)
        # Setting Joints Variables
        jnts = []
        spinesRes = []
        spinesIK = []
        if self.haveIK == "Enabled":
            hipRes = "JntDrv_FK_Hip"; chestRes = "JntDrv_FK_Chest"
            for x in range(1, (self.numberOfJnts + 1)):
                spinesRes.append(("JntDrv_FK_Spine_"+str(x)))
            jnts.append(hipRes); jnts.extend(spinesRes); jnts.append(chestRes)
            for x in range(1, (self.numberOfIKJnts + 1)):
                spinesIK.append(("JntBnd_IK_Spine_"+str(x)))
            jnts.extend(spinesIK)
        else:
            hipRes = "JntBnd_Hip"; chestRes = "JntBnd_Chest"
            for x in range(1, (self.numberOfJnts + 1)):
                spinesRes.append(("JntBnd_Spine_"+str(x)))
            jnts.append(hipRes); jnts.extend(spinesRes); jnts.append(chestRes)


        # Create Joints

        self.createJoints(jnts)
        chains = self.connectJntChains(jnts)
        self.orientJnts(chains)
        self.setRotOrderJnts(chains)


        # Create Controls

        # ctrlColor = "Yellow"; ctrlMainColor = "DarkYellow"; tweakColor = "DarkGreen"
        ctrlColor = 'Primary'; ctrlMainColor = 'Secondary'; tweakColor = 'Tertiary'; ctrlGlobalColor = 'Global'
        ctrlNames = []
        ctrlSizes = []
        if self.haveIK == "Disabled":
            ctrlNames.append("Ctrl_FK_Hip")
            ctrlSizes.append(1.5 * self.gblScaleGuide[0])
            for x in range(1, (self.numberOfJnts + 1)):
                ctrlNames.append(("Ctrl_FK_Spine_"+str(x)))
                ctrlSizes.append(1.2 * self.gblScaleGuide[0])
            ctrlNames.append("Ctrl_FK_Chest")
            ctrlSizes.append(1.5 * self.gblScaleGuide[0])
            self.createCtrlsFK(names=ctrlNames, sizes=ctrlSizes, color=ctrlColor, jnts=chains[0])
            self.manageAttrCtrlsFK(ctrls=ctrlNames)
            self.adjustCtrlsFK(ctrls=ctrlNames)
            grpSpineCtrls, grpCtrlsFKConst = self.setHierarchyCtrlsFK(ctrls=ctrlNames)
            self.setRotOrderFK(ctrls=ctrlNames)
            rootCtrl = self.createRootCtrl(jnts=chains[0], color=ctrlGlobalColor)
        elif self.haveIK == "Enabled":
            for x in range(1, (self.numberOfJnts + 1)):
                ctrlNames.append(("Ctrl_FK_Spine_"+str(x)))
                ctrlSizes.append(1.5 * self.gblScaleGuide[0])
            self.createCtrlsFK(names=ctrlNames, sizes=ctrlSizes, color=ctrlMainColor, jnts=chains[0][1:(x+1)])
            self.manageAttrCtrlsFK(ctrls=ctrlNames)
            self.adjustCtrlsFK(ctrls=ctrlNames)
            grpSpineCtrls, grpCtrlsFKConst = self.setHierarchyCtrlsFK(ctrls=ctrlNames)
            self.setRotOrderFK(ctrls=ctrlNames)
            ctrlNames.append("Ctrl_IK_Hip")
            ctrlSizes.append(1 * self.gblScaleGuide[0])
            ctrlNames.append("Ctrl_IK_Chest")
            ctrlSizes.append(1 * self.gblScaleGuide[0])
            if self.haveBendIK == True:
                ctrlNames.append("Ctrl_IK_Spine_Bend")
                ctrlSizes.append(1 * self.gblScaleGuide[0])
            ctrlsIK = self.createCtrlsIK(jnts=chains[1], color=[ctrlColor, tweakColor], fkJnts=chains[0])
            rootCtrl = self.createRootCtrl(jnts=chains[1], color=ctrlGlobalColor)
            self.adjustctrlsIK(ctrls=ctrlsIK)
            allIKCtrls = []
            allIKCtrls.append(rootCtrl)
            allIKCtrls.extend(ctrlsIK)
            self.manageAttrCtrlsIK(ctrls=allIKCtrls)
            if self.haveBendIK == True: self.setupBendIK(ctrls=ctrlsIK)


        # Create Setup

        if self.haveIK == "Enabled":
            self.associateFK(jnts=chains[0][1:(self.numberOfJnts+1)], ctrls=ctrlNames[0:self.numberOfJnts])
            jntsCrv, ikSpine, crvSpine = self.associateIK(jnts=chains[1], ctrls=ctrlsIK)
            twistCtrls = []
            twistCtrls.append(rootCtrl)
            twistCtrls.extend(ctrlNames[self.numberOfJnts:(self.numberOfJnts + 2)])
            if self.haveBendIK == True: twistCtrls.append(ctrlNames[-1])
            print ("\nMy IK Ctrls = %s") %(twistCtrls)
            if self.haveTwistIK == True:
                self.createTwistIK(jnts=jntsCrv, ctrls=twistCtrls, ikHandle=ikSpine)
            if self.haveStretchIK == True:
                self.createStretchIK(crvIK=crvSpine, ctrlRoot=rootCtrl, jnts=chains[1])
        else:
            self.associateFK(jnts=chains[0], ctrls=ctrlNames)


        # Clean Up Component
        cmds.select(chains[0][0], r=True)
        if self.haveIK == "Enabled": grpFKJnts = cmds.group(n=("Grp_JntDrv_Spine_FKConst"))
        else: grpFKJnts = cmds.group(n=("Grp_JntBnd_Spine_FKConst"))
        cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], (grpFKJnts+".rotatePivot"), (grpFKJnts+".scalePivot"), rpr=True)
        if self.haveIK == "Enabled":
            cmds.select(chains[1][0], jntsCrv, r=True)
            grpIKJnts = cmds.group(n="Grp_JntBnd_Spine_IKConst")
            cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], (grpIKJnts+".rotatePivot"), (grpIKJnts+".scalePivot"), rpr=True)
            cmds.select(jntsCrv, r=True)
            grpIKCrvJnts = cmds.group(n="Grp_JntDrv_Spine_CrvJnts_IKConst")
            cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], (grpIKCrvJnts+".rotatePivot"), (grpIKCrvJnts+".scalePivot"), rpr=True)
            cmds.select(grpIKJnts, grpIKCrvJnts, r=True)
            grpJntsDONOTTOUCH = cmds.group(n="DO_NOT_TOUCH")
            cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], (grpJntsDONOTTOUCH+".rotatePivot"), (grpJntsDONOTTOUCH+".scalePivot"), rpr=True)
            cmds.setAttr((grpJntsDONOTTOUCH+".useOutlinerColor"), 1)
            cmds.setAttr((grpJntsDONOTTOUCH+".outlinerColorR"), 0.9372)
            cmds.setAttr((grpJntsDONOTTOUCH+".outlinerColorG"), 0.2823)
            cmds.setAttr((grpJntsDONOTTOUCH+".outlinerColorB"), 0.2117)
            cmds.select(grpFKJnts, grpJntsDONOTTOUCH, r=True)
            grpSpineJnts = cmds.group(n="Grp_JntBnd_Spine")
            cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], (grpSpineJnts+".rotatePivot"), (grpSpineJnts+".scalePivot"), rpr=True)
            grpCtrlsIKConst = cmds.group(n=("Grp_Ctrl_Spine_IKConst"), em=True)
            for c in ctrlsIK:
                cmds.parent(("Grp_"+str(c)), grpCtrlsIKConst)
            cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], (grpCtrlsIKConst+".rotatePivot"), (grpCtrlsIKConst+".scalePivot"), rpr=True)
            cmds.parent(grpCtrlsIKConst, grpSpineCtrls)
            # Connect Root Ctrl
            cmds.select(rootCtrl, grpFKJnts, r=True)
            const = cmds.parentConstraint(weight=1, mo=True)
            cmds.select(rootCtrl, grpIKJnts, r=True)
            const = cmds.parentConstraint(weight=1, mo=True)
            cmds.select(rootCtrl, grpIKCrvJnts, r=True)
            const = cmds.parentConstraint(weight=1, mo=True)
            cmds.select(rootCtrl, grpCtrlsFKConst, r=True)
            const = cmds.parentConstraint(weight=1, mo=True)
            cmds.select(rootCtrl, grpCtrlsIKConst, r=True)
            const = cmds.parentConstraint(weight=1, mo=True)
            # Hide Attrs
            attrs = []
            attrs.append(grpFKJnts); attrs.append(grpIKJnts); attrs.append(grpIKCrvJnts); attrs.append(grpCtrlsFKConst); attrs.append(grpCtrlsIKConst)
            attrs.append(grpJntsDONOTTOUCH); attrs.append(grpSpineCtrls); attrs.append(grpSpineJnts)
            for a in attrs:
                ctrl.Control(n=a, t="Lock and Hide", s=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])
            # Create Component hierarchy
            if self.setupFull == 1:
                cmds.parent(grpSpineJnts, "Grp_Sktn")
                cmds.parent(("Grp_"+str(rootCtrl)), "Grp_Ctrl")
                cmds.parent(grpSpineCtrls, "Grp_Ctrl")
                cmds.parent(ikSpine, "Grp_ikHdle")
                cmds.parent(crvSpine, "Grp_Xtra_ToHide")
            elif self.setupFull == 2:
                cmds.select(grpSpineJnts, grpSpineCtrls, ("Grp_"+str(rootCtrl)), ikSpine, crvSpine, r=True)
                grpSpine = cmds.group(n="Grp_HumanSpine")
        else:
            cmds.select(grpFKJnts, r=True)
            grpSpineJnts = cmds.group(n="Grp_JntBnd_Spine")
            cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], (grpSpineJnts+".rotatePivot"), (grpSpineJnts+".scalePivot"), rpr=True)
            # Connect Root Ctrl
            cmds.select(rootCtrl, grpFKJnts, r=True)
            const = cmds.parentConstraint(weight=1, mo=True)
            cmds.select(rootCtrl, grpCtrlsFKConst, r=True)
            const = cmds.parentConstraint(weight=1, mo=True)
            # Hide Attrs
            attrs = []
            attrs.append(grpFKJnts); attrs.append(grpCtrlsFKConst); attrs.append(grpSpineCtrls); attrs.append(grpSpineJnts)
            for a in attrs:
                ctrl.Control(n=a, t="Lock and Hide", s=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])
            # Create Component hierarchy
            if self.setupFull == 1:
                cmds.parent(grpSpineJnts, "Grp_Sktn")
                cmds.parent(("Grp_"+str(rootCtrl)), "Grp_Ctrl")
                cmds.parent(grpSpineCtrls, "Grp_Ctrl")
            elif self.setupFull == 2:
                cmds.select(grpSpineJnts, grpSpineCtrls, ("Grp_"+str(rootCtrl)), r=True)
                grpSpine = cmds.group(n="Grp_HumanSpine")

        # Return Features

        if self.haveIK == "Enabled":
            self.jntsBnd.extend(chains[1])
            self.jntsDrv.extend(chains[0])
            self.jntsDrv.extend(jntsCrv)
        elif self.haveRibbon == "Enabled":
            pass
        else: self.jntsBnd.extend(chains[0])

    def createJoints(self, jnts=[]):
        posSpines = []
        pos = [(self.posHip[0], self.posHip[1], self.posHip[2])]
        for x in range(1, (self.numberOfJnts + 1)):
            toExec = ("var = [(self.posSpine"+str(x)+"[0]), (self.posSpine"+str(x)+"[1]), (self.posSpine"+str(x)+"[2])]")
            exec(toExec)
            pos.append(var)
        var = [(self.posChest[0]), (self.posChest[1]), (self.posChest[2])]
        pos.append(var)
        if self.solverType == 1:
            distHipChest = [(self.posChest[0] - self.posHip[0]), (self.posChest[1] - self.posHip[1]), (self.posChest[2] - self.posHip[2])]
            percentDist = (100.0 / (self.numberOfIKJnts - 1)) / 100.0
            distJntToJnt = [(distHipChest[0] * percentDist), (distHipChest[1] * percentDist), (distHipChest[2] * percentDist)]
            for x in range(0, self.numberOfIKJnts):
                if x == 0: posIK = [(self.posHip[0]), (self.posHip[1]), (self.posHip[2])]
                else: posIK = [((distJntToJnt[0] * x) + self.posHip[0]), ((distJntToJnt[1] * x) + self.posHip[1]), ((distJntToJnt[2] * x) + self.posHip[2])]
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
        for x in range(0, (self.numberOfJnts + 1)):
            try:
                cmds.parent(jnts[x+1], jnts[x])
            except IndexError:
                cmds.warning(("Index "+str(x)+" ignored"))
        # print ("Chain 1 = %s") %(jnts[0:(self.numberOfJnts + 2)])
        chains.append(jnts[0:(self.numberOfJnts + 2)])
        if self.haveIK == "Enabled":
            jntsFK = (self.numberOfJnts + 2)
            totalJnts = self.numberOfIKJnts + self.numberOfJnts
            for x in range(jntsFK, (totalJnts + 1)):
                try:
                    cmds.parent(jnts[x+1], jnts[x])
                except IndexError:
                    cmds.warning(("Index "+str(x)+" ignored"))
                # print ("Parent "+str(x+1)+", "+str(x))
            # print ("\nChain 2 = %s") %(jnts[jntsFK:(totalJnts+2)])
            chains.append(jnts[jntsFK:(totalJnts+2)])
        return chains

    def orientJnts(self, chains=[]):
        count = len(chains)
        for x in range(0, count):
            cmds.select(chains[x][0])
            cmds.joint(edit=True, oj="xyz", sao="zup", ch=True, zso=True) # XYZ
            cmds.select(chains[x][-1])
            cmds.joint(edit=True, oj="none", zso=True)

    def setRotOrderJnts(self, chains=[]):
        for c in chains:
            for jnt in c:
                cmds.setAttr((jnt+".rotateOrder"), 3) # XZY

    def createCtrlsFK(self, names=[], sizes=[], color="", jnts=[]):
        x = 0
        for name in names:
            ctrl.Control(n=name, t="Circle", s=sizes[x], c=color)
            grp = cmds.group(n=("Grp_"+name))
            cmds.select(jnts[x], r=True)
            cmds.select(grp, add=True)
            const = cmds.parentConstraint(weight=1)
            cmds.select(const, r=True)
            cmds.Delete()
            x += 1

    def manageAttrCtrlsFK(self, ctrls=[]):
        for c in ctrls:
            ctrl.Control(n=c, t="Lock and Hide", s=["tx", "ty", "tz", "sx", "sy", "sz"])

    def adjustCtrlsFK(self, ctrls=[]):
        for c in ctrls:
            cmds.select((c+".cv[0:7]"), r=True)
            cmds.rotate(0, 0, 90, r=True, os=True)

    def setHierarchyCtrlsFK(self, ctrls=[]):
        for x in range(0, (len(ctrls) - 1)):
            try:
                cmds.parent(("Grp_"+ctrls[x+1]), ctrls[x])
            except IndexError:
                cmds.warning(("Index "+str(x)+" ignored"))
        cmds.select(("Grp_"+ctrls[0]), r=True)
        grpCtrlsFKConst = cmds.group(n=("Grp_Ctrl_Spine_FKConst"))
        cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], (grpCtrlsFKConst+".rotatePivot"), (grpCtrlsFKConst+".scalePivot"), rpr=True)
        cmds.select(grpCtrlsFKConst, r=True)
        grpCtrlsFK = cmds.group(n=("Grp_Ctrl_Spine"))
        cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], (grpCtrlsFK+".rotatePivot"), (grpCtrlsFK+".scalePivot"), rpr=True)
        return grpCtrlsFK, grpCtrlsFKConst

    def setRotOrderFK(self, ctrls=[]):
        for ctrl in ctrls:
            cmds.setAttr((ctrl+".rotateOrder"), 3) # XZY

    def associateFK(self, jnts=[], ctrls=[]):
        for x in range(0, len(ctrls)):
            cmds.connectAttr((ctrls[x]+".r"), (jnts[x]+".r"))

    def createCtrlsIK(self, jnts=[], color=[], fkJnts=[]):
        ctrlsIK = []
        c = ctrl.Control(n=("Ctrl_IK_Hip"), t="Hip", s=(1.5 * self.gblScaleGuide[0]), c=color[0])
        ctrlsIK.append(c)
        grpOff = cmds.group(n=("Grp_"+str(c)))
        cmds.select(jnts[0], grpOff, r=True)
        const = cmds.parentConstraint(weight=1)
        cmds.select(const, r=True)
        cmds.Delete()
        cmds.select(fkJnts[0], grpOff, r=True)
        cmds.parentConstraint(weight=1, mo=True)
        c = ctrl.Control(n=("Ctrl_IK_Chest"), t="Chest", s=(2 * self.gblScaleGuide[0]), c=color[0])
        ctrlsIK.append(c)
        grpOff = cmds.group(n=("Grp_"+str(c)))
        cmds.select(jnts[-1], grpOff, r=True)
        const = cmds.parentConstraint(weight=1)
        cmds.select(const, r=True)
        cmds.Delete()
        cmds.select(fkJnts[-1], grpOff, r=True)
        cmds.parentConstraint(weight=1, mo=True)
        if self.haveBendIK == True:
            dist = [(self.posChest[0] - self.posHip[0]), (self.posChest[1] - self.posHip[1]), (self.posChest[2] - self.posHip[2])]
            pos = [(dist[0] * 0.5), (dist[1] * 0.5), (dist[2] * 0.5)]
            finalPos = [(self.posHip[0] + pos[0]), (self.posHip[1] + pos[1]), (self.posHip[2] + pos[2])]
            cmds.select(cl=True)
            loc = cmds.joint(p=(finalPos[0], finalPos[1], finalPos[2]))
            cmds.select(cl=True)
            c = ctrl.Control(n=("Ctrl_IK_Spine_Bend"), t="Gear Smooth", s=(1.3 * self.gblScaleGuide[0]), c=color[1])
            grp = cmds.group(n=("Grp_"+str(c)))
            cmds.move(0, 0, 0, (grp+".rotatePivot"), (grp+".scalePivot"), rpr=True)
            cmds.select(loc, grp, r=True)
            pntConst = cmds.pointConstraint(weight=1)
            cmds.select(jnts[0], grp, r=True)
            oriConst = cmds.orientConstraint(weight=1)
            ctrlsIK.append(c)
            cmds.select(pntConst, oriConst, loc, r=True)
            cmds.Delete()
        return ctrlsIK

    def adjustctrlsIK(self, ctrls=[]):
        for ctrl in ctrls:
            cmds.select((str(ctrl)+".cv[*]"), r=True)
            cmds.rotate(-90, -90, 0, r=True, os=True)
            cmds.select(cl=True)

    def manageAttrCtrlsIK(self, ctrls=[]):
        for c in ctrls:
            ctrl.Control(n=str(c), t="Lock and Hide", s=["sx", "sy", "sz"])
        rootAttrs = 0;
        # if self.haveTwistIK == True: rootAttrs += 1
        if self.haveStretchIK == True: rootAttrs += 1
        if self.haveStretchMultIK == True: rootAttrs += 1
        if self.haveClampStretchIK == True: rootAttrs += 2
        if self.haveSquashIK == True: rootAttrs += 1
        if self.haveSquashMultIK == True: rootAttrs += 1
        # Add Attrs
        if self.haveBendIK == True:
            cmds.addAttr(("Grp_"+str(ctrls[3])+"|"+str(ctrls[3])),
                ln="SPINE", nn="___________________ SPINE", at="enum", en="__________:")
            cmds.setAttr(("Grp_"+str(ctrls[3])+"|"+str(ctrls[3])+".SPINE"),
                edit=True, channelBox=True)
            cmds.addAttr(("Grp_"+str(ctrls[3])+"|"+str(ctrls[3])),
                ln="FollowSpine", at="bool")
            cmds.setAttr(("Grp_"+str(ctrls[3])+"|"+str(ctrls[3])+".FollowSpine"),
                edit=True, k=True)
        if self.haveTwistIK == True or self.haveStretchIK == True:
            cmds.addAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])), ln="SPINE", nn="___________________ SPINE", at="enum", en="__________:")
            cmds.setAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])+".SPINE"), edit=True, channelBox=True)
            cmds.addAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])),
                ln="SPINE", nn="___________________ SPINE", at="enum", en="__________:")
            cmds.setAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])+".SPINE"), edit=True, channelBox=True)
            cmds.addAttr(("|Grp_"+str(ctrls[2])+"|"+str(ctrls[2])),
                ln="SPINE", nn="___________________ SPINE", at="enum", en="__________:")
            cmds.setAttr(("|Grp_"+str(ctrls[2])+"|"+str(ctrls[2])+".SPINE"), edit=True, channelBox=True)
            if not rootAttrs == 0:
                cmds.addAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])), ln="RootSpineSettings", at="compound", nc=rootAttrs)
        if self.haveTwistIK == True:
            # Root | Hip | Chest | Bend
            # cmds.addAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])), ln="AutoTwist", at="enum", en="Off:On:", p="RootSpineSettings")
            cmds.addAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])), ln="HipTwistMult", at="double", dv=0)
            cmds.addAttr(("|Grp_"+str(ctrls[2])+"|"+str(ctrls[2])), ln="ChestTwistMult", at="double", dv=0)
        if self.haveStretchIK == True:
            cmds.addAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])), ln="SpineStretch", at="bool", p="RootSpineSettings")
        if self.haveStretchMultIK == True:
            cmds.addAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])), ln="SpineStretchMult", at="double", min=0.01, dv=1, p="RootSpineSettings")
        if self.haveClampStretchIK == True:
            cmds.addAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])), ln="ClampStretch", at="bool", p="RootSpineSettings")
            cmds.addAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])), ln="ClampValue", at="double", min=1, dv=1.5, p="RootSpineSettings")
        if self.haveSquashIK == True:
            cmds.addAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])), ln="SpineSquash", at="bool", p="RootSpineSettings")
        if self.haveSquashMultIK == True:
            cmds.addAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])), ln="SpineSquashMult", at="double", min=0.01, dv=1, p="RootSpineSettings")
        # Set Attrs
        if self.haveTwistIK == True:
            # cmds.setAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])+".AutoTwist"), edit=True, k=True)
            cmds.setAttr(("|Grp_"+str(ctrls[1])+"|"+str(ctrls[1])+".HipTwistMult"), edit=True, k=True)
            cmds.setAttr(("|Grp_"+str(ctrls[2])+"|"+str(ctrls[2])+".ChestTwistMult"), edit=True, k=True)
        if self.haveStretchIK == True:
            cmds.setAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])+".SpineStretch"), edit=True, k=True)
        if self.haveStretchMultIK == True:
            cmds.setAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])+".SpineStretchMult"), edit=True, k=True)
        if self.haveClampStretchIK == True:
            cmds.setAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])+".ClampStretch"), edit=True, k=True)
            cmds.setAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])+".ClampValue"), edit=True, k=True)
        if self.haveSquashIK == True:
            cmds.setAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])+".SpineSquash"), edit=True, k=True)
        if self.haveSquashMultIK == True:
            cmds.setAttr(("|Grp_"+str(ctrls[0])+"|"+str(ctrls[0])+".SpineSquashMult"), edit=True, k=True)

    def associateIK(self, jnts=[], ctrls=[]):
        jntsCrv = []
        ikSpine, effSpine, crvSpine = cmds.ikHandle(n="ikHdle_Spine", sol="ikSplineSolver", sj=jnts[0], ee=jnts[-1])
        cmds.select(jnts[0], r=True)
        jntHip = cmds.duplicate(rr=True)
        jntHipChildren = cmds.listRelatives(ad=True, f=True)
        cmds.select(jntHipChildren[0], r=True)
        jntChest = cmds.duplicate(rr=True)
        cmds.parent(w=True)
        for x in range(0, len(jntHipChildren)):
            cmds.select(jntHipChildren[x], r=True)
            cmds.Delete()
        if self.haveBendIK == True:
            cmds.select(cl=True)
            jntBend = cmds.joint()
            cmds.select("Ctrl_IK_Spine_Bend", jntBend, r=True)
            pntConst = cmds.pointConstraint(weight=1)
            cmds.select(pntConst, r=True)
            cmds.Delete()
            cmds.parent(jntBend, jntHip)
            cmds.select(jntBend, r=True)
            cmds.joint(edit=True, oj="none", zso=True)
            cmds.parent(w=True)
        cmds.rename(jntHip, "JntDrv_Crv_IK_Hip")
        cmds.rename(jntChest, "JntDrv_Crv_IK_Chest")
        if self.haveBendIK == True:
            cmds.rename(jntBend, "JntDrv_Crv_IK_Spine_Bend")
            jntsCrv.append("JntDrv_Crv_IK_Spine_Bend")
        jntsCrv.append("JntDrv_Crv_IK_Hip")
        jntsCrv.append("JntDrv_Crv_IK_Chest")
        cmds.skinCluster(jntsCrv, crvSpine, tsb=True, sm=0, nw=1, mi=len(jntsCrv), rui=True, omi=True, dr=4.0)
        cmds.rename(effSpine, "Eff_Spine")
        cmds.rename(crvSpine, "Crv_Spine")
        for jnt in jntsCrv:
            cmds.setAttr((jnt+".rotateOrder"), 2) # ZXY
        for ctrl in ctrls:
            cmds.setAttr((str(ctrl)+".rotateOrder"), 2) # ZXY
         # Hip | Chest | Bend
        cmds.select(str(ctrls[0]), jntsCrv[-2], r=True)
        cmds.parentConstraint(weight=1)
        cmds.select(str(ctrls[1]), jntsCrv[-1], r=True)
        cmds.parentConstraint(weight=1)
        if self.haveBendIK == True:
            cmds.select(str(ctrls[2]), jntsCrv[0], r=True)
            cmds.parentConstraint(weight=1)
        return jntsCrv, ikSpine, "Crv_Spine"

    def createRootCtrl(self, jnts=[], color=""):
        c = ctrl.Control(n=("Ctrl_Root"), t="Root", s=(1.7 * self.gblScaleGuide[0]), c=color)
        grp = cmds.group(n=("Grp_"+str(c)))
        cmds.move(self.posHip[0], self.posHip[1], self.posHip[2], r=True)
        cmds.setAttr((str(c)+".rotateOrder"), 2) # ZXY
        return c

    def setupBendIK(self, ctrls=[]):
        # CTRLS = Hip | Chest | Bend
        cmds.select(str(ctrls[2]), r=True)
        grpBendOff = cmds.listRelatives(p=True)
        cmds.select(str(ctrls[0]), str(ctrls[1]), grpBendOff, r=True)
        const = cmds.parentConstraint(weight=1, mo=True)
        bcBendFollow = cmds.shadingNode("blendColors", asUtility=True, n="Bc_Spine_Bend_Follow")
        cmds.connectAttr((str(ctrls[2])+".FollowSpine"), (bcBendFollow+".blender"))
        cmds.connectAttr((bcBendFollow+".outputR"), (str(const[0])+"."+str(ctrls[0])+"W0"))
        cmds.connectAttr((bcBendFollow+".outputR"), (str(const[0])+"."+str(ctrls[1])+"W1"))
        cmds.setAttr(((str(ctrls[2])+".FollowSpine")), True)

    def createTwistIK(self, jnts=[], ctrls=[], ikHandle=""):
        # CTRLS: Root | Hip | Chest | Bend
        # JNTS: Bend | Hip | Chest
        # mdAutoTwistChest = cmds.shadingNode("multiplyDivide", asUtility=True, n="Md_Spine_Chest_AutoTwist")
        # mdAutoTwistHip = cmds.shadingNode("multiplyDivide", asUtility=True, n="Md_Spine_Hip_AutoTwist")
        pmaTwistOffsetChest = cmds.shadingNode("plusMinusAverage", asUtility=True, n="Pma_Spine_Chest_TwistOffset")
        pmaTwistOffsetHip = cmds.shadingNode("plusMinusAverage", asUtility=True, n="Pma_Spine_Hip_TwistOffset")
        pmaCounterTwist = cmds.shadingNode("plusMinusAverage", asUtility=True, n="Pma_Spine_CounterTwist")
        # cmds.connectAttr((str(ctrls[2])+".rx"), (mdAutoTwistChest+".input1X"))
        # cmds.connectAttr((str(ctrls[0])+".AutoTwist"), (mdAutoTwistChest+".input2X"))
        cmds.connectAttr((str(ctrls[2])+".rx"), (pmaTwistOffsetChest+".input1D[0]"))
        cmds.connectAttr((str(ctrls[2])+".ChestTwistMult"), (pmaTwistOffsetChest+".input1D[1]"))
        # cmds.connectAttr((str(ctrls[0])+".AutoTwist"), (mdAutoTwistHip+".input1X"))
        cmds.connectAttr((str(ctrls[1])+".rx"), (pmaTwistOffsetHip+".input1D[0]"))
        cmds.connectAttr((str(ctrls[1])+".HipTwistMult"), (pmaTwistOffsetHip+".input1D[1]"))
        # cmds.connectAttr((pmaTwistOffsetHip+".output1D"), (mdAutoTwistHip+".input2X"))
        cmds.connectAttr((pmaTwistOffsetHip+".output1D"), (ikHandle+".roll"))
        cmds.connectAttr((pmaTwistOffsetChest+".output1D"), (pmaCounterTwist+".input1D[0]"))
        cmds.connectAttr((pmaTwistOffsetHip+".output1D"), (pmaCounterTwist+".input1D[1]"))
        cmds.setAttr((pmaCounterTwist+".operation"), 2)
        cmds.connectAttr((pmaCounterTwist+".output1D"), (ikHandle+".twist"))
        # cmds.setAttr((str(ctrls[0])+".AutoTwist"), True)

    def createStretchIK(self, crvIK="", ctrlRoot="", jnts=[]):
        cmds.select(crvIK, r=True)
        crvIKShape = cmds.listRelatives(s=True)
        info = cmds.shadingNode("curveInfo", asUtility=True, n="Cinf_Spine_Info")
        mdStretch = cmds.shadingNode("multiplyDivide", asUtility=True, n="Md_Spine_Stretch_Div")
        bcStretchSwitch = cmds.shadingNode("blendColors", asUtility=True, n="Bc_Spine_Stretch_Switch")
        if self.gblScale == True:
            mdGblScaleStretch = cmds.shadingNode("multiplyDivide", asUtility=True, n="Md_Spine_Stretch_GblScale_Div")
        if self.haveStretchMultIK == True:
            mdStretchMult = cmds.shadingNode("multiplyDivide", asUtility=True, n="Md_Spine_StretchMult_Mult")
        if self.haveClampStretchIK == True:
            cmpClampStretch = cmds.shadingNode("clamp", asUtility=True, n="Cmp_Spine_Stretch")
            bcClampStretchSwitch = cmds.shadingNode("blendColors", asUtility=True, n="Bc_Spine_ClampStretch_Switch")
        if self.haveSquashIK == True:
            mdSqrtStretch = cmds.shadingNode("multiplyDivide", asUtility=True, n="Md_Spine_SqrtStretch_Pow")
            mdSquash = cmds.shadingNode("multiplyDivide", asUtility=True, n="Md_Spine_Squash_Div")
            bcSquashSwitch = cmds.shadingNode("blendColors", asUtility=True, n="Bc_Spine_Squash_Switch")
        if self.haveSquashMultIK == True:
            mdSquashMult = cmds.shadingNode("multiplyDivide", asUtility=True, n="Md_Spine_SquashMult_Mult")
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
            cmds.connectAttr((str(ctrlRoot)+".SpineStretchMult"), (mdStretchMult+".input2X"))
            cmds.connectAttr((mdStretchMult+".outputX"), (bcStretchSwitch+".color1R"))
            cmds.setAttr((bcStretchSwitch+".color2R"), 1)
            cmds.connectAttr((str(ctrlRoot)+".SpineStretch"), (bcStretchSwitch+".blender"))
        else:
            cmds.connectAttr((mdStretch+".outputX"), (bcStretchSwitch+".color1R"))
            cmds.setAttr((bcStretchSwitch+".color2R"), 1)
            cmds.connectAttr((str(ctrlRoot)+".SpineStretch"), (bcStretchSwitch+".blender"))
        if self.haveClampStretchIK == True:
            cmds.connectAttr((bcStretchSwitch+".outputR"), (cmpClampStretch+".inputR"))
            cmds.connectAttr((str(ctrlRoot)+".ClampValue"), (cmpClampStretch+".maxR"))
            cmds.connectAttr((cmpClampStretch+".outputR"), (bcClampStretchSwitch+".color1R"))
            cmds.connectAttr((bcStretchSwitch+".outputR"), (bcClampStretchSwitch+".color2R"))
            cmds.connectAttr((str(ctrlRoot)+".ClampStretch"), (bcClampStretchSwitch+".blender"))
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
                cmds.connectAttr((str(ctrlRoot)+".SpineSquashMult"), (mdSquashMult+".input2X"))
                cmds.connectAttr((mdSquashMult+".outputX"), (bcSquashSwitch+".color1R"))
                cmds.setAttr((bcSquashSwitch+".color2R"), 1)
                cmds.connectAttr((str(ctrlRoot)+".SpineSquash"), (bcSquashSwitch+".blender"))
            else:
                cmds.connectAttr((mdSquash+".outputX"), (bcSquashSwitch+".color1R"))
                cmds.setAttr((bcSquashSwitch+".color2R"), 1)
                cmds.connectAttr((str(ctrlRoot)+".SpineSquash"), (bcSquashSwitch+".blender"))
            for x in range(0, (self.numberOfIKJnts - 1)):
                cmds.connectAttr((bcSquashSwitch+".outputR"), (jnts[x]+".sy"))
                cmds.connectAttr((bcSquashSwitch+".outputR"), (jnts[x]+".sz"))
