import sys
import os
import shiboken2
import maya.cmds as cmds
import maya.OpenMayaUI as omui1
from functools import partial
from PySide2 import QtCore, QtGui, QtWidgets, QtUiTools
from maya.api import OpenMaya as om2


SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
MAIN_UI_PATH = os.path.join(SCRIPT_PATH, "gui", "qtproj_gfUtilitiesBelt", "gfutilitiesbelt_main.ui")
ADDPOCKET_UI_PATH = os.path.join(SCRIPT_PATH, "gui", "qtproj_gfUtilitiesBelt", "gfutilitiesbelt_addpocket.ui")
EDITPOCKET_UI_PATH = os.path.join(SCRIPT_PATH, "gui", "qtproj_gfUtilitiesBelt", "gfUtilitiesBelt_editpocket.ui")
CREATETOOL_UI_PATH = os.path.join(SCRIPT_PATH, "gui", "qtproj_gfUtilitiesBelt", "gfUtilitiesBelt_createtool.ui")


class MainUI_Win_DEV(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainUI_Win_DEV, self).__init__(parent=parent)
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(MAIN_UI_PATH)
        file.open(QtCore.QFile.ReadOnly)
        mWin = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QWidget)
        self.ui = loader.load(file, mWin)
        file.close()

        self.ui.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.ui.setWindowFlags(QtCore.Qt.Tool)
        self.ui.destroyed.connect(self.onExitCode)
        self.ui.show()

    def onExitCode(self):
        sys.stdout.write("Window closed!\n")



class AddPocketUI_Win_DEV(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddPocketUI_Win_DEV, self).__init__(parent=parent)
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(ADDPOCKET_UI_PATH)
        file.open(QtCore.QFile.ReadOnly)
        mWin = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QWidget)
        self.ui = loader.load(file, mWin)
        file.close()

        self.ui.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        # self.ui.setWindowFlags(QtCore.Qt.Tool)
        self.ui.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowMinimizeButtonHint |
                               QtCore.Qt.WindowCloseButtonHint)
        self.ui.show()



class EditPocketUI_Win_DEV(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(EditPocketUI_Win_DEV, self).__init__(parent=parent)
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(EDITPOCKET_UI_PATH)
        file.open(QtCore.QFile.ReadOnly)
        mWin = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QWidget)
        self.ui = loader.load(file, mWin)
        file.close()

        self.ui.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.ui.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowMinimizeButtonHint |
                               QtCore.Qt.WindowCloseButtonHint)
        self.ui.show()



class CreatePocketUI_Win_DEV(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CreatePocketUI_Win_DEV, self).__init__(parent=parent)
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(CREATETOOL_UI_PATH)
        file.open(QtCore.QFile.ReadOnly)
        mWin = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QWidget)
        self.ui = loader.load(file, mWin)
        file.close()

        self.ui.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.ui.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowMinimizeButtonHint |
                               QtCore.Qt.WindowCloseButtonHint)
        self.ui.show()



def main_DEV():
    if (cmds.window("gfutilitiesbelt_mainUI", ex=True)):
        cmds.deleteUI("gfutilitiesbelt_mainUI")
    app = MainUI_Win_DEV()

def addPocket_DEV():
    if (cmds.window("gfUtilitiesBelt_addPocketUI", ex=True)):
        cmds.deleteUI("gfUtilitiesBelt_addPocketUI")
    app = AddPocketUI_Win_DEV()

def editPocket_DEV():
    if (cmds.window("gfUtilitiesBelt_editPocketUI", ex=True)):
        cmds.deleteUI("gfUtilitiesBelt_editPocketUI")
    app = EditPocketUI_Win_DEV()

def createTool_DEV():
    if (cmds.window("gfUtilitiesBelt_createToolUI", ex=True)):
        cmds.deleteUI("gfUtilitiesBelt_createToolUI")
    app = CreatePocketUI_Win_DEV()



"""
================================================================================================================================================
"""
from gfUtilitiesBelt.core import coreFuncs as core
from gfUtilitiesBelt.core import fileManagement as fileM
reload(core)
reload(fileM)

from gftoolsdevelopment.core import widgets as gfWidgets

from gfUtilitiesBelt.gui.qtproj_gfUtilitiesBelt import gfutilitiesbelt_main as gfMainWin
from gfUtilitiesBelt.gui.qtproj_gfUtilitiesBelt import gfutilitiesbelt_addpocket as gfAddWin
from gfUtilitiesBelt.gui.qtproj_gfUtilitiesBelt import gfutilitiesbelt_editpocket as gfEditWin
reload(gfWidgets)
reload(gfMainWin)
reload(gfAddWin)
reload(gfEditWin)


class EditUI_Win(gfEditWin.Ui_gfutilitiesbelt_editpocketUI):
    def __init__(self, name):
        mWin = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QWidget)
        super(EditUI_Win, self).__init__(parent=mWin)
        self.name = name
        self.pocketName = "%s.gfPocket" % self.name
        self.ADDED_TOOL_COLOR = QtGui.QColor(0, 255, 0)
        self.NON_ADDED_TOOL_COLOR = QtGui.QColor(190, 190, 190)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.connectSlots()
        self.fillCategories()

    def start(self):
        self.show()

    def connectSlots(self):
        self.lbl_pocketName.setText("%s    " % self.pocketName)
        self.btn_cancel.clicked.connect(lambda: self.close())
        self.btn_addTool.clicked.connect(self.addToolToPocket)
        self.btn_removeTool.clicked.connect(self.removeToolToPocket)
        self.btn_edit.clicked.connect(self.editPocket)
        self.cmb_categories.currentIndexChanged.connect(self.changeCategory)

    def importPocket(self):
        try:
            path = os.path.join(fileM.POCKETS_PATH, self.pocketName)
            pocketTools = core.readPocket(path)
        except:
            sys.stderr.write("File is from an older version.\n")
            self.close()
            return
        mayaData = core.getMayaData()
        for tool in pocketTools:
            if tool in mayaData.keys():
                btn = gfWidgets.PreviewButton()
                btn.setObjectName("preview_%s" % tool)
                if mayaData[tool]["imageLabel"] != "":
                    btn.setText(mayaData[tool]["imageLabel"])
                btn.setImage(":%s" % mayaData[tool]["icon"])
                btn.setToolTip(mayaData[tool]["name"])
                self.lay_flow.addWidget(btn)
        for i in range(self.lst_tools.count()):
            item = self.lst_tools.item(i)
            if item.toolTip() in pocketTools:
                brush = QtGui.QBrush()
                brush.setColor(self.ADDED_TOOL_COLOR)
                item.setForeground(brush)
            # else:
            #     sys.stderr.write("Tool [%s] not recognized.\n" % key)

    def fillCategories(self):
        mayaData = core.getMayaData()
        categories = []
        for key, value in mayaData.items():
            toolName = value["name"]
            category = value["category"]
            if category not in categories:
                categories.append(category)
                self.cmb_categories.addItem(category)
        self.cmb_categories.addItem("Custom Tools")
        # Add Preview Layout
        self.scr_previewArea = QtWidgets.QScrollArea(self.wdg_previewArea)
        self.scr_previewArea.setObjectName("scr_previewArea")
        self.scr_previewArea.setWidgetResizable(True)
        self.scr_previewArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.wdg_scrPreviewArea = QtWidgets.QWidget(self.scr_previewArea)
        self.wdg_scrPreviewArea.setObjectName("wdg_scrPreviewArea")
        self.wdg_scrPreviewArea.setStyleSheet("background-color: rgb(40, 40, 40);")
        self.lay_flow = gfWidgets.FlowLayout(self.wdg_scrPreviewArea, hspacing=5, vspacing=5)
        self.lay_flow.setObjectName("lay_flowPreviewArea")
        self.lay_flow.setContentsMargins(5, 5, 5, 5)
        self.lay_flow.setSpacing(1)
        self.scr_previewArea.setWidget(self.wdg_scrPreviewArea)
        self.lay_previewArea.addWidget(self.scr_previewArea)
        self.importPocket()

    def checkAddedTools(self):
        mayaData = core.getMayaData()
        items = []
        names = []
        length = self.lay_flow.count()
        for index in range(length):
            layItem = self.lay_flow.itemAt(index)
            item = layItem.widget()
            name = item.objectName().split("preview_")[1]
            for key, value in mayaData.items():
                if key == name:
                    items.append(item)
                    names.append(key)
        return items, names

    def changeCategory(self):
        self.lst_tools.clear()
        mayaData = core.getMayaData()
        try:
            addedTools = self.checkAddedTools()[1]
        except:
            pass
        name = self.cmb_categories.currentText()
        for key, value in mayaData.items():
            toolName = key.split("|")
            toolName.pop(0)
            toolName = ' | '.join(toolName)
            category = value["category"]
            if category == name:
                self.lst_tools.addItem(toolName)
                curIndex = self.lst_tools.count() - 1
                item = self.lst_tools.item(curIndex)
                try:
                    if key in addedTools:
                        brush = QtGui.QBrush()
                        brush.setColor(self.ADDED_TOOL_COLOR)
                        item.setForeground(brush)
                    else:
                        brush = QtGui.QBrush()
                        brush.setColor(self.NON_ADDED_TOOL_COLOR)
                        item.setForeground(brush)
                except:
                    brush = QtGui.QBrush()
                    brush.setColor(self.NON_ADDED_TOOL_COLOR)
                    item.setForeground(brush)
                item.setIcon(QtGui.QIcon(":%s" % value["icon"]))
                item.setToolTip(key)

    def addToolToPocket(self):
        mayadata = core.getMayaData()
        selTools = []
        for tool in self.lst_tools.selectedItems():
            brush = QtGui.QBrush()
            brush.setColor(self.ADDED_TOOL_COLOR)
            tool.setForeground(brush)
            selTools.append(tool.toolTip())
        added = self.checkAddedTools()[1]
        for key, value in mayadata.items():
            if key in selTools:
                if key not in added:
                    btn = gfWidgets.PreviewButton()
                    btn.setObjectName("preview_%s" % key)
                    if value["imageLabel"] != "":
                        btn.setText(value["imageLabel"])
                    btn.setImage(":%s" % value["icon"])
                    btn.setToolTip(value["name"])
                    self.lay_flow.addWidget(btn)
                    for i in range(self.lst_tools.count()):
                        item = self.lst_tools.item(i)
                        self.lst_tools.setItemSelected(item, False)
                else:
                    sys.stderr.write("Tool [%s] already added.\n" % key)

    def removeToolToPocket(self):
        addedItems, addedNames = self.checkAddedTools()
        selTools = []
        for tool in self.lst_tools.selectedItems():
            brush = QtGui.QBrush()
            brush.setColor(self.NON_ADDED_TOOL_COLOR)
            tool.setForeground(brush)
            selTools.append(tool.toolTip())
        for sel in selTools:
            if sel in addedNames:
                length = self.lay_flow.count()
                for index in range(length):
                    layItem = self.lay_flow.itemAt(index)
                    try:
                        item = layItem.widget()
                        name = item.objectName().split("preview_")[1]
                        if sel == name:
                            self.lay_flow.removeWidget(item)
                            item.deleteLater()
                        for i in range(self.lst_tools.count()):
                            item = self.lst_tools.item(i)
                            self.lst_tools.setItemSelected(item, False)
                    except:
                        pass

    def editPocket(self):
        tools = []
        length = self.lay_flow.count()
        for index in range(length):
            layItem = self.lay_flow.itemAt(index)
            item = layItem.widget()
            name = item.objectName().split("preview_")[1]
            tools.append(name)
        core.editTab(name=self.name, tools=tools)

        self.close()



class AddUI_Win(gfAddWin.Ui_gfutilitiesbelt_addpocketUI):
    def __init__(self):
        mWin = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QWidget)
        super(AddUI_Win, self).__init__(parent=mWin)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.connectSlots()

    def start(self):
        self.show()

    def connectSlots(self):
        self.btn_cancel.clicked.connect(lambda: self.close())
        self.btn_create.clicked.connect(self.createTab)
        self.btn_import.clicked.connect(self.importPocket)
        self.btn_cancelImport.clicked.connect(self.clearImport)

    def createTab(self):
        name = self.txt_name.text()
        if name == "":
            sys.stderr.write("Please type any name.\n")
        else:
            core.advancedCreateTab(name=name)
            self.close()

    def importPocket(self):
        try:
            name, fileName, tools = core.importPocket()
        except:
            sys.stderr.write("File is from an older version.\n")
            return
        self.lst_tools.clear()
        mayaData = core.getMayaData()
        for tool in tools:
            if tool in mayaData.keys():
                toolName = tool.split("|")
                toolName.pop(0)
                toolName = ' | '.join(toolName)
                self.lst_tools.addItem(toolName)
                curIndex = self.lst_tools.count() - 1
                item = self.lst_tools.item(curIndex)
                item.setIcon(QtGui.QIcon(":%s" % mayaData[tool]["icon"]))
                item.setToolTip(tool)
        self.lbl_importedFile.setText(fileName)
        self.btn_cancelImport.setEnabled(True)
        self.txt_name.setText(name)

    def clearImport(self):
        self.lbl_importedFile.setText("")
        self.lst_tools.clear()
        self.btn_cancelImport.setEnabled(False)


class MainUI_Win(gfMainWin.Ui_gfutilitiesbelt_mainUI):
    def __init__(self):
        self.INITIAL_SIZE = [250, 600]
        mWin = shiboken2.wrapInstance(long(omui1.MQtUtil.mainWindow()), QtWidgets.QWidget)
        super(MainUI_Win, self).__init__(parent=mWin)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.connectSlots()

    def start(self):
        core.autoUpdateLibraries()

        self.show(dockable=True, width=self.INITIAL_SIZE[0], height=self.INITIAL_SIZE[1], floating=False)
        cmds.workspaceControl('gfutilitiesbelt_mainUIWorkspaceControl', e=True,
            rsw=self.INITIAL_SIZE[0], rsh=self.INITIAL_SIZE[0])

        core.startCheck()
        self.createHomeTab()

    def connectSlots(self):
        self.btn_addPocket.clicked.connect(self.showAddUi)
        self.btn_addPocket.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.btn_addPocket.customContextMenuRequested.connect(self.addPocketContextMenu)
        self.btn_listView.clicked.connect(lambda: sys.stdout.write("In Development...\n"))
        self.btn_iconView.clicked.connect(lambda: sys.stdout.write("In Development...\n"))
        self.tbw_pocketArea.tabCloseRequested.connect(self.deleteCurrentTab)
        tabBar = self.tbw_pocketArea.tabBar()
        tabBar.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        tabBar.customContextMenuRequested.connect(self.tabContextmenu)

    def showAddUi(self, *args):
        if cmds.window("gfutilitiesbelt_addpocketUI", ex=True):
            cmds.setFocus("gfutilitiesbelt_addpocketUI")
        else:
            app = AddUI_Win()
            app.start()

    def showEditUi(self, pocket, *args):
        if cmds.window("gfutilitiesbelt_editpocketUI", ex=True):
            cmds.setFocus("gfutilitiesbelt_editpocketUI")
        else:
            app = EditUI_Win(name=pocket)
            app.start()

    def addPocketContextMenu(self, position):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.addTabQuickName = QtWidgets.QLineEdit()
        self.addTabQuickName.setSizePolicy(sizePolicy)
        self.addTabQuickName.setMinimumWidth(150)
        self.addTabQuickName.setMaximumWidth(150)
        self.addTabQuickName.setPlaceholderText("Pocket name")
        self.addTabQuickName.setClearButtonEnabled(True)
        self.addTabQuickName.returnPressed.connect(self.quickCreateTab)
        self.addTabContextMenu = QtWidgets.QMenu()
        wdg = QtWidgets.QWidgetAction(self.addTabContextMenu)
        wdg.setDefaultWidget(self.addTabQuickName)
        nameAct = self.addTabContextMenu.addAction(wdg)
        self.addTabQuickName.setFocus()
        action = self.addTabContextMenu.exec_(self.btn_addPocket.mapToGlobal(position))

    @QtCore.Slot()
    def quickCreateTab(self):
        name = self.addTabQuickName.text()
        if name == "":
            sys.stderr.write("Please type any name.\n")
        else:
            tab = core.createTab(name=name)
            self.addTabContextMenu.close()
            self.addTabContextMenu.deleteLater()
            self.tbw_pocketArea.setCurrentWidget(tab)

    def tabContextmenu(self, position):
        index, widget, exists = core.checkHomeTab(self.tbw_pocketArea)
        if not exists:
            self.tabMenu = QtWidgets.QMenu()
            editAct = self.tabMenu.addAction("Edit")
            saveAct = self.tabMenu.addAction("Save")
            deleteAct = self.tabMenu.addAction("Delete")
            closeAct = self.tabMenu.addAction("Close")
            curWidget = self.tbw_pocketArea.currentWidget()
            action = self.tabMenu.exec_(curWidget.mapToGlobal(position))

            if action == editAct:
                widget = self.tbw_pocketArea.currentWidget()
                name = widget.objectName().split("_")[-1]
                self.showEditUi(pocket=name)
            elif action == saveAct:
                sys.stdout.write("In Progress")
            elif action == closeAct:
                index = self.tbw_pocketArea.currentIndex()
                self.deleteCurrentTab(index)
            elif action == deleteAct:
                widget = self.tbw_pocketArea.currentWidget()
                name = widget.objectName().split("_")[1]
                delete = cmds.confirmDialog(t="%s.gfPocket" % name, m="You are about to delete %s.gfPocket.\nAre you sure?" % name,
                    b=["Yes", "No"], db="No", cb="No", ds="No")
                if delete == "Yes":
                    index = self.tbw_pocketArea.currentIndex()
                    self.deleteCurrentTab(index)
                    path = os.path.join(fileM.POCKETS_PATH, "%s.gfPocket" % name)
                    os.remove(path)
                    sys.stdout.write("%s.gfPocket successfully deleted.\n" % name)
                else:
                    sys.stdout.write("Operation canceled.\n")
        else:
            self.tabMenu = QtWidgets.QMenu()
            addAct = self.tabMenu.addAction("Add pocket")
            curWidget = self.tbw_pocketArea.currentWidget()
            action = self.tabMenu.exec_(curWidget.mapToGlobal(position))

            if action == addAct:
                self.showAddUi()

    def deleteCurrentTab(self, index):
        curTab = self.tbw_pocketArea.widget(index)
        curTabName = curTab.objectName()
        if curTabName != "tab_home":
            self.tbw_pocketArea.removeTab(index)
            curTab.deleteLater()
            if self.tbw_pocketArea.count() == 0:
                self.createHomeTab()
        else:
            sys.stderr.write("Can't delete tab Home.\n")

    def createHomeTab(self):
        index, widget, exists = core.checkHomeTab(self.tbw_pocketArea)
        if not exists:
            self.tab_home = QtWidgets.QWidget()
            self.tab_home.setObjectName("tab_home")
            self.lay_home = QtWidgets.QVBoxLayout(self.tab_home)
            self.lay_home.setContentsMargins(1, 1, 1, 1)
            self.lay_home.setSpacing(1)
            self.lay_home.setObjectName("lay_home")
            self.lbl_home = QtWidgets.QLabel(self.tab_home)
            font = QtGui.QFont()
            font.setPointSize(14)
            self.lbl_home.setFont(font)
            self.lbl_home.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.lbl_home.setToolTip("Click to add a new pocket.")
            self.lbl_home.setText("<html><head/><body><p>Hey buddy! </p><p>May I help you?</p></body></html>")
            self.lbl_home.setAlignment(QtCore.Qt.AlignCenter)
            self.lbl_home.setObjectName("lbl_home")
            self.lay_home.addWidget(self.lbl_home)
            self.tbw_pocketArea.addTab(self.tab_home, "Home")
            self.lbl_home.mouseReleaseEvent = self.showAddUi
            self.tbw_pocketArea.setTabsClosable(False)
            self.tbw_pocketArea.setMovable(False)
        else:
            sys.stderr.write("Home tab already loaded.\n")


def main():
    if (cmds.window("gfutilitiesbelt_mainUI", ex=True)):
        cmds.deleteUI("gfutilitiesbelt_mainUI")
    app = MainUI_Win()
