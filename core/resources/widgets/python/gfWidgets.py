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
    * DialogButton
    * MenuButton
    * SearchButton
    * ListViewButton
    * TabWidget

Sources:
    * https://www.toptal.com/c-plus-plus/rounded-corners-bezier-curves-qpainter
    * https://stackoverflow.com/questions/58248659/how-to-animate-a-qpushbutton-backgrounds-gradient-to-go-from-left-to-right-on-h
    * https://stackoverflow.com/questions/47094871/how-to-custom-qtabwidget-tab?rq=1

This code supports Pylint. Rc file in project.
"""
import math
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

from gfUtilitiesBelt.core import resources
reload(resources)



fonts = [
    ":/gfFonts/WorkSans-Light",
    ":/gfFonts/WorkSans-Medium",
    ":/gfFonts/WorkSans-Regular",
    ":/gfFonts/WorkSans-SemiBold"
]
for font in fonts:
    if font not in QtGui.QFontDatabase().families():
        QtGui.QFontDatabase.addApplicationFont(font)




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
        self._icon = QtGui.QImage(":/gfIcons/gfUtilitiesBelt_python32")
        # self._icon = QtGui.QImage(":menuIconFile.png")
        # self._icon = QtGui.QImage(":polyBevel.png")
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
            raise TypeError("Must set a <ListIconButton.DisplayStyle> object. Default: <ListIconButton.DisplayStyle.kListStyle>")
        if style == ListIconButton.DisplayStyle.kIconStyle:
            self.setFixedSize(self.height(), self.height())
            # TODO: Watch this, may cause errors
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
        iconPos = QtCore.QPoint(self._margin / 2, self._margin / 2)
        iconSize = QtCore.QSize(self.height() - self._margin, self.height() - self._margin)
        iconRect = QtCore.QRect(iconPos, iconSize)
        iconImg = self._icon.scaled(iconSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        iconPix = QtGui.QPixmap.fromImage(iconImg)
        painter.drawPixmap(iconRect, iconPix)

        if self._style == ListIconButton.DisplayStyle.kIconStyle:
            # Draw Text BG
            painter.restore()
            painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50)))
            painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
            textPos = QtCore.QPoint(0, self.height() - (self.height() * 0.35))
            textSize = QtCore.QSize(self.height(), self.height() * 0.35)
            textRect = QtCore.QRect(textPos, textSize)
            painter.drawRoundedRect(textRect, self._radius, self._radius)

            # Draw Text
            painter.restore()
            font = QtGui.QFont()
            font.setPixelSize(10)
            painter.setFont(font)
            painter.setPen(QtGui.QPen(QtGui.QColor(238, 238, 238)))
            textPos = QtCore.QPoint(0, self.height() - (self.height() * 0.35))
            textSize = QtCore.QSize(self.height(), self.height() * 0.35)
            textRect = QtCore.QRect(textPos, textSize)
            painter.drawText(textRect, QtCore.Qt.AlignCenter, self._text)
        else:
            # Draw Text
            painter.restore()
            font = QtGui.QFont()
            font.setFamily("Work Sans SemiBold")
            font.setPixelSize(14)
            painter.setFont(font)
            textPos = QtCore.QPoint(iconSize.width() + (self._margin / 2) + self._margin, self._margin / 2)
            textSize = QtCore.QSize(self.width() - textPos.x() - self._margin, (self.height() / 2) - self._margin / 2)
            textRect = QtCore.QRect(textPos, textSize)
            painter.drawText(textRect, QtCore.Qt.AlignVCenter, self._text)

            # Draw Description
            painter.restore()
            font = QtGui.QFont()
            font.setFamily("Montserrat Regular")
            font.setPixelSize(9)
            painter.setFont(font)
            descPos = QtCore.QPoint(iconSize.width() + (self._margin / 2) + self._margin, textSize.height() + self._margin / 2)
            descSize = QtCore.QSize(self.width() - textPos.x() - self._margin, (self.height() / 2) - self._margin / 2)
            descRect = QtCore.QRect(descPos, descSize)
            painter.drawText(descRect, QtCore.Qt.AlignVCenter, self._description)

        # Draw BG Hover
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, self._alpha)))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        painter.drawRoundedRect(self.rect(), self._radius, self._radius)





class DialogButton(QtWidgets.QPushButton):
    hoverEntered = QtCore.Signal()
    hoverLeaved = QtCore.Signal()
    clicked = QtCore.Signal()
    rightClicked = QtCore.Signal()
    doubleClicked = QtCore.Signal()


    class DisplayStyle(object):
        kMainPriority = 0
        kSecondaryPriority = 1
        kLastPriority = 2

        @staticmethod
        def checkStyle(style):
            if isinstance(style, int):
                if 0 <= style <= 2:
                    return True
            return False


    def __init__(self, text=None, parent=None):
        super(DialogButton, self).__init__(parent)
        self._text = "" if text is None else text
        self._radius = 12
        self._style = DialogButton.DisplayStyle.kSecondaryPriority
        self._color = QtGui.QColor(200, 200, 200)


    def displayStyle(self):
        return self._style


    def setDisplayStyle(self, style):
        if not DialogButton.DisplayStyle.checkStyle(style):
            raise TypeError("Must set a <DialogButton.DisplayStyle> object. Default: <DialogButton.DisplayStyle.kSecondaryPriority>")
        self._style = style


    def text(self):
        return self._text


    def setText(self, text):
        self._text = text


    def color(self):
        return self._color


    def setColor(self, color):
        self._color = color
        self.repaint(self.rect())


    def radius(self):
        return self._radius


    def setRadius(self, radius):
        self._radius = radius
        self.repaint(self.rect())


    def sizeHint(self):
        return QtCore.QSize(120, 40)


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
            return super(DialogButton, self).event(event)
        except Exception:
            return True


    def hoverMoveEvent(self, event):
        if self.rect().contains(event.pos()):
            self.hoverEnterEvent(event)
        else:
            self.hoverLeaveEvent(event)


    def hoverEnterEvent(self, event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.repaint(self.rect())
        self.hoverEntered.emit()


    def hoverLeaveEvent(self, event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
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
        rect = self.rect()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        painter.save()

        fontColor = self._color
        fontFamily = "Work Sans SemiBold"
        gradient = QtGui.QLinearGradient(rect.topLeft(), rect.bottomRight())
        gradient.setColorAt(0, self._color)
        gradient.setColorAt(1, self._color)

        if self._style == DialogButton.DisplayStyle.kMainPriority:
            # Draw BG
            painter.restore()
            painter.setBrush(QtGui.QBrush(gradient))
            painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
            painter.drawRoundedRect(rect, self._radius, self._radius)
            fontColor = QtGui.QColor(255 - self._color.red(), 255 - self._color.green(), 255 - self._color.blue())
        elif self._style == DialogButton.DisplayStyle.kSecondaryPriority:
            # Draw Stroke
            painter.restore()
            painter.setBrush(QtGui.QBrush(QtCore.Qt.NoBrush))
            pen = QtGui.QPen(QtGui.QBrush(gradient), 2)
            painter.setPen(pen)
            pntList = []
            pntList.append(QtCore.QPoint(rect.left() + 1, rect.top() + rect.height() - 1)) # Bottom left
            pntList.append(QtCore.QPoint(rect.left() + rect.width() - 1, rect.top() + rect.height() - 1)) # Bottom right
            pntList.append(QtCore.QPoint(rect.left() + rect.width() - 1, rect.top() + 2)) # Top right
            pntList.append(QtCore.QPoint(rect.left() + 1, rect.top() + 2)) # Top left
            painter.drawPath(self._getPath(pntList))
        else:
            fontFamily = "Work Sans Medium"

        # Draw Text
        painter.restore()
        font = QtGui.QFont()
        font.setPixelSize(14)
        font.setFamily(fontFamily)
        painter.setFont(font)
        painter.setPen(QtGui.QPen(fontColor))
        painter.drawText(rect, QtCore.Qt.AlignCenter, self._text)


    def _getDistance(self, pt1, pt2):
        return math.sqrt(math.pow(pt1.x() - pt2.x(), 2) + math.pow(pt1.y() - pt2.y(), 2))


    def _getLineStart(self, pntList, index):
        pnt1 = pntList[index]
        pnt2 = pntList[(index + 1) % len(pntList)]
        rat = self._radius / self._getDistance(pnt1, pnt2)
        rat = 0.5 if rat > 0.5 else rat
        resPnt = QtCore.QPoint()
        resPnt.setX((1.0 - rat) * pnt1.x() + rat * pnt2.x())
        resPnt.setY((1.0 - rat) * pnt1.y() + rat * pnt2.y())
        return resPnt


    def _getLineEnd(self, pntList, index):
        pnt1 = pntList[index]
        pnt2 = pntList[(index + 1) % len(pntList)]
        rat = self._radius / self._getDistance(pnt1, pnt2)
        rat = 0.5 if rat > 0.5 else rat
        resPnt = QtCore.QPoint()
        resPnt.setX(rat * pnt1.x() + (1.0 - rat) * pnt2.x())
        resPnt.setY(rat * pnt1.y() + (1.0 - rat) * pnt2.y())
        return resPnt


    def _getPath(self, pntList):
        path = QtGui.QPainterPath()
        for i in range(len(pntList)):
            pnt1 = self._getLineStart(pntList, i)
            if i == 0:
                path.moveTo(pnt1)
            else:
                path.quadTo(pntList[i], pnt1)
            pnt2 = self._getLineEnd(pntList, i)
            path.lineTo(pnt2)
        # Close the last corner
        pnt1 = self._getLineStart(pntList, 0)
        path.quadTo(pntList[0], pnt1)
        return path
