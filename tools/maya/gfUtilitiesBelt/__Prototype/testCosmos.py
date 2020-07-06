__author__ = 'Martin Gunnarsson (hello@deerstranger.com)'
__version__ = '1.5'
from maya import mel, cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQDockWidget
from extensions.Qt import QtWidgets, QtCompat, QtCore, QtGui
import extensions.qtCore as qtCore
from extensions.flowLayout import FlowLayout
import tempfile, webbrowser, os, shutil, sys, time, prefs, functions, library, copy
from library import compareEngine, getFavorites, getBlacklisted, getContent
from mayaPortal import mayaWindow, getMayaCommands, installHotkey, displayViewMessage
os.environ['QT_PREFERRED_BINDING'] = os.pathsep.join(['PySide2', 'PySide2'])
logger = functions.installLogger('Cosmos logger', file=prefs.getPrefsFolder() + os.sep + 'cosmos_logger.log')
relativePath = os.path.dirname(os.path.realpath(__file__)) + os.sep
parentPath = os.path.abspath(os.path.join(relativePath, os.pardir))
uiPath = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'ui' + os.sep
menuLogo = ('{}icons{}mainLogo.png').format(relativePath, os.sep)
iconFolder = ('{}icons{}').format(relativePath, os.sep)
searchMayaMenus = True
maxResultCount = 100
maxCardInWindow = 8
startupHotkey = True
windowAnim = True
menubar = True
windowPosition = None
from variables import *
qtCore.windowAnim = windowAnim
favoriteActionsList = prefs.getList('favoriteList')
latestActionsList = prefs.getList('latestList')
dockedWindows = []
try:
    cmds.evalDeferred('cosmos.scan()', lp=True)
    cmds.evalDeferred('cosmos.setInterfaceColor()', lp=True)
    if startupHotkey is True:
        cmds.evalDeferred('cosmos.installHotkey()', lp=True)
except:
    scan()
    setInterfaceColor()
    if startupHotkey is True:
        installHotkey()

def setInterfaceColor():
    global uicolor
    grayMode = prefs.getGenericSettings('noColorMode')
    if grayMode == 'True':
        uicolor = {'R': 68, 'G': 68, 'B': 68, 'A': 255}
    else:
        uicolor = {'R': 64, 'G': 97, 'B': 127, 'A': 250}


def scan():
    getContent()
    loadMayaCommands()
    output = loadMayaCommands()


def rescan():
    scan()
    displayWindow('search')
    displayViewMessage(text='Library Reloaded')


def start():
    if prefs.prefExist('cosmos_settings.xml') == True:
        if prefs.prefsValid() == True:
            try:
                if cosmosTutorialWindow.ui.hotkeyValueText.isVisible():
                    cosmosTutorialWindow.ui.hotkeyValueText.setText('(You got this!)')
                    cosmosTutorialWindow.ui.handIcon.setIcon(QtGui.QPixmap(('{}').format(relativePath.replace('\\', '/') + 'icons/hand.png')))
                    qtCore.propertyAnimation(start=[10, 10], end=[30, 30], duration=300, object=cosmosTutorialWindow.ui.handIcon, property='iconSize', mode='OutBounce')
                else:
                    displayWindow('search')
            except:
                displayWindow('search')

        else:
            displayViewMessage(text='Problem loading Cosmos preferences\nCheck the script-editor for more info.', mode='error')
            print '\n--- Error reading Cosmos Preferences ---'
            print 'Not very normal, but your settings look to be corrupted:'
            print "'" + prefs.home + os.sep + 'cosmos_settings.xml' + "'"
            print 'Most likely badly formated, delete file to generate a new one.'
            print '-----------------------------------------'
    else:
        prefs.createFile()
        getContent()
        displayWindow('tutorial')


def close():
    for window in mayaWindow().children():
        if isinstance(window, searchWindow):
            window.close()
            print 'Closing Cosmos Instance'


def search(input):
    for window in mayaWindow().children():
        if isinstance(window, searchWindow):
            window.ui.inputField.setText(input)


def browser(url):
    webbrowser.open(url, new=2)


def loadMayaCommands():
    global mayaCommandList
    if searchMayaMenus is True:
        mayaCommandList = getMayaCommands()
        if mayaCommandList != None:
            pass
        else:
            logger.error('Cant find a proper maya menu')
    else:
        mayaCommandList = []
    return len(mayaCommandList)


def removeBlacklisted(commandList):
    """Remove blacklisted from a list"""
    if len(library.blacklistedCommands) >= 1:
        for item in commandList[:]:
            for number, blacklisted in enumerate(library.blacklistedCommands):
                if item['name'] == blacklisted['name']:
                    if item['category'] == blacklisted['category']:
                        if item['info'] == blacklisted['info']:
                            commandList.remove(item)

    return commandList


def filterActions(search=False, gate=0.1, paths=[], categories=[], tags=[], favorites=False, blacklisted=False, description=False, icon=None, mayaCommands=True, cosmosCommands=True):
    favoriteActionsList = prefs.getList('favoriteList')
    commandList = []
    if cosmosCommands == True:
        commandList += library.cosmosCommandList
    if mayaCommands == True:
        commandList += mayaCommandList
    if len(categories) >= 1:
        list = []
        for category in categories:
            list += [ dictionary for dictionary in commandList if category in dictionary['category'] ]

        commandList = list
    if len(tags) >= 1:
        list = []
        for tag in tags:
            list += [ dictionary for dictionary in commandList if tag in dictionary['tags'] ]

        commandList = list
    if len(paths) >= 1:
        list = []
        for path in paths:
            list += [ dictionary for dictionary in commandList if path in dictionary['category'] ]

        commandList = list
    if description != False:
        commandList = [ dictionary for dictionary in commandList if description in dictionary['info'] ]
    if description != False:
        commandList = [ dictionary for dictionary in commandList if description in dictionary['info'] ]
    if icon != None:
        if icon is True:
            commandList = [ dictionary for dictionary in commandList if dictionary['icon'] != '' ]
        elif icon is False:
            commandList = [ dictionary for dictionary in commandList if dictionary['icon'] == '' ]
    if favorites != False:
        if len(favoriteActionsList) >= 1:
            list = []
            for favorite in favoriteActionsList:
                list += [ item for item in commandList if item['name'] == favorite['name'] ]

            commandList = list
        else:
            commandList = []
    if blacklisted != False:
        if len(library.blacklistedCommands) >= 1:
            list = []
            for item in commandList[:]:
                for number, blacklisted in enumerate(library.blacklistedCommands):
                    if item['name'] == blacklisted['name']:
                        if item['category'] == blacklisted['category']:
                            if item['info'] == blacklisted['info']:
                                list.append(item)

            commandList = list
        else:
            commandList = []
    if search != False:
        itemsToRemove = []
        for item in commandList:
            name = item['name']
            scoreValue = compareEngine(search, item['name'], item['category'], item['tags'], item['info'])
            if scoreValue >= gate:
                item['score'] = scoreValue
            else:
                itemsToRemove.append(item)

        for item in itemsToRemove:
            commandList.remove(item)

    else:
        for item in commandList:
            item['score'] = 1

        search = ''
    return commandList


def sortActions(actions=[], sortingMethod='score', favorite=True, latest=True, prefered=False):
    global favoriteActionsList
    global latestActionsList
    if sortingMethod == 'score':
        if prefered != False:
            preferedList = prefs.getPreferedSearch(prefered)
            if preferedList != None:
                if len(preferedList) >= 1:
                    for item in actions:
                        for number, prefered in enumerate(sorted(preferedList, key=lambda object: int(object['count']))[::-1]):
                            if item['name'].lower() == prefered['name'].lower():
                                item['score'] += 10 * int(prefered['count'])
                            elif '@' in prefered['name']:
                                if prefered['name'].lower().split('@')[-1] == item['category'].lower():
                                    item['score'] += 10 * int(prefered['count'])

        if len(favoriteActionsList) >= 1:
            for item in actions:
                for favorite in favoriteActionsList:
                    if item['name'] in favorite['name']:
                        item['score'] += 100

        baseScore = 10
        if len(latestActionsList) >= 1:
            for item in actions:
                for number, latest in enumerate(latestActionsList):
                    if item['name'] in latest['name']:
                        item['score'] += baseScore
                        baseScore *= 0.9

    actions = sorted(actions, key=lambda input: input['name'])
    if sortingMethod == 'score':
        actionsOutput = sorted(actions, key=lambda input: input['score'])[::-1]
    else:
        if sortingMethod == 'alphabetical':
            actionsOutput = sorted(actions, key=lambda input: input['name'])
        else:
            if sortingMethod == 'category':
                actionsOutput = sorted(actions, key=lambda input: input['category'])
            else:
                if sortingMethod == 'path':
                    actionsOutput = sorted(actions, key=lambda input: input['category'])
                else:
                    if sortingMethod == 'tags':
                        actionsOutput = sorted(actions, key=lambda input: input['tags'])
                    else:
                        actionsOutput = actions
                        print ("INVALID SORTING: '{}'").format(sortingMethod)
                        print 'No valid sorting method specified, returning original list'
    return actionsOutput


def filterSearch(filterCategory=None, filterSearch=None, search=None, mayaCommands=True, cosmosCommands=True):
    results = []
    cosmosCommandList = library.cosmosCommandList
    if filterCategory != None:
        cosmosList = [ item for item in library.cosmosCommandList if filterSearch.lower() in item[filterCategory].lower() ]
        if mayaCommands == True:
            mayaFilteredList = [ dictionary for dictionary in mayaCommandList if filterSearch.lower() in dictionary[filterCategory].lower()
                               ]
    if search == None:
        if filterCategory != None:
            if mayaCommands == True:
                results = cosmosList + mayaFilteredList
            else:
                results = cosmosList
        elif mayaCommands == False:
            results = cosmosCommandList
        else:
            results = cosmosCommandList + mayaCommandList
    else:
        for item in cosmosCommandList:
            info = item['info']
            tags = item['tags']
            command = item['command']
            name = item['name']
            icon = item['icon']
            category = item['category']
            scoreValue = compareEngine(search, name, tags, info, category)
            if scoreValue >= 0.2:
                item['score'] = scoreValue
                results.append(item)

        if mayaCommands == True:
            for item in mayaCommandList:
                info = item['info']
                name = item['name']
                category = item['category']
                scoreValue = compareEngine(search, name + ' ' + category, category + ' ' + name, info)
                if scoreValue >= 0.1:
                    icon = item['icon']
                    command = item['command']
                    tags = item['tags']
                    item['score'] = scoreValue
                    results.append(item)

        preferedList = prefs.getPreferedSearch(search)
        if preferedList != None:
            if len(preferedList) >= 1:
                for item in results:
                    for prefered in preferedList:
                        if item['name'] in prefered['name']:
                            if '@' in prefered['name']:
                                if prefered['name'].split('@')[-1] == item['category']:
                                    item['score'] += 50 * int(prefered['count'])
                            else:
                                item['score'] += 50 * int(prefered['count'])

        if len(favoriteActionsList) >= 1:
            for item in results:
                for favorite in favoriteActionsList:
                    if item['name'] == favorite['name']:
                        item['score'] += 100

        baseScore = 10
        if len(latestActionsList) >= 1:
            for item in results:
                for number, latest in enumerate(latestActionsList):
                    if item['name'] in latest['name']:
                        item['score'] += baseScore
                        baseScore *= 0.9

        if len(library.blacklistedCommands) >= 1:
            for item in results[:]:
                for number, blacklisted in enumerate(library.blacklistedCommands):
                    if item['name'] == blacklisted['name']:
                        if item['category'] == blacklisted['category']:
                            if item['info'] == blacklisted['info']:
                                results.remove(item)

        results = sorted(results, key=lambda input: input['score'])[::-1]
    return results


def createHeader(name='My Amazing header', layout=None, icon=None):
    headerWidget = headerUI()
    headerWidget.setTitle(name + ':')
    if icon != None:
        headerWidget.setIcon(icon, absolute=True)
    headerWidgetHolder = QtWidgets.QListWidgetItem(layout)
    headerWidgetHolder.setData(109, headerWidget)
    headerWidgetHolder.setSizeHint(QtCore.QSize(100, 35))
    layout.setItemWidget(headerWidgetHolder, headerWidget)
    return


def createCard(name='', command='', altCommand=None, id=None, parent='', tags='', icon='', info='', favorite=0, layout=None, setIcon=False, absoluteIcon=False, score=None):
    cardWidget = cardUI()
    if id == 'COSMOS':
        cardWidget.simpleMode(True)
    else:
        if id != None:
            cardWidget.setId(id)
        if score != None:
            cardWidget.score = score
        cardWidget.setTitle(name)
        cardWidget.setCommand(command)
        cardWidget.setCategory(parent)
        cardWidget.setTags(tags)
        cardWidget.setIconPath(icon)
        cardWidget.setDescription(info)
        cardWidget.setAltCommand(altCommand)
        if setIcon is True:
            if absoluteIcon == True:
                cardWidget.setIcon(icon, absolute=True)
            elif absoluteIcon == False:
                cardWidget.setIcon(icon)
        for favorite in library.favoriteListCommands:
            if favorite['name'] == name:
                if favorite['category'] in parent:
                    if favorite['info'] in info:
                        cardWidget.setFavorite(True)

        if layout is None:
            return
        if type(layout) == QtWidgets.QVBoxLayout:
            layout.addWidget(cardWidget)
            return cardWidget
    cardWidgetHolder = QtWidgets.QListWidgetItem(layout)
    cardWidgetHolder.setData(109, cardWidget)
    cardWidgetHolder.setData(100, name)
    cardWidgetHolder.setSizeHint(QtCore.QSize(50, 45))
    layout.setItemWidget(cardWidgetHolder, cardWidget)
    return cardWidgetHolder
    return


class headerUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(headerUI, self).__init__(parent)
        self.built = True
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.mainFrame = QtWidgets.QFrame(self)
        self.descriptionLabel = QtWidgets.QLabel(self.mainFrame)
        self.descriptionLabel.setStyleSheet('color: rgb(250,250,250,150);\nbackground-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(0, 0, 0, 40), stop: 0.5 rgb(0, 0, 0, 20));color: rgb(250, 250, 250, 150);border-radius:0px;padding-bottom:2px;')
        self.descriptionLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(11)
        self.descriptionLabel.setFont(font)
        self.gridLayout.addWidget(self.descriptionLabel)

    def setTitle(self, title):
        self.descriptionLabel.setText(title)


class cardUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(cardUI, self).__init__(parent)
        self.last = None
        self.built = False
        self.build = False
        self.name = ''
        self.id = None
        self.tags = ''
        self.description = ''
        self.category = ''
        self.iconOnly = ''
        self.special = False
        self.blacklisted = False
        self.iconPath = None
        self.absoluteIcon = False
        self.starred = False
        self.altCommand = None
        self.score = None
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        self.setStatusTip('Click to run this Action')
        self.setToolTip('Click to run this Action')
        self.installEventFilter(self)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.mainFrame = QtWidgets.QFrame(self)
        self.mainFrame.setObjectName('cardBackground')
        self.gridLayout_2 = QtWidgets.QGridLayout(self.mainFrame)
        self.gridLayout_2.setContentsMargins(7, 0, 3, 0)
        self.gridLayout_2.setSpacing(0)
        return

    def delayedBuild(self):
        buttonSize = 16
        self.mainFrame.setStyleSheet('QFrame#cardBackground{border:solid;border-radius:0px;border-top-width:1px;border-color: rgb(0, 0, 0,30);}')
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(8, 0, 0, 0)
        self.topLayout = QtWidgets.QHBoxLayout()
        self.categoryLabel = QtWidgets.QLabel(self.mainFrame)
        self.categoryLabel.setStyleSheet('color: rgb(250,250,250,150);\nbackground-color: rgb(250, 250, 250,0);')
        self.categoryLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.topLayout.addWidget(self.categoryLabel)
        self.mainLayout.addLayout(self.topLayout)
        self.nameLabel = QtWidgets.QLabel(self.mainFrame)
        self.nameLabel.setStyleSheet('color: rgb(250, 250, 250);\nbackground-color: rgb(250, 250, 250,0);')
        self.nameLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.topLayout.addWidget(self.nameLabel)
        font = QtGui.QFont()
        font.setBold(True)
        self.nameLabel.setFont(font)
        self.bottomLayout = QtWidgets.QHBoxLayout()
        self.descriptionLabel = QtWidgets.QLabel(self.mainFrame)
        self.descriptionLabel.setStyleSheet('color: rgb(250,250,250,100);\nbackground-color: rgb(250, 250, 250,0);')
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.descriptionLabel.setMinimumHeight(20)
        self.bottomLayout.addWidget(self.descriptionLabel)
        self.mainLayout.addLayout(self.bottomLayout)
        self.gridLayout_2.addLayout(self.mainLayout, 0, 2, 1, 1)
        self.icon = QtWidgets.QToolButton(self.mainFrame)
        iconSize = 32
        self.icon.setMinimumSize(QtCore.QSize(iconSize, iconSize))
        self.icon.setMaximumSize(QtCore.QSize(iconSize, iconSize))
        self.icon.setIconSize(QtCore.QSize(iconSize, iconSize))
        self.icon.setStyleSheet('border: none; background-color: rgb(0, 250, 0,0);')
        self.gridLayout_2.addWidget(self.icon, 0, 1)
        self.altButton = fadeButton(self.mainFrame)
        self.altButton.setSize(buttonSize, buttonSize)
        self.altButton.hide()
        self.gridLayout_2.addWidget(self.altButton, 0, 3)
        self.starButton = fadeButton(self.mainFrame)
        self.starButton.setSize(buttonSize, buttonSize)
        self.starButton.setStatusTip('Favorite this item')
        self.starUncheckedOpacity = 0.1
        self.starCheckedOpacity = 0.8
        self.starButton.setOpacity(self.starUncheckedOpacity)
        self.gridLayout_2.addWidget(self.starButton, 0, 4)
        self.starButton.clicked.connect(self.saveFavorite)
        self.altButton.clicked.connect(lambda : self.execute(alt=True))
        self.menuButton = fadeButton(self.mainFrame)
        self.menuButton.setStatusTip('Open the Menu for this Action')
        self.menuButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.menuButton.setSize(7, buttonSize + 2)
        self.gridLayout_2.addWidget(self.menuButton, 0, 5)
        self.menuButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.menuButton.clicked.connect(self.leftClickMenu)
        self.popMenu = QtWidgets.QMenu(self)
        menuBarString = ('QMenu{{background-color: rgba({R},{G},{B},{A});color: rgb(255,255,250,150);}}QMenu::item:selected{{color: rgba(255, 255, 255, 250);}}').format(R=uicolor['R'], G=uicolor['G'], B=uicolor['B'], A=uicolor['A'])
        self.popMenu.setStyleSheet(menuBarString)
        self.menuButton.setMenu(self.popMenu)
        self.gridLayout.addWidget(self.mainFrame, 0, 1)
        try:
            self.starButton.setIcon(self.starbuttonImage)
        except:
            self.starbuttonImage = QtGui.QPixmap(('{}').format(relativePath.replace('\\', '/') + 'icons/starred.png'))
            self.starButton.setIcon(self.starbuttonImage)

        try:
            self.altButton.setIcon(self.altbuttonImage)
        except:
            self.altbuttonImage = QtGui.QPixmap(('{}').format(relativePath.replace('\\', '/') + 'icons/altCommand.png'))
            self.altButton.setIcon(self.altbuttonImage)

        try:
            self.menuButton.setIcon(self.menuButtonImage)
        except:
            self.menuButtonImage = QtGui.QPixmap(('{}').format(relativePath.replace('\\', '/') + 'icons/actionMenu.png'))
            self.menuButton.setIcon(self.menuButtonImage)

        self.updateInfo()

    def buildMethod(self):
        self.timer = QtCore.QTimer(singleShot=True)
        self.timer.timeout.connect(self.delayedBuild)
        self.timer.start(1)

    def updateInfo(self):
        self.nameLabel.setText(self.name)
        displayCategory = cleanCategory(self.category) + ' / '
        self.categoryLabel.setText(displayCategory)
        qtCore.autoFieldWidth(self.categoryLabel)
        self.descriptionLabel.setText(self.description)
        if self.altCommand != None:
            self.altButton.show()
        else:
            self.altButton.hide()
        if self.starred is True:
            self.starButton.setOpacity(self.starCheckedOpacity)
            qtCore.fadeAnimation(start=self.starUncheckedOpacity, end=self.starCheckedOpacity, duration=100, object=self.starButton.opacityEffect)
        else:
            if self.starred is False:
                qtCore.fadeAnimation(start='current', end=self.starUncheckedOpacity, duration=400, object=self.starButton.opacityEffect)
                self.starButton.setOpacity(self.starUncheckedOpacity)
        setIconFromString(self.icon, self.iconPath, absolute=self.absoluteIcon, name=self.name + ' ' + self.description)
        if self.special is True:
            self.categoryLabel.hide()
            self.starButton.hide()
            self.menuButton.hide()
        else:
            self.categoryLabel.show()
            self.starButton.show()
        return

    def leftClickMenu(self):
        self.popMenu.clear()
        if str(self.id) != 'None':
            editAction = QtWidgets.QAction('Edit', self)
            editAction.triggered.connect(self.editAction)
            self.popMenu.addAction(editAction)
        if self.starred is False:
            favoriteAction = QtWidgets.QAction('Star', self)
            favoriteAction.triggered.connect(lambda : self.setFavorite(True))
        else:
            favoriteAction = QtWidgets.QAction('Unstar', self)
            favoriteAction.triggered.connect(lambda : self.setFavorite(False))
        if len(library.blacklistedCommands) >= 1:
            for number, blacklisted in enumerate(library.blacklistedCommands):
                if self.name in blacklisted['name']:
                    if self.category in blacklisted['category']:
                        if self.description in blacklisted['info']:
                            self.blacklisted = True

        if self.blacklisted is False:
            blacklistAction = QtWidgets.QAction('Blacklist', self)
            blacklistAction.triggered.connect(lambda : self.appendBlacklist(mode='add'))
        else:
            blacklistAction = QtWidgets.QAction('Remove from Blacklist', self)
            blacklistAction.triggered.connect(lambda : self.appendBlacklist(mode='remove'))
        deleteAction = QtWidgets.QAction('Delete', self)
        deleteAction.triggered.connect(self.removeAction)
        self.popMenu.addAction(favoriteAction)
        self.popMenu.addAction(blacklistAction)
        if str(self.id) != 'None':
            self.popMenu.addSeparator()
            self.popMenu.addAction(deleteAction)
        self.popMenu.exec_(QtGui.QCursor.pos())

    def removeAction(self):
        action = library.getActionById(self.id)
        library.askDeleteAction(action)

    def execute(self, alt=False):
        executeCard(self, forceAlt=alt)
        self.setNormal()
        if self.special is False:
            prefs.addRecentSearch(self)
            for window in mayaWindow().children():
                if isinstance(window, searchWindow):
                    window.tryClose()

    def editAction(self):
        cosmosTransferId = self.id
        status = True
        if 'MAYA' in self.tags:
            status = False
        if self.special is True:
            status = False
        if cosmosTransferId is None:
            status = False
        if status is True:
            self.actionFile = library.getActionPathById(cosmosTransferId)
            if self.actionFile != None:
                displayWindow('actionInfo')
                cosmosActionInfoWindow.attachAction(cosmosTransferId)
            else:
                displayViewMessage(text=("The Action '{}' cant be found").format(self.nameLabel.text()), mode='error')
        else:
            displayViewMessage(text=("The Action '{}' cant be edited").format(self.nameLabel.text()), mode='error')
            logger.info(('The action "{}" in "{}" cant be edited').format(self.nameLabel.text(), self.category))
        self.setNormal()
        return

    def appendBlacklist(self, mode='add'):
        if mode == 'add':
            prefs.addBlacklisted(self)
        else:
            if mode == 'remove':
                prefs.removeListItem('blackList', self.name, self.category, self.description)
        getBlacklisted()
        searchInstances = returnInstances(searchWindow)
        for window in searchInstances:
            if window.activeButton == 'Blacklist':
                window.displayBlackListed()
            else:
                window.search(window.ui.inputField.text())

        windowInstances = returnInstances(genericDockingWindow)
        for window in windowInstances:
            if window.ui.checkbox_blacklisted.isChecked() == True:
                window.filter()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.setActive()
            self.last = 'Click'

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.last == 'Click':
                QtWidgets.QApplication.instance().setDoubleClickInterval(200)
                QtCore.QTimer().singleShot(QtWidgets.QApplication.instance().doubleClickInterval(), self.performSingleClickAction)
            else:
                self.message = 'Double Click'
                self.update()
                self.setNormal()

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.last = 'Double Click'
            self.editAction()

    def performSingleClickAction(self):
        if self.last == 'Click':
            self.message = 'Click'
            self.update()
            self.execute()

    def simpleMode(self, mode):
        self.special = True

    def setId(self, inputId):
        self.id = inputId

    def getId(self):
        return self.id

    def setTags(self, tags):
        self.tags = tags

    def getTags(self):
        return self.tags

    def setCommand(self, command):
        self.command = command

    def getCommand(self):
        return self.command

    def setAltCommand(self, command):
        self.altCommand = command

    def getAltCommand(self):
        return self.altCommand

    def setTitle(self, title):
        self.name = title

    def getTitle(self):
        return self.name

    def setCategory(self, category):
        self.category = category

    def altCommandExist(self):
        if self.altCommand is None:
            return False
        return True
        return

    def getCategory(self):
        return self.category

    def setDescription(self, description):
        self.description = description

    def getDescription(self):
        return self.description

    def setIconPath(self, iconPath, absolute=False):
        self.iconPath = iconPath
        self.absoluteIcon = absolute

    def getIconPath(self):
        return self.iconPath

    def setIcon(self, iconInput, absolute=False):
        self.iconOnly = iconInput
        self.absoluteIcon = absolute

    def setFavorite(self, state):
        try:
            self.starred = state
            if state is True:
                self.starButton.setOpacity(self.starCheckedOpacity)
                qtCore.fadeAnimation(start=self.starUncheckedOpacity, end=self.starCheckedOpacity, duration=100, object=self.starButton.opacityEffect)
            else:
                if state is False:
                    qtCore.fadeAnimation(start='current', end=self.starUncheckedOpacity, duration=400, object=self.starButton.opacityEffect)
                    self.starButton.setOpacity(self.starUncheckedOpacity)
        except:
            pass

    def saveFavorite(self):
        global favoriteActionsList
        name = self.name
        if self.starred is False:
            if self.id is None:
                idOutput = 'MAYA'
            else:
                idOutput = self.id
            status = prefs.addFavorite(self)
            if status is True:
                getFavorites()
                self.starButton.setOpacity(self.starCheckedOpacity)
                self.starred = True
                logger.info(("Unstarred item: '{}'").format(name))
        else:
            prefs.removeListItem('favoriteList', self.name, self.category, self.description)
            qtCore.fadeAnimation(start='current', end=self.starUncheckedOpacity, duration=400, object=self.starButton.opacityEffect)
            self.starButton.setOpacity(self.starUncheckedOpacity)
            self.starred = False
            logger.info(("Unstarred item: '{}'").format(name))
        windowInstances = returnInstances(genericDockingWindow)
        for window in windowInstances:
            if window.ui.checkbox_favorite.isChecked() == True:
                window.filter()
            else:
                window.updateCard(name=name, setFavorite=self.starred)

        for window in mayaWindow().children():
            if isinstance(window, searchWindow):
                if window.activeButton == 'favorites':
                    window.statusButtonClicked('Favorites')

        favoriteActionsList = prefs.getList('favoriteList')
        return

    def getFavorite(self):
        return self.starred

    def setActive(self):
        self.mainFrame.setStyleSheet('background-color: rgb(250, 250, 250,50);')

    def setNormal(self):
        self.mainFrame.setStyleSheet('background-color: rgb(0,0,0,0);')
        self.setCategory(self.category)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.GrabMouse:
            return QtWidgets.QMainWindow.eventFilter(self, object, event)
        if event.type() == QtCore.QEvent.WindowActivate or event.type() == QtCore.QEvent.Enter:
            self.activateWindow()
            return QtWidgets.QMainWindow.eventFilter(self, object, event)
        if event.type() == QtCore.QEvent.WindowDeactivate:
            return QtWidgets.QMainWindow.eventFilter(self, object, event)
        if event.type() == QtCore.QEvent.DragLeave:
            print 'You dragged a file from here'
        else:
            if event.type() == QtCore.QEvent.DragMove:
                print 'You dragged a file from here'
            else:
                if event.type() == QtCore.QEvent.Drop:
                    print 'You dropped a file on me'
                else:
                    if event.type() == QtCore.QEvent.FocusIn:
                        return QtWidgets.QMainWindow.eventFilter(self, object, event)
                    if event.type() == QtCore.QEvent.FocusOut:
                        self.fadeCloseWindow()
                    else:
                        return QtWidgets.QMainWindow.eventFilter(self, object, event)


class filterHeader(QtWidgets.QPushButton):
    """Add a custom header for the actionlist"""

    def __init__(self, args):
        self.height = 30
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.setStylesheet('background-color: rgb(0, 0, 0, 0);color: rgb(250,250,250,100)')
        self.disasbled(True)


class filterCheckbox(QtWidgets.QCheckBox):
    """Create a checkbox that returns the result to its parent instance"""

    def __init__(self):
        super(filterCheckbox, self).__init__()
        self.type = None
        self.attribute = None
        self.setMinimumHeight(30)
        self.setMaximumHeight(30)
        return

    def setTitle(self, title):
        self.setText(title)
        qtCore.autoFieldWidth(self, offset=30)


class tagButton(QtWidgets.QPushButton):
    """Create a checkbox that returns the result to its parent instance"""

    def __init__(self):
        super(tagButton, self).__init__()
        self.tag = None
        self.closeTag = False
        self.setObjectName('tagItem')
        self.setMinimumHeight(20)
        self.setMaximumHeight(20)
        self.setStyleSheet('QPushButton\n{\n\nbackground-color: rgb(250,250,250,30);\ncolor: rgb(250, 250, 250);\nborder-top-left-radius: 9px;\nborder-top-right-radius: 0px;\nborder-bottom-left-radius: 9px;\nborder-bottom-right-radius: 0px;\npadding-left: 10px;\npadding-right: 5px;\n}\n\nQPushButton:hover\n{\n\nbackground-color: rgb(250,250,250,20);\n}\n\nQPushButton:pressed\n{\n\nbackground-color: rgb(0,0,0,30);\n}')
        return

    def setTitle(self, title):
        self.setText(title)
        self.tag = title

    def closeMode(self):
        self.closeTag = True
        self.setIcon(QtGui.QPixmap(('{}').format(relativePath.replace('\\', '/') + 'icons/action_cross.png')))
        self.setIconSize(QtCore.QSize(10, 10))
        self.setStyleSheet('QPushButton\n{\n\nmargin-right: 5px;background-color: rgb(250,250,250,30);\ncolor: rgb(250, 250, 250);\nborder-top-left-radius: 0px;\nborder-top-right-radius: 9px;\nborder-bottom-left-radius: 0px;\nborder-bottom-right-radius: 9px;\npadding-left: 2px;\npadding-right: 4;\n}\n\nQPushButton:hover\n{\n\nbackground-color: rgb(250,250,250,20);\n}\n\nQPushButton:pressed\n{\n\nbackground-color: rgb(0,0,0,30);\n}')


class fadeButton(QtWidgets.QToolButton):
    """Create star-icon on card """

    def __init__(self, parent):
        super(fadeButton, self).__init__()
        self.width = 20
        self.height = 20
        self.opacity = 0.3
        self.endOpacity = 0.7
        self.inAnimDuration = 300
        self.outAnimDuration = 800
        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacityEffect)
        self.setAutoFillBackground(True)
        self.setOpacity(self.opacity)
        self.activeButton = False
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.setStyleSheet('QToolButton {color: rgb(250, 250, 250);background-color: rgb(0, 250, 0,0);border-style: None;border-width: 0px;}QToolButton:menu-indicator { image: none; }')

    def setOpacity(self, opacity):
        self.opacityEffect.setOpacity(opacity)
        self.opacity = opacity

    def setSize(self, width, height):
        self.setIconSize(QtCore.QSize(width, height))
        self.width = width
        self.height = height

    def enterEvent(self, event):
        if self.activeButton is False:
            qtCore.fadeAnimation(start='current', end=self.endOpacity, duration=self.inAnimDuration, object=self.opacityEffect)

    def leaveEvent(self, event):
        if self.activeButton is False:
            qtCore.fadeAnimation(start='current', end=self.opacity, duration=self.outAnimDuration, object=self.opacityEffect)


class hoverButton(QtWidgets.QToolButton):
    """Create star-icon on card """

    def __init(self, parent):
        QToolButton.__init__(self, parent)
        self.buttonSize = 20
        self.offset = 3
        qtCore.propertyAnimation(start=['current', 'current'], end=[self.buttonSize, self.buttonSize], duration=400, object=self, property='minimumSize')
        qtCore.propertyAnimation(start=['current', 'current'], end=[self.buttonSize, self.buttonSize], duration=400, object=self, property='maximumSize')
        qtCore.propertyAnimation(start=['current', 'current'], end=[self.buttonSize, self.buttonSize], duration=400, object=self)

    def enterEvent(self, event):
        qtCore.propertyAnimation(start=['current', 'current'], end=[
         self.buttonSize + self.offset, self.buttonSize + self.offset], duration=200, object=self, property='minimumSize')
        qtCore.propertyAnimation(start=['current', 'current'], end=[
         self.buttonSize + self.offset, self.buttonSize + self.offset], duration=200, object=self, property='maximumSize')
        qtCore.propertyAnimation(start=['current', 'current'], end=[
         self.buttonSize + self.offset, self.buttonSize + self.offset], duration=200, object=self)

    def leaveEvent(self, event):
        qtCore.propertyAnimation(start=['current', 'current'], end=[self.buttonSize, self.buttonSize], duration=400, object=self, property='minimumSize')
        qtCore.propertyAnimation(start=['current', 'current'], end=[self.buttonSize, self.buttonSize], duration=400, object=self, property='maximumSize')
        qtCore.propertyAnimation(start=['current', 'current'], end=[self.buttonSize, self.buttonSize], duration=400, object=self)


def returnInstances(name):
    global dockedWindows
    instances = []
    for window in mayaWindow().children():
        if isinstance(window, name):
            instances.append(window)

    if 'genericDockingWindow' in str(name):
        instances += dockedWindows
    return instances


def displayWindow(window):
    global cosmosActionInfoWindow
    global cosmosActionsWindow
    global cosmosSearchWindow
    global cosmosSetupWindow
    global cosmosTutorialWindow
    global createCategory_openWindow
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    if window is 'setup':
        cosmosSetupWindow = SetupWindow(parent=mayaWindow())
        cosmosSetupWindow.activateWindow()
    else:
        if window is 'tutorial':
            cosmosTutorialWindow = tutorialWindow(parent=mayaWindow())
            cosmosTutorialWindow.activateWindow()
        else:
            if window is 'actions':
                cosmosActionsWindow = actionListFilter(parent=mayaWindow())
                cosmosActionsWindow.activateWindow()
            else:
                if window is 'actionInfo':
                    cosmosActionInfoWindow = actionInfoWindow(parent=mayaWindow())
                    cosmosActionInfoWindow.activateWindow()
                else:
                    if window is 'search':
                        for window in mayaWindow().children():
                            if isinstance(window, searchWindow):
                                window.fadeCloseWindow()

                        cosmosSearchWindow = searchWindow(parent=mayaWindow())
                        cosmosSearchWindow.activateWindow()
                    else:
                        if window is 'createCategory':
                            createCategory_openWindow = createCategoryWindow(parent=mayaWindow())
    app.exec_()
    return


class genericWindow(QtWidgets.QDialog):

    def __init__(self, interfacePath, parent=None):
        super(genericWindow, self).__init__(parent)
        self.interfacePath = interfacePath
        self.ui = qtCore.qtUiLoader(self.interfacePath)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.ui)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.initUI()
        self.setObjectName(str(self.objectName))

    def showEvent(self, event):
        self.show()
        if self.dockedMode is False:
            qtCore.centerWidgetOnScreen(self)
            qtCore.fadeWindowAnimation(start=0, end=1, duration=400, object=self)
            qtCore.slideWindowAnimation(start=30, end=0, duration=300, object=self)

    def initUI(self):
        self.dockedMode = False
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        try:
            self.ui.frame.setStyleSheet('border-radius: 5px;background-color: rgb(' + ('{},{},{},{}').format(uicolor['R'], uicolor['G'], uicolor['B'], uicolor['A']) + ');')
        except:
            pass

        try:
            self.ui.closeButton.setStyleSheet('QPushButton {background-color: rgb(0,0,0,0);border-image: url(' + relativePath.replace('\\', '/') + 'icons/closeWindow.png); }QPushButton:hover { border-image: url(' + relativePath.replace('\\', '/') + 'icons/closeWindow_hover.png);}QPushButton:pressed{ border-image: url(' + relativePath.replace('\\', '/') + 'icons/closeWindow_hover.png);}')
            self.ui.closeButton.clicked.connect(self.fadeCloseWindow)
        except:
            pass

        try:
            QtWidgets.QSizeGrip(self.ui.resizeCorner)
        except:
            pass

        QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), self.ui, self.fadeCloseWindow)
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dockedMode is False:
            try:
                x = event.globalX()
                y = event.globalY()
                x_w = self.offset.x()
                y_w = self.offset.y()
                self.move(x - x_w, y - y_w)
            except:
                pass

    def closeEvent(self, event):
        event.accept()
        qtCore.fadeWindowAnimation(start=1, end=0, duration=400, object=self, finishAction=self.deleteLater)
        qtCore.slideWindowAnimation(start=0, end=300, duration=500, object=self)

    def fadeCloseWindow(self):
        qtCore.fadeWindowAnimation(start=1, end=0, duration=300, object=self, finishAction=self.deleteInstances)

    def deleteInstances(self):
        mayaMainWindow = mayaWindow()
        for obj in mayaMainWindow.children():
            if isinstance(obj, genericWindow):
                if obj.objectName() == str(self.objectName):
                    obj.setParent(None)
                    obj.deleteLater()
                    del obj

        return


class genericDockingWindow(MayaQWidgetDockableMixin, genericWindow):

    def __init__(self, interfacePath, parent=None):
        genericWindow.__init__(self, interfacePath, parent)


class tutorialWindow(QtWidgets.QDialog):

    def __init__(self, parent=None, title=None):
        super(tutorialWindow, self).__init__(parent)
        try:
            exec 'cosmosTutorialWindow.close()'
        except:
            pass

        self.initUI()
        qtCore.centerWidgetOnScreen(self)
        self.show()

    def initUI(self):
        self.resize(685, 290)
        self.maxNumber = 4
        self.ui = qtCore.qtUiLoader(('{}interface_tutorial.ui').format(uiPath))
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.ui)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.ui.closeButton.setStyleSheet('QPushButton \n{\nborder-image: url(' + relativePath.replace('\\', '/') + 'icons/closeWindow.png); \n}\nQPushButton:hover \n{\n border-image: url(' + relativePath.replace('\\', '/') + 'icons/closeWindow_hover.png);\n}\n\nQPushButton:pressed\n{\n border-image: url(' + relativePath.replace('\\', '/') + 'icons/closeWindow_hover.png);\n}\n')
        self.ui.closeButton.clicked.connect(self.fadeCloseWindow)
        self.ui.documentation_button.clicked.connect(lambda : browser('http://cosmos.toolsfrom.space/documentation'))
        if sys.platform == 'darwin':
            self.ui.hotkey.setText('SHIFT + TAB')
        else:
            self.ui.hotkey.setText('CTRL + TAB')
        self.ui.tutorialFrame.setStyleSheet('QFrame\n{\nborder-radius: 5px;\nbackground-color: rgb(' + ('{},{},{},{}').format(uicolor['R'], uicolor['G'], uicolor['B'], uicolor['A']) + ');\n}')
        self.ui.cosmosBigIcon.setPixmap(QtGui.QPixmap(('{}icons{}mainLogo.png').format(relativePath, os.sep)))
        self.ui.starPicture.setIcon(QtGui.QPixmap(relativePath.replace('\\', '/') + 'icons/starred.png'))
        self.ui.blacklistPicture.setIcon(QtGui.QPixmap(relativePath.replace('\\', '/') + 'icons/actionBlacklist.png'))
        self.ui.optionsPicture.setIcon(QtGui.QPixmap(relativePath.replace('\\', '/') + 'icons/altCommand.png'))
        self.ui.endStar.setIcon(QtGui.QPixmap(relativePath.replace('\\', '/') + 'icons/starred.png'))
        self.ui.smallLogo.setIcon(QtGui.QPixmap(menuLogo))
        self.ui.smallLogo.setAutoRaise(False)
        path = relativePath.replace('\\', '/') + 'icons/gif_tutorial.gif'
        self.gif_file = open(path, 'rb').read()
        self.gifByteArray = QtCore.QByteArray(self.gif_file)
        self.gifBuffer = QtCore.QBuffer(self.gifByteArray)
        self.movie = QtGui.QMovie()
        self.movie.setFormat('GIF')
        self.movie.setDevice(self.gifBuffer)
        self.movie.setDevice(self.gifBuffer)
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.setScaledSize(QtCore.QSize(501, 118))
        self.movie.setSpeed(100)
        self.movie.jumpToFrame(0)
        self.ui.searchGifHolder.setMovie(self.movie)
        self.ui.rightButton.clicked.connect(lambda : self.buttonPress(+1))
        self.ui.leftButton.clicked.connect(lambda : self.buttonPress(-1))
        self.ui.pageButton_00.clicked.connect(lambda : self.setIndex(0))
        self.ui.pageButton_01.clicked.connect(lambda : self.setIndex(1))
        self.ui.pageButton_02.clicked.connect(lambda : self.setIndex(2))
        self.ui.pageButton_03.clicked.connect(lambda : self.setIndex(3))
        self.ui.pageButton_04.clicked.connect(lambda : self.setIndex(4))
        self.tabOpacityEffect = QtWidgets.QGraphicsOpacityEffect(self)
        self.ui.tutorialHolder.setGraphicsEffect(self.tabOpacityEffect)
        self.ui.tutorialHolder.setAutoFillBackground(True)
        self.tabOpacityEffect.setOpacity(0)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setIndex(0)
        self.ui.smallLogo.hide()

    def setIndex(self, indexNumber):
        qtCore.fadeAnimation(start='current', end=0, duration=400, object=self.tabOpacityEffect)
        if indexNumber <= 0:
            indexNumber = 0
        if indexNumber >= self.maxNumber:
            indexNumber = self.maxNumber
        if indexNumber is 0:
            self.ui.pageButton_00.setChecked(True)
        else:
            if indexNumber is 1:
                self.ui.pageButton_01.setChecked(True)
            else:
                if indexNumber is 2:
                    self.ui.pageButton_02.setChecked(True)
                    self.movieTimer = QtCore.QTimer(singleShot=True)
                    self.movieTimer.timeout.connect(lambda : self.movie.start())
                    self.movieTimer.start(1100)
                else:
                    if indexNumber is 3:
                        self.ui.pageButton_03.setChecked(True)
                    else:
                        if indexNumber is 4:
                            self.ui.pageButton_04.setChecked(True)
                        else:
                            if indexNumber is 5:
                                self.ui.pageButton_05.setChecked(True)
                            else:
                                if indexNumber is 6:
                                    self.ui.pageButton_06.setChecked(True)
        self.propertiesTimer = QtCore.QTimer(singleShot=True)
        self.propertiesTimer.timeout.connect(self.fade_up_tab)
        self.propertiesTimer.timeout.connect(lambda : self.ui.tutorialHolder.setCurrentIndex(indexNumber))
        self.propertiesTimer.start(450)
        previousText = 'Previous'
        nextText = 'Next'
        skipText = 'Skip'
        closeText = 'Finish'
        if indexNumber == 0:
            self.ui.leftButton.setText(skipText)
            self.ui.smallLogo.hide()
        else:
            if indexNumber <= self.maxNumber - 1:
                self.ui.leftButton.setText(previousText)
                self.ui.rightButton.setText(nextText)
                self.ui.smallLogo.show()
            else:
                if indexNumber == self.maxNumber:
                    self.ui.leftButton.setText(previousText)
                    self.ui.rightButton.setText(closeText)

    def fade_up_tab(self):
        qtCore.fadeAnimation(start='current', end=1, duration=400, object=self.tabOpacityEffect)

    def buttonPress(self, input):
        current = self.ui.tutorialHolder.currentIndex()
        action = 'flip'
        if current is 0:
            if input is -1:
                action = 'close'
        else:
            if current is self.maxNumber:
                if input is 1:
                    action = 'close'
        if action == 'flip':
            self.incrementIndex(input)
        else:
            if action == 'close':
                self.launchCosmos()

    def incrementIndex(self, input):
        current = self.ui.tutorialHolder.currentIndex()
        self.setIndex(current + input)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)

    def launchCosmos(self):
        self.ui.hotkeyValueText.setHidden(True)
        self.fadeCloseWindow()
        start()

    def fadeCloseWindow(self):
        qtCore.fadeWindowAnimation(start=1, end=0, duration=400, object=self, finishAction=self.close)


class actionListFilter(genericDockingWindow):

    def __init__(self, parent=None):
        interfacePath = ('{}interface_actionList.ui').format(uiPath)
        super(actionListFilter, self).__init__(interfacePath, parent)
        self.checkboxes = []
        self.actions = []
        self.cards = []
        self.totalActions = 0
        self.sortingMethod = ''
        self.paths = []
        self.categories = []
        self.tags = []
        self.favorites = False
        self.ui.sortingField.setCurrentIndex(1)
        self.ui.dockButton.clicked.connect(self.makeDockable)
        self.ui.addActionButton.clicked.connect(self.openAddActionWindow)
        self.ui.clearButton.clicked.connect(self.clearValues)
        self.ui.sortingField.currentIndexChanged.connect(self._delayedFilter)
        self.ui.actionList.verticalScrollBar().valueChanged.connect(self.updateSelectedView)
        self.ui.actionList.verticalScrollBar().rangeChanged.connect(self.updateSelectedView)
        self.ui.checkbox_favorite.clicked.connect(self.appendCheckboxState)
        self.ui.checkbox_blacklisted.clicked.connect(self.appendCheckboxState)
        self.ui.checkbox_hasIcon.clicked.connect(self.appendCheckboxState)
        self.ui.checkbox_noIcon.clicked.connect(self.appendCheckboxState)
        self.ui.clearButton.hide()
        self.resize(430, 590)
        self.setWindowTitle('Cosmos Actions')
        self.ui.dockButton.setStyleSheet('QPushButton \n{\nborder-image: url(' + relativePath.replace('\\', '/') + 'icons/maxWindow.png); \n}\nQPushButton:hover \n{\n border-image: url(' + relativePath.replace('\\', '/') + 'icons/maxWindow_hover.png);\n}\n\nQPushButton:pressed\n{\n border-image: url(' + relativePath.replace('\\', '/') + 'icons/maxWindow_hover.png);\n}\n')
        self.ui.clearButton.setIcon(QtGui.QPixmap(('{}').format(relativePath.replace('\\', '/') + 'icons/action_cross.png')))
        self.ui.clearButton.setIconSize(QtCore.QSize(10, 10))
        self.headerObjects = [
         self.ui.filterHeader, self.ui.favoritesHeader, self.ui.listHeader,
         self.ui.categoriesHeader, self.ui.tagsHeader]
        self.frameObjects = [self.ui.filterFrame, self.ui.favoritesFrame, self.ui.listFrame, self.ui.categoriesFrame,
         self.ui.tagsFrame]
        for number, header in enumerate(self.headerObjects):
            header.setIcon(QtGui.QPixmap(('{}').format(relativePath.replace('\\', '/') + 'icons/action_closed.png')))
            header.setIconSize(QtCore.QSize(15, 15))
            if number >= 1:
                opacityEffect = QtWidgets.QGraphicsOpacityEffect(header)
                header.setGraphicsEffect(opacityEffect)
                opacityEffect.setOpacity(0.6)
            header.clicked.connect(self.setViewState)

        for frame in self.frameObjects[::-1]:
            frame.setMinimumHeight(0)
            frame.setMaximumHeight(0)

        self.generateFlowLayouts()
        self.propertiesTimer = QtCore.QTimer(singleShot=True)
        self.propertiesTimer.timeout.connect(self.getActionProperties)
        self.propertiesTimer.start(0)
        path = relativePath.replace('\\', '/') + 'icons/loading.gif'
        self.gif_file = open(path, 'rb').read()
        self.gifByteArray = QtCore.QByteArray(self.gif_file)
        self.gifBuffer = QtCore.QBuffer(self.gifByteArray)
        self.movie = QtGui.QMovie()
        self.movie.setFormat('GIF')
        self.movie.setDevice(self.gifBuffer)
        self.movie.setDevice(self.gifBuffer)
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.movie.setScaledSize(QtCore.QSize(15, 15))
        self.ui.loadingGif.setMovie(self.movie)
        self.movie.jumpToFrame(0)
        self.movie.start()
        self.gif_opacityEffect = QtWidgets.QGraphicsOpacityEffect(self.ui.loadingGif)
        self.ui.loadingGif.setGraphicsEffect(self.gif_opacityEffect)
        self.gif_opacityEffect.setOpacity(0)
        self.filterTimer = QtCore.QTimer(singleShot=True)
        self.filterTimer.timeout.connect(self.filter)
        self.filterTimer.start(0)
        self.show()
        self.ui.frame.setStyleSheet('background-color: rgb(' + ('{},{},{},{}').format(uicolor['R'], uicolor['G'], uicolor['B'], uicolor['A']) + ');\nborder-radius: 5px;')

    def updateSelectedView(self):
        buildCardInView(self.ui.actionList)

    def generateFlowLayouts(self):
        for element in self.frameObjects[2:]:
            for item in element.children():
                item.deleteLater()

            FlowLayout(element)

    def getActionProperties(self):
        self.paths = prefs.getGenericSettings('scriptPath').split(';')
        self.categories = library.cosmosCategories
        self.categories = [ cleanCategory(category) for category in self.categories ]
        self.tags = library.getTags()
        self.actions = library.cosmosCommandList
        self.totalActions = len(self.actions)
        self.generateCheckboxes(self.ui.tagsFrame, self.tags)
        self.generateCheckboxes(self.ui.categoriesFrame, self.categories)
        self.generateCheckboxes(self.ui.listFrame, self.paths)

    def appendCheckboxState(self):
        checkBox = self.sender()
        if checkBox.isChecked() == True:
            self.checkboxes.append(checkBox)
        else:
            self.checkboxes.remove(checkBox)
        if len(self.checkboxes) >= 1:
            self.ui.clearButton.show()
        else:
            self.ui.clearButton.hide()
        self.filter()

    def generateCheckboxes(self, element, items):
        """Fill a element with appropiate content"""
        for item in element.children():
            if type(item) == filterCheckbox:
                if item not in self.checkboxes:
                    item.deleteLater()

        flowLayout = element.children()[0]
        for item in items:
            checkbox = filterCheckbox()
            checkbox.setTitle(item)
            if len(self.checkboxes) >= 1:
                for object in self.checkboxes[:]:
                    if object.parent() == element:
                        if object.attribute == item:
                            checkbox.setChecked(True)
                            self.checkboxes.remove(object)
                            object.deleteLater()
                            self.checkboxes.append(checkbox)
                            break

            checkbox.type = element.objectName().replace('Frame', '')
            checkbox.attribute = item
            checkbox.clicked.connect(self.appendCheckboxState)
            flowLayout.addWidget(checkbox)

    def clearValues(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)

        self.ui.checkbox_hasIcon.setChecked(False)
        self.ui.checkbox_noIcon.setChecked(False)
        del self.checkboxes[:]
        self.setViewState(element=self.ui.filterHeader)
        self.closeTimer = QtCore.QTimer(singleShot=True)
        self.closeTimer.timeout.connect(self.ui.clearButton.hide)
        self.closeTimer.start(300)
        self.cardTimer = QtCore.QTimer(singleShot=True)
        self.cardTimer.timeout.connect(self.filter)
        self.cardTimer.start(400)

    def populateListWithIcons(self):
        for item in self.ui.actionList.findItems('', QtCore.Qt.MatchRegExp):
            cardItem = item.data(109)
            try:
                iconPath = cardItem.getIconPath()
                cardItem.setIcon(iconPath)
            except:
                pass

    def _delayedFilter(self):
        qtCore.fadeAnimation(start=self.gif_opacityEffect.opacity(), end=1, duration=100, object=self.gif_opacityEffect)
        self.filterTimer = QtCore.QTimer(singleShot=True)
        self.filterTimer.timeout.connect(self.filter)
        self.filterTimer.start(0)

    def filter(self):
        QtWidgets.QApplication.processEvents()
        paths = []
        tags = []
        categories = []
        others = 0
        favorites = False
        icon = None
        blacklisted = False
        for checkbox in self.checkboxes:
            try:
                if checkbox.type == 'list':
                    attributeList = paths
                else:
                    if checkbox.type == 'tags':
                        attributeList = tags
                    else:
                        if checkbox.type == 'categories':
                            attributeList = categories
                attributeList.append(checkbox.attribute)
            except:
                type = checkbox.objectName().replace('checkbox_', '')
                if type == 'favorite':
                    favorites = True
                    others += 1
                if type == 'hasIcon':
                    icon = True
                    others += 1
                if type == 'noIcon':
                    icon = False
                    others += 1
                if type == 'blacklisted':
                    blacklisted = True
                    others += 1

        self.actions = filterActions(paths=paths, categories=categories, tags=tags, mayaCommands=False, icon=icon, favorites=favorites, blacklisted=blacklisted)
        self._createCards()
        qtCore.fadeAnimation(start=self.gif_opacityEffect.opacity(), end=0, duration=800, object=self.gif_opacityEffect)
        QtWidgets.QApplication.processEvents()
        string = ''
        if len(categories) == 0 and len(paths) == 0 and len(tags) == 0 and others == 0:
            string = 'Filters'
        else:
            string = ('Filters ({})').format(len(paths) + len(tags) + len(categories) + others)
        self.ui.filterHeader.setText(string)
        return

    def updateCard(self, name, setName=None, setCommand=None, setCategory=None, setTags=None, setIcon=None, setInfo=None, setFavorite=None):
        for card in self.cards:
            card = card.data(109)
            if card.getTitle() == name:
                if setName != None:
                    card.setTitle(setName)
                if setCategory != None:
                    card.setCategory(setCategory)
                if setTags != None:
                    card.setTags(setTags)
                if setIcon != None:
                    if '/' in setIcon or '\\' in setIcon:
                        card.setIconPath(setIcon, absolute=True)
                    else:
                        card.setIconPath(setIcon)
                if setInfo != None:
                    card.setDescription(setInfo)
                if setFavorite != None:
                    card.setFavorite(setFavorite)
                try:
                    self.buildTimer = QtCore.QTimer(singleShot=True)
                    self.buildTimer.timeout.connect(card.updateInfo())
                    self.buildTimer.start(100)
                except:
                    pass

        return

    def _createCards(self):
        """Clear the list then create a card for every action"""
        self.cards = []
        start = time.time()
        listLayout = self.ui.actionList
        listLayout.clear()
        self.sortActions()
        if len(self.actions) >= 1:
            currentLetter = ''
            currentCategory = ''
            currentTag = ''
            currentPath = 'None'
            topScore = self.actions[0]['score']
            bottomScore = self.actions[-1]['score']
            currentScore = 0
            listLayout.setUpdatesEnabled(False)
            listLayout.blockSignals(True)
            listLayout.blockSignals(True)
            for number, action in enumerate(self.actions):
                QtWidgets.QApplication.processEvents()
                if self.sortingMethod == 'Alphabetical':
                    if action['name'][0] != currentLetter:
                        currentLetter = action['name'][0]
                        createHeader(name=currentLetter.upper(), layout=listLayout)
                if self.sortingMethod == 'Category':
                    if action['category'] != currentCategory:
                        currentCategory = action['category']
                        cleanCategoryName = cleanCategory(action['category'])
                        createHeader(name=cleanCategoryName, layout=listLayout)
                if self.sortingMethod == 'Tags':
                    if number is 0:
                        if action['tags'] == '':
                            createHeader(name='No tags', layout=listLayout)
                    if action['tags'] != currentTag:
                        currentTag = action['tags']
                        createHeader(name=currentTag, layout=listLayout)
                if self.sortingMethod == 'Path':
                    if currentPath not in action['category']:
                        currentPath = returnScriptPathOnly(action['category'])
                        createHeader(name=currentPath, layout=listLayout)
                if self.sortingMethod == 'Relevance':
                    if action['score'] == bottomScore:
                        if currentScore != action['score']:
                            createHeader(name='Never used', layout=listLayout)
                            currentScore = action['score']
                    elif action['score'] == topScore:
                        if currentScore != action['score']:
                            createHeader(name='Most Relevant', layout=listLayout)
                            currentScore = action['score']
                    elif action['score'] <= topScore * 0.8:
                        if currentScore >= topScore * 0.8:
                            createHeader(name='Somewhat Relevant', layout=listLayout)
                            currentScore = action['score']
                if 'id' not in action:
                    action['id'] = None
                card = createCard(id=action['id'], name=action['name'], command=action['command'], parent=action['category'], tags=action['tags'], icon=action['icon'], info=action['info'], layout=listLayout)
                self.cards.append(card)

            listLayout.setUpdatesEnabled(True)
            listLayout.blockSignals(False)
            listLayout.blockSignals(False)
            buildCardInView(self.ui.actionList)
            if len(self.actions) == self.totalActions:
                self.ui.statusField.setText(('{} actions').format(len(self.actions)))
            else:
                self.ui.statusField.setText(('{} actions of {} filtered').format(len(self.actions), self.totalActions))
        else:
            self.ui.statusField.setText('No actions to show for the current filter')
        return

    def openAddActionWindow(self):
        displayWindow('actionInfo')

    def sortActions(self):
        """Sort the avalible actions in self based on the method of self"""
        self.sortingMethod = self.ui.sortingField.currentText()
        sortingMethod = self.sortingMethod.lower()
        if sortingMethod == 'relevance':
            sortingMethod = 'score'
        self.actions = sortActions(self.actions, sortingMethod=sortingMethod)

    def setViewState(self, element=None, noDelay=False):
        """Open or close the specified element by reversing the current"""
        if element is None:
            element = self.sender()
        headerName = str(element.objectName())
        frameName = headerName.replace('Header', 'Frame')
        frameObject = None
        for frame in self.frameObjects:
            if frame.objectName() == frameName:
                frameObject = frame

        height = frameObject.size().height()
        width = frameObject.size().width()
        closedHeight = 0
        contentHeight = 0
        for number, child in enumerate(frameObject.children()):
            if type(child) == FlowLayout:
                contentHeight = child.heightForWidth(width)
                break
            elif type(child) == QtWidgets.QVBoxLayout:
                pass
            elif type(child) == QtWidgets.QFrame:
                if child.isHidden() is False:
                    contentHeight += child.height()
            elif type(child) == QtWidgets.QPushButton:
                if child.isHidden() is False:
                    contentHeight += child.height()
            elif type(child) == QtCore.QPropertyAnimation:
                pass
            else:
                contentHeight += child.height()

        if height == closedHeight:
            newHeight = contentHeight
            element.setIcon(QtGui.QPixmap(('{}').format(relativePath.replace('\\', '/') + 'icons/action_open.png')))
        else:
            newHeight = closedHeight
            element.setIcon(QtGui.QPixmap(('{}').format(relativePath.replace('\\', '/') + 'icons/action_closed.png')))
        if 'filter' in frameName:
            expandingMode = True
        else:
            expandingMode = False
        qtCore.animateWidgetSize(frameObject, start=(width, height), end=(width, newHeight), expanding=expandingMode)
        return

    def showEvent(self, event):
        event.accept()

    def makeDockable(self):
        self.dockedMode = True
        self.setWindowFlags(QtCore.Qt.Tool)
        self.show()
        workspaceControlName = self.objectName() + 'WorkspaceControl'
        self.setDockableParameters(dockable=True, floating=False, area='right')
        self.show(dockable=True, area='right', floating=False)
        try:
            dockedWindow = cmds.workspaceControl(workspaceControlName, e=True, ttc=['AttributeEditor', -1], wp='preferred', mw=420)
        except:
            pass

        dockedWindows.append(self)
        self.raise_()
        self.setWindowFlags(self.windowFlags() & QtCore.Qt.FramelessWindowHint)
        self.ui.scrollAreaWidgetContents.setStyleSheet('')
        self.ui.topWidget.hide()
        self.ui.frame.setStyleSheet('border-radius: 0px')
        self.ui.scrollArea.setStyleSheet('/* Main\n/* Scrollbar Vertical */\nQScrollBar:vertical\n{\nbackground-color: rgb(13, 41, 54,0);\nwidth: 10px;\n}\n\nQScrollBar::handle:vertical:hover\n{\nbackground-color: rgb(250, 250, 250,60);\n}\n\n/* Scrollbar background for top and bottom*/\nQScrollBar:sub-page:vertical,QScrollBar:add-page:vertical\n{\nbackground-color: rgb(27, 55, 69,0);\nwidth: 10px;\n}\n\n\n/* The scrollbar itself*/\nQScrollBar::handle:vertical {\n\nbackground-color: rgb(250, 250, 250,50);\nborder-radius: 4px;\nwidth: 10px;\n}\n\n\n')
        self.ui.scrollAreaWidgetContents.setStyleSheet('')


class searchWindow(QtWidgets.QDialog):

    def __init__(self, parent=None, title=None):
        super(searchWindow, self).__init__(parent)
        self.initUI()
        self.startMode()
        self.open()

    def open(self):
        global windowPosition
        self.show()
        self.ui.listWidget.setStyleSheet('QListWidget\n{\noutline: 0;\nbackground-color: rgb(0, 0, 0,0);\nborder-radius: 5px;\nborder: solid;\nborder-width:0;\n}\n\nQListWidget::item\n{\npadding: -1px;\noutline: 0;\nborder: solid;\nborder-width:0;\n}\n\nQListWidget::item:hover\n{\nbackground-color: rgb(0,0,0,10);\n}\n\nQListWidget::item:selected\n{\npadding: 0px;\nbackground-color: rgb(250,250, 250,20);\nborder-radius: 1px;\n}\n\n\n/* Scrollbar  */\nQScrollBar:vertical\n{\nbackground-color: rgb(0, 0, 0,0);\nwidth: 8px;\npadding: 0px 1px 0px 1px;\n}\n\n/* Scrollbar background for top and bottom*/\nQScrollBar:sub-page:vertical,QScrollBar:add-page:vertical\n{\nbackground-color: rgb(200,200, 200,100);\nwidth: 2px;\n}\n\n\n/* The scrollbar itself*/\nQScrollBar::handle:vertical \n{\nbackground-color: rgb(250,250,250,50);\nborder-radius: 3px;\nwidth: 10px;\npadding: 0px 0px 0px 0px;\n}\n\n/* The scrollbar itself HOVER*/\nQScrollBar::handle:vertical:hover\n{\nbackground-color: rgb(250,250,250,70);\nborder-radius: 3px;\nwidth: 10px;\npadding: 0px 0px 0px 0px;\n}\n\n/* The scrollbar itself PRESSED*/\nQScrollBar::handle:vertical:pressed\n{\nbackground-color: rgb(250,250,250,100);\nborder-radius: 3px;\nwidth: 10px;\npadding: 0px 0px 0px 0px;\n}\n\n/* Top and bottom arrows*/\nQScrollBar::add-line:vertical,QScrollBar::sub-line:vertical {\nwidth: 0px;\nheight: 0px;\n}\n\n/* Scrollbar background for top and bottom*/\nQScrollBar:sub-page:vertical,QScrollBar:add-page:vertical\n{\nbackground-color:  rgb(250, 250, 250,0);\n}')
        itemCount = self.ui.listWidget.count()
        if itemCount >= maxCardInWindow:
            itemCount = maxCardInWindow
        windowOffset = self.cardHeight * itemCount * 0.25
        qtCore.fadeWindowAnimation(start=0, end=1, duration=50, object=self)
        if windowPosition != None:
            self.move(windowPosition[0], windowPosition[1] + windowOffset)
        qtCore.slideWindowAnimation(start=30, end=-windowOffset, duration=200, object=self)
        self.ui.inputField.setFocus()
        return

    def initUI(self):
        self.cardHeight = 45
        self.windowWidth = 430
        if prefs.getGenericSettings('alwaysOn') == 'True':
            self.keepOpen = True
        else:
            self.keepOpen = False
        self.activeButton = None
        mayaPrefs = prefs.getGenericSettings('mayaCommands')
        if mayaPrefs == 'True':
            self.mayaCommands = True
        if mayaPrefs == 'False':
            self.mayaCommands = False
        self.ui = qtCore.qtUiLoader(('{}interface_search.ui').format(uiPath))
        self.setWindowOpacity(0)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.ui)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.ui.mainFrame.setStyleSheet('QFrame#mainFrame\n{\nbackground-color: rgb(' + ('{},{},{},{}').format(uicolor['R'], uicolor['G'], uicolor['B'], uicolor['A']) + ');\nborder-radius: 5px;\n}')
        colorOffset = -10
        self.ui.infoBar.setStyleSheet('QWidget#infoBar\n{\nborder-style: None;border-top-left-radius: 5px;border-top-right-radius: 5px;background-color: rgb(' + ('{},{},{},{}').format(uicolor['R'] + colorOffset, uicolor['G'] + colorOffset, uicolor['B'] + colorOffset, uicolor['A']) + ')}')
        QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), self.ui, self.fadeCloseWindow)
        QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.ui.listWidget, self.execute)
        QtWidgets.QShortcut(QtGui.QKeySequence('Space'), self.ui.listWidget, self.execute)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_1), self.ui.listWidget, lambda : self.statusButtonClicked(input='Latest'))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_2), self.ui.listWidget, lambda : self.statusButtonClicked(input='Favorites'))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_3), self.ui.listWidget, lambda : self.statusButtonClicked(input='Blacklist'))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_4), self.ui.listWidget, lambda : self.statusButtonClicked(input='Menu'))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_L), self.ui.listWidget, lambda : displayWindow('actions'))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_K), self.ui.listWidget, lambda : displayWindow('actionInfo'))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_P), self.ui.listWidget, lambda : displayWindow('setup'))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_F), self.ui.listWidget, self.toggleFavorite)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_B), self.ui.listWidget, self.toggleBlacklist)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_E), self.ui.listWidget, self.editAction)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Tab), self.ui.listWidget, self.execute)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Return), self.ui.listWidget, self.execute)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Space), self.ui.listWidget, self.execute)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.ALT + QtCore.Qt.Key_Return), self.ui.listWidget, self.execute)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.ALT + QtCore.Qt.Key_Space), self.ui.listWidget, self.execute)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_Return), self.ui.listWidget, self.execute)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_Space), self.ui.listWidget, self.execute)
        QtWidgets.QShortcut(QtGui.QKeySequence('Down'), self.ui.inputField, lambda : self.changeListIndex(1))
        QtWidgets.QShortcut(QtGui.QKeySequence('Up'), self.ui.inputField, lambda : self.changeListIndex(-1))
        self.infoLayout = self.ui.infoBar.children()[0]
        self.ui.latestButton = fadeButton(self.ui.infoBar)
        self.ui.latestButton.setText('Latest')
        self.ui.latestButton.setIcon(QtGui.QPixmap(('{}icons{}statusBar_recent.png').format(relativePath, os.sep)))
        self.infoLayout.addWidget(self.ui.latestButton)
        self.ui.favButton = fadeButton(self.ui.infoBar)
        self.ui.favButton.setText('Favorites')
        self.ui.favButton.setIcon(QtGui.QPixmap(('{}icons{}statusBar_favorite.png').format(relativePath, os.sep)))
        self.infoLayout.addWidget(self.ui.favButton)
        self.ui.blackButton = fadeButton(self.ui.infoBar)
        self.ui.blackButton.setText('Blacklist')
        self.ui.blackButton.setIcon(QtGui.QPixmap(('{}icons{}statusBar_blocked.png').format(relativePath, os.sep)))
        self.infoLayout.addWidget(self.ui.blackButton)
        self.ui.menuButton = fadeButton(self.ui.infoBar)
        self.ui.menuButton.setText('Menu')
        self.ui.menuButton.setIcon(QtGui.QPixmap(('{}icons{}statusBar_menu.png').format(relativePath, os.sep)))
        self.infoLayout.addWidget(self.ui.menuButton)
        self.ui.closeButton = fadeButton(self.ui.infoBar)
        self.ui.closeButton.setIcon(QtGui.QPixmap(('{}icons{}closeWindow_hover.png').format(relativePath, os.sep)))
        self.ui.closeButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.infoLayout.addWidget(self.ui.closeButton)
        self.ui.inputField.textChanged.connect(self.search)
        self.ui.latestButton.clicked.connect(self.statusButtonClicked)
        self.ui.favButton.clicked.connect(self.statusButtonClicked)
        self.ui.blackButton.clicked.connect(self.statusButtonClicked)
        self.ui.menuButton.clicked.connect(self.statusButtonClicked)
        self.ui.closeButton.clicked.connect(self.fadeCloseWindow)
        self.ui.infofield.clicked.connect(self.triggerInfoField)
        self.ui.listWidget.verticalScrollBar().valueChanged.connect(self.updateSelectedView)
        self.ui.listWidget.verticalScrollBar().rangeChanged.connect(self.updateSelectedView)
        self.ui.inputField.setMaximumWidth(3)
        self.ui.inputField.setMinimumWidth(3)
        self.resize(self.windowWidth, 50)
        self.setMatched(infoText='Type to search...')
        getBlacklisted()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        if menubar is False:
            self.ui.infoBar.hide()
        self.installEventFilter(self)
        return

    def editAction(self):
        currentItem = self.ui.listWidget.currentItem()
        card = currentItem.data(109)
        status = True
        if 'MAYA' in card.tags:
            status = False
        if card.special is True:
            status = False
        if status is True:
            card.editAction()
        else:
            print 'The action cant be edited'

    def updateSelectedView(self):
        buildCardInView(self.ui.listWidget)

    def statusButtonClicked(self, input=None):
        if input is None:
            sending_button = self.sender()
            name = sending_button.text()
        else:
            name = input
        inactivebuttons = [self.ui.latestButton, self.ui.favButton, self.ui.blackButton, self.ui.menuButton]
        self.activeButton = name
        if name == 'Latest':
            activeButton = inactivebuttons[0]
            self.startMode(editMode='latest')
        if name == 'Favorites':
            activeButton = inactivebuttons[1]
            self.startMode(editMode='favorites')
        if name == 'Blacklist':
            activeButton = inactivebuttons[2]
            self.displayBlackListed()
        if name == 'Menu':
            activeButton = inactivebuttons[3]
            self.displayMenu()
        if name == 'None':
            activeButton = None
        if name != 'None':
            inactivebuttons.remove(activeButton)
        for button in inactivebuttons:
            qtCore.fadeAnimation(start='current', end=0.3, duration=300, object=button.opacityEffect)
            button.activeButton = False

        if activeButton != None:
            qtCore.fadeAnimation(start='current', end=1, duration=50, object=activeButton.opacityEffect)
            activeButton.activeButton = True
        return

    def startMode(self, editMode=False):
        favoriteActionsList = prefs.getList('favoriteList')
        latestActionsList = prefs.getList('latestList')
        self.mode = prefs.getGenericSettings('listMode')
        if editMode != False:
            self.mode = editMode
        if self.mode == 'favorites':
            header = 'Favorite Actions'
            list = favoriteActionsList
            activeButton = self.ui.favButton
        else:
            header = 'Latest Actions'
            list = latestActionsList
            activeButton = self.ui.latestButton
        if editMode != False:
            prefs.writegenericSettings('listMode', editMode)
        else:
            qtCore.fadeAnimation(start='current', end=1, duration=1000, object=activeButton.opacityEffect)
            activeButton.activeButton = True
        self.displayItems(list)
        self.activeButton = self.mode
        self.setMatched(infoText=header, iconPath=menuLogo)

    def setMatched(self, iconPath='', infoText=None):
        if infoText == None:
            currentItem = self.ui.listWidget.currentItem()
            if self.ui.listWidget.count() >= 1:
                card = currentItem.data(109)
                name = card.getTitle()
                iconPath = card.getIconPath()
                self.ui.mainIcon.setIcon(QtGui.QPixmap(returnIconPath(iconPath)))
            else:
                name = ' - No matches - '
                iconPath = menuLogo
        else:
            name = infoText
            iconPath = iconPath
        self.ui.infofield.setText(name)
        self.ui.mainIcon.setIcon(QtGui.QPixmap(returnIconPath(iconPath)))
        return

    def triggerInfoField(self):
        self.ui.inputField.setText('')
        self.ui.inputField.setFocus()

    def search(self, currentSearch, noDelay=False):
        if self.activeButton != 'None':
            self.statusButtonClicked(input='None')
        start = time.time()
        self.results = []
        qtCore.autoFieldWidth(self.ui.inputField, offset=5)
        matchedIcon = menuLogo
        matchedText = ''
        if ':' in currentSearch:
            if 'cosmos:' in currentSearch:
                search = currentSearch.split(':')[-1]
                self.results = filterSearch(mayaCommands=False, search=search)
            elif 'maya:' in currentSearch:
                search = currentSearch.split(':')[-1]
                self.results = filterSearch(mayaCommands=True, search=search, filterCategory='category', filterSearch='')
            elif currentSearch == 'category:':
                for category in library.cosmosCategories:
                    category = cleanCategory(category)
                    self.results.append({'category': category, 'name': category, 'id': 'COSMOS', 'info': ' ', 'icon': ('{}icons{}actionList.png').format(relativePath, os.sep), 'command': unicode(("cosmos.search('category:{}:')").format(category), 'utf-8'), 'tags': 'None'})

        else:
            if len(currentSearch) >= 2:
                splittedSearch = library.splitSearchQuery(currentSearch)
                self.results = filterActions(search=splittedSearch['search'], mayaCommands=self.mayaCommands, tags=splittedSearch['tags'], categories=splittedSearch['categories'])
                self.results = removeBlacklisted(self.results)
                self.results = sortActions(actions=self.results, prefered=currentSearch)
        if noDelay is False:
            if len(self.results) >= 1:
                firstItem = self.results[0]
                matchedIcon = firstItem['icon']
                matchedText = firstItem['name']
            else:
                if len(currentSearch) == 0:
                    matchedText = 'Type to search...'
                    self.startMode()
                try:
                    self.timer.stop()
                except:
                    pass

            if len(currentSearch) != 0:
                self.timer = QtCore.QTimer(singleShot=True)
                self.timer.timeout.connect(lambda : self.displayItems(self.results))
                self.timer.start(50)
                self.setMatched(infoText=matchedText, iconPath=matchedIcon)
        end = time.time()

    def displayItems(self, inputList):
        getFavorites()
        if self.ui.listWidget.count() >= 1:
            self.ui.listWidget.clear()
        listLayout = self.ui.listWidget
        if type(inputList) == list:
            for number, item in enumerate(inputList[:maxResultCount]):
                if 'altCommand' in item:
                    altCommand = item['altCommand']
                else:
                    altCommand = None
                if 'id' in item:
                    id = item['id']
                else:
                    id = None
                if 'score' in item:
                    score = item['score']
                else:
                    score = None
                createCard(name=item['name'], info=item['info'], command=item['command'], altCommand=altCommand, icon=item['icon'], parent=item['category'], layout=listLayout, tags=item['tags'], setIcon=True, id=id, score=score)

            qtCore.selectItem(self.ui.listWidget, 0)
        buildCardInView(listLayout)
        self.setWindowSize()
        self.setMatched()
        return

    def displayBlackListed(self):
        self.ui.listWidget.clear()
        self.displayItems(library.blacklistedCommands)
        self.setMatched(infoText='Blacklisted Actions', iconPath=menuLogo)

    def displayMenu(self):
        self.ui.listWidget.clear()
        self.setMatched(infoText='Cosmos Menu', iconPath=menuLogo)
        createCard(name='Add Action', command='cosmos.displayWindow("actionInfo")', icon=('{}icons{}actionsAddAction.png').format(relativePath, os.sep), info='Add your own script', layout=self.ui.listWidget, setIcon=True, id='COSMOS', absoluteIcon=True)
        createCard(name='ActionList', command='cosmos.displayWindow("actions")', icon=('{}icons{}actionActionsList.png').format(relativePath, os.sep), info='View and filter actions', layout=self.ui.listWidget, setIcon=True, id='COSMOS', absoluteIcon=True)
        createCard(name='Settings', command='cosmos.displayWindow("setup")', icon=('{}icons{}actionSettings.png').format(relativePath, os.sep), info='Open Settings', layout=self.ui.listWidget, setIcon=True, id='COSMOS', absoluteIcon=True)
        createCard(name='Rescan', command='cosmos.rescan()', icon=('{}icons{}actionScan.png').format(relativePath, os.sep), info='Scan your external changes', layout=self.ui.listWidget, setIcon=True, id='COSMOS', absoluteIcon=True)
        createCard(name='Help/Feedback', command="cosmos.browser('http://cosmos.toolsfrom.space/documentation/')", icon=('{}icons{}actionHelp.png').format(relativePath, os.sep), info='Open the documentation', layout=self.ui.listWidget, setIcon=True, id='COSMOS', absoluteIcon=True)
        createCard(name='Tutorial', command='cosmos.displayWindow("tutorial")', icon=('{}icons{}actionTutorial.png').format(relativePath, os.sep), info='Show introduction tutorial again', layout=self.ui.listWidget, setIcon=True, id='COSMOS', absoluteIcon=True)
        createCard(name='Donate', command="cosmos.browser('https://www.paypal.me/deerstranger/5')", icon=('{}icons{}actionHeart.png').format(relativePath, os.sep), info='If you like this, please consider helping out', layout=self.ui.listWidget, setIcon=True, id='COSMOS', absoluteIcon=True)
        self.updateSelectedView()
        self.setWindowSize()
        qtCore.selectItem(self.ui.listWidget, 0)

    def changeListIndex(self, input):
        currentItem = self.ui.listWidget.currentItem()
        if self.ui.listWidget.count() >= 1:
            currentIndex = self.ui.listWidget.indexFromItem(currentItem)
            currentNumber = currentIndex.row()
            if currentNumber + input >= 0:
                if currentNumber + input + 1 >= self.ui.listWidget.count() + 1:
                    newItem = self.ui.listWidget.item(0)
                else:
                    newItem = self.ui.listWidget.item(currentNumber + input)
            if currentNumber + input == -1:
                newItem = self.ui.listWidget.item(self.ui.listWidget.count() - 1)
            self.ui.listWidget.setCurrentItem(newItem)
            self.setMatched()

    def setWindowSize(self):
        currentSize = self.size()
        oldwindowWidth = currentSize.width()
        inputField = self.ui.inputField.height()
        infobar = 0
        if self.ui.infoBar.isHidden() is False:
            infobar = self.ui.infoBar.height()
        list = self.ui.listWidget.count() * self.cardHeight
        padding = inputField + infobar
        newWindowHeight = padding + list
        maxItems = maxCardInWindow
        maxHeight = padding + self.cardHeight * maxItems
        if newWindowHeight >= maxHeight:
            newWindowHeight = maxHeight
        qtCore.resizeWindowAnimation(start=(currentSize.width(), currentSize.height()), end=(
         currentSize.width(), newWindowHeight), duration=200, object=self, attribute='size')
        if self.ui.listWidget.count() >= maxCardInWindow:
            self.ui.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        else:
            self.ui.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def resizeEvent(self, event):
        self.repaint()

    def toggleFavorite(self):
        currentItem = self.ui.listWidget.currentItem()
        if self.ui.listWidget.count() >= 1:
            currentSearch = self.ui.inputField.text()
            try:
                card = currentItem.data(109)
            except:
                card = None

            if card != None:
                special = card.special
                if special is False:
                    card.saveFavorite()
        return

    def toggleBlacklist(self):
        currentItem = self.ui.listWidget.currentItem()
        curentIndex = self.ui.listWidget.currentRow()
        if self.ui.listWidget.count() >= 1:
            currentSearch = self.ui.inputField.text()
            try:
                card = currentItem.data(109)
            except:
                card = None

            if card != None:
                special = card.special
                if special is False:
                    getBlacklisted()
                    blackListed = False
                    if len(library.blacklistedCommands) >= 1:
                        for number, blacklisted in enumerate(library.blacklistedCommands):
                            if card.name in blacklisted['name']:
                                if card.category in blacklisted['category']:
                                    if card.description in blacklisted['info']:
                                        blackListed = True

                    if blackListed:
                        prefs.removeListItem('blackList', card.name, card.category, card.description)
                    else:
                        prefs.addBlacklisted(card)
                    self.setWindowSize()
                    getBlacklisted()
                    if self.activeButton == 'None' or self.activeButton == 'Blacklist':
                        self.ui.listWidget.takeItem(curentIndex)
                    windowInstances = returnInstances(genericDockingWindow)
                    for window in windowInstances:
                        try:
                            if window.ui.checkbox_blacklisted.isChecked() == True:
                                window.filter()
                        except:
                            pass

        return

    def execute(self):
        currentItem = self.ui.listWidget.currentItem()
        if self.ui.listWidget.count() >= 1:
            currentSearch = self.ui.inputField.text()
            card = currentItem.data(109)
            name = card.name
            category = card.getCategory()
            id = card.getId()
            special = card.special
            result = executeCard(card)
            if result == 'success':
                if special == False:
                    prefs.addRecentSearch(card)
                    if len(currentSearch) >= 1:
                        if id is None:
                            prefs.savePreferedSearch(currentSearch, name + '@' + category)
                        else:
                            prefs.savePreferedSearch(currentSearch, name)
                    if prefs.getGenericSettings('alwaysOn') == 'False':
                        self.tryClose()
                    else:
                        self.activateWindow()
        return

    def tryClose(self):
        if prefs.getGenericSettings('alwaysOn') == 'False':
            modifierKeys = QtWidgets.QApplication.keyboardModifiers()
            if modifierKeys == QtCore.Qt.ShiftModifier:
                self.activateWindow()
            elif modifierKeys == QtCore.Qt.ShiftModifier | QtCore.Qt.AltModifier:
                self.activateWindow()
            else:
                self.fadeCloseWindow()

    def fadeCloseWindow(self):
        qtCore.slideWindowAnimation(start=0, end=200, duration=100, object=self)
        self.deleteLater()
        self.timer = QtCore.QTimer(singleShot=True)
        self.timer.timeout.connect(self.deleteWindow)
        self.timer.start(300)

    def deleteWindow(self):
        del self

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        global windowPosition
        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
            windowPosition = [
             self.pos().x(), self.pos().y()]
        except:
            return 'Something'

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.GrabMouse:
            return QtWidgets.QMainWindow.eventFilter(self, object, event)
        if event.type() == QtCore.QEvent.WindowActivate or event.type() == QtCore.QEvent.Enter:
            self.activateWindow()
            return QtWidgets.QMainWindow.eventFilter(self, object, event)
        if event.type() == QtCore.QEvent.WindowDeactivate:
            try:
                self.tryClose()
            except:
                pass

            return QtWidgets.QMainWindow.eventFilter(self, object, event)
        if event.type() == QtCore.QEvent.FocusIn:
            return QtWidgets.QMainWindow.eventFilter(self, object, event)
        if event.type() == QtCore.QEvent.FocusOut:
            self.fadeCloseWindow()
            return QtWidgets.QMainWindow.eventFilter(self, object, event)
        return QtWidgets.QMainWindow.eventFilter(self, object, event)


class createCategoryWindow(genericWindow):

    def __init__(self, parent=None):
        interfacePath = ('{}interface_createCategory.ui').format(uiPath)
        super(createCategoryWindow, self).__init__(interfacePath, parent)
        try:
            exec 'createCategory_openWindow.close()'
        except:
            pass

        self.editMode = False
        self.activePath = None
        self.scriptPath = prefs.getGenericSettings('scriptPath')
        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.appendCategoryToList)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setModal(1)
        self.show()
        return

    def fillCategories(self, scriptPath):
        self.activePath = scriptPath
        categories = library.getCategories(self.activePath)
        self.ui.categoryList.addItem('- None -')
        for category in categories:
            self.ui.categoryList.addItem(cleanCategory(category))

    def appendCategoryToList(self):
        newCategoryName = self.ui.nameField.text()
        subCategory = self.ui.categoryList.currentText()
        if subCategory != '- None -':
            newCategoryName = subCategory + os.sep + newCategoryName
        if len(newCategoryName) >= 2:
            status = True
            for category in library.getCategories(self.activePath):
                if newCategoryName == cleanCategory(category):
                    displayViewMessage(text='Category already exists', mode='error')
                    self.ui.nameLabel.setStyleSheet('color: rgb(206, 69, 31,255);')
                    self.ui.nameLabel.setText('Choose a name not already taken:')
                    status = False

            if status is True:
                windowInstances = returnInstances(actionInfoWindow)
                for window in windowInstances:
                    window.fillCategoryInterface(append=newCategoryName)

                self.close()
        else:
            self.ui.nameLabel.setStyleSheet('color: rgb(186, 49, 31,240);')
            self.ui.nameLabel.setText('Category Name please:')


class actionInfoWindow(genericWindow):

    def __init__(self, parent=None, title=None):
        interfacePath = ('{}interface_action.ui').format(uiPath)
        super(actionInfoWindow, self).__init__(interfacePath, parent)
        self.resize(430, 390)
        self.editMode = False
        self.action = None
        self.setWindowTitle('Cosmos Action')
        self.ui.saveButton.clicked.connect(self.saveAction)
        self.ui.testButton.clicked.connect(self.testAction)
        self.ui.openFolderButton.clicked.connect(self.openLocation)
        self.ui.bigIcon.clicked.connect(self.pickIcon)
        self.ui.addCategoryButton.clicked.connect(self.displayCategory)
        self.ui.deleteButton.clicked.connect(self.deleteActionQuestion)
        self.ui.addTagButton.clicked.connect(self.displayTagsField)
        self.ui.tagsField.editingFinished.connect(self.ui.tagsButtonLayout.show)
        self.ui.tagsField.editingFinished.connect(self.ui.tagsField.hide)
        self.ui.tagsField.editingFinished.connect(self.convertTags)
        self.ui.pathField.currentIndexChanged.connect(lambda : self.fillCategoryInterface())
        for field in [self.ui.nameField, self.ui.descriptionField, self.ui.tagsField, self.ui.iconField, self.ui.scriptContentField]:
            field.textChanged.connect(self.updateField)

        self.ui.tagsField.hide()
        self.ui.openFolderButton.hide()
        self.ui.iconFieldFrame.hide()
        self.ui.deleteButton.hide()
        self.ui.iconFieldCloseButton.clicked.connect(self.ui.iconFieldFrame.hide)
        self.addOpacityEffect = QtWidgets.QGraphicsOpacityEffect(self)
        self.ui.addPopup.setGraphicsEffect(self.addOpacityEffect)
        self.ui.addPopup.setAutoFillBackground(True)
        self.addOpacityEffect.setOpacity(0)
        self.testOpacityEffect = QtWidgets.QGraphicsOpacityEffect(self)
        self.ui.testPopup.setGraphicsEffect(self.testOpacityEffect)
        self.ui.testPopup.setAutoFillBackground(True)
        self.testOpacityEffect.setOpacity(0)
        self.ui.scriptContentField.setTabStopWidth(35)
        self.scriptPathList = prefs.getGenericSettings('scriptPath').split(';')
        for path in self.scriptPathList:
            self.ui.pathField.addItem(path)

        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_T), self.ui, self.displayTagsField)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_F), self.ui, self.ui.iconFieldFrame.show)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S), self.ui, self.saveAction)
        self.setAcceptDrops(True)
        if any(('cosmosPrefs' in item for item in self.scriptPathList)) == True:
            match = [ item for item in self.scriptPathList if 'cosmosPrefs' in item ][0]
            matchIndex = self.ui.pathField.findText(match)
            self.ui.pathField.setCurrentIndex(matchIndex)
        else:
            self.fillCategoryInterface(setUser=True)
        self.ui.bigIcon.setIcon(QtGui.QPixmap(('{}').format(relativePath.replace('\\', '/') + 'icons/addIcon.png')))
        self.show()
        return

    def displayCategory(self):
        displayWindow('createCategory')
        windowInstances = returnInstances(createCategoryWindow)
        windowInstances[0].fillCategories(self.ui.pathField.currentText())

    def attachAction(self, actionId):
        self.action = library.getActionById(actionId)
        if self.action != None:
            self.actionFile = library.getActionPathById(actionId)
            actionScriptPath = returnScriptPathOnly(self.actionFile)
            self.ui.nameField.setText(self.action['name'])
            self.ui.descriptionField.setText(self.action['info'])
            self.ui.tagsField.setText(self.action['tags'])
            self.convertTags()
            self.ui.iconField.setText(self.action['icon'])
            self.ui.bigIcon.setIcon(QtGui.QPixmap(loadActionIcon(self.action['icon'])))
            for path in self.scriptPathList:
                if actionScriptPath in path:
                    userIndex = self.ui.pathField.findText(actionScriptPath)
                    self.ui.pathField.setCurrentIndex(userIndex)
                    break

            self.fillCategoryInterface(setItem=cleanCategory(self.action['category']))
            self.scriptExstension = self.action['syntax']
            if self.scriptExstension == 'mel':
                self.ui.melButton.setChecked(1)
            if self.scriptExstension == 'python':
                self.ui.pythonButton.setChecked(1)
            self.ui.scriptContentField.clear()
            self.ui.scriptContentField.insertPlainText(self.action['command'])
            self.ui.deleteButton.show()
            self.ui.openFolderButton.show()
            self.ui.saveButton.setText('Save Changes')
            self.editMode = False
        return

    def displayTagsField(self):
        currentTagsText = self.ui.tagsField.text()
        currentTagsText = currentTagsText.replace(', ', ',')
        currentTagsText = currentTagsText.replace(',,', ',')
        if len(currentTagsText) >= 1:
            if currentTagsText[-1] != ',':
                currentTagsText = currentTagsText + ','
        self.ui.tagsField.setText(currentTagsText)
        self.ui.tagsButtonLayout.hide()
        self.ui.tagsField.show()
        self.ui.tagsField.setFocus()

    def convertTags(self):
        tags = self.ui.tagsField.text().split(',')
        layout = self.ui.tagsButtonLayout.children()[0]
        for number, object in enumerate(self.ui.tagsButtonLayout.children()):
            if 'tagItem' in object.objectName():
                object.deleteLater()

        for tagName in tags[::-1]:
            if len(tagName) >= 3:
                button = tagButton()
                button.setTitle(tagName)
                button.clicked.connect(self.ui.tagsButtonLayout.hide)
                button.clicked.connect(self.ui.tagsField.show)
                button.clicked.connect(self.ui.tagsField.setFocus)
                layout.insertWidget(0, button)
                removeButton = tagButton()
                removeButton.tag = tagName
                removeButton.closeMode()
                removeButton.clicked.connect(self.removeTag)
                layout.insertWidget(1, removeButton)

    def removeTag(self):
        tag = self.sender()
        tagName = tag.tag
        currentTagsText = self.ui.tagsField.text()
        currentTagsText = currentTagsText.replace(tagName, '')
        currentTagsText = currentTagsText.replace(',,', ',')
        if len(currentTagsText) >= 1:
            if currentTagsText[-1] == ',':
                currentTagsText = currentTagsText[:-1]
        self.ui.tagsField.setText(currentTagsText)
        self.convertTags()

    def fillCategoryInterface(self, append=None, setUser=False, setItem=False):
        self.ui.listField.clear()
        activePath = self.ui.pathField.currentText()
        if append != None:
            self.ui.listField.addItem(append)
        categories = library.getCategories(activePath)
        for category in categories:
            self.ui.listField.addItem(cleanCategory(category))

        if setUser == True:
            for category in library.getCategories(activePath):
                if 'user' in category:
                    userIndex = self.ui.listField.findText('user')
                    if userIndex >= 0:
                        self.ui.listField.setCurrentIndex(userIndex)
                    else:
                        self.ui.listField.setCurrentIndex(0)
                    break

        if setItem != False:
            for category in library.getCategories(activePath):
                if setItem in category:
                    userIndex = self.ui.listField.findText(setItem)
                    self.ui.listField.setCurrentIndex(userIndex)
                    break

        return

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
            self.ui.frame.setStyleSheet('border-radius: 5px;\nbackground-color: rgb(' + ('{},{},{},{}').format(uicolor['R'] + 20, uicolor['G'] + 20, uicolor['B'] + 20, uicolor['A']) + ');')

    def dragLeaveEvent(self, e):
        self.ui.frame.setStyleSheet('border-radius: 5px;\nbackground-color: rgb(' + ('{},{},{},{}').format(uicolor['R'], uicolor['G'], uicolor['B'], uicolor['A']) + ');')

    def dropEvent(self, event):
        self.ui.frame.setStyleSheet('border-radius: 5px;\nbackground-color: rgb(' + ('{},{},{},{}').format(uicolor['R'], uicolor['G'], uicolor['B'], uicolor['A']) + ');')
        droppedCommand = event.mimeData().text()
        mayaShelf = mel.eval('global string $gShelfTopLevel; $temp=$gShelfTopLevel;')
        currentTab = cmds.shelfTabLayout(mayaShelf, q=True, selectTab=True)
        buttons = cmds.layout(currentTab, q=True, ca=True)
        for button in buttons:
            if 'separator' not in button:
                if cmds.shelfButton(button, q=True, command=True) == droppedCommand:
                    name = cmds.shelfButton(button, q=True, label=True)
                    info = cmds.shelfButton(button, q=True, annotation=True)
                    command = cmds.shelfButton(button, q=True, command=True)
                    image = cmds.shelfButton(button, q=True, image1=True)
                    language = cmds.shelfButton(button, q=True, stp=True)
                    if len(name) >= 40:
                        if len(info) >= 5:
                            if len(info) <= 40:
                                name = info
                            else:
                                name = ''
                        else:
                            name = ''
                    for iconName in cmds.resourceManager(nameFilter='*'):
                        if iconName == image:
                            image = (':{}').format(image.split('.')[0])

                    self.ui.scriptContentField.clear()
                    self.ui.scriptContentField.insertPlainText(command)
                    self.ui.nameField.setText(name)
                    self.ui.descriptionField.setText(info)
                    self.ui.tagsField.setText(currentTab)
                    self.ui.iconField.setText(image)
                    self.ui.bigIcon.setIcon(QtGui.QPixmap(image))
                    self.convertTags()
                    if language == 'mel':
                        self.ui.melButton.setChecked(1)
                    if language == 'python':
                        self.ui.pythonButton.setChecked(1)

    def deleteActionQuestion(self):
        self.ui.deleteButton.setText('Press again to Delete')
        self.timer = QtCore.QTimer(singleShot=True)
        self.timer.timeout.connect(lambda : self.ui.deleteButton.clicked.connect(self.deleteAction))
        self.timer.start(50)
        self.ui.deleteButton.setStyleSheet('QPushButton\n{\n\nbackground-color: rgb(186, 49, 31,240);\ncolor: rgb(250, 250, 250);\nborder-radius: 5px;\npadding: 2px;\n}\n\nQPushButton:hover\n{\n\nbackground-color: rgb(196, 59, 41,240);\n}\n\nQPushButton:pressed\n{\n\nbackground-color: rgb(176, 39, 21,240);\n}')

    def deleteAction(self):
        result = library.removeActionByFile(self.actionFile)
        self.fadeCloseWindow()

    def updateField(self, hello=None, input=None, mode='reset', *args):
        self.editMode = True
        characterString = '\'"*'
        if mode == 'error':
            color = 'rgb(255,84,0)'
        else:
            if mode == 'reset':
                color = 'rgb(0,0,0, 0)'
        styleSheetString = 'QLineEdit:focus\n{\nbackground-color: rgb(0, 0, 0,50);\n}\n\nQLineEdit\n{\nbackground-color: rgb(0, 0, 0,0);\ncolor: rgb(200, 200, 200);\npadding: 5px;\nborder-radius: 5px;\nborder-style: solid;\nborder-color: ' + color + ';\nborder-width: 1px;\n}'
        if input == None:
            sending_button = self.sender()
        if input == 'name':
            self.ui.nameField.setStyleSheet(styleSheetString)
            text = self.ui.nameField.text()
            qtCore.autoFieldWidth(self.ui.nameField, offset=15, minimum=80)
            for character in characterString:
                if character in text:
                    self.ui.nameField.setText(text.replace(character, ''))

        else:
            if input == 'description':
                self.ui.descriptionField.setStyleSheet(styleSheetString)
                text = self.ui.descriptionField.text()
                qtCore.autoFieldWidth(self.ui.descriptionField, offset=15, minimum=80)
                for character in characterString:
                    if character in text:
                        self.ui.descriptionField.setText(text.replace(character, ''))

            else:
                if input == 'category':
                    styleSheetString = '\ufeffQComboBox\n{\nbackground-color: rgb(0, 0, 0,50);\ncolor: rgb(200, 200, 200);\npadding-left: 4px;\nborder-top-left-radius: 5px;\nborder-top-right-radius: 0px;\nborder-bottom-left-radius: 5px;\nborder-bottom-right-radius: 0px;\nborder-style: solid;\nborder-color: ' + color + ';\nborder-width: 1px;\n}\n\nQComboBox QAbstractItemView {\ncolor: rgb(200, 200, 200);\n}\n\nQComboBox::item {\nborder: 0px solid black;\nmin-height: 35px; \n}\n\n\n/* #Items */\nQListView::item {\nmin-height: 35px; \nborder: solid;\nborder-width:1;\n}\n\n\n\n\n\n/* Button when open*/\n\nQComboBox:!editable:on, QComboBox::drop-down:editable:on {\nbackground-color: rgb(0, 0, 0,50);\ncolor: rgb(200, 200, 200);\npadding-left: 4px;\n\n}\n\n/* Normal arrow look*/\n\nQComboBox::down-arrow\n{\n\tmargin-top: 4px;\n\tborder-left: 7px solid rgb(27, 42, 50,0);\n\tborder-right: 7px solid rgb(27, 42, 50,0);\n\tborder-bottom: 7px solid rgb(27, 42, 50,0);\n\tborder-top: 6px solid  rgb(200,200, 200);\n}\n\n/* Arrow on open*/\n\nQComboBox:down-arrow:on\n{\n\tmargin-bottom: 4px;\n\tborder-left: 7px solid rgb(27, 42, 50,0);\n\tborder-right: 7px solid rgb(27, 42, 50,0);\n\tborder-top: 7px solid rgb(27, 42, 50,0);\n\tborder-bottom: 6px solid  rgb(200,200, 200);\n}\n\n/* Arrow background */\n\nQComboBox::drop-down {\n    subcontrol-origin: padding;\n    subcontrol-position: top right;\n\tpadding-right: 10px;\nborder-bottom-left-radius: 5px;\nborder-top-left-radius: 5px;\nborder-bottom-right-radius: 0px;\nborder-top-right-radius: 0px;\n}\n\n\n\n\n/* Scrollbar  */\nQScrollBar:vertical\n{\nbackground-color: rgb(0, 0, 0,0);\nwidth: 8px;\n}\n\n/* Scrollbar background for top and bottom*/\nQScrollBar:sub-page:vertical,QScrollBar:add-page:vertical\n{\nbackground-color: rgb(200,200, 200,100);\nwidth: 6px;\n}\n\n\n/* The scrollbar itself*/\nQScrollBar::handle:vertical \n{\nbackground-color: rgb(250,250,250,150);\nborder-radius: 4px;\nwidth: 8px;\n}\n\n/* Top and bottom arrows*/\nQScrollBar::add-line:vertical,QScrollBar::sub-line:vertical {\nwidth: 0px;\nheight: 0px;\n}\n\n/* Scrollbar background for top and bottom*/\nQScrollBar:sub-page:vertical,QScrollBar:add-page:vertical\n{\nbackground-color:  rgb(250, 250, 250,0);\n}'
                    self.ui.listField.setStyleSheet(styleSheetString)
                else:
                    if input == 'tags':
                        self.ui.tagsField.setStyleSheet(styleSheetString)
                        text = self.ui.tagsField.text()
                        for character in characterString:
                            if character in text:
                                self.ui.tagsField.setText(text.replace(character, ''))

                    else:
                        if input == 'icon':
                            self.ui.bigIcon.setStyleSheet(styleSheetString)
                        else:
                            if input == 'script':
                                styleSheetString = 'QPlainTextEdit\n{\nbackground-color: rgb(0, 0, 0,50);\ncolor: rgb(180,180,180);\npadding: 5px;\nborder-style: solid;\nborder-color: ' + color + ';\nborder-width: 1px;\n}\n/* Scrollbar  */\nQScrollBar:vertical\n{\nbackground-color: rgb(0, 0, 0,50);\nwidth: 8px;\n}\n\n/* Scrollbar background for top and bottom*/\nQScrollBar:sub-page:vertical,QScrollBar:add-page:vertical\n{\nbackground-color: rgb(200,200, 200,100);\nwidth: 6px;\n}\n\n\n/* The scrollbar itself*/\nQScrollBar::handle:vertical \n{\nbackground-color: rgb(250,250,250,150);\nborder-radius: 4px;\nwidth: 8px;\n}\n\n/* Top and bottom arrows*/\nQScrollBar::add-line:vertical,QScrollBar::sub-line:vertical {\nwidth: 0px;\nheight: 0px;\n}\n\n/* Scrollbar background for top and bottom*/\nQScrollBar:sub-page:vertical,QScrollBar:add-page:vertical\n{\nbackground-color:  rgb(250, 250, 250,0);\n}'
                                self.ui.scriptContentField.setStyleSheet(styleSheetString)
                            else:
                                if sending_button.objectName() == 'scriptContentField':
                                    self.updateField(input='script', mode=mode)
                                else:
                                    if sending_button.objectName() == 'nameField':
                                        self.updateField(input='name', mode=mode)
                                    else:
                                        if sending_button.objectName() == 'descriptionField':
                                            self.updateField(input='description', mode=mode)
                                        else:
                                            sending_button.setStyleSheet(styleSheetString)
        return

    def animatePopup(self, input, message, mode):
        if input == 'test':
            element = self.ui.testPopup
            elementEffect = self.testOpacityEffect
            self.ui.testPopup.setText(message)
            testTimer = QtCore.QTimer(singleShot=True)
            self.timer = testTimer
        if input == 'add':
            element = self.ui.addPopup
            elementEffect = self.addOpacityEffect
            self.ui.addPopup.setText(message)
            addTimer = QtCore.QTimer(singleShot=True)
            self.timer = addTimer
        if mode == 'error':
            element.setStyleSheet('color: rgb(255, 84, 0);')
        else:
            if mode == 'reset':
                element.setStyleSheet('color: rgb(160, 160, 160);')
        qtCore.fadeAnimation(start=0, end=1, duration=800, object=elementEffect)
        self.timer.timeout.connect(lambda : qtCore.fadeAnimation(start='current', end=0, duration=500, object=elementEffect))
        self.timer.start(1500)

    def openLocation(self):
        print 'Opening location for Action:', self.actionFile
        actionScriptPath = os.path.dirname(self.actionFile)
        prefs.openFolder(self.actionFile)

    def testAction(self):
        if self.testOpacityEffect.opacity >= 0.5:
            qtCore.fadeAnimation(start='current', end=0, duration=200, object=self.testOpacityEffect)
        exec 'cmds.undoInfo(openChunk=True)'
        script = self.ui.scriptContentField.toPlainText().encode('utf-8')
        tempFile = tempfile.TemporaryFile()
        tempFile.write(script)
        tempFile.seek(0)
        script = tempFile.read()
        tempFile.close()
        status = True
        if script == '':
            self.updateField('', input='script', mode='error')
            status = False
        if status == True:
            scriptType = 'python'
            if self.ui.melButton.isChecked() == True:
                scriptType = 'mel'
            try:
                if scriptType is 'python':
                    executePython(script)
                else:
                    executeMel(script)
                self.animatePopup('test', 'No errors found ', 'reset')
                displayViewMessage(text=('Sucefully executed {} script').format(scriptType))
            except Exception as errorMessage:
                self.animatePopup('test', str(errorMessage), 'error')
                displayViewMessage(text=str(errorMessage), mode='error')
                logger.error(('Adding Action problem: {}').format(errorMessage))
                raise

        else:
            self.animatePopup('test', 'No code found...', 'error')
        exec 'cmds.undoInfo(closeChunk=True)'

    def saveAction(self):
        status = True
        name = self.ui.nameField.text()
        description = self.ui.descriptionField.text()
        tags = self.ui.tagsField.text()
        iconPath = self.ui.iconField.text()
        script = self.ui.scriptContentField.toPlainText()
        actionPath = self.ui.pathField.currentText()
        category = self.ui.listField.currentText()
        categoryPath = actionPath + category
        if self.ui.melButton.isChecked() is True:
            format = 'mel'
        else:
            format = 'python'
        if name == '':
            self.updateField('', input='name', mode='error')
            status = False
        if description == '':
            self.updateField('', input='description', mode='error')
            status = False
        if script == '':
            self.updateField('', input='script', mode='error')
            status = False
        if category == '':
            self.updateField('', input='category', mode='error')
            status = False
        if status == True:
            filterList = '\'$#}";@`>'
            safe = True
            character = ''
            for filter in filterList:
                if filter in name:
                    character = filter
                    safe = 'Name'
                    self.updateField(input='name', mode='error')
                elif filter in description:
                    character = filter
                    safe = 'Description'
                    self.updateField(input='description', mode='error')
                elif filter in tags:
                    character = filter
                    safe = 'Tags'
                    self.updateField(input='tags', mode='error')

            if safe is True:
                if not os.path.exists(categoryPath):
                    os.makedirs(categoryPath)
                    prefs.writeCategory(categoryPath)
                if self.action is None:
                    status = library.writeAction(name=name, info=description, tags=tags, icon=iconPath, command=script, syntax=format, location=categoryPath)
                else:
                    updatedCategoryStatus = False
                    updatedTagsStatus = self.action['tags'] != tags
                    updatedNameStatus = self.action['name'] != name
                    updatedInfoStatus = self.action['info'] != description
                    updatedIconStatus = self.action['icon'] != iconPath
                    library.editAction(file=self.actionFile, name=name, info=description, tags=tags, icon=iconPath, command=script, syntax=format)
                    prefs.updateList(listName='favoriteList', oldName=self.action['name'], name=name, info=description, tags=tags, iconPath=iconPath)
                    prefs.updateList(listName='latestList', oldName=self.action['name'], name=name, info=description, tags=tags, iconPath=iconPath)
                    if cleanCategory(self.action['category']) != category:
                        oldFile = self.actionFile
                        newPath = actionPath + os.sep + category
                        if not os.path.exists(newPath):
                            os.makedirs(newPath)
                        shutil.move(oldFile, newPath)
                        updatedCategoryStatus = True
                if status == True:
                    if self.action is None:
                        displayViewMessage(text=("'{}' was added to your Actionsfolder").format(name))
                        logger.info(('New action added: "{}" in {}').format(name, category))
                    else:
                        displayViewMessage(text=("'{}' updated").format(name))
                        logger.info(('Action updated: "{}" in {}').format(name, category))
                    self.editMode = False
                    getContent()
                    windowInstances = returnInstances(genericDockingWindow)
                    if self.action is None:
                        for window in windowInstances:
                            window.getActionProperties()
                            window.filter()

                    else:
                        updatedName = None
                        updatedCategory = None
                        updatedCommand = None
                        updatedTags = None
                        updatedIcon = None
                        updatedInfo = None
                        if updatedNameStatus is True:
                            updatedName = name
                        if updatedTagsStatus is True:
                            updatedTags = tags
                        if updatedInfoStatus is True:
                            updatedInfo = description
                        if updatedIconStatus is True:
                            updatedIcon = iconPath
                        if updatedCategoryStatus is True:
                            updatedCategory = categoryPath
                        for window in windowInstances:
                            if updatedTagsStatus or updatedCategoryStatus:
                                window.getActionProperties()
                            if updatedNameStatus or updatedTagsStatus or updatedInfoStatus or updatedIconStatus or updatedCategoryStatus:
                                window.updateCard(self.action['name'], setName=updatedName, setCategory=updatedCategory, setTags=updatedTags, setIcon=updatedIcon, setInfo=updatedInfo, setFavorite=None)
                            if window.sortingMethod == 'Category' or window.sortingMethod == 'Path':
                                if updatedCategoryStatus is True:
                                    window.filter()
                            elif window.sortingMethod == 'Tags':
                                if updatedTagsStatus is True:
                                    window.filter()
                            elif window.sortingMethod == 'Alphabetical':
                                if updatedNameStatus is True:
                                    window.filter()

                    modifierKeys = QtWidgets.QApplication.keyboardModifiers()
                    if modifierKeys == QtCore.Qt.ShiftModifier:
                        if self.action is None:
                            self.ui.nameField.setText('')
                            self.ui.descriptionField.setText('')
                            self.ui.tagsField.setText('')
                            self.ui.iconField.setText('')
                            self.ui.scriptContentField.clear()
                            self.ui.pythonButton.setChecked(1)
                    else:
                        self.fadeCloseWindow()
                else:
                    self.animatePopup('add', 'Something wrong when adding the script...our bad', 'error')
                    logger.error('Something wrong when adding the script...our bad')
            else:
                self.animatePopup('add', ("Unsafe character '{}' in {} field").format(character, safe), 'error')
        else:
            if len(category) == 0:
                self.animatePopup('add', 'No category selected, create a new one', 'error')
            else:
                self.animatePopup('add', 'You need to fill in all fields', 'error')
        return

    def pickIcon(self):
        try:
            path = lastIconPath
        except:
            path = prefs.getGenericSettings('scriptPath').split(';')[-1]

        dialog = QtWidgets.QFileDialog()
        filters = 'Images (*.png *.xpm *.jpg *.jpeg *.bmp, *.svg)'
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        file = dialog.getOpenFileName(None, 'Pick icon', path, filters)
        lastIconPath = os.path.dirname(file[0])
        if len(file[0]) >= 1:
            self.ui.iconField.setText(file[0])
            if '.svg' in file[0]:
                print 'This is a SVG icon for big-ones'
                iconFile = qtCore.load_svg(file[0], size=(40, 40))
                self.ui.bigIcon.setIcon(iconFile)
            else:
                self.ui.bigIcon.setIcon(QtGui.QPixmap(file[0]))
        return

    def makeDockable(self):
        self.dockedMode = True
        self.setDockableParameters(dockable=True, floating=False, area='right', width=400)
        self.setWindowFlags(self.windowFlags() & QtCore.Qt.FramelessWindowHint)
        self.ui.closeButton.hide()
        self.ui.frame.setStyleSheet('border-radius: 0px')
        self.show()


class SetupWindow(genericWindow):

    def __init__(self, parent=None, title=None):
        interfacePath = ('{}interface_settingsSetup.ui').format(uiPath)
        super(SetupWindow, self).__init__(interfacePath, parent)
        try:
            exec 'cosmosSetupWindow.close()'
        except:
            pass

        self.resize(550, 270)
        preferenceState = prefs.prefExist('cosmos_settings.xml')
        if preferenceState is True:
            self.checkPrefs()
        self.ui.saveButton.clicked.connect(self.saveSettings)
        self.ui.resetButton.clicked.connect(self.resetChangeState)
        self.ui.addScriptFolderButton.clicked.connect(self.showProjectPicker)
        self.ui.openScriptFolderButton.clicked.connect(self.openScriptpath)
        self.ui.removeScriptFolderButton.clicked.connect(self.removePath)
        self.ui.actionPathField.clicked.connect(self.ui.removeScriptFolderButton.show)
        self.ui.resetPathButton.clicked.connect(self.resetPaths)
        self.ui.removeScriptFolderButton.hide()
        self.ui.openScriptFolderButton.hide()
        self.ui.versionText.setText('v' + __version__)
        self.ui.smallLogo.setAutoFillBackground(True)
        self.ui.smallLogo.setIcon(QtGui.QPixmap(menuLogo))
        self.show()

    def resetPaths(self):
        self.ui.actionPathField.clear()
        pathString = prefs.generateDefaultPath().split(';')
        for path in pathString:
            item = QtWidgets.QListWidgetItem(path)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.ui.actionPathField.addItem(item)

    def removePath(self):
        self.ui.actionPathField.takeItem(self.ui.actionPathField.currentIndex().row())

    def checkPrefs(self):
        preferenceState = prefs.prefExist('cosmos_settings.xml')
        if preferenceState is False:
            prefs.createFile()
        alwaysOn = prefs.getGenericSettings('alwaysOn')
        grayMode = prefs.getGenericSettings('noColorMode')
        scriptPathList = prefs.getGenericSettings('scriptPath').split(';')
        try:
            mayaCommands = prefs.getGenericSettings('mayaCommands')
        except:
            prefs.addGenericSettings('mayaCommands', 'True')
            mayaCommands = prefs.getGenericSettings('mayaCommands')

        for path in scriptPathList:
            item = QtWidgets.QListWidgetItem(path)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.ui.actionPathField.addItem(item)

        self.ui.actionPathField.clearSelection()
        if alwaysOn == 'True':
            self.ui.alwaysOn.toggle()
        if grayMode == 'True':
            self.ui.noColorMode.toggle()
        if mayaCommands == 'False':
            self.ui.mayaCommands.toggle()
        searches = prefs.getListCount('latestList')
        if searches == 0:
            self.ui.resetButton.hide()
            self.ui.resetLabel.hide()
        self.ui.saveButton.setFocus()

    def resetChangeState(self):
        self.ui.resetButton.setText('Press again to confirm')
        self.ui.resetButton.clicked.connect(self.reset)

    def reset(self):
        self.ui.resetButton.hide()
        status = True
        message = 'All search and action data reset'
        prefs.resetFile('searches')
        status = prefs.resetFile('settings')
        if status is False:
            message = 'Problem under the hood. (Its not you, its me)'
        self.ui.resetLabel.setText(message)

    def showProjectPicker(self):
        try:
            scriptPath = prefs.getGenericSettings('scriptPath').split(';')[0]
        except:
            scriptPath = None

        if scriptPath != None:
            pass
        else:
            path = os.path.curdir
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly)
        directory = dialog.getExistingDirectory(self, 'Add New Action Folder', scriptPath)
        if len(directory) >= 1:
            if directory[-1] != '/' or directory[-1] != '\\':
                directory = directory + os.sep
            item = QtWidgets.QListWidgetItem(directory)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.ui.actionPathField.addItem(item)
        return

    def openScriptpath(self):
        index = self.ui.actionPathField.currentIndex().row()
        item = self.ui.actionPathField.item(index)
        path = item.text()
        prefs.openFolder(path)

    def saveSettings(self):
        items = []
        for index in xrange(self.ui.actionPathField.count()):
            items.append(self.ui.actionPathField.item(index).text())

        newScriptPath = (';').join(items)
        alwaysOnValue = str(self.ui.alwaysOn.isChecked())
        noColorValue = str(self.ui.noColorMode.isChecked())
        mayaCommand = str(self.ui.mayaCommands.isChecked())
        prefs.writegenericSettings('alwaysOn', alwaysOnValue)
        prefs.writegenericSettings('noColorMode', noColorValue)
        prefs.writegenericSettings('scriptPath', newScriptPath)
        prefs.writegenericSettings('mayaCommands', mayaCommand)
        self.close()
        setInterfaceColor()
        displayViewMessage(text='Settings saved')
        for window in mayaWindow().children():
            if isinstance(window, searchWindow):
                window.keepOpen = False

        displayWindow('search')
        for window in mayaWindow().children():
            if isinstance(window, searchWindow):
                window.keepOpen = True

        getContent()
        windowInstances = returnInstances(genericDockingWindow)
        for window in windowInstances:
            window.getActionProperties()
            window.filter()


def returnIconPath(iconInput):
    if iconInput != None:
        if ':' in iconInput:
            return iconInput
        if 'mayaDefault' in iconInput:
            return ('{}icons{}mayaDefault.png').format(relativePath, os.sep)
        if iconInput == menuLogo:
            return menuLogo
        if iconInput == '':
            return ('{}icons{}noName.png').format(relativePath, os.sep)
        iconPath = None
        for path in library.cosmosIconsList:
            if len(iconInput) >= 1:
                if iconInput in path:
                    iconPath = path
                    break

        if iconPath != None:
            return iconPath
        return ('{}icons{}noName.png').format(relativePath, os.sep)
    else:
        return ('{}icons{}noName.png').format(relativePath, os.sep)
    return


def setIconFromString(icon, string, absolute=False, name=None):
    iconPath = None
    if absolute is True:
        iconPath = string
    else:
        if ':' in string:
            iconPath = string
        else:
            if 'mayaDefault' in string:
                if name != None:
                    if 'paint' in name.lower():
                        iconPath = ('{}icons{}mayaPaint.png').format(relativePath, os.sep)
                    elif 'weights' in name.lower():
                        iconPath = ('{}icons{}mayaPaint.png').format(relativePath, os.sep)
                    else:
                        iconPath = ('{}icons{}mayaDefault.png').format(relativePath, os.sep)
                else:
                    iconPath = ('{}icons{}mayaDefault.png').format(relativePath, os.sep)
            else:
                if string == '':
                    iconPath = ('{}icons{}noName.png').format(relativePath, os.sep)
                else:
                    for path in library.cosmosIconsList:
                        if string in path:
                            iconPath = path
                            break

                if iconPath == None:
                    iconPath = ('{}icons{}noName.png').format(relativePath, os.sep)
    if 'svg' in iconPath:
        iconFile = qtCore.load_svg(iconPath, size=(30, 30))
        icon.setIcon(iconFile)
    else:
        icon.setIcon(QtGui.QPixmap(iconPath))
    return


def loadActionIcon(icon):
    iconPath = None
    for path in library.cosmosIconsList:
        if len(icon) >= 1:
            if icon in path:
                iconPath = path
                break

    if iconPath is None:
        iconPath = ('{}icons{}noName.png').format(relativePath, os.sep)
    return iconPath


def executePython(command):
    status = 'success'
    exec 'cmds.undoInfo(openChunk=True)'
    cmds.evalDeferred(command)
    exec 'cmds.undoInfo(closeChunk=True)'
    return status


def executeMel(command):
    status = 'success'
    exec 'cmds.undoInfo(openChunk=True)'
    mel.eval(command)
    exec 'cmds.undoInfo(closeChunk=True)'
    cmds.repeatLast(ac=command, acl='Cosmos Mel Command')
    return status


def executeAction(actionID):
    status = 'success'
    exec 'cmds.undoInfo(openChunk=True)'
    action = library.getActionById(actionID)
    if action != None:
        if action['syntax'] == 'mel':
            status = executeMel(action['command'])
        elif action['syntax'] == 'python':
            executePython(action['command'])
            try:
                cmds.repeatLast(ac=('python("cosmos.executeAction(\'{}\')");').format(actionID), acl='Cosmos Python Command')
            except:
                pass

    else:
        print 'File is not found'
        status = ('File not found for:\n{}').format(actionID)
    exec 'cmds.undoInfo(closeChunk=True)'
    return status


def executeCard(card, forceAlt=False):
    status = 'success'
    name = card.getTitle()
    description = card.getDescription()
    category = card.getCategory()
    command = card.getCommand()
    altCommand = card.getAltCommand()
    iconPath = card.getIconPath()
    id = card.getId()
    message = cleanCategory(category) + '/ ' + name
    modifierKeys = QtWidgets.QApplication.keyboardModifiers()
    if modifierKeys == QtCore.Qt.AltModifier:
        if altCommand != None:
            forceAlt = True
    else:
        if modifierKeys == QtCore.Qt.ShiftModifier | QtCore.Qt.AltModifier:
            if altCommand != None:
                forceAlt = True
    exec 'cmds.undoInfo(openChunk=True)'
    if type(command) is unicode or type(command) is str:
        if 'cosmos.' in command:
            cmds.evalDeferred(command)
        elif '.action' in command:
            status = executeAction(command)
        elif 'mel.eval' in command:
            status = executeMel(command, name)
        elif '@pointerRef' in command:
            pointer = None
            for item in mayaCommandList:
                if name in item['name']:
                    if category in item['category']:
                        if description in item['info']:
                            if forceAlt is True:
                                pointer = item['altCommand']
                                message = name + ' [OPTIONS]'
                            else:
                                pointer = item['command']
                            break

            if pointer != None:
                pointer.trigger()
            else:
                status = ("Pointer not found for '{}'").format(command)
                logger.warning(("Error executing command: NAME:'{}' CATEGORY:'{}' COMMAND:'{}'").format(name, category, command))
        else:
            status = ("Command string '{}' not found").format(command)
    else:
        if forceAlt is False:
            command.trigger()
        else:
            altCommand.trigger()
            message = name + ' [OPTIONS]'
    if status == 'success':
        if card.special == False:
            displayViewMessage(text=message)
    else:
        if card.special == False:
            displayViewMessage(text=('{}').format(status), mode='error')
        logger.error(("Error executing command: \nNAME:'{}' CATEGORY:'{}'COMMAND:'{}'").format(name, category, command))
    exec 'cmds.undoInfo(closeChunk=True)'
    return status


def importer():
    path = os.path.curdir
    dialog = QtWidgets.QFileDialog()
    filters = 'Images (*.zip *.action)'
    dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
    file = dialog.getOpenFileName(None, 'Pick icon', path, filters)
    if len(file) >= 1:
        print file[0]
    return


def cleanCategory(category):
    for path in library.scriptPath:
        if path in category:
            cleanCategory = category.replace(path, '')
            break
        else:
            cleanCategory = category

    return cleanCategory


def returnScriptPathOnly(category):
    scriptPath = None
    for path in library.scriptPath:
        if path in category:
            cleanCategory = category.replace(path, '')
            scriptPath = path.replace(cleanCategory, '')
            break

    if scriptPath != None:
        return scriptPath
    return


def buildCardInView(listwidget):
    rect = listwidget.viewport().contentsRect()
    top = listwidget.indexAt(rect.topLeft())
    if top.isValid():
        bottom = listwidget.indexAt(rect.bottomLeft())
        if not bottom.isValid():
            bottom = listwidget.model().index(listwidget.count() - 1)
        topNumber = bottom.row() + 1
        if bottom.row() + 1 <= 9:
            topNumber = 9
        for index in range(top.row(), topNumber):
            listItem = listwidget.item(index)
            try:
                card = listItem.data(109)
                if card != None:
                    if card.built == False:
                        card.buildMethod()
                        card.built = True
            except:
                pass

    return


def buildCardInList(listwidget):
    for item in list.findItems('', QtCore.Qt.MatchRegExp):
        try:
            card = listItem.data(109)
            if card != None:
                if card.built == False:
                    card.buildMethod()
                    card.built = True
        except:
            pass

    return
