import sys
import os
from maya import cmds
from PySide2 import QtWidgets, QtCore, QtGui

import testinho as uiClass
reload(uiClass)


class POSELIBRARY(uiClass.RightClickMenuButton4):

    def __init__(self):
        super(POSELIBRARY, self).__init__()
        
        # Global Variables
        self.libraryDirectory = 'C:/Users/gfranca/Documents/maya/2017/scripts/gfTools/gfPoseLib'

        # Call Functions
        self.uiConfigure()

        # Show UI
        self.show(dockable=True)

        # Configure Workspace
        cmds.workspaceControl(self.CONTROL_NAME + "WorkspaceControl", e=True,
                              iw=275, mw=True, dtc=['ToolBox', 'right'], wp='preferred', fl=True)

    def uiConfigure(self):
        # Create a custom context menu for tree widget
        self.button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.button.customContextMenuRequested.connect(self.addMenu)

    def addMenu(self, position):
        menu = QtWidgets.QMenu()
        action = QtWidgets.QAction(self.button)
        action.setObjectName('action_deleteButton')
        action.setText('Delete')
        action.triggered.connect(self.removeButton)
        menu.addAction(action)
        menu.exec_(self.button.mapToGlobal(position))

    def removeButton(self):
        self.button.deleteLater()
