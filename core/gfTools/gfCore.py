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

Todo:
    * Geometry module (Maybe).
    * Rigging module.
    * Skinning module.
    * Attribute module.

This code supports Pylint. Rc file in project.
"""
import os


def version():
    """Return the application version in a string.

    Returns:
        str: The application version.
    """
    return "@GFTOOLS_STR_VERSION@"


def majorVersion():
    """Return the application major version.

    Returns:
        int: The application major version.
    """
    return int("@GFTOOLS_MAJOR_VERSION@")


def minorVersion():
    """Return the application minor version.

    Returns:
        int: The application minor version.
    """
    return int("@GFTOOLS_MINOR_VERSION@")


def patchVersion():
    """Return the application patch version.

    Returns:
        int: The application patch version.
    """
    return int("@GFTOOLS_PATCH_VERSION@")


def mayaVersionsCompatible():
    """Return the list of Maya versions that is compatible with this version of gfTools.

    Returns:
        list: A list of strings of every Maya version compatible.
    """
    versions = "@GFTOOLS_MAYA_VERSIONS_COMPATIBLE@"
    return versions.split(";")


def platform():
    """Return the platform compatible with this build.

    Returns:
        str: The platform name compatible with this build.
    """
    return "@CMAKE_SYSTEM_NAME@"


def installLocation():
    """Return the path to the install location of gfTools.

    Returns:
        str: The gfTools installation path.
    """
    libPath = os.path.join(os.path.dirname(__file__))
    gfToolsPath = os.path.join(libPath, os.pardir, os.pardir, os.pardir, os.pardir, os.pardir)
    return os.path.abspath(gfToolsPath)








# pylint: disable=import-error, import-outside-toplevel
# if sys.version_info.major >= 3:
#     import pickle
# else:
#     import cPickle as pickle



# def version():
#     """Return the application version.

#     Returns:
#         str: The application version.
#     """
#     data = getAppInfo()
#     if not data:
#         return
#     return data["Version"]


# def getAppInfo():
#     """Return application information.

#     Returns:
#         Dict or False: The dict containing all the application information if file founded.
#     """
#     gfToolsPath = installLocation()
#     appInfoFile = os.path.join(gfToolsPath, "core", "app")
#     try:
#         with open(appInfoFile, "rb") as f:
#             data = pickle.load(f)
#     except IOError as err:
#         print(err)
#         return False
#     return data


# def verifyMayaVersion():
#     """Verify if the current Maya version is compatible with gfTools.

#     Returns:
#         bool: True if its compatible False if its not.
#     """
#     import maya.cmds as cmds
#     currentVersion = int(cmds.about(version=True))

#     data = getAppInfo()
#     if not data:
#         return False
#     if currentVersion not in data["Maya Versions Compatible"]:
#         return False
#     return True


# def verifyPlatform():
#     """Verify if gfTools is compatible with current system platform.

#     Returns:
#         bool: True if its compatible False if its not.
#     """
#     data = getAppInfo()
#     if not data:
#         return False
#     if platform.system() != data["Platform"]:
#         return False
#     return True


# def installLocation():
#     """Return the path to the install location of gfTools.

#     Returns:
#         str: The gfTools installation path
#     """
#     gfToolsPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
#     return gfToolsPath
