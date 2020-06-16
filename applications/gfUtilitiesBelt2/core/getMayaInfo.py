# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

====================================================================================================

How to use:
    * Copy the parent folder to the MAYA_SCRIPT_PATH.
    * To find MAYA_SCRIPT_PATH paste this command in a Python tab:
        import os; os.environ["MAYA_SCRIPT_PATH"].split(";")
    * In Maya, go to Windows > Settings/Preferences > Plug-in Manager.
    * Browse for "gfTools > plug-ins > dev > python"
    * Find gfTools_P.py and import it.

Requirements:
    * Maya 2017 or above.

Todo:
    * NDA

Sources:
    * NDA

This code supports Pylint. Rc file in project.
"""
import sys
import os
import json
import shiboken2
from collections import OrderedDict
from PySide2 import QtWidgets
import maya.OpenMayaUI as omui1
import maya.cmds as cmds
import maya.mel as mel

if sys.version_info.major >= 3:
    import pickle
else:
    import cPickle as pickle

from gfUtilitiesBelt2.core import appInfo
reload(appInfo)

# TODO: Update maya tools filter from maya info ???
# TODO: Remove JSON support and only generate binary file.


kMayaToolsFilter = [
    "Recent Commands",
    "Recent Files",
    "Recent Projects",
    "Hotbox",
    "Help",
    "No sounds available",
    "No Quick Select Sets Defined"
]
kMayaInfoFileName = "mayaData"
kMayaInfoFilePath = os.path.join(appInfo.kCorePath, kMayaInfoFileName)




def writeMayaInfoFile(mayaInfo, bin=False):
    """Write a json file with specified dict containing all Maya info.

    Args:
        mayaInfo (OrderedDict): The info dictionary to write in the json file.
        bin (bool: False [Optional]): Write in binary mode.

    Returns:
        True: If succeeded.
    """
    fullPath = kMayaInfoFilePath
    if bin:
        with open(fullPath, "wb") as f:
            pickle.dump(mayaInfo, f, pickle.HIGHEST_PROTOCOL)
    else:
        with open(fullPath, "w") as f:
            json.dump(mayaInfo, f, indent=4, ensure_ascii=False)
    
    return True


def readMayaInfoFile(bin=False):
    """Read the json file containing all Maya info.

    Args:
        bin (bool: False [Optional]): Read in binary mode.

    Returns:
        OrderedDict: The dictionary containing all the Maya info.

    Raises:
        RuntimeError: If the file does not exists.
    """
    fullPath = kMayaInfoFilePath
    if not checkMayaInfoFile():
        raise RuntimeError("Maya info file not founded.")
    if bin:
        with open(fullPath, "rb") as f:
            data = pickle.load(f)
    else:
        with open(fullPath, "r") as f:
            data = json.load(f, object_pairs_hook=OrderedDict)

    return data


def checkMayaInfoFile():
    """Check if Maya info file exists and is valid.

    Returns:
        True or False: If file exists and is valid or not.
    """
    fileName = kMayaInfoFileName
    path = appInfo.kCorePath
    if fileName not in os.listdir(path):
        return False

    return True


def updateMayaInfo():
    """Update all infos gathered from Maya.

    Returns:
        True: If succeeded.
    """
    # TODO: writeMayaInfoFile in binary mode.
    mayaWin = getMayaWindow()
    mayaMenuBar = getMayaMenuBar(mayaWin)
    mayaMenuList = filterMayaMenus(mayaMenuBar)
    data = OrderedDict()
    menuCount = len(mayaMenuList)
    useProgressBar("Gathering Maya info...", 0, begin=True, maxValue=menuCount)
    for i, menu in enumerate(mayaMenuList):
        useProgressBar("Gathering Maya info...", i)
        menu.aboutToShow.emit()
        getCmdsFromMenu(menu, menu, data)
    writeMayaInfoFile(data, bin=False)
    useProgressBar("Gathering Maya info...", i, end=True)
    return True


def searchMayaTool():
    pass




###########################
# HIGH-LEVEL FUNCTIONS

def getMayaWindow():
    """Return the Maya main window as QMainWindow object.
    
    Returns:
        QMainWindow: The Maya main window as QMainWindow object.

    Raises:
        RuntimeError: If not succeeded.
    """
    win = omui1.MQtUtil.mainWindow()
    qWindow = shiboken2.wrapInstance(long(win), QtWidgets.QMainWindow)
    return qWindow


def getMayaMenuBar(qWindow):
    """Return the menu bar from the Maya main window.

    Args:
        qWindow (QMainWindow): The window to find the menu bar.

    Returns:
        QMenuBar: The menu bar.

    Raises:
        RuntimeError: If its not a menu bar in the specified window.
    """
    for widget in qWindow.children():
        if isinstance(widget, QtWidgets.QMenuBar):
            qMenuBar = widget
            return qMenuBar
    raise RuntimeError("Could not find a QMenuBar in the window specified.")


def filterMayaMenus(qMenuBar):
    """Return a list of menus attatched in a menu bar.

    Args:
        qMenuBar (QMenuBar): The menu bar to be inspected.

    Returns:
        list: The list of QMenus attatched in the specified menu bar.
    """
    filterList = kMayaToolsFilter
    menuList = []
    for menu in qMenuBar.children():
        if isinstance(menu, QtWidgets.QMenu) and all(filt not in menu.title() for filt in filterList):
            menuList.append(menu)
    
    return menuList


def getCmdsFromMenu(qMenu, parentMenu, outDict):
    """Retrieve a dictionary containing the information of all the Maya tools.

    Args:
        qMenu (QMenu): The menu to be inspected.
        parentMenu (qMenu): The parent of the qMenu.
        outDict (OrderedDict): The output dictionary containing all the data.
    """
    filterList = kMayaToolsFilter
    for menuItem in qMenu.children():
        if isinstance(menuItem, QtWidgets.QMenu):
            if not any(filt in menuItem.title() for filt in filterList):
                menuItem.aboutToShow.emit()
                keyName = getFullPathItem(menuItem)[0]
                del outDict[keyName]
                getCmdsFromMenu(menuItem, parentMenu, outDict)
        elif isinstance(menuItem, QtWidgets.QWidgetAction):
            if not any(filt in menuItem.text() for filt in filterList):
                if not menuItem.isSeparator():
                    mMenuItem = omui1.MQtUtil.fullName(long(shiboken2.getCppPointer(menuItem)[0]))
                    toolInfo = OrderedDict()
                    keyName, path = getFullPathItem(menuItem)
                    toolInfo["name"] = menuItem.text()
                    toolInfo["info"] = menuItem.toolTip()
                    toolInfo["category"] = path[0]
                    doubleCmd = getInfoFromMenuItem(mMenuItem, toolInfo)
                    if doubleCmd is not None:
                        outDict.items()[-1][1]["doubleCommand"] = doubleCmd
                    else:
                        outDict[keyName] = toolInfo


def getInfoFromMenuItem(menuItem, menuInfo):
    """Get icon from Maya menuItem.

    Args:
        menuItem (str): The menuItem to be inspected.
        menuInfo (OrderedDict): The output tool info dictionary.

    Returns:
        None or str: None if the specified menuItem is not an optionBox or the double command if the specified menuItem is an optionBox.
    """
    command = cmds.menuItem(menuItem, q=True, c=True)
    if command is not None:
        command = str(command)
    commandType = cmds.menuItem(menuItem, q=True, dmc=True, stp=True)

    if cmds.menuItem(menuItem, q=True, iob=True):
        # If this menuItem is an optionBox
        return command

    itemIconPath = cmds.menuItem(menuItem, q=True, i=True)
    if itemIconPath == "":
        itemIconPath = cmds.menuItem(menuItem, q=True, fi=True)
        if itemIconPath == "":
            itemIconPath = "commandButton.png" if commandType == "mel" else "pythonFamily.png"

    if cmds.menuItem(menuItem, q=True, i=True):
        itemImageLabel = ""
    else:
        itemImageLabel = cmds.menuItem(menuItem, q=True, iol=True)
        if itemImageLabel == "":
            tokens = menuInfo["name"].split(" ")
            if len(tokens) == 1:
                if len(menuInfo["name"]) > 3:
                    itemImageLabel = menuInfo["name"][:4]
                else:
                    itemImageLabel = menuInfo["name"]
            else:
                itemImageLabel = "".join([first[0] for first in tokens])

    menuInfo["icon"] = itemIconPath
    menuInfo["imageLabel"] = itemImageLabel
    menuInfo["command"] = command
    menuInfo["doubleCommand"] = None
    menuInfo["commandType"] = commandType



def getFullPathItem(item):
    """Get the full path of a QMenu.

    Args:
        item (QMenu or QWidgetAction): The item to be inspected.

    Returns:
        str: The full path of the item.
        list: The parent tree of the specified object.
    """
    parentList = []
    parItem = item
    while True:
        if isinstance(item.parentWidget(), QtWidgets.QMenu):
            parentList.append(item.parentWidget().title())
            item = item.parentWidget()
        else:
            break
    parentList.reverse()
    if isinstance(parItem, QtWidgets.QMenu):
        name = parItem.title()
    else:
        name = parItem.text()
    fullPath = "|".join(parentList) + "|%s" % name
    return fullPath, parentList


def useProgressBar(status, progress, begin=False, end=False, maxValue=100):
    """Use the Maya main progress bar.

    Args:
        status (str): The current status of the progress.
        progress (int): The current progress.
        begin (bool: False [Optional]): Used to begin a new progress bar.
        end (bool: False [Optional]): Used to end a progress bar.
        maxValue (int: 100 [Optional]): Used to specify the max value of the progress bar.
    """
    gMainProgressBar = mel.eval("$tmp = $gMainProgressBar")
    if begin:
        cmds.progressBar(
            gMainProgressBar, e=True, bp=True, ii=False, st=status,
            max=maxValue
        )
    elif end:
        cmds.progressBar(gMainProgressBar, e=True, ep=True)
    else:
        cmds.progressBar(gMainProgressBar, e=True, st=status, pr=progress)
