# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testmainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_gfTestMainWindow(object):
    def setupUi(self, gfTestMainWindow):
        gfTestMainWindow.setObjectName("gfTestMainWindow")
        gfTestMainWindow.resize(275, 600)
        gfTestMainWindow.setStyleSheet("background-color: rgb(85, 170, 0);")
        self.centralwidget = QtWidgets.QWidget(gfTestMainWindow)
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
        gfTestMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(gfTestMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 275, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSacanagem = QtWidgets.QMenu(self.menubar)
        self.menuSacanagem.setObjectName("menuSacanagem")
        gfTestMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(gfTestMainWindow)
        self.statusbar.setObjectName("statusbar")
        gfTestMainWindow.setStatusBar(self.statusbar)
        self.actionMeuCU = QtWidgets.QAction(gfTestMainWindow)
        self.actionMeuCU.setObjectName("actionMeuCU")
        self.actionExit = QtWidgets.QAction(gfTestMainWindow)
        self.actionExit.setObjectName("actionExit")
        self.action_aqui_mesmo = QtWidgets.QAction(gfTestMainWindow)
        self.action_aqui_mesmo.setObjectName("action_aqui_mesmo")
        self.menuFile.addAction(self.actionMeuCU)
        self.menuFile.addAction(self.actionExit)
        self.menuSacanagem.addAction(self.action_aqui_mesmo)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSacanagem.menuAction())

        self.retranslateUi(gfTestMainWindow)
        QtCore.QMetaObject.connectSlotsByName(gfTestMainWindow)

    def retranslateUi(self, gfTestMainWindow):
        _translate = QtCore.QCoreApplication.translate
        gfTestMainWindow.setWindowTitle(_translate("gfTestMainWindow", "MainWindow"))
        self.pushButton.setText(_translate("gfTestMainWindow", "PushButton"))
        self.pushButton_2.setText(_translate("gfTestMainWindow", "PushButton"))
        self.pushButton_3.setText(_translate("gfTestMainWindow", "PushButton"))
        self.menuFile.setTitle(_translate("gfTestMainWindow", "File"))
        self.menuSacanagem.setTitle(_translate("gfTestMainWindow", "Sacanagem"))
        self.actionMeuCU.setText(_translate("gfTestMainWindow", "MeuCU"))
        self.actionExit.setText(_translate("gfTestMainWindow", "Exit"))
        self.action_aqui_mesmo.setText(_translate("gfTestMainWindow", "É aqui mesmo"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    gfTestMainWindow = QtWidgets.QMainWindow()
    ui = Ui_gfTestMainWindow()
    ui.setupUi(gfTestMainWindow)
    gfTestMainWindow.show()
    sys.exit(app.exec_())

