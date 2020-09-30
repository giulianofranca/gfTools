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
    * Run this script using either Python2.x or Python3.x

Requirements:
    * Maya 2018 or above.

This code supports Pylint. Rc file in project.
"""
# pylint: disable=import-error
import os
import maya.cmds as cmds
import maya.mel as mel

kShelfName = "gfTools"
kShelfPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "shelves"))
kShelfFile = os.path.join(kShelfPath, "shelf_%s.mel" % kShelfName)


def load():
    """Load gfTools custom shelf"""
    if not cmds.shelfLayout(kShelfName, q=True, ex=True):
        createShelf(kShelfFile)

def unload():
    """Unload gfTools custom shelf"""
    if cmds.shelfLayout(kShelfName, q=True, ex=True):
        deleteShelf(kShelfName)




def createShelf(shelfFileName):
    """Create a shelf"""
    # pylint: disable=undefined-loop-variable
    shortFileName = os.path.basename(shelfFileName)
    shortName = shortFileName.replace(".mel", "")
    shelfName = shortName.replace("shelf_", "")

    # Find if a copy of gfTools shelf is in prefs folder
    shelfDirs = cmds.internalVar(ush=True).split(os.pathsep)
    for shelfDir in shelfDirs:
        if (shelfDir.startswith(cmds.internalVar(upd=True))
                and shelfDir.endswith("prefs/shelves/")):
            # We have found the shelves directory
            break
    if not os.path.isfile(os.path.join(shelfDir, "%s.deleted" % shortFileName)):
        mel.eval('source "%s";' % shelfFileName)

    gShelfForm = mel.eval("$tmpVar = $gShelfForm")
    gShelfTopLevel = mel.eval("$tmpVar = $gShelfTopLevel")

    cmds.setParent(gShelfTopLevel)
    shelfHeight = cmds.tabLayout(gShelfTopLevel, q=True, h=True)
    cmds.tabLayout(gShelfTopLevel, e=True, vis=False)

    cmds.setParent(gShelfForm)
    spacingSeparator = cmds.separator(h=shelfHeight, st="single")

    cmds.formLayout(gShelfForm, e=True, af=[(spacingSeparator, "top", 0),
                                            (spacingSeparator, "left", 0),
                                            (spacingSeparator, "bottom", 0),
                                            (spacingSeparator, "right", 0)])

    cmds.tabLayout(gShelfTopLevel, e=True, m=False)
    cmds.setParent(gShelfTopLevel)

    newShelfName = cmds.shelfLayout(shelfName)

    # Match the style of the other tabs
    kids = cmds.tabLayout(gShelfTopLevel, q=True, ca=True)
    if len(kids) > 0:
        style = cmds.shelfLayout("%s|%s" % (gShelfTopLevel, kids[0]), q=True, style=True)
    else:
        style = cmds.optionVar(q="shelfItemStyle")
    mel.eval('shelfStyle %s "Small" %s' % (style, newShelfName))

    cmds.tabLayout(gShelfTopLevel, e=True, m=True, vis=True)

    shelves = cmds.tabLayout(gShelfTopLevel, q=True, ca=True)
    curShelfName = shelves[len(shelves) - 1]

    cmds.deleteUI(spacingSeparator)

    # Do that preferences thing
    nShelves = cmds.shelfTabLayout(gShelfTopLevel, q=True, nch=True)
    cmds.optionVar(
        iv=("shelfLoad%s" % nShelves, 0),
        sv=[("shelfName%s" % nShelves, curShelfName),
            ("shelfAlign%s" % nShelves, "left"),
            ("shelfFile%s" % nShelves, "shelf_%s" % curShelfName)]
    )

    # Save shelf file to shelves directory
    saveCmd = 'import maya.cmds as cmds; cmds.saveShelf("%s", "%sshelf_%s")' % (newShelfName, shelfDir, curShelfName)
    cmds.evalDeferred(saveCmd)

    cmds.tabLayout(gShelfTopLevel, e=True, st=curShelfName)

    # Set the current shelf option var
    shelfNum = cmds.tabLayout(gShelfTopLevel, q=True, sti=True)
    cmds.optionVar(iv=["selectedShelf", shelfNum])

    return curShelfName




def deleteShelf(shelfName):
    """Delete a shelf"""
    # pylint: disable=bare-except
    gShelfTopLevel = mel.eval("$tmpVar = $gShelfTopLevel")
    cmds.setParent(gShelfTopLevel)

    shelves = cmds.tabLayout(gShelfTopLevel, q=True, ca=True)
    numShelves = len(shelves)

    # Bail if there is something really weird going on
    if numShelves <= 0:
        return False

    # Check for the last shelf
    if numShelves == 1:
        # Cannot delete the last shelf
        return False

    # Update the preferences
    nShelves = cmds.shelfTabLayout(gShelfTopLevel, q=True, nch=True)
    for shelfNum in range(1, nShelves):
        if shelfName == cmds.optionVar(q="shelfName%s" % shelfNum):
            break
    for i in range(shelfNum, nShelves):
        align = "left"
        if cmds.optionVar(ex="shelfAlign%s" % (i+1)):
            align = cmds.optionVar(q="shelfAlign%s" % (i+1))
        cmds.optionVar(
            iv=("shelfLoad%s" % i, cmds.optionVar(q="shelfLoad%s" % (i + 1))),
            sv=[("shelfName%s" % i, cmds.optionVar(q="shelfName%s" % (i + 1))),
                ("shelfAlign%s" % i, align),
                ("shelfFile%s" % i, cmds.optionVar(q="shelfFile%s" % (i + 1)))]
        )
    cmds.optionVar(
        rm=["shelfLoad%s" % nShelves,
            "shelfName%s" % nShelves,
            "shelfAlign%s" % nShelves,
            "shelfFile%s" % nShelves]
    )

    # The optionVars have all been updated, so it's safe do delete and have
    # the shelfTabChange() method triggered. See Maya-3288.
    cmds.deleteUI("%s|%s" % (gShelfTopLevel, shelfName), lay=True)

    shelfDirs = cmds.internalVar(ush=True)
    shelfArray = shelfDirs.split(os.pathsep)
    for shelf in shelfArray:
        fileName = "%sshelf_%s.mel" % (shelf, shelfName)
        deletedFileName = "%s.deleted" % fileName

        # Fix for bug #125494. Remove the .deleted file if it already exists.
        try:
            cmds.sysFile(delete=deletedFileName)
        except:
            pass

        if cmds.file(fileName, q=True, ex=True):
            cmds.sysFile(fileName, ren=deletedFileName)
            break

    mel.eval("shelfTabChange()")
    return True
