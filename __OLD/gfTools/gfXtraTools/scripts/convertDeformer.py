###############################################################################
# @Name: convertDeformer
# @NiceName: Convert Deformer
# @Category: Rigging
# @Description: Convert one type of deformer to another.
# @Favorite: False
# @Author: Giuliano Franca
# --------------------------------------------------------------------------- #
# Needs two classes. One is the QtWidget interface and the other is the
# operator class with all of functionalities of the script.
###############################################################################

import sys
import maya.cmds as cmds
from maya.api import OpenMaya as om2
from maya.api import OpenMayaAnim as oma2
from PySide2 import QtWidgets, QtGui, QtCore



class convertDeformerUI(QtWidgets.QWidget):
    """
    INFO
    """

    def __init__(self):
        super(convertDeformerUI, self).__init__()
        # [comboBoxGrpWidget] Deformer type to Deformer type
        # [objectLoaderWidget] Deformer 1
        # [objectLoaderWidget] Deformer 2
        # [checkBoxWidget] Maintain old deformer on/off
        # [buttonWidget] Convert
        pass



class convertDeformerFUNCS(object):
    """
    Create a null with a position and rotation for the pole vector.
    """

    def __init__(self):
        # 1- Check if each objects matches the deformer type.
        # 2- Load the correct function for determinated deformer convertion.
        # 3- Delete or not the old deformer.
        pass


    def softSelToCluster(self):
        # Get soft selection range and influence
        softSel = om2.MGlobal.getRichSelection()
        selList = softSel.getSelection()
        component = selList.getComponent(0)
        componentIndex = om2.MFnSingleIndexedComponent(component[1])
        vertexList = componentIndex.getElements()
        weightList = dict()
        for x in range(len(vertexList)):
            weight = componentIndex.weight(x)
            influence = weight.influence
            weightList.setdefault(vertexList[x], influence)
        # Set soft selection range and influence to new cluster
        rangeVertices = selList.getSelectionStrings()
        myCluster = cmds.cluster(rangeVertices, n='MyCluster')
        for x in weightList:
            curVertex = x
            curWeight = weightList[x]
            cmds.setAttr('%s.weightList[0].w[%i]' % (myCluster[0],
                curVertex), curWeight)

    def latticeToSkinCluster1(self):
        sel = cmds.ls(sl=True) # Sel lattice
        latticeShape = cmds.listRelatives(sel[0], type='lattice')[0]
        ffd = cmds.listConnections(latticeShape, type='ffd')[0]
        skin = cmds.listConnections(latticeShape, type='skinCluster')[0]
        geometry = cmds.lattice(latticeShape, q=True, g=True)[0]
        jntList = cmds.skinCluster(skin, q=True, inf=True)
        # Geometry to DagPath
        meshDag = om2.MSelectionList().add(geometry).getDagPath(0)
        # Get the mesh origin position
        meshFn = om2.MFnMesh(meshDag)
        geoPosition = meshFn.getPoints(om2.MSpace.kObject)
        # Get the weight from each joint
        weightList = list()
        for x in range(len(jntList)):
            jntParent = cmds.listRelatives(jntList[x], p=True)
            jntChild = cmds.listRelatives(jntList[x], c=True)
            if jntParent: cmds.parent(jntList[x], w=True)
            if jntChild: cmds.parent(jntChild[0], w=True)
            jntDag = om2.MSelectionList().add(jntList[x]).getDagPath(0)
            transFn = om2.MFnTransform(jntDag)
            worldPos = transFn.translation(om2.MSpace.kWorld)
            moveWorld = om2.MVector(worldPos.x+1, worldPos.y, worldPos.z)
            transFn.setTranslation(moveWorld, om2.MSpace.kWorld)
            movePosition = meshFn.getPoints(om2.MSpace.kObject)
            jntWeights = list()
            for x in range(len(movePosition)):
                length = movePosition[x] - geoPosition[x]
                weight = length.length()
                jntWeights.append(weight)
            weightList.append(jntWeights)
            transFn.setTranslation(worldPos, om2.MSpace.kWorld)
        if jntParent: cmds.parent(jntList[x], jntParent[0])
        if jntChild: cmds.parent(jntChild[0], jntList[x])
        # Set joint weights to geometry
        geoSkin = cmds.skinCluster(jntList, geometry)[0]
        skinDepend = om2.MSelectionList().add(geoSkin).getDependNode(0)
        skinFn = oma2.MFnSkinCluster(skinDepend)
        # Vertex components
        vertexIndexList = range(len(geoPosition))
        indexCompFn = om2.MFnSingleIndexedComponent()
        vertexComp = indexCompFn.create(om2.MFn.kMeshVertComponent)
        indexCompFn.addElements(vertexIndexList)
        # Influences
        influenceObjs = skinFn.influenceObjects()
        influenceList = om2.MIntArray()
        for inf in influenceObjs:
            curIndex = skinFn.indexForInfluenceObject(inf)
            influenceList.append(curIndex)
        # Weights
        mWeightList = om2.MDoubleArray()
        for x in range(len(weightList[0])):
            for y in range(len(weightList)):
                mWeightList.append(weightList[y][x])
        skinFn.setWeights(meshDag, vertexComp, influenceList, mWeightList)
        cmds.setAttr('%s.envelope' % skin, 0)
        cmds.setAttr('%s.envelope' % ffd, 0)
