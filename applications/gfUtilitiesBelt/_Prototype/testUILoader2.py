import sys
import os
import shiboken2
import maya.cmds as cmds
import maya.OpenMayaUI as omui1
from PySide2 import QtCore, QtWidgets, QtUiTools
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


SCRIPTLOC = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
UIFILELOC = os.path.join(SCRIPTLOC, "gui", "testUI", "testmainwindow.ui")


def loadUIWidget(uifilename, parent=None):
    loader = QtUiTools.QUiLoader()
    uifile = QtCore.QFile(uifilename)
    uifile.open(QtCore.QFile.ReadOnly)
    ui = loader.load(uifile, parent)
    uifile.close()
    return ui



def getMayaMainWindow():
    win = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QWidget)
    return win



# def getWorkspaceParent():
#     if cmds.workspaceControl("NewTest", ex=True):
#         cmds.deleteUI("NewTest")
#
#     mainControl = cmds.workspaceControl("NewTest", iw=275, mw=True, l='NewTest',
#         dtc=['ToolBox', 'right'], wp='preferred', fl=True)
#
#     dock = omui1.MQtUtil.findControl("NewTest")
#     qDock = shiboken2.wrapInstance(long(dock), QtWidgets.QWidget)
#
#     return qDock



# class templateUIDemo(QtWidgets.QMainWindow):
#     def __init__(self):
#         mainUI = UIFILELOC
#         qParent = getMayaMainWindow()
#         super(templateUIDemo, self).__init__(qParent)
#
#         self.MainWindowUI = loadUIWidget(mainUI, qParent)
#         self.MainWindowUI.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
#         self.MainWindowUI.destroyed.connect(self.onExitCode)
#         self.MainWindowUI.show()
#
#     def onExitCode(self):
#         sys.stdout.write("You closed the window!\n")


'''
class dockWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=getMayaMainWindow(), *args, **kwargs):
        super(dockWindow, self).__init__(parent=parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setWindowTitle("dockWindow")

    def dockCloseEventTriggered(self):
        self.close()
        self.deleteLater()



class templateUIDemoDockable(dockWindow):
    def __init__(self, parent=None):
        super(templateUIDemoDockable, self).__init__(parent=parent)



def runDockable():
    app = templateUIDemoDockable()
    app.show(dockable=True, floating=True, area='left', allowedArea='left')
    # app.setDockableParameters(dockable=True, floating=True, area='left', allowedArea='left')
    app.raise_()
'''


class templateUIDemo(QtWidgets.QMainWindow):
    def __init__(self):
        super(templateUIDemo, self).__init__()
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(UIFILELOC)
        file.open(QtCore.QFile.ReadOnly)
        mWin = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QWidget)
        self.MainWindowUI = loader.load(file, mWin)
        file.close()

        self.MainWindowUI.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.MainWindowUI.destroyed.connect(self.onExitCode)
        print(self.MainWindowUI.centralWidget().objectName())
        self.MainWindowUI.show()

    def onExitCode(self):
        sys.stdout.write("You closed the window!\n")



def run():
    if (cmds.window("gfTestMainWindow", ex=True)):
        cmds.deleteUI("gfTestMainWindow")
    app = templateUIDemo()
    # app.show(dockable=True)
    return app



# class templateDock(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
#     DOCK_LABEL_NAME = "gfCustomDock"
#     CONTROL_NAME = "gfCustomDockWin"
#
#     def __init__(self):
#         super(templateDock, self).__init__()
#
#         if cmds.window("%sWorkspaceControl" % templateDock.CONTROL_NAME, ex=True):
#             cmds.deleteUI("%sWorkspaceControl" % templateDock.CONTROL_NAME)
#
#         self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
#
#
#
# class templateUIDemoDockable(templateDock):
#     DOCK_LABEL_NAME = "childTestWindow"
#     CONTROL_NAME = "childTestWindowWin"
#
#     def __init__(self):
#         mainUI = UIFILELOC
#         mMain = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QWidget)
#         super(templateDock, self).__init__(mMain)
#
#         self.MainWindowUI = loadUIWidget(mainUI, mMain)
#         self.MainWindowUI.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
#         self.MainWindowUI.destroyed.connect(self.onExitCode)
#
#     def onExitCode(self):
#         sys.stdout.write("You closed the window!")



# def runDockable():
#     if not (cmds.window("gfTestMainWindow", exists=True)):
#         app = templateUIDemoDockable()
#         app.show(dockable=True)
#         return app
#     else:
#         cmds.deleteUI("gfTestMainWindow")
#         sys.stderr.write("Deu erro ai parca!")


'''
====================================================
990
createCategoryWindow
actionInfoWindow
setupWindow
'''



class MyDockableButton(MayaQWidgetDockableMixin, QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(MyDockableButton, self).__init__(parent=parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred )
        self.setText('Push Me')



class MyDockableWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MyDockableWindow, self).__init__(parent=parent)
        self.setObjectName("gfTestMainWindow")
        self.resize(275, 600)
        self.setStyleSheet("background-color: rgb(85, 170, 0);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 275, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSacanagem = QtWidgets.QMenu(self.menubar)
        self.menuSacanagem.setObjectName("menuSacanagem")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionMeuCU = QtWidgets.QAction(self)
        self.actionMeuCU.setObjectName("actionMeuCU")
        self.actionExit = QtWidgets.QAction(self)
        self.actionExit.setObjectName("actionExit")
        self.action_aqui_mesmo = QtWidgets.QAction(self)
        self.action_aqui_mesmo.setObjectName("action_aqui_mesmo")
        self.menuFile.addAction(self.actionMeuCU)
        self.menuFile.addAction(self.actionExit)
        self.menuSacanagem.addAction(self.action_aqui_mesmo)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSacanagem.menuAction())

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent=parent)
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(UIFILELOC)
        file.open(QtCore.QFile.ReadOnly)
        mWin = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QWidget)
        self.MainWindowUI = loader.load(file, mWin)
        file.close()

        self.MainWindowUI.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.MainWindowUI.destroyed.connect(self.onExitCode)
        print(self.MainWindowUI.centralWidget().objectName())
        # self.MainWindowUI.show()

    def onExitCode(self):
        sys.stdout.write("You closed the window!\n")

def runTest():
    # Show the button as a non-dockable floating window.
    #
    # button = MyDockableButton()
    dock = MyDockableWindow()
    # window = MyWindow(parent=dock)
    dock.show(dockable=True)
    # button.show(dockable=False)

    # showRepr() can be used to display the current dockable settings.
    #
    # print('# ' + button.showRepr())
    # show(dockable=False, height=23, width=70, y=610, x=197, floating=True)

    # Change it to a dockable floating window.
    #
    # button.show(dockable=True)
    # print('# ' + button.showRepr())
    # button.show(dockable=True, area='none', height=23, width=70, y=610, x=197, floating=True)
    # window.show(dockable=False, area='none', height=23, width=70, y=610, x=197, floating=True)
