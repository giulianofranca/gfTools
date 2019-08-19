import maya.cmds as cmds
import maya.mel as mel
from functools import partial


from gfTools.gfAutoRig.settings import guides
from gfTools.gfAutoRig.settings import log
from gfTools.gfAutoRig.settings.uiConfig import HSpineUIConfig as HSpineUI
from gfTools.gfAutoRig.settings.uiConfig import HLegsUIConfig as HLegsUI
from gfTools.gfAutoRig.settings.uiConfig import HArmsUIConfig as HArmsUI
from gfTools.gfAutoRig.settings.uiConfig import HHeadsUIConfig as HHeadsUI
reload(guides); reload(log); reload(HLegsUI); reload(HArmsUI); reload(HSpineUI); reload(HHeadsUI)


class config(object):

    def __init__(self, *args):
        self.OutFeatLay = "scrOutputs"
        self.PropLay = "scrProperties"
        self.tabProperties = "tabProperties"
        self.nUI = "gfAutoRigUI"
        self.tUI = "gfAutoRig"
        self.promptLog = "promptLog"

    # SET THE CHARACTER NAME
    def setCharName(self, *args):
        charName = cmds.textFieldGrp("txtCharName", q=True, tx=True)
        log.buildLog(msg="setCharNameUI", btn=charName, stop=True)

    # SET THE CHARACTER TYPE
    def setCharType(self, *args):
        charType = cmds.optionMenu("optCharType", q=True, v=True)
        cmds.textFieldGrp("txtCharTypeCGeo", edit=True, tx=charType)
        if charType != "Select Type":
            log.buildLog(msg="setCharTypeUI", btn=charType, stop=True)
        else: pass

    def findGeometryFieldsVal(self, ct=""):
        fields = []
        if ct == "Biped Human":
            fields.append(cmds.textFieldGrp("txtBaseBodyCGeo", q=True, tx=True))
            fields.append(cmds.textFieldGrp("txtLeftEyeCGeo", q=True, tx=True))
            fields.append(cmds.textFieldGrp("txtRightEyeCGeo", q=True, tx=True))
            fields.append(cmds.textFieldGrp("txtUpperTeethCGeo", q=True, tx=True))
            fields.append(cmds.textFieldGrp("txtLowerTeethCGeo", q=True, tx=True))
            fields.append(cmds.textFieldGrp("txtTongueCGeo", q=True, tx=True))
            fNames = {0:'txtBaseBodyCGeo', 1:'txtLeftEyeCGeo', 2:'txtRightEyeCGeo', 3:'txtUpperTeethCGeo', 4:'txtLowerTeethCGeo', 5:'txtTongueCGeo'}
        return fields, fNames

    # ADD SELECTED GEOMETRY IN GEOMETRY LIST
    def addGeometry(self, index, txt="", *args):
        # Detect selection and her childs
        oldSel = cmds.ls(sl=True, typ="transform")
        oldSelChildren = []
        x = 0
        newSel = []
        numGrp = 0
        for o in oldSel:
            oldSelChildren.append(cmds.listRelatives(o, c=True))
        # Remove groups of the new selection
        while(x < len(oldSelChildren)):
            if cmds.ls(oldSelChildren[x], tr=True):
                numGrp += 1
            else:
                newSel.append(oldSel[x])
            x += 1
        # print("\n"+str(numGrp)+" groups detected!") -----------------------------------------------> PRINT
        # print("Your non-groups selected: "+str(newSel)) -----------------------------------------------> PRINT
        # Add only meshes in geometry list
        newSelShapes = cmds.listRelatives(newSel, s=True)
        x = 0
        # Fing char type
        charType = cmds.optionMenu("optCharType", q=True, v=True)
        if charType == "Select Type": cmds.warning("Select your char type!"); return False
        cmds.textFieldGrp(txt, edit=True, tx=newSel[0])
        # Find Fields
        fields, fNames = self.findGeometryFieldsVal(ct=charType)
        # print ("\n My Fields = %s") %(fields) -----------------------------------------------> PRINT
        newList = []
        cmds.textScrollList("lstAllGeo", edit=True, ra=True)
        # Setting the final list
        for f in fields:
            if not f == '':
                newList.append(f)
        # Append list to UI
        for l in newList:
            cmds.textScrollList("lstAllGeo", edit=True, a=[l])
        cmds.setAttr((newSel[0]+".overrideDisplayType"), 0)
        cmds.setAttr((newSel[0]+".overrideEnabled"), False)
        cmds.select(cl=True)
        log.buildLog(msg=None, stop=True)

    # REMOVE SELECTED GEOMETRY IN GEOMETRY LIST
    def removeGeometry(self, *args):
        charType = cmds.optionMenu("optCharType", q=True, v=True)
        if charType == "Select Type": cmds.warning("Select your char type!"); return False
        fields, fNames = self.findGeometryFieldsVal(ct=charType)
        sel = cmds.textScrollList("lstAllGeo", q=True, si=True)
        if sel == None: cmds.warning("Select at least one object!"); return False
        for s in sel:
            cmds.textScrollList("lstAllGeo", edit=True, ri=s)
            cmds.setAttr((s+".overrideDisplayType"), 0)
            cmds.setAttr((s+".overrideEnabled"), False)
            for x in range(0, len(fNames)):
                if cmds.textFieldGrp(fNames[x], q=True, tx=True) == s:
                    cmds.textFieldGrp(fNames[x], edit=True, tx='')
            log.buildLog(msg="removeGeometryUI", btn=s, stop=False)
        log.buildLog(msg=None, stop=True)

    # REMOVE ALL GEOMETRY IN GEOMETRY LIST
    def clearGeometry(self, *args):
        charType = cmds.optionMenu("optCharType", q=True, v=True)
        if charType == "Select Type": cmds.warning("Select your char type!"); return False
        fields, fNames = self.findGeometryFieldsVal(ct=charType)
        lst = cmds.textScrollList("lstAllGeo", q=True, ai=True)
        for l in lst:
            cmds.setAttr((l+".overrideDisplayType"), 0)
            cmds.setAttr((l+".overrideEnabled"), False)
        cmds.textScrollList("lstAllGeo", edit=True, ra=True)
        for x in range(0, len(fNames)):
            cmds.textFieldGrp(fNames[x], edit=True, tx='')
        log.buildLog(msg="clearGeometryUI", stop=True)

    def wireGeometry(self, *args):
        listedGeo = cmds.textScrollList("lstAllGeo", q=True, ai=True)
        if not listedGeo == None:
            for geo in listedGeo:
                if cmds.getAttr((geo+".overrideEnabled")) == False:
                    cmds.setAttr((geo+".overrideEnabled"), True)
                    cmds.setAttr((geo+".overrideDisplayType"), 1)
                elif cmds.getAttr((geo+".overrideEnabled")) == True:
                    cmds.setAttr((geo+".overrideDisplayType"), 0)
                    cmds.setAttr((geo+".overrideEnabled"), False)

    # SELECT GEOMETRY SELECTED IN GEOMETRY LIST
    def selectGeometry(self, *args):
        selItem = cmds.textScrollList("lstAllGeo", q=True, si=True)
        cmds.select(selItem, r=True)
        for s in selItem:
            log.buildLog(msg="selectGeometryUI", btn=s, stop=False)
        cmds.textScrollList("lstAllGeo", edit=True, da=True)
        log.buildLog(msg=None, stop=True)

    # VERIFY WHAT COMPONENTS IS ALREADY CREATED
    def verifyChildsCharField(self, *args):
        Childs = cmds.layout(self.OutFeatLay, q=True, ca=True)
        return Childs

    # ADD COMPONENTS IN UI
    def setComponentCharField(self, oldChilds, newChild): # <<<-------------------------------------------- MELHORAR
        Childs = []
        #print(oldChilds)
        if oldChilds != None:
            Childs.extend(oldChilds)
        else: pass
        Childs.append(newChild)
        for c in Childs:
            self.checkAddComponentsCharField(c)
        return True

    # DELETE COMPONENTS IN UI
    def deleteAllChildsCharField(self, childs, unique, logUnique=True, *args):
        if unique == True:
            cmds.deleteUI(childs)
            log.buildLog(msg="componentDeletedUI", btn=childs, stop=False)
            deleteProp = self.verifyPropertiesCharField(childs)
            if deleteProp != 'NDA':
                cmds.deleteUI(deleteProp)
                log.buildLog(msg="deletePropertiesUI", btn=childs, stop=False)
                OldChilds = self.verifyChildsCharField()
                if OldChilds == None:
                    guides.loadGuides()._DeleteHierarchy()
                guides.loadGuides().deleteGuides(childs)
                self.loadComponentProperties("<<<Master Features>>>")
            else:
                cmds.warning("Properties don't finded")
        elif unique == False:
            if childs != None:
                for old in childs:
                    cmds.deleteUI(old)
                    log.buildLog(msg="componentDeletedUI", btn=old, stop=False) # <<< ---------------------------------------------------  AQUI
                    deleteProp = self.verifyPropertiesCharField(old)
                    if deleteProp != 'NDA':
                        cmds.deleteUI(deleteProp)
                        log.buildLog(msg="deletePropertiesUI", btn=old, stop=False)
                    else:
                        cmds.warning("Properties don't finded")
                    log.buildLog(msg="componentDeletedUI", btn=old, stop=False)
                self.loadComponentProperties("<<<Master Features>>>")
        else:
            cmds.warning("\nNDA")
        if logUnique == True: log.buildLog(msg=None, stop=True)
        else: log.buildLog(msg=None, stop=False)

    # CREATE/RELOAD COMPONENTS IN UI
    def reloadCharField(self, btnClicked, reloadAll, method="NDA", logUnique=True, *args):
        #self.reloadCharField("compHumanLegs", False) # Adicionar Component na tabela (Name, DeleteAll?)
        #self.reloadCharField("compHumanLegs", True) # Limpar e Adicionar Component na tabela (Name, DeleteAll?)
        #self.reloadCharField(None, True) # Limpar todos Components na tabela (Name, DeleteAll?)
        #self.reloadCharField(None, False) # Verificar Components na tabela (Name, DeleteAll?)

        # Verify what childs is already created
        OldChilds = self.verifyChildsCharField()
        if reloadAll == True:
            # Delete all childs clearComponentsUI
            log.buildLog(msg="clearComponentsUI")
            self.deleteAllChildsCharField(OldChilds, False, False)
            if cmds.objExists("gfARGuides:Grp_Guides"):
                guides.loadGuides()._DeleteHierarchy()
            OldChilds = []
            if method == "Create":
                self.setComponentCharField(None, btnClicked)
            else: pass
        elif reloadAll == False:
            # Maintain old childs
            if OldChilds != None:
                # If char field contain old childs
                if btnClicked in OldChilds:
                    # If component clicked already created
                    cmds.warning("Component already exists!")
                    log.buildLog(msg="componentExistsUI", btn=btnClicked, stop=False)
                else:
                    # If component clicked was not created
                    if btnClicked != None:
                        # If component clicked is not invalid create component
                        if method == "Create":
                            OldChilds = self.verifyChildsCharField()
                            if OldChilds == None:
                                guides.loadGuides()._SetHierarchy()
                            self.setComponentCharField(None, btnClicked)
                            log.buildLog(msg="componentCreatedUI", btn=btnClicked, stop=False)
                            properties = self.verifyPropertiesCharField(btnClicked)
                            self.createComponentProperties(properties)
                            log.buildLog(msg="createPropertiesUI", btn=btnClicked, stop=False)
                            # Create Guides # <<<----------------------------------------------------------------- MELHORAR
                            guides.loadGuides().buildGuides(btnClicked)
                        else: pass
                    else:
                        # If component clicked is invalid
                        cmds.warning("Component invalid! Check core gui code to fix...")
            else:
                # Reload old childs and add new childs
                if btnClicked != None:
                    # If component clicked is not invalid create component
                    if method == "Create":
                        OldChilds = self.verifyChildsCharField()
                        if OldChilds == None:
                            guides.loadGuides()._SetHierarchy()
                        self.setComponentCharField(None, btnClicked)
                        log.buildLog(msg="componentCreatedUI", btn=btnClicked, stop=False)
                        properties = self.verifyPropertiesCharField(btnClicked)
                        self.createComponentProperties(properties)
                        log.buildLog(msg="createPropertiesUI", btn=btnClicked, stop=False)
                        # Create Guides # <<<----------------------------------------------------------------- MELHORAR
                        guides.loadGuides().buildGuides(btnClicked)
                    else: pass
                else:
                    # If component clicked is invalid
                    cmds.warning("Component invalid! Check core gui code to fix...")
        if logUnique == True: log.buildLog(msg=None, stop=True)
        else: log.buildLog(msg=None, stop=False)

    # --------------------------------------------------------------------------------------------------------
    # ADD COMPONENTS BUTTONS TO UI                              <<< ADICIONAR FERRAMENTAS AQUI >>>
    # --------------------------------------------------------------------------------------------------------
    def loadComponentsUI(self):
        cmds.button("btnHumanSpine", l="Human Spine", w=136, h=40, p="scrComponents", c=partial(self.reloadCharField, "compHumanSpine", False, "Create", True))
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnHumanLegs", l="Human Legs", w=136, h=40, p="scrComponents", c=partial(self.reloadCharField, "compHumanLegs", False, "Create", True))
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnHumanArms", l="Human Arms", w=136, h=40, p="scrComponents", c=partial(self.reloadCharField, "compHumanArms", False, "Create", True))
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnHumanHead", l="Human Head", w=136, h=40, p="scrComponents", c=partial(self.reloadCharField, "compHumanHead", False, "Create", True))
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnCreatureTail", l="Creature Tail", w=136, h=40, p="scrComponents", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnCreatureTentacle", l="Creature Tentacle", w=136, h=40, p="scrComponents", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnBirdSpine", l="Bird Spine", w=136, h=40, p="scrComponents", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnBirdLeg", l="Bird Leg", w=136, h=40, p="scrComponents", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnBirdWing", l="Bird Wing", w=136, h=40, p="scrComponents", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnBirdTail", l="Bird Tail", w=136, h=40, p="scrComponents", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnBirdNeck", l="Bird Neck", w=136, h=40, p="scrComponents", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnBirdHead", l="Bird Head", w=136, h=40, p="scrComponents", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnCarChassis", l="Car Chassis", w=136, h=40, p="scrComponents", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnCarWheel", l="Car Wheel", w=136, h=40, p="scrComponents", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnCarSuspension", l="Car Suspension", w=136, h=40, p="scrComponents", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnCarDoor", l="Car Door", w=136, h=40, p="scrComponents", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnCarHood", l="Car Hood", w=136, h=40, p="scrComponents", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnCarTrunk", l="Car Trunk", w=136, h=40, p="scrComponents", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button("btnTankTreads", l="Tank Treads", w=136, h=40, p="scrComponents", en=False)
        cmds.separator(w=136, h=3, st="none")

    # --------------------------------------------------------------------------------------------------------
    # ADD PRESETS BUTTONS TO UI                                 <<< ADICIONAR FERRAMENTAS AQUI >>>
    # --------------------------------------------------------------------------------------------------------
    def loadPresetsUI(self):
        cmds.button(l="Biped Human", w=136, h=40, p="scrPresets", c=partial(self.loadBuiltInPresetCharField, "Biped Human"))
        cmds.separator(w=136, h=3, st="none")
        cmds.button(l="Biped Creature", w=136, h=40, p="scrPresets", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button(l="Quadruped", w=136, h=40, p="scrPresets", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button(l="Fish", w=136, h=40, p="scrPresets", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button(l="Bird", w=136, h=40, p="scrPresets", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button(l="Octopus", w=136, h=40, p="scrPresets", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button(l="Turtle", w=136, h=40, p="scrPresets", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button(l="Car", w=136, h=40, p="scrPresets", en=False)
        cmds.separator(w=136, h=3, st="none")
        cmds.button(l="Tank", w=136, h=40, p="scrPresets", en=False)
        cmds.separator(w=136, h=3, st="none")

    # --------------------------------------------------------------------------------------------------------
    # VERIFY AND CONVERT COMPONENTS TO PROPERTIES               <<< ADICIONAR FERRAMENTAS AQUI >>>
    # --------------------------------------------------------------------------------------------------------
    def verifyPropertiesCharField(self, obj, *args):
        return{
            'compHumanSpine': 'layHumanSpine',
            'compHumanLegs': 'layHumanLegs',
            'compHumanArms': 'layHumanArms',
            'compHumanHead': 'layHumanHead',
            }.get(obj, 'NDA')

    # --------------------------------------------------------------------------------------------------------
    # ADD COMPONENTS TO UI                                       <<< ADICIONAR FERRAMENTAS AQUI >>>
    # --------------------------------------------------------------------------------------------------------
    def checkAddComponentsCharField(self, add):
        if add == "compHumanSpine": self.addComponentCharField("compHumanSpine")
        elif add == "compHumanLegs": self.addComponentCharField("compHumanLegs")
        elif add == "compHumanArms": self.addComponentCharField("compHumanArms")
        elif add == "compHumanHead": self.addComponentCharField("compHumanHead")

    # --------------------------------------------------------------------------------------------------------
    # DELETE COMPONENTS PROPERTIES VISIBLE                       <<< ADICIONAR FERRAMENTAS AQUI >>>
    # --------------------------------------------------------------------------------------------------------
    def deleteComponentProperties(self):
        cmds.columnLayout("layMasterFeat", edit=True, vis=False)
        cmds.columnLayout("layEditCharGeo", edit=True, vis=False)
        if(cmds.columnLayout("layHumanSpine", exists=True)):
            cmds.columnLayout("layHumanSpine", edit=True, vis=False)
        if(cmds.columnLayout("layHumanLegs", exists=True)):
            cmds.columnLayout("layHumanLegs", edit=True, vis=False)
        if(cmds.columnLayout("layHumanArms", exists=True)):
            cmds.columnLayout("layHumanArms", edit=True, vis=False)
        if(cmds.columnLayout("layHumanHead", exists=True)):
            cmds.columnLayout("layHumanHead", edit=True, vis=False)

    # --------------------------------------------------------------------------------------------------------
    # LOAD COMPONENTS PRESETS TO UI                              <<< ADICIONAR FERRAMENTAS AQUI >>>
    # --------------------------------------------------------------------------------------------------------
    def loadBuiltInPresetCharField(self, presetName, *args):
        if presetName == "Biped Human":
            self.reloadCharField("", True, "NDA", True)
            log.buildLog(btn="Human Biped", msg="loadBuiltInPresetUI", stop=True)
            self.reloadCharField("compHumanSpine", False, "Create", False)
            self.reloadCharField("compHumanLegs", False, "Create", False)
            self.reloadCharField("compHumanArms", False, "Create", False)
            self.reloadCharField("compHumanHead", False, "Create", True)

    # --------------------------------------------------------------------------------------------------------
    # CREATE COMPONENTS INTERFACE                                <<< ADICIONAR FERRAMENTAS AQUI >>>
    # --------------------------------------------------------------------------------------------------------
    def addComponentCharField(self, childName):
        DarkGrey = [0.18, 0.18, 0.18]
        LightGrey = [0.35, 0.35, 0.35]
        SoftYellow = [0.96078, 0.84314, 0.43137]
        if childName == "compHumanSpine":
            # Human Spine
            cmds.gridLayout("compHumanSpine", w=197, h=43, nc=1, cwh=(210,40), parent=self.OutFeatLay)
            cmds.rowLayout(w=197, h=40, nc=6, bgc=[DarkGrey[0], DarkGrey[1], DarkGrey[2]])
            cmds.separator(w=5, h=3, st="none")
            cmds.text(l="Human Spine")
            cmds.separator(w=46, h=3, st="none")
            cmds.button(l="Del", bgc=[LightGrey[0], LightGrey[1], LightGrey[2]], c=partial(self.deleteAllChildsCharField, "compHumanSpine", True, "NDA", False))
            cmds.separator(w=1, h=3, st="none")
            cmds.button(l="Edit", bgc=[LightGrey[0], LightGrey[1], LightGrey[2]], c=partial(self.loadComponentProperties, "Human Spine"))
        elif childName == "compHumanLegs":
            # Human Legs
            cmds.gridLayout("compHumanLegs", w=197, h=43, nc=1, cwh=(210,40), parent=self.OutFeatLay)
            cmds.rowLayout(w=197, h=40, nc=8, bgc=[DarkGrey[0], DarkGrey[1], DarkGrey[2]])
            cmds.separator(w=5, h=3, st="none")
            cmds.text(l="Human Legs")
            cmds.separator(w=25, h=3, st="none")
            cmds.textField("txtNumberHLegs", w=20, tx="2", ed=False, bgc=[SoftYellow[0], SoftYellow[1], SoftYellow[2]])
            cmds.separator(w=3, h=3, st="none")
            cmds.button(l="Del", bgc=[LightGrey[0], LightGrey[1], LightGrey[2]], c=partial(self.deleteAllChildsCharField, "compHumanLegs", True, "NDA", False))
            cmds.separator(w=1, h=3, st="none")
            cmds.button(l="Edit", bgc=[LightGrey[0], LightGrey[1], LightGrey[2]], c=partial(self.loadComponentProperties, "Human Legs"))
        elif childName == "compHumanArms":
            # Human Arms
            cmds.gridLayout("compHumanArms", w=197, h=43, nc=1, cwh=(210,40), parent=self.OutFeatLay)
            cmds.rowLayout(w=197, h=40, nc=8, bgc=[DarkGrey[0], DarkGrey[1], DarkGrey[2]])
            cmds.separator(w=5, h=3, st="none")
            cmds.text(l="Human Arms")
            cmds.separator(w=23, h=3, st="none")
            cmds.textField("txtNumberHArms", w=20, tx="2", ed=False, bgc=[SoftYellow[0], SoftYellow[1], SoftYellow[2]])
            cmds.separator(w=3, h=3, st="none")
            cmds.button(l="Del", bgc=[LightGrey[0], LightGrey[1], LightGrey[2]], c=partial(self.deleteAllChildsCharField, "compHumanArms", True, "NDA", False))
            cmds.separator(w=1, h=3, st="none")
            cmds.button(l="Edit", bgc=[LightGrey[0], LightGrey[1], LightGrey[2]], c=partial(self.loadComponentProperties, "Human Arms"))
        elif childName == "compHumanHead":
            # Human Head
            cmds.gridLayout("compHumanHead", w=197, h=43, nc=1, cwh=(210,40), parent=self.OutFeatLay)
            cmds.rowLayout(w=197, h=40, nc=8, bgc=[DarkGrey[0], DarkGrey[1], DarkGrey[2]])
            cmds.separator(w=5, h=3, st="none")
            cmds.text(l="Human Head")
            cmds.separator(w=21, h=3, st="none")
            cmds.textField(w=20, tx="1", ed=False, bgc=[SoftYellow[0], SoftYellow[1], SoftYellow[2]])
            cmds.separator(w=3, h=3, st="none")
            cmds.button(l="Del", bgc=[LightGrey[0], LightGrey[1], LightGrey[2]], c=partial(self.deleteAllChildsCharField, "compHumanHead", True, "NDA", False))
            cmds.separator(w=1, h=3, st="none")
            cmds.button(l="Edit", bgc=[LightGrey[0], LightGrey[1], LightGrey[2]], c=partial(self.loadComponentProperties, "Human Head"))
        elif childName == "NDA":
            cmds.warning("\nNDA")

    # --------------------------------------------------------------------------------------------------------
    # CREATE PROPERTIES INTERFACE                                <<< ADICIONAR FERRAMENTAS AQUI >>>
    # --------------------------------------------------------------------------------------------------------
    def createComponentProperties(self, comp):
        DarkGrey = [0.18, 0.18, 0.18]
        Grey = [0.29, 0.29, 0.29]
        if comp == "layHumanSpine":
            cmds.columnLayout("layHumanSpine", w=308, vis=False, parent=self.PropLay)
            cmds.frameLayout("frmMainSettingsHSpine", w=318, cl=False, cll=True, bgs=True, l="Spine Main Settings")
            cmds.separator(w=5, h=1, st="none")
            cmds.rowLayout("layNumJntsHSpine", nc=2)
            cmds.intSliderGrp("intNumJntsHSpine", l="Number of joints: ", cw=([(1, 120), (2, 40), (3, 130)]), f=True, min=2, max=5, fmn=2, fmx=5, v=3, cc=partial(guides.loadGuides().reloadGuides, "intNumJntsHSpine", ""))
            cmds.setParent('..')
            cmds.rowLayout("layTangentCtrlsHSpine", nc=2, en=False)
            cmds.checkBoxGrp("cbxTangentCtrlsHSpine", l="Tangent Ctrls: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Control spine with tangents)")
            cmds.setParent('..')
            cmds.rowLayout("layScaleSpineHSpine", nc=2, en=False)
            cmds.checkBoxGrp("cbxScaleSpineHSpine", l="Scale Spine: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Scale spine uniformly)")
            cmds.setParent('..')
            cmds.rowLayout("layHybridTypeHSpine", nc=1, en=False)
            cmds.radioButtonGrp("radHybridTypeHSpine", l="Hybrid Type: ", nrb=2, la2=["IK Spline", "Ribbon"], cw=([(1, 120), (2, 80)]), sl=1, onc=partial(HSpineUI.setHybridTypeHSpine))
            cmds.setParent('..')
            cmds.separator(w=5, h=1, st="none")
            cmds.setParent("layHumanSpine")
            cmds.frameLayout("frmIKSplineSettingsHSpine", w=318, cl=True, cll=True, bgs=True, l="IK Spline Settings", en=True)
            cmds.separator(w=5, h=1, st="none")
            cmds.optionMenuGrp("optEnIKSplineHSpine", l="Enable IK Spline: ", cw2=(120, 120), cc=partial(HSpineUI.enableIKSplineHSpine))
            cmds.menuItem(l="Disabled")
            cmds.menuItem(l="Enabled")
            cmds.rowLayout("layNumIKSplineJntsHSpine", nc=2, en=False)
            cmds.intSliderGrp("intNumIKSplineJntsHSpine", l="Number of joints: ", cw=([(1, 120), (2, 40), (3, 130)]), f=True, min=3, max=15, fmn=3, fmx=15, v=7)
            cmds.setParent('..')
            cmds.rowLayout("layTwistIKHSpine", nc=2, en=False)
            cmds.checkBoxGrp("cbxTwistIKHSpine", l="Twist IK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Enable IK spline to twist)")
            cmds.setParent('..')
            cmds.rowLayout("layStretchIKHSpine", nc=2, en=False)
            cmds.checkBoxGrp("cbxStretchIKHSpine", l="Stretch IK: ", ncb=1, cw=([(1, 120), (2, 70)]), cc=partial(HSpineUI.enableStretchIKHSpine))
            cmds.text(l="(Enable IK spine to stretch)")
            cmds.setParent('..')
            cmds.rowLayout("layStretckIKMultHSpine", nc=2, en=False)
            cmds.checkBoxGrp("cbxStretckIKMultHSpine", l="Stretch multipliers: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Multiply stretch to a value)")
            cmds.setParent('..')
            cmds.rowLayout("layClampStretchHSpine", nc=2, en=False)
            cmds.checkBoxGrp("cbxClampStretchHSpine", l="Clamp stretch: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Clamp stretch to a value)")
            cmds.setParent('..')
            cmds.rowLayout("laySquashIKHSpine", nc=2, en=False)
            cmds.checkBoxGrp("cbxSquashIKHSpine", l="Squash IK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Enable IK spine to squash)")
            cmds.setParent('..')
            cmds.rowLayout("laySquashIKMultHSpine", nc=2, en=False)
            cmds.checkBoxGrp("cbxSquashIKMultHSpine", l="Squash multipliers: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Multiply squash to a value)")
            cmds.setParent('..')
            cmds.rowLayout("layTweakIKHSpine", nc=2, en=False)
            cmds.checkBoxGrp("cbxBendIKHSpine", l="Bend controller: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Ctrl to bend middle of spine)")
            cmds.setParent('..')
            cmds.separator(w=5, h=1, st="none")
            cmds.setParent("layHumanSpine")
            cmds.frameLayout("frmRibbonSettingsHSpine", w=318, cl=True, cll=True, bgs=True, l="Ribbon Settings", en=False)
            cmds.separator(w=5, h=1, st="none")
            cmds.optionMenuGrp("optEnRibbonHSpine", l="Enable Ribbon: ", cw2=(120, 120), cc=partial(HSpineUI.enableRibbonHSpine))
            cmds.menuItem(l="Disabled")
            cmds.menuItem(l="Enabled")
            cmds.rowLayout("layNumRibJntsHSpine", nc=2, en=False)
            cmds.intSliderGrp("intNumRibJntsHSpine", l="Number of joints: ", cw=([(1, 120), (2, 40), (3, 130)]), f=True, min=3, max=15, fmn=3, fmx=15, v=7)
            cmds.setParent('..')
            cmds.rowLayout("layBendCtrlsHSpine", nc=2, en=False)
            cmds.checkBoxGrp("cbxBendCtrlsHSpine", l="Bend ctrls: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layTweakCtrlsHSpine", nc=2, en=False)
            cmds.checkBoxGrp("cbxTweakCtrlsHSpine", l="Tweak ctrls: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layTwistAttrsHSpine", nc=2, en=False)
            cmds.checkBoxGrp("cbxTwistAttrsHSpine", l="Twist attrs: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("laySineAttrsHSpine", nc=2, en=False)
            cmds.checkBoxGrp("cbxSineAttrsHSpine", l="Sine attrs: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layStretchAttrsHSpine", nc=2, en=False)
            cmds.checkBoxGrp("cbxStretchAttrsHSpine", l="Stretch attrs: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Don't working yet, sry)")
            cmds.setParent('..')
            cmds.rowLayout("layExtraFreeSlotsHSpine", nc=2, en=False)
            cmds.checkBoxGrp("cbxExtraFreeSlotsHSpine", l="Extra free slots: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layNumExtraSlotsHSpine", nc=2, en=False)
            cmds.intSliderGrp("intNumExtraSlotsHSpine", l="Number extra slots: ", cw=([(1, 120), (2, 40), (3, 130)]), f=True, min=1, max=3, fmn=1, fmx=3, v=1)
            cmds.setParent('..')
            cmds.separator(w=5, h=1, st="none")
            cmds.setParent("layHumanSpine")
        elif comp == "layHumanLegs":
            # Human Legs
            cmds.columnLayout("layHumanLegs", w=308, vis=False, parent=self.PropLay)
            cmds.frameLayout("frmMainSettingsHLegs", w=318, cl=False, cll=True, bgs=True, l="Legs Main Settings")
            cmds.separator(w=5, h=1, st="none")
            cmds.rowLayout("layHaveHipHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxHaveHipHLegs", l="Have Unique Hip: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Don't working yet, sry)")
            cmds.setParent('..')
            cmds.rowLayout(w=315, nc=1, cl1="left")
            cmds.radioButtonGrp("radMultLegsHLegs", l="Multiple Legs: ", nrb=2, la2=["No", "Yes"], cw=([(1, 120), (2, 50)]), sl=1, onc=partial(HLegsUI.multipleLegsHLegs))
            cmds.setParent('..')
            cmds.rowLayout("layMultLegsHLegs", nc=4, en=False)
            cmds.separator(w=40, h=3, st="single", bgc=[Grey[0], Grey[1], Grey[2]])   # <<<----------------------------------------------------------------------------------------------- OLHAR AQUI
            cmds.button("btnAddLegHLegs", w=120, l="Add Leg", c=partial(HLegsUI.addHLegs))
            cmds.separator(w=5, h=3, st="none")
            cmds.button("btnRemLegHLegs", w=120, l="Remove Leg", en=False, c=partial(HLegsUI.remHLegs))
            cmds.setParent('..')
            cmds.rowColumnLayout("layMultHumanLegsHLegs", w=300, nc=1)
            cmds.rowLayout("layMultLLegHLegs", w=310, nc=2)
            cmds.separator(w=5, h=3, st="none")
            cmds.frameLayout("frmLeftLegHLegs", w=312, cl=True, cll=True, bgs=True, l="Left Leg")
            cmds.textFieldGrp("txtLLegParentHLegs", l="Leg Parent: ", cw2=(110, 120), tx="None", ed=False)
            cmds.checkBoxGrp("cbxLLegHaveFingersHLegs", l="Have fingers: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(HLegsUI.haveFingersHLegs, "LLeg"))
            cmds.rowLayout("layLLegNumFingersHLegs", nc=1, en=False)
            cmds.intSliderGrp("intLLegNumFingersHLegs", l="Number of fingers: ", cw=([(1, 110), (2, 40), (3, 130)]), f=True, min=3, max=6, fmn=3, fmx=6, v=5)
            cmds.setParent('..')
            cmds.setParent('layMultHumanLegsHLegs')
            cmds.rowLayout("layMultRLegHLegs", w=310, nc=2)
            cmds.separator(w=5, h=3, st="none")
            cmds.frameLayout("frmRightLegHLegs", w=310, cl=True, cll=True, bgs=True, l="Right Leg")
            cmds.textFieldGrp("txtRLegParentHLegs", l="Leg Parent: ", cw2=(120, 120), tx="None", ed=False)
            cmds.checkBoxGrp("cbxRLegHaveFingersHLegs", l="Have fingers: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(HLegsUI.haveFingersHLegs, "RLeg"))
            cmds.rowLayout("layRLegNumFingersHLegs", nc=1, en=False)
            cmds.intSliderGrp("intRLegNumFingersHLegs", l="Number of fingers: ", cw=([(1, 110), (2, 40), (3, 130)]), f=True, min=3, max=6, fmn=3, fmx=6, v=5)
            cmds.setParent('..')
            cmds.setParent("layHumanLegs")
            cmds.frameLayout("frmFKSettingsHLegs", w=318, cl=True, cll=True, bgs=True, l="FK Settings")
            cmds.separator(w=5, h=1, st="none")
            cmds.rowLayout("layStretchFKHLegs", nc=2, en=True)
            cmds.checkBoxGrp("cbxStretchFKHLegs", l="Stretch FK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("laySquashFKHLegs", nc=2, en=True)
            cmds.checkBoxGrp("cbxSquashFKHLegs", l="Squash FK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layScaleFKHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxScaleFKHLegs", l="Scale Legs FK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Don't working yet, sry)")
            cmds.setParent('..')
            cmds.rowLayout("layVariableFKHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxVariableFKHLegs", l="Variable FK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Don't working yet, sry)")
            cmds.setParent('..')
            cmds.separator(w=5, h=1, st="none")
            cmds.setParent("layHumanLegs")
            cmds.frameLayout("frmIKSettingsHLegs", w=318, cl=True, cll=True, bgs=True, l="IK Settings")
            cmds.separator(w=5, h=1, st="none")
            cmds.optionMenuGrp("optEnIKHLegs", l="Enable IK: ", cw2=(120, 120), cc=partial(HLegsUI.enableIKHLeg))
            cmds.menuItem(l="Disabled")
            cmds.menuItem(l="Enabled")
            cmds.radioButtonGrp("radIKFKTypHLegs", l="Switch type: ", nrb=2, la2=["Choice", "Blend"], cw=([(1, 120), (2, 70)]), sl=1, en=False)
            cmds.rowLayout("layAutoManuPvHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxAutoManuPvHLegs", l="Auto/Manual Pv: ", ncb=1, cw=([(1, 120), (2, 70)]), cc=partial(HLegsUI.enableStretchIKMultHLeg))
            cmds.text(l="(NoFlip leg without pv)")
            cmds.setParent('..')
            cmds.rowLayout("layDualIKFKSeamHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxDualIKFKSeamHLegs", l="Dual IK/FK seamless: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Don't working yet, sry)")
            cmds.setParent('..')
            cmds.rowLayout("layStretchIKHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxStretchIKHLegs", l="Stretch IK: ", ncb=1, cw=([(1, 120), (2, 70)]), cc=partial(HLegsUI.enableStretchIKHLeg))
            cmds.text(l="(Enable IK leg to stretch)")
            cmds.setParent('..')
            cmds.rowLayout("layStretckIKMultHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxStretckIKMultHLegs", l="Stretch multipliers: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Multiply stretch to a value)")
            cmds.setParent('..')
            cmds.rowLayout("layClampStretchHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxClampStretchHLegs", l="Clamp stretch: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Clamp stretch to a value)")
            cmds.setParent('..')
            cmds.rowLayout("laySquashIKHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxHLegSquashIK", l="Squash IK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Enable IK leg to squash)")
            cmds.setParent('..')
            cmds.rowLayout("laySquashIKMultHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxSquashIKMultHLegs", l="Squash multipliers: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Multiply squash to a value)")
            cmds.setParent('..')
            cmds.rowLayout("layKneeLockHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxKneeLockHLegs", l="Knee lock: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Lock knee to pv controller)")
            cmds.setParent('..')
            cmds.rowLayout("laySoftIKHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxSoftIKHLegs", l="Soft IK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Don't working yet, sry)")
            cmds.setParent('..')
            cmds.rowLayout("layScaleIKHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxScaleIKHLegs", l="Scale legs IK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Don't working yet, sry)")
            cmds.setParent('..')
            cmds.rowLayout("layReverseFootHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxReverseFootHLegs", l="Reverse foot: ", ncb=1, cw=([(1, 120), (2, 70)]), cc=partial(HLegsUI.toggleReverseFootGuidesHLegs))
            cmds.text(l="(Advanced foot attributes)")
            cmds.setParent('..')
            cmds.separator(w=5, h=1, st="none")
            cmds.setParent("layHumanLegs")
            cmds.frameLayout("frmRibbonSettingsHLegs", w=318, cl=True, cll=True, bgs=True, l="Ribbon Settings")
            cmds.separator(w=5, h=1, st="none")
            cmds.optionMenuGrp("optEnRibbonHLegs", l="Enable Ribbon: ", cw2=(120, 120), cc=partial(HLegsUI.enableRibbonHLeg))
            cmds.menuItem(l="Disabled")
            cmds.menuItem(l="Enabled")
            cmds.rowLayout("layNumRibJntsHLegs", nc=2, en=False)
            cmds.intSliderGrp("intNumRibJntsHLegs", l="Number of joints: ", cw=([(1, 120), (2, 40), (3, 130)]), f=True, min=5, max=29, fmn=5, fmx=29, v=17)
            cmds.setParent('..')
            cmds.rowLayout("layBendCtrlsHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxBendCtrlsHLegs", l="Bend ctrls: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layTweakCtrlsHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxTweakCtrlsHLegs", l="Tweak ctrls: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layTwistAttrsHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxTwistAttrsHLegs", l="Twist attrs: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("laySineAttrsHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxSineAttrsHLegs", l="Sine attrs: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("laySquashAttrsHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxSquashAttrsHLegs", l="Squash attrs: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layExtraFreeSlotsHLegs", nc=2, en=False)
            cmds.checkBoxGrp("cbxExtraFreeSlotsHLegs", l="Extra free slots: ", ncb=1, cw=([(1, 120), (2, 70)]), cc=partial(HLegsUI.enableExtraFreeSlotsHLeg))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layNumExtraSlotsHLegs", nc=2, en=False)
            cmds.intSliderGrp("intNumExtraSlotsHLegs", l="Number extra slots: ", cw=([(1, 120), (2, 40), (3, 130)]), f=True, min=1, max=3, fmn=1, fmx=3, v=1)
            cmds.setParent('..')
            cmds.separator(w=5, h=1, st="none")
            cmds.setParent("layHumanLegs")
            cmds.frameLayout("frmSpaceSwitchSettingsHLegs", w=318, cl=True, cll=True, bgs=True, l="Space Switch Settings")
            cmds.separator(w=5, h=1, st="none")
            cmds.optionMenuGrp("optEnSpaceSwitchHLegs", l="Enable Space Switch: ", cw2=(120, 120), cc=partial(HLegsUI.enableSpaceSwitchHLeg))
            cmds.menuItem(l="Disabled")
            cmds.menuItem(l="Enabled")
            cmds.rowLayout("layMethodHLegs", nc=1, en=False)
            cmds.radioButtonGrp("radMethodHLegs", l="Method: ", nrb=2, la2=["Maya Consts", "Space Consts"], cw=([(1, 120), (2, 90)]), sl=1)
            cmds.setParent('..')
            cmds.rowLayout("layLegsSpaceHLegs", nc=3, en=False)
            cmds.optionMenuGrp("optLegsSpaceHLegs", l="Legs Spaces: ", cw2=(120, 120))
            cmds.menuItem(l="Human|Hip")
            cmds.menuItem(l="Human|Root")
            cmds.menuItem(l="Human|Chest")
            cmds.menuItem(l="Human|Neck")
            cmds.menuItem(l="Global")
            cmds.button(l="+", w=25, c=partial(HLegsUI.legsSpacesHLegs, "add"))
            cmds.button(l="-", w=25, c=partial(HLegsUI.legsSpacesHLegs, "rem"))
            cmds.setParent('..')
            cmds.rowLayout("layLegsSpaceListHLegs", nc=2, en=False)
            cmds.separator(w=30, h=1, st="none")
            cmds.textScrollList("lstLegsSpaceListHLegs", h=100, ams=True)
            cmds.setParent('..')
            cmds.rowLayout("layPvSpaceHLegs", nc=3, en=False)
            cmds.optionMenuGrp("optPvSpaceHLegs", l="Pole Vector Spaces: ", cw2=(120, 120))
            cmds.menuItem(l="Human|Leg")
            cmds.menuItem(l="Human|Arm")
            cmds.menuItem(l="Human|Hip")
            cmds.menuItem(l="Human|Root")
            cmds.menuItem(l="Human|Chest")
            cmds.menuItem(l="Human|Neck")
            cmds.menuItem(l="Global")
            cmds.button(l="+", w=25, c=partial(HLegsUI.pvSpacesHLegs, "add"))
            cmds.button(l="-", w=25, c=partial(HLegsUI.pvSpacesHLegs, "rem"))
            cmds.setParent('..')
            cmds.rowLayout("layPvSpaceListHLegs", nc=2, en=False)
            cmds.separator(w=30, h=1, st="none")
            cmds.textScrollList("lstPvSpaceListHLegs", h=100, ams=True)
            cmds.setParent('..')
            cmds.separator(w=5, h=1, st="none")
            cmds.setParent("layHumanLegs")
            cmds.frameLayout("frmExtraSettingsHLegs", w=318, cl=True, cll=True, bgs=True, l="Extra Settings")
            cmds.text(l="Lattice Controls: Y/N")
        elif comp == "layHumanArms":
            # Human Arms
            cmds.columnLayout("layHumanArms", w=308, vis=False, parent=self.PropLay)
            cmds.frameLayout("frmMainSettingsHArms", w=318, cl=False, cll=True, bgs=True, l="Arms Main Settings")
            cmds.separator(w=5, h=1, st="none")
            cmds.rowLayout("layForearmTwistHArms", nc=2, en=True)
            cmds.checkBoxGrp("cbxForearmTwistHArms", l="Forearm Twist: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout(w=315, nc=1, cl1="left")
            cmds.radioButtonGrp("radMultArmsHArms", l="Multiple Arms: ", nrb=2, la2=["No", "Yes"], cw=([(1, 120), (2, 50)]), sl=1, onc=partial(HArmsUI.multipleArmsHArms))
            cmds.setParent('..')
            cmds.rowLayout("layMultArmsHArms", nc=4, en=False)
            cmds.separator(w=40, h=3, st="single", bgc=[Grey[0], Grey[1], Grey[2]])
            cmds.button("btnAddArmHArms", w=120, l="Add Arm", c=partial(HArmsUI.addHArms))
            cmds.separator(w=5, h=3, st="none")
            cmds.button("btnRemArmHArms", w=120, l="Remove Arm", en=False, c=partial(HArmsUI.remHArms))
            cmds.setParent('..')
            cmds.rowColumnLayout("layMultHumanArmsHArms", w=300, nc=1)
            cmds.rowLayout("layMultLArmHArms", w=310, nc=2)
            cmds.separator(w=5, h=3, st="none")
            cmds.frameLayout("frmLeftArmHArms", w=312, cl=True, cll=True, bgs=True, l="Left Arm")
            cmds.textFieldGrp("txtLArmParentHArms", l="Arm Parent: ", cw2=(110, 120), tx="None", ed=False)
            cmds.checkBoxGrp("cbxLArmHaveClavicleHArms", l="Have clavicle: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(HArmsUI.haveClavicleHArms, "LArm"))
            cmds.checkBoxGrp("cbxLArmHaveFingersHArms", l="Have fingers: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(HArmsUI.haveFingersHArms, "LArm"))
            cmds.rowLayout("layLArmNumFingersHArms", nc=1, en=False)
            cmds.intSliderGrp("intLArmNumFingersHArms", l="Number of fingers: ", cw=([(1, 110), (2, 40), (3, 130)]), f=True, min=3, max=6, fmn=3, fmx=6, v=5)
            cmds.setParent('..')
            cmds.setParent('layMultHumanArmsHArms')
            cmds.rowLayout("layMultRArmHArms", w=310, nc=2)
            cmds.separator(w=5, h=3, st="none")
            cmds.frameLayout("frmRightArmHArms", w=310, cl=True, cll=True, bgs=True, l="Right Arm")
            cmds.textFieldGrp("txtRArmParentHArms", l="Arm Parent: ", cw2=(120, 120), tx="None", ed=False)
            cmds.checkBoxGrp("cbxRArmHaveClavicleHArms", l="Have clavicle: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(HArmsUI.haveClavicleHArms, "RArm"))
            cmds.checkBoxGrp("cbxRArmHaveFingersHArms", l="Have fingers: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(HArmsUI.haveFingersHArms, "RArm"))
            cmds.rowLayout("layRArmNumFingersHArms", nc=1, en=False)
            cmds.intSliderGrp("intRArmNumFingersHArms", l="Number of fingers: ", cw=([(1, 110), (2, 40), (3, 130)]), f=True, min=3, max=6, fmn=3, fmx=6, v=5)
            cmds.setParent('..')
            cmds.setParent("layHumanArms")
            cmds.frameLayout("frmFKSettingsHArms", w=318, cl=True, cll=True, bgs=True, l="FK Settings")
            cmds.separator(w=5, h=1, st="none")
            # cmds.rowLayout("layClavicleFKHArms", nc=2, en=False)
            # cmds.checkBoxGrp("cbxClavicleFKHArms", l="FK Clavicle: ", ncb=1, cw=([(1, 120), (2, 70)]))
            # cmds.text(l="(Info about...)")
            # cmds.setParent('..')
            cmds.rowLayout("layStretchFKHArms", nc=2, en=True)
            cmds.checkBoxGrp("cbxStretchFKHArms", l="Stretch FK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("laySquashFKHArms", nc=2, en=True)
            cmds.checkBoxGrp("cbxSquashFKHArms", l="Squash FK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layVariableFKHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxVariableFKHArms", l="Variable FK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Don't working yet, sry)")
            cmds.setParent('..')
            cmds.rowLayout("layScaleFKHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxScaleFKHArms", l="Scale Arms FK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Don't working yet, sry)")
            cmds.setParent('..')
            cmds.separator(w=5, h=1, st="none")
            cmds.setParent("layHumanArms")
            cmds.frameLayout("frmIKSettingsHArms", w=318, cl=True, cll=True, bgs=True, l="IK Settings")
            cmds.separator(w=5, h=1, st="none")
            cmds.optionMenuGrp("optEnIKHArms", l="Enable IK: ", cw2=(120, 120), cc=partial(HArmsUI.enableIKHArm))
            cmds.menuItem(l="Disabled")
            cmds.menuItem(l="Enabled")
            cmds.radioButtonGrp("radIKFKTypHArms", l="Switch type: ", nrb=2, la2=["Choice", "Blend"], cw=([(1, 120), (2, 70)]), sl=1, en=False)
            cmds.rowLayout("layAutoManuPvHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxAutoManuPvHArms", l="Auto/Manual Pv: ", ncb=1, cw=([(1, 120), (2, 70)]), cc=partial(HArmsUI.enableStretchIKMultHArm))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layDualIKFKSeamHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxDualIKFKSeamHArms", l="Dual IK/FK seamless: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Don't working yet, sry)")
            cmds.setParent('..')
            cmds.rowLayout("layStretchIKHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxStretchIKHArms", l="Stretch IK: ", ncb=1, cw=([(1, 120), (2, 70)]), cc=partial(HArmsUI.enableStretchIKHArm))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layStretckIKMultHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxStretckIKMultHArms", l="Stretch multipliers: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layClampStretchHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxClampStretchHArms", l="Clamp stretch: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("laySquashIKHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxHArmSquashIK", l="Squash IK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("laySquashIKMultHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxSquashIKMultHArms", l="Squash multipliers: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layElbowLockHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxElbowLockHArms", l="Elbow lock: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("laySoftIKHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxSoftIKHArms", l="Soft IK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Don't working yet, sry)")
            cmds.setParent('..')
            cmds.rowLayout("layScaleIKHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxScaleIKHArms", l="Scale arms IK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Don't working yet, sry)")
            cmds.setParent('..')
            cmds.rowLayout("layReverseHandHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxReverseHandHArms", l="Reverse hand: ", ncb=1, cw=([(1, 120), (2, 70)]), cc=partial(HArmsUI.toggleReverseHandGuidesHArms))
            cmds.text(l="(Don't working yet, sry)")
            cmds.setParent('..')
            cmds.rowLayout("layClavicleIKHArms", nc=2, en=False)
            cmds.radioButtonGrp("radClavicleTypeHArms", l="Clavicle Type: ", nrb=3, la3=["IK/FK", "FK only", "IK only"], cw=([(1, 120), (2, 48), (3, 60)]), sl=2, en=False)
            cmds.setParent('..')
            cmds.separator(w=5, h=1, st="none")
            cmds.setParent("layHumanArms")
            cmds.frameLayout("frmRibbonSettingsHArms", w=318, cl=True, cll=True, bgs=True, l="Ribbon Settings")
            cmds.separator(w=5, h=1, st="none")
            cmds.optionMenuGrp("optEnRibbonHArms", l="Enable Ribbon: ", cw2=(120, 120), cc=partial(HArmsUI.enableRibbonHArm))
            cmds.menuItem(l="Disabled")
            cmds.menuItem(l="Enabled")
            cmds.rowLayout("layNumRibJntsHArms", nc=2, en=False)
            cmds.intSliderGrp("intNumRibJntsHArms", l="Number of joints: ", cw=([(1, 120), (2, 40), (3, 130)]), f=True, min=5, max=29, fmn=5, fmx=29, v=17)
            cmds.setParent('..')
            cmds.rowLayout("layBendCtrlsHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxBendCtrlsHArms", l="Bend ctrls: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layTweakCtrlsHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxTweakCtrlsHArms", l="Tweak ctrls: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layTwistAttrsHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxTwistAttrsHArms", l="Twist attrs: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("laySineAttrsHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxSineAttrsHArms", l="Sine attrs: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("laySquashAttrsHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxSquashAttrsHArms", l="Squash attrs: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Don't working yet, sry)")
            cmds.setParent('..')
            cmds.rowLayout("layExtraFreeSlotsHArms", nc=2, en=False)
            cmds.checkBoxGrp("cbxExtraFreeSlotsHArms", l="Extra free slots: ", ncb=1, cw=([(1, 120), (2, 70)]), cc=partial(HArmsUI.enableExtraFreeSlotsHArm))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layNumExtraSlotsHArms", nc=2, en=False)
            cmds.intSliderGrp("intNumExtraSlotsHArms", l="Number extra slots: ", cw=([(1, 120), (2, 40), (3, 130)]), f=True, min=1, max=3, fmn=1, fmx=3, v=1)
            cmds.setParent('..')
            cmds.separator(w=5, h=1, st="none")
            cmds.setParent("layHumanArms")
            cmds.frameLayout("frmSpaceSwitchSettingsHArms", w=318, cl=True, cll=True, bgs=True, l="Space Switch Settings")
            cmds.separator(w=5, h=1, st="none")
            cmds.optionMenuGrp("optEnSpaceSwitchHArms", l="Enable Space Switch: ", cw2=(120, 120), cc=partial(HArmsUI.enableSpaceSwitchHArm))
            cmds.menuItem(l="Disabled")
            cmds.menuItem(l="Enabled")
            cmds.rowLayout("layMethodHArms", nc=1, en=False)
            cmds.radioButtonGrp("radMethodHArms", l="Method: ", nrb=2, la2=["Maya Consts", "Space Consts"], cw=([(1, 120), (2, 90)]), sl=1)
            cmds.setParent('..')
            cmds.rowLayout("layArmsSpaceHArms", nc=3, en=False)
            cmds.optionMenuGrp("optArmsSpaceHArms", l="Arms Spaces: ", cw2=(120, 120))
            cmds.menuItem(l="Human|Hip")
            cmds.menuItem(l="Human|Root")
            cmds.menuItem(l="Human|Chest")
            cmds.menuItem(l="Human|Neck")
            cmds.menuItem(l="Global")
            cmds.button(l="+", w=25, c=partial(HArmsUI.armsSpacesHArms, "add"))
            cmds.button(l="-", w=25, c=partial(HArmsUI.armsSpacesHArms, "rem"))
            cmds.setParent('..')
            cmds.rowLayout("layArmsSpaceListHArms", nc=2, en=False)
            cmds.separator(w=30, h=1, st="none")
            cmds.textScrollList("lstArmsSpaceListHArms", h=100, ams=True)
            cmds.setParent('..')
            cmds.rowLayout("layPvSpaceHArms", nc=3, en=False)
            cmds.optionMenuGrp("optPvSpaceHArms", l="Pole Vector Spaces: ", cw2=(120, 120))
            cmds.menuItem(l="Human|Arm")
            cmds.menuItem(l="Human|Hip")
            cmds.menuItem(l="Human|Root")
            cmds.menuItem(l="Human|Chest")
            cmds.menuItem(l="Human|Neck")
            cmds.menuItem(l="Global")
            cmds.button(l="+", w=25, c=partial(HArmsUI.pvSpacesHArms, "add"))
            cmds.button(l="-", w=25, c=partial(HArmsUI.pvSpacesHArms, "rem"))
            cmds.setParent('..')
            cmds.rowLayout("layPvSpaceListHArms", nc=2, en=False)
            cmds.separator(w=30, h=1, st="none")
            cmds.textScrollList("lstPvSpaceListHArms", h=100, ams=True)
            cmds.setParent('..')
            cmds.separator(w=5, h=1, st="none")
            cmds.setParent("layHumanArms")
            cmds.frameLayout("frmExtraSettingsHArms", w=318, cl=True, cll=True, bgs=True, l="Extra Settings")
            cmds.setParent("layHumanArms")
        elif comp == "layHumanHead":
            # Human Legs
            cmds.columnLayout("layHumanHead", w=308, vis=False, parent=self.PropLay)
            cmds.frameLayout("frmMainSettingsHHeads", w=318, cl=False, cll=True, bgs=True, l="Head Main Settings")
            cmds.separator(w=5, h=1, st="none")
            cmds.rowLayout("layNumJntsHHeads", nc=2, en=False)
            cmds.intSliderGrp("intNumJntsHHeads", l="Num of Neck Jnts: ", cw=([(1, 120), (2, 40), (3, 130)]), f=True, min=2, max=4, fmn=2, fmx=4, v=2)
            cmds.setParent('..')
            cmds.rowLayout("layScaleHeadsHHeads", nc=2, en=False)
            cmds.checkBoxGrp("cbxScaleHeadsHHeads", l="Scale Heads: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Scale heads uniformly)")
            cmds.setParent('..')
            cmds.rowLayout("layHybridTypeHHeads", nc=1, en=False)
            cmds.radioButtonGrp("radHybridTypeHHeads", l="Hybrid Type: ", nrb=2, la2=["IK Spline", "Ribbon"], cw=([(1, 120), (2, 80)]), sl=1, onc=partial(HHeadsUI.setHybridTypeHHeads))
            cmds.setParent('..')
            cmds.rowLayout(w=315, nc=1, cl1="left")
            cmds.radioButtonGrp("radMultHeadsHHeads", l="Multiple Heads: ", nrb=2, la2=["No", "Yes"], cw=([(1, 120), (2, 50)]), sl=1)
            cmds.setParent('..')
            cmds.rowLayout("layMultHeadsHHeads", nc=4, en=False)
            cmds.separator(w=40, h=3, st="single", bgc=[Grey[0], Grey[1], Grey[2]])   # <<<----------------------------------------------------------------------------------------------- OLHAR AQUI
            cmds.button("btnAddHeadHHeads", w=120, l="Add Head")
            cmds.separator(w=5, h=3, st="none")
            cmds.button("btnRemHeadHHeads", w=120, l="Remove Head")
            cmds.setParent('..')
            cmds.rowColumnLayout("layMultHumanHeadsHHeads", w=300, nc=1)
            cmds.rowLayout("layMultHead1HHeads", w=310, nc=2)
            cmds.separator(w=5, h=3, st="none")
            cmds.frameLayout("frmHead1HHeads", w=312, cl=True, cll=True, bgs=True, l="Head 1")
            cmds.rowLayout("layHead1CreateEyesHHeads", nc=2, en=True)
            cmds.checkBoxGrp("cbxHead1CreateEyesHHeads", l="Create Eyes: ", ncb=1, cw=([(1, 110), (2, 70)]), cc=partial(HHeadsUI.enableEyesHHeads))
            cmds.text(l="(Create eyes setup)")
            cmds.setParent('..')
            cmds.rowLayout("layHead1NumEyesHHeads", nc=1, en=False)
            cmds.intSliderGrp("intHead1NumEyesHHeads", l="Number of Eyes: ", cw=([(1, 110), (2, 40), (3, 130)]), f=True, min=1, max=8, fmn=1, fmx=8, v=2)
            cmds.setParent('..')
            cmds.rowLayout("layHead1CreateTongueHHeads", nc=2, en=False)
            cmds.checkBoxGrp("cbxHead1CreateTongueHHeads", l="Create Tongue: ", ncb=1, cw=([(1, 110), (2, 70)]))
            cmds.text(l="(Create tongue setup)")
            cmds.setParent('..')
            cmds.rowLayout("layHead1CreateJawHHeads", nc=2, en=True)
            cmds.checkBoxGrp("cbxHead1CreateJawHHeads", l="Create Jaw: ", ncb=1, cw=([(1, 110), (2, 70)]))
            cmds.text(l="(Create jaw setup)")
            cmds.setParent('..')
            cmds.rowLayout("layHead1CreateTeethsHHeads", nc=2, en=True)
            cmds.checkBoxGrp("cbxHead1CreateTeethsHHeads", l="Create Teeths: ", ncb=1, cw=([(1, 110), (2, 70)]))
            cmds.text(l="(Create basic teeths setup)")
            cmds.setParent('..')
            cmds.rowLayout("layHead1SepNeckHHeads", nc=2, en=False)
            cmds.checkBoxGrp("cbxHead1SepNeckHHeads", l="Separated Neck: ", ncb=1, cw=([(1, 110), (2, 70)]))
            cmds.text(l="(Create IK ctrl to neck)")
            cmds.setParent('..')
            cmds.setParent("layHumanHead")
            cmds.separator(w=5, h=1, st="none")
            cmds.setParent("layHumanHead")
            cmds.frameLayout("frmIKSplineSettingsHHeads", w=318, cl=True, cll=True, bgs=True, l="IK Spline Settings", en=True)
            cmds.separator(w=5, h=1, st="none")
            cmds.optionMenuGrp("optEnIKSplineHHeads", l="Enable IK Spline: ", cw2=(120, 120), cc=partial(HHeadsUI.enableIKSplineHHeads))
            cmds.menuItem(l="Disabled")
            cmds.menuItem(l="Enabled")
            cmds.rowLayout("layNumIKSplineJntsHHeads", nc=2, en=False)
            cmds.intSliderGrp("intNumIKSplineJntsHHeads", l="Number of joints: ", cw=([(1, 120), (2, 40), (3, 130)]), f=True, min=3, max=15, fmn=3, fmx=15, v=5)
            cmds.setParent('..')
            cmds.rowLayout("layStretchIKHHeads", nc=2, en=False)
            cmds.checkBoxGrp("cbxStretchIKHHeads", l="Stretch IK: ", ncb=1, cw=([(1, 120), (2, 70)]), cc=partial(HHeadsUI.enableStretchIKHHeads))
            cmds.text(l="(Enable IK spine to stretch)")
            cmds.setParent('..')
            cmds.rowLayout("layStretckIKMultHHeads", nc=2, en=False)
            cmds.checkBoxGrp("cbxStretckIKMultHHeads", l="Stretch multipliers: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Multiply stretch to a value)")
            cmds.setParent('..')
            cmds.rowLayout("layClampStretchHHeads", nc=2, en=False)
            cmds.checkBoxGrp("cbxClampStretchHHeads", l="Clamp stretch: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Clamp stretch to a value)")
            cmds.setParent('..')
            cmds.rowLayout("laySquashIKHHeads", nc=2, en=False)
            cmds.checkBoxGrp("cbxSquashIKHHeads", l="Squash IK: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Enable IK spine to squash)")
            cmds.setParent('..')
            cmds.rowLayout("laySquashIKMultHHeads", nc=2, en=False)
            cmds.checkBoxGrp("cbxSquashIKMultHHeads", l="Squash multipliers: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Multiply squash to a value)")
            cmds.setParent('..')
            cmds.rowLayout("layTweakIKHHeads", nc=2, en=False)
            cmds.checkBoxGrp("cbxBendIKHHeads", l="Bend controller: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Ctrl to bend middle of spine)")
            cmds.setParent('..')
            cmds.separator(w=5, h=1, st="none")
            cmds.setParent("layHumanHead")
            cmds.frameLayout("frmRibbonSettingsHHeads", w=318, cl=True, cll=True, bgs=True, l="Ribbon Settings", en=False)
            cmds.separator(w=5, h=1, st="none")
            cmds.optionMenuGrp("optEnRibbonHHeads", l="Enable Ribbon: ", cw2=(120, 120), cc=partial(HHeadsUI.enableRibbonHHeads))
            cmds.menuItem(l="Disabled")
            cmds.menuItem(l="Enabled")
            cmds.rowLayout("layNumRibJntsHHeads", nc=2, en=False)
            cmds.intSliderGrp("intNumRibJntsHHeads", l="Number of joints: ", cw=([(1, 120), (2, 40), (3, 130)]), f=True, min=3, max=15, fmn=3, fmx=15, v=7)
            cmds.setParent('..')
            cmds.rowLayout("layBendCtrlsHHeads", nc=2, en=False)
            cmds.checkBoxGrp("cbxBendCtrlsHHeads", l="Bend ctrls: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layTweakCtrlsHHeads", nc=2, en=False)
            cmds.checkBoxGrp("cbxTweakCtrlsHHeads", l="Tweak ctrls: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layTwistAttrsHHeads", nc=2, en=False)
            cmds.checkBoxGrp("cbxTwistAttrsHHeads", l="Twist attrs: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("laySineAttrsHHeads", nc=2, en=False)
            cmds.checkBoxGrp("cbxSineAttrsHHeads", l="Sine attrs: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layStretchAttrsHHeads", nc=2, en=False)
            cmds.checkBoxGrp("cbxStretchAttrsHHeads", l="Stretch attrs: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Don't working yet, sry)")
            cmds.setParent('..')
            cmds.rowLayout("layExtraFreeSlotsHHeads", nc=2, en=False)
            cmds.checkBoxGrp("cbxExtraFreeSlotsHHeads", l="Extra free slots: ", ncb=1, cw=([(1, 120), (2, 70)]))
            cmds.text(l="(Info about...)")
            cmds.setParent('..')
            cmds.rowLayout("layNumExtraSlotsHHeads", nc=2, en=False)
            cmds.intSliderGrp("intNumExtraSlotsHHeads", l="Number extra slots: ", cw=([(1, 120), (2, 40), (3, 130)]), f=True, min=1, max=3, fmn=1, fmx=3, v=1)
            cmds.setParent('..')
            cmds.separator(w=5, h=1, st="none")
            cmds.setParent("layHumanHead")
            cmds.frameLayout("frmSpaceSwitchSettingsHHeads", w=318, cl=True, cll=True, bgs=True, l="Space Switch Settings")
            cmds.separator(w=5, h=1, st="none")
            cmds.optionMenuGrp("optEnSpaceSwitchHHeads", l="Enable Space Switch: ", cw2=(120, 120), cc=partial(HHeadsUI.enableSpaceSwitchHHeads))
            cmds.menuItem(l="Disabled")
            cmds.menuItem(l="Enabled")
            cmds.rowLayout("layMethodHHeads", nc=1, en=False)
            cmds.radioButtonGrp("radMethodHHeads", l="Method: ", nrb=2, la2=["Maya Consts", "Space Consts"], cw=([(1, 120), (2, 90)]), sl=1)
            cmds.setParent('..')
            cmds.rowLayout("layHeadsSpaceHHeads", nc=3, en=False)
            cmds.optionMenuGrp("optHeadsSpaceHHeads", l="Heads Spaces: ", cw2=(120, 120))
            cmds.menuItem(l="Human|Neck")
            cmds.menuItem(l="Human|Chest")
            cmds.menuItem(l="Human|Hip")
            cmds.menuItem(l="Human|Root")
            cmds.menuItem(l="Global")
            cmds.button(l="+", w=25, c=partial(HHeadsUI.legsSpacesHHeads, "add"))
            cmds.button(l="-", w=25, c=partial(HHeadsUI.legsSpacesHHeads, "rem"))
            cmds.setParent('..')
            cmds.rowLayout("layHeadsSpaceListHHeads", nc=2, en=False)
            cmds.separator(w=30, h=1, st="none")
            cmds.textScrollList("lstHeadsSpaceListHHeads", h=100, ams=True)
            cmds.setParent('..')
            cmds.separator(w=5, h=1, st="none")
            cmds.setParent("layHumanHead")

    # --------------------------------------------------------------------------------------------------------
    # LOAD COMPONENTS PROPERTIES TO UI                           <<< ADICIONAR FERRAMENTAS AQUI >>>
    # --------------------------------------------------------------------------------------------------------
    def loadComponentProperties(self, comp, *args):
        if comp == "Char Geometry":
            # layOutfitNames
            cmds.tabLayout(self.tabProperties, edit=True, tabLabel=[(self.PropLay, 'Properties > General > Edit Char Geometry')])
            self.deleteComponentProperties()
            cmds.columnLayout("layEditCharGeo", edit=True, vis=True)
            log.buildLog(btn="Edit Char Geo", msg="loadPropertiesUI", stop=True)
        elif comp == "<<<Master Features>>>":
            cmds.tabLayout(self.tabProperties, edit=True, tabLabel=[(self.PropLay, 'Properties > Rigging > <<< Master Features >>>')])
            self.deleteComponentProperties()
            cmds.columnLayout("layMasterFeat", edit=True, vis=True)
            log.buildLog(btn="<<< Master Features >>>", msg="loadPropertiesUI", stop=True)
        elif comp == "Human Spine":
            cmds.tabLayout(self.tabProperties, edit=True, tabLabel=[(self.PropLay, 'Properties > Rigging > Human Spine')])
            self.deleteComponentProperties()
            if(cmds.columnLayout("layHumanSpine", exists=True)):
                cmds.columnLayout("layHumanSpine", edit=True, vis=True)
                log.buildLog(btn="Human Spine", msg="loadPropertiesUI", stop=True)
            else:
                log.buildLog(btn="Human Spine", msg="loadPropertiesUI", stop=True)
        elif comp == "Human Legs":
            cmds.tabLayout(self.tabProperties, edit=True, tabLabel=[(self.PropLay, 'Properties > Rigging > Human Legs')])
            self.deleteComponentProperties()
            if(cmds.columnLayout("layHumanLegs", exists=True)):
                cmds.columnLayout("layHumanLegs", edit=True, vis=True)
                log.buildLog(btn="Human Legs", msg="loadPropertiesUI", stop=True)
            else:
                log.buildLog(btn="Human Legs", msg="loadPropertiesUI", stop=True)
        elif comp == "Human Arms":
            cmds.tabLayout(self.tabProperties, edit=True, tabLabel=[(self.PropLay, 'Properties > Rigging > Human Arms')])
            self.deleteComponentProperties()
            if(cmds.columnLayout("layHumanArms", exists=True)):
                cmds.columnLayout("layHumanArms", edit=True, vis=True)
                log.buildLog(btn="Human Arms", msg="loadPropertiesUI", stop=True)
            else:
                log.buildLog(btn="Human Arms", msg="loadPropertiesUI", stop=True)
        elif comp == "Human Head":
            cmds.tabLayout(self.tabProperties, edit=True, tabLabel=[(self.PropLay, 'Properties > Rigging > Human Head')])
            self.deleteComponentProperties()
            if(cmds.columnLayout("layHumanHead", exists=True)):
                cmds.columnLayout("layHumanHead", edit=True, vis=True)
                log.buildLog(btn="Human Head", msg="loadPropertiesUI", stop=True)
            else:
                log.buildLog(btn="Human Head", msg="loadPropertiesUI", stop=True)
