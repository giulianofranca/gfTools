# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

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

Disclaimer:
    THIS PLUGIN IS JUST A PROTOTYPE. YOU MUST USE THE C++ RELEASE PLUGIN FOR PRODUCTION.
    YOU CAN FIND THE C++ RELEASE PLUGIN FOR YOUR SPECIFIC PLATFORM IN RELEASES FOLDER:
    "gfTools > plug-ins > Release"

How to use:
    * Copy the parent folder to the MAYA_SCRIPT_PATH.
    * To find MAYA_SCRIPT_PATH paste this command in a Python tab:
        import os; os.environ["MAYA_SCRIPT_PATH"].split(";")
    * In Maya, go to Windows > Settings/Preferences > Plug-in Manager.
    * Browse for "gfTools > core > plugin > dev > Python"
    * Find gfTools_P.py and import it.

Requirements:
    * Maya 2017 or above.

Todo:
    * Update to PySide2?.

This code supports Pylint. Rc file in project.
"""
import maya.cmds as cmds
import maya.api._OpenMaya_py2 as om2

class MainMenu(object):
    """Main class of gfTools menu. """

    kMenuName = ""
    kMenuLabel = ""

    def __init__(self):
        """Constructor."""
        return

    @classmethod
    def exists(cls):
        """Check if menu exists.

        Returns:
            bool: True if exists False if is not.
        """
        return cmds.menu(MainMenu.kMenuName, ex=True)

    @classmethod
    def deleteIfExists(cls):
        """Check if menu exists. If exists, delete it.

        Returns:
            True: If succeed.
        """
        if MainMenu.exists():
            cmds.deleteUI(MainMenu.kMenuName)

        return True

    @classmethod
    def loadMenu(cls):
        """Load the gfTools menu in Maya menu.

        Returns:
            True: If succeed.
        """
        MainMenu.deleteIfExists()

        mayaMenu = "MayaWindow"
        mainMenu = MainMenu.kMenuName
        mainLabel = MainMenu.kMenuLabel
        toolsMenu = "gfTools_PToolsMenu"
        toolsLabel = "Tools"

        cmds.menu(mainMenu, l=mainLabel, to=True, p=mayaMenu)
        # cmds.menuItem(l="Login")
        # cmds.menuItem(l="Sign Up")
        # cmds.menuItem(d=True)
        cmds.menuItem(toolsMenu, l=toolsLabel, to=True, sm=True)
        cmds.menuItem(l="Create IK Solver")
        # cmds.menuItem(l="Create IK Solver Options", ob=True)
        cmds.menuItem(l="Create PSD")
        # cmds.menuItem(l="Create PSD Options", ob=True)
        cmds.menuItem(l="Parent Constraint")
        # cmds.menuItem(l="Parent Constraint Options", ob=True)
        cmds.menuItem(l="Aim Constraint")
        # cmds.menuItem(l="Aim Constraint Options", ob=True)
        cmds.menuItem(l="Blend Transformations")
        # cmds.menuItem(l="Blend Transformations Options", ob=True)
        cmds.setParent("..", m=True)
        cmds.menuItem(d=True)
        cmds.menuItem(l="About Application", c=MainMenu.aboutApplication)

        return True

    @classmethod
    def unloadMenu(cls):
        """Unload the gfTools menu in Maya menu.

        Returns:
            True: If succeed.
        """
        MainMenu.deleteIfExists()

        return True

    @staticmethod
    def aboutApplication(*args):
        """About application"""
        # pylint: disable=unused-argument
        om2.MGlobal.displayInfo(u"gfTools [Python Prototype] | Copyright (c) 2019 Giuliano França")
