import sys, os
import maya.cmds as cmds
import maya.OpenMaya as om

from gfTools.gfRigSystem.utils import log
from gfTools.gfRigSystem.utils import components
reload(log); reload(components)


def loadComponentGuidesInfo(component, side):
    guidesInfo = {}
    cmpnts = components.findComponents()
    for cmpnt in cmpnts:
        if component == cmpnt['Name'].lower():
            guides = cmpnt['Guides']
            newGuides = {}
            if side == 'R':
                for guideName, guideValue in guides.items():
                    newGuides[guideName] = [guideValue[0] * (-1), guideValue[1], guideValue[2]]
                return newGuides
            else:
                return guides
