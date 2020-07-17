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

Layouts:
    * FlowLayout

Todo:
    * NDA

Sources:
    * https://doc.qt.io/qtforpython/overviews/qtwidgets-layouts-flowlayout-example.html

This code supports Pylint. Rc file in project.
"""
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui


class FlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None):
        super(FlowLayout, self).__init__(parent)
        self._hspacing = -1
        self._vspacing = -1
        self._items = []

        self.setContentsMargins(-1, -1, -1, -1)


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
        return None


    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None


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
