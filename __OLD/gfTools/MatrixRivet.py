# New Matrix Ribbon

# Aim Constraint Rivet
# Connect tangent U results in the same behaviour as a follicle.
sfc = 'Sfc_Shin'
posRivet = cmds.shadingNode('pointOnSurfaceInfo', asUtility=True, n=('Pos_Rivet_1'))
aimRivet = cmds.shadingNode('aimConstraint', asUtility=True, n=('Aim_Rivet_1'))
locResult = cmds.spaceLocator(p=(0, 0, 0), n=('Loc_Rivet_1'))[0]
cmds.connectAttr(sfc+'Shape.worldSpace[0]', posRivet+'.inputSurface')
cmds.setAttr(posRivet+'.turnOnPercentage', True)
cmds.setAttr(posRivet+'.parameterU', 0.5)
cmds.setAttr(posRivet+'.parameterV', 0)
cmds.connectAttr(posRivet+'.normal', aimRivet+'.target[0].targetTranslate')
cmds.connectAttr(posRivet+'.tangentV', aimRivet+'.worldUpVector')
cmds.connectAttr(posRivet+'.position', locResult+'.t')
cmds.connectAttr(aimRivet+'.constraintRotate', locResult+'.r')
cmds.parent(aimRivet, locResult)

# Matrix Math Rivet
# - First three rows of the matrix describe the X, Y and Z axis and the fourth row
# is the position
# - The third vector for third row is a cross product of the first 2 vectors
# - Connect tangent U results in the same behaviour as a follicle.
# - Rever world parent position
# - Rever vector product
# - If percentage turned off, the rivet snaps back to origin if value > 1
# - Write a node for these sliding setups and have the choice for tangent 
# U or V
sfc = 'Sfc_Shin'
posRivet = cmds.shadingNode('pointOnSurfaceInfo', asUtility=True, n=('Pos_Rivet_1'))
mtxRivet = cmds.shadingNode('fourByFourMatrix', asUtility=True, n=('Mtx_Rivet_1'))
vecRivet = cmds.shadingNode('vectorProduct', asUtility=True, n=('Vec_Rivet_1'))
dtxRivet = cmds.shadingNode('decomposeMatrix', asUtility=True, n=('Dtx_Rivet_1'))
locResult = cmds.spaceLocator(p=(0, 0, 0), n=('Loc_Rivet_1'))[0]
cmds.addAttr(locResult, ln='OffsetU', at='double', min = 0, dv=0, k=True)
cmds.addAttr(locResult, ln='OffsetV', at='double', min = 0, dv=0, k=True)
cmds.connectAttr(locResult+'.OffsetU', posRivet+'.parameterU')
cmds.connectAttr(locResult+'.OffsetV', posRivet+'.parameterV')
cmds.connectAttr(sfc+'Shape.worldSpace[0]', posRivet+'.inputSurface')
cmds.setAttr(posRivet+'.turnOnPercentage', True)
cmds.setAttr(locResult+'.OffsetU', 0.5)
cmds.setAttr(locResult+'.OffsetV', 0)
cmds.connectAttr(posRivet+'.normal', vecRivet+'.input1')
cmds.connectAttr(posRivet+'.tangentV', vecRivet+'.input2')
cmds.setAttr(vecRivet+'.operation', 2)
cmds.connectAttr(posRivet+'.normalX', mtxRivet+'.in00')
cmds.connectAttr(posRivet+'.normalY', mtxRivet+'.in01')
cmds.connectAttr(posRivet+'.normalZ', mtxRivet+'.in02')
cmds.connectAttr(posRivet+'.tangentVx', mtxRivet+'.in10')
cmds.connectAttr(posRivet+'.tangentVy', mtxRivet+'.in11')
cmds.connectAttr(posRivet+'.tangentVz', mtxRivet+'.in12')
cmds.connectAttr(vecRivet+'.outputX', mtxRivet+'.in20')
cmds.connectAttr(vecRivet+'.outputY', mtxRivet+'.in21')
cmds.connectAttr(vecRivet+'.outputZ', mtxRivet+'.in22')
cmds.connectAttr(posRivet+'.positionX', mtxRivet+'.in30')
cmds.connectAttr(posRivet+'.positionY', mtxRivet+'.in31')
cmds.connectAttr(posRivet+'.positionZ', mtxRivet+'.in32')
cmds.connectAttr(mtxRivet+'.output', dtxRivet+'.inputMatrix')
cmds.connectAttr(dtxRivet+'.outputTranslate', locResult+'.t')
cmds.connectAttr(dtxRivet+'.outputRotate', locResult+'.r')