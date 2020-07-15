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
    * Add fade animations

Sources:
    * https://help.autodesk.com/view/MAYAUL/2019/ENU/?guid=Maya_SDK_MERGED_Writing_Workspace_controls_html
    * https://help.autodesk.com/view/MAYAUL/2019/ENU/?guid=Maya_SDK_MERGED_Maya_Python_API_Working_with_PySide_in_Maya_PyQt_and_PySide_Widget_Best_html
    * https://gist.github.com/liorbenhorin/217bfb7e54c6f75b9b1b2b3d73a1a43a
    * https://gist.github.com/liorbenhorin/69da10ec6f22c6d7b92deefdb4a4f475 <-- This

This code supports Pylint. Rc file in project.
"""
# This is only to call the application
from PySide2 import QtUiTools
from PySide2 import QtCore
from gfUtilitiesBelt2.core import config
from gfUtilitiesBelt2.core import ui
reload(config)
reload(ui)




def main():
    settings = config.runStartConfigurations()
    mainWin = ui.showWindow(settings)
    # TODO: Add load plugin button in shelf
    # Open the gui with all settings
    # Capture the width and height before close the application