# -*- coding: utf-8 -*-
"""
Copyright 2020 Giuliano Franca

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

====================================================================================================

Widgets:
    * ClickableLabel
    * ListIconButton

Todo:
    * NDA

Sources:
    * NDA

This code supports Pylint. Rc file in project.
"""
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui


class ListIconButton(QtWidgets.QPushButton):
    hoverEntered = QtCore.Signal()
    hoverLeaved = QtCore.Signal()
    clicked = QtCore.Signal()
    rightClicked = QtCore.Signal()
    doubleClicked = QtCore.Signal()


    class DisplayStyle(object):
        kListStyle = 0
        kIconStyle = 1

        @staticmethod
        def checkStyle(style):
            if isinstance(style, int):
                if 0 <= style <= 1:
                    return True
            return False


    def __init__(self, parent=None):
        super(ListIconButton, self).__init__(parent)
        self._icon = QtGui.QImage(":polyBevel.png")
        self._text = "ListIconButton"
        self._description = "Description"
        self._style = ListIconButton.DisplayStyle.kIconStyle
        self._margin = 8
        self._radius = 5
        self._alpha = 0

        self.setMinimumHeight(40)


    def displayStyle(self):
        return self._style


    def setDisplayStyle(self, style):
        if not ListIconButton.DisplayStyle.checkStyle(style):
            raise TypeError("Must set a ListIconButton.DisplayStyle object. Default: ListIconButton.DisplayStyle.kListStyle")
        self._style = style


    def icon(self):
        return self._icon


    def setIcon(self, icon):
        self._icon = icon


    def text(self):
        return self._text


    def setText(self, text):
        self._text = text


    def description(self):
        return self._description


    def setDescription(self, desc):
        self._description = desc


    def margin(self):
        return self._margin


    def setMargin(self, margin):
        self._margin = int(margin)


    def sizeHint(self):
        return QtCore.QSize(40, 40)


    def event(self, event):
        if event.type() == QtCore.QEvent.HoverMove:
            self.hoverMoveEvent(event)
            return True
        elif event.type() == QtCore.QEvent.HoverLeave:
            self.hoverLeaveEvent(event)
            return True
        elif event.type() == QtCore.QEvent.MouseButtonPress:
            self.clickEvent(event)
            return True
        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            self.doubleClickEvent(event)
            return True
        try:
            return super(ListIconButton, self).event(event)
        except Exception:
            return True


    def hoverMoveEvent(self, event):
        if self.rect().contains(event.pos()):
            self.hoverEnterEvent(event)
        else:
            self.hoverLeaveEvent(event)


    def hoverEnterEvent(self, event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self._alpha = 25.5
        self.repaint(self.rect())
        self.hoverEntered.emit()


    def hoverLeaveEvent(self, event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self._alpha = 0
        self.repaint(self.rect())
        self.hoverLeaved.emit()


    def clickEvent(self, event):
        if self.rect().contains(event.pos()):
            if event.button() == QtCore.Qt.RightButton:
                self.rightClicked.emit()
            elif event.button() == QtCore.Qt.LeftButton:
                self.clicked.emit()


    def doubleClickEvent(self, event):
        if self.rect().contains(event.pos()):
            if event.button() == QtCore.Qt.LeftButton:
                self.doubleClicked.emit()

    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        painter.save()

        # Draw BG
        painter.setBrush(QtGui.QBrush(QtGui.QColor(80, 80, 80)))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        painter.drawRoundedRect(self.rect(), self._radius, self._radius)

        # Draw Icon
        painter.restore()
        iconPos = QtCore.QPoint((self._margin / 2), self._margin / 2)
        iconSize = QtCore.QSize(self.height() - self._margin, self.height() - self._margin)
        iconRect = QtCore.QRect(iconPos, iconSize)
        iconImg = self._icon.scaled(iconSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        iconPix = QtGui.QPixmap.fromImage(iconImg)
        painter.drawPixmap(iconRect, iconPix)
        # painter.drawRect(iconRect)

        # Draw Text
        painter.restore()
        font = QtGui.QFont()
        font.setPixelSize(14)
        font.setBold(True)
        painter.setFont(font)
        textSpacing = 0
        textPos = QtCore.QPoint(iconSize.width() + (self._margin / 2) + self._margin, self._margin / 2)
        textSize = QtCore.QSize(self.width() - textPos.x() - self._margin, (self.height() / 2) - self._margin / 2)
        textRect = QtCore.QRect(textPos, textSize)
        painter.drawText(textRect, QtCore.Qt.AlignVCenter, self._text)
        # painter.drawRect(textRect)

        # Draw Description
        painter.restore()
        font = QtGui.QFont()
        font.setPixelSize(9)
        painter.setFont(font)
        descPos = QtCore.QPoint(iconSize.width() + (self._margin / 2) + self._margin, textSize.height() + self._margin / 2)
        descSize = QtCore.QSize(self.width() - textPos.x() - self._margin, (self.height() / 2) - self._margin / 2)
        descRect = QtCore.QRect(descPos, descSize)
        painter.drawText(descRect, QtCore.Qt.AlignVCenter, self._description)
        # painter.drawRect(descRect)

        # Draw BG Hover
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, self._alpha)))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        painter.drawRoundedRect(self.rect(), self._radius, self._radius)
