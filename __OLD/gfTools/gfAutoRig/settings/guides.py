import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaRender as omr
from functools import partial

from gfTools.__OLD.gfTools.gfAutoRig.settings import controls as ctrls
from gfTools.__OLD.gfTools.gfAutoRig.components import humanLegs as HLegs
from gfTools.__OLD.gfTools.gfAutoRig.components import humanArms as HArms
reload(ctrls); reload(HLegs); reload(HArms)


class loadGuides(object):

    def __init__(self):
        # Verify components
        self.outlDark = [0.4, 0.4, 0.4]
        self.outlDontTouch = [0.9372, 0.2823, 0.2117]
        self.outlUnparent = [0.95686, 0.81569, 0.24706]
        self.outlParent = [0.42941, 0.82745, 0.38627]
        # ---------------------------------------------------------------------------------------------------------
        # Variables
        # ---------------------------------------------------------------------------------------------------------
        # Human Spine
        self.gdRoot            = [0, 100, 0];        self.gdHip             = [0, 92, 0];        self.gdSpine1          = [0, 103.5, 0]
        self.gdSpine2          = [0, 115, 0];        self.gdSpine3          = [0, 126.5, 0];     self.gdChest           = [0, 138, 0]
        # Human Legs
        self.gdLThigh          = [10, 90, 0];        self.gdLShin           = [10, 50, 0];       self.gdLAnkle          = [10, 8, 0]
        self.gdLToe            = [10, 3, 12];        self.gdLLegEnd         = [10, 3, 20];       self.gdRThigh          = [-10, 90, 0]
        self.gdRShin           = [-10, 50, 0];       self.gdRAnkle          = [-10, 8, 0];       self.gdRToe            = [-10, 3, 12]
        self.gdRLegEnd         = [-10, 3, 20];
        if cmds.objExists("gfARGuides:Ctrl_L_Ankle"):
            self.pos = cmds.xform("gfARGuides:Ctrl_L_Ankle", q=True, ws=True, rp=True)
            self.gdLTipHeel = [self.pos[0], 0, (self.pos[2] - 7)]
        if cmds.objExists("gfARGuides:Ctrl_L_Toe"):
            self.pos = cmds.xform("gfARGuides:Ctrl_L_Toe", q=True, ws=True, rp=True)
            self.gdLInFoot = [(self.pos[0] - 7), 0, self.pos[2]]
            self.gdLOutFoot = [(self.pos[0] + 7), 0, self.pos[2]]
        if cmds.objExists("gfARGuides:Ctrl_L_LegEnd"):
            self.pos = cmds.xform("gfARGuides:Ctrl_L_LegEnd", q=True, ws=True, rp=True)
            self.gdLTipFoot = [self.pos[0], 0, (self.pos[2] + 5)]
        if cmds.objExists("gfARGuides:Ctrl_R_Ankle"):
            self.pos = cmds.xform("gfARGuides:Ctrl_R_Ankle", q=True, ws=True, rp=True)
            self.gdRTipHeel = [self.pos[0], 0, (self.pos[2] - 7)]
        if cmds.objExists("gfARGuides:Ctrl_R_Toe"):
            self.pos = cmds.xform("gfARGuides:Ctrl_R_Toe", q=True, ws=True, rp=True)
            self.gdRInFoot = [(self.pos[0] + 7), 0, self.pos[2]]
            self.gdROutFoot = [(self.pos[0] - 7), 0, self.pos[2]]
        if cmds.objExists("gfARGuides:Ctrl_R_LegEnd"):
            self.pos = cmds.xform("gfARGuides:Ctrl_R_LegEnd", q=True, ws=True, rp=True)
            self.gdRTipFoot = [self.pos[0], 0, (self.pos[2] + 5)]
        # Human Arms
        self.gdLClavicle       = [10, 148, 0];       self.gdLUpperArm       = [22, 148, 0];       self.gdLForearm        = [42, 148, 0]
        self.gdLWrist          = [69, 148, 0];       self.gdLPalm           = [79.2, 148, 0];     self.gdLArmEnd         = [86.2, 148, 0]
        self.gdLThumbMeta      = [72.8, 148, 3.5];   self.gdLThumbProx      = [76.5, 148, 4];     self.gdLThumbDist      = [78.7, 148, 4.55]
        self.gdLThumbEnd       = [80.2, 148, 4.9];   self.gdLIndexMeta      = [72, 148, 2];       self.gdLIndexProx      = [79, 148, 2]
        self.gdLIndexMid       = [82, 148, 2];       self.gdLIndexDist      = [84.3, 148, 2];     self.gdLIndexEnd       = [86, 148, 2]
        self.gdLMiddleMeta     = [72, 148, 0.5];     self.gdLMiddleProx     = [79.2, 148, 0.5];   self.gdLMiddleMid      = [82.2, 148, 0.5]
        self.gdLMiddleDist     = [84.5, 148, 0.5];   self.gdLMiddleEnd      = [86.2, 148, 0.5];   self.gdLRingMeta       = [72, 148, -1]
        self.gdLRingProx       = [78.5, 148, -1];    self.gdLRingMid        = [81.5, 148, -1];    self.gdLRingDist       = [83.8, 148, -1]
        self.gdLRingEnd        = [85.5, 148, -1];    self.gdLPinkyMeta      = [72, 148, -2.5];    self.gdLPinkyProx      = [78, 148, -2.5]
        self.gdLPinkyMid       = [81, 148, -2.5];    self.gdLPinkyDist      = [83.3, 148, -2.5];  self.gdLPinkyEnd       = [85, 148, -2.5]
        self.gdRClavicle       = [-10, 148, 0];      self.gdRUpperArm       = [-22, 148, 0];      self.gdRForearm        = [-42, 148, 0]
        self.gdRWrist          = [-69, 148, 0];      self.gdRPalm           = [-79.2, 148, 0];    self.gdRArmEnd         = [-86.2, 148, 0]
        self.gdRThumbMeta      = [-72.8, 148, 3.5];  self.gdRThumbProx      = [-76.5, 148, 4];    self.gdRThumbDist      = [-78.7, 148, 4.55]
        self.gdRThumbEnd       = [-80.2, 148, 4.9];  self.gdRIndexMeta      = [-72, 148, 2];      self.gdRIndexProx      = [-79, 148, 2]
        self.gdRIndexMid       = [-82, 148, 2];      self.gdRIndexDist      = [-84.3, 148, 2];    self.gdRIndexEnd       = [-86, 148, 2]
        self.gdRMiddleMeta     = [-72, 148, 0.5];    self.gdRMiddleProx     = [-79.2, 148, 0.5];  self.gdRMiddleMid      = [-82.2, 148, 0.5]
        self.gdRMiddleDist     = [-84.5, 148, 0.5];  self.gdRMiddleEnd      = [-86.2, 148, 0.5];  self.gdRRingMeta       = [-72, 148, -1]
        self.gdRRingProx       = [-78.5, 148, -1];   self.gdRRingMid        = [-81.5, 148, -1];   self.gdRRingDist       = [-83.8, 148, -1]
        self.gdRRingEnd        = [-85.5, 148, -1];   self.gdRPinkyMeta      = [-72, 148, -2.5];   self.gdRPinkyProx      = [-78, 148, -2.5]
        self.gdRPinkyMid       = [-81, 148, -2.5];   self.gdRPinkyDist      = [-83.3, 148, -2.5]; self.gdRPinkyEnd       = [-85, 148, -2.5]
        # Human Heads
        self.gdNeck            = [0, 154, 0];        self.gdHead            = [0, 161, 0];       self.gdJaw             = [0, 164, 2]
        self.gdJawPivot        = [0, 160.5, 6];      self.gdJawEnd          = [0, 160.5, 12.5];  self.gdHeadEnd         = [0, 175, 0]
        # ---------------------------------------------------------------------------------------------------------
        # INIT
        # ---------------------------------------------------------------------------------------------------------
        # Verify components
        # self._setNamespace("End")

    def _setNamespace(self, method, move=False):
        if method == "Start":
            if cmds.namespace(ex="gfARGuides"):
                cmds.namespace(set="gfARGuides")
            else:
                cmds.namespace(add="gfARGuides")
                cmds.namespace(set="gfARGuides")
        elif method == "End":
            cmds.namespace(set=":")
        elif method == "Delete":
            if cmds.namespace(ex="gfARGuides"):
                cmds.namespace(set=":")
                cmds.namespace(mv=("gfARGuides", ":"))
                cmds.namespace(rm="gfARGuides")
        elif method == "Move":
            for m in move:
                cmds.rename(m, ("gfARGuides:"+m))

    def _SetHierarchy(self):
        self._setNamespace("Start")
        if cmds.objExists("Grp_Guides"):
            cmds.select("Grp_Guides", r=True)
            cmds.Delete()
        mainNode = cmds.group(em=True)
        componentsNode = cmds.group(em=True, p=mainNode)
        notTouchNode = cmds.group(em=True, p=mainNode)
        globalNode = cmds.group(em=True, p=notTouchNode)
        clusterNode = cmds.group(em=True, p=notTouchNode)
        volumeNode = cmds.group(em=True, p=notTouchNode)
        cmds.rename(mainNode, "Grp_Guides")
        cmds.rename(componentsNode, "Grp_Components")
        cmds.rename(globalNode, "Grp_Global")
        cmds.rename(notTouchNode, "DO_NOT_TOUCH")
        cmds.rename(clusterNode, "Grp_Cls")
        cmds.rename(volumeNode, "Grp_Volume")
        cmds.setAttr("gfARGuides:Grp_Guides.useOutlinerColor", 1)
        cmds.setAttr("gfARGuides:Grp_Guides.outlinerColorR", self.outlDark[0])
        cmds.setAttr("gfARGuides:Grp_Guides.outlinerColorG", self.outlDark[1])
        cmds.setAttr("gfARGuides:Grp_Guides.outlinerColorB", self.outlDark[2])
        cmds.setAttr("gfARGuides:Grp_Guides|gfARGuides:DO_NOT_TOUCH.useOutlinerColor", 1)
        cmds.setAttr("gfARGuides:Grp_Guides|gfARGuides:DO_NOT_TOUCH.outlinerColorR", self.outlDontTouch[0])
        cmds.setAttr("gfARGuides:Grp_Guides|gfARGuides:DO_NOT_TOUCH.outlinerColorG", self.outlDontTouch[1])
        cmds.setAttr("gfARGuides:Grp_Guides|gfARGuides:DO_NOT_TOUCH.outlinerColorB", self.outlDontTouch[2])
        cmds.setAttr("gfARGuides:Grp_Guides|gfARGuides:DO_NOT_TOUCH|gfARGuides:Grp_Global.useOutlinerColor", 1)
        cmds.setAttr("gfARGuides:Grp_Guides|gfARGuides:DO_NOT_TOUCH|gfARGuides:Grp_Global.outlinerColorR", self.outlParent[0])
        cmds.setAttr("gfARGuides:Grp_Guides|gfARGuides:DO_NOT_TOUCH|gfARGuides:Grp_Global.outlinerColorG", self.outlParent[1])
        cmds.setAttr("gfARGuides:Grp_Guides|gfARGuides:DO_NOT_TOUCH|gfARGuides:Grp_Global.outlinerColorB", self.outlParent[2])
        cmds.select(cl=True)
        ctrls.Control(n="Ctrl_Global", t="Gear", s=3, c="Yellow")
        cmds.addAttr("gfARGuides:|Ctrl_Global", ln="GlobalScale", at="double", min=0, dv=1)
        cmds.setAttr("gfARGuides:|Ctrl_Global.GlobalScale", edit=True, channelBox=True)
        cmds.connectAttr("gfARGuides:|Ctrl_Global.t", "gfARGuides:Grp_Guides|gfARGuides:Grp_Components.t", f=True)
        cmds.connectAttr("gfARGuides:|Ctrl_Global.r", "gfARGuides:Grp_Guides|gfARGuides:Grp_Components.r", f=True)
        cmds.connectAttr("gfARGuides:|Ctrl_Global.s", "gfARGuides:Grp_Guides|gfARGuides:Grp_Components.s", f=True)
        cmds.setAttr("gfARGuides:|Ctrl_Global.v", lock=True, keyable=False, channelBox=False)
        cmds.cluster(n=("Cls_Ctrl_Global_Scale"))
        cmds.setAttr("gfARGuides:Cls_Ctrl_Global_ScaleHandle.v", False)
        cmds.setAttr("gfARGuides:|Ctrl_Global.v", lock=True, keyable=False, channelBox=False)
        cmds.parent("gfARGuides:|Ctrl_Global", "gfARGuides:Grp_Guides|gfARGuides:DO_NOT_TOUCH|gfARGuides:Grp_Global")
        cmds.parent("gfARGuides:|Cls_Ctrl_Global_ScaleHandle", "gfARGuides:Grp_Guides|gfARGuides:DO_NOT_TOUCH|gfARGuides:Grp_Cls")
        cmds.select(cl=True)
        cmds.connectControl("fltGblCtrlScaMFeat", "gfARGuides:Cls_Ctrl_Global_ScaleHandle.sx", "gfARGuides:Cls_Ctrl_Global_ScaleHandle.sy", "gfARGuides:Cls_Ctrl_Global_ScaleHandle.sz")
        cmds.connectControl("fltGblCtrlTxMFeat", "gfARGuides:Cls_Ctrl_Global_ScaleHandle.tx")
        cmds.connectControl("fltGblCtrlTzMFeat", "gfARGuides:Cls_Ctrl_Global_ScaleHandle.tz")
        cmds.rowLayout("layGblCtrlScaMFeat", edit=True, en=True)
        cmds.rowLayout("layGblCtrlTxMFeat", edit=True, en=True)
        cmds.rowLayout("layGblCtrlTzMFeat", edit=True, en=True)
        if not cmds.objExists('gfARGuides:Mtl_Guides'):
            sh = cmds.shadingNode("lambert", asShader=True)
            sg = cmds.sets(r=True, nss=True, em=True, n=("lambert"+sh[-1]+"SG"))
            cmds.connectAttr((sh+".outColor"), (sg+".surfaceShader"))
            cmds.setAttr((sh+".incandescenceR"), 1)
            cmds.setAttr((sh+".incandescenceG"), 1)
            cmds.setAttr((sh+".incandescenceB"), 1)
            cmds.rename(sh, "Mtl_Guides")
            cmds.rename(sg, "Mtl_GuidesSG")
        self._setNamespace("End")

    def _DeleteHierarchy(self):
        cmds.select("gfARGuides:Grp_Guides", r=True)
        if cmds.objExists("gfARGuides:Mtl_Guides") and cmds.objExists("gfARGuides:Mtl_GuidesSG"):
            cmds.select("gfARGuides:Mtl_Guides", add=True)
            cmds.select("gfARGuides:Mtl_GuidesSG", add=True, ne=True)
        cmds.Delete()
        self._setNamespace("Delete")
        cmds.rowLayout("layGblCtrlScaMFeat", edit=True, en=False)
        cmds.rowLayout("layGblCtrlTxMFeat", edit=True, en=False)
        cmds.rowLayout("layGblCtrlTzMFeat", edit=True, en=False)

    def _GuidesColors(self):
        pass

    def _createCtrl(self, n, t, s=2):
        ctrl = cmds.sphere(p=(0, 0, 0), ax=(0, 1, 0), ssw=0, esw=360, r=1, d=3, ut=0, tol=0.01, s=4, nsp=2)
        cmds.setAttr((ctrl[0]+".sx"), s)
        cmds.setAttr((ctrl[0]+".sy"), s)
        cmds.setAttr((ctrl[0]+".sz"), s)
        cmds.move(t[0], t[1], t[2], r=True)
        cmds.DeleteHistory()
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.rename(ctrl[0], ("Ctrl_"+str(n)))
        cmds.select(cl=True)
        return ("gfARGuides:Ctrl_"+n)

    def _createVolume(self, n):
        ctrl = cmds.polyCylinder(r=1, h=2, sx=10, sy=1, sz=1, ax=(0, 1, 0), rcp=0, cuv=3, ch=1)
        cmds.setAttr((ctrl[0]+".sx"), 3)
        cmds.setAttr((ctrl[0]+".sy"), 3)
        cmds.setAttr((ctrl[0]+".sz"), 3)
        cmds.DeleteHistory()
        cmds.select((ctrl[0]+".f[20:29]"), r=True)
        cmds.select((ctrl[0]+".f[10:19]"), add=True)
        cmds.delete()
        cmds.select(ctrl[0], r=True)
        cmds.DeleteHistory()
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.rename(ctrl[0], ("Gd_"+n))
        cmds.select(cl=True)

    def _createVolume2(self, n, pnts, s=2):
        ctrl = cmds.polyCylinder(r=1, h=2, sx=10, sy=1, sz=1, ax=(0, 1, 0), rcp=0, cuv=3, ch=1)
        cmds.setAttr((ctrl[0]+".sx"), s)
        cmds.setAttr((ctrl[0]+".sy"), s)
        cmds.setAttr((ctrl[0]+".sz"), s)
        cmds.DeleteHistory()
        cmds.select((ctrl[0]+".f[20:29]"), r=True)
        cmds.select((ctrl[0]+".f[10:19]"), add=True)
        cmds.delete()
        cmds.select(ctrl[0], r=True)
        cmds.DeleteHistory()
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.rename(ctrl[0], ("Gd_"+n))
        cmds.select(cl=True)
        cmds.setAttr(("gfARGuides:Gd_"+n+"Shape.overrideEnabled"), True)
        cmds.setAttr(("gfARGuides:Gd_"+n+"Shape.overrideDisplayType"), 2)
        cmds.select("gfARGuides:Gd_L_Thigh.vtx[10:19]")
        cl = cmds.cluster(n="Cls_Teste_Top")
        cmds.setAttr((cl[1]+".v"), False)
        cmds.select(cl=True)

    def deleteGuides(self, gd):
        Childs = cmds.layout("scrOutputs", q=True, ca=True)
        if gd == "compHumanSpine":
            if Childs != None:
                cmds.select("gfARGuides:Grp_Guides|gfARGuides:Grp_Components|gfARGuides:Grp_HumanSpine", r=True)
                cmds.Delete()
        elif gd == "compHumanLegs":
            if Childs != None:
                cmds.select("gfARGuides:Grp_Guides|gfARGuides:Grp_Components|gfARGuides:Grp_HumanLegs", r=True)
                cmds.Delete()
        elif gd == "compHumanArms":
            if Childs != None:
                cmds.select("gfARGuides:Grp_Guides|gfARGuides:Grp_Components|gfARGuides:Grp_HumanArms", r=True)
                cmds.Delete()
        elif gd == "compHumanHead":
            if Childs != None:
                cmds.select("gfARGuides:Grp_Guides|gfARGuides:Grp_Components|gfARGuides:Grp_HumanHeads", r=True)
                cmds.Delete()

    def reloadGuides(self, nameComp="", ctrlName="", *args):
        sel = cmds.ls(sl=True, type="transform")
        if nameComp == "intNumJntsHSpine":
            ctrl = []
            offsetHip = cmds.xform("gfARGuides:Ctrl_Hip", q=True, ws=True, rp=True)
            offsetChest = cmds.xform("gfARGuides:Ctrl_Chest", q=True, ws=True, rp=True)
            numJnts = cmds.intSliderGrp("intNumJntsHSpine", q=True, v=True)
            distX = (offsetChest[0] - offsetHip[0]) / (numJnts + 1)
            distY = (offsetChest[1] - offsetHip[1]) / (numJnts + 1)
            for x in range(0,6):
                if cmds.objExists(("gfARGuides:Ctrl_Spine"+str(x))):
                    cmds.select(("gfARGuides:Ctrl_Spine"+str(x)))
                    cmds.Delete()
            # print distX, distY
            self._setNamespace("Start")
            for x in range(1, (numJnts + 1)):
                ctrl.append(self._createCtrl(n=("Spine"+str(x)), t=[offsetHip[0], (offsetHip[1] + (distY * x)), offsetHip[2]], s=0.9))
            for c in ctrl:
                cmds.setAttr((c+".overrideEnabled"), True)
                cmds.setAttr((c+".overrideColor"), 16)
                cmds.select(c, r=True)
                cmds.sets(edit=True, forceElement="gfARGuides:Mtl_GuidesSG")
                cmds.parent(c, ("gfARGuides:Grp_HumanSpine"))
            self._setNamespace("End")
            cmds.select(cl=True)
        elif nameComp == "cbxReverseFootHLegs":
            ctrl = []
            self._setNamespace("Start")
            if ctrlName == "L":
                if cmds.objExists("gfARGuides:Ctrl_L_TipHeel") and cmds.objExists("gfARGuides:Ctrl_L_InFoot") and cmds.objExists("gfARGuides:Ctrl_L_OutFoot") and cmds.objExists("gfARGuides:Ctrl_L_TipFoot"):
                    cmds.select("gfARGuides:Ctrl_L_TipHeel", "gfARGuides:Ctrl_L_InFoot", "gfARGuides:Ctrl_L_OutFoot", "gfARGuides:Ctrl_L_TipFoot", r=True)
                    cmds.Delete()
                else:
                    ctrl.append(self._createCtrl(n=(ctrlName+"_TipHeel"), t=[self.gdLTipHeel[0], self.gdLTipHeel[1], self.gdLTipHeel[2]], s=1.3))
                    ctrl.append(self._createCtrl(n=(ctrlName+"_InFoot"), t=[self.gdLInFoot[0], self.gdLInFoot[1], self.gdLInFoot[2]], s=1.3))
                    ctrl.append(self._createCtrl(n=(ctrlName+"_OutFoot"), t=[self.gdLOutFoot[0], self.gdLOutFoot[1], self.gdLOutFoot[2]], s=1.3))
                    ctrl.append(self._createCtrl(n=(ctrlName+"_TipFoot"), t=[self.gdLTipFoot[0], self.gdLTipFoot[1], self.gdLTipFoot[2]], s=1.3))
                    for c in ctrl:
                        cmds.setAttr((c+".overrideEnabled"), True)
                        cmds.setAttr((c+".overrideColor"), 16)
                        cmds.select(c, r=True)
                        cmds.sets(edit=True, forceElement="gfARGuides:Mtl_GuidesSG")
                        cmds.parent(c, ("gfARGuides:Grp_"+ctrlName+"_Leg_HLegs"))
            elif ctrlName == "R":
                if cmds.objExists("gfARGuides:Ctrl_R_TipHeel") and cmds.objExists("gfARGuides:Ctrl_R_InFoot") and cmds.objExists("gfARGuides:Ctrl_R_OutFoot") and cmds.objExists("gfARGuides:Ctrl_R_TipFoot"):
                    cmds.select("gfARGuides:Ctrl_R_TipHeel", "gfARGuides:Ctrl_R_InFoot", "gfARGuides:Ctrl_R_OutFoot", "gfARGuides:Ctrl_R_TipFoot", r=True)
                    cmds.Delete()
                else:
                    ctrl.append(self._createCtrl(n=(ctrlName+"_TipHeel"), t=[self.gdRTipHeel[0], self.gdRTipHeel[1], self.gdRTipHeel[2]], s=1.3))
                    ctrl.append(self._createCtrl(n=(ctrlName+"_InFoot"), t=[self.gdRInFoot[0], self.gdRInFoot[1], self.gdRInFoot[2]], s=1.3))
                    ctrl.append(self._createCtrl(n=(ctrlName+"_OutFoot"), t=[self.gdROutFoot[0], self.gdROutFoot[1], self.gdROutFoot[2]], s=1.3))
                    ctrl.append(self._createCtrl(n=(ctrlName+"_TipFoot"), t=[self.gdRTipFoot[0], self.gdRTipFoot[1], self.gdRTipFoot[2]], s=1.3))
                    for c in ctrl:
                        cmds.setAttr((c+".overrideEnabled"), True)
                        cmds.setAttr((c+".overrideColor"), 16)
                        cmds.select(c, r=True)
                        cmds.sets(edit=True, forceElement="gfARGuides:Mtl_GuidesSG")
                        cmds.parent(c, ("gfARGuides:Grp_"+ctrlName+"_Leg_HLegs"))
            self._setNamespace("End")
            cmds.select(sel, r=True)
        elif nameComp == "cbxArmHaveClavicleHArms":
            ctrl = []
            self._setNamespace("Start")
            if ctrlName == "LArm":
                if cmds.checkBoxGrp(("cbx"+ctrlName+"HaveClavicleHArms"), q=True, v1=True) == True:
                    """ Create guides. """
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Clavicle"), t=[self.gdLClavicle[0], self.gdLClavicle[1], self.gdLClavicle[2]]))
                    for c in ctrl:
                        cmds.setAttr((c+".overrideEnabled"), True)
                        cmds.setAttr((c+".overrideColor"), 16)
                        cmds.select(c, r=True)
                        cmds.sets(edit=True, forceElement="gfARGuides:Mtl_GuidesSG")
                        cmds.parent(c, ("gfARGuides:Grp_"+ctrlName[0]+"_Arm_HArms"))
                else:
                    """ Delete guides. """
                    cmds.select('gfARGuides:Ctrl_'+ctrlName[0]+'_Clavicle')
                    cmds.delete()
            elif ctrlName == "RArm":
                if cmds.checkBoxGrp(("cbx"+ctrlName+"HaveClavicleHArms"), q=True, v1=True) == True:
                    """ Create guides. """
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Clavicle"), t=[self.gdRClavicle[0], self.gdRClavicle[1], self.gdRClavicle[2]]))
                    for c in ctrl:
                        cmds.setAttr((c+".overrideEnabled"), True)
                        cmds.setAttr((c+".overrideColor"), 16)
                        cmds.select(c, r=True)
                        cmds.sets(edit=True, forceElement="gfARGuides:Mtl_GuidesSG")
                        cmds.parent(c, ("gfARGuides:Grp_"+ctrlName[0]+"_Arm_HArms"))
                else:
                    """ Delete guides. """
                    cmds.select('gfARGuides:Ctrl_'+ctrlName[0]+'_Clavicle')
                    cmds.delete()
            else:
                pass
            self._setNamespace("End")
            cmds.select(sel, r=True)
        elif nameComp == "cbxArmHaveFingersHArms":
            ctrl = []
            self._setNamespace("Start")
            if ctrlName == "LArm":
                if cmds.checkBoxGrp(("cbx"+ctrlName+"HaveFingersHArms"), q=True, v1=True) == True:
                    """ Create guides. """
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Thumb_Meta"), t=[self.gdLThumbMeta[0], self.gdLThumbMeta[1], self.gdLThumbMeta[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Thumb_Prox"), t=[self.gdLThumbProx[0], self.gdLThumbProx[1], self.gdLThumbProx[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Thumb_Dist"), t=[self.gdLThumbDist[0], self.gdLThumbDist[1], self.gdLThumbDist[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Thumb_End"), t=[self.gdLThumbEnd[0], self.gdLThumbEnd[1], self.gdLThumbEnd[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Index_Meta"), t=[self.gdLIndexMeta[0], self.gdLIndexMeta[1], self.gdLIndexMeta[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Index_Prox"), t=[self.gdLIndexProx[0], self.gdLIndexProx[1], self.gdLIndexProx[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Index_Mid"), t=[self.gdLIndexMid[0], self.gdLIndexMid[1], self.gdLIndexMid[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Index_Dist"), t=[self.gdLIndexDist[0], self.gdLIndexDist[1], self.gdLIndexDist[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Index_End"), t=[self.gdLIndexEnd[0], self.gdLIndexEnd[1], self.gdLIndexEnd[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Middle_Meta"), t=[self.gdLMiddleMeta[0], self.gdLMiddleMeta[1], self.gdLMiddleMeta[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Middle_Prox"), t=[self.gdLMiddleProx[0], self.gdLMiddleProx[1], self.gdLMiddleProx[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Middle_Mid"), t=[self.gdLMiddleMid[0], self.gdLMiddleMid[1], self.gdLMiddleMid[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Middle_Dist"), t=[self.gdLMiddleDist[0], self.gdLMiddleDist[1], self.gdLMiddleDist[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Middle_End"), t=[self.gdLMiddleEnd[0], self.gdLMiddleEnd[1], self.gdLMiddleEnd[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Ring_Meta"), t=[self.gdLRingMeta[0], self.gdLRingMeta[1], self.gdLRingMeta[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Ring_Prox"), t=[self.gdLRingProx[0], self.gdLRingProx[1], self.gdLRingProx[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Ring_Mid"), t=[self.gdLRingMid[0], self.gdLRingMid[1], self.gdLRingMid[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Ring_Dist"), t=[self.gdLRingDist[0], self.gdLRingDist[1], self.gdLRingDist[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Ring_End"), t=[self.gdLRingEnd[0], self.gdLRingEnd[1], self.gdLRingEnd[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Pinky_Meta"), t=[self.gdLPinkyMeta[0], self.gdLPinkyMeta[1], self.gdLPinkyMeta[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Pinky_Prox"), t=[self.gdLPinkyProx[0], self.gdLPinkyProx[1], self.gdLPinkyProx[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Pinky_Mid"), t=[self.gdLPinkyMid[0], self.gdLPinkyMid[1], self.gdLPinkyMid[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Pinky_Dist"), t=[self.gdLPinkyDist[0], self.gdLPinkyDist[1], self.gdLPinkyDist[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Pinky_End"), t=[self.gdLPinkyEnd[0], self.gdLPinkyEnd[1], self.gdLPinkyEnd[2]], s=0.5))
                    for c in ctrl:
                        cmds.setAttr((c+".overrideEnabled"), True)
                        cmds.setAttr((c+".overrideColor"), 16)
                        cmds.select(c, r=True)
                        cmds.sets(edit=True, forceElement="gfARGuides:Mtl_GuidesSG")
                        cmds.parent(c, ("gfARGuides:Grp_"+ctrlName[0]+"_Arm_HArms"))
                    """ Parent palm and armEnd to figers and hide them. """
                    cmds.parent('gfARGuides:Ctrl_'+ctrlName[0]+'_Palm', 'gfARGuides:Ctrl_'+ctrlName[0]+'_Middle_Prox')
                    cmds.parent('gfARGuides:Ctrl_'+ctrlName[0]+'_ArmEnd', 'gfARGuides:Ctrl_'+ctrlName[0]+'_Middle_End')
                    cmds.hide('gfARGuides:Ctrl_'+ctrlName[0]+'_Palm', 'gfARGuides:Ctrl_'+ctrlName[0]+'_ArmEnd')
                else:
                    cmds.parent('gfARGuides:Ctrl_'+ctrlName[0]+'_Palm', 'gfARGuides:Grp_'+ctrlName[0]+'_Arm_HArms')
                    cmds.parent('gfARGuides:Ctrl_'+ctrlName[0]+'_ArmEnd', 'gfARGuides:Grp_'+ctrlName[0]+'_Arm_HArms')
                    cmds.showHidden('gfARGuides:Ctrl_'+ctrlName[0]+'_Palm', 'gfARGuides:Ctrl_'+ctrlName[0]+'_ArmEnd')
                    """ Delete guides. """
                    toDel = cmds.ls('*gfARGuides:Ctrl_'+ctrlName[0]+'_Thumb*', '*gfARGuides:Ctrl_'+ctrlName[0]+'_Index*', '*gfARGuides:Ctrl_'+ctrlName[0]+'_Middle*',
                        '*gfARGuides:Ctrl_'+ctrlName[0]+'_Ring*', '*gfARGuides:Ctrl_'+ctrlName[0]+'_Pinky*', type='transform')
                    cmds.delete(toDel)
            elif ctrlName == "RArm":
                if cmds.checkBoxGrp(("cbx"+ctrlName+"HaveFingersHArms"), q=True, v1=True) == True:
                    """ Create guides. """
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Thumb_Meta"), t=[self.gdRThumbMeta[0], self.gdRThumbMeta[1], self.gdRThumbMeta[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Thumb_Prox"), t=[self.gdRThumbProx[0], self.gdRThumbProx[1], self.gdRThumbProx[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Thumb_Dist"), t=[self.gdRThumbDist[0], self.gdRThumbDist[1], self.gdRThumbDist[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Thumb_End"), t=[self.gdRThumbEnd[0], self.gdRThumbEnd[1], self.gdRThumbEnd[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Index_Meta"), t=[self.gdRIndexMeta[0], self.gdRIndexMeta[1], self.gdRIndexMeta[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Index_Prox"), t=[self.gdRIndexProx[0], self.gdRIndexProx[1], self.gdRIndexProx[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Index_Mid"), t=[self.gdRIndexMid[0], self.gdRIndexMid[1], self.gdRIndexMid[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Index_Dist"), t=[self.gdRIndexDist[0], self.gdRIndexDist[1], self.gdRIndexDist[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Index_End"), t=[self.gdRIndexEnd[0], self.gdRIndexEnd[1], self.gdRIndexEnd[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Middle_Meta"), t=[self.gdRMiddleMeta[0], self.gdRMiddleMeta[1], self.gdRMiddleMeta[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Middle_Prox"), t=[self.gdRMiddleProx[0], self.gdRMiddleProx[1], self.gdRMiddleProx[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Middle_Mid"), t=[self.gdRMiddleMid[0], self.gdRMiddleMid[1], self.gdRMiddleMid[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Middle_Dist"), t=[self.gdRMiddleDist[0], self.gdRMiddleDist[1], self.gdRMiddleDist[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Middle_End"), t=[self.gdRMiddleEnd[0], self.gdRMiddleEnd[1], self.gdRMiddleEnd[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Ring_Meta"), t=[self.gdRRingMeta[0], self.gdRRingMeta[1], self.gdRRingMeta[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Ring_Prox"), t=[self.gdRRingProx[0], self.gdRRingProx[1], self.gdRRingProx[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Ring_Mid"), t=[self.gdRRingMid[0], self.gdRRingMid[1], self.gdRRingMid[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Ring_Dist"), t=[self.gdRRingDist[0], self.gdRRingDist[1], self.gdRRingDist[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Ring_End"), t=[self.gdRRingEnd[0], self.gdRRingEnd[1], self.gdRRingEnd[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Pinky_Meta"), t=[self.gdRPinkyMeta[0], self.gdRPinkyMeta[1], self.gdRPinkyMeta[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Pinky_Prox"), t=[self.gdRPinkyProx[0], self.gdRPinkyProx[1], self.gdRPinkyProx[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Pinky_Mid"), t=[self.gdRPinkyMid[0], self.gdRPinkyMid[1], self.gdRPinkyMid[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Pinky_Dist"), t=[self.gdRPinkyDist[0], self.gdRPinkyDist[1], self.gdRPinkyDist[2]], s=0.5))
                    ctrl.append(self._createCtrl(n=(ctrlName[0]+"_Pinky_End"), t=[self.gdRPinkyEnd[0], self.gdRPinkyEnd[1], self.gdRPinkyEnd[2]], s=0.5))
                    for c in ctrl:
                        cmds.setAttr((c+".overrideEnabled"), True)
                        cmds.setAttr((c+".overrideColor"), 16)
                        cmds.select(c, r=True)
                        cmds.sets(edit=True, forceElement="gfARGuides:Mtl_GuidesSG")
                        cmds.parent(c, ("gfARGuides:Grp_"+ctrlName[0]+"_Arm_HArms"))
                    """ Parent palm and armEnd to figers and hide them. """
                    cmds.parent('gfARGuides:Ctrl_'+ctrlName[0]+'_Palm', 'gfARGuides:Ctrl_'+ctrlName[0]+'_Middle_Prox')
                    cmds.parent('gfARGuides:Ctrl_'+ctrlName[0]+'_ArmEnd', 'gfARGuides:Ctrl_'+ctrlName[0]+'_Middle_End')
                    cmds.hide('gfARGuides:Ctrl_'+ctrlName[0]+'_Palm', 'gfARGuides:Ctrl_'+ctrlName[0]+'_ArmEnd')
                else:
                    cmds.parent('gfARGuides:Ctrl_'+ctrlName[0]+'_Palm', 'gfARGuides:Grp_'+ctrlName[0]+'_Arm_HArms')
                    cmds.parent('gfARGuides:Ctrl_'+ctrlName[0]+'_ArmEnd', 'gfARGuides:Grp_'+ctrlName[0]+'_Arm_HArms')
                    cmds.showHidden('gfARGuides:Ctrl_'+ctrlName[0]+'_Palm', 'gfARGuides:Ctrl_'+ctrlName[0]+'_ArmEnd')
                    """ Delete guides. """
                    toDel = cmds.ls('*gfARGuides:Ctrl_'+ctrlName[0]+'_Thumb*', '*gfARGuides:Ctrl_'+ctrlName[0]+'_Index*', '*gfARGuides:Ctrl_'+ctrlName[0]+'_Middle*',
                        '*gfARGuides:Ctrl_'+ctrlName[0]+'_Ring*', '*gfARGuides:Ctrl_'+ctrlName[0]+'_Pinky*', type='transform')
                    cmds.delete(toDel)
            else:
                pass
            self._setNamespace("End")
            cmds.select(sel, r=True)

    def buildGuides(self, typ):
        sel = cmds.ls(sl=True, type="transform")
        if cmds.objExists(("gfARGuides:Ctrl_Global")):
            ctrlGblSca = cmds.xform("gfARGuides:Ctrl_Global", q=True, s=True, r=True)
            cmds.xform("gfARGuides:Ctrl_Global", s=(1, 1, 1))
        if typ == "compHumanSpine":
            self.buildHumanSpine()
            cmds.parent("gfARGuides:Grp_HumanSpine", "gfARGuides:Grp_Guides|gfARGuides:Grp_Components")
            cmds.setAttr("gfARGuides:Grp_HumanSpine.useOutlinerColor", True)
            cmds.setAttr("gfARGuides:Grp_HumanSpine.outlinerColorR", self.outlParent[0])
            cmds.setAttr("gfARGuides:Grp_HumanSpine.outlinerColorG", self.outlParent[1])
            cmds.setAttr("gfARGuides:Grp_HumanSpine.outlinerColorB", self.outlParent[2])
            cmds.select(cl=True)
        elif typ == "compHumanLegs":
            multLegs = cmds.radioButtonGrp("radMultLegsHLegs", q=True, sl=True)
            legIndex = cmds.textField("txtNumberHLegs", q=True, tx=True)
            if multLegs == 1:
                self.buildHumanLeg("left")
                self.buildHumanLeg("right")
                cmds.select("gfARGuides:Grp_L_Leg_HLegs", "gfARGuides:Grp_R_Leg_HLegs")
                grp = cmds.group()
                cmds.rename(grp, ("gfARGuides:Grp_HumanLegs"))
                cmds.parent("gfARGuides:Grp_HumanLegs", "gfARGuides:Grp_Guides|gfARGuides:Grp_Components")
                cmds.setAttr("gfARGuides:Grp_HumanLegs.useOutlinerColor", True)
                cmds.setAttr("gfARGuides:Grp_HumanLegs.outlinerColorR", self.outlParent[0])
                cmds.setAttr("gfARGuides:Grp_HumanLegs.outlinerColorG", self.outlParent[1])
                cmds.setAttr("gfARGuides:Grp_HumanLegs.outlinerColorB", self.outlParent[2])
                cmds.select(cl=True)
            elif multLegs == 2:
                pass
        elif typ == "compHumanArms":
            self.buildHumanArm("left")
            self.buildHumanArm("right")
            cmds.select("gfARGuides:Grp_L_Arm_HArms", "gfARGuides:Grp_R_Arm_HArms")
            grp = cmds.group()
            cmds.rename(grp, ("gfARGuides:Grp_HumanArms"))
            cmds.parent("gfARGuides:Grp_HumanArms", "gfARGuides:Grp_Guides|gfARGuides:Grp_Components")
            cmds.setAttr("gfARGuides:Grp_HumanArms.useOutlinerColor", True)
            cmds.setAttr("gfARGuides:Grp_HumanArms.outlinerColorR", self.outlParent[0])
            cmds.setAttr("gfARGuides:Grp_HumanArms.outlinerColorG", self.outlParent[1])
            cmds.setAttr("gfARGuides:Grp_HumanArms.outlinerColorB", self.outlParent[2])
            cmds.select(cl=True)
        elif typ == "compHumanHead":
            self.buildHumanHeads()
            cmds.parent("gfARGuides:Grp_HumanHeads", "gfARGuides:Grp_Guides|gfARGuides:Grp_Components")
            cmds.setAttr("gfARGuides:Grp_HumanHeads.useOutlinerColor", True)
            cmds.setAttr("gfARGuides:Grp_HumanHeads.outlinerColorR", self.outlParent[0])
            cmds.setAttr("gfARGuides:Grp_HumanHeads.outlinerColorG", self.outlParent[1])
            cmds.setAttr("gfARGuides:Grp_HumanHeads.outlinerColorB", self.outlParent[2])
            cmds.select(cl=True)
        if cmds.objExists(("gfARGuides:Ctrl_Global")): cmds.xform("gfARGuides:Ctrl_Global", s=(ctrlGblSca[0], ctrlGblSca[1], ctrlGblSca[2]))
        cmds.select(sel, r=True)

    # --------------------------------------------------------------------------------------------------------------------
    # ------------------------ BUILD GUIDES
    # --------------------------------------------------------------------------------------------------------------------
    def buildHumanSpine(self):
        ctrl = []
        self._setNamespace("Start")
        # Set controllers
        # ctrl.append(self._createCtrl(n="Root", t=[self.gdRoot[0], self.gdRoot[1], self.gdRoot[2]]))
        ctrl.append(self._createCtrl(n="Hip", t=[self.gdHip[0], self.gdHip[1], self.gdHip[2]]))
        ctrl.append(self._createCtrl(n="Spine1", t=[self.gdSpine1[0], self.gdSpine1[1], self.gdSpine1[2]], s=0.9))
        ctrl.append(self._createCtrl(n="Spine2", t=[self.gdSpine2[0], self.gdSpine2[1], self.gdSpine2[2]], s=0.9))
        ctrl.append(self._createCtrl(n="Spine3", t=[self.gdSpine3[0], self.gdSpine3[1], self.gdSpine3[2]], s=0.9))
        ctrl.append(self._createCtrl(n="Chest", t=[self.gdChest[0], self.gdChest[1], self.gdChest[2]]))
        # Group controls
        for c in ctrl:
            cmds.setAttr((c+".overrideEnabled"), True)
            cmds.setAttr((c+".overrideColor"), 16)
            cmds.select(c, r=True)
            cmds.sets(edit=True, forceElement="gfARGuides:Mtl_GuidesSG")
        cmds.select(ctrl, r=True)
        grp = cmds.group()
        cmds.rename(grp, "Grp_HumanSpine")
        self._setNamespace("End")

    def buildHumanLeg(self, name):
        # Store infos
        # if cmds.objExists(("gfARGuides:Ctrl_"+self.side+"_Thigh")):
        ctrl = []
        self._setNamespace("Start")
        # Set controllers for each leg
        if name == "left":
            name = "L"
            names = [(name+"_Thigh"), (name+"_Shin"), (name+"_Ankle"), (name+"_Toe"), (name+"_LegEnd")]
            ctrl.append(self._createCtrl(n=(name+"_Thigh"), t=[self.gdLThigh[0], self.gdLThigh[1], self.gdLThigh[2]]))
            ctrl.append(self._createCtrl(n=(name+"_Shin"), t=[self.gdLShin[0], self.gdLShin[1], self.gdLShin[2]]))
            ctrl.append(self._createCtrl(n=(name+"_Ankle"), t=[self.gdLAnkle[0], self.gdLAnkle[1], self.gdLAnkle[2]]))
            ctrl.append(self._createCtrl(n=(name+"_Toe"), t=[self.gdLToe[0], self.gdLToe[1], self.gdLToe[2]]))
            ctrl.append(self._createCtrl(n=(name+"_LegEnd"), t=[self.gdLLegEnd[0], self.gdLLegEnd[1], self.gdLLegEnd[2]]))
        elif name == "right":
            name = "R"
            names = [(name+"_Thigh"), (name+"_Shin"), (name+"_Ankle"), (name+"_Toe"), (name+"_LegEnd")]
            ctrl.append(self._createCtrl(n=(name+"_Thigh"), t=[self.gdRThigh[0], self.gdRThigh[1], self.gdRThigh[2]]))
            ctrl.append(self._createCtrl(n=(name+"_Shin"), t=[self.gdRShin[0], self.gdRShin[1], self.gdRShin[2]]))
            ctrl.append(self._createCtrl(n=(name+"_Ankle"), t=[self.gdRAnkle[0], self.gdRAnkle[1], self.gdRAnkle[2]]))
            ctrl.append(self._createCtrl(n=(name+"_Toe"), t=[self.gdRToe[0], self.gdRToe[1], self.gdRToe[2]]))
            ctrl.append(self._createCtrl(n=(name+"_LegEnd"), t=[self.gdRLegEnd[0], self.gdRLegEnd[1], self.gdRLegEnd[2]]))
        # Group controls
        for c in ctrl:
            cmds.setAttr((c+".overrideEnabled"), True)
            cmds.setAttr((c+".overrideColor"), 16)
            cmds.select(c, r=True)
            cmds.sets(edit=True, forceElement="gfARGuides:Mtl_GuidesSG")
        cmds.select(ctrl, r=True)
        grp = cmds.group()
        cmds.rename(grp, ("Grp_"+name+"_Leg_HLegs"))
        # Set volumes for each leg
        # self._createVolume(n=(name+"_Thigh"))
        # Organize in a group called Grp_Leg_Name
        self._setNamespace("End")

    def buildHumanArm(self, name):
        ctrl = []
        self._setNamespace("Start")
        # Set controllers for each leg
        if name == "left":
            name = "L"
            ctrl.append(self._createCtrl(n=(name+"_UpperArm"), t=[self.gdLUpperArm[0], self.gdLUpperArm[1], self.gdLUpperArm[2]]))
            ctrl.append(self._createCtrl(n=(name+"_Forearm"), t=[self.gdLForearm[0], self.gdLForearm[1], self.gdLForearm[2]]))
            ctrl.append(self._createCtrl(n=(name+"_Wrist"), t=[self.gdLWrist[0], self.gdLWrist[1], self.gdLWrist[2]]))
            ctrl.append(self._createCtrl(n=(name+"_Palm"), t=[self.gdLPalm[0], self.gdLPalm[1], self.gdLPalm[2]]))
            ctrl.append(self._createCtrl(n=(name+"_ArmEnd"), t=[self.gdLArmEnd[0], self.gdLArmEnd[1], self.gdLArmEnd[2]]))
        elif name == "right":
            name = "R"
            ctrl.append(self._createCtrl(n=(name+"_UpperArm"), t=[self.gdRUpperArm[0], self.gdRUpperArm[1], self.gdRUpperArm[2]]))
            ctrl.append(self._createCtrl(n=(name+"_Forearm"), t=[self.gdRForearm[0], self.gdRForearm[1], self.gdRForearm[2]]))
            ctrl.append(self._createCtrl(n=(name+"_Wrist"), t=[self.gdRWrist[0], self.gdRWrist[1], self.gdRWrist[2]]))
            ctrl.append(self._createCtrl(n=(name+"_Palm"), t=[self.gdRPalm[0], self.gdRPalm[1], self.gdRPalm[2]]))
            ctrl.append(self._createCtrl(n=(name+"_ArmEnd"), t=[self.gdRArmEnd[0], self.gdRArmEnd[1], self.gdRArmEnd[2]]))
        # Group controls
        for c in ctrl:
            cmds.setAttr((c+".overrideEnabled"), True)
            cmds.setAttr((c+".overrideColor"), 16)
            cmds.select(c, r=True)
            cmds.sets(edit=True, forceElement="gfARGuides:Mtl_GuidesSG")
        cmds.select(ctrl, r=True)
        grp = cmds.group()
        cmds.rename(grp, ("Grp_"+name+"_Arm_HArms"))
        # Set volumes for each leg
        # self._createVolume(n=(name+"_Thigh"))
        # Organize in a group called Grp_Leg_Name
        self._setNamespace("End")

    def buildHumanHeads(self):
        self._setNamespace("Start")
        # Set controllers
        ctrl = []
        ctrl.append(self._createCtrl(n="Neck", t=[self.gdNeck[0], self.gdNeck[1], self.gdNeck[2]], s=1.2))
        ctrl.append(self._createCtrl(n="Head", t=[self.gdHead[0], self.gdHead[1], self.gdHead[2]], s=1.2))
        ctrl.append(self._createCtrl(n="Jaw", t=[self.gdJaw[0], self.gdJaw[1], self.gdJaw[2]], s=1.2))
        ctrl.append(self._createCtrl(n="JawPivot", t=[self.gdJawPivot[0], self.gdJawPivot[1], self.gdJawPivot[2]], s=1.2))
        ctrl.append(self._createCtrl(n="JawEnd", t=[self.gdJawEnd[0], self.gdJawEnd[1], self.gdJawEnd[2]], s=1.2))
        ctrl.append(self._createCtrl(n="HeadEnd", t=[self.gdHeadEnd[0], self.gdHeadEnd[1], self.gdHeadEnd[2]], s=1.2))
        # Group controls
        for c in ctrl:
            cmds.setAttr((c+".overrideEnabled"), True)
            cmds.setAttr((c+".overrideColor"), 16)
            cmds.select(c, r=True)
            cmds.sets(edit=True, forceElement="gfARGuides:Mtl_GuidesSG")
        cmds.select(ctrl, r=True)
        grp = cmds.group()
        cmds.rename(grp, "Grp_HumanHeads")
        self._setNamespace("End")
