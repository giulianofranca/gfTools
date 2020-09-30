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
import os
import platform

# Check if this script is using mayapy.
try:
    import maya.cmds as cmds
except ImportError:
    raise RuntimeError("Could not find Maya. You should use this script inside Maya, just drag it into the viewport.")

mayaVersion = cmds.about(version=True)

# Import gfCore module to get information needed to install gfTools Maya plugins. gfCore is platform independant.
try:
    from gfTools import gfCore
except ImportError:
    raise RuntimeError("Could not find gfCore module.")

dialogTitle = "gfTools for Maya Uninstallation"
uninstallMsg = "This will uninstall gfTools plugins for Autodesk Maya. Are you sure you want to uninstall it?"
modPathErrorMsg = "Could not find Maya module path. Uninstallation interrupted."
appNotFounded = "gfTools installation not founded. Uninstallation interrupted."
sucessMsg = "Uninstallation completed! You need to restart Maya to take effects."


def windows():
    return platform.system() == "Windows"

def linux():
    return platform.system() == "Linux"

def macOS():
    return platform.system() == "Darwin"

def getMayaModulePath():
    print("Checking Maya module path...")
    modPaths = os.environ["MAYA_MODULE_PATH"].split(os.pathsep)
    if windows():
        matches = [mayaVersion, "Common Files"]
    elif linux():
        matches = [mayaVersion, os.environ["HOME"]]
    elif macOS():
        matches = [mayaVersion]
    path = None
    for modPath in modPaths:
        if all(match in modPath for match in matches):
            path = modPath
            break
    if not path:
        emitMsg(modPathErrorMsg)
        return None
    if not os.path.isdir(path):
        os.mkdir(path)
    print("Maya module path: %s" % os.path.abspath(path))
    return os.path.abspath(path)

def checkMod(modPath):
    print("Checking existed installation...")
    filePath = os.path.join(modPath, "gfTools.mod")
    if not os.path.isfile(filePath):
        emitMsg(appNotFounded, icn="warning")
        return False
    return True

def uninstallModFile(modFile):
    # pylint: disable=broad-except
    print("Uninstalling module file...")
    try:
        os.remove(modFile)
    except Exception as err:
        emitMsg(err)
        return False
    return True

def emitMsg(msg, b=["Ok"], db="Ok", icn="critical", **kwargs):
    # pylint: disable=exec-used, dangerous-default-value, unused-argument, invalid-name
    cmd = "cmds.confirmDialog(t=dialogTitle, m=msg, b=b, db=db, icn=icn"
    for key, value in kwargs.items():
        cmd += ', %s="%s"' % (key, value)
    cmd += ")"
    exec(cmd)
    print(msg)

def emitUninstallPrompt():
    status = cmds.confirmDialog(t=dialogTitle, m=uninstallMsg, b=["Uninstall", "Cancel"], db="Uninstall",
                                cb="Cancel", ds="Cancel", icn="question")
    if status == "Uninstall":
        return True
    return False

#############################################################################################
# RUN

def onMayaDroppedPythonFile(*args):
    # pylint: disable=unused-argument
    # 1- Prompt Uninstallation
    print("")
    uninstallIt = emitUninstallPrompt()
    if not uninstallIt:
        emitMsg("The uninstallation was canceled.")
        return
    print("Uninstalling gfTools for Autodesk Maya %s." % mayaVersion)
    # 2- Get Maya module path
    modPath = getMayaModulePath()
    if not modPath:
        return
    # 3- Check gfTools installation
    status = checkMod(modPath)
    if not status:
        return
    # 4- Print gfTools information
    print("gfTools version: %s" % gfCore.version())
    print("gfTools directory: %s" % gfCore.installLocation())
    # 5- Find and delete gfTools mod file
    modFile = os.path.join(modPath, "gfTools.mod")
    print("Found gfTools mod file: %s" % modFile)
    status = uninstallModFile(modFile)
    if not status:
        return
    # 6- Prompt to restart Maya
    emitMsg(sucessMsg, icn="information")
