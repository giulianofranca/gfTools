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
from gfUtilitiesBelt2.core.getMayaInfo import getMayaWindow
reload(appInfo)


kMainUIFile = os.path.join(appInfo.kGUIPath, "win_main.ui")




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

class MainWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        loader = QtUiTools.QUiLoader()
        uiFile = QtCore.QFile(kMainUIFile)
        uiFile.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(uiFile, self)
        uiFile.close()

        self.initUI()
        self.show()
        self.activateWindow()

    def initUI(self):
        self.setWindowTitle("%s %s" %(appInfo.kApplicationName, appInfo.kApplicationVersion))
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1.0)
        self.oldPos = self.pos()
        self.ui.btnClose.clicked.connect(lambda: self.close())

    def mousePressEvent(self, event):
        localPos = QtCore.QPoint(event.localPos().x(), event.localPos().y())
        if self.childAt(event.pos()) == self.ui.frmTitleBar:
            if self.windowOpacity() <= 1.0:
                self.setWindowOpacity(0.5)
        self.oldPos = [localPos, self.pos()]

    def mouseMoveEvent(self, event):
        localClickPos = self.oldPos[0]
        globalClickPos = localClickPos + self.oldPos[1]
        if self.childAt(localClickPos) == self.ui.frmTitleBar:
            delta = QtCore.QPoint(event.globalPos() - globalClickPos)
            self.move(self.pos() + delta)
            self.oldPos = [localClickPos, self.pos()]
        # localClickPos = self.oldPos[0]
        # globalClickPos = localClickPos + self.oldPos[1]
        # if localClickPos.y() <= self.ui.frmTitleBar.height():
        #     delta = QtCore.QPoint(event.globalPos() - globalClickPos)
        #     self.move(self.pos() + delta)
        #     self.oldPos = [localClickPos, self.pos()]

    def mouseReleaseEvent(self, event):
        if self.windowOpacity() < 1.0:
            self.setWindowOpacity(1.0)

    def closeEvent(self, event):
        event.accept()
        sys.stdout.write("Application closed.\n")


####################################
# EDIT POCKET WINDOW CLASS
