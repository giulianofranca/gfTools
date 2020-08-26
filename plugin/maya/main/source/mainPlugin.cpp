/*
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
    * Copy the plugin file to the MAYA_PLUG_IN_PATH.
    * To find MAYA_PLUG_IN_PATH paste this command in a Python tab:
        import os; os.environ["MAYA_PLUG_IN_PATH"].split(";")
    * In Maya, go to Windows > Settings/Preferences > Plug-in Manager.
    * Find the plugin file and import it. Can be:
        Windows: gfTools.mll
        OSX: gfTools.bundle
        Linux: gfTools.so

Requirements:
    * Maya 2018 or above.

Todo:
    * Load/Unload shelf
    * Undo stack for rig framework

Sources:
    * NDA
*/
#include <maya/MFnPlugin.h>
#include <maya/MTypeId.h>
#include <maya/MGlobal.h>


const char* kAuthor = "Giuliano Franca";
MString res = MGlobal::executePythonCommandStringResult("import gfTools; gfTools.version()");
const char* kVersion = res.asChar();
const char* kRequiredAPIVersion = "Any";


MStatus initializePlugin(MObject mobject){
    MStatus status;
    MFnPlugin mPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion, &status);
    status = mPlugin.setName("gfTools");

    MGlobal::executePythonCommand("import gfToolsMenu; gfToolsMenu.load()");
    MGlobal::executePythonCommand("import gfToolsShelf; gfToolsShelf.load()");
    MGlobal::displayInfo("[gfTools] Plugin loaded successfully.");

    return status;
}

MStatus uninitializePlugin(MObject mobject){
    MStatus status;
    MFnPlugin mPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion, &status);

    MGlobal::executePythonCommand("import gfToolsMenu; gfToolsMenu.unload()");
    MGlobal::executePythonCommand("import gfToolsShelf; gfToolsShelf.unload()");
    MGlobal::displayInfo("[gfTools] Plugin unloaded successfully.");

    return status;
}