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
    * Copy the parent folder to the MAYA_SCRIPT_PATH.
    * To find MAYA_SCRIPT_PATH paste this command in a Python tab:
        import os; os.environ["MAYA_SCRIPT_PATH"].split(";")
    * In Maya, go to Windows > Settings/Preferences > Plug-in Manager.
    * Browse for "gfTools > plug-ins > dev > python"
    * Find gfTools_P.py and import it.

Requirements:
    * Maya 2017 or above.

Todo:
    * Add commands to generate/read settings for the application

Sources:
    * NDA

This code supports Pylint. Rc file in project.
"""
import os
import maya.cmds as cmds


kApplicationName = "gfUtilitiesBelt"
kApplicationVersion = "1.0.09"
kMinRequiredVersion = "1.0"
kMayaVersion = cmds.about(v=True)

kCorePath = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
kAppPath = os.path.normpath(os.path.abspath(os.path.join(kCorePath, os.pardir)))
kCustomToolsPath = os.path.normpath(os.path.abspath(os.path.join(kAppPath, "customTools")))
kGUIPath = os.path.normpath(os.path.abspath(os.path.join(kAppPath, "gui")))
kPocketsPath = os.path.normpath(os.path.abspath(os.path.join(kAppPath, "pockets")))




def checkVersion(version):
    """Check if the given version is compatible with this app version.

    Args:
        version (str): The version to check.

    Returns:
        True or False: True if the version is compatible and False if is not.
    """
    version = float(".".join(version.split(".")[:2]))
    requiredVersion = float(".".join(kMinRequiredVersion.split(".")))
    return version >= requiredVersion


def checkMayaVersion(version):
    """Check if the given version is greater or equal to current Maya version.

    Args:
        version (str): The version to check.

    Returns:
        True or False: True if the version is greater or equal and False if is not.
    """
    version = float(version)
    mayaVersion = float(kMayaVersion)
    return version >= mayaVersion