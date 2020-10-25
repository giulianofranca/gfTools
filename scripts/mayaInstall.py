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
import shutil

# Check if this script is using mayapy.
try:
    import maya.cmds as cmds
except ImportError:
    raise RuntimeError("Could not find Maya. You should use this script inside Maya, just drag it into the viewport.")

mayaVersion = cmds.about(version=True)

gfToolsPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
libPath = os.path.join(gfToolsPath, "lib", "maya", str(mayaVersion), "python")
if not libPath in sys.path:
    sys.path.append(libPath)

# Import gfCore module to get information needed to install gfTools Maya plugins. gfCore is platform independant.
try:
    from gfTools import gfCore
except ImportError:
    raise RuntimeError("Could not find gfCore module.")


compatibleVersions = gfCore.mayaVersionsCompatible()

wrongPlatform = ("This gfTools build is only compatible with (%s) systems. You can get a compatible version at github.com/giuliano-franca/gfTools/releases"
                 % platform.system())
dialogTitle = "gfTools for Maya Installation"
installMsg = "This will install gfTools plugins for Autodesk Maya. Are you sure you want to install it?"
wrongVersionMsg = ("Maya version not compatible (%s). gfTools can only be installed in Autodesk Maya versions %s to %s. Installation interrupted."
                   % (mayaVersion, compatibleVersions[0], compatibleVersions[-1]))
modPathErrorMsg = "Could not find Maya module path. Installation interrupted."
alreadyInstalledMsg = "gfTools is already installed. Installation interrupted."
sucessMsg = "Installation completed! You need to restart Maya to take effects."


def windows():
    return gfCore.platform() == "Windows"

def linux():
    return gfCore.platform() == "Linux"

def macOS():
    return gfCore.platform() == "Darwin"

def checkPlatform():
    print("Checking platform...")
    if platform.system() != gfCore.platform():
        emitMsg(wrongPlatform)
        return False
    return True

def checkMayaVersion():
    print("Checking Maya version...")
    if mayaVersion not in compatibleVersions:
        emitMsg(wrongVersionMsg)
        return False
    return True

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
    if os.path.isfile(filePath):
        emitMsg(alreadyInstalledMsg, icn="warning")
        return False
    return True

def generateModFile():
    print("Generating module file...")
    fileName = os.path.join(gfToolsPath, "gfTools.mod")
    if windows():
        plat = "win64"
    elif linux():
        plat = "linux"
    elif macOS():
        plat = "mac"
    lines = ["+ PLATFORM:%s MAYAVERSION:%s gfTools %s %s\n" % (plat, mayaVersion, gfCore.version(), gfCore.installLocation())]
    # TODO: Review this to work with build options (e.g.: only-libs)
    # TODO: Maybe remove the PLATFORM tag
    lines.append("PYTHONPATH +:= lib/maya/%s/python\n" % mayaVersion)
    lines.append("PYTHONPATH +:= core/resources/widgets/python\n")
    lines.append("PYTHONPATH +:= scripts/maya\n")
    lines.append("PYTHONPATH +:= tools/maya\n")
    lines.append("MAYA_SCRIPT_PATH +:= scripts/maya\n")
    lines.append("MAYA_SCRIPT_PATH +:= scripts/maya/AETemplates\n")
    lines.append("MAYA_PLUG_IN_PATH +:= plugin/maya/%s\n" % mayaVersion)
    lines.append("XBMLANGPATH +:= core/resources/icons%s\n" % ("/%B" if linux() else ""))
    with open(fileName, "w") as f:
        f.writelines(lines)
    return fileName

def installModFile(modFile, mayaModPath):
    # pylint: disable=broad-except
    print("Installing module file...")
    try:
        shutil.copy(modFile, mayaModPath)
    except Exception as err:
        print(err)
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

def emitInstallPrompt():
    status = cmds.confirmDialog(t=dialogTitle, m=installMsg, b=["Install", "Cancel"], db="Install",
                                cb="Cancel", ds="Cancel", icn="question")
    if status == "Install":
        return True
    return False

#############################################################################################
# RUN

def onMayaDroppedPythonFile(*args):
    # pylint: disable=unused-argument
    # 1- Prompt installation
    print("")
    installIt = emitInstallPrompt()
    if not installIt:
        emitMsg("The installation was canceled.")
        return
    print("Installing gfTools for Autodesk Maya %s." % mayaVersion)
    # 2- Verify platform compatibility
    status = checkPlatform()
    if not status:
        return
    # 3- Verify Maya version compatibility
    status = checkMayaVersion()
    if not status:
        return
    # 4- Get Maya module path
    modPath = getMayaModulePath()
    if not modPath:
        return
    # 5- Print gfTools information
    print("gfTools version: %s" % gfCore.version())
    print("gfTools directory: %s" % gfCore.installLocation())
    # 6- Generate the mod file
    status = checkMod(modPath)
    if not status:
        return
    modFile = generateModFile()
    # 7- Copy the generated mod file to Maya mod path
    status = installModFile(modFile, modPath)
    if not status:
        os.remove(modFile)
        return
    # 8- Delete leftover file
    print("Cleaning leftover files...")
    os.remove(modFile)
    # 9- Prompt to restart Maya
    emitMsg(sucessMsg, icn="information")
