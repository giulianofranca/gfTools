###################################################################################################################
# HOW TO USE DOCK WINDOW
# 1- Import PySide2, import maya.cmds and import MayaQWidgetDockableMixin from maya.app.general.mayaMixin
# 2- Create class dockWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow)
###################################################################################################################
import weakref
import shiboken2
from PySide2 import QtWidgets, QtCore, QtGui
from maya import cmds
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


class dockWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    DOCK_LABEL_NAME = 'Test'
    CONTROL_NAME = 'testWindow'
    instances = list()

    def __init__(self):
        super(dockWindow, self).__init__()
        dockWindow.deleteInstances()
        self.__class__.instances.append(weakref.proxy(self))
        # Not sure, but I suppose that we better keep track of instances of our window and keep Maya environment clean.
        # So we'll remove all instances before creating a new one.
        if cmds.window(self.CONTROL_NAME + "WorkspaceControl", ex=True):
            print("Removing", self.CONTROL_NAME + "WorkspaceControl")
            cmds.deleteUI(self.CONTROL_NAME + "WorkspaceControl")
            print("Removed", self.CONTROL_NAME + "WorkspaceControl")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        # Set object name and window title
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
                # ignore the fact that the actual parent has already been deleted by Maya...
                pass
            try:
                dockWindow.instances.remove(ins)
                del ins
            except:
                # Supress error
                pass
    def setupUi(self):
        pass


def getMainWindow():
    """
    Get main Maya window instance.
    """
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = shiboken2.wrapInstance(long(mayaMainWindowPtr), QMainWindow)
    return mayaMainWindow


def dock_window(dialog_class, width=440):
    """
    This function is to be updates to actually dock window on creation to the right.
    """
    dock_win = dialog_class()
    dock_win.show(dockable=True)
    return dock_win


def show_test():
    # This is how to call and show a window
    ChildTestWindow().show(dockable=True)


class ChildTestWindow(dockWindow):
    """
    Example child window inheriting from main class.
    """
    DOCK_LABEL_NAME = 'child test window'  # Window display name
    instances = list()
    CONTROL_NAME = 'child_test_win'  # Window unique object name
    def __init__(self):
        super(ChildTestWindow, self).__init__()

    def setupUi(self):
        self.setObjectName(self.CONTROL_NAME)
        self.setWindowTitle(self.DOCK_LABEL_NAME)
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.my_label = QtWidgets.QLabel('Beam me up, Scotty!')
        self.main_layout.addWidget(self.my_label)

        self.menuBar = QtWidgets.QMenuBar()
        self.presetsMenu = self.menuBar.addMenu(("&Presets"))
        self.saveConfigAction = QtWidgets.QAction(("&Save Settings"), self)
        self.presetsMenu.addAction(self.saveConfigAction)

        self.setMenuBar(self.menuBar)

        self.statusBar = QtWidgets.QStatusBar()
        self.statusBar.showMessage("Status bar ready.")

        self.setStatusBar(self.statusBar)

        self.statusBar.setObjectName("statusBar")
        self.setStyleSheet("#statusBar {background-color:#faa300;color:#fff}")
# =============================================================================================================================================================
# class Ui_MainWindow(object):
#     windowName = "MyWindow"
#     windowTitle = "My Window"
#
#     def _convertMayaElementsToQt(self, mayaLayout):
#         '''
#         Find a pointer to the mayaLayout, wrap the pointer into a QWidget and return the QWidget.
#         '''
#         ptr = omui.MQtUtil.findControl(mayaLayout)
#         outputWidget = shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)
#         return outputWidget
#
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName(Ui_MainWindow.windowName)
#         MainWindow.setWindowTitle(Ui_MainWindow.windowTitle)
#         MainWindow.resize(800, 600)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
#         self.verticalLayout.setObjectName("verticalLayout")
#         self.workspaceControl = self.mayaWorkspaceWidget() # This is a QWidget
#         self.mayaViewport = self.mayaViewportWidget()
#         self.mayaViewport = self._convertMayaElementsToQt(self.mayaViewport) # This is a QWidget
#         self.mayaViewport.setParent(self.workspaceControl)
#         self.pushButton = QtWidgets.QPushButton()
#         self.pushButton.setText("Click me")
#         self.pushButton.setObjectName("pushButton")
#         self.pushButton.setParent(self.workspaceControl)
#         self.verticalLayout.addWidget(self.workspaceControl)
#         # self.verticalLayout.addWidget(self.mayaViewport)
#         # self.verticalLayout.addWidget(self.pushButton)
#         MainWindow.setCentralWidget(self.centralwidget)
#
#     def mayaWorkspaceWidget(self):
#         workspaceName = Ui_MainWindow.windowName + "_workspaceControl"
#         try:
#             cmds.deleteUI(workspaceName)
#         except:
#             pass
#         mainControl = cmds.workspaceControl(workspaceName, ttc=["AttributeEditor", -1], iw=200, mw=True,
#                                              wp='preferred', label="Teste")
#         # mainControl = cmds.workspaceControl(self.widgets['WorkspaceName'], iw=275, mw=True, l='gfMayaTools',
#         #                                     dtc=['ToolBox', 'right'], wp='preferred', fl=True)
#         cmds.workspaceControl(workspaceName, e=True, vis=True)
#         cmds.workspaceControl(workspaceName, e=True, r=True)  # raise it
#         cmds.evalDeferred(lambda *args: cmds.workspaceControl(mainControl, e=True, r=True))
#         mainControlWidget = self._convertMayaElementsToQt(mainControl)
#         mainControlWidget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
#         return mainControlWidget
#
#     ####################################################################################################################
#     # MAYA CUSTOM WIDGETS
#     ####################################################################################################################
#
#     def mayaViewportWidget(self):
#         '''
#         Create a maya.cmds widget and return the parent layout.
#         '''
#         cmds.setParent(self.verticalLayout.objectName())
#         paneLayoutName = cmds.paneLayout()
#         modelPanelName = cmds.modelPanel("embeddedModelPanel#", cam='persp')
#         return paneLayoutName


# class mayaWorkspaceControl(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         QtWidgets.QWidget.__init__(self)
#
#     def setupUi(self):
#         workspaceName = Ui_MainWindow.windowName + "_workspaceControl"
#         try:
#             cmds.deleteUI(workspaceName)
#         except:
#             pass
#         mainControl = cmds.workspaceControl(workspaceName, ttc=["AttributeEditor", -1], iw=200, mw=True,
#                                              wp='preferred', label="Teste")
#         # mainControl = cmds.workspaceControl(self.widgets['WorkspaceName'], iw=275, mw=True, l='gfMayaTools',
#         #                                     dtc=['ToolBox', 'right'], wp='preferred', fl=True)
#         cmds.workspaceControl(workspaceName, e=True, vis=True)
#         cmds.workspaceControl(workspaceName, e=True, r=True)  # raise it
#         cmds.evalDeferred(lambda *args: cmds.workspaceControl(mainControl, e=True, r=True))
#         mainControlWidget = self._convertMayaElementsToQt(mainControl)
#         mainControlWidget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
#         return mainControlWidget
