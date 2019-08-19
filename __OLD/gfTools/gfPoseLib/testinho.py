import sys
import os
import weakref
import shiboken2
from PySide2 import QtWidgets, QtCore, QtGui
from maya import cmds
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


class dockWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    DOCK_LABEL_NAME = 'gfCustomDock'
    CONTROL_NAME = 'gfCustomDockWin'
    instances = list()

    def __init__(self):
        super(dockWindow, self).__init__()
        dockWindow.deleteInstances()
        self.__class__.instances.append(weakref.proxy(self))
        if cmds.workspaceControl(self.CONTROL_NAME + "WorkspaceControl", ex=True):
            cmds.deleteUI(self.CONTROL_NAME + "WorkspaceControl")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.setupUi()

    @staticmethod
    def deleteInstances():
        for ins in dockWindow.instances:
            try:
                print('Delete {}'.format(ins))
            except:
                print('Window reference seems to be removed already, ignore.')
            try:
                ins.setParent(None)
                ins.deleteLater()
            except:
                pass
            try:
                dockWindow.instances.remove(ins)
                del ins
            except:
                pass

    def setupUi(self):
        pass


class RightClickMenuButton(QtWidgets.QMainWindow):

    def __init__(self):
        super(RightClickMenuButton, self).__init__()
        self.setObjectName('testWindow')
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName('centralWidget')
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.button = QtWidgets.QPushButton()
        self.button.setText('Delete me with right click')
        self.button.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.addMenuActions()
        self.verticalLayout.addWidget(self.button)
        self.setCentralWidget(self.centralWidget)

    def addMenuActions(self):
        delete = QtWidgets.QAction(self.button)
        delete.setText('Delete')
        delete.triggered.connect(self.removeButton)
        self.button.addAction(delete)

    def removeButton(self):
        self.button.deleteLater()


class RightClickMenuButton2(dockWindow):
    DOCK_LABEL_NAME = 'child test window'  # Window display name
    instances = list()
    CONTROL_NAME = 'child_test_win'  # Window unique object name

    def __init__(self):
        super(RightClickMenuButton2, self).__init__()
        self.setObjectName(self.CONTROL_NAME)
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName('centralWidget')
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName('verticalLayout')
        self.button = QtWidgets.QPushButton()
        self.button.setObjectName('btnDelete')
        self.button.setText('Delete me with right click')
        # self.button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self.button.customContextMenuRequested.connect(self.addMenu)
        self.verticalLayout.addWidget(self.button)
        self.setCentralWidget(self.centralWidget)

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


class RightClickMenuButton3(dockWindow):
    DOCK_LABEL_NAME = 'child test window'  # Window display name
    instances = list()
    CONTROL_NAME = 'child_test_win'  # Window unique object name

    def __init__(self):
        super(RightClickMenuButton3, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName(self.CONTROL_NAME)
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName('centralWidget')
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName('verticalLayout')

        self.treeWidget = QtWidgets.QTreeWidget()
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setObjectName('treeWidget')
        item0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item0.setExpanded(True)
        item1 = QtWidgets.QTreeWidgetItem(item0)
        item2 = QtWidgets.QTreeWidgetItem(item0)
        self.treeWidget.topLevelItem(0).setText(0, 'A')
        self.treeWidget.topLevelItem(0).child(0).setText(0, 'TAMO AI')
        self.treeWidget.topLevelItem(0).child(1).setText(0, 'NA MACIOTA')
        # self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self.treeWidget.customContextMenuRequested.connect(self.addMenu)

        self.verticalLayout.addWidget(self.treeWidget)
        self.setCentralWidget(self.centralWidget)


class RightClickMenuButton4(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    CONTROL_NAME = 'TESTWindow'
    instances = list()

    def __init__(self):
        super(RightClickMenuButton4, self).__init__()
        RightClickMenuButton4.deleteInstances()
        if cmds.workspaceControl(self.CONTROL_NAME + 'WorkspaceControl', ex=True):
            cmds.deleteUI(self.CONTROL_NAME + 'WorkspaceControl')
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setObjectName('TESTWindow')
        self.setWindowTitle('TESTE')
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName('centralWidget')
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName('verticalLayout')
        self.button = QtWidgets.QPushButton()
        self.button.setObjectName('btnDelete')
        self.button.setText('Delete me with right click')
        # self.button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self.button.customContextMenuRequested.connect(self.addMenu)
        self.verticalLayout.addWidget(self.button)
        self.setCentralWidget(self.centralWidget)

    @staticmethod
    def deleteInstances():
        for ins in RightClickMenuButton4.instances:
            try:
                print('Delete {}'.format(ins))
            except:
                print('Window reference seems to be removed already, ignore.')
            try:
                ins.setParent(None)
                ins.deleteLater()
            except:
                pass
            try:
                RightClickMenuButton4.instances.remove(ins)
                del ins
            except:
                pass

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
# 1- Set widget a setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
# 2- Create action parented to a widget
# 3- Set text to this action
# 4- Create a signal triggered.connect(function) to a QAction
# 5- Set widget addAction(QAction)
