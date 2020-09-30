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

This code supports Pylint. Rc file in project.
"""
# pylint: disable=import-error, fixme, missing-function-docstring
from distutils.spawn import find_executable
import sys
import os
import platform
import time
import argparse
import shlex
import shutil
import subprocess
import zipfile


sourcePath = os.path.abspath(os.path.dirname(__file__))
_project = "gfTools"
mToolsList = ["gfUtilitiesBelt"]
mVersionsCompatible = [2018, 2019, 2020]

def windows():
    return platform.system() == "Windows"

def linux():
    return platform.system() == "Linux"

def macOS():
    return platform.system() == "Darwin"

def printLine(level=1):
    if level >= 1:
        print("")

def printError(err, log=None):
    if log:
        log.write("[ERROR] %s\n" % err)
    raise RuntimeError("\n%s\nSee gfTools log: %s" % (err, logFilePath))

def printMessage(msg, log=None):
    if log:
        log.write("\t%s\n" % msg)
    if args.verbosity >= 1:
        print("\t%s" % msg)

def printCommand(cmd, log=None):
    if log:
        log.write(cmd)
    if args.verbosity >= 2:
        sys.stdout.write(cmd)



def findVersion():
    filePath = os.path.join(sourcePath, "cmake", "defaults", "Version.cmake")
    with open(filePath, "r") as versionF:
        content = versionF.readlines()
        for line in content:
            if "GFTOOLS_STR_VERSION" in line:
                content = line[4:-2].replace("GFTOOLS_STR_VERSION ", "")
                break
    return content.replace('"', '')

def findCMake():
    result = find_executable("cmake")
    if result is None:
        raise RuntimeError("Couldn't find CMake installed in your system. Please check if it is installed.")

def findVisualStudioVersion():
    msvcCompiler = find_executable("cl")
    if msvcCompiler:
        return float(os.environ["VisualStudioVersion"])
    return None

def findGenerator(logF=None):
    generator = args.generator
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
    printMessage("Using generator: %s" % generator, logF)
    args.generator = generator

def findConfig(logF=None):
    cfg = "Release"
    if args.debugMode:
        cfg = "Debug"
    printMessage("Build config: %s" % cfg, logF)
    args.config = cfg

def findPythonVersion(logF=None):
    major = sys.version_info.major
    minor = sys.version_info.minor
    patch = sys.version_info.micro
    pyVersion = "%s.%s.%s" % (major, minor, patch)
    printMessage("Current Python version: %s" % pyVersion, logF)
    return pyVersion

def printProcessesList(logF=None):
    printMessage("Processes list:", logF)
    printMessage("- Build documentation:%s%s" % (" " * 15, "On" if args.buildDocs else "Off"), logF)
    printMessage("- Build libraries:%s%s" % (" " * 19, "On" if args.buildLibs else "Off"), logF)
    printMessage("- Build nodes:%s%s" % (" " * 23, "On" if args.buildNodes else "Off"), logF)
    printMessage("- Build tools:%s%s" % (" " * 23, "On" if args.buildTools else "Off"), logF)
    for t in mToolsList:
        toolStatus = "On" if t in args.toolsList else "Off"
        if not args.buildTools:
            toolStatus = "Off"
        printMessage("\t- %s:%s%s" % (t, " " * 11, toolStatus), logF)
    printMessage("- Use Mayapy:%s%s" % (" " * 24, "On" if args.useMayapy else "Off"), logF)
    printMessage("- Pack toolkit:%s%s" % (" " * 22, "On" if args.packaging else "Off"), logF)

def run(command):
    printCommand("Running command: %s\n" % command, logFile)
    cmdargs = shlex.split(command)
    encoding = sys.stdout.encoding or "UTF-8"
    process = subprocess.Popen(cmdargs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    content = []
    while True:
        out = process.stdout.readline()
        outLine = out.decode(encoding)
        content.append(outLine)
        if outLine:
            printCommand("%s" % outLine, logFile)
        elif process.poll() is not None:
            break
    if process.returncode != 0:
        content = "".join(content)
        printError(content)
    return process

def runCMake(buildDir, buildArgs=None):
    command = []
    command.append("cmake")
    command.append("-S .")
    command.append("-B ./%s" % buildDir)
    command.append("-G \"%s\"" % args.generator)
    command.append("-DCMAKE_INSTALL_PREFIX=%s" % args.installLocation)
    command.append("-DCMAKE_BUILD_TYPE=%s" % args.config)
    if buildArgs:
        command.extend(buildArgs)
    run(" ".join(command))

    command = "cmake --build ./%s --config %s --target install" % (buildDir, args.config)
    run(command)

def createDir(dirPath):
    pathSplit = dirPath.split(os.path.sep)
    for split in range(len(pathSplit)):
        path = os.path.abspath(os.path.sep.join(pathSplit[:split+1]))
        if not os.path.isdir(path):
            os.mkdir(path)

#############################################################################################
# BUILD TOOLKIT

startTime = time.time()
_version = findVersion()

description = """
Build script for gfTools

Build all the C++ files in the plugin and export a single folder containing all
the dependencies necessary to run gfTools based on your OS.
"""
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=description
)

parser.add_argument("installLocation", type=str,
                    help="The directory where gfTools will be installed.")

group = parser.add_argument_group(title="gfTools Options")
group.add_argument("--maya-versions", type=int,
                   default=[mVersionsCompatible[-1]], nargs="+",
                   choices=mVersionsCompatible, dest="mayaVersions",
                   help="""Select which Maya versions that will be compiled for.
                        If doesn't specified any, it will compile for latest version
                        (%s).""" % mVersionsCompatible[-1])
group.add_argument("--use-mayapy", action="store_true", dest="useMayapy",
                   help="""Specify this flag if you want to use the mayapy
                        to build the python bindings. The default is to use
                        a system Python of version 2.7.""")

subgroup = group.add_mutually_exclusive_group()
subgroup.add_argument("--build-docs", dest="buildDocs", action="store_true",
                      default=False, help="Build documentation.")
subgroup.add_argument("--skip-docs", dest="buildDocs", action="store_false",
                      help="Skip building the documentation. (Default)")

subgroup = group.add_mutually_exclusive_group()
subgroup.add_argument("--build-tools", dest="buildTools", action="store_true",
                      default=True,
                      help="Copy all the tools. (Default)")
subgroup.add_argument("--skip-tools", dest="buildTools", action="store_false",
                      help="Do not copy any tool.")
group.add_argument("--tools-list", type=str,
                   default=mToolsList, nargs="+",
                   choices=mToolsList, dest="toolsList",
                   help="""Select which tools to be installed.
                        If doesn't specifed any, it will install all the tools.""")

subgroup = group.add_mutually_exclusive_group()
subgroup.add_argument("--build-nodes", dest="buildNodes", action="store_true",
                      default=True,
                      help="Build the Autodesk Maya nodes plugin. (Default)")
subgroup.add_argument("--skip-nodes", dest="buildNodes", action="store_false",
                      help="Skip the build of the Autodesk Maya nodes plugin.")

subgroup = group.add_mutually_exclusive_group()
subgroup.add_argument("--build-libraries", dest="buildLibs", action="store_true",
                      default=True,
                      help="Build all the libraries. (Default)")
subgroup.add_argument("--skip-libraries", dest="buildLibs", action="store_false",
                      help="Skip the build of all the libraries.")

subgroup = group.add_mutually_exclusive_group()
subgroup.add_argument("--only-tools", dest="onlyTools", action="store_true",
                      default=False,
                      help="Build only the tools.")
subgroup.add_argument("--only-nodes", dest="onlyNodes", action="store_true",
                      default=False,
                      help="Build only the nodes.")
subgroup.add_argument("--only-libs", dest="onlyLibs", action="store_true",
                      default=False,
                      help="Build only the libraries.")

parser.add_argument("--generator", type=str,
                    help="CMake generator to use with libraries build.")
parser.add_argument("--dry-run", dest="dryRun", action="store_true",
                    help="Only show the processes list.")
parser.add_argument("--debug-mode", action="store_true", dest="debugMode",
                    help="Build in debug mode.")
parser.add_argument("--packaging", action="store_true",
                    help="Pack the tool in a zip file for distribution.")
parser.add_argument("--clean-up-after", action="store_true", dest="cleanUp",
                    help="Delete build files after completed.")

group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="count", default=1, dest="verbosity",
                   help="Increase verbosity level (1-2).")
group.add_argument("-q", "--quiet", action="store_const", const=0, dest="verbosity",
                   help="Supress all output except for error messages.")

parser.add_argument("--version", action="version",
                    version="%s %s" % (_project, _version),
                    help="Show %s version." % _project)

args = parser.parse_args()
logFilePath = os.path.join(sourcePath, "build", "log.txt")
if not args.dryRun:
    os.chdir(sourcePath)
    if not os.path.isdir("build"):
        createDir(os.path.dirname(logFilePath))
timePattern = "%M mins and %S secs"

#---------------------- SOLVE FLAGS -----------------------
if args.onlyTools:
    args.buildDocs = False
    args.buildLibs = False
    args.buildNodes = False
    args.buildTools = True
elif args.onlyNodes:
    args.buildDocs = False
    args.buildLibs = False
    args.buildNodes = True
    args.buildTools = False
elif args.onlyLibs:
    args.buildDocs = False
    args.buildLibs = True
    args.buildNodes = False
    args.buildTools = False

#------------------------ INITIAL ------------------------
if args.dryRun:
    args.verbosity = 1
    printLine(args.verbosity)
    printMessage("%s version: %s" % (_project, _version))
    findCMake()
    findGenerator()
    findConfig()
    printMessage("Autodesk Maya versions: %s" % (", ".join([str(v) for v in args.mayaVersions])))
    pyVer = findPythonVersion()
    if pyVer.split(".")[:2] != ["2", "7"]:
        printError("Current Python version (%s) is not compatible. You should use 2.7.x" % pyVer)
    printMessage("Install location: %s" % args.installLocation)
    printProcessesList()
    printLine(args.verbosity)
else:
    with open(logFilePath, "a+") as logFile:
        printLine(args.verbosity)
        printMessage("Starting %s configuration process...\n" % _project, logFile)
        printMessage("%s version: %s" % (_project, _version), logFile)
        findCMake()
        findGenerator(logFile)
        findConfig(logFile)
        printMessage("Autodesk Maya versions: %s" % (", ".join([str(v) for v in args.mayaVersions])), logFile)
        pyVer = findPythonVersion(logFile)
        if pyVer.split(".")[:2] != ["2", "7"]:
            printError("Current Python version (%s) is not compatible. You should use 2.7.x" % pyVer, logFile)
        printMessage("Install location: %s" % args.installLocation, logFile)
        printProcessesList(logFile)
        printLine(args.verbosity)

#----------------------- RUN CMAKE -----------------------
        for mv in args.mayaVersions:
            buildFolder = os.path.join("build", str(mv))
            createDir(buildFolder)
            printMessage("Building gfTools for Autodesk Maya %s..." % str(mv), logFile)
            cmakeArgs = []
            cmakeArgs.append("-DMAYA_VERSION=%s" % str(mv))
            if args.useMayapy:
                cmakeArgs.append("-DUSE_MAYAPY=ON")
            if args.buildDocs:
                cmakeArgs.append("-DBUILD_DOCS=ON")
            if args.buildTools:
                cmakeArgs.append("-DBUILD_TOOLS=ON")
                cmakeArgs.append("-DTOOLS_SELECTION=\"%s\"" % args.toolsList[0])
            if args.buildNodes:
                cmakeArgs.append("-DBUILD_NODES=ON")
            if args.buildLibs:
                cmakeArgs.append("-DBUILD_LIBS=ON")
            runCMake(buildFolder, cmakeArgs)

#------------------------ PACKAGING ------------------------
        if args.packaging:
            installDir = os.path.abspath(os.path.join(args.installLocation, os.pardir))
            os.chdir(installDir)
            printMessage("Packaging %s..." % _project, logFile)
            packageName = "%s-%s-%s.zip" % (_project, _version, platform.system())
            packagePath = os.path.join(args.installLocation, packageName)
            with zipfile.ZipFile(packagePath, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(args.installLocation):
                    for f in files:
                        if f == packageName:
                            continue
                        toPackage = os.path.join(root, f).replace(installDir, "")[1::]
                        zipf.write(toPackage)
                        printCommand("Added to package: %s\n" % toPackage, logFile)

#------------------------- SUMMARY -------------------------
        printLine(args.verbosity)
        printMessage("-" * 80, logFile)
        printMessage("The configuration process is done!", logFile)
        printLine(args.verbosity)
        printMessage("%s was installed in: %s" % (_project, args.installLocation), logFile)
        runTime = time.strftime(timePattern, time.gmtime(time.time() - startTime))
        printMessage("Total time elapsed: %s." % runTime, logFile)
        if args.cleanUp:
            folderToClean = os.path.dirname(logFilePath)
            shutil.rmtree(folderToClean, False)
