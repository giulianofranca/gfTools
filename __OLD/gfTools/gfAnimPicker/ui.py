import maya.cmds as cmds
from functools import partial

class CharacterPicker(object):
    
    def __init__(self):
        
        # Class var
        self.widgets = dict()
        self.namespaces = list()
        
        # Get namespaces
        namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
        for name in namespaces:
            if cmds.objExists(name+':Chest'):
                self.namespaces.append(name)
        
        self.buildUI()
        
    def buildUI(self):
        
        if cmds.window("characterPicker_UI", exists=True):
            cmds.deleteUI("characterPicker_UI")
            
        self.widgets['window'] = cmds.window("characterPicker_UI", t='Character Picker', w=400, h=600, mnb=False, mxb=False)
        
        self.widgets['mainLayout'] = cmds.columnLayout(w=400, h=600)
        
        self.widgets['menuBarLayout'] = cmds.menuBarLayout()
        self.widgets['helpMenu'] = cmds.menu(l='Help', helpMenu=True)
        cmds.menuItem(l='About', c=self.aboutWindow)
        cmds.menuItem(l='Help', c=self.help)
        
        self.widgets['activeChar'] = cmds.optionMenu(l='Active Character: ', w=400)
        
        for name in self.namespaces:
            cmds.menuItem(l=name, p=self.widgets['activeChar'])
            
        self.widgets['formLayout'] = cmds.formLayout(w=400, h=600)
    
        # Create the buttons
        self.widgets['headButton'] = cmds.button(l='', w=40, h=40, bgc=[0, 0.593, 1])
        self.widgets['chestButton'] = cmds.button(l='', w=100, h=40, bgc=[0.824, 0.522, 0.275])
        self.widgets['spine2Button'] = cmds.button(l='', w=100, h=40, bgc=[0.824, 0.522, 0.275])
        self.widgets['spine1Button'] = cmds.button(l='', w=100, h=40, bgc=[0.824, 0.522, 0.275])
        self.widgets['allSpineButton'] = cmds.button(l='', w=30, h=30, bgc=[0.0, 1.0, 0.0])
        
        # Attatch button commands
        cmds.button(self.widgets['headButton'], e=True, c=partial(self.selectControl, ['Head'], [(self.widgets['headButton'], [0, 0.593, 1])]))
        cmds.button(self.widgets['chestButton'], e=True, c=partial(self.selectControl, ['Chest'], [(self.widgets['chestButton'], [0.824, 0.522, 0.275])]))
        cmds.button(self.widgets['spine2Button'], e=True, c=partial(self.selectControl, ['Spine2'], [(self.widgets['spine2Button'], [0.824, 0.522, 0.275])]))
        cmds.button(self.widgets['spine1Button'], e=True, c=partial(self.selectControl, ['Spine1'], [(self.widgets['spine1Button'], [0.824, 0.522, 0.275])]))
        cmds.button(self.widgets['allSpineButton'], e=True, c=partial(self.selectControl, ['Spine1', 'Spine2', 'Chest', 'Head'], 
                                                                      [(self.widgets['spine1Button'], [0.824, 0.522, 0.275]),
                                                                       (self.widgets['spine2Button'], [0.824, 0.522, 0.275]),
                                                                       (self.widgets['chestButton'], [0.824, 0.522, 0.275]),
                                                                       (self.widgets['headButton'], [0, 0.593, 1])]))
        
        # Place the buttons
        cmds.formLayout(self.widgets['formLayout'], e=True, af=[(self.widgets['headButton'], 'left', 175), (self.widgets['headButton'], 'top', 100)])
        cmds.formLayout(self.widgets['formLayout'], e=True, af=[(self.widgets['chestButton'], 'left', 145), (self.widgets['chestButton'], 'top', 150)])
        cmds.formLayout(self.widgets['formLayout'], e=True, af=[(self.widgets['spine2Button'], 'left', 145), (self.widgets['spine2Button'], 'top', 200)])
        cmds.formLayout(self.widgets['formLayout'], e=True, af=[(self.widgets['spine1Button'], 'left', 145), (self.widgets['spine1Button'], 'top', 250)])
        cmds.formLayout(self.widgets['formLayout'], e=True, af=[(self.widgets['allSpineButton'], 'left', 255), (self.widgets['allSpineButton'], 'top', 220)])
        
            
        cmds.showWindow(self.widgets['window'])
        
    def selectControl(self, controls, buttonInfo, *args):
        
        # buttonInfo = [[buttonNames], [buttonBGC]]
        
        activeChar = cmds.optionMenu(self.widgets['activeChar'], q=True, v=True) + ':'
        mods = cmds.getModifiers()
        
        # If held shift...
        if (mods & 1) > 0: 
            for i in range(len(controls)):
                cmds.select(activeChar+controls[i], tgl=True)
                buttonName = buttonInfo[i][0]
                buttonColor = buttonInfo[i][1]
                cmds.button(buttonName, e=True, bgc=[1.0, 1.0, 1.0])
                ++i
                self.createSelectionScriptJob(activeChar+controls[i], buttonName, buttonColor)                
        # if held ctrl...
        # elif (mods & 4) > 0:
            # for i in range(len(controls)):
                # cmds.select(controls[i], d=True)
        # if just clicked...
        else:
            cmds.select(cl=True)
            for i in range(len(controls)):
                cmds.select(activeChar+controls[i], add=True)
                buttonName = buttonInfo[i][0]
                buttonColor = buttonInfo[i][1]
                cmds.button(buttonName, e=True, bgc=[1.0, 1.0, 1.0])
                ++i
                self.createSelectionScriptJob(activeChar+controls[i], buttonName, buttonColor)                     
                
    def createSelectionScriptJob(self, control, buttonName, buttonColor):
        
        scriptJobNum = cmds.scriptJob(event = ['SelectionChanged', partial(self.deselectControl, control, buttonName, buttonColor)], runOnce=True, parent=self.widgets['window'])
        
    def deselectControl(self, control, buttonName, buttonColor):
        
        sel = cmds.ls(sl=True)
        
        if control not in sel:
            cmds.button(buttonName, e=True, bgc=buttonColor)
        else:
            self.createSelectionScriptJob(control, buttonName, buttonColor)
            
    def aboutWindow(self, *args):
        
        if cmds.window('aboutCharPickerUI', exists=True):
            cmds.deleteUI('aboutCharPickerUI')
            
        self.widgets['aboutWindow'] = cmds.window('aboutCharPickerUI', w=300, h=150, mnb=False, mxb=False, t='About')
        cmds.showWindow(self.widgets['aboutWindow'])
        
    def help(self, *args):
        
        cmds.launch(web='http://www.autodesk.com')