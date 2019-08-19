# Procedural Ribbon Rig function
# Types of ribbon = Follicle, Aim Constraint, Matrix
import sys

from maya import cmds
from maya.api import OpenMaya as om2


def ribbon(name, res, type='Matrix', srt=['t', 'r', 's']):
    def getDagPath(node=None):
        sel = om2.MSelectionList()
        sel.add(node)
        dag = sel.getDagPath(0)
        return dag

    if type == 'Matrix':
        if 'r' in srt:
            pass
        else:
            pass
    elif type == 'Aim Constraint':
        pass
    elif type == 'Follicle':
        pass
