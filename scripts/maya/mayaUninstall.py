# -*- coding: utf-8 -*-
"""
Copyright 2020 Giuliano Franca

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

====================================================================================================

How to use:
    * Drag and drop this script in the Autodesk Maya viewport

Requirements:
    * Maya 2018 or above.

This code supports Pylint. Rc file in project.
"""
# pylint: disable=missing-function-docstring
import sys
import os
import platform
import maya.cmds as cmds

kAppPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

kMayaVersion = cmds.about(version=True)

kDialogTitle = "gfTools for Maya Uninstallation"
kUninstallMsg = "This will uninstall gfTools plugins for Autodesk Maya. Are you sure you want to uninstall it?"
kModPathErrorMsg = "Could not find Maya module path. Uninstallation interrupted."
kAppNotFounded = "gfTools installation not founded. Uninstallation interrupted."
kSucessMsg = "Uninstallation completed! You need to restart Maya to take effects."

def windows():
    return platform.system() == "Windows"

def linux():
    return platform.system() == "Linux"

def macOS():
    return platform.system() == "Darwin"

def printMsg(msg):
    sys.stdout.write("%s\n" % msg)


def getMayaModulePath():
    printMsg("Checking Maya module path...")
    mModPath = os.environ["MAYA_MODULE_PATH"]
    paths = mModPath.split(";") if windows() else mModPath.split(":")
    if windows():
        matches = [kMayaVersion, "Common Files"]
    elif linux():
        matches = [kMayaVersion, os.environ["HOME"]]
    elif macOS():
        matches = [kMayaVersion]
    path = None
    for modPath in paths:
        if all(match in modPath for match in matches):
            path = modPath
            break
    if not path:
        emitMsg(kModPathErrorMsg)
        return None
    if not os.path.isdir(path):
        os.mkdir(path)
    return os.path.abspath(path)

def checkMod(modPath):
    filePath = os.path.join(modPath, "gfTools.mod")
    return os.path.isfile(filePath)

def uninstallModFile(modFile):
    # pylint: disable=broad-except
    printMsg("Uninstalling module file...")
    try:
        os.remove(modFile)
    except Exception as err:
        emitMsg(err)
        return False
    return True

def emitMsg(msg, b=["Ok"], db="Ok", icn="critical", **kwargs):
    # pylint: disable=exec-used, dangerous-default-value, unused-argument, invalid-name
    cmd = "cmds.confirmDialog(t=kDialogTitle, m=msg, b=b, db=db, icn=icn"
    for key, value in kwargs.items():
        cmd += ', %s="%s"' % (key, value)
    cmd += ")"
    exec(cmd)
    printMsg(msg)

def emitUninstallPrompt():
    status = cmds.confirmDialog(t=kDialogTitle, m=kUninstallMsg, b=["Uninstall", "Cancel"], db="Uninstall",
                                cb="Cancel", ds="Cancel", icn="question")
    if status == "Uninstall":
        return True
    else:
        return False

#############################################################################################
# RUN

def onMayaDroppedPythonFile(*args):
    # pylint: disable=unused-argument
    # 1- Promp Uninstallation
    printMsg("")
    uninstallIt = emitUninstallPrompt()
    if not uninstallIt:
        emitMsg("The uninstallation was canceled.")
        return
    printMsg("Uninstalling gfTools for Autodesk Maya %s." % kMayaVersion)
    # 2- Get Maya module path
    modPath = getMayaModulePath()
    if not modPath:
        return
    printMsg("Maya module path: %s" % modPath)
    # 3- Check gfTools installation
    status = checkMod(modPath)
    if not status:
        emitMsg(kAppNotFounded, icn="warning")
        return
    printMsg("gfTools directory path: %s" % kAppPath)
    # 4- Find and delete gfTools mod file
    modFile = os.path.join(modPath, "gfTools.mod")
    printMsg("Found gfTools mod file: %s" % modFile)
    status = uninstallModFile(modFile)
    if not status:
        return
    # 5- Promp to restart Maya
    emitMsg(kSucessMsg, icn="information")
