# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'radiobtngrp.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widRadioBtnGrp(object):
    def setupUi(self, widRadioBtnGrp):
        widRadioBtnGrp.setObjectName("widRadioBtnGrp")
        widRadioBtnGrp.resize(404, 40)
        self.layWidRadioBtnGrp = QtWidgets.QVBoxLayout(widRadioBtnGrp)
        self.layWidRadioBtnGrp.setContentsMargins(5, 5, 5, 5)
        self.layWidRadioBtnGrp.setSpacing(5)
        self.layWidRadioBtnGrp.setObjectName("layWidRadioBtnGrp")
        self.frmRadioBtnGrp = QtWidgets.QFrame(widRadioBtnGrp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmRadioBtnGrp.sizePolicy().hasHeightForWidth())
        self.frmRadioBtnGrp.setSizePolicy(sizePolicy)
        self.frmRadioBtnGrp.setMinimumSize(QtCore.QSize(0, 30))
        self.frmRadioBtnGrp.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frmRadioBtnGrp.setObjectName("frmRadioBtnGrp")
        self.layRadioBtnGrp = QtWidgets.QHBoxLayout(self.frmRadioBtnGrp)
        self.layRadioBtnGrp.setContentsMargins(5, 5, 5, 5)
        self.layRadioBtnGrp.setSpacing(10)
        self.layRadioBtnGrp.setObjectName("layRadioBtnGrp")
        self.lblRadioBtnGrp = QtWidgets.QLabel(self.frmRadioBtnGrp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblRadioBtnGrp.sizePolicy().hasHeightForWidth())
        self.lblRadioBtnGrp.setSizePolicy(sizePolicy)
        self.lblRadioBtnGrp.setMinimumSize(QtCore.QSize(120, 0))
        self.lblRadioBtnGrp.setMaximumSize(QtCore.QSize(120, 16777215))
        self.lblRadioBtnGrp.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblRadioBtnGrp.setObjectName("lblRadioBtnGrp")
        self.layRadioBtnGrp.addWidget(self.lblRadioBtnGrp)
        self.radRadioBtnGrp1 = QtWidgets.QRadioButton(self.frmRadioBtnGrp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radRadioBtnGrp1.sizePolicy().hasHeightForWidth())
        self.radRadioBtnGrp1.setSizePolicy(sizePolicy)
        self.radRadioBtnGrp1.setChecked(True)
        self.radRadioBtnGrp1.setObjectName("radRadioBtnGrp1")
        self.layRadioBtnGrp.addWidget(self.radRadioBtnGrp1)
        self.radRadioBtnGrp2 = QtWidgets.QRadioButton(self.frmRadioBtnGrp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radRadioBtnGrp2.sizePolicy().hasHeightForWidth())
        self.radRadioBtnGrp2.setSizePolicy(sizePolicy)
        self.radRadioBtnGrp2.setObjectName("radRadioBtnGrp2")
        self.layRadioBtnGrp.addWidget(self.radRadioBtnGrp2)
        self.radRadioBtnGrp3 = QtWidgets.QRadioButton(self.frmRadioBtnGrp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radRadioBtnGrp3.sizePolicy().hasHeightForWidth())
        self.radRadioBtnGrp3.setSizePolicy(sizePolicy)
        self.radRadioBtnGrp3.setObjectName("radRadioBtnGrp3")
        self.layRadioBtnGrp.addWidget(self.radRadioBtnGrp3)
        self.radRadioBtnGrp4 = QtWidgets.QRadioButton(self.frmRadioBtnGrp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radRadioBtnGrp4.sizePolicy().hasHeightForWidth())
        self.radRadioBtnGrp4.setSizePolicy(sizePolicy)
        self.radRadioBtnGrp4.setObjectName("radRadioBtnGrp4")
        self.layRadioBtnGrp.addWidget(self.radRadioBtnGrp4)
        self.layWidRadioBtnGrp.addWidget(self.frmRadioBtnGrp)

        self.retranslateUi(widRadioBtnGrp)
        QtCore.QMetaObject.connectSlotsByName(widRadioBtnGrp)

    def retranslateUi(self, widRadioBtnGrp):
        _translate = QtCore.QCoreApplication.translate
        widRadioBtnGrp.setWindowTitle(_translate("widRadioBtnGrp", "Form"))
        self.lblRadioBtnGrp.setText(_translate("widRadioBtnGrp", "Radio Button Group"))
        self.radRadioBtnGrp1.setText(_translate("widRadioBtnGrp", "Radio1"))
        self.radRadioBtnGrp2.setText(_translate("widRadioBtnGrp", "Radio2"))
        self.radRadioBtnGrp3.setText(_translate("widRadioBtnGrp", "Radio3"))
        self.radRadioBtnGrp4.setText(_translate("widRadioBtnGrp", "Radio4"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widRadioBtnGrp = QtWidgets.QWidget()
    ui = Ui_widRadioBtnGrp()
    ui.setupUi(widRadioBtnGrp)
    widRadioBtnGrp.show()
    sys.exit(app.exec_())

