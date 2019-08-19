import sys
import os
import functools
import maya.cmds as cmds
import maya.api.OpenMaya as om2


def shelfTool(ann, lbl, imglbl, icn, cmd, cmdtype, double, maw=0, mah=0):
    """ Load Maya tool properties. """
    finalCmd = 'cmds.shelfButton('
