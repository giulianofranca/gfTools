import os
import sys
import shiboken2
import maya.OpenMayaUI as omui1
from PySide2 import QtCore, QtWidgets, QtUiTools


class GFCustomTool(object):
    def __init__(self):
        self.TOOL_NAME = "gfCustomTool_1"
        self.TOOLTIP = "NDA"
        self.ICON = ""
        self._checkClass()
        self.computeSingleCommand()
        self.computeDoubleCommand()

    def _checkClass(self):
        if isinstance(self, GFCustomTool):
            print("Tudo certo")
        else:
            print("Inheritance needed.")

    @property
    def mayaWindow(self):
        """
        Name: mayaWindow
        Type: PySide2.QtWidgets.QWidget instance
        Access: R
        Description: Return the Maya main window as PySide2 QWidget object.
        """
        mWin = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QWidget)
        return mWin

    def displayWindow(self, parent=self.mayaWindow):
        """
        Signature: <GFCustomTool>.displayWindow()
        Parameters:
        Returns:
        Description: Run the single click command from the custom tool.
        """
        pass

    def computeSingleCommand(self):
        """
        Signature: <GFCustomTool>.computeSingleCommand()
        Parameters:
        Returns:
        Description: Run the single click command from the custom tool.
        """
        print("Compute Command printed.")

    def computeDoubleCommand(self):
        """
        Signature: <GFCustomTool>.computeDoubleCommand()
        Parameters:
        Returns:
        Description: Run the double click command from the custom tool.
        """
        print("Compute Double Command printed.")
