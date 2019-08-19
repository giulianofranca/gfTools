'''
My Pose Library v0.1
Data             : June 6, 2018
Last Modified    : June 6, 2018
Author           : Subin Gopi
subing85@gmail.com
'''
'''
    Comecar no ep15
'''

import sys
import os
import json
import shutil
import datetime
from functools import partial
from maya import cmds
from PySide2 import QtWidgets, QtCore, QtGui

import mainwindow as uiClass
reload(uiClass)


class POSELIBRARY(uiClass.Ui_PoseLibWin):

    def __init__(self):
        super(POSELIBRARY, self).__init__()

        # Global Variables
        self.libraryDirectory = 'C:/Users/%s/Documents/maya/2017/scripts/gfTools/gfPoseLib/poseData' % (os.getenv('USERNAME'))
        self.currentDirectory = os.path.abspath(os.path.dirname(__file__))
        self.iconPath = self.currentDirectory + '/icons'
        self.tempDirectory = os.path.abspath(os.getenv('TEMP')).replace('\\', '/')
        self.snapshotPath = '%s/MyPose_Snapshot.png' % (self.tempDirectory)

        # Call Functions
        self.uiConfigure()
        self.iconConfigure()
        self.loadFolderStructure(self.libraryDirectory)

        # Show UI
        self.show(dockable=True)

        # Configure Workspace
        # cmds.workspaceControl(self.ui.CONTROL_NAME + "WorkspaceControl", e=True,
        #                       iw=275, mw=True, dtc=['ToolBox', 'right'], wp='preferred', fl=True)

    def uiConfigure(self):
        # Configure Splitter
        self.splitter.setSizes([200, 500, 200])
        # Create a custom context menu for QTreeWidget
        self.treeWidget_folderList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_folderList.customContextMenuRequested.connect(self.onFolderContextMenu)
        # Snapshot of current pose
        self.button_snapShot.clicked.connect(self.takeSnapshot)
        self.loadImageToButton(self.button_snapShot, ':/camera.svg', [30, 30])  # character.svg | checker.svg | chooser.svg | file.svg
        # Save the current pose
        self.button_save.clicked.connect(self.savePose)
        # Load pose to UI
        self.treeWidget_folderList.itemClicked.connect(self.loadCurrentFolder)

    def iconConfigure(self):
        menuList = self.findChildren(QtWidgets.QAction)
        for i in range(len(menuList)):
            objName = menuList[i].objectName()
            iconList = ['folder-new', 'expandContainer', 'collapseContainer']
            if objName:
                curIcon = objName.split('_')[1]
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(':/'+iconList[i]+'.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                menuList[i].setIcon(icon)

    def onFolderContextMenu(self, position):
        # self.folderMenu.exec_(QtGui.QCursor.pos()) # Add menu to the current cursor position
        menu = QtWidgets.QMenu()
        self.action_createFolder.triggered.connect(self.createFolder)
        self.action_expand.triggered.connect(self.expandFolder)
        self.action_collapse.triggered.connect(self.collapseFolder)
        menu.addAction(self.action_createFolder)
        menu.addSeparator()
        menu.addAction(self.action_expand)
        menu.addAction(self.action_collapse)
        # menu.addAction(self.action_openFolderLocation)
        menu.exec_(self.treeWidget_folderList.mapToGlobal(position))

    def createFolder(self):
        folderName, ok = QtWidgets.QInputDialog.getText(self, 'Folder name', 'Enter the folder name', QtWidgets.QLineEdit.Normal)
        if ok:
            parent = self.treeWidget_folderList
            curPath = self.libraryDirectory
            if self.treeWidget_folderList.selectedItems():
                parent = self.treeWidget_folderList.selectedItems()[-1]
                curPath = str(parent.toolTip(0))
            if not os.path.isdir('%s/%s' % (curPath, str(folderName))):
                item = QtWidgets.QTreeWidgetItem(parent)
                item.setText(0, str(folderName))
                item.setToolTip(0, '%s/%s' % (curPath, str(folderName)))
                # Connect icon
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(':/loadPreset_100.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item.setIcon(0, icon)
                if parent is not self.treeWidget_folderList:
                    self.treeWidget_folderList.setItemExpanded(parent, True)
                    self.treeWidget_folderList.setItemSelected(parent, False)
                self.treeWidget_folderList.setItemSelected(item, True)
                os.makedirs('%s/%s' % (curPath, str(folderName)))

    def expandFolder(self):
        if self.treeWidget_folderList.selectedItems():
            curItem = self.treeWidget_folderList.selectedItems()[-1]
            self.dependentList = [curItem]
            self.collectChildItems(curItem)
            for dependent in self.dependentList:
                self.treeWidget_folderList.setItemExpanded(dependent, True)
        else:
            self.treeWidget_folderList.expandAll()

    def collapseFolder(self):
        curItem = self.treeWidget_folderList.invisibleRootItem()
        if self.treeWidget_folderList.selectedItems():
            curItem = self.treeWidget_folderList.selectedItems()[-1]
        self.dependentList = [curItem]
        self.collectChildItems(curItem)
        for dependent in self.dependentList:
            self.treeWidget_folderList.setItemExpanded(dependent, False)

    def collectChildItems(self, parent):
        for i in range(parent.childCount()):
            curChild = parent.child(i)
            self.dependentList.append(curChild)
            self.collectChildItems(curChild)

    def getFolderStructure(self, path):
        dirList = dict()
        for root, dirs, files in os.walk(path):
            folderList = root.split(os.sep)
            folders = dirList
            for folder in folderList:
                folders = folders.setdefault(folder, dict())
        return dirList

    def loadFolderToTreeWidget(self, dirList, parent, path):
        for dir in dirList:
            if dir:
                item = QtWidgets.QTreeWidgetItem(parent)
                item.setText(0, dir)
                self.folderPath = '%s/%s' % (path, dir)
                item.setToolTip(0, self.folderPath)
                # Connect icon
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(':/loadPreset_100.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item.setIcon(0, icon)
                self.loadFolderToTreeWidget(dirList[dir], item, self.folderPath)
        self.folderPath = path

    def loadFolderStructure(self, path):
        dirList = self.getFolderStructure(path)
        self.folderPath = path
        self.loadFolderToTreeWidget(dirList[path], self.treeWidget_folderList, path)

    def takeSnapshot(self):
        print(self.snapshotPath)
        if os.path.isfile(self.snapshotPath):
            try:
                os.chmod(self.snapshotPath, 0777)
                os.remove(self.snapshotPath)
            except Exception, result:
                print(result)

        curFrame = cmds.currentTime(q=True)
        modelPanelList = cmds.getPanel(type='modelPanel')
        for mPanel in modelPanelList:
            cmds.modelEditor(mPanel, e=True, alo=False, pm=True)
        playblast = cmds.playblast(st=curFrame, et=curFrame, fmt='image', cc=True, v=False, orn=False, fp=1, p=100, c='png',
                                   wh=[512, 512], quality=100, cf=self.snapshotPath)
        self.loadImageToButton(self.button_snapShot, self.snapshotPath, [150, 150])
        for mPanel in modelPanelList:
            cmds.modelEditor(mPanel, e=True, alo=True)

    def loadImageToButton(self, button, path, size):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(size[0], size[1]))

    def savePose(self):
        poseLabel = str(self.lineEdit_poseLabel.text())
        if poseLabel:
            curItem = self.treeWidget_folderList.selectedItems()
            if curItem:
                # Collect ctrls attributes and attribute values
                selList = cmds.ls(sl=True)
                if selList:
                    ctrlInfoList = {}
                    for sel in selList:
                        attrList = cmds.listAttr(sel, k=True, u=True, sn=True)
                        attrInfoList = {}
                        if attrList:
                            for attr in attrList:
                                attrValue = cmds.getAttr('%s.%s' % (sel, attr))
                                attrInfoList.setdefault(attr.encode(), attrValue)
                            curCtrl = sel
                            # Check the reference
                            if cmds.referenceQuery(sel, inr=True):
                                refPath = cmds.referenceQuery(sel, f=True)
                                nameSpace = cmds.file(refPath, q=True, ns=True)
                                curCtrl = sel.replace('%s:' % (nameSpace), '')
                        ctrlInfoList.setdefault(curCtrl.encode(), attrInfoList)
                    # Data history
                    owner = os.getenv('USERNAME')
                    time = datetime.datetime.now().strftime("%A, %B %d, %Y %H:%M %p")
                    mayaVersion = cmds.about(q=True, v=True)
                    version = '0.1'
                    dataList = {'control': ctrlInfoList, 'history': [owner, time, mayaVersion, version]}
                    # Write Pose Data
                    curFolderPath = str(curItem[-1].toolTip(0))
                    dataPath = '%s/%s.gfpose' % (curFolderPath, poseLabel)
                    if os.path.isfile(dataPath):
                        try:
                            os.chmod(dataPath, 0777)
                            os.remove(dataPath)
                        except Exception, result:
                            print(result)
                    with open(dataPath, 'w') as doc:
                        jsonData = json.dumps(dataList, indent=4)
                        doc.write(jsonData)
                    # Pose Icon
                    curPoseIcon = self.snapshotPath
                    if not os.path.isfile(curPoseIcon):
                        curPoseIcon = '%s/icons/user.png' % (self.currentDirectory)
                    curPosePath = dataPath.replace('.gfpose', '.png')
                    if curPoseIcon == '%s/icons/user.png' % (self.currentDirectory):
                        try:
                            shutil.copy2(curPoseIcon, curPosePath)
                        except Exception, result:
                            print(result)
                    else:
                        try:
                            shutil.move(curPoseIcon, curPosePath)
                        except Exception, result:
                            print(result)
                    message = QtWidgets.QMessageBox()
                    message.setWindowTitle('Success!')
                    message.setIcon(QtWidgets.QMessageBox.Information)
                    message.setText('Successfully export My Pose Data.')
                    result = message.exec_()
                    self.lineEdit_poseLabel.clear()
                    self.loadImageToButton(self.button_snapShot, ':/camera.svg', [30, 30])
                    self.loadCurrentFolder()
                else:
                    message = QtWidgets.QMessageBox()
                    message.setWindowTitle('Something wrong :(')
                    message.setIcon(QtWidgets.QMessageBox.Warning)
                    message.setText('No controls selected.\t')
                    message.setInformativeText('Please select at least one control.')
                    result = message.exec_()
            else:
                message = QtWidgets.QMessageBox()
                message.setWindowTitle('Something wrong :(')
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.setText('No folder selected.\t')
                message.setInformativeText('Please select the folder.')
                result = message.exec_()
                # if result == QtWidgets.QMessageBox.Ok:
                #     print('Ok cliked')
        else:
            message = QtWidgets.QMessageBox()
            message.setWindowTitle('Something wrong :(')
            message.setIcon(QtWidgets.QMessageBox.Warning)
            message.setText('Type a valid name.\t')
            message.setInformativeText('Please type any valid name.')
            result = message.exec_()

    def loadCurrentFolder(self):
        curItems = self.treeWidget_folderList.selectedItems()
        # Add child items with selected QTreeItem
        self.dependentList = []
        for item in curItems:
            self.dependentList.append(item)
            self.collectChildItems(item)
        self.removeExistWidget(self.gridLayout_poseList)
        self.loadPoseToLayout(self.dependentList)

    def removeExistWidget(self, layout):
        for i in range(layout.count()):
            if layout.itemAt(i).widget():
                layout.itemAt(i).widget().deleteLater()

    def loadPoseToLayout(self, itemList):
        poseList = list()
        for item in itemList:
            curPath = str(item.toolTip(0))
            if os.path.isdir(curPath):
                dirList = os.listdir(curPath)
                for file in dirList:
                    if os.path.isfile('%s/%s' % (curPath, file)):
                        if file.endswith('.gfpose'):
                            poseList.append('%s/%s' % (curPath, file))
        row = -1
        column = 0
        coordinateList = list()
        for i in range(len(poseList)):
            if i % 3:
                column += 1
                coordinateList.append([row, column])
            else:
                row += 1
                column = 0
                coordinateList.append([row, column])
        for i in range(len(poseList)):
            poseLabel = os.path.splitext(os.path.basename(poseList[i]))[0]
            toolBtn = QtWidgets.QToolButton(self.scrollAreaWidget_pose)
            toolBtn.setObjectName('toolButton_%s' % (poseLabel))
            toolBtn.setText(poseLabel)
            toolBtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            toolBtn.setMinimumSize(QtCore.QSize(125, 125))
            toolBtn.setMaximumSize(QtCore.QSize(125, 125))
            poseIconPath = poseList[i].replace('.gfpose', '.png')
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(poseIconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            toolBtn.setIcon(icon)
            toolBtn.setIconSize(QtCore.QSize(100, 100))
            self.gridLayout_poseList.addWidget(toolBtn, coordinateList[i][0], coordinateList[i][1], 1, 1)

            toolBtn.clicked.connect(partial(self.setCurrentPose, poseList[i]))

    def setCurrentPose(self, posePath):
        # Import the pose data to scene.
        with open(posePath, 'r') as doc:
            dataList = json.load(doc)

        selList = cmds.ls(sl=True)
        for sel in selList:
            curCtrl = sel
            if cmds.referenceQuery(sel, inr=True):
                refPath = cmds.referenceQuery(sel, f=True)
                nameSpace = cmds.file(refPath, q=True, ns=True)
                curCtrl = sel.replace('%s:' % (nameSpace), '')
            if curCtrl in dataList['control']:
                attrList = dataList['control'][curCtrl]
                for attr in attrList:
                    attrValue = attrList[attr]
                    cmds.setAttr('%s.%s' % (sel, attr), attrValue)
        curIconPath = posePath.replace('.gfpose', '.png')
        self.loadImageToButton(self.button_snapShot, curIconPath, [150, 150])
        curPoseLabel = os.path.splitext(os.path.basename(posePath))[0]
        self.lineEdit_poseLabel.setText(curPoseLabel)
        # Load history
        historyData = dataList['history']
        historyList = ['Owner: %s' % (historyData[0]),
                       'Created: %s' % (historyData[1]),
                       'Maya version: %s' % (historyData[2]),
                       'Module version: %s' % (historyData[3])
                       ]
        self.textEdit_history.setText('\n'.join(historyList))
        print("Successfull import My Pose Data.")
