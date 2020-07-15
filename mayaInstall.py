import sys
import os
import json
import platform
import shutil
import subprocess
import maya.cmds as cmds

kAppPath = os.path.abspath(os.path.dirname(__file__))
kMayaVersion = cmds.about(version=True)

kDialogTitle = "gfTools for Maya Install."
kInstallMsg = "This will install gfTools plugins for Autodesk Maya. Are you sure you want to install it?"
kCancelMsg = "The installation was canceled."
kWrongVersionMsg = "Wrong Maya version (%s). gfTools can only be installed in Autodesk Maya versions 2017 to 2020. Installation interrupted." % kMayaVersion
kModPathErrorMsg = "Could not find Maya module path. Installation interrupted."
kSystemNotRecMsg = "System (%s) not compatible." % platform.system()
kCouldNotInfoMsg = "Could not get application info. Installation interrupted."
kWrongPlatformMsg = "Wrong gfTools platform. (%s)" % platform.system()
kAppInstalledMsg = "gfTools is already installed. Installation interrupted."
kSucessMsg1 = "Installation completed! You need to restart Maya to take effects. (Don't worry. We are gonna let you save your file before restart)"
kSucessMsg2 = "Installation completed!\n\nYou need to restart Maya to take effects.\n(Don't worry. We are gonna let you save your file before restart)"
kRestartCancelMsg = "Restart operation canceled. You need to restart manually."

def windows():
    return platform.system() == "Windows"

def linux():
    return platform.system() == "Linux"

def macOS():
    return platform.system() == "Darwin"

def onMayaDroppedPythonFile(obj):
    if windows():
        installWindows()
    elif linux():
        installLinux()
    elif macOS():
        installOSX()
    else:
        emitSystemNotCompatibleMsg()
        return
    return True



def getMayaVersion():
    sys.stdout.write("Checking Maya version...\n")
    version = int(cmds.about(version=True))
    if version < 2017:
        status = emitMayaVersionErrorMsg()
        return status
    return True

def getMayaModulePath():
    sys.stdout.write("Checking Maya module path...\n")
    matches = [kMayaVersion, "Common Files"]
    if windows():
        paths = os.environ["MAYA_MODULE_PATH"].split(";")
    else:
        paths = os.environ["MAYA_MODULE_PATH"].split(":")
    path = None
    for modPath in paths:
        if all(match in modPath for match in matches):
            path = modPath
            break
    if not path:
        emitModPathErrorMsg()
        return False
    return os.path.abspath(path)

def getAppInfo():
    infoFilePath = os.path.abspath(os.path.join(kAppPath, "core", "__info"))
    if not os.path.isfile(infoFilePath):
        emitAppInfoErrorMsg()
        return False
    with open(infoFilePath, "r") as f:
        try:
            info = json.load(f)
        except Exception as err:
            emitAppInfoErrorMsg(err)
            return False
    try:
        if not info["Application"]:
            emitAppInfoErrorMsg()
            return False
        if not info["Current Version"]:
            emitAppInfoErrorMsg()
            return False
        if not info["Platform"]:
            emitAppInfoErrorMsg()
            return False
    except Exception as err:
        emitAppInfoErrorMsg(err)
        return False
    if info["Platform"] != platform.system():
        emitWrongPlatformErrorMsg()
        return False
    return info

def checkMod(modPath):
    filePath = os.path.join(modPath, "gfTools.mod")
    return os.path.isfile(filePath)

def generateMod(info):
    sys.stdout.write("Generating module file...\n")
    fileName = os.path.join(kAppPath, "gfTools.mod")
    lines = []
    if windows():
        appLine = "+ PLATFORM:win64 MAYAVERSION:%s %s %s %s\n" % (kMayaVersion, info["Application"], info["Current Version"], info["Path"])
    elif linux():
        appLine = "+ PLATFORM:linux MAYAVERSION:%s %s %s %s\n" % (kMayaVersion, info["Application"], info["Current Version"], info["Path"])
    else:
        appLine = "+ PLATFORM:mac MAYAVERSION:%s %s %s %s\n" % (kMayaVersion, info["Application"], info["Current Version"], info["Path"])
    lines.append(appLine)
    lines.append("PYTHONPATH +:= core/widgets/python")
    lines.append("PYTHONPATH +:= tools/maya\n")
    lines.append("MAYA_SCRIPT_PATH +:= plug-ins/maya/AETemplates\n")
    lines.append("MAYA_SCRIPT_PATH +:= tools/maya\n")
    lines.append("MAYA_PLUG_IN_PATH +:= plugin/maya/release/%s\n" % kMayaVersion)
    lines.append("MAYA_SHELF_PATH +:= core/utils/shelf\n")
    lines.append("XBMLANGPATH +:= core/utils/icons\n")
    with open(fileName, "w") as f:
        f.writelines(lines)
    return fileName

def installModFile(modFile, mayaModPath):
    sys.stdout.write("Installing module file...\n")
    try:
        shutil.copy(modFile, mayaModPath)
    except Exception as err:
        emitInstallModErrorMsg(err)
        return False
    return True

def saveScene():
    curScene = cmds.file(q=True, sn=True)
    if curScene == "":
        curScene = "untitled"
    status = emitSaveSceneMsg(curScene)
    if not status:
        emitCancelRestartMsg()
        return False
    if status == "Save As...":
        cmds.SaveSceneAs()
    return True

def restartMaya():
    def restart():
        mayaDir = os.path.abspath(os.path.join(os.environ["MAYA_LOCATION"], "bin"))
        if windows():
            mayaExec = os.path.abspath(os.path.join(mayaDir, "maya.exe"))
        elif linux():
            mayaExec = os.path.abspath(os.path.join(mayaDir, "maya.bin"))
        curScene = cmds.file(q=True, sn=True)
        command = 'confirmDialog -t "%s" -m "gfTools uninstalled successfully!" -b "Ok" -icn "information";' % kDialogTitle
        if windows():
            if curScene != "":
                subprocess.Popen([mayaExec, "-file", curScene, "-command", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                subprocess.Popen([mayaExec, "-command", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            if curScene != "":
                subprocess.Popen([mayaExec, "-batch", "-file", curScene, "-command", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                subprocess.Popen([mayaExec, "-batch", "-command", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmds.scriptJob = cmds.scriptJob(event=["quitApplication", restart], ro=True)
    cmds.quit(f=True)

def emitSystemNotCompatibleMsg():
    cmds.confirmDialog(t=kDialogTitle, m=kSystemNotRecMsg, b=["Ok"], db="Ok", ds="Ok", icn="critical")
    sys.stdout.write("%s\n" % kSystemNotRecMsg)

def emitInstallMsg():
    status = cmds.confirmDialog(t=kDialogTitle, m=kInstallMsg, b=["Install", "Cancel"], db="Install", 
        cb="Cancel", ds="Cancel", icn="question")
    if status == "Install":
        return True
    else:
        return False

def emitCancelMsg():
    cmds.confirmDialog(t=kDialogTitle, m=kCancelMsg, b=["Ok"], db="Ok", ds="Ok", icn="warning")
    sys.stdout.write("gfTools installation canceled.\n")

def emitMayaVersionErrorMsg():
    cmds.confirmDialog(t=kDialogTitle, m=kWrongVersionMsg, b=["Ok"], db="Ok", ds="Ok", icn="critical")
    sys.stdout.write("%s\n" % kWrongVersionMsg)
    return False

def emitModPathErrorMsg():
    cmds.confirmDialog(t=kDialogTitle, m=kModPathErrorMsg, b=["Ok"], db="Ok", ds="Ok", icn="critical")
    sys.stdout.write("%s\n" % kModPathErrorMsg)
    return False

def emitAppInfoErrorMsg(err):
    msg = kCouldNotInfoMsg
    if err:
        msg = "%s\n[Exception] %s" % (kCouldNotInfoMsg, err)
    cmds.confirmDialog(t=kDialogTitle, m=msg, b=["Ok"], db="Ok", ds="Ok", icn="critical")
    sys.stdout.write("%s\n" % msg)

def emitInstallModErrorMsg(msg):
    msg = "%s. Installation interrupted." % msg
    cmds.confirmDialog(t=kDialogTitle, m=msg, b=["Ok"], db="Ok", ds="Ok", icn="critical")
    sys.stdout.write("%s\n" % msg)

def emitWrongPlatformErrorMsg():
    cmds.confirmDialog(t=kDialogTitle, m=kWrongPlatformMsg, b=["Ok"], db="Ok", ds="Ok", icn="critical")
    sys.stdout.write("%s\n" % kWrongPlatformMsg)

def emitAppInstalledMsg():
    cmds.confirmDialog(t=kDialogTitle, m=kAppInstalledMsg, b=["Ok"], db="Ok", ds="Ok", icn="warning")
    sys.stdout.write("%s\n" % kAppInstalledMsg)

def emitInstallCompleteMsg():
    sys.stdout.write("%s\n" % kSucessMsg1)
    status = cmds.confirmDialog(t=kDialogTitle, m=kSucessMsg2, b=["Restart", "I'll do it later"], db="Restart",
        cb="I'll do it later", ds="I'll do it later", icn="information")
    if status == "Restart":
        return True
    else:
        return False

def emitSaveSceneMsg(scene):
    msg = "Save changes to %s?" % scene
    sys.stdout.write("%s\n" % msg)
    status = cmds.confirmDialog(t=kDialogTitle, m=msg, b=["Save As...", "Don't Save", "Cancel"], db="Save As...",
        cb="Don't Save", ds="Cancel", icn="question")
    if status == "Cancel":
        return False
    return status

def emitCancelRestartMsg():
    cmds.confirmDialog(t=kDialogTitle, m=kRestartCancelMsg, b=["Ok"], db="Ok", ds="Ok", icn="information")
    sys.stdout.write("%s\n" % kRestartCancelMsg)



def installWindows():
    # 0- Prompt installation.
    installIt = emitInstallMsg()
    if not installIt:
        emitCancelMsg()
        return
    sys.stdout.write("\nInstalling gfTools for Autodesk Maya %s.\n" % kMayaVersion)
    sys.stdout.write("Current platform: Windows %s\n" % platform.release())
    # 1- Get current Maya version.
    status = getMayaVersion()
    if not status:
        return
    # 2- Get Maya module path.
    modPath = getMayaModulePath()
    if not modPath:
        return
    sys.stdout.write("Maya module path: %s\n" % modPath)
    # 3- Get gfTools information (directory, appName, version).
    appInfo = getAppInfo()
    if not appInfo:
        return
    appInfo["Path"] = kAppPath
    sys.stdout.write("gfTools version: %s\n" % appInfo["Current Version"])
    sys.stdout.write("gfTools directory path: %s\n" % kAppPath)
    # 4- Generate the mod file.
    status = checkMod(modPath)
    if status:
        emitAppInstalledMsg()
        return
    modFile = generateMod(appInfo)
    # 5- Copy the generated mod file to Maya mod path, if it doesn't exists.
    status = installModFile(modFile, modPath)
    if not status:
        return
    # 6- Delete leftover file.
    sys.stdout.write("Cleaning leftover files...\n")
    os.remove(modFile)
    # 7- Prompt to restart Maya.
    status = emitInstallCompleteMsg()
    if status:
        status = saveScene()
        if status:
            restartMaya()
    else:
        emitCancelRestartMsg()

def installOSX():
    # 0- Prompt installation.
    installIt = emitInstallMsg()
    if not installIt:
        emitCancelMsg()
        return
    sys.stdout.write("\nInstalling gfTools for Autodesk Maya %s.\n" % kMayaVersion)
    sys.stdout.write("Current platform: MacOS %s\n" % platform.mac_ver())
    # 1- Get current Maya version.
    status = getMayaVersion()
    if not status:
        return
    # 2- Get Maya module path.
    modPath = getMayaModulePath()
    if not modPath:
        return
    sys.stdout.write("Maya module path: %s\n" % modPath)
    # 3- Get gfTools information (directory, appName, version).
    sys.stdout.write("gfTools directory path: %s\n" % kAppPath)
    # 4- Generate the mod file.
    # 5- Copy the generated mod file to Maya mod path, if it doesn't exists.
    # 6- Restart Maya?

def installLinux():
    # 0- Prompt installation.
    installIt = emitInstallMsg()
    if not installIt:
        emitCancelMsg()
        return
    sys.stdout.write("\nInstalling gfTools for Autodesk Maya %s.\n" % kMayaVersion)
    sys.stdout.write("Current platform: Linux %s\n" % (" ".join(platform.dist()[:2]).title()))
    # 1- Get current Maya version.
    status = getMayaVersion()
    if not status:
        return
    # 2- Get Maya module path.
    modPath = getMayaModulePath()
    if not modPath:
        return
    sys.stdout.write("Maya module path: %s\n" % modPath)
    # 3- Get gfTools information (directory, appName, version).
    sys.stdout.write("gfTools directory path: %s\n" % kAppPath)
    # 4- Generate the mod file.
    # 5- Copy the generated mod file to Maya mod path, if it doesn't exists.
    # 6- Restart Maya?
