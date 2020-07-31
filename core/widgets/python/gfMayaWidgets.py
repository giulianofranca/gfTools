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
    * Create a class inherited from one of the module classes.
    e.g.:
        class MyWindow(gfMayaWidgets.GenericWidgetDock):
            kUiFilePath = "<path/to/ui/file.ui>"
            kWindowName = "myWindowWin"
            kWindowLabel = "My Window Title"
            kWorkspaceName = "myWindowDock"
            kWorkspaceOptions = "ttc=['AttributeEditor', -1], iw=300, mw=True, wp='preferred'"

            def __init__(self, data=None, parent=None):
                super(MyWindow, self).__init__(data, parent)

            def sizeHint(self):
                return QtCore.QSize(300, 600)

            def closeEvent(self, event):
                print("Application closed.")

    * Create a function to display this window. You can optionaly pass a dictionary containing the appSettings.
    e.g.:
        def showWindow():
            win = gfMayaWidgets.showMayaWidget(MyWindow, appData)
            return win

    * To show the window just call showWindow().
    * The ui file content can be acessed by self.ui.

Classes:
    * GenericWidgetWin          | Simple QWidget window
    * GenericWidgetDock         | Simple QWidget dockable window
    * GenericDialogWin          | Simple QDialog window

Functions:
    * showMayaWidget(widgetClass, data=None)
    * execMayaWidget(widgetClass, data=None)

Todo:
    * Make ability to not use a .ui file

Sources:
    * https://gist.github.com/liorbenhorin/69da10ec6f22c6d7b92deefdb4a4f475

This code supports Pylint. Rc file in project.
"""
import sys
import os
import shiboken2
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtUiTools
import maya.cmds as cmds
import maya.OpenMayaUI as omui1


class GenericWidgetWin(QtWidgets.QWidget):
    
    def __new__(cls, data=None, parent=None):
        version = cmds.about(version=True)
        if int(version) < 2017:
            raise RuntimeError("Maya version not supported (%s)." % version)
        return super(GenericWidgetWin, cls).__new__(cls)

    def __init__(self, data=None, parent=None):
        super(GenericWidgetWin, self).__init__(parent)
        self.setObjectName(self.kWindowName)
        self.setWindowTitle(self.kWindowLabel)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.checkUiFile()
        self.loadUiFile()

    @staticmethod
    def _checkDependencies(obj):
        attrs = ["kUiFilePath", "kWindowName", "kWindowLabel"]
        for attr in attrs:
            if not hasattr(obj, attr):
                msg = msg = "Class attribute <%s.%s> don't exists. You have to define it in order to use GenericWidgetWin." % (obj.__name__, attr)
                raise AttributeError(msg)
            else:
                cmd = "typeMatch = isinstance(obj.%s, str)" % attr
                exec cmd
                if not typeMatch:
                    msg = "Class attribute <%s.%s> must be a string." % (obj.__name__, attr)
                    raise AttributeError(msg)

    def checkUiFile(self):
        if self.kUiFilePath is None or not os.path.isfile(self.kUiFilePath):
            raise RuntimeError("Ui file not founded.")

    def loadUiFile(self):
        loader = QtUiTools.QUiLoader()
        uiFile = QtCore.QFile(self.kUiFilePath)
        uiFile.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(uiFile, self)
        uiFile.close()
        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.ui)




class GenericWidgetDock(GenericWidgetWin):
    kWorkspaceName = None
    kWorkspaceOptions = None

    def __init__(self, data=None, parent=None):
        self.dockWidget = parent
        super(GenericWidgetDock, self).__init__(data, parent)

    @staticmethod
    def _checkDependencies(obj):
        attrs = ["kUiFilePath", "kWindowName", "kWindowLabel", "kWorkspaceName", "kWorkspaceOptions"]
        for attr in attrs:
            if not hasattr(obj, attr):
                msg = msg = "Class attribute <%s.%s> don't exists. You have to define it in order to use GenericWidgetWin." % (obj.__name__, attr)
                raise AttributeError(msg)
            else:
                cmd = "typeMatch = isinstance(obj.%s, str)" % attr
                exec cmd
                if not typeMatch:
                    msg = "Class attribute <%s.%s> must be a string." % (obj.__name__, attr)
                    raise AttributeError(msg)

    def loadUiFile(self):
        loader = QtUiTools.QUiLoader()
        uiFile = QtCore.QFile(self.kUiFilePath)
        uiFile.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(uiFile, self)
        uiFile.close()
        self.mainLayout = self.dockWidget.layout()
        self.mainLayout.addWidget(self.ui)




class GenericDialogWin(QtWidgets.QDialog):

    def __new__(cls, data=None, parent=None):
        version = cmds.about(version=True)
        if int(version) < 2017:
            raise RuntimeError("Maya version not supported (%s)." % version)
        return super(GenericDialogWin, cls).__new__(cls)

    def __init__(self, data=None, parent=None):
        super(GenericDialogWin, self).__init__(parent)
        self.setObjectName(self.kWindowName)
        self.setWindowTitle(self.kWindowLabel)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.checkUiFile()
        self.loadUiFile()
        self.moveToCenterScreen()

    @staticmethod
    def _checkDependencies(obj):
        attrs = ["kUiFilePath", "kWindowName", "kWindowLabel"]
        for attr in attrs:
            if not hasattr(obj, attr):
                msg = "Class attribute <%s.%s> don't exists. You have to define it in order to use GenericDialogWin." % (obj.__name__, attr)
                raise AttributeError(msg)
            else:
                cmd = "typeMatch = isinstance(obj.%s, str)" % attr
                exec cmd
                if not typeMatch:
                    msg = "Class attribute <%s.%s> must be a string." % (obj.__name__, attr)
                    raise AttributeError(msg)

    def checkUiFile(self):
        if self.kUiFilePath is None or not os.path.isfile(self.kUiFilePath):
            raise RuntimeError("Ui file not founded.")

    def loadUiFile(self):
        loader = QtUiTools.QUiLoader()
        uiFile = QtCore.QFile(self.kUiFilePath)
        uiFile.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(uiFile, self)
        uiFile.close()
        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.ui)

    def moveToCenterScreen(self):
        screenGeo = QtGui.QGuiApplication.screens()[0].geometry()
        center = screenGeo.center()
        self.move(center.x() - self.ui.width() * 0.5, center.y() - self.ui.height() * 0.5)




def showMayaWidget(widgetClass, data=None):
    widgetClass._checkDependencies(widgetClass)
    if issubclass(widgetClass, GenericWidgetDock):
        if cmds.workspaceControl(widgetClass.kWorkspaceName, q=True, ex=True):
            cmds.workspaceControl(widgetClass.kWorkspaceName, q=True, close=True)
            cmds.deleteUI(widgetClass.kWorkspaceName, control=True)
        cmd = "workspace = cmds.workspaceControl(widgetClass.kWorkspaceName, %s, l=widgetClass.kWindowLabel)" % widgetClass.kWorkspaceOptions
        exec cmd in globals(), locals()
        workspacePtr = omui1.MQtUtil.findControl(workspace)
        parent = shiboken2.wrapInstance(long(workspacePtr), QtWidgets.QWidget)
        parent.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
    else:
        if cmds.window(widgetClass.kWindowName, q=True, ex=True):
            cmds.deleteUI(widgetClass.kWindowName)
        parent = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QMainWindow)
    win = widgetClass(data, parent)
    if issubclass(widgetClass, GenericWidgetDock):
        parent.destroyed.connect(lambda: win.close())
    else:
        win.show()
        win.activateWindow()
    return win




def execMayaWidget(widgetClass, data=None):
    widgetClass._checkDependencies(widgetClass)
    if issubclass(widgetClass, GenericWidgetDock):
        raise RuntimeError("Window inherited by <GenericWidgetDock> cannot be executed in execMayaWidget().")
    parent = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QMainWindow)
    win = widgetClass(data, parent)
    win.exec_()
