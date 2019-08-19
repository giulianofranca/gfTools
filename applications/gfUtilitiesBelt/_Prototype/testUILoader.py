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
