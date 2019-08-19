# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'intslider.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widIntSlider(object):
    def setupUi(self, widIntSlider):
        widIntSlider.setObjectName("widIntSlider")
        widIntSlider.resize(400, 40)
        self.layWidIntSlider = QtWidgets.QVBoxLayout(widIntSlider)
        self.layWidIntSlider.setContentsMargins(5, 5, 5, 5)
        self.layWidIntSlider.setSpacing(5)
        self.layWidIntSlider.setObjectName("layWidIntSlider")
        self.frmIntSlider = QtWidgets.QFrame(widIntSlider)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmIntSlider.sizePolicy().hasHeightForWidth())
        self.frmIntSlider.setSizePolicy(sizePolicy)
        self.frmIntSlider.setMinimumSize(QtCore.QSize(0, 30))
        self.frmIntSlider.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frmIntSlider.setObjectName("frmIntSlider")
        self.layIntSlider = QtWidgets.QHBoxLayout(self.frmIntSlider)
        self.layIntSlider.setContentsMargins(5, 5, 5, 5)
        self.layIntSlider.setSpacing(10)
        self.layIntSlider.setObjectName("layIntSlider")
        self.lblIntSlider = QtWidgets.QLabel(self.frmIntSlider)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblIntSlider.sizePolicy().hasHeightForWidth())
        self.lblIntSlider.setSizePolicy(sizePolicy)
        self.lblIntSlider.setMinimumSize(QtCore.QSize(120, 0))
        self.lblIntSlider.setMaximumSize(QtCore.QSize(120, 16777215))
        self.lblIntSlider.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblIntSlider.setObjectName("lblIntSlider")
        self.layIntSlider.addWidget(self.lblIntSlider)
        self.txtIntSlider = QtWidgets.QLineEdit(self.frmIntSlider)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtIntSlider.sizePolicy().hasHeightForWidth())
        self.txtIntSlider.setSizePolicy(sizePolicy)
        self.txtIntSlider.setMinimumSize(QtCore.QSize(60, 0))
        self.txtIntSlider.setMaximumSize(QtCore.QSize(60, 16777215))
        self.txtIntSlider.setObjectName("txtIntSlider")
        self.layIntSlider.addWidget(self.txtIntSlider)
        self.sldIntSlider = QtWidgets.QSlider(self.frmIntSlider)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sldIntSlider.sizePolicy().hasHeightForWidth())
        self.sldIntSlider.setSizePolicy(sizePolicy)
        self.sldIntSlider.setMinimumSize(QtCore.QSize(100, 0))
        self.sldIntSlider.setOrientation(QtCore.Qt.Horizontal)
        self.sldIntSlider.setObjectName("sldIntSlider")
        self.layIntSlider.addWidget(self.sldIntSlider)
        self.layWidIntSlider.addWidget(self.frmIntSlider)

        self.retranslateUi(widIntSlider)
        QtCore.QMetaObject.connectSlotsByName(widIntSlider)

    def retranslateUi(self, widIntSlider):
        _translate = QtCore.QCoreApplication.translate
        widIntSlider.setWindowTitle(_translate("widIntSlider", "Form"))
        self.lblIntSlider.setText(_translate("widIntSlider", "Integer slider"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widIntSlider = QtWidgets.QWidget()
    ui = Ui_widIntSlider()
    ui.setupUi(widIntSlider)
    widIntSlider.show()
    sys.exit(app.exec_())
