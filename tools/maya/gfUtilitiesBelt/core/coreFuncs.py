import sys
import os
import shutil
import datetime
import collections
import shiboken2
import json
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as omui1
from PySide2 import QtCore, QtGui, QtWidgets

from gfUtilitiesBelt.core import fileManagement as fileM
from gftoolsdevelopment.core import widgets as gfWidgets

TAB_WIDGET = "tbw_gfPocketArea"
MAYA_TOOLS_FILTER = ['Recent Commands', 'Recent Files', 'Recent Projects', 'Hotbox', 'Help', 'No sounds available',
                     'No Quick Select Sets Defined']


def getMayaIcons():
    for item in cmds.resourceManager(nf="*"):
        cmds.resourceManager(s=[item, os.path.join(fileM.MAYA_ICONS_PATH, item)])

def getMayaData():
    file = fileM.MAYA_TOOLS_FILE_PATH
    with open(file, "r") as f:
        data = json.load(f, object_pairs_hook=collections.OrderedDict)
    return data

def importPocket():
    filter = "gfPockets (*.gfPocket)"
    file = cmds.fileDialog2(ff=filter, dir=fileM.POCKETS_PATH, ds=2, cap="Import Pocket", fm=1,
        okc="Import", cc="Cancel")[0]
    with open(file, "r") as f:
        content = json.load(f)

    # Version check
    fileVersion = float(content["Current Version"])
    appVersion = float(fileM.REQUIRED_VERSION)
    if fileVersion >= appVersion:
        name = content["Pocket Name"]
        return name, os.path.basename(file), content["Tools"]
    else:
        return

def readPocket(file):
    with open(file, "r") as f:
        content = json.load(f)

    # Version check
    fileVersion = float(content["Current Version"])
    appVersion = float(fileM.REQUIRED_VERSION)
    if fileVersion >= appVersion:
        tools = content["Tools"]
        return tools
    else:
        return
#====================================================================================================================
def getTabWidget():
    tabWidgetPtr = omui1.MQtUtil.findControl(TAB_WIDGET)
    tabWidget = shiboken2.wrapInstance(long(tabWidgetPtr), QtWidgets.QTabWidget)
    return tabWidget


def advancedCreateTab(name="New"):
    tabWidget = getTabWidget()
    createTab(name=name)


def editTab(name, tools=[]):
    # Edit the file
    # Add buttons to the current tab
    # tab_[name]
    mayaData = getMayaData()
    wdgPtr = omui1.MQtUtil.findControl("wdg_scr%s" % name)
    wdg = shiboken2.wrapInstance(long(wdgPtr), QtWidgets.QWidget)
    layFlow = wdg.layout()
    # print(type(layFlow))
    for tool in tools:
        if tool in mayaData.keys():
            btn = gfWidgets.UtilitiesButton()
            btn.setObjectName("preview_%s" % tool)
            if mayaData[tool]["imageLabel"] != "":
                btn.setText(mayaData[tool]["imageLabel"])
            btn.setImage(":%s" % mayaData[tool]["icon"])
            btn.setToolTip(mayaData[tool]["name"])
            btn.clicked.connect(lambda: mel.eval(mayaData[tool]["command"]))
            # btn.mouseDoubleClickEvent.connect(lambda: mel.eval(mayaData[tool]["doubleCommand"]))
            # btn.doubleClicked.connect(lambda: mel.eval(mayaData[tool]["doubleCommand"]))
            layFlow.addWidget(btn)
    fileM.savePocket(name, tools)


def createTab(name="New"):
    tabWidget = getTabWidget()
    pocketsPath = fileM.POCKETS_PATH
    initDir = os.getcwd()
    os.chdir(pocketsPath)
    pockets = [f.split(".")[0] for f in os.listdir(pocketsPath) if os.path.isfile(f)]
    repeat = 0
    for p in pockets:
        if name in p:
            repeat += 1
    if name in pockets:
        name = "%s(%s)" % (name, repeat)
    if name != "home":
        tab_new = QtWidgets.QWidget()
        tab_new.setObjectName("tab_%s" % name)
        lay_new = QtWidgets.QVBoxLayout(tab_new)
        lay_new.setContentsMargins(1, 1, 1, 1)
        lay_new.setSpacing(1)
        lay_new.setObjectName("lay_main%s" % name)
        scr_main = QtWidgets.QScrollArea(tab_new)
        scr_main.setObjectName("scr_%s" % name)
        scr_main.setWidgetResizable(True)
        scr_main.setFrameShape(QtWidgets.QFrame.NoFrame)
        wdg_main = QtWidgets.QWidget(scr_main)
        wdg_main.setObjectName("wdg_scr%s" % name)
        lay_flow = gfWidgets.FlowLayout(wdg_main)
        lay_flow.setObjectName("lay_flow%s" % name)
        lay_flow.setContentsMargins(7, 7, 7, 7)
        lay_flow.setSpacing(2)

        fileM.savePocket(name, [])
        os.chdir(initDir)

        scr_main.setWidget(wdg_main)
        lay_new.addWidget(scr_main)

        tabWidget.addTab(tab_new, name)
        index, widget, exists = checkHomeTab(tabWidget)
        if exists:
            deleteHomeTab(tabWidget)
            tabWidget.setTabsClosable(True)
            tabWidget.setMovable(True)
        return tab_new
    else:
        sys.stderr.write("Can't create a tab with name \"home\".\n")
        return


def deleteHomeTab(tabWidget):
    index, widget, exists = checkHomeTab(tabWidget)
    if exists:
        tabWidget.removeTab(index)
        widget.deleteLater()
    else:
        sys.stdout("Home tab don't exists.\n")


def checkHomeTab(tabWidget):
    length = tabWidget.count()
    homeIndex = None
    homeWidget = None
    for index in range(length):
        widget = tabWidget.widget(index)
        if widget.objectName() == "tab_home":
            homeIndex = index
            homeWidget = widget
    if homeIndex is not None:
        return homeIndex, homeWidget, True
    else:
        return homeIndex, homeWidget, False


def startCheck():
    data = fileM.readSettings()
    settings = data["Settings"]
    pocketsOpen = settings["OpenedPockets"].split(";")


def autoUpdateLibraries():
    if os.path.isfile(fileM.MAYA_TOOLS_FILE_PATH):
        daysStep = 5

        initDir = os.getcwd()
        backupPath = fileM.MAYA_BACKUP_TOOLS_PATH

        os.chdir(backupPath)
        backupList = [name for name in os.listdir(backupPath) if os.path.isfile(name)]
        lastBackup = backupList[-1]
        lastBackupDate = datetime.datetime.strptime(lastBackup.split("_")[1], "%m-%d-%Y")
        backupDay = lastBackupDate + datetime.timedelta(days=daysStep)
        today = datetime.datetime.today()
        if today >= backupDay:
            updateLibraries()
        os.chdir(initDir)
    else:
        updateLibraries()


def updateLibraries():
    amount = 0
    cmds.progressWindow(title="Update Libraries", progress=amount, status = "Getting mayaData path: 0%")

    # Get mayaData path.
    mayaDataPath = fileM.MAYA_TOOLS_PATH
    backupPath = fileM.MAYA_BACKUP_TOOLS_PATH
    mayaDataFilePath = fileM.MAYA_TOOLS_FILE_PATH
    amount += 12.5
    cmds.progressWindow(e=True, progress=amount, status="Check if old mayaData file exists: "+ str(amount) +"%")

    # Check if old mayaData file exists.
    if os.path.isfile(mayaDataFilePath):
        backupLength = len([name for name in os.listdir(backupPath) if os.path.isfile(name)])
        if backupLength >= 5:
            # Delete the first backup
            os.remove(os.listdir(backupPath)[0])
        name = 'mayaData_%s.json' % (datetime.datetime.now().strftime('%m-%d-%Y_%H-%M'))
        os.rename(mayaDataFilePath, os.path.join(mayaDataPath, name))
        shutil.move(os.path.join(mayaDataPath, name), os.path.join(backupPath, name))
    amount += 12.5
    cmds.progressWindow(e=True, progress=amount, status="Getting Maya Qt Window: "+ str(amount) +"%")

    # Get Maya Qt Window Pointer
    win = omui1.MQtUtil.mainWindow()
    mWindow = shiboken2.wrapInstance(long(win), QtWidgets.QMainWindow)
    amount += 12.5
    cmds.progressWindow(e=True, progress=amount, status="Setting menu filters: "+ str(amount) +"%")

    # Set menu filters and variables
    filterList = MAYA_TOOLS_FILTER
    mMenu = list()
    mCmdList = collections.OrderedDict()
    amount += 12.5
    cmds.progressWindow(e=True, progress=amount, status="Getting Maya menu bar: "+ str(amount) +"%")

    # Get Maya Menu Bar
    for widget in mWindow.children():
        if type(widget) is QtWidgets.QMenuBar:
            mMenuBar = widget
    amount += 12.5
    cmds.progressWindow(e=True, progress=amount, status="Filtering Maya menus: "+ str(amount) +"%")

    # Filter Maya Menus
    for menu in mMenuBar.children():
        if type(menu) is QtWidgets.QMenu and all(filter not in menu.title() for filter in filterList):
            mMenu.append(menu)
    amount += 12.5
    cmds.progressWindow(e=True, progress=amount, status="Retrieving all tools: "+ str(amount) +"%")

    # Retrieve all commands information from each menu
    for qMenu in mMenu:
        qMenu.aboutToShow.emit()
        getMayaCommandsFromMenu(qMenu, filterList, qMenu, mCmdList)
    amount += 12.5
    cmds.progressWindow(e=True, progress=amount, status="Saving the commands: "+ str(amount) +"%")

    # Save the commands info to an file in json format
    with open(mayaDataFilePath, 'w') as f:
        json.dump(mCmdList, f, indent=4, ensure_ascii=False)
    amount += 12.5
    cmds.progressWindow(e=True, progress=amount, status="Finalizing: "+ str(amount) +"%")
    cmds.pause(seconds=1)
    cmds.progressWindow(endProgress=True)


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
                        cmdDict[keyName] = collections.OrderedDict([('name', itemName),
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
