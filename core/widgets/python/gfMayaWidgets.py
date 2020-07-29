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
            kWindowName = "myWindowWin"
            kWindowLabel = "myWindow title"
            kWorkspaceName = "myWindowDock"
            kWorkspaceOptions = "ttc=['AttributeEditor', -1], iw=300, mw=True, wp='preferred'"

            def __init__(self, settings=None, parent=None):
                self.kUiFilePath = "<path/to/ui/file.ui>"
                super(MyWindow, self).__init__(settings, parent)

            def sizeHint(self):
                return QtCore.QSize(300, 600)

            def closeEvent(self, event):
                print("Application closed.")

    * Create a function to display this window. You can optionaly pass a dictionary containing the appSettings.
    e.g.:
        def showWindow():
            win = gfMayaWidgets.showMayaWidget(MyWindow, appSettings)
            return win

    * To show the window just call showWindow().
    * The ui file content can be acessed by self.ui.

Classes:
    * GenericWidgetWin          | Simple QWidget window
    * GenericWidgetDock         | Simple QWidget dockable window
    * GenericDialogWin          | Simple QDialog window

Functions:
    * showMayaWidget(widgetClass, settings=None)
    * execMayaWidget(widgetClass, settings=None)

Todo:
    * NDA

Sources:
    * https://gist.github.com/liorbenhorin/69da10ec6f22c6d7b92deefdb4a4f475

This code supports Pylint. Rc file in project.
"""
import sys
import os
import weakref
import shiboken2
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtUiTools
import maya.cmds as cmds
import maya.OpenMayaUI as omui1


class GenericWidgetWin(QtWidgets.QWidget):
    kInstances = []
    kWindowName = None
    kWindowLabel = None

    def __new__(cls, settings=None, parent=None):
        cls.checkMayaVersion()
        return super(GenericWidgetWin, cls).__new__(cls)

    def __init__(self, settings=None, parent=None):
        super(GenericWidgetWin, self).__init__(parent)
        self.deleteInstances()
        self.__class__.kInstances.append(weakref.proxy(self))

        self.setObjectName(self.kWindowName)
        self.setWindowTitle(self.kWindowLabel)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.genericWindowFlags = QtCore.Qt.Window
        self.setWindowFlags(self.genericWindowFlags)

        self.checkUiFile()
        self.loadUiFile()

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

    def closeEvent(self, event):
        event.accept()
        sys.stdout.write("Application closed.\n")

    def deleteInstances(self):
        for instance in self.kInstances:
            try:
                instance.setParent(None)
                instance.deleteLater()
            except:
                # Ignore the fact that the actual parent has already been deleted by Maya...
                pass

            self.kInstances.remove(instance)
            del instance

    @staticmethod
    def checkMayaVersion():
        version = cmds.about(version=True)
        if int(version) < 2017:
            raise RuntimeError("Maya version not supported (%s)." % version)

    # @classmethod
    # def deleteWindow(cls):
    #     if cmds.window(cls.kWindowName, q=True, ex=True):
    #         cmds.deleteUI(cls.kWindowName)




class GenericWidgetDock(GenericWidgetWin):
    kWorkspaceName = None
    kWorkspaceOptions = None

    def __init__(self, settings=None, parent=None):
        self.dockWidget = parent
        super(GenericWidgetDock, self).__init__(settings, parent)

    def closeEvent(self, event):
        event.accept()
        sys.stdout.write("Dock closed.\n")

    def loadUiFile(self):
        loader = QtUiTools.QUiLoader()
        uiFile = QtCore.QFile(self.kUiFilePath)
        uiFile.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(uiFile, self)
        uiFile.close()
        self.dockLayout = self.dockWidget.layout()
        self.dockLayout.addWidget(self.ui)

    # @classmethod
    # def deleteWindow(cls):
    #     if cmds.workspaceControl(cls.kWorkspaceName, q=True, exists=True):
    #         cmds.workspaceControl(cls.kWorkspaceName, e=True, close=True)
    #         cmds.deleteUI(cls.kWorkspaceName, control=True)

    # @classmethod
    # def dock(cls):
    #     cls.deleteWindow()
    #     command = "workspace = cmds.workspaceControl(cls.kWorkspaceName, %s, l=cls.kWindowLabel)" % cls.kWorkspaceOptions
    #     exec command in globals(), locals()
    #     workspacePtr = omui1.MQtUtil.findControl(workspace)
    #     workspaceWidget = shiboken2.wrapInstance(long(workspacePtr), QtWidgets.QWidget)
    #     workspaceWidget.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
    #     return workspaceWidget




class GenericDialogWin(QtWidgets.QWidget):
    kInstances = []
    kWindowName = None
    kWindowLabel = None

    def __new__(cls, settings=None, parent=None):
        cls.checkMayaVersion()
        return super(GenericDialogWin, cls).__new__(cls)

    def __init__(self, settings=None, parent=None):
        super(GenericDialogWin, self).__init__(parent)
        self.deleteInstances()
        self.__class__.kInstances.append(weakref.proxy(self))

        self.setObjectName(self.kWindowName)
        self.setWindowTitle(self.kWindowLabel)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.checkUiFile()
        self.loadUiFile()

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

    def closeEvent(self, event):
        event.accept()
        sys.stdout.write("Application closed.\n")

    def deleteInstances(self):
        for instance in self.kInstances:
            try:
                instance.setParent(None)
                instance.deleteLater()
            except:
                # Ignore the fact that the actual parent has already been deleted by Maya...
                pass

            self.kInstances.remove(instance)
            del instance

    @staticmethod
    def checkMayaVersion():
        version = cmds.about(version=True)
        if int(version) < 2017:
            raise RuntimeError("Maya version not supported (%s)." % version)

    @classmethod
    def deleteWindow(cls):
        if cmds.window(cls.kWindowName, q=True, ex=True):
            cmds.deleteUI(cls.kWindowName)




def showMayaWidget2(widgetClass, settings=None):
    # TODO: Delete deleteWindow() and dock() class methods
    widgetClass.deleteWindow()
    if issubclass(widgetClass, GenericWidgetDock):
        parent = widgetClass.dock()
    else:
        parent = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QMainWindow)
    win = widgetClass(settings, parent)
    if issubclass(widgetClass, GenericWidgetDock):
        parent.destroyed.connect(lambda: win.close())
        cmds.evalDeferred(lambda *args: cmds.workspaceControl(widgetClass.kWorkspaceName, e=True, rs=True))
    else:
        win.show()
        win.activateWindow()
    return win




def showMayaWidget(widgetClass, settings=None):
    if issubclass(widgetClass, GenericWidgetDock):
        if cmds.workspaceControl(widgetClass.kWorkspaceName, q=True, exists=True):
            cmds.workspaceControl(widgetClass.kWorkspaceName, e=True, close=True)
            cmds.deleteUI(widgetClass.kWorkspaceName, control=True)
        command = "workspace = cmds.workspaceControl(widgetClass.kWorkspaceName, %s, l=widgetClass.kWindowLabel)" % widgetClass.kWorkspaceOptions
        exec command in globals(), locals()
        workspacePtr = omui1.MQtUtil.findControl(workspace)
        parent = shiboken2.wrapInstance(long(workspacePtr), QtWidgets.QWidget)
        parent.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
    else:
        if cmds.window(widgetClass.kWindowName, q=True, ex=True):
            cmds.deleteUI(widgetClass.kWindowName)
        if issubclass(widgetClass, GenericWidgetWin):
            parent = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QMainWindow)
        else:
            parent = None
    win = widgetClass(settings, parent)
    if issubclass(widgetClass, GenericWidgetDock):
        parent.destroyed.connect(lambda: win.close())
        # cmds.evalDeferred(lambda *args: cmds.workspaceControl(widgetClass.kWorkspaceName, e=True, rs=True))
    else:
        win.show()
        win.activateWindow()
    return win


        




def execMayaWidget(widgetClass, settings=None):
    widgetClass.deleteWindow()
    if issubclass(widgetClass, GenericWidgetDock):
        parent = widgetClass.dock()
    else:
        parent = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QMainWindow)
    win = widgetClass(settings, parent)
    if issubclass(widgetClass, GenericWidgetDock):
        parent.destroyed.connect(lambda: win.close())
    else:
        win.exec_()
    if issubclass(widgetClass, GenericWidgetDock):
        cmds.evalDeferred(lambda *args: cmds.workspaceControl(widgetClass.kWorkspaceName, e=True, rs=True))
    return win