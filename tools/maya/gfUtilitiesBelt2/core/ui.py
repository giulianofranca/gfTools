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
import functools
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import maya.cmds as cmds

from gfUtilitiesBelt2.core import appInfo
from gfUtilitiesBelt2.core import config
from gfUtilitiesBelt2.core import pockets
from gfUtilitiesBelt2.core import resources
import gfMayaWidgets
import gfWidgets
import gfLayouts
reload(appInfo)
reload(config)
reload(pockets)
reload(resources)
reload(gfMayaWidgets)
reload(gfWidgets)
reload(gfLayouts)


def showWindow(settings):
    fonts = [
    ":/fonts/fonts/WorkSans-Light.ttf",
    ":/fonts/fonts/WorkSans-Medium.ttf",
    ":/fonts/fonts/WorkSans-Regular.ttf",
    ":/fonts/fonts/WorkSans-SemiBold.ttf"
    ]
    for font in fonts:
        if font not in QtGui.QFontDatabase().families():
            QtGui.QFontDatabase.addApplicationFont(font)

    win = gfMayaWidgets.showMayaWidget(MainWin, data=settings)
    return win



########################################################################
# MAIN WINDOW CLASS

class MainWin(gfMayaWidgets.GenericWidgetDock):
    kUiFilePath = os.path.join(appInfo.kGUIPath, "win_main.ui")
    kWindowName = "%sWin" % appInfo.kApplicationName
    kWindowLabel = "%s" % appInfo.kApplicationName
    kWorkspaceName = "%sDock" % appInfo.kApplicationName
    kWorkspaceOptions = "dtc=['ToolBox', 'right'], iw=281, wp='preferred', mw=True"


    def __init__(self, data=None, parent=None):
        super(MainWin, self).__init__(parent)
        self.appConfig = data
        self.appSettings = data["Settings"]
        self.pockets = self.appConfig["Opened Pockets"]
        self.listView = False           # TODO: Read from settings

        self.initUI()


    def initUI(self):
        # TODO: Load ui in center of the screen
        self.ui.lblAppTitle.setText(appInfo.kApplicationName)
        self.ui.lblAppVersion.setText("version %s" % appInfo.kApplicationVersion)
        self.ui.wdgSideMenu.setFixedWidth(0)
        self.ui.txtSearch.setFixedHeight(0)
        self.ui.btnMenu.clicked.connect(self.showSideMenu)
        self.ui.btnSearch.clicked.connect(self.showSearchField)
        self.ui.btnListView.clicked.connect(self.toggleListView)
        self.ui.btnAboutApp.clicked.connect(self.loadAboutWin)
        self.ui.btnSettings.clicked.connect(self.loadSettingsWin)
        if not self.appConfig["Opened Pockets"]:
            self.generateTestPocket()
            # self.generateHomePocket()

        cmds.evalDeferred(self.autoUpdateLibraries)


    def loadAboutWin(self):
        gfMayaWidgets.openMayaDialog(AboutWin)


    def loadSettingsWin(self):
        gfMayaWidgets.showMayaWidget(SettingsWin)


    def resizeEvent(self, event):
        if self.ui.btnMenu.isChecked():
            self.ui.wdgSideMenu.setFixedWidth(event.size().width())


    def showSearchField(self):
        if self.ui.btnSearch.isChecked():
            self.ui.txtSearch.setFixedHeight(30)
        else:
            self.ui.txtSearch.setFixedHeight(0)

        
    def showSideMenu(self):
        if self.ui.btnMenu.isChecked():
            if issubclass(MainWin, gfMayaWidgets.GenericWidgetDock):
                self.ui.wdgSideMenu.setFixedWidth(self.parentWidget().width())
            else:
                self.ui.wdgSideMenu.setFixedWidth(self.width())
            # TODO: Animate this
            self.ui.btnMenu.setIcon(QtGui.QIcon(":/icons/img/gfUtilitiesBelt_close16.png"))
            self.ui.btnSearch.setVisible(False)
            self.ui.btnListView.setVisible(False)
            self.ui.txtSearch.setVisible(False)
        else:
            self.ui.wdgSideMenu.setFixedWidth(0)
            # TODO: Animate this
            self.ui.btnMenu.setIcon(QtGui.QIcon(":/icons/img/gfUtilitiesBelt_menu16.png"))
            self.ui.btnSearch.setVisible(True)
            self.ui.btnListView.setVisible(True)
            self.ui.txtSearch.setVisible(True)


    def toggleListView(self):
        # TODO: Every time a pocket is showed update list view
        if self.ui.btnListView.isChecked():
            self.listView = True
            self.ui.btnListView.setText("Icon View")
            self.ui.btnListView.setIcon(QtGui.QIcon(":/icons/img/gfUtilitiesBelt_iconView16.png"))
        else:
            self.listView = False
            self.ui.btnListView.setText("List View")
            self.ui.btnListView.setIcon(QtGui.QIcon(":/icons/img/gfUtilitiesBelt_listView16.png"))


    def autoUpdateLibraries(self):
        # TODO: Generate progress bar
        config.updateCheckMayaLibraries(self.appConfig)


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
        homeLabel.setToolTip("Create a pocket")
        homeLay.addWidget(homeLabel)
        self.ui.tabPockets.setTabsClosable(False)
        self.ui.tabPockets.addTab(homeTab, "Home")


    def generateTestPocket(self):
        tabHome = QtWidgets.QWidget()
        tabHome.setObjectName("tabHome")
        layHome = QtWidgets.QVBoxLayout(tabHome)
        layHome.setObjectName("layTabHome")
        layHome.setContentsMargins(0, 0, 0, 0)
        layHome.setSpacing(0)
        scrTab = QtWidgets.QScrollArea(tabHome)
        scrTab.setObjectName("srcTabHome")
        scrTab.setWidgetResizable(True)
        scrTab.setFrameShape(QtWidgets.QFrame.NoFrame)
        wdgContent = QtWidgets.QWidget(scrTab)
        wdgContent.setObjectName("wdgContentHome")
        if self.listView:
            layContent = QtWidgets.QVBoxLayout(wdgContent)
        else:
            # layContent = gfLayouts.FlowLayout(wdgContent)
            layContent = QtWidgets.QVBoxLayout(wdgContent)
        layContent.setObjectName("layContentHome")
        layContent.setContentsMargins(8, 8, 8, 8)
        layContent.setSpacing(8)
        for i in range(30):
            testWdg = gfWidgets.ListIconButton(wdgContent)
            testWdg.setMinimumHeight(40)
            testWdg.setText("Custom Tool".split("|")[-1])
            # testWdg.setText("NS")
            testWdg.setDescription("Create a bevel along the selected edges or faces")
            testWdg.setToolTip(testWdg.description())
            # testWdg.setDisplayStyle(gfWidgets.ListIconButton.DisplayStyle.kIconStyle)
            testWdg.setDisplayStyle(gfWidgets.ListIconButton.DisplayStyle.kListStyle)
            layContent.addWidget(testWdg)
        scrTab.setWidget(wdgContent)
        layHome.addWidget(scrTab)
        self.ui.tabPockets.setTabsClosable(False)
        self.ui.tabPockets.addTab(tabHome, "Home")


    def createTab(self, name="New"):
        # TODO: When the user create a new tab this function catch a signal
        nameCount = 0
        for pckt in self.pockets:
            if name == pckt.name:
                nameCount += 1
        if nameCount:
            name = "%s%s" % (name, nameCount)
        tabWidget = QtWidgets.QWidget()
        tabWidget.setObjectName("tab%s" % name)
        layTab = QtWidgets.QVBoxLayout(tabWidget)
        layTab.setObjectName("layTab%s" % name)
        layTab.setContentsMargins(0, 0, 0, 0)
        layTab.setSpacing(0)
        txtSearch = QtWidgets.QLineEdit(tabWidget)
        txtSearch.setObjectName("txtSearch%s" % name)
        txtSearch.setPlaceholderText("Search")
        txtSearch.setFixedHeight(0)
        txtSearch.setClearButtonEnabled(True)
        layTab.addWidget(txtSearch)
        scrTab = QtWidgets.QScrollArea(tabWidget)
        scrTab.setObjectName("srcTab%s" % name)
        scrTab.setWidgetResizable(True)
        scrTab.setFrameShape(QtWidgets.QFrame.NoFrame)
        wdgContent = QtWidgets.QWidget(scrTab)
        wdgContent.setObjectName("wdgContent%s" % name)
        # TODO: layout changed by list view button
        layContent = QtWidgets.QVBoxLayout(wdgContent)
        layContent.setObjectName("layContentHome")
        layContent.setContentsMargins(8, 8, 8, 8)
        layContent.setSpacing(8)
        scrTab.setWidget(wdgContent)
        layTab.addWidget(scrTab)
        self.ui.tabPockets.setTabsClosable(True)
        self.ui.tabPockets.addTab(tabWidget, name)


    def updateTabs(self):
        pass


    def sizeHint(self):
        return QtCore.QSize(281, 600)


    def closeEvent(self, event):
        event.accept()
        sys.stdout.write("%s closed.\n" % appInfo.kApplicationName)




########################################################################
# ABOUT APPLICATION WINDOW CLASS

class AboutWin(gfMayaWidgets.GenericDialogWin):
    kUiFilePath = os.path.join(appInfo.kGUIPath, "win_about.ui")
    kWindowName = "%sAboutWin" % appInfo.kApplicationName
    kWindowLabel = "About"


    def __init__(self, data=None, parent=None):
        super(AboutWin, self).__init__(parent)

        self.initUI()


    def initUI(self):
        self.setWindowFlags(QtCore.Qt.Tool)
        self.ui.lblAppTitle.setText(appInfo.kApplicationName)
        self.ui.lblAppVersion.setText("version %s" % appInfo.kApplicationVersion)
        self.closeBtn = gfWidgets.DialogButton("Close", self)
        self.closeBtn.setFixedHeight(30)
        self.closeBtn.setColor(QtGui.QColor(200, 200, 200))
        self.closeBtn.setRadius(8)
        self.closeBtn.setDisplayStyle(gfWidgets.DialogButton.DisplayStyle.kMainPriority)
        self.closeBtn.clicked.connect(lambda: self.close())
        self.ui.layCloseButton.addWidget(self.closeBtn)


    def sizeHint(self):
        return QtCore.QSize(400, 300)




########################################################################
# SETTINGS WINDOW CLASS

class SettingsWin(gfMayaWidgets.GenericWidgetWin):
    kUiFilePath = os.path.join(appInfo.kGUIPath, "win_settings.ui")
    kWindowName = "%sSettingsWin" % appInfo.kApplicationName
    kWindowLabel = "Settings"


    def __init__(self, data=None, parent=None):
        super(SettingsWin, self).__init__(parent)


    def sizeHint(self):
        return QtCore.QSize(600, 400)
