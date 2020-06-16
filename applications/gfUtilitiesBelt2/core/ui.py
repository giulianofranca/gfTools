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
    * NDA

Sources:
    * NDA

This code supports Pylint. Rc file in project.
"""
import weakref
import sys
import os
import shiboken2
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtUiTools
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMaya as omui1
import maya.cmds as cmds

from gfUtilitiesBelt2.core import appInfo
reload(appInfo)




# def dockWindow(winClass):
#     # TODO: Review this functionality.
#     # 1- If the workspace control already exists, delete it and create a new control.
#     if cmds.workspaceControl(winClass.kWorkspaceControlName, q=True, ex=True):
#         cmds.workspaceControl(winClass.kWorkspaceControlName, e=True, close=True)
#         cmds.deleteUI(winClass.kWorkspaceControlName, control=True)

#     # 2- Create a workspaceControl manually.
#     dockControl = cmds.workspaceControl(
#         winClass.kWorkspaceControlName,
#         iw=275,
#         mw=True,
#         l=winClass.kWorkspaceControlLabel,
#         dtc=["ToolBox", "right"],
#         wp="preferred",
#         fl=True
#     )

#     # 3- Wrap the workspaceControl to a QWidget.
#     dockWidgetPtr = omui1.MQtUtil.findControl(winClass.kWorkspaceControlName)
#     dockWidget = shiboken2.wrapInstance(long(dockWidgetPtr), QtWidgets.QWidget) # TODO: Study more about this
#     dockWidget.setAttribute(QtCore.Qt.WA_DeleteOnClose)

#     # 4- Parent the main class to a dockWidget.
#     mainWin = winClass(dockWidget)

#     # 5- Restore the dockWidget to show the gui.
#     cmds.evalDeferred(lambda *args: cmds.workspaceControl(dockControl, e=True, rs=True))

#     # 6- Return the class
#     return mainWin



class GenericDockWindow(MayaQWidgetDockableMixin, QtWidgets.QWidget):

    kInstances = []

    def __init__(self, uiFile, parent=None):
        super(GenericWindow, self).__init__(parent=parent)
        GenericWindow.deleteInstances()
        self.kInstances.append(weakref.proxy(self))     # if error, try self.__class__.kInstances instead

        # Read .ui file
        self.uiFile = uiFile
        loader = QtUiTools.QUiLoader()
        uiFile = QtCore.QFile(uiFile)
        uiFile.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(uiFile, self)
        uiFile.close()

        self.initUI()

    def initUI(self):
        self.ui.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(QtCore.Qt.Tool)

    def deleteInstances(self):
        for instance in self.kInstances:
            try:
                instance.setParent(None)
                instance.deleteLater()
            except:
                # Ignore the fact that the actual parent has already been deleted by Maya.
                pass

            self.kInstances.remove(instance)
            del instance

    def showEvent(self, event):
        self.show()

    def closeEvent(self, event):
        # Use event.accept or event.ignore
        event.accept()
        sys.stdout.write("Application closed")




####################################
# MAIN WINDOW CLASS

# class MainWindow(QtWidgets.QMainWindow):

#     kinstances = []
#     kControlName = "%s_WorkspaceControl" appInfo.kApplicationName
#     kControlLabel = appInfo.kApplicationName


#     ######################################
#     # MAIN METHODS

#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent=parent)
#         MainWindow.deleteInstances()
#         self.__class__.kinstances.append(weakref.proxy(self))

#         # Set the workspaceControl margins
#         self.windowName = self.kControlName
#         self.ui = parent
#         self.workspaceLayout = parent.layout()
#         self.workspaceLayout.setContentsMargins(2, 2, 2, 2)

#         loader = QtUiTools.QUiLoader()

#     @staticmethod
#     def deleteInstances():
#         for instance in MainWindow.kinstances:
#             try:
#                 instance.setParent(None)
#                 instance.deleteLater()
#             except:
#                 # Ignore the fact that the actual parent has already been deleted by Maya.
#                 pass

#             MainWindow.kinstances.remove(instance)
#             del instance

#     def onExitCode(self):
#         pass


####################################
# EDIT POCKET WINDOW CLASS
