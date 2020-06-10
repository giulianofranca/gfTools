# Compile all plugins from gfTools for all platforms and all maya versions
# https://gist.github.com/jlgerber/5b82d962857792c08300853ebe523a8c
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
import tarfile
# TODO: Add a function to read gfTools already compiled and zipped from all OS and pull them all toghether automatically.

defaultPath = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
_project = "gfTools"
_version = "1.0"

startTime = time.time()

def windows():
    return platform.system() == "Windows"

def linux():
    return platform.system() == "Linux"

def macOS():
    return platform.system() == "Darwin"

def findCMake():
    result = shutil.which("cmake")
    if result is None:
        raise RuntimeError("Couldn't find CMake in your system. Please check if it is installed.")
    sys.stdout.write("\nCMake found.\n")

def findPython3():
    python3 = sys.version_info.major >= 3
    if not python3:
        raise RuntimeError("This script need to be running using any Python 3 version. (Script builded with Python 3.7.4)")
    sys.stdout.write("\nPython 3 found.")

def findVisualStudioVersion():
    msvcCompiler = find_executable("cl")
    if msvcCompiler:
        return float(os.environ["VisualStudioVersion"])
    return None

def run(command):
    sys.stdout.write("Running command: %s\n\n" % command)
    args = shlex.split(command)
    encoding = sys.stdout.encoding or "UTF-8"
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        out = process.stdout.readline()
        outLine = out.decode(encoding)
        if outLine:
            sys.stdout.write("%s" %outLine)
        elif process.poll() is not None:
            break
    return process

def runCMake(args, version):
    buildFolder = "./build/%s" % version
    command = []
    command.append("cmake")
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
    if generator is not None:
        generator = '-G "%s"' % generator
    command.append(generator)
    installSource = args.installSource
    if installSource:
        command.append("-DINSTALL_SOURCE=ON")
    command.append("-DMAYA_VERSION=%s" % str(version))
    if args.installLocation is not None:
        command.append("-DCMAKE_INSTALL_PREFIX=%s" % args.installLocation)
    command.append("-S .")
    command.append("-B %s" % buildFolder)
    process = run(" ".join(command))

    config = args.config
    command = ("cmake --build {build} --config {config} --target install"
               .format(build=buildFolder, config=config))
    process2 = run(command)

def getFilesRecursively(rootDir, extension=None, toPass=None):
    assert isinstance(extension, str) or extension is None
    assert isinstance(toPass, list) or toPass is None
    for root, dirs, files in os.walk(rootDir):
        passCheck = False
        if toPass is not None:
            for passVar in toPass:
                if passVar in os.path.abspath(root):
                    passCheck = True
                    break
        if passCheck:
            continue
        for f in files:
            if extension is None or f.lower().endswith(extension):
                yield os.path.normpath(os.path.abspath(os.path.join(root, f)))

def getFilesFromDir(rootDir, extension=None, toPass=None):
    assert isinstance(extension, list) or extension is None
    assert isinstance(toPass, list) or toPass is None
    for f in os.listdir(rootDir):
        passCheck = False
        if toPass is not None:
            for passVar in toPass:
                if f == passVar:
                    passCheck = True
                    break
        if passCheck:
            continue
        if extension is not None:
            for ext in extension:
                if f.upper().endswith(ext.upper()):
                    yield os.path.normpath(os.path.abspath(f))
        else:
            yield os.path.normpath(os.path.abspath(f))



#############################################################################################
# BUILD PLUGIN

description = """
Build script for gfTools

Build all the C++ files in the plugin and export a single folder containing all
the dependencies necessary to run gfTools on Maya based on your OS.
"""
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=description
)
parser.add_argument("-mv", "--maya-version", type=int, nargs="+", choices=[2017, 2018, 2019, 2020],
                    help="Select which maya versions will be compiled.", dest="mayaVersion")
parser.add_argument("-c", "--config", type=str, choices=["Debug", "Release"], default="Release",
                    help="The output config.")
parser.add_argument("-o", "--output", type=str, default=defaultPath, dest="installLocation",
                    help="Custom install location.")
parser.add_argument("-is", "--install-source", action="store_true", dest="installSource",
                    help="Export the source code whithin the builded plugin.")
parser.add_argument("-ea", "--export-all", action="store_true", dest="exportAll",
                    help="Export all %s project, including Python applications." % _project)
parser.add_argument("-ez", "--export-zip", action="store_true", dest="exportZip",
                    help="Export a zip file with the plugin builded.")
parser.add_argument("-ca", "--clean-after", action="store_true", dest="cleanAfter",
                    help="Clean the build folder after building.")
parser.add_argument("-g", "--generator", type=str,
                    help="CMake generator to use when building libraries with 'cmake'.")
parser.add_argument("--version", action="version", version="%s Builder %s" % (_project, _version),
                    help="Show program's version.")

args = parser.parse_args()
os.chdir(defaultPath)

findPython3()
findCMake()
sys.stdout.write("\n\n\tStart %s build process.\n" % _project)
outputName = "gfTools_%s" % platform.system()

#------------------------ PLUG-INS ------------------------
if args.mayaVersion is None:
    mayaVersions = [2017, 2018, 2019, 2020]
else:
    mayaVersions = args.mayaVersion
compTime = []
for version in mayaVersions:
    startCompTime = time.time()
    sys.stdout.write("\n\n\tStart building for Autodesk Maya %s.\n\n" % version)
    runCMake(args, version)
    sys.stdout.write("\n\tBuild for Autodesk Maya %s complete!" % version)
    runTime = round(time.time() - startCompTime, 2)
    sys.stdout.write("\n\tTime elapsed: %s secs" % runTime)
    compTime.append(runTime)

#------------------------ EXPORT ALL ------------------------
if args.exportAll:
    # 3- Get core folder
    # 4- Get utils folder
    # foldersToPass = ["__OLD", "_studies", "python", "starters"]

    startExportTime = time.time()
    sys.stdout.write("\n\n\n\tStart exporting %s files.\n\n" % _project)

    # 1- Get project main files
    sys.stdout.write("Exporting project main files:\n")
    toPass = ["build.py", "pylintInitHook.py"]
    ext = [".py", ".md", "LICENSE"]
    if args.installSource:
        toPass = []
        ext.extend([".txt", ".pylintrc"])
    files = getFilesFromDir(".", ext, toPass)
    for f in files:
        sys.stdout.write("- Copying file: %s.\n" % f)
        shutil.copy(f, outputName)

    # 2- Get applications folder
    # TODO: Solve this after fix all the problems with gfTools applications
    # sys.stdout.write("\nExporting applications files:\n")
    # toPass = ["__Prototype", "api"]
    # ext = [".py", ".json"]
    # files = getFilesRecursively("applications")

    # 3- Get cmake folder
    # if args.installSource:
    #     sys.stdout.write("Exporting cmake files:\n")
    #     files = getFilesRecursively("cmake")
    #     path = os.path.join(outputName, "cmake")
    #     os.makedirs(path)
    #     for f in files:
    #         sys.stdout.write("- Copying file: %s.\n" % f)
    #         shutil.copy(f, path)

    # 4- Get core folder
    # sys.stdout.write("Exporting core files:\n")
    # toPass = ["_studies"]
    # ext = [".py"]
    # files = []
    # for e in ext:
    #     files.extend(getFilesRecursively("core", e, toPass))
    # for f in files:
    #     sys.stdout.write("- Copying file: %s.\n" % f)
    #     shutil.copytree(f, os.path.join(outputName, "core"))



# This test failed in get core folder
# path = os.path.join(outputName, "core")
# os.makedirs(path, exist_ok=True)
# print("------ %s" % os.path.dirname(os.path.abspath(os.path.join(f, os.pardir))))
# if os.path.basename(os.path.dirname(f)) != "core":
#     print("------- %s" % os.path.basename(os.path.abspath(os.path.join(f, os.pardir))))
#     toCreate = []
#     toCreate.append("widgets")
# shutil.copy(f, path)


#------------------------ FINISHING ------------------------
installLocation = os.path.normpath(os.path.join(defaultPath, outputName))
sys.stdout.write("\n\n\n\t%s\n" % ("-" * 60))
sys.stdout.write("\tThe build process is done!\n")
for i, version in enumerate(mayaVersions):
    sys.stdout.write("\tPlug-ins compilation for Autodesk Maya %s: [Done] | %s secs elapsed.\n" % (version, compTime[i]))
sys.stdout.write("\tThe build output is: %s" % installLocation)

if args.exportZip:
    sys.stdout.write("\n\n\tExporting to a compressed file...\n")
    if linux():
        sys.stdout.write("\t- Exporting %s.tar.gz file.\n" % outputName)
        # TODO: Export in .tar.gz format
    else:
        sys.stdout.write("\t- Exporting %s.zip file.\n" % outputName)
        zipname = "%s.zip" % outputName
        with zipfile.ZipFile(zipname, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(outputName):
                for file in files:
                    zipf.write(os.path.join(root, file))
    sys.stdout.write("\tZip compression complete.")

if args.cleanAfter:
    sys.stdout.write("\n\n\tCleaning up project folder...\n")
    sys.stdout.write("\t- Removing build folder.\n")
    shutil.rmtree("build", ignore_errors=True)
    sys.stdout.write("\tCleaning complete.\n")

runTime = round(time.time() - startTime, 2)
sys.stdout.write("\n\n\tProcess done! Total time Elapsed: %s secs\n" % runTime)
