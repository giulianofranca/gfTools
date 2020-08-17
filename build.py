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
    * Run this script using either Python2.x or Python3.x

Requirements:
    * Maya 2018 or above.
    * Qt 5.6.1 and 5.12.5

This code supports Pylint. Rc file in project.
"""
from distutils.spawn import find_executable
import sys
import os
import shutil
import shlex
import time
import argparse
import platform
import subprocess
import zipfile
# pylint: disable=import-error, fixme, missing-function-docstring
if sys.version_info.major >= 3:
    import pickle
else:
    import cPickle as pickle
# TODO: Add flag --qt-location
# TODO: Create gfTools.py standalone script to retrieve gfTools information
# TODO: Remove "tools/maya" from module PYTHONPATH and create gfTools.py to launch tools
# TODO: Finish Tools area of the build.py

defaultPath = os.path.abspath(os.path.dirname(__file__))
mayaToolsList = ["gfUtilitiesBelt"]
mayaVersions = [2018, 2019, 2020]
_project = "gfTools"
_version = "1.0.26 alpha"

def windows():
    return platform.system() == "Windows"

def linux():
    return platform.system() == "Linux"

def macOS():
    return platform.system() == "Darwin"

def printLine():
    print("")

def printMessage(msg):
    print("\t%s" % msg)

def printCommand(cmd, log=None):
    if log:
        log.write(cmd)
    if args.verbosity >= 2:
        sys.stdout.write(cmd)

def findCMake():
    result = find_executable("cmake")
    if result is None:
        raise RuntimeError("Couldn't find CMake in your system. Please check if it is installed.")

def findVisualStudioVersion():
    msvcCompiler = find_executable("cl")
    if msvcCompiler:
        return float(os.environ["VisualStudioVersion"])
    return None

def findGenerator(buildArgs):
    generator = buildArgs.generator
    if generator is None and windows():
        msvcVersion = findVisualStudioVersion()
        if msvcVersion is None:
            raise RuntimeError("Could not find MSVC installed.")
        if msvcVersion >= 16.0:
            generator = "Visual Studio 16 2019"
        elif msvcVersion >= 15.0:
            generator = "Visual Studio 15 2017 Win64"
        else:
            generator = "Visual Studio 14 2015 Win64"
    elif generator is None and linux():
        generator = "Unix Makefiles"
    elif generator is None and macOS():
        generator = "XCode"
    printMessage("Using generator: %s" % generator)
    buildArgs.generator = generator

def findConfig(buildArgs):
    config = "Release"
    if buildArgs.debugMode:
        config = "Debug"
    printMessage("Build config: %s" % config)

def printProcessList(buildArgs):
    printMessage("Processes list:")
    printMessage("- Build Plug-ins for Autodesk Maya:")
    if buildArgs.mayaVersions is None:
        mVers = mayaVersions
    else:
        mVers = buildArgs.mayaVersions
    for ver in mVers:
        printMessage("\t- Maya %s Plug-ins" % ver)
    printMessage("- Build and copy tools for Autodesk Maya:")
    for tool in mayaToolsList:
        printMessage("\t- %s" % tool)
    printMessage("- Copy Autodesk Maya scripts")
    printMessage("- Generate config files")
    printMessage("- Copy resources files")
    if buildArgs.packaging:
        printMessage("- Package %s for distribution" % _project)

def run(command):
    # pylint: disable=redefined-outer-name
    with open(logFilePath, "a+") as logFile:
        printCommand("Running command: %s\n" % command, logFile)
        cmdargs = shlex.split(command)
        encoding = sys.stdout.encoding or "UTF-8"
        process = subprocess.Popen(cmdargs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            out = process.stdout.readline()
            outLine = out.decode(encoding)
            if outLine:
                printCommand("%s" % outLine, logFile)
            elif process.poll() is not None:
                break
    if process.returncode != 0:
        if args.verbosity < 2:
            with open(logFilePath, "r") as logFile:
                content = logFile.read().split("Running command: ")
                print(content[-1])
        raise RuntimeError("See log %s" % logFilePath)
    return process

def runCMake(configArgs, src, buildFolder, buildArgs):
    command = []
    command.append("cmake")
    command.append("-S %s" % src)
    command.append("-B %s" % buildFolder)
    command.append('-G "%s"' % configArgs.generator)
    command.append("-DCMAKE_INSTALL_PREFIX=%s" % configArgs.installLocation)
    command.extend(buildArgs)
    run(" ".join(command))

    config = "Debug" if configArgs.debugMode else "Release"
    command = ("cmake --build {build} --config {config} --target install"
               .format(build=buildFolder, config=config))
    run(command)

def runCMakeMaya(configArgs, src, ver):
    buildFolderName = "-".join(src.split(os.path.sep)[1::])
    buildFolder = "./build/%s%s" %(buildFolderName, ver)
    buildArgs = []
    buildArgs.append("-DMAYA_VERSION=%s" % str(ver))
    runCMake(configArgs, src, buildFolder, buildArgs)

def createDir(dirPath):
    pathSplit = dirPath.split(os.path.sep)
    for split in range(len(pathSplit)):
        path = os.path.abspath(os.path.sep.join(pathSplit[:split+1]))
        if not os.path.isdir(path):
            os.mkdir(path)

def copyFiles(rootDir, destDir, extensions=None, ignore=None):
    # pylint: disable=redefined-outer-name
    with open(logFilePath, "a+") as logFile:
        toCopy = []
        for rootWalk, _, filenames in os.walk(rootDir):
            for filename in filenames:
                ignoreStatus = False
                if ignore is not None:
                    for ignoreVal in ignore:
                        if ignoreVal == filename:
                            ignoreStatus = True
                            break
                if ignoreStatus:
                    continue
                if extensions is not None:
                    for extn in extensions:
                        if filename.upper().endswith(extn.upper()):
                            path = os.path.join(rootWalk, filename).replace(rootDir, "")[1::]
                            toCopy.append(path)
                else:
                    path = os.path.join(rootWalk, filename).replace(rootDir, "")[1::]
                    toCopy.append(path)
        for fc in toCopy:
            fileSplit = fc.split(os.path.sep)
            if len(fileSplit) > 1:
                for pathSplit in fileSplit:
                    srcPath = os.path.join(rootDir, pathSplit)
                    destPath = os.path.join(destDir, pathSplit)
                    if os.path.isdir(srcPath) and not os.path.isdir(destPath):
                        os.mkdir(destPath)
            srcPath = os.path.join(rootDir, fc)
            destPath = os.path.join(destDir, fc)
            shutil.copy(srcPath, destPath)
            printCommand("Copied file: %s >> %s\n" % (srcPath, destPath), logFile)


#############################################################################################
# BUILD TOOLKIT

description = """
Build script for gfTools

Build all the C++ files in the plugin and export a single folder containing all
the dependencies necessary to run gfTools based on your OS.
"""
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=description
)
parser.add_argument("installLocation", type=str, metavar="install-location",
                    help="Select the local of the installation.")
parser.add_argument("-mv", "--maya-versions", type=int, nargs="+", choices=mayaVersions, dest="mayaVersions",
                    help="Select which Maya versions will be compiled for. If doesn't specified it will compile for all versions.")
parser.add_argument("-g", "--generator", type=str,
                    help="CMake generator to use with libraries build.")
parser.add_argument("-v", "--verbose", action="count", default=1, dest="verbosity",
                    help="Increase verbosity level (1-2)")
parser.add_argument("--debug-mode", action="store_true", dest="debugMode",
                    help="Build in debug mode.")
parser.add_argument("--packaging", action="store_true",
                    help="Package the tool for distribution after compiling.")
parser.add_argument("--version", action="version", version="%s Builder %s" % (_project, _version),
                    help="Show %s version." % _project)

startTime = time.time()
args = parser.parse_args()
logFilePath = os.path.join(defaultPath, "build", "log.txt")
createDir(os.path.dirname(logFilePath))
timePat = "%M mins and %S secs"


#------------------------ INITIAL -------------------------
with open(logFilePath, "a+") as logFile:
    printLine()
    printMessage("Start %s configuration process.\n" % _project)
    printMessage("%s version: %s" % (_project, _version))
    findCMake()
    findGenerator(args)
    findConfig(args)
    printProcessList(args)
    outputName = "%s" % (_project)
    os.chdir(defaultPath)
    if not os.path.isdir(os.path.join(defaultPath, "build")):
        os.mkdir("build")
    if not os.path.isdir(args.installLocation):
        os.mkdir(args.installLocation)
    printLine()

#------------------------ PLUG-INS ------------------------
    # Maya
    mPluginsBTime = []
    if args.mayaVersions is None:
        mVersions = mayaVersions
    else:
        mVersions = args.mayaVersions
    for v in mVersions:
        startCompTime = time.time()
        printMessage("Building plug-ins for Autodesk Maya %s..." % v)
        runCMakeMaya(args, "./plugin/maya", v)
        printCommand("\tBuild for Autodesk Maya %s complete!\n" % v, logFile)
        runTime = time.time() - startCompTime
        runTimeStr = time.strftime(timePat, time.gmtime(runTime))
        printCommand("\tTime elapsed: %s mins\n" % runTime, logFile)
        mPluginsBTime.append(runTime)
    mPluginsBTime = time.strftime(timePat, time.gmtime(sum(mPluginsBTime)))

#-------------------------- TOOLS --------------------------
    startToolsTime = time.time()
    toolsFolder = os.path.join(defaultPath, "tools")
    # Maya
    mayaToolsFolder = os.path.join(toolsFolder, "maya")
    # dest = args.installLocation
    # Build
    # printMessage("Building tools for Autodesk Maya...")
    # Copy
    # printMessage("Copying tools for Autodesk Maya...")
    # copy_tree(src, dst)
    toolsCBTime = time.strftime(timePat, time.gmtime(time.time() - startToolsTime))

#------------------------- SCRIPTS -------------------------
    scriptsFolder = os.path.join(defaultPath, "scripts")
    # Maya
    printMessage("Copying Autodesk Maya scripts...")
    mayaFolder = os.path.join(scriptsFolder, "maya")
    dest = os.path.join(args.installLocation, "scripts", "maya")
    ext = [".py", ".mel"]
    ign = None
    createDir(dest)
    copyFiles(mayaFolder, dest, ext, ign)

#---------------------- CONFIG FILES -----------------------
    printMessage("Generating config files...")
    coreFolder = os.path.join(args.installLocation, "core")
    createDir(coreFolder)
    # Generate info file
    infoDict = dict()
    infoDict["Application"] = _project
    infoDict["Current Version"] = _version
    infoDict["Platform"] = platform.system()
    infoDict["Maya Versions Compatible"] = mVersions
    infoFileName = "app"
    infoFile = os.path.join(coreFolder, infoFileName)
    with open(infoFile, "wb") as f:
        pickle.dump(infoDict, f, pickle.HIGHEST_PROTOCOL)
    # TODO: Copy scripts in core folder
    # Copy license and how to
    files = [os.path.join(defaultPath, "LICENSE")]
    files.append(os.path.join(defaultPath, "install_instructions.txt"))
    files.append(os.path.join(defaultPath, "uninstall_instructions.txt"))
    for f in files:
        shutil.copy(f, args.installLocation)

#----------------------- RESOURCES -------------------------
    printMessage("Copying resources files...")
    startResTime = time.time()
    resourcesFolder = os.path.join(coreFolder, "resources")
    # Fonts
    fontsZip = os.path.join(defaultPath, "core", "resources", "fonts", "design.zip")
    dest = os.path.join(resourcesFolder, "fonts")
    createDir(dest)
    with zipfile.ZipFile(fontsZip, "r") as zipf:
        zipf.extractall(dest)
    printCommand("Fonts extracted: %s\n" % dest, logFile)
    # Icons
    iconsZip = os.path.join(defaultPath, "core", "resources", "icons", "design.zip")
    dest = os.path.join(resourcesFolder, "icons")
    createDir(dest)
    with zipfile.ZipFile(iconsZip, "r") as zipf:
        zipf.extractall(dest)
    printCommand("Icons extracted: %s\n" % dest, logFile)
    # Widgets
    widgetsFolder = os.path.join(defaultPath, "core", "resources", "widgets", "python")
    dest = os.path.join(resourcesFolder, "widgets", "python")
    ext = None
    ign = None
    createDir(dest)
    copyFiles(widgetsFolder, dest, ext, ign)
    # QRC
    qrcFile = os.path.join(defaultPath, "core", "resources", "gfResources.qrc")
    shutil.copy(qrcFile, resourcesFolder)
    printCommand("Qrc file copied: %s\n" % resourcesFolder, logFile)
    resourcesCTime = time.strftime(timePat, time.gmtime(time.time() - startResTime))

#------------------------ PACKAGING ------------------------
    if args.packaging:
        startPackageTime = time.time()
        installDir = os.path.abspath(os.path.join(args.installLocation, os.pardir))
        os.chdir(installDir)
        printMessage("Packaging %s..." % _project)
        packageName = "%s-%s-%s%s" % (_project, _version.replace(".", "-"), platform.system(), ".zip")
        pardir = os.path.abspath(os.path.join(args.installLocation, os.pardir))
        packagePath = os.path.join(args.installLocation, packageName)
        with zipfile.ZipFile(packagePath, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(args.installLocation):
                for f in files:
                    if f == packageName:
                        continue
                    toPackage = os.path.join(root, f).replace(installDir, "")[1::]
                    zipf.write(toPackage)
                    printCommand("Added to package: %s\n" % toPackage, logFile)
        packageTime = time.strftime(timePat, time.gmtime(time.time() - startPackageTime))

#------------------------ FINISHING ------------------------
    printLine()
    printMessage("%s" % ("-" * 80))
    printMessage("The build process is done!")
    printMessage("Plug-ins build for Autodesk Maya: %s[Done] | %s." % (" " * 11, mPluginsBTime))
    # printMessage("Build and copy tools for Autodesk Maya: %s[Done] | %s." %(" " * 5, toolsCBTime))
    printMessage("%s resources copy: %s[Done] | %s." % (_project, " " * 21, resourcesCTime))
    if args.packaging:
        printMessage("gfTools package: %s[Done] | %s." % (" " * 28, packageTime))

    printLine()
    printMessage("%s was installed in: %s" % (_project, args.installLocation))
    runTime = time.strftime(timePat, time.gmtime(time.time() - startTime))
    printMessage("Total time elapsed: %s." % runTime)
