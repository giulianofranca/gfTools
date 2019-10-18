# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Requirements:
    Maya 2017 or above.

Todo:
    * TODO(gfranca): If don't have a metadata attribute of the rig, don't display the marking menu.
    * TODO(gfranca): Types of rig objs: ctrl, srt, buffer, hrc, char, cmpnt

Sources:
    * http://www.chrisevans3d.com/pub_blog/mighty-message-attribute/
    * http://www.chrisevans3d.com/pub_blog/object-oriented-python-in-maya-pt-1/

This code supports Pylint. Rc file in project.
"""
import maya.cmds as cmds
import maya.api._OpenMaya_py2 as om2


kMenuName = "testMarkingMenu"


class TestingMarkingMenu(object):
    """Marking menu for testing purposes.

    This can be used to create an attribute with createAttribute() function. Constant types are:
    kInt, kFloat, kDouble, kShort, kLong, kBool, kAngle, kDistance, kTime, kFloatMatrix, kDoubleMatrix,
    kString, kMesh, kNurbsCurve, kNurbsSurface and kEnum.
    """

    def __init__(self):
        """Constructor.

        Removes the old instance automatically and create a fresh one when called.

        Args:
            self: self.
        """
        self.menu = None
        self.removeOldVersion()
        self.buildMarkingMenu()

    def removeOldVersion(self):
        """Remove old version in case of new instance.

        Args:
            self: self.
        """
        if cmds.popupMenu(kMenuName, ex=True):
            cmds.deleteUI(kMenuName)

    def buildMarkingMenu(self):
        """Build a new marking menu.

        Args:
            self: self.
        """
        sel = om2.MGlobal.getActiveSelectionList()
        if sel.length() < 1:
            return
        lastSelMob = sel.getDependNode(sel.length() - 1)
        if not lastSelMob.hasFn(om2.MFn.kDagNode):
            objName = om2.MFnDependencyNode(lastSelMob).name()
            om2.MGlobal.displayInfo("%s object is not a Dag Node." % objName)
        cmds.popupMenu(
            kMenuName,
            mm=True,            # Define a marking menu
            b=2,                # Mouse button to trigger: 1 = left, 2 = middle, 3 = right
            aob=True,           # Allow option boxes
            ctl=True,           # Ctrl modifier
            alt=True,           # Alt modifier
            sh=False,           # Shift modifier
            p="viewPanes",      # Parent element
            pmo=True,
            pmc=self.buildItems
        )

    def buildItems(self, menu, parent):
        """Build items for the marking menu.

        Args:
            menu (string): The current menu.
            parent (string): The parent of marking menu.
        """
        # pylint: disable=unused-argument
        cmds.menuItem(p=menu, l="South West Button", rp="SW", c="print('SouthWest')", i="pythonFamily.png")
        cmds.menuItem(p=menu, l="South East Button", rp="SE", c="print('SouthEast')", i="pythonFamily.png")
        cmds.menuItem(p=menu, l="North East Button", rp="NE", c="print('NorthEast')", i="pythonFamily.png")

        subMenu = cmds.menuItem(p=menu, l="North Sub Menu", rp="N", sm=True)
        cmds.menuItem(p=subMenu, l="North Sub Menu Item 1")
        cmds.menuItem(p=subMenu, l="North Sub Menu Item 2")

        cmds.menuItem(p=menu, l="South", rp="S", c="print('South')")
        cmds.menuItem(p=menu, ob=True, c="print('South with options')")

        cmds.menuItem(p=menu, l="First menu item in the list")
        cmds.menuItem(p=menu, l="Second menu item in the list")
        cmds.menuItem(p=menu, l="Third menu item in the list")
        cmds.menuItem(p=menu, l="Create a poly cube", c="print('Creating poly cube')")
