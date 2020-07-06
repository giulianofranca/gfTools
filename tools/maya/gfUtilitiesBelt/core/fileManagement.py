import sys
import os
import json
import datetime
import collections

APP_VERSION = "1.0"
REQUIRED_VERSION = "1.0"

SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
SETTINGS_PATH = os.path.join(SCRIPT_PATH, "core", "settings.json")
POCKETS_PATH = os.path.join(SCRIPT_PATH, "pockets")
TOOLS_PATH = os.path.join(SCRIPT_PATH, "tools")
MAYA_ICONS_PATH = os.path.join(SCRIPT_PATH, "gui", "icons", "MAYA")
MAYA_TOOLS_PATH = os.path.join(SCRIPT_PATH, "tools", "_mayaData")
MAYA_BACKUP_TOOLS_PATH = os.path.join(MAYA_TOOLS_PATH, "_backup")
MAYA_TOOLS_FILE_PATH = os.path.join(MAYA_TOOLS_PATH, "mayaData.json")


FILE_PATH = os.path.join(POCKETS_PATH, "test.gfPocket")



def readSettings():
    try:
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
    except:
        settings = collections.OrderedDict()
        settings["Application"] = "gfUtilitiesBelt"
        settings["Current Version"] = APP_VERSION
        settings["Required Version"] = REQUIRED_VERSION
        configs = collections.OrderedDict()
        configs["AutoLoad"] = True
        configs["OpenedPockets"] = ""
        settings["Settings"] = configs
        with open(SETTINGS_PATH, "w") as f:
            json.dump(settings, f, indent=4, ensure_ascii=True)

    return settings


def savePocket(name, tools):
    old = None
    filepath = os.path.join(POCKETS_PATH, "%s.gfPocket" % name)
    if os.path.isfile(filepath):
        with open(filepath) as f:
            old = json.load(f)

    data = collections.OrderedDict()
    data["Pocket Name"] = name
    if old is not None:
        data["Created Version"] = old["Created Version"]
    else:
        data["Created Version"] = APP_VERSION
    data["Current Version"] = APP_VERSION
    if old is not None:
        data["Created"] = old["Created"]
    else:
        data["Created"] = datetime.datetime.now().strftime("%B %d, %Y - %I:%M:%S %p")
    data["Last Modified"] = datetime.datetime.now().strftime("%B %d, %Y - %I:%M:%S %p")
    if old is not None:
        data["Tools"] = []
        data["Tools"].extend(tools)
    else:
        data["Tools"] = []

    # Populate tools
    # for t in tools:
    #     data["Tools"].append(t)

    # Export file
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=True)

    return True


def readToolsFromPocket(pocket):
    pass


# saveFile("Giuliano", FILE_PATH)
