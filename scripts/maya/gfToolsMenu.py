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
# pylint: disable=import-error
import webbrowser
import maya.cmds as cmds

kMenuName = "gfToolsMenu"


def load():
    """Load gfTools custom menu"""
    if not cmds.menu(kMenuName, q=True, ex=True):
        gfToolsMenu = cmds.menu(kMenuName, l="gfTools", to=True, p="MayaWindow")
        cmds.menuItem(l="Load Nodes Plug-in", p=gfToolsMenu)
        cmds.menuItem(d=True, p=gfToolsMenu)
        cmds.menuItem(l="Look for Updates...", p=gfToolsMenu, c=checkUpdates)
        cmds.menuItem(d=True, p=gfToolsMenu)
        cmds.menuItem(l="gfTools Main Page", p=gfToolsMenu, c=launchWebsite)
        cmds.menuItem(l="About", p=gfToolsMenu)

def unload():
    """Unload gfTools custom menu"""
    if cmds.menu(kMenuName, q=True, ex=True):
        cmds.deleteUI(kMenuName)




def checkUpdates(*args):
    """Look if a newer version of gfTools is available"""
    # pylint: disable=unused-argument
    cmds.warning("This version not support auto-update yet. Sorry about that.")

def launchWebsite(*args):
    """Open the gfTools github page"""
    # pylint: disable=unused-argument
    webbrowser.open('https://github.com/giuliano-franca/gfTools')
