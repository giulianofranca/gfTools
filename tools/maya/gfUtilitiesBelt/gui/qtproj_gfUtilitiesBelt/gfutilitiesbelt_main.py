# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gfutilitiesbelt_main.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import sys
from PySide2 import QtCore, QtGui, QtWidgets
from maya import cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

class Ui_gfutilitiesbelt_mainUI(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.CONTROL_NAME = "gfutilitiesbelt_mainUI"
        super(Ui_gfutilitiesbelt_mainUI, self).__init__(parent=parent)
        if cmds.workspaceControl(self.CONTROL_NAME + 'WorkspaceControl', ex=True):
            cmds.deleteUI(self.CONTROL_NAME + 'WorkspaceControl')
        self.setupUi()

    def setupUi(self):
        self.setObjectName(self.CONTROL_NAME)
        self.resize(250, 600)
        self.setMinimumSize(QtCore.QSize(200, 300))
        self.wdg_central = QtWidgets.QWidget(self)
        self.wdg_central.setObjectName("wdg_central")
        self.lay_central = QtWidgets.QVBoxLayout(self.wdg_central)
        self.lay_central.setContentsMargins(1, 1, 1, 1)
        self.lay_central.setSpacing(1)
        self.lay_central.setObjectName("lay_central")
        self.wdg_settingsArea = QtWidgets.QWidget(self.wdg_central)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wdg_settingsArea.sizePolicy().hasHeightForWidth())
        self.wdg_settingsArea.setSizePolicy(sizePolicy)
        self.wdg_settingsArea.setMinimumSize(QtCore.QSize(0, 18))
        self.wdg_settingsArea.setStyleSheet("")
        self.wdg_settingsArea.setObjectName("wdg_settingsArea")
        self.lay_settingsArea = QtWidgets.QHBoxLayout(self.wdg_settingsArea)
        self.lay_settingsArea.setContentsMargins(1, 1, 1, 1)
        self.lay_settingsArea.setSpacing(3)
        self.lay_settingsArea.setObjectName("lay_settingsArea")
        self.btn_iconView = QtWidgets.QPushButton(self.wdg_settingsArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_iconView.sizePolicy().hasHeightForWidth())
        self.btn_iconView.setSizePolicy(sizePolicy)
        self.btn_iconView.setMinimumSize(QtCore.QSize(25, 20))
        self.btn_iconView.setMaximumSize(QtCore.QSize(25, 20))
        self.btn_iconView.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_iconView.setStyleSheet("background-color: transparent;\n"
"border: None;")
        self.btn_iconView.setObjectName("btn_iconView")
        self.lay_settingsArea.addWidget(self.btn_iconView)
        self.btn_listView = QtWidgets.QPushButton(self.wdg_settingsArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_listView.sizePolicy().hasHeightForWidth())
        self.btn_listView.setSizePolicy(sizePolicy)
        self.btn_listView.setMinimumSize(QtCore.QSize(25, 20))
        self.btn_listView.setMaximumSize(QtCore.QSize(25, 20))
        self.btn_listView.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_listView.setStyleSheet("background-color: transparent;\n"
"border: None;")
        self.btn_listView.setObjectName("btn_listView")
        self.lay_settingsArea.addWidget(self.btn_listView)
        spacerItem = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lay_settingsArea.addItem(spacerItem)
        self.btn_addPocket = QtWidgets.QPushButton(self.wdg_settingsArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_addPocket.sizePolicy().hasHeightForWidth())
        self.btn_addPocket.setSizePolicy(sizePolicy)
        self.btn_addPocket.setMinimumSize(QtCore.QSize(70, 20))
        self.btn_addPocket.setMaximumSize(QtCore.QSize(70, 20))
        self.btn_addPocket.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_addPocket.setStyleSheet("background-color: transparent;\n"
"border: None;")
        self.btn_addPocket.setIconSize(QtCore.QSize(70, 20))
        self.btn_addPocket.setObjectName("btn_addPocket")
        self.lay_settingsArea.addWidget(self.btn_addPocket)
        self.lay_central.addWidget(self.wdg_settingsArea)
        self.tbw_pocketArea = QtWidgets.QTabWidget(self.wdg_central)
        self.tbw_pocketArea.setTabsClosable(True)
        self.tbw_pocketArea.setObjectName("tbw_gfPocketArea")
        # self.tab_home = QtWidgets.QWidget()
        # self.tab_home.setObjectName("tab_home")
        # self.lay_home = QtWidgets.QVBoxLayout(self.tab_home)
        # self.lay_home.setContentsMargins(1, 1, 1, 1)
        # self.lay_home.setSpacing(1)
        # self.lay_home.setObjectName("lay_home")
        # self.lbl_home = QtWidgets.QLabel(self.tab_home)
        # font = QtGui.QFont()
        # font.setPointSize(14)
        # self.lbl_home.setFont(font)
        # self.lbl_home.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # self.lbl_home.setToolTip("")
        # self.lbl_home.setAlignment(QtCore.Qt.AlignCenter)
        # self.lbl_home.setObjectName("lbl_home")
        # self.lay_home.addWidget(self.lbl_home)
        # self.tbw_pocketArea.addTab(self.tab_home, "")
        self.lay_central.addWidget(self.tbw_pocketArea)
        self.setCentralWidget(self.wdg_central)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, gfutilitiesbelt_mainUI):
        _translate = QtCore.QCoreApplication.translate
        gfutilitiesbelt_mainUI.setWindowTitle(_translate("gfutilitiesbelt_mainUI", "gfUtilitiesBelt"))
        self.btn_iconView.setText(_translate("gfutilitiesbelt_mainUI", "[:]"))
        self.btn_listView.setText(_translate("gfutilitiesbelt_mainUI", "="))
        self.btn_addPocket.setText(_translate("gfutilitiesbelt_mainUI", "Add"))
        # self.lbl_home.setText(_translate("gfutilitiesbelt_mainUI", "<html><head/><body><p>Hey buddy! </p><p>May I help you?</p></body></html>"))
        # self.tbw_pocketArea.setTabText(self.tbw_pocketArea.indexOf(self.tab_home), _translate("gfutilitiesbelt_mainUI", "Home"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     gfutilitiesbelt_mainUI = QtWidgets.QMainWindow()
#     ui = Ui_gfutilitiesbelt_mainUI()
#     ui.setupUi(gfutilitiesbelt_mainUI)
#     gfutilitiesbelt_mainUI.show()
#     sys.exit(app.exec_())
