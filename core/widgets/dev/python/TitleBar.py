# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

====================================================================================================

How to use:
    * Copy the parent folder to the MAYA_SCRIPT_PATH.
    * To find MAYA_SCRIPT_PATH paste this command in a Python tab:
        import os; os.environ["MAYA_SCRIPT_PATH"].split(";")
    * In Maya, go to Windows > Settings/Preferences > Plug-in Manager.
    * Browse for "gfTools > plug-ins > dev > python"
    * Find gfTools_P.py and import it.

Requirements:
    * Maya 2017 or above.

Todo:
    * NDA

Sources:
    * https://www.learnpyqt.com/widgets/
    * https://www.learnpyqt.com/courses/custom-widgets/creating-your-own-custom-widgets/

This code supports Pylint. Rc file in project.
"""
import sys
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

# QtCore: QParallelAnimationGroup, QPropertyAnimation
# https://code-examples.net/it/q/1ef8b66


class GFTitleBar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(GFTitleBar, self).__init__(parent)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Fixed
        )
        self.setMinimumSize(0, 24)
        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        
        self._createTitleLayout()
        # self._createSpacer()
        # self._createCloseButton()


    ########################################################
    # PRIVATE METHODS

    def _createTitleLayout(self):
        self.titleLayout = QtWidgets.QHBoxLayout(self)
        self.titleLayout.setContentsMargins(8, 4, 8, 4)
        self.titleLayout.setSpacing(8)
        self.setLayout(self.titleLayout)

    def _createSpacer(self):
        self.spacer = QtWidgets.QSpacerItem()
        width = self.width() * 0.15
        titleMargins = self.titleLayout.contentsMargins()
        height = self.height() - (titleMargins.top() + titleMargins.bottom())
        self.spacer.changeSize(
            width, height,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.titleLayout.insertWidget(0, self.spacer)

    def _createCloseButton(self):
        self.closeButton = QtWidgets.QPushButton()
        self.closeButton.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        size = self.height()
        self.closeButton.setMinimumSize(size, size)
        self.closeButton.setMaximumSize(size, size)
        self.closeButton.setText("X")
        self.titleLayout.insertWidget(1, self.closeButton)


    ########################################################
    # EVENT METHODS


    ########################################################
    # REGULAR METHODS

    def addButton(self, button):
        pass

    def setTitleMargins(self, left, top, right, bottom):
        self.titleLayout.setContentsMargins(8, 4, 8, 4)

    def setTitleSpacing(self, space):
        self.titleLayout.setSpacing(space)