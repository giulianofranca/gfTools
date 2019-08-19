# Started Thursday, November 8, 2018, 2:30 PM
###########################################################################################################################
# WORKFLOW
###########################################################################################################################
# 1- Find all Maya tools with their icons and create a offline file to store them.
# 2- Open the UI.
# 3- Create a Tab
# 4- Select a preset or a custom tab.
# 5- If custom tab, select all your tools in a list with categories.
# 6- When finished, click create.
# 7- Single or double click in a tool to use it.

import sys
import os
import re
import json
import shiboken2
from collections import OrderedDict
from maya import cmds
from maya import OpenMayaUI as omui1
from PySide2 import QtWidgets


####################
# MENUBAR
####################


def createNewTab():
    pass


def deleteCurrentTab():
    pass


def importTab():
    pass


def importMayaShelf():
    # 1- Open a file dialog to retrieve a .mel file
    shelvesPath = '%s/prefs/shelves' % cmds.about(pd=True)
    shelfFilter = '*.mel'
    selectedFile = cmds.fileDialog2(cap='Import Maya Shelf.', fm=1, ff=shelfFilter, dir=shelvesPath)[0]

    # 2- Parse the file using re module
    pattern = re.compile(r'shelfButton(.*?);', re.DOTALL)
    shelfButtons = list()
    with open(selectedFile, 'r') as f:
        content = f.read()
        matches = pattern.findall(content)
    result = [shelfButtons.append(m.replace('\n', '').replace('        ', '')) for m in matches]

    # 3- If the file is not a shelf, return a error
    if shelfButtons != [] and len(shelfButtons) >= 1:
        pass
    else:
        return False

    # Take all the information from a shelfButton and put in a dict.
    info = OrderedDict()
    for btn in shelfButtons:
        w = re.search(r'-width (.*?)-height', btn).group(1)
        h = re.search(r'-height (.*?)-manage', btn).group(1)
        toolTip = re.search(r'-annotation (.*?)-enableBackground', btn).group(1)[1:-2]
        alignment = re.search(r'-align (.*?)-label', btn).group(1)[1:-2]
        name = re.search(r'-label (.*?)-labelOffset', btn).group(1)[1:-2]
        try:
            imageLabel = re.search(r'-imageOverlayLabel (.*?)-overlayLabelColor', btn).group(1)[1:-2]
        except:
            imageLabel = None
        icon = re.search(r'-image (.*?)-image1', btn).group(1)[1:-2]
        style = re.search(r'-style (.*?)-marginWidth', btn).group(1)[1:-2]
        command = re.search(r'-command (.*?)-sourceType', btn).group(1)[1:-2]
        try:
            doubleCommand = re.search(r'-doubleClickCommand (.*?)-commandRepeatable', btn).group(1)[1:-2]
        except:
            doubleCommand = None
        commandType = re.search(r'-sourceType (.*?)(-commandRepeatable|-doubleClickCommand)', btn).group(1)[1:-2]
        menuItems = re.findall(r'-mi (.*?)-mi', btn)
        if menuItems == []:
            menuItems = None
        shelfBtnInfo = OrderedDict([
            ('width', w),
            ('height', h),
            ('toolTip', toolTip),
            ('align', alignment),
            ('name', name),
            ('imageLabel', imageLabel),
            ('icon', icon),
            ('style', style),
            ('command', command),
            ('doubleCommand', doubleCommand),
            ('commandType', commandType),
            ('menuItems', menuItems)])
        info[name] = shelfBtnInfo

    # 4- Get the shelfButton information in a temporary json file
    path = '%s/test.json' % shelvesPath
    with open(path, 'w') as f:
        json.dump(info, f, indent=4, ensure_ascii=False)

    # 5- Create a tab than add the shelfButton information.

    # 6- Delete the temporary json file.


def exportTab():
    pass


def exportMayaShelf():
    pass


def createTool():
    pass


def updateLibraries():
    # Get Maya Qt Window Pointer
    win = omui1.MQtUtil.mainWindow()
    mWindow = shiboken2.wrapInstance(long(win), QtWidgets.QMainWindow)

    # Set menu filters and variables
    filterList = ['Recent Commands', 'Recent Files', 'Recent Projects', 'Hotbox', 'Help', 'No sounds available',
        'No Quick Select Sets Defined']
    mMenu = list()
    mCmdList = OrderedDict()

    # Get Maya Menu Bar
    for widget in mWindow.children():
        if type(widget) is QtWidgets.QMenuBar:
            mMenuBar = widget

    # Filter Maya Menus
    for menu in mMenuBar.children():
        if type(menu) is QtWidgets.QMenu and all(filter not in menu.title() for filter in filterList):
            mMenu.append(menu)

    # Retrieve all commands information from each menu
    for qMenu in mMenu:
        qMenu.aboutToShow.emit()
        getMayaCommandsFromMenu(qMenu, filterList, qMenu, mCmdList)

    # Save the commands info to an file in json format
    path = '%s/scripts/gfTools/gfMayaTool/fileMenuInfo.json' % cmds.about(pd=True)
    with open(path, 'w') as f:
        json.dump(mCmdList, f, indent=4, ensure_ascii=False)



def getMayaCommandsFromMenu(menu, filterList, parentMenu, cmdDict):
    # Retrieve all QWidgetAction from each menu
    for menuItem in menu.children():
        if type(menuItem) is QtWidgets.QMenu:
            if not any(filter in menuItem.title() for filter in filterList):
                menuItem.aboutToShow.emit()
                parentList = getParentList(menuItem)
                keyName = '|'.join(parentList) + '|%s' % menuItem.title()
                del cmdDict[keyName]
                getMayaCommandsFromMenu(menuItem, filterList, parentMenu, cmdDict)
        elif type(menuItem) is QtWidgets.QWidgetAction:
            if not any(filter in menuItem.text() for filter in filterList):
                if not menuItem.isSeparator():
                    mMenuItem = omui1.MQtUtil.fullName(long(shiboken2.getCppPointer(menuItem)[0]))
                    parentList = getParentList(menuItem)
                    keyName = '|'.join(parentList) + '|%s' % menuItem.text()
                    itemName = menuItem.text()
                    itemInfo = menuItem.toolTip()
                    category = parentList[0]
                    command = cmds.menuItem(mMenuItem, q=True, c=True)
                    if command is not None:
                        command = str(command)
                    commandType = cmds.menuItem(mMenuItem, q=True, dragMenuCommand=True, stp=True)
                    itemIconPath = cmds.menuItem(mMenuItem, q=True, i=True)
                    if itemIconPath == '':
                        itemIconPath = cmds.menuItem(mMenuItem, q=True, fi=True)
                        if itemIconPath == '':
                            if commandType == 'mel':
                                itemIconPath = 'commandButton.png'
                            else:
                                itemIconPath = 'pythonFamily.png'
                    if cmds.menuItem(mMenuItem, q=True, i=True):
                        itemImageLabel = ''
                    else:
                        itemImageLabel = cmds.menuItem(mMenuItem, q=True, iol=True)
                        if itemImageLabel == '':
                            tokens = menuItem.text().split(' ')
                            if len(tokens) == 1:
                                if len(menuItem.text()) > 3:
                                    itemImageLabel = menuItem.text()[:4]
                                else:
                                    itemImageLabel = menuItem.text()
                            else:
                                itemImageLabel = ''.join([first[0] for first in tokens])
                    if cmds.menuItem(mMenuItem, q=True, iob=True):
                        cmdDict.items()[-1][1]['doubleCommand'] = command
                    else:
                        cmdDict[keyName] = OrderedDict([('name', itemName),
                                                        ('info', itemInfo),
                                                        ('category', category),
                                                        ('imageLabel', itemImageLabel),
                                                        ('icon', itemIconPath),
                                                        ('command', command),
                                                        ('doubleCommand', None),
                                                        ('commandType', commandType)])


def getParentList(item):
    parentList = list()
    for x in range(10):
        if type(item.parentWidget()) is QtWidgets.QMenu:
            parentList.append(item.parentWidget().title())
            item = item.parentWidget()
        else:
            break
    parentList.reverse()
    return parentList


def buildMayaMenus():
    from maya import mel
    # C:\Program Files\Autodesk\Maya2017\scripts\startup
    mel.eval('buildFileMenu')
    mel.eval('buildEditMenu("MayaWindow|mainEditMenu")')
    mel.eval('ModCreateMenu mainCreateMenu')
    mel.eval('buildSelectMenu MayaWindow|mainSelectMenu')
    mel.eval('ModObjectsMenu MayaWindow|mainModifyMenu')
    mel.eval('buildViewMenu("MayaWindow|mainWindowMenu")')
    mel.eval('PolygonsMeshMenu MayaWindow|mainMeshMenu')
    mel.eval('PolygonsBuildMenu MayaWindow|mainEditMeshMenu')
    mel.eval('PolygonsBuildToolsMenu MayaWindow|mainMeshToolsMenu')
    mel.eval('ModelingMeshDisplayMenu MayaWindow|mainMeshDisplayMenu')
    mel.eval('ModelingCurvesMenu MayaWindow|mainCurvesMenu')
    mel.eval('ModelingSurfacesMenu MayaWindow|mainSurfacesMenu')
    mel.eval('ChaDeformationsMenu MayaWindow|mainDeformMenu')
    mel.eval('ModelingUVMenu MayaWindow|mainUVMenu')
    mel.eval('ModelingGenerateMenu MayaWindow|mainGenerateMenu')
    # Rigging
    mel.eval('ChaSkeletonsMenu MayaWindow|mainRigSkeletonsMenu')
    mel.eval('ChaSkinningMenu MayaWindow|mainRigSkinningMenu')
    mel.eval('ChaDeformationsMenu MayaWindow|mainRigDeformationsMenu')
    mel.eval('AniConstraintsMenu MayaWindow|mainRigConstraintsMenu')
    mel.eval('ChaControlsMenu MayaWindow|mainRigControlMenu')
    # Animation
    mel.eval('AniKeyMenu MayaWindow|mainKeysMenu')
    mel.eval('AniPlaybackMenu MayaWindow|mainPlaybackMenu')
    mel.eval('AniVisualizeMenu MayaWindow|mainVisualizeMenu')
    mel.eval('ChaDeformationsMenu MayaWindow|mainDeformationMenu')
    mel.eval('AniConstraintsMenu MayaWindow|mainConstraintsMenu')
    # FX
    mel.eval('DynParticlesMenu MayaWindow|mainParticlesMenu')
    mel.eval('DynFluidsMenu MayaWindow|mainFluidsMenu')
    mel.eval('DynClothMenu MayaWindow|mainNClothMenu')
    mel.eval('DynCreateHairMenu MayaWindow|mainHairMenu')
    mel.eval('NucleusConstraintMenu MayaWindow|mainNConstraintMenu')
    mel.eval('NucleusCacheMenu MayaWindow|mainNCacheMenu')
    mel.eval('DynFieldsSolverMenu MayaWindow|mainFieldsSolverMenu')
    mel.eval('DynEffectsMenu MayaWindow|mainDynEffectsMenu')
    # Rendering
    mel.eval('RenShadersMenu MayaWindow|mainShadingMenu')
    mel.eval('RenTexturingMenu MayaWindow|mainRenTexturingMenu')
    mel.eval('RenRenderMenu MayaWindow|mainRenderMenu')
    mel.eval('buildCartoonMenu MayaWindow|mainCartoonMenu')
    mel.eval('RenStereoMenu MayaWindow|mainStereoMenu')
    # Missing: Cache | MASH | Bifrost Fluids | Boss


def autoLoadTool():
    # 1- Read the files in tool folder.
    # 2- Create a custom userSetup.py to apply auto load tool function.
    # 3- Create a boolean variable to store this information in a file.
    # 4- Read this information every time when application starts.
    pass


def howToUse():
    pass


def about():
    pass


####################
# MAIN UI
####################

def createShelfLayout():
    pass


####################
# CORE
####################

def createShelfButton(toolTip, name, imageLabel, icon, command, doubleCommand, commandType):
    w = 35
    h = 35
    font = 'plainLabelFont'
    olc = (0.8, 0.8, 0.8)
    olbc = (0, 0, 0, 0.5)
    style = 'iconOnly'
    alpha = True
    background = False
    cmds.shelfButton(enableCommandRepeat=True, en=True, w=w, h=h, m=True, vis=True, po=False, ann=toolTip, enableBackground=background,
                     al='center', l=name, lo=0, ua=alpha, font=font, iol=imageLabel, overlayLabelColor=olc, overlayLabelBlackColor=olbc, i=icon,
                     il=icon, st=style, mw=0, mh=0, c=command, stp=commandType, rpt=True, dcc=doubleCommand, flat=True)


def execTool():
    pass
