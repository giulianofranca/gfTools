import sys
from PySide2 import QtWidgets, QtCore, QtGui

class MyCheckBox(QtWidgets.QCheckBox):

    def __init__(self, *args, **kwargs):
        super(MyCheckBox, self).__init__()
        self.setStyleSheet("background-color:rgb(0, 0, 0);\n"+
            "color: rgb(255, 255, 255);\n")
        self.setChecked(True)
        self.setEnabled(True)
        self._enable = True

    def mousePressEvent(self, *args, **kwargs):
        if self.isChecked():
            self.setChecked(False)
        else:
            self.setChecked(True)
        return QtWidgets.QCheckBox.mousePressEvent(self, *args, **kwargs)

    def paintEvent(self, event):
        # Just setting some size aspects
        self.setMinimumHeight(40)
        self.setMinimumWidth(100)
        self.setMaximumHeight(50)
        self.setMaximumWidth(150)

        self.resize(self.parent().width(), self.parent().height()) # Aqui vai dar pau
        painter = QtGui.QPainter()
        painter.begin(self)

        # For the black background
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0), style=QtCore.Qt.SolidPattern)
        painter.fillRect(self.rect(), brush)

        # Smooth curves
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # For the on off font
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPixelSize(18)
        painter.setFont(font)

        # Change the look of on/off
        if self.isChecked():
            # Blue Fill
            brush = QtGui.QBrush(QtGui.QColor(50, 50, 255), style=QtCore.Qt.SolidPattern)
            painter.setBrush(brush)

            # Rounded rectangle as a whole
            painter.drawRoundedRect(0, 0, self.width()-2, self.height()-2, self.height()/2, self.height()/2)

            # White circle/button instead of the thick mark
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255), style=QtCore.Qt.SolidPattern)
            painter.setBrush(brush)
            painter.drawEllipse(self.width()-self.height(), 0, self.height(), self.height())

            # On text
            painter.drawText(self.width()/4, self.height()/1.5, "On")

        else:
            # Gray Fill
            brush = QtGui.QBrush(QtGui.QColor(50, 50, 50), style=QtCore.Qt.SolidPattern)
            painter.setBrush(brush)

            # Rounded rectangle as a whole
            painter.drawRoundedRect(0, 0, self.width()-2, self.height()-2, self.height()/2, self.height()/2)

            # White circle/button instead of the thick but in different location
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255), style=QtCore.Qt.SolidPattern)
            painter.setBrush(brush)
            painter.drawEllipse(0, 0, self.height(), self.height())

            # Off text
            painter.drawText(self.width()/2, self.height()/1.5, "Off")

        painter.end()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    wgt = QtWidgets.QWidget()
    wgt.setStyleSheet("background-color: rgb(0, 0, 0);\n")
    cb = MyCheckBox()
    cb.setParent(wgt)
    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(cb)
    wgt.resize(200, 100)
    wgt.show()
    sys.exit(app.exec_())
