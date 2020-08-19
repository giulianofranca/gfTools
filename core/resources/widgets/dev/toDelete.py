import os
import sys
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtUiTools

kPluginPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "gfWidgets_Windows", "Release", "gfWidgets.dll"))
kFilePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "test2.ui"))


class MyWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        loader = QtUiTools.QUiLoader()
        uiFile = QtCore.QFile(kFilePath)
        loader.addPluginPath(os.path.dirname(kPluginPath))
        uiFile.open(QtCore.QIODevice.ReadOnly)
        self.ui = loader.load(uiFile, self)
        uiFile.close()
        print(self.layout())
        print(self.ui.layout())

        self.show()
        self.activateWindow()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MyWin()
    sys.exit(app.exec_())