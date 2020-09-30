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
import maya.cmds as cmds
import gfTools.gfCore as gfCore

def launchMayaNodes():
    """Launch gfToolsNodes for Autodesk Maya."""
    if gfCore.platform() == "Windows":
        cmds.loadPlugin("gfToolsNodes.mll")
    elif gfCore.platform() == "Linux":
        cmds.loadPlugin("gfToolsNodes.so")
    else:
        cmds.loadPlugin("gfToolsNodes.bundle")

def launchGFUtilitiesBeltMaya():
    """Launch gfUtilitiesBelt for Autodesk Maya."""
    # pylint: disable=import-error, undefined-variable
    from gfUtilitiesBelt import run
    reload(run)
    run.main()
