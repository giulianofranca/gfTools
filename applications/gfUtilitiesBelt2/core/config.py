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
    * Add commands to generate/read settings for the application

Sources:
    * NDA

This code supports Pylint. Rc file in project.
"""
import sys
import os
import json
import collections
import datetime

from gfUtilitiesBelt2.core import appInfo
from gfUtilitiesBelt2.core import getMayaInfo
from gfUtilitiesBelt2.core import pockets
reload(appInfo)
reload(getMayaInfo)
reload(pockets)


# Settings
kLastMayaInfoUpdate = None
kLastMayaUsed = None
kMayaInfoUpdateThreshold = 5
kOpenedPockets = None
kLastPocket = None
kListView = False
kWidth = 275
kHeight = 600

# Default application settings
kDefaultAutoLoad = False
kDefaultAutoUpdate = True

kSettingsFileName = "settings.json"
kSettingsFilePath = os.path.join(appInfo.kCorePath, kSettingsFileName)
kDatetimeFormat = "%m-%d-%Y_%H-%M"




def createDefaultSettings():
    """Create the default settings dictionary.

    Returns:
        OrderedDict: The settings dictionary.
    """
    settings = collections.OrderedDict()
    appSettings = collections.OrderedDict()
    appSettings["Auto Load"] = kDefaultAutoLoad
    appSettings["Auto Update"] = kDefaultAutoUpdate
    appSettings["Maya Info Update Threshold"] = kMayaInfoUpdateThreshold
    settings["Application"] = appInfo.kApplicationName
    settings["Current Version"] = appInfo.kApplicationVersion
    settings["Required Version"] = appInfo.kMinRequiredVersion
    settings["Last Maya Info Update"] = kLastMayaInfoUpdate
    settings["Last Maya Used"] = kLastMayaUsed
    settings["Opened Pockets"] = kOpenedPockets
    settings["Last Pocket Used"] = kLastPocket
    settings["List View"] = kListView
    settings["Width"] = kWidth
    settings["Height"] = kHeight
    settings["Settings"] = appSettings
    return settings



def runStartConfigurations():
    """Run the necessary checks and configurations to start the application.

    Returns:
        OrderedDict: The settings dictionary.
    """
    # 1- Read settings file
    updateSettings()
    settings = readSettingsFile()
    appSettings = settings["Settings"]

    # 2- Check if maya info file exist. If not, update maya info
    mayaVersion = appInfo.kMayaVersion
    if not getMayaInfo.checkMayaInfoFile():
        getMayaInfo.updateMayaInfo()
        settings["Last Maya Info Update"] = getCurrentDateTime(string=True)
        settings["Last Maya Used"] = mayaVersion
    else:
        # 3- Check if current Maya version is different than last Maya version used
        if mayaVersion != settings["Last Maya Used"]:
            getMayaInfo.updateMayaInfo()
            settings["Last Maya Info Update"] = getCurrentDateTime(string=True)
            settings["Last Maya Used"] = mayaVersion

    # 4- Find if auto update is enabled
    autoUpdate = appSettings["Auto Update"]
    if autoUpdate:
        # 5- If is, check the threshold and update.
        lastUpdate = convertStrToDatetime(settings["Last Maya Info Update"])
        now = getCurrentDateTime()
        threshold = datetime.timedelta(hours=appSettings["Maya Info Update Threshold"])
        if now - lastUpdate > threshold:
            getMayaInfo.updateMayaInfo()
            settings["Last Maya Info Update"] = getCurrentDateTime(string=True)

    # 5- Check the opened pockets and last pocket used. Check if they exist and is valid.
    if settings["Opened Pockets"] is not None:
        for pocket in settings["Opened Pockets"]:
            status = pockets.Pocket.checkFile(pocket)
            if not status:
                sys.stdout.write("[%s] The file %s was not recognized as a valid Pocket file. Operation skipped." % (appInfo.kApplicationName, pocket))
                settings["Opened Pockets"].remove(pocket)
    if settings["Last Pocket Used"] is not None:
        lastPocketUsed = settings["Last Pocket Used"]
        status = pockets.Pocket.checkFile(lastPocketUsed)
        if not status:
            sys.stdout.write("[%s] The file %s was not recognized as a valid Pocket file. Operation skipped." % (appInfo.kApplicationName, lastPocketUsed))
            settings["Last Pocket Used"] = None

    # 6- Save settings file
    updateSettings(settings)

    # 7- Return the settings dictionary
    return settings


def writeSettingsFile(settings):
    """Write a json file with specified settings.

    Args:
        settings (OrderecDict): The settings dictionary to write in the json file.

    Returns:
        True: If succeeded.
    """
    fullPath = kSettingsFilePath
    with open(fullPath, "w") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)

    return True


def readSettingsFile():
    """Read the json file containing all application settings.

    Returns:
        OrderedDict: The dictionary containing all the application settings.

    Raises:
        RuntimeError: If the file does not exists.
    """
    fullPath = kSettingsFilePath
    if not checkSettingsFile():
        raise RuntimeError("Settings file not founded.")
    with open(fullPath, "r") as f:
        settings = json.load(f, object_pairs_hook=collections.OrderedDict)

    return settings


def checkSettingsFile():
    """Check if settings file exists and is valid.

    Returns:
        True or False: If file exists and is valid or not.
    """
    fileName = kSettingsFileName
    path = appInfo.kCorePath
    if fileName not in os.listdir(path):
        return False

    return True


def updateSettings(settings=None):
    """Update all application settings.

    If settings file exist and settings is None the function will do nothing, just pass.
    Otherwise, if settings file does not exist this function will create settings file
    with default settings or with specified settings.

    Args:
        settings (OrderedDict: None [Optional]): The dictionary containing the settings.

    Returns:
        True: If succeeded.
    """
    if not checkSettingsFile():
        if settings is not None:
            writeSettingsFile(settings)
        else:
            # Create settings file with default settings.
            settings = createDefaultSettings()
            writeSettingsFile(settings)
    else:
        if settings is not None:
            # Update settings file if file already exists and settings is not None
            writeSettingsFile(settings)

    return True


def getCurrentDateTime(string=False):
    """Return the current datetime already formatted.

    Args:
        string (bool: False [Optional]): Convert the datetime to string.

    Returns:
        str or datetime: The current datetime already string formatted or not.
    """
    if string:
        return datetime.datetime.now().strftime(kDatetimeFormat)
    else:
        return datetime.datetime.now()


def convertStrToDatetime(string):
    """Return the datetime specified in a datetime format.

    Returns:
        datetime: The datetime specified.
    """
    return datetime.datetime.strptime(string, kDatetimeFormat)
