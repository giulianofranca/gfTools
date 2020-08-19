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
# pylint: disable=missing-function-docstring, wrong-import-position
import sys
import os
import platform
import shutil
import maya.cmds as cmds

kAppPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
kScriptsPath = os.path.join(kAppPath, "scripts", "standalone")
if not kScriptsPath in sys.path:
    sys.path.append(kScriptsPath)

# pylint: disable=import-error
# Import gfTools module to get information needed to install Maya plugins
import gfTools


kMayaVersion = cmds.about(version=True)

kDialogTitle = "gfTools for Maya Installation"
kInstallMsg = "This will install gfTools plugins for Autodesk Maya. Are you sure you want to install it?"
kWrongVersionMsg = "Wrong Maya version (%s). gfTools can only be installed in Autodesk Maya versions 2018 to 2020. Installation interrupted." % kMayaVersion
kModPathErrorMsg = "Could not find Maya module path. Installation interrupted."
kCouldNotInfoMsg = "Could not get application info. Installation interrupted."
kSystemNotRecMsg = "System (%s) not compatible." % platform.system()
kAlreadyInstalledMsg = "gfTools is already installed. Installation interrupted."
kSucessMsg = "Installation completed! You need to restart Maya to take effects."

def windows():
    return platform.system() == "Windows"

def linux():
    return platform.system() == "Linux"

def macOS():
    return platform.system() == "Darwin"

def printMsg(msg):
    sys.stdout.write("%s\n" % msg)


def getMayaVersion():
    printMsg("Checking Maya version...")
    status = getAppInfo()
    if not status:
        return False
    status = gfTools.verifyMayaVersion()
    if not status:
        emitMsg(kWrongVersionMsg)
        return False
    return True

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

def getAppInfo():
    data = gfTools.getAppInfo()
    if not data:
        emitMsg(kCouldNotInfoMsg)
        return False
    return data

def checkMod(modPath):
    filePath = os.path.join(modPath, "gfTools.mod")
    return os.path.isfile(filePath)

def generateModFile(data):
    printMsg("Generating module file...")
    fileName = os.path.join(kAppPath, "gfTools.mod")
    if windows():
        plat = "win64"
    elif linux():
        plat = "linux"
    else:
        plat = "mac"
    lines = ["+ PLATFORM:%s MAYAVERSION:%s %s %s %s\n" % (plat, kMayaVersion, data["Application"], data["Current Version"], data["Path"])]
    lines.append("PYTHONPATH +:= core/resources/widgets/python\n")
    lines.append("PYTHONPATH +:= tools/maya\n")
    lines.append("PYTHONPATH +:= scripts/standalone\n")
    lines.append("PYTHONPATH +:= scripts/maya\n")
    lines.append("MAYA_PLUG_IN_PATH +:= plugin/maya/release/Maya%s\n" % kMayaVersion)
    lines.append("MAYA_SHELF_PATH +:= scripts/maya/shelves\n")
    lines.append("MAYA_CUSTOM_TEMPLATE_PATH +:= scripts/maya/AETemplates\n")
    lines.append("XBMLANGPATH +:= core/resources/icons%s\n" % ("/%B" if linux() else ""))
    with open(fileName, "w") as f:
        f.writelines(lines)
    return fileName

def installModFile(modFile, mayaModPath):
    # pylint: disable=broad-except
    printMsg("Installing module file...")
    try:
        shutil.copy(modFile, mayaModPath)
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

def emitInstallPrompt():
    status = cmds.confirmDialog(t=kDialogTitle, m=kInstallMsg, b=["Install", "Cancel"], db="Install",
                                cb="Cancel", ds="Cancel", icn="question")
    if status == "Install":
        return True
    else:
        return False

#############################################################################################
# RUN

def onMayaDroppedPythonFile(*args):
    # pylint: disable=unused-argument
    # 1- Prompt installation
    printMsg("")
    installIt = emitInstallPrompt()
    if not installIt:
        emitMsg("The installation was canceled.")
        return
    printMsg("Installing gfTools for Autodesk Maya %s." % kMayaVersion)
    # 2- Verify Maya version compatibility
    verify = getMayaVersion()
    if not verify:
        return
    # 3- Get Maya module path
    modPath = getMayaModulePath()
    if not modPath:
        return
    printMsg("Maya module path: %s" % modPath)
    # 4- Get gfTools information
    appData = getAppInfo()
    if not appData:
        return
    appData["Path"] = kAppPath
    printMsg("gfTools version: %s" % appData["Current Version"])
    printMsg("gfTools directory path: %s" % appData["Path"])
    # 5- Generate the mod file
    status = checkMod(modPath)
    if status:
        emitMsg(kAlreadyInstalledMsg, icn="warning")
        return
    modFile = generateModFile(appData)
    # 6- Copy the generated mod file to Maya mod path
    status = installModFile(modFile, modPath)
    if not status:
        os.remove(modFile)
        return
    # 7- Delete leftover file
    printMsg("Cleaning leftover files...")
    os.remove(modFile)
    # 8- Prompt to restart Maya
    emitMsg(kSucessMsg, icn="information")
