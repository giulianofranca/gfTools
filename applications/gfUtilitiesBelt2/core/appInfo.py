# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

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
kApplicationVersion = "1.0.03"
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