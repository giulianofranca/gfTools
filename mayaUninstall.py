import sys
import os
import platform
import subprocess
import maya.cmds as cmds

kAppPath = os.path.abspath(os.path.dirname(__file__))
kMayaVersion = cmds.about(version=True)

kDialogTitle = "gfTools for Maya Uninstall."
kUninstallMsg = "This will uninstall gfTools plugins for Autodesk Maya. Are you sure you want to uninstall it?"
kCancelMsg = "The uninstallation was canceled."
kWrongVersionMsg = "Wrong Maya version (%s). gfTools can only be installed in Autodesk Maya versions 2017 to 2020. Uninstallation interrupted." % kMayaVersion
kModPathErrorMsg = "Could not find Maya module path. Uninstallation interrupted."
kSystemNotRecMsg = "System (%s) not compatible." % platform.system()
kAppNotInstalledMsg = "gfTools is not properly installed. Uninstallation interrupted."
kSucessMsg1 = "Uninstallation completed! You need to restart Maya to take effects. (Don't worry. We are gonna let you save your file before restart)"
kSucessMsg2 = "Uninstallation completed!\n\nYou need to restart Maya to take effects.\n(Don't worry. We are gonna let you save your file before restart)"
kRestartCancelMsg = "Restart operation canceled. You need to restart manually."

def windows():
    return platform.system() == "Windows"

def linux():
    return platform.system() == "Linux"

def macOS():
    return platform.system() == "Darwin"

def onMayaDroppedPythonFile(obj):
    if windows():
        uninstallWindows()
    elif linux():
        uninstallLinux()
    elif macOS():
        uninstallOSX()
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

def checkMod(modPath):
    filePath = os.path.join(modPath, "gfTools.mod")
    return os.path.isfile(filePath)

def uninstallModFile(modFile):
    sys.stdout.write("Uninstalling module file...\n")
    try:
        os.remove(modFile)
    except Exception as err:
        emitUninstallModErrorMsg(err)
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

def emitUninstallMsg():
    status = cmds.confirmDialog(t=kDialogTitle, m=kUninstallMsg, b=["Uninstall", "Cancel"], db="Uninstall", 
        cb="Cancel", ds="Cancel", icn="question")
    if status == "Uninstall":
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

def emitAppNotInstalledMsg():
    cmds.confirmDialog(t=kDialogTitle, m=kAppNotInstalledMsg, b=["Ok"], db="Ok", ds="Ok", icn="warning")
    sys.stdout.write("%s\n" % kAppNotInstalledMsg)

def emitUninstallModErrorMsg(msg):
    msg = "%s. Uninstallation interrupted." % msg
    cmds.confirmDialog(t=kDialogTitle, m=msg, b=["Ok"], db="Ok", ds="Ok", icn="critical")
    sys.stdout.write("%s\n" % msg)

def emitUninstallCompleteMsg():
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



def uninstallWindows():
    # 0- Prompt uninstallation.
    uninstallIt = emitUninstallMsg()
    if not uninstallIt:
        emitCancelMsg()
        return
    sys.stdout.write("\nUninstalling gfTools for Autodesk Maya %s.\n" % kMayaVersion)
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
    # 3- Check gfTools installation.
    status = checkMod(modPath)
    if not status:
        emitAppNotInstalledMsg()
        return
    modFile = os.path.abspath(os.path.join(modPath, "gfTools.mod"))
    sys.stdout.write("Found gfTools mod file: %s\n" % modFile)
    # 4- Find and delete gfTools mod file.
    uninstallModFile(modFile)
    # 5- Prompt to restart Maya.
    status = emitUninstallCompleteMsg()
    if status:
        status = saveScene()
        if status:
            restartMaya()
    else:
        emitCancelRestartMsg()

def uninstallOSX():
    # 0- Prompt uninstallation.
    uninstallIt = emitUninstallMsg()
    if not uninstallIt:
        emitCancelMsg()
        return
    sys.stdout.write("\nUninstalling gfTools for Autodesk Maya %s.\n" % kMayaVersion)
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
    # 3- Check gfTools installation.
    status = checkMod(modPath)
    if not status:
        emitAppNotInstalledMsg()
        return
    modFile = os.path.abspath(os.path.join(modPath, "gfTools.mod"))
    sys.stdout.write("Found gfTools mod file: %s\n" % modFile)
    # 4- Find and delete gfTools mod file.
    uninstallModFile(modFile)
    # 5- Prompt to restart Maya.
    status = emitUninstallCompleteMsg()
    if status:
        status = saveScene()
        if status:
            restartMaya()
    else:
        emitCancelRestartMsg()

def uninstallLinux():
    # 0- Prompt uninstallation.
    uninstallIt = emitUninstallMsg()
    if not uninstallIt:
        emitCancelMsg()
        return
    sys.stdout.write("\nUninstalling gfTools for Autodesk Maya %s.\n" % kMayaVersion)
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
    # 3- Check gfTools installation.
    status = checkMod(modPath)
    if not status:
        emitAppNotInstalledMsg()
        return
    modFile = os.path.abspath(os.path.join(modPath, "gfTools.mod"))
    sys.stdout.write("Found gfTools mod file: %s\n" % modFile)
    # 4- Find and delete gfTools mod file.
    uninstallModFile(modFile)
    # 5- Prompt to restart Maya.
    status = emitUninstallCompleteMsg()
    if status:
        status = saveScene()
        if status:
            restartMaya()
    else:
        emitCancelRestartMsg()
