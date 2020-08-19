import sys
from PySide2 import QtCore, QtGui, QtWidgets



class FlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, margin=-1, hspacing=-1, vspacing=-1):
        super(FlowLayout, self).__init__(parent)
        self._hspacing = hspacing
        self._vspacing = vspacing
        self._items = []
        self.setContentsMargins(margin, margin, margin, margin)

    def __del__(self):
        del self._items[:]

    def addItem(self, item):
        self._items.append(item)

    def horizontalSpacing(self):
        if self._hspacing >= 0:
            return self._hspacing
        else:
            return self.smartSpacing(QtWidgets.QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self._vspacing >= 0:
            return self._vspacing
        else:
            return self.smartSpacing(QtWidgets.QStyle.PM_LayoutVerticalSpacing)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)

    def expandingDirections(self):
        return QtCore.Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QtCore.QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QtCore.QSize(left + right, top + bottom)
        return size

    def doLayout(self, rect, testonly):
        left, top, right, bottom = self.getContentsMargins()
        effective = rect.adjusted(+left, +top, -right, -bottom)
        x = effective.x()
        y = effective.y()
        lineHeight = 0
        for item in self._items:
            widget = item.widget()
            hspace = self.horizontalSpacing()
            if hspace == -1:
                hspace = widget.style().layoutSpacing(
                    QtWidgets.QSizePolicy.PushButton,
                    QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Horizontal
                )
            vspace = self.verticalSpacing()
            if vspace == -1:
                vspace = widget.style().layoutSpacing(
                    QtWidgets.QSizePolicy.PushButton,
                    QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Vertical
                )
            nextX = x + item.sizeHint().width() + hspace
            if nextX - hspace > effective.right() and lineHeight > 0:
                x = effective.x()
                y = y + lineHeight + vspace
                nextX = x + item.sizeHint().width() + hspace
                lineHeight = 0
            if not testonly:
                item.setGeometry(
                    QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint())
                )
            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())
        return y + lineHeight - rect.y() + bottom

    def smartSpacing(self, pm):
        parent = self.parent()
        if parent is None:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()



class UtilitiesButton(QtWidgets.QPushButton):
    # doubleClicked = QtCore.Slot()
    # clicked = QtCore.Slot()

    def __init__(self, parent=None):
        super(UtilitiesButton, self).__init__(parent=parent)
        self.image = QtGui.QImage(":pythonFamily.png")
        self.hover = False

        self.config()


    def config(self):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(35, 35))
        self.setMaximumSize(QtCore.QSize(35, 35))
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setIconSize(self.size())
        self.setMouseTracking(True)
        # super().clicked.connect(self.checkDoubleClick)

    def mouseDoubleClickEvent(self, event):
        self.emit(doubleClicked())

    # @QtCore.Slot()
    # def checkDoubleClick(self):
    #     if self.timer.isActive():
    #         self.doubleClicked.emit()
    #         self.timer.stop()
    #     else:
    #         self.timer.start(250)

    def setImage(self, image):
        image = QtGui.QImage(image)
        self.image = image

    def enterEvent(self, event):
        self.hover = True

    def leaveEvent(self, event):
        self.hover = False

    def paintEvent(self, event):
        p = QtGui.QPainter()
        p.begin(self)
        bgColor = QtGui.QColor(74, 74, 74)
        textBackground = QtGui.QColor(30, 30, 30)
        textColor = QtGui.QColor(240, 240, 240)
        hoverColor = QtGui.QColor(255, 255, 255, 40)
        # Background
        p.fillRect(self.rect(), bgColor)
        # Icon
        p.drawImage(self.rect(), self.image)
        # Hover Effect
        if self.hover:
            p.fillRect(self.rect(), hoverColor)
        # Text Background
        if self.text() != "":
            textBGRect = QtCore.QRect(0, 21, 35, 14)
            p.fillRect(textBGRect, textBackground)
        # Text
        if self.text() != "":
            font = QtGui.QFont()
            font.setPointSize(8)
            fm = QtGui.QFontMetrics(font)
            w = (self.width() - fm.width(self.text())) / 2
            h = self.height() - 3
            p.setPen(textColor)
            p.setFont(font)
            p.drawText(QtCore.QPoint(w, h), self.text())
        p.end()



class PreviewButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(PreviewButton, self).__init__(parent=parent)
        self.image = QtGui.QImage(":pythonFamily.png")

        self.config()


    def config(self):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(28, 28))
        self.setMaximumSize(QtCore.QSize(28, 28))
        self.setIconSize(self.size())
        self.setMouseTracking(True)

    def setImage(self, image):
        image = QtGui.QImage(image)
        self.image = image

    def paintEvent(self, event):
        p = QtGui.QPainter()
        p.begin(self)
        bgColor = QtGui.QColor(44, 44, 44)
        textBackground = QtGui.QColor(30, 30, 30)
        textColor = QtGui.QColor(240, 240, 240)
        hoverColor = QtGui.QColor(255, 255, 255, 40)
        # Background
        p.fillRect(self.rect(), bgColor)
        # Icon
        p.drawImage(self.rect(), self.image)
        # Text Background
        if self.text() != "":
            textBGRect = QtCore.QRect(0, 16, 28, 12)
            p.fillRect(textBGRect, textBackground)
        # Text
        if self.text() != "":
            font = QtGui.QFont()
            font.setPointSize(7)
            fm = QtGui.QFontMetrics(font)
            w = (self.width() - fm.width(self.text())) / 2
            h = self.height() - 2
            p.setPen(textColor)
            p.setFont(font)
            p.drawText(QtCore.QPoint(w, h), self.text())
        p.end()



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, text, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.mainArea = QtWidgets.QScrollArea(self)
        self.mainArea.setWidgetResizable(True)
        widget = QtWidgets.QWidget(self.mainArea)
        widget.setMinimumWidth(50)
        layout = FlowLayout(widget)
        self.words = []
        for word in text.split():
            btn = UtilitiesButton()
            btn.setImage(":menuIconFile.png") # menuIconFile.png | kinJoint.png
            btn.setText("OSS")
            btn.setToolTip("Test")
            self.words.append(btn)
            layout.addWidget(btn)
        self.mainArea.setWidget(widget)
        self.setCentralWidget(self.mainArea)


# app = QtWidgets.QApplication(sys.argv)
# window = MainWindow('Harry Potter is a series of fantasy literature')
# window.show()
# sys.exit(app.exec_())
