# -*- coding: utf-8 -*-
"""
This code supports Pylint. Rc file in project.
This code is
"""
import sys
import os

kPlatform = sys.platform

if kPlatform == "win32":
    # Append Maya modules to PYTHONPATH
    sys.path.append("%s\\Python\\Lib\\site-packages" % os.environ["MAYA_LOCATION"])

    # Append Maya devkit completition files to PYTHONPATH
    sys.path.append("%s\\devkit\\other\\pymel\\extras\\completition\\py" % os.environ["MAYA_LOCATION"])

elif kPlatform == "darwin":
    # Append Maya modules to PYTHONPATH
    sys.path.append(
        "%s\\files\\Maya.app\\Contents\\Framework\\Python.framework\\Versions\\Current\\lib\\python2.7\\site-packages"
        % os.environ["MAYA_LOCATION"]
    )

elif kPlatform == "linux":
    # Append Maya modules to PYTHONPATH
    sys.path.append("%s\\files\\lib\\python2.7\\site-packages" % os.environ["MAYA_LOCATION"])
