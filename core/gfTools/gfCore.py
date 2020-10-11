## @package gfCore
#  Documentation for this module.
#
#  More defails.
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
import maya.cmds as cmds

## Return the application version in a string.
#
#  @return str The application version.
def version():
    """Return the application version in a string.

    Returns:
        str: The application version.
    """
    return "@GFTOOLS_STR_VERSION@"


## Documentation for a class.
#
#  More details.
class Test:

    ## @var _memVar
    #  a member variable

    ## The constructor.
    def __init__(self):
        self._memVar = 0

    ## Documentation for a method.
    #  @param self The object pointer.
    def pyMethod(self):
        pass


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


def tweakVersion():
    """Return the application tweak version.

    Returns:
        str: The application tweak version.
    """
    return "@GFTOOLS_TWEAK_VERSION@"


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


def loadPlugin():
    """Load gfTools plugin.

    Returns:
        Bool: True if it suceeded and False if it doesn't.
    """
    # pylint: disable=broad-except
    if platform() == "Windows":
        pluginExt = ".mll"
    elif platform() == "Linux":
        pluginExt = ".so"
    elif platform() == "Darwin":
        pluginExt = ".bundle"
    pluginName = "gfTools%s" % pluginExt
    try:
        cmds.loadPlugin(pluginName)
    except Exception:
        return False
    return True


def isPluginLoaded():
    """Is plugin loaded?"""
    if platform() == "Windows":
        pluginExt = ".mll"
    elif platform() == "Linux":
        pluginExt = ".so"
    elif platform() == "Darwin":
        pluginExt = ".bundle"
    pluginName = "gfTools%s" % pluginExt
    return cmds.pluginInfo(pluginName, q=True, loaded=True)
