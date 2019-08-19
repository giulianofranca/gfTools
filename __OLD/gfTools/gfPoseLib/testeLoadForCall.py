import shiboken2
from PySide2 import QtWidgets, QtCore
from maya import cmds
from maya import OpenMayaUI as omui

# from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
# from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


import testeLoad as uiClass
reload(uiClass)


class UI_Funcs(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        # super(UI_Funcs, self).__init__(parent)
        # self.setWindowFlags(QtCore.Qt.Tool)
        self.ui = uiClass.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
