# -*- coding: utf-8 -*-
"""
Pylint Init Hook code.
"""
import sys
import os

kPlatform = sys.platform
try:
    kMayaLocation = os.environ["MAYA_LOCATION"]
except KeyError:
    if kPlatform == "win32":
        kMayaLocation = "C:\\Program Files\\Autodesk\\Maya2017"
    elif kPlatform == "darwin":
        kMayaLocation = "/Users/Shared/Autodesk/maya/2017"
    elif kPlatform == "linux":
        kMayaLocation = "/usr/autodesk/maya2017"



if kPlatform == "win32":
    # Append Maya modules to PYTHONPATH
    # sys.path.append("%s\\Python\\Lib\\site-packages" % kMayaLocation)

    # Append Maya devkit completition files to PYTHONPATH
    sys.path.append("%s\\devkit\\other\\pymel\\extras\\completition\\py" % kMayaLocation)

elif kPlatform == "darwin":
    # Append Maya modules to PYTHONPATH
    sys.path.append(
        "%s\\files\\Maya.app\\Contents\\Framework\\Python.framework\\Versions\\Current\\lib\\python2.7\\site-packages"
        % kMayaLocation
    )

elif kPlatform == "linux":
    # Append Maya modules to PYTHONPATH
    # sys.path.append("%s\\files\\lib\\python2.7\\site-packages" % kMayaLocation)

    # Append Maya devkit completition files to PYTHONPATH
    sys.path.append("%s/devkit/other/pymel/extras/completition/py" % kMayaLocation)
