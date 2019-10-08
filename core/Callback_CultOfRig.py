# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Maya IDs:
    Prototypes: 0x0012f7c0 - 0x0012f7ff
    Releases: 0x00130d80 - 0x00130e7f

Redistribution:
    Something here.

Requirements:
    Maya 2017 or above.

Todo:
    * NDA
    * https://github.com/mgear-dev/mgear_core/blob/4b363aba97794b23363b5a15de58aa9710d7d8e0/scripts/mgear/core/attribute.py

This code supports Pylint. Rc file in project.
"""
import maya.api._OpenMaya_py2 as om2

def myCallback(msg, plug1, plug2, clientData):
    """Callback function"""
    if msg == 2056:
        srtTransPlugs = interestingPlugs(plug1)
        if len(srtTransPlugs) != 0:
            values = [p.asFloat() for p in srtTransPlugs[1:4]]
            for eachDestPlug in messageConnectedPlugs(plug1):
                destTransPlugs = interestingPlugs(eachDestPlug)[1:4]
                for i, p in enumerate(destTransPlugs):
                    p.setFloat(values[i])


def interestingPlugs(plug):
    """Is plug interesting?"""
    nodeFn = om2.MFnDependencyNode(plug.node())
    pNames = ("t", "tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz")
    return [nodeFn.findPlug(name, False) for name in pNames]

def messageConnectedPlugs(plug):
    """Message connected nodes"""
    nodeFn = om2.MFnDependencyNode(plug.node())
    msgPlug = nodeFn.findPlug("message", False)
    return [om2.MPlug(otherP) for otherP in msgPlug.destinations()]

sel = om2.MGlobal.getActiveSelectionList()

mob = None

if sel.length():
    mob = sel.getDependNode(0)

test = om2.MObject()

if mob is not None:
    nodeFn = om2.MFnDependencyNode(mob)
    transXPlug = nodeFn.findPlug("tx", False)
    for eachCB in om2.MMessage.nodeCallbacks(mob):
        om2.MMessage.removeCallback(eachCB)
    om2.MNodeMessage.addAttributeChangedCallback(mob, myCallback)
