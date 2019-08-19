###############################################################################
# @Name: getPVLocation
# @NiceName: Get Pole Vector Location
# @Category: Rigging
# @Description: Get location of pole vector in a joint chain.
# @Favorite: False
# @Author: Giuliano Franca
# --------------------------------------------------------------------------- #
# Needs two classes. One is the QtWidget interface and the other is the
# operator class with all of functionalities of the script.
###############################################################################

import sys
from maya.api import OpenMaya as om2
from PySide2 import QtWidgets, QtGui, QtCore



class getPVLocationUI(QtWidgets.QWidget):
    """
    INFO
    """

    def __init__(self):
        super(getPVLocationUI, self).__init__()
        # [objectLoaderWidget] Joint chain
        # [intSliderWidget] Pole Vector distance
        # [checkBoxWidget] Orientation on/off
        # [buttonWidget] Get transformations
        pass



class getPVLocationFUNCS(object):
    """
    Create a null with a position and rotation for the pole vector.
    """

    def __init__(self, chain):
        self.chain = chain
        self.transformsDags = list()
        self.positions = list()
        self.transFn = om2.MFnTransform()
        self.calculate()


    def calculate(self):
        # 1- Get all the transforms in selectionList.
        [self.transformsDags.append(om2.MSelectionList().add(self.chain[x]).getDagPath(0)) for x in range(3)]

        # 2- Get the position of all the objects in selectionList.
        for x in range(len(self.transformsDags)):
            self.transFn.setObject(self.transformsDags[x])
            self.self.positions.append(transFn.translation(om2.MSpace.kWorld))

        # 3- Do a calculation.
        startEndV = self.positions[-1] - self.positions[0]
        startMidV = self.positions[1] - self.positions[0]
        dotP = startMidV * startEndV
        proj = float(dotP) / float(startEndV.length())
        startEndN = startEndV.normal()
        projV = startEndN * proj
        arrowV = startMidV - projV
        arrowV *= 4
        pos = arrowV + self.positions[1]
        cross1 = startEndV ^ startMidV
        cross1.normalize()
        cross2 = cross1 ^ arrowV
        cross2.normalize()
        arrowV.normalize()
        matrixArray = [arrowV.x, arrowV.y, arrowV.z, 0,
                       cross1.x, cross1.y, cross1.z, 0,
                       cross2.x, cross2.y, cross2.z, 0,
                       0, 0, 0, 1]
        matrixM = om2.MMatrix(matrixArray)
        matrixFn = om2.MTransformationMatrix(matrixM)
        rot = matrixFn.rotation(asQuaternion=False)

        # 4- Create a object with position and orientation.
        null = om2.MFnDagNode().create('transform', 'pvLocation_srt', om2.MObject.kNullObj)
        nullDag = om2.MDagPath().getAPathTo(null)
        self.transFn.setObject(nullDag)
        self.transFn.setTranslation(pos, om2.MSpace.kWorld)
        self.transFn.setRotation(rot, om2.MSpace.kTransform)
