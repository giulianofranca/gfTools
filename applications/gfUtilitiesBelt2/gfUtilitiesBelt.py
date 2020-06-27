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
    * Add fade animations

Sources:
    * https://help.autodesk.com/view/MAYAUL/2019/ENU/?guid=Maya_SDK_MERGED_Writing_Workspace_controls_html
    * https://help.autodesk.com/view/MAYAUL/2019/ENU/?guid=Maya_SDK_MERGED_Maya_Python_API_Working_with_PySide_in_Maya_PyQt_and_PySide_Widget_Best_html
    * https://gist.github.com/liorbenhorin/217bfb7e54c6f75b9b1b2b3d73a1a43a
    * https://gist.github.com/liorbenhorin/69da10ec6f22c6d7b92deefdb4a4f475 <-- This

This code supports Pylint. Rc file in project.
"""
# This is only to call the application
from gfUtilitiesBelt2.core import config
from gfUtilitiesBelt2.core import ui
from gfUtilitiesBelt2.core.getMayaInfo import getMayaWindow
from PySide2 import QtUiTools
from PySide2 import QtCore
reload(config)
reload(ui)




def main():
    path = "C:/Users/gfranca/Documents/maya/2017/scripts/gfTools/core/widgets/gfWidgets_Windows/Release/gfWidgets.dll"
    pluginLoader = QtCore.QPluginLoader(path)
    print(pluginLoader.staticInstances())
    # status = pluginLoader.instance()
    # print(status)
    # loader = QtUiTools.QUiLoader()
    # loader.registerCustomWidget()
    # settings = config.runStartConfigurations()
    # mainWin = ui.MainWin(getMayaWindow())
    # Open the gui with all settings
    # Capture the width and height before close the application