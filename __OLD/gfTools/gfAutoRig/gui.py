import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
from functools import partial
import os


from gfTools.__OLD.gfTools.gfAutoRig.settings import log
from gfTools.__OLD.gfTools.gfAutoRig.settings import guides
from gfTools.__OLD.gfTools.gfAutoRig.settings.uiConfig import masterUIConfig
from gfTools.__OLD.gfTools.gfAutoRig.settings import buildRig as rig
reload(log)
reload(guides)
reload(masterUIConfig)
reload(rig)


class gfAutoRigUI(object):

    def __init__(self):
        self.nUI = "gfAutoRigUI"
        self.tUI = "gfAutoRig"
        self.OutFeatLay = "scrOutputs"
        self.PropLay = "scrProperties"
        self.promptLog = "promptLog"
        self.tabProperties = "tabProperties"
        self.logLines = []
        self.wUI = 723
        self.hUI = 650
        self.scriptPath = os.path.dirname(os.path.abspath( __file__ ))

        self.verifyUI()
        self.display()
        log.buildLog(msg="initialized")

    def verifyUI(self):
        if(cmds.window(self.nUI, exists=True)):
            cmds.deleteUI(self.nUI)

    def display(self):

        # Variables
        mainForm = ''
        tabName = ''
        tabChar = ''
        tabProperties = ''
        tabFeat = ''
        tabOutput = ''
        layName = ''
        layCreate = ''
        layProperties = ''
        layComp = ''
        layPresets = ''
        layOutput = ''
        laySkin = ''
        layDynamics = ''
        Yellow = [0.96863, 0.79216, 0.09412]
        DarkGrey = [0.18, 0.18, 0.18]
        LightGrey = [0.35, 0.35, 0.35]
        SoftYellow = [0.96078, 0.84314, 0.43137]

        # Window
        cmds.window(self.nUI, w=self.wUI, h=self.hUI, t=self.tUI, mb=True, mxb=False, s=False)
        cmds.menu(l="Help", helpMenu=True)
        cmds.menuItem(l="How to Use")
        cmds.menuItem(d=True)
        cmds.menuItem(l="About Application")
        cmds.menu(l="File")
        cmds.menuItem(l="Save Character")
        cmds.menuItem(l="Save Character", ob=True)
        cmds.menuItem(l="Load Character")
        cmds.menu(l="Rigging")
        cmds.menuItem(l="Save custom rig preset")
        cmds.menuItem(l="Save custom rig preset", ob=True)
        cmds.menuItem(l="Load custom rig preset")
        cmds.menuItem(l="Guides", d=True)
        cmds.menuItem(l="Parent guides")
        cmds.menuItem(l="Unparent guides")
        cmds.menuItem(l="Reload guides")
        cmds.menuItem(l="Mirror guides", cb=True)
        cmds.menuItem(l="Name guides", cb=True)
        cmds.menuItem(l="Convert rig to guides")
        cmds.menuItem(l="Convert rig to guides", ob=True)
        cmds.menuItem(l="Ctrls", d=True)
        cmds.menuItem(l="Load gfCtrlEditor")
        cmds.menu(l="Proxy")
        cmds.menuItem(l="Teste")
        cmds.menu(l="Skinning")
        cmds.menuItem(l="Teste")
        cmds.menuItem(l="PSD", d=True)
        cmds.menuItem(l="Load gfPSDTool")
        cmds.menu(l="Dynamics")
        cmds.menuItem(l="Teste")
        cmds.menu(l="Log")
        cmds.menuItem(l="Clear log", c=partial(log.buildLog, None, False, "promptLog", False, False, "clearLog"))
        cmds.menuItem(l="Show after operation", cb=True)
        cmds.menuItem(d=True)
        cmds.menuItem(l="Export character features")
        cmds.menuItem(l="Export character features options", ob=True)
        cmds.menuItem(l="Export character log")
        cmds.menuItem(l="Export character log options", ob=True)

        mainForm = cmds.formLayout(w=self.wUI, h=self.hUI, nd=100)

        #---------------------------------------------------------------------------------------
        # NAME FIELD
        #---------------------------------------------------------------------------------------
        tabName = cmds.tabLayout(w=self.wUI, h=100, tv=False)
        layName = cmds.rowLayout(w=self.wUI, h=100, nc=7) #723
        # Meus names vem aqui
        cmds.columnLayout("layCharName", w=150, h=100)
        cmds.separator(w=150, h=3, st="none")
        cmds.textFieldGrp("txtCharName", w=150, h=40, l="Char Name: ", rat=[(1, "top", 0), (2, "bottom", 0)], cat=[(1, "left", 0), (2, "both", -143)],
            cc=masterUIConfig.config().setCharName)
        cmds.separator(w=150, h=7, st="none")
        cmds.setParent(layName)
        cmds.separator(w=15, h=15, st="none")
        cmds.columnLayout("layTeste", w=195, h=100)
        cmds.separator(w=195, h=5, st="none")
        cmds.text(l="Char Type: ")
        cmds.separator(w=195, h=5, st="none")
        cmds.optionMenu("optCharType", w=195, cc=masterUIConfig.config().setCharType)
        cmds.menuItem(l="Select Type")
        cmds.menuItem(l="Creature")
        cmds.menuItem(l="Biped Human")
        cmds.menuItem(l="Quadruped")
        cmds.menuItem(l="Fish")
        cmds.menuItem(l="Bird")
        cmds.menuItem(l="Octopus")
        cmds.menuItem(l="Turtle")
        cmds.menuItem(l="Car")
        cmds.menuItem(l="Tank")
        cmds.setParent(layName)
        cmds.separator(w=15, h=3, st="none")
        cmds.columnLayout("layGeometry", w=200, h=100)
        cmds.separator(w=200, h=3, st="none")
        cmds.text("txtAllGeo", l="Char Geometries: ", ann="Select in order: Base Body, Left Eye, Right Eye, Upper Teeth, Lower Teeth, Tongue, Extra Meshes")
        cmds.separator(w=150, h=5, st="none")
        cmds.textScrollList("lstAllGeo", w=200, h=65, ams=True, dcc=masterUIConfig.config().selectGeometry)
        cmds.setParent(layName)
        cmds.separator(w=4, h=15, st="none")

        cmds.gridLayout("layEditGeo", w=122, h=112, nc=2, cwh=(61,46))
        cmds.rowLayout("layAddGeo", w=61, h=46, nc=1, en=True)
        cmds.button(w=55, h=40, l="Add", c=partial(masterUIConfig.config().loadComponentProperties, "Char Geometry"))
        cmds.setParent('..')
        cmds.rowLayout("layRemGeo", w=61, h=46, nc=1, en=True)
        cmds.button(w=55, h=40, l="Rem", c=masterUIConfig.config().removeGeometry)
        cmds.setParent('..')
        cmds.rowLayout("layClsGeo", w=61, h=46, nc=1, en=True)
        cmds.button(w=55, h=40, l="Cls", c=masterUIConfig.config().clearGeometry)
        cmds.setParent('..')
        cmds.rowLayout("layWireGeo", w=61, h=46, nc=1, en=True)
        cmds.button(w=55, h=40, l="Wire", c=masterUIConfig.config().wireGeometry)
        cmds.setParent('..')


        # cmds.columnLayout("layCharButtons", w=200, h=100)
        # cmds.separator(w=200, h=3, st="none")
        # cmds.button(w=120, l="Add Geometry", c=masterUIConfig.config().addGeometry)
        # cmds.separator(w=150, h=7, st="none")
        # cmds.button(w=120, l="Remove Geometry", c=masterUIConfig.config().removeGeometry)
        # cmds.separator(w=150, h=7, st="none")
        # cmds.button(w=120, l="Clear Geometry", c=masterUIConfig.config().clearGeometry)
        # cmds.separator(w=150, h=7, st="none")
        cmds.setParent(layName)

        cmds.setParent(layName)

        # Character name
        # Character all geometry
        # Character L/R Eyes


        cmds.tabLayout(tabName, edit=True, tabLabel=[(layName, 'Name')])
        # cmds.formLayout(layName, edit=True, af=[("txtCharName", "top", 20), ("txtCharName", "left", 5)])
        cmds.setParent(mainForm)

        #---------------------------------------------------------------------------------------
        # CHAR FIELD
        #---------------------------------------------------------------------------------------
        cmds.tabLayout("tabChar", w=390, h=550) # Tab lado esquerdo

        cmds.rowColumnLayout("layRig", w=393, h=292, nc=1)
        gridLayRig = cmds.rowColumnLayout(w=393, h=492, nc=2)
        tabFeat = cmds.tabLayout(w=160, h=465)
        layComp = cmds.columnLayout()
        # Meus Components vem aqui
        cmds.scrollLayout("scrComponents", w=155, h=465, vsb=True)# Height = tab - 27
        masterUIConfig.config().loadComponentsUI()
        cmds.setParent(tabFeat)

        layPresets = cmds.columnLayout()
        # Meus Presets vem aqui
        cmds.scrollLayout("scrPresets", w=155, h=465, vsb=True)
        masterUIConfig.config().loadPresetsUI()
        cmds.setParent(gridLayRig)

        tabOutput = cmds.tabLayout(w=220, h=490, tv=False)
        layOutput = cmds.columnLayout()
        cmds.rowLayout("layDsgnOutputs", nc=1)
        cmds.separator(w=210, h=3, st="in", bgc=[Yellow[0], Yellow[1], Yellow[2]])
        cmds.setParent('..')
        cmds.frameLayout("FrameOutput", cll=0, l="Your Char Rigging Output Features")
        # Master features
        cmds.gridLayout("compChar", w=197, h=40, nc=1, cwh=(213,40))
        cmds.rowLayout(w=200, h=40, nc=4, bgc=[DarkGrey[0], DarkGrey[1], DarkGrey[2]])
        cmds.separator(w=10, h=3, st="none")
        cmds.text(l="<<< Master Features >>>")
        cmds.separator(w=17, h=3, st="none")
        cmds.button(l="Edit", bgc=[LightGrey[0], LightGrey[1], LightGrey[2]], c=partial(masterUIConfig.config().loadComponentProperties, "<<<Master Features>>>"))
        cmds.setParent("FrameOutput")
        cmds.scrollLayout(self.OutFeatLay, w=214, h=411, cr=True, mcw=157, vsb=True) # Height = tab - 27
        # Meus Outputs vem aqui <<< BUTTON CLICK >>>

        cmds.setParent("tabChar")
        # Proxy Tab
        layProxy = cmds.columnLayout()
        cmds.text(r"NOT WORKING YET, SRY! :(")
        cmds.separator(w=5, h=10, st="none")
        cmds.text("TODO: Substitute component")
        cmds.setParent("tabChar")
        # Skin Tab
        laySkin = cmds.columnLayout()
        cmds.text(r"NOT WORKING YET, SRY! :(")
        cmds.setParent("tabChar")
        # Dynamics Tab
        layDynamics = cmds.columnLayout()
        cmds.text(r"NOT WORKING YET, SRY! :(")
        cmds.separator(w=5, h=10, st="none")
        cmds.text("TODO: Matrix colision")
        cmds.text("TODO: Soft Feet")
        cmds.text("TODO: Dynamics Joints")
        cmds.text("TODO: Muscle Stuffs")
        cmds.text("TODO: Smart collision")
        cmds.setParent("tabChar")
        # Log Tab
        cmds.gridLayout("layLog", w=390, h=525, nc=1, cwh=(395, 525))
        cmds.rowLayout("logCreate", w=370, h=470, nc=2)
        cmds.separator(w=5, h=3, st="none")
        cmds.scrollLayout(self.promptLog, w=370, h=525, vsb=True)
        cmds.setParent("layRig")
        # Function Buttons
        cmds.separator(w=331, h=2, st="none")
        cmds.rowLayout(w=331, nc=3)
        cmds.button(l="Clear All Components", w=151, h=25, bgc=[DarkGrey[0], DarkGrey[1], DarkGrey[2]], c=partial(masterUIConfig.config().reloadCharField, "compHumanSpine", True, "NDA", False))
        cmds.separator(w=12, h=3, st="none")
        cmds.button(l="Rig Character", w=211, h=25, bgc=[SoftYellow[0], SoftYellow[1], SoftYellow[2]], c=partial(rig.buildRig, self.scriptPath))
        cmds.setParent("tabChar")


        cmds.tabLayout("tabChar", edit=True, tabLabel=[("layRig", 'Rigging'), (layProxy, 'Proxy'), (laySkin, 'Skinning'), (layDynamics, 'Dynamics'), ("layLog", 'Log')])
        cmds.tabLayout(tabFeat, edit=True, tabLabel=[(layComp, 'Components'), (layPresets, 'Presets')])
        cmds.tabLayout(tabOutput, edit=True, tabLabel=[(layOutput, 'Char Output')])
        cmds.setParent(mainForm)

        #---------------------------------------------------------------------------------------
        # PROPERTIES FIELD
        #---------------------------------------------------------------------------------------
        cmds.tabLayout(self.tabProperties, w=330, h=550)
        cmds.scrollLayout(self.PropLay, cr=True, mcw=322)
        # <<< Master Features >>>
        cmds.columnLayout("layMasterFeat", w=308, vis=True)
        cmds.frameLayout("frmGlobalControlMFeat", w=318, cl=False, cll=True, bgs=True, l="Global Control")
        cmds.separator(w=5, h=1, st="none")
        cmds.rowLayout(w=315, nc=1, cl1="left")
        cmds.textFieldGrp("txtCharTypeMFeat", l="Char Type: ", cw2=(120, 170), tx="Select Type", ed=False)
        cmds.setParent('..')
        cmds.rowLayout("layCompSetupMFeat", w=315, nc=1, cl1="left", en=True)
        cmds.radioButtonGrp("radCompSetupMFeat", l="Components Setup: ", nrb=2, la2=["Full", "Separated"], cw=([(1, 120), (2, 60)]), sl=1)
        cmds.setParent('..')
        cmds.rowLayout("layNodeTypeMFeat", w=315, nc=1, cl1="left", en=False)
        cmds.radioButtonGrp("radNodeTypeMFeat", l="Nodes types (BETA): ", nrb=2, la2=["Maya", "Custom"], cw=([(1, 120), (2, 60)]), sl=1)
        cmds.setParent('..')
        cmds.rowLayout("layGlobalScaleMFeat", nc=2, en=True)
        cmds.checkBoxGrp("cbxGlobalScaleMFeat", l="Global Scale: ", ncb=1, cw=([(1, 120), (2, 70)]))
        cmds.text(l="(Free scale your char)")
        cmds.setParent('..')
        cmds.rowLayout("layTrackingCtrlMFeat", nc=2, en=True)
        cmds.checkBoxGrp("cbxTrackingCtrlMFeat", l="Tracking Ctrl: ", ncb=1, cw=([(1, 120), (2, 70)]))
        cmds.text(l="(Control to attach extra motion)")
        cmds.setParent('..')
        cmds.text(l="-----        Adjust global control position        -----")
        cmds.rowLayout("layGblCtrlScaMFeat", nc=1, en=False)
        cmds.floatSliderGrp("fltGblCtrlScaMFeat", l="Control Scale: ", cw=([(1, 120), (2, 50), (3, 120)]), f=True, min=0, max=20, fmn=0, fmx=20, v=1)
        cmds.setParent('..')
        cmds.rowLayout("layGblCtrlTxMFeat", nc=1, en=False)
        cmds.floatSliderGrp("fltGblCtrlTxMFeat", l="Control Trans X: ", cw=([(1, 120), (2, 50), (3, 120)]), f=True, min=-30, max=30, fmn=-30, fmx=30, v=0)
        cmds.setParent('..')
        cmds.rowLayout("layGblCtrlTzMFeat", nc=1, en=False)
        cmds.floatSliderGrp("fltGblCtrlTzMFeat", l="Control Trans Z: ", cw=([(1, 120), (2, 50), (3, 120)]), f=True, min=-30, max=30, fmn=-30, fmx=30, v=0)
        cmds.setParent('..')
        cmds.separator(w=5, h=1, st="none")
        cmds.setParent("layMasterFeat")
        cmds.frameLayout("frmMasterControlMFeat", w=318, cl=False, cll=True, bgs=True, l="Master Control")
        cmds.separator(w=5, h=1, st="none")
        cmds.optionMenuGrp("optEnMasterCtrlMFeat", l="Master Ctrl: ", cw2=(120, 120))
        cmds.menuItem(l="Disabled")
        cmds.menuItem(l="Enabled")
        cmds.rowLayout("layRigModeAttrMFeat", nc=2, en=True)
        cmds.checkBoxGrp("cbxRigModeAttrMFeat", l="Rig Mode Attr: ", ncb=1, cw=([(1, 120), (2, 70)]))
        cmds.text(l="(Skinned, proxy...)")
        cmds.setParent('..')
        cmds.rowLayout("layHideShowCtrlsAttrMFeat", nc=2, en=True)
        cmds.checkBoxGrp("cbxHideShowCtrlsAttrMFeat", l="Hide/Show Ctrls: ", ncb=1, cw=([(1, 120), (2, 70)]))
        cmds.text(l="(Controls visibility)")
        cmds.setParent('..')
        cmds.rowLayout("layHideShowJntsAttrMFeat", nc=2, en=True)
        cmds.checkBoxGrp("cbxHideShowJntsAttrMFeat", l="Hide/Show Joints: ", ncb=1, cw=([(1, 120), (2, 70)]))
        cmds.text(l="(Joints visibility)")
        cmds.setParent('..')
        cmds.rowLayout("layCharSizeAttrMFeat", nc=2, en=True)
        cmds.checkBoxGrp("cbxCharSizeAttrMFeat", l="Char Size Attr: ", ncb=1, cw=([(1, 120), (2, 70)]))
        cmds.text(l="(Size of the character)")
        cmds.setParent('..')
        cmds.rowLayout("layChangeOutfitAttrMFeat", nc=2, en=True)
        cmds.checkBoxGrp("cbxChangeOutfitAttrMFeat", l="Change Outfit Attr: ", ncb=1, cw=([(1, 120), (2, 70)]))
        cmds.text(l="(Change char outfits)")
        cmds.setParent('..')
        cmds.separator(w=5, h=1, st="none")
        cmds.setParent("layMasterFeat")
        cmds.frameLayout("frmExtraSettingsMFeat", w=318, cl=True, cll=True, bgs=True, l="Extra Settings")
        cmds.separator(w=5, h=1, st="none")
        cmds.rowLayout("layCreateQSSMFeat", nc=2, en=True)
        cmds.checkBoxGrp("cbxCreateQSSMFeat", l="Create QSSs: ", ncb=1, cw=([(1, 120), (2, 70)]))
        cmds.text(l="(Pre-setted selection sets)")
        cmds.setParent('..')
        cmds.rowLayout("layOutputSkeletonMFeat", nc=2, en=False)
        cmds.checkBoxGrp("cbxOutputSkeletonMFeat", l="Output Skeleton: ", ncb=1, cw=([(1, 120), (2, 70)]))
        cmds.text(l="(Don't working yet, sry)")
        cmds.setParent('..')
        cmds.separator(w=5, h=1, st="none")
        cmds.setParent("layMasterFeat")
        cmds.frameLayout("frmOutputSettingsMFeat", w=318, cl=True, cll=True, bgs=True, l="Output Settings", en=False)
        cmds.separator(w=5, h=1, st="none")
        cmds.setParent(self.PropLay)
        # Character Geometry
        cmds.columnLayout("layEditCharGeo", w=308, vis=False)
        cmds.frameLayout("frmGlobalControlCGeo", w=318, cl=False, cll=True, bgs=True, l="Attach Geometries")
        cmds.separator(w=5, h=1, st="none")
        cmds.rowLayout(w=315, nc=1, cl1="left")
        cmds.textFieldGrp("txtCharTypeCGeo", l="Char Type: ", cw2=(120, 170), tx="Select Type", ed=False)
        cmds.setParent('..')
        cmds.rowLayout("layBaseBodyCGeo", nc=2)
        cmds.textFieldGrp("txtBaseBodyCGeo", l="Base Body: ", cw2=(120, 125), ed=False)
        cmds.button(l="<<<", w=35, c=partial(masterUIConfig.config().addGeometry, 0, "txtBaseBodyCGeo"))
        cmds.setParent('..')
        cmds.rowLayout("layLeftEyeCGeo", nc=2)
        cmds.textFieldGrp("txtLeftEyeCGeo", l="Left Eye: ", cw2=(120, 125), ed=False)
        cmds.button(l="<<<", w=35, c=partial(masterUIConfig.config().addGeometry, 1, "txtLeftEyeCGeo"))
        cmds.setParent('..')
        cmds.rowLayout("layRightEyeCGeo", nc=2)
        cmds.textFieldGrp("txtRightEyeCGeo", l="Right Eye: ", cw2=(120, 125), ed=False)
        cmds.button(l="<<<", w=35, c=partial(masterUIConfig.config().addGeometry, 2, "txtRightEyeCGeo"))
        cmds.setParent('..')
        cmds.rowLayout("layUpperTeethCGeo", nc=2)
        cmds.textFieldGrp("txtUpperTeethCGeo", l="Upper Teeth: ", cw2=(120, 125), ed=False)
        cmds.button(l="<<<", w=35, c=partial(masterUIConfig.config().addGeometry, 3, "txtUpperTeethCGeo"))
        cmds.setParent('..')
        cmds.rowLayout("layLowerTeethCGeo", nc=2)
        cmds.textFieldGrp("txtLowerTeethCGeo", l="Lower Teeth: ", cw2=(120, 125), ed=False)
        cmds.button(l="<<<", w=35, c=partial(masterUIConfig.config().addGeometry, 4, "txtLowerTeethCGeo"))
        cmds.setParent('..')
        cmds.rowLayout("layTongueCGeo", nc=2)
        cmds.textFieldGrp("txtTongueCGeo", l="Tongue: ", cw2=(120, 125), ed=False)
        cmds.button(l="<<<", w=35, c=partial(masterUIConfig.config().addGeometry, 5, "txtTongueCGeo"))
        cmds.setParent('..')
        cmds.rowColumnLayout("layAllOutfitsCGeo", w=300, nc=1)
        cmds.rowLayout("layOutfitsSpacerCGeo", w=310, nc=2)
        cmds.separator(w=5, h=3, st="none")
        cmds.frameLayout("frmOutfitsCGeo", w=312, cl=True, cll=True, bgs=True, l="Outfits")
        cmds.rowLayout("layOutfitsCGeo", nc=3)
        cmds.textFieldGrp("txtOutfitsCGeo", l="Add Outfit: ", cw2=(120, 105))
        cmds.button(l="+", w=25)
        cmds.button(l="-", w=25)
        cmds.setParent('..')
        cmds.separator(w=5, h=1, st="none")
        cmds.setParent("layEditCharGeo")

        cmds.separator(w=5, h=1, st="none")
        cmds.setParent(self.PropLay)


        cmds.tabLayout(self.tabProperties, edit=True, tabLabel=[(self.PropLay, 'Properties > Rigging > <<< Master Features >>>')])
        cmds.setParent(mainForm)

        cmds.setParent(top=True)
        cmds.formLayout(mainForm, edit=True, af=[(tabName, "top", 0), (tabName, "left", 0),
                                                 ("tabChar", "top", 100), ("tabChar", "left", 0),
                                                 (self.tabProperties, "top", 100), (self.tabProperties, "left", 392),
                                                 #(tabFeat, "top", 125), (tabFeat, "left", 25),
                                                 #(tabOutput, "top", 100), (tabOutput, "left", 160)
                                                 ])
        cmds.showWindow(self.nUI)
        cmds.setFocus(self.nUI)
