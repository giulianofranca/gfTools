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
    * NDA

Sources:
    * NDA

This code supports Pylint. Rc file in project.
"""
import sys
import os
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

import maya.cmds as cmds
import gfMayaWidgets
from gfUtilitiesBelt2.core import appInfo
from gfUtilitiesBelt2.core import config
reload(gfMayaWidgets)
reload(appInfo)
reload(config)


def showWindow(settings):
    win = gfMayaWidgets.showMayaWidget(MainWin, settings)
    return win



########################################################################
# MAIN WINDOW CLASS

class MainWin(gfMayaWidgets.GenericWidgetDock):
    kUiFilePath = os.path.join(appInfo.kGUIPath, "win_main.ui")
    kWindowName = "gfUtilitiesBeltWin"
    kWindowLabel = "%s" % appInfo.kApplicationName
    kWorkspaceName = "gfUtilitiesBeltDock"
    kWorkspaceOptions = "dtc=['ToolBox', 'right'], iw=281, wp='preferred', mw=True"


    def __init__(self, settings=None, parent=None):
        super(MainWin, self).__init__(settings, parent)
        self.appConfig = settings
        self.appSettings = settings["Settings"]

        cmds.evalDeferred(self.autoUpdateLibraries)


    def autoUpdateLibraries(self):
        config.updateCheckMayaLibraries(self.appConfig)
        if not self.appConfig["Opened Pockets"]:
            self.generateHomePocket()


    def generateHomePocket(self):
        homeTab = QtWidgets.QWidget()
        homeTab.setObjectName("tabHome")
        homeLay = QtWidgets.QVBoxLayout(homeTab)
        homeLay.setObjectName("layTabHome")
        homeLabel = QtWidgets.QLabel(homeTab)
        homeLabel.setObjectName("lblHome")
        homeFont = QtGui.QFont()
        homeFont.setPointSize(16)
        homeLabel.setFont(homeFont)
        homeLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        homeLabel.setAlignment(QtCore.Qt.AlignCenter)
        homeLabel.setText("<html><head/><body><p>Hey buddy!<br/><br/>May I help you?</p></body></html>")
        homeLay.addWidget(homeLabel)
        self.ui.tabPockets.setTabsClosable(False)
        self.ui.tabPockets.addTab(homeTab, "Home")


    def sizeHint(self):
        return QtCore.QSize(281, 600)


    def closeWorkspace(self):
        sys.stdout.write("gfUtilitiesBelt closed.\n")


########################################################################
# EDIT POCKET WINDOW CLASS
