import maya.cmds as cmds
import maya.mel as mel

class buildLog(object):

    def __init__(self, msg, btn=False, parent="promptLog", dsp=True, stop=True, partial="NDA", *args):
        self.message = msg
        self.partial = partial
        self.btnClicked = btn
        self.parent = parent
        self.display = dsp
        self.stop = stop
        self.logLines = []
        if self.message == "initialized": self.initialized()
        elif self.message == "setCharNameUI": self.setCharNameUI()
        elif self.message == "setCharTypeUI": self.setCharTypeUI()
        elif self.message == "addGeometryUI": self.addGeometryUI()
        elif self.message == "removeGeometryUI": self.removeGeometryUI()
        elif self.message == "clearGeometryUI": self.clearGeometryUI()
        elif self.message == "selectGeometryUI": self.selectGeometryUI()
        elif self.message == "componentCreatedUI": self.componentCreatedUI()
        elif self.message == "componentExistsUI": self.componentExistsUI()
        elif self.message == "componentDeletedUI": self.componentDeletedUI()
        elif self.message == "clearComponentsUI": self.clearComponentsUI()
        elif self.message == "loadBuiltInPresetUI": self.loadBuiltInPresetUI()
        elif self.message == "createPropertiesUI": self.createPropertiesUI()
        elif self.message == "deletePropertiesUI": self.deletePropertiesUI()
        elif self.message == "loadPropertiesUI": self.loadPropertiesUI()
        elif self.message == "whiteLine": self.whiteLine()
        elif self.message == None: self._result(True)
        else: pass

        if self.partial == "clearLog": self.clearLog()
        elif self.partial == "exportLog": self.exportLog()
        else: pass

    def initialized(self):
        cmds.text("\\\\   initialized [result: True]", parent=self.parent)
        cmds.text("\\\\", parent=self.parent)
        self.logLines += ["\\\\   initialized [result: True]"]
        self.logLines += ["\\\\"]
        for l in self.logLines:
            print l

    def exportLog(self):
        pass

    def clearLog(self):
        cmds.deleteUI("logCreate")
        cmds.rowLayout("logCreate", w=370, h=470, nc=2, parent="layLog")
        cmds.separator(w=5, h=3, st="none")
        cmds.scrollLayout("promptLog", w=370, h=525, vsb=True)
        self.logLines = []
        cmds.text("\\\\   initialized [result: True]", parent=self.parent)
        cmds.text("\\\\", parent=self.parent)
        self.logLines += ["\\\\   initialized [result: True]"]
        self.logLines += ["\\\\"]

    def _result(self, result):
        if self.stop == True:
            if result == True:
                cmds.text("\\\\   [result: True]", parent=self.parent)
                cmds.text("\\\\", parent=self.parent)
                self.logLines += ["\\\\   [result: True]"]
                self.logLines += ["\\\\"]
            else:
                cmds.text("\\\\   [result: False]", parent=self.parent)
                cmds.text("\\\\", parent=self.parent)
                self.logLines += ["\\\\   [result: False]"]
                self.logLines += ["\\\\"]
        else: pass

    def whiteLine(self):
        if self.display == True:
            cmds.text(("\\\\   "), parent=self.parent)
            self.logLines += [("\\\\   ")]
            self._result(True)
        else: pass

    def setCharNameUI(self):
        if self.display == True:
            cmds.text(("\\\\   Name of the character changed to: ("+str(self.btnClicked)+")"), parent=self.parent)
            self.logLines += [("\\\\   Name of the character changed to: ("+str(self.btnClicked)+")")]
            self._result(True)
        else: pass

    def setCharTypeUI(self):
        if self.display == True:
            cmds.text(("\\\\   Type of the character changed to: ("+str(self.btnClicked)+")"), parent=self.parent)
            self.logLines += [("\\\\   Type of the character changed to: ("+str(self.btnClicked)+")")]
            self._result(True)
        else: pass

    def addGeometryUI(self):
        if self.display == True:
            cmds.text(("\\\\   ("+str(self.btnClicked)+") geometry appended"), parent=self.parent)
            self.logLines += [("\\\\   ("+str(self.btnClicked)+") geometry appended")]
            self._result(True)
        else: pass

    def removeGeometryUI(self):
        if self.display == True:
            cmds.text(("\\\\   ("+str(self.btnClicked)+") geometry removed"), parent=self.parent)
            self.logLines += [("\\\\   ("+str(self.btnClicked)+") geometry removed")]
            self._result(True)
        else: pass

    def clearGeometryUI(self):
        if self.display == True:
            cmds.text(("\\\\   All geometry in geometry list removed"), parent=self.parent)
            self.logLines += [("\\\\   All geometry in geometry list removed")]
            self._result(True)
        else: pass

    def selectGeometryUI(self):
        if self.display == True:
            cmds.text(("\\\\   ("+str(self.btnClicked)+") geometry selected through geometry list"), parent=self.parent)
            self.logLines += [("\\\\   ("+str(self.btnClicked)+") geometry selected through geometry list")]
            self._result(True)
        else: pass

    def componentCreatedUI(self):
        if self.display == True:
            cmds.text(("\\\\   ("+str(self.btnClicked)+") component created"), parent=self.parent)
            self.logLines += [("\\\\   ("+str(self.btnClicked)+") component created")]
            self._result(True)
        else: pass

    def componentExistsUI(self):
        if self.display == True:
            cmds.text(("\\\\   ("+str(self.btnClicked)+") component already exists"), parent=self.parent)
            self.logLines += [("\\\\   ("+str(self.btnClicked)+") component already exists")]
            self._result(True)
        else: pass

    def componentDeletedUI(self):
        if self.display == True:
            cmds.text(("\\\\   ("+str(self.btnClicked)+") component deleted"), parent=self.parent)
            self.logLines += [("\\\\   ("+str(self.btnClicked)+") component deleted")]
            self._result(True)
        else: pass

    def clearComponentsUI(self):
        if self.display == True:
            cmds.text(("\\\\   Clear all components"), parent=self.parent)
            self.logLines += ["\\\\   Clear all components"]
        else: pass

    def loadBuiltInPresetUI(self):
        if self.display == True:
            cmds.text(("\\\\   ("+str(self.btnClicked)+") preset is being created"), parent=self.parent)
            self.logLines += [("\\\\   ("+str(self.btnClicked)+") preset is being created")]
        else: pass

    def createPropertiesUI(self):
        if self.display == True:
            cmds.text(("\\\\   ("+str(self.btnClicked)+") properties created"), parent=self.parent)
            self.logLines += [("\\\\   ("+str(self.btnClicked)+") properties is created")]
            self._result(True)
        else: pass

    def deletePropertiesUI(self):
        if self.display == True:
            cmds.text(("\\\\   ("+str(self.btnClicked)+") properties deleted"), parent=self.parent)
            self.logLines += [("\\\\   ("+str(self.btnClicked)+") properties is deleted")]
            self._result(True)
        else: pass

    def loadPropertiesUI(self):
        if self.display == True:
            cmds.text(("\\\\   ("+str(self.btnClicked)+") properties loaded"), parent=self.parent)
            self.logLines += [("\\\\   ("+str(self.btnClicked)+") properties is loaded")]
            self._result(True)
        else: pass


class buildLogHumanLeg(buildLog):

    def __init__(self, msg, btn=False, parent="promptLog", dsp=True, stop=True):
        super(buildLogHumanLeg, self).__init__(msg, btn, parent, dsp, stop)
        if self.message == "multLegsPropUI": self.multLegsPropUI()
        elif self.message == "addRemLegsPropUI": self.addRemLegsPropUI()
        elif self.message == "haveFingersLegsPropUI": self.haveFingersLegsPropUI()
        elif self.message == "startBuildHumanLeg": self.startBuildHumanLeg()
        elif self.message == "readFeatures": self.readFeatures()
        elif self.message == "foundGuidesTrans": self.foundGuidesTrans()
        elif self.message == "settingJntsVariables": self.settingJntsVariables()
        elif self.message == "createJnts": self.createJnts()
        elif self.message == "connectJnts": self.connectJnts()
        elif self.message == "jntChainsCreated": self.jntChainsCreated()
        elif self.message == "orientJnts": self.orientJnts()
        cmds.scrollLayout("promptLog", edit=True, sp=("down"))

    def multLegsPropUI(self):
        if self.display == True:
            if self.btnClicked == 1:
                cmds.text(("\\\\   Multiple Human Legs mode disabled"), parent=self.parent)
                self.logLines += [("\\\\   Multiple Human Legs mode disabled")]
                self._result(True)
            elif self.btnClicked == 2:
                cmds.text(("\\\\   Multiple Human Legs mode enabled"), parent=self.parent)
                self.logLines += [("\\\\   Multiple Human Legs mode enabled")]
                self._result(True)
        else: pass

    def addRemLegsPropUI(self):
        if self.display == True:
            if self.btnClicked == "add":
                cmds.text(("\\\\   Human Leg added"), parent=self.parent)
                self.logLines += [("\\\\   Human Leg added")]
                self._result(True)
            elif self.btnClicked == "rem":
                cmds.text(("\\\\   Human Leg removed"), parent=self.parent)
                self.logLines += [("\\\\   Human Leg removed")]
                self._result(True)
        else: pass

    def haveFingersLegsPropUI(self):
        if self.display == True:
            check = cmds.checkBoxGrp(("cbx"+self.btnClicked+"HaveFingersHLegs"), q=True, v1=True)
            if check == True:
                cmds.text(("\\\\   Human ("+str(self.btnClicked)+") have fingers enabled"), parent=self.parent)
                self.logLines += [("\\\\   Human ("+str(self.btnClicked)+") have fingers enabled")]
                self._result(True)
            else:
                cmds.text(("\\\\   Human ("+str(self.btnClicked)+") have fingers disabled"), parent=self.parent)
                self.logLines += [("\\\\   Human ("+str(self.btnClicked)+") have fingers disabled")]
                self._result(True)
        else: pass

    def numFingersLegsPropUI(self):
        if self.display == True:
            pass
        else: pass

    def startBuildHumanLeg(self):
        if self.display == True:
            if self.btnClicked == "All":
                cmds.text(("\\\\   =================[BUILDING]================="), parent=self.parent)
                cmds.text(("\\\\   "), parent=self.parent)
                cmds.text(("\\\\   ====== START BUILDING HUMAN LEGS..."), parent=self.parent)
                cmds.text(("\\\\   "), parent=self.parent)
                self.logLines += [("\\\\   =================[BUILDING]=================")]
                self.logLines += [("\\\\   ")]
                self.logLines += [("\\\\   ====== START BUILDING HUMAN LEGS...")]
                self.logLines += [("\\\\   ")]
                self._result(True)
            else:
                cmds.text(("\\\\   BUILDING ("+str(self.btnClicked)+") ..."), parent=self.parent)
                self.logLines += [("\\\\   BUILDING ("+str(self.btnClicked)+") ...")]
                self._result(True)
        else: pass

    def readFeatures(self):
        if self.display == True:
            if self.btnClicked == "All":
                cmds.text(("\\\\   All human legs features readed"), parent=self.parent)
                self.logLines += [("\\\\   All human legs features readed")]
                self._result(True)
            elif self.btnClicked == "Start":
                cmds.text(("\\\\   Reading all human legs features..."), parent=self.parent)
                self.logLines += [("\\\\   Reading all human legs features...")]
                self._result(True)
        else: pass

    def foundGuidesTrans(self):
        if self.display == True:
            if self.btnClicked == "All":
                cmds.text(("\\\\   All guides transformations founded"), parent=self.parent)
                self.logLines += [("\\\\   All guides transformations founded")]
                self._result(True)
            elif self.btnClicked == "Start":
                cmds.text(("\\\\   Finding guides transformations..."), parent=self.parent)
                self.logLines += [("\\\\   Finding guides transformations...")]
                self._result(True)
            else:
                cmds.text(("\\\\   ("+str(self.btnClicked)+") guide transformation founded"), parent=self.parent)
                self.logLines += [("\\\\   ("+str(self.btnClicked)+") guide transformation founded")]
                self._result(True)
        else: pass

    def settingJntsVariables(self):
        if self.display == True:
            cmds.text(("\\\\   Setting joints variables..."), parent=self.parent)
            self.logLines += [("\\\\   Setting joints variables...")]
            self._result(True)
        else: pass

    def createJnts(self):
        if self.display == True:
            if self.btnClicked == "All":
                cmds.text(("\\\\   All joints created"), parent=self.parent)
                self.logLines += [("\\\\   All joints created")]
                self._result(True)
            elif self.btnClicked == "Start":
                cmds.text(("\\\\   Creating joints..."), parent=self.parent)
                self.logLines += [("\\\\   Creating joints...")]
                self._result(True)
            else:
                cmds.text(("\\\\   Joint name ("+str(self.btnClicked[0])+") created in pos ("+str(self.btnClicked[1])+")"), parent=self.parent)
                self.logLines += [("\\\\   Joint name ("+str(self.btnClicked[0])+") created in pos ("+str(self.btnClicked[1])+")")]
                self._result(True)
        else: pass

    def connectJnts(self):
        if self.display == True:
            cmds.text(("\\\\   Connecting ("+str(self.btnClicked)+") joints..."), parent=self.parent)
            self.logLines += [("\\\\   Connecting ("+str(self.btnClicked)+") joints...")]
            if self.btnClicked == "21":
                cmds.text(("\\\\   Joints connected:"), parent=self.parent)
                cmds.text(("\\\\   -- Result joints"), parent=self.parent)
                cmds.text(("\\\\   -- IK/FK joints"), parent=self.parent)
                cmds.text(("\\\\   -- Auto Pv joints"), parent=self.parent)
                self.logLines += [("\\\\   Joints connected:")]
                self.logLines += [("\\\\   -- Result joints")]
                self.logLines += [("\\\\   -- IK/FK joints")]
                self.logLines += [("\\\\   -- Auto Pv joints")]
            elif self.btnClicked == "15":
                cmds.text(("\\\\   Joints connected:"), parent=self.parent)
                cmds.text(("\\\\   -- Result joints"), parent=self.parent)
                cmds.text(("\\\\   -- IK/FK joints"), parent=self.parent)
                self.logLines += [("\\\\   Joints connected:")]
                self.logLines += [("\\\\   -- Result joints")]
                self.logLines += [("\\\\   -- IK/FK joints")]
            elif self.btnClicked == "5":
                cmds.text(("\\\\   Joints connected:"), parent=self.parent)
                cmds.text(("\\\\   -- Result joints"), parent=self.parent)
                self.logLines += [("\\\\   Joints connected:")]
                self.logLines += [("\\\\   -- Result joints")]
            self._result(True)
        else: pass

    def jntChainsCreated(self):
        if self.display == True:
            cmds.text(("\\\\   Chain: "+str(self.btnClicked)), parent=self.parent)
            self.logLines += [("\\\\   Chain: "+str(self.btnClicked))]
            self._result(True)
        else: pass

    def orientJnts(self):
        if self.display == True:
            if self.btnClicked[0] == "Start":
                cmds.text(("\\\\   Orienting ("+str(self.btnClicked[1])+") joint chains..."), parent=self.parent)
                self.logLines += [("\\\\   Orienting ("+str(self.btnClicked[1])+") joint chains...")]
            elif self.btnClicked[0] == "Run":
                if self.btnClicked[1] == "5":
                    cmds.text(("\\\\   Joint chain (Result) oriented (XYX)"), parent=self.parent)
                    cmds.text(("\\\\   Joint chain (FK) oriented (XYX)"), parent=self.parent)
                    cmds.text(("\\\\   Joint chain (IK) oriented (XYX)"), parent=self.parent)
                    cmds.text(("\\\\   Joint chain (Pv) oriented (XYX)"), parent=self.parent)
                    cmds.text(("\\\\   Joint chain (NoFlip) oriented (XYX)"), parent=self.parent)
                    self.logLines += [("\\\\   Joint chain (Result) oriented (XYX)")]
                    self.logLines += [("\\\\   Joint chain (FK) oriented (XYX)")]
                    self.logLines += [("\\\\   Joint chain (IK) oriented (XYX)")]
                    self.logLines += [("\\\\   Joint chain (Pv) oriented (XYX)")]
                    self.logLines += [("\\\\   Joint chain (NoFlip) oriented (XYX)")]
                elif self.btnClicked[1] == "3":
                    cmds.text(("\\\\   Joint chain (Result) oriented (XYX)"), parent=self.parent)
                    cmds.text(("\\\\   Joint chain (FK) oriented (XYX)"), parent=self.parent)
                    cmds.text(("\\\\   Joint chain (IK) oriented (XYX)"), parent=self.parent)
                    self.logLines += [("\\\\   Joint chain (Result) oriented (XYX)")]
                    self.logLines += [("\\\\   Joint chain (FK) oriented (XYX)")]
                    self.logLines += [("\\\\   Joint chain (IK) oriented (XYX)")]
                elif self.btnClicked[1] == "1":
                    cmds.text(("\\\\   Joint chain (Result) oriented (XYX)"), parent=self.parent)
                    self.logLines += [("\\\\   Joint chain (Result) oriented (XYX)")]
                cmds.text(("\\\\   Joint chains oriented"), parent=self.parent)
                self.logLines += [("\\\\   Joint chains oriented")]
            self._result(True)
        else: pass

class buildLogHumanArm(buildLog):

    def __init__(self, msg, btn=False, parent="promptLog", dsp=True, stop=True):
        super(buildLogHumanArm, self).__init__(msg, btn, parent, dsp, stop)
        if self.message == "multLegsPropUI": self.multLegsPropUI()
        elif self.message == "addRemLegsPropUI": self.addRemLegsPropUI()
        elif self.message == "haveFingersLegsPropUI": self.haveFingersLegsPropUI()
        elif self.message == "startBuildHumanLeg": self.startBuildHumanLeg()
        elif self.message == "readFeatures": self.readFeatures()
        elif self.message == "foundGuidesTrans": self.foundGuidesTrans()
        elif self.message == "settingJntsVariables": self.settingJntsVariables()
        elif self.message == "createJnts": self.createJnts()
        elif self.message == "connectJnts": self.connectJnts()
        elif self.message == "jntChainsCreated": self.jntChainsCreated()
        elif self.message == "orientJnts": self.orientJnts()
        cmds.scrollLayout("promptLog", edit=True, sp=("down"))

    def multArmsPropUI(self):
        if self.display == True:
            if self.btnClicked == 1:
                cmds.text(("\\\\   Multiple Human Arms mode disabled"), parent=self.parent)
                self.logLines += [("\\\\   Multiple Human Arms mode disabled")]
                self._result(True)
            elif self.btnClicked == 2:
                cmds.text(("\\\\   Multiple Human Arms mode enabled"), parent=self.parent)
                self.logLines += [("\\\\   Multiple Human Arms mode enabled")]
                self._result(True)
        else: pass

    def addRemArmsPropUI(self):
        if self.display == True:
            if self.btnClicked == "add":
                cmds.text(("\\\\   Human Arm added"), parent=self.parent)
                self.logLines += [("\\\\   Human Arm added")]
                self._result(True)
            elif self.btnClicked == "rem":
                cmds.text(("\\\\   Human Arm removed"), parent=self.parent)
                self.logLines += [("\\\\   Human Arm removed")]
                self._result(True)
        else: pass

    def haveFingersArmsPropUI(self):
        if self.display == True:
            check = cmds.checkBoxGrp(("cbx"+self.btnClicked+"HaveFingersHArms"), q=True, v1=True)
            if check == True:
                cmds.text(("\\\\   Human ("+str(self.btnClicked)+") have fingers enabled"), parent=self.parent)
                self.logLines += [("\\\\   Human ("+str(self.btnClicked)+") have fingers enabled")]
                self._result(True)
            else:
                cmds.text(("\\\\   Human ("+str(self.btnClicked)+") have fingers disabled"), parent=self.parent)
                self.logLines += [("\\\\   Human ("+str(self.btnClicked)+") have fingers disabled")]
                self._result(True)
        else: pass

    def numFingersArmsPropUI(self):
        if self.display == True:
            pass
        else: pass

    def startBuildHumanArm(self):
        if self.display == True:
            if self.btnClicked == "All":
                cmds.text(("\\\\   =================[BUILDING]================="), parent=self.parent)
                cmds.text(("\\\\   "), parent=self.parent)
                cmds.text(("\\\\   ====== START BUILDING HUMAN ARMS..."), parent=self.parent)
                cmds.text(("\\\\   "), parent=self.parent)
                self.logLines += [("\\\\   =================[BUILDING]=================")]
                self.logLines += [("\\\\   ")]
                self.logLines += [("\\\\   ====== START BUILDING HUMAN ARMS...")]
                self.logLines += [("\\\\   ")]
                self._result(True)
            else:
                cmds.text(("\\\\   BUILDING ("+str(self.btnClicked)+") ..."), parent=self.parent)
                self.logLines += [("\\\\   BUILDING ("+str(self.btnClicked)+") ...")]
                self._result(True)
        else: pass

    def readFeatures(self):
        if self.display == True:
            if self.btnClicked == "All":
                cmds.text(("\\\\   All human arms features readed"), parent=self.parent)
                self.logLines += [("\\\\   All human arms features readed")]
                self._result(True)
            elif self.btnClicked == "Start":
                cmds.text(("\\\\   Reading all human arms features..."), parent=self.parent)
                self.logLines += [("\\\\   Reading all human arms features...")]
                self._result(True)
        else: pass

    def foundGuidesTrans(self):
        if self.display == True:
            if self.btnClicked == "All":
                cmds.text(("\\\\   All guides transformations founded"), parent=self.parent)
                self.logLines += [("\\\\   All guides transformations founded")]
                self._result(True)
            elif self.btnClicked == "Start":
                cmds.text(("\\\\   Finding guides transformations..."), parent=self.parent)
                self.logLines += [("\\\\   Finding guides transformations...")]
                self._result(True)
            else:
                cmds.text(("\\\\   ("+str(self.btnClicked)+") guide transformation founded"), parent=self.parent)
                self.logLines += [("\\\\   ("+str(self.btnClicked)+") guide transformation founded")]
                self._result(True)
        else: pass

    def settingJntsVariables(self):
        if self.display == True:
            cmds.text(("\\\\   Setting joints variables..."), parent=self.parent)
            self.logLines += [("\\\\   Setting joints variables...")]
            self._result(True)
        else: pass

    def createJnts(self):
        if self.display == True:
            if self.btnClicked == "All":
                cmds.text(("\\\\   All joints created"), parent=self.parent)
                self.logLines += [("\\\\   All joints created")]
                self._result(True)
            elif self.btnClicked == "Start":
                cmds.text(("\\\\   Creating joints..."), parent=self.parent)
                self.logLines += [("\\\\   Creating joints...")]
                self._result(True)
            else:
                cmds.text(("\\\\   Joint name ("+str(self.btnClicked[0])+") created in pos ("+str(self.btnClicked[1])+")"), parent=self.parent)
                self.logLines += [("\\\\   Joint name ("+str(self.btnClicked[0])+") created in pos ("+str(self.btnClicked[1])+")")]
                self._result(True)
        else: pass

    def connectJnts(self):
        if self.display == True:
            cmds.text(("\\\\   Connecting ("+str(self.btnClicked)+") joints..."), parent=self.parent)
            self.logLines += [("\\\\   Connecting ("+str(self.btnClicked)+") joints...")]
            if self.btnClicked == "21":
                cmds.text(("\\\\   Joints connected:"), parent=self.parent)
                cmds.text(("\\\\   -- Result joints"), parent=self.parent)
                cmds.text(("\\\\   -- IK/FK joints"), parent=self.parent)
                cmds.text(("\\\\   -- Auto Pv joints"), parent=self.parent)
                self.logLines += [("\\\\   Joints connected:")]
                self.logLines += [("\\\\   -- Result joints")]
                self.logLines += [("\\\\   -- IK/FK joints")]
                self.logLines += [("\\\\   -- Auto Pv joints")]
            elif self.btnClicked == "15":
                cmds.text(("\\\\   Joints connected:"), parent=self.parent)
                cmds.text(("\\\\   -- Result joints"), parent=self.parent)
                cmds.text(("\\\\   -- IK/FK joints"), parent=self.parent)
                self.logLines += [("\\\\   Joints connected:")]
                self.logLines += [("\\\\   -- Result joints")]
                self.logLines += [("\\\\   -- IK/FK joints")]
            elif self.btnClicked == "5":
                cmds.text(("\\\\   Joints connected:"), parent=self.parent)
                cmds.text(("\\\\   -- Result joints"), parent=self.parent)
                self.logLines += [("\\\\   Joints connected:")]
                self.logLines += [("\\\\   -- Result joints")]
            self._result(True)
        else: pass

    def jntChainsCreated(self):
        if self.display == True:
            cmds.text(("\\\\   Chain: "+str(self.btnClicked)), parent=self.parent)
            self.logLines += [("\\\\   Chain: "+str(self.btnClicked))]
            self._result(True)
        else: pass

    def orientJnts(self):
        if self.display == True:
            if self.btnClicked[0] == "Start":
                cmds.text(("\\\\   Orienting ("+str(self.btnClicked[1])+") joint chains..."), parent=self.parent)
                self.logLines += [("\\\\   Orienting ("+str(self.btnClicked[1])+") joint chains...")]
            elif self.btnClicked[0] == "Run":
                if self.btnClicked[1] == "5":
                    cmds.text(("\\\\   Joint chain (Result) oriented (XYX)"), parent=self.parent)
                    cmds.text(("\\\\   Joint chain (FK) oriented (XYX)"), parent=self.parent)
                    cmds.text(("\\\\   Joint chain (IK) oriented (XYX)"), parent=self.parent)
                    cmds.text(("\\\\   Joint chain (Pv) oriented (XYX)"), parent=self.parent)
                    cmds.text(("\\\\   Joint chain (NoFlip) oriented (XYX)"), parent=self.parent)
                    self.logLines += [("\\\\   Joint chain (Result) oriented (XYX)")]
                    self.logLines += [("\\\\   Joint chain (FK) oriented (XYX)")]
                    self.logLines += [("\\\\   Joint chain (IK) oriented (XYX)")]
                    self.logLines += [("\\\\   Joint chain (Pv) oriented (XYX)")]
                    self.logLines += [("\\\\   Joint chain (NoFlip) oriented (XYX)")]
                elif self.btnClicked[1] == "3":
                    cmds.text(("\\\\   Joint chain (Result) oriented (XYX)"), parent=self.parent)
                    cmds.text(("\\\\   Joint chain (FK) oriented (XYX)"), parent=self.parent)
                    cmds.text(("\\\\   Joint chain (IK) oriented (XYX)"), parent=self.parent)
                    self.logLines += [("\\\\   Joint chain (Result) oriented (XYX)")]
                    self.logLines += [("\\\\   Joint chain (FK) oriented (XYX)")]
                    self.logLines += [("\\\\   Joint chain (IK) oriented (XYX)")]
                elif self.btnClicked[1] == "1":
                    cmds.text(("\\\\   Joint chain (Result) oriented (XYX)"), parent=self.parent)
                    self.logLines += [("\\\\   Joint chain (Result) oriented (XYX)")]
                cmds.text(("\\\\   Joint chains oriented"), parent=self.parent)
                self.logLines += [("\\\\   Joint chains oriented")]
            self._result(True)
        else: pass
