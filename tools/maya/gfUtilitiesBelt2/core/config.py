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
import datetime
from collections import OrderedDict

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
    settings = OrderedDict()
    appSettings = OrderedDict()
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
    settings["Settings"] = appSettings
    return settings



def runStartConfigurations():
    """Run the necessary checks and configurations to start the application.

    Returns:
        OrderedDict: The settings dictionary.
    """
    # TODO: Update Maya info after the ui loads
    # 1- Read settings file
    updateSettings()
    settings = readSettingsFile()
    appSettings = settings["Settings"]

    # 2- Check the opened pockets and last pocket used. Check if they exist and is valid.
    if settings["Opened Pockets"] is not None:
        for pocket in settings["Opened Pockets"]:
            status = pockets.Pocket.checkFile(pocket)
            if not status:
                sys.stdout.write("[%s] The file %s was not recognized as a valid Pocket file or doesn't exist. Operation skipped." % (appInfo.kApplicationName, pocket))
                settings["Opened Pockets"].remove(pocket)
    if settings["Last Pocket Used"] is not None:
        lastPocketUsed = settings["Last Pocket Used"]
        status = pockets.Pocket.checkFile(lastPocketUsed)
        if not status:
            sys.stdout.write("[%s] The file %s was not recognized as a valid Pocket file or doesn't exist. Operation skipped." % (appInfo.kApplicationName, lastPocketUsed))
            settings["Last Pocket Used"] = None

    # 3- Save settings file
    updateSettings(settings)

    # 4- Return the settings dictionary
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
        settings = json.load(f, object_pairs_hook=OrderedDict)

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


def getTimedeltaFromThreshold(threshold):
    """Return the timedelta from given hours threshold.

    Args:
        threshold (str): The threshold in hours.

    Returns:
        timedelta: The timedelta instance.
    """
    return datetime.timedelta(hours=threshold)


def updateCheckMayaLibraries(settings):
    """Check and update Maya tools library.

    Args:
        settings (OrderedDict): The application settings dict.
    """
    # 1- Check if Maya info file exist. If not, update Maya info.
    mayaVersion = appInfo.kMayaVersion
    if not getMayaInfo.checkMayaInfoFile():
        getMayaInfo.updateMayaInfo()
        settings["Last Maya Info Update"] = getCurrentDateTime(string=True)
        settings["Last Maya Used"] = mayaVersion
    else:
        # 2- Check if current Maya version is different then last Maya version used
        if mayaVersion != settings["Last Maya Used"]:
            getMayaInfo.updateMayaInfo()
            settings["Last Maya Info Update"] = getCurrentDateTime(string=True)
            settings["Last Maya Used"] = mayaVersion
    # 3- Find if auto update is enabled
    autoUpdate = settings["Settings"]["Auto Update"]
    if autoUpdate:
        # 4- If it is, check the threshold and update.
        lastUpdate = convertStrToDatetime(settings["Last Maya Info Update"])
        now = getCurrentDateTime()
        threshold = getTimedeltaFromThreshold(settings["Settings"]["Maya Info Update Threshold"])
        if now - lastUpdate > threshold:
            getMayaInfo.updateMayaInfo()
            settings["Last Maya Info Update"] = getCurrentDateTime(string=True)
    # 5- Update settings file
    updateSettings(settings)