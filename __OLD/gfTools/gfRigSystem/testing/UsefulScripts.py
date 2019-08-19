################################################################################################################################################################
################## USEFULL INFO
# 1- HumanLeg orientation is (L) XYZ+ XZY
################################################################################################################################################################

import sys
import math
import maya.cmds as cmds
import maya.api.OpenMaya as om2


def getDagPath(obj):
    sel = om2.MSelectionList()
    sel.add(obj)
    return sel.getDagPath(0).fullPathName()


def createChar(name):
    if cmds.objExists(name+'_char'):
        print('Char [%s] already created in this scene. [%s] loaded.' %(name, name))
        return name+'_char'
    else:
        charNode = cmds.group(em=True, n=name+'_char')
        cmds.setAttr(charNode+'.useOutlinerColor', True)
        cmds.setAttr(charNode+'.outlinerColor', 0.0, 1.0, 0.0)
        deform = cmds.group(em=True, n='deform_hrc')
        globalTransform = cmds.group(em=True, n='globalTransform_hrc')
        geometry = cmds.group(em=True, n='geometry_hrc')
        cmds.parent(deform, globalTransform, geometry, charNode)
        cmds.select(cl=True)
        return charNode


def createDeformationLayer(char, name):
    path = '|'+char+'|deform_hrc'
    if cmds.objExists(path):
        defLayer = cmds.group(em=True, n=name+'_defLyr')
        cmds.parent(defLayer, path)
        return defLayer
    else:
        cmds.error("Object don't exists: %s" %(char))
        return False


# Read Guides and create a joint chain
def createChain(guides, side, cmpnt, obj='srt', orient='XYY+', order='XYZ'):
    # USE: Select all the guides in order in a array, the orient (XYZ+)
    # and the rotation order (XZY) then run the function
    # 1- Parse all parameters
    # 2- Read all guides pos and create joints in each pos
    # 3- Connect all the joints created
    # 4- Apply orient and rotation order to joint chain
    # FOR UPDATE: Allow correct naming of joints
    oj = ''
    sao = ''
    rot = 0
    if guides == [] or guides == None: return False
    if type(side) is not str or side.upper() not in ['L', 'R', 'M']: return False
    if len(orient) != 4 or len(order) != 3: return False
    if obj.lower() not in ['srt', 'bnd']: return False
    for x in range(1, 5):
        if x != 4:
            if orient[x-1].upper() not in ['X', 'Y', 'Z']: return False
        else:
            if orient[x-1] not in ['+', '-']: return False
    if orient[0].upper() == 'X':
        if orient[1].upper() == 'Y': oj = 'xyz'
        elif orient[1].upper() == 'Z': oj = 'xzy'
    elif orient[0].upper() == 'Y':
        if orient[1].upper() == 'X': oj = 'yxz'
        elif orient[1].upper() == 'Z': oj = 'yzx'
    elif orient[0].upper() == 'Z':
        if orient[1].upper() == 'X': oj = 'zxy'
        elif orient[1].upper() == 'Y': oj = 'zyx'
    if orient[2].upper() == 'X':
        if orient[3] == '+': sao = 'xup'
        elif orient[3] == '-': sao = 'xdown'
    elif orient[2].upper() == 'Y':
        if orient[3] == '+': sao = 'yup'
        elif orient[3] == '-': sao = 'yup'
    elif orient[2].upper() == 'Z':
        if orient[3] == '+': sao = 'zup'
        elif orient[3] == '-': sao = 'zup'
    if order.upper() == 'XYZ': rot = 0
    elif order.upper() == 'YZX': rot = 1
    elif order.upper() == 'ZXY': rot = 2
    elif order.upper() == 'XZY': rot = 3
    elif order.upper() == 'YXZ': rot = 4
    elif order.upper() == 'ZYX': rot = 5
    else: return False
    # ----
    jnts = list()
    for x in range(len(guides)):
        if obj == 'bnd':
            if x == len(guides) - 1: name = cmpnt+'_'+side+'_joint'+str(x+1)+'_srt'
            else: name = cmpnt+'_'+side+'_joint'+str(x+1)+'_'+obj.lower()
        else: name = cmpnt+'_'+side+'_joint'+str(x+1)+'_'+obj.lower()
        cmds.select(cl=True)
        pos = cmds.xform(guides[x], q=True, ws=True, rp=True)
        jnt = cmds.joint(p=(0, 0, 0), n=name)
        jnts.append(jnt)
        cmds.xform(jnt, ws=True, t=(pos[0], pos[1], pos[2]))
    jnts.reverse()
    for x in range(len(jnts) - 1): cmds.parent(jnts[x], jnts[x+1])
    for x in range(len(jnts)): cmds.setAttr(jnts[x]+'.rotateOrder', rot)
    cmds.joint(jnts[-1], e=True, oj=oj, sao=sao, ch=True, zso=True)
    cmds.joint(jnts[0], e=True, oj='none', ch=True, zso=True)
    jnts.reverse()


def blendChains(in1, in2, outChain, blender, attrName, conn=['T', 'R', 'S']):
    # USE: Select each chain in a different array, blender obj and attr in another array, type a attrName
    # and select the attrs for connection ('T', 'R', 'S')
    # 1- Parse all parameters.
    # 2- Verify if the three chains length is the same. If not, set minimum for chain has less.
    # 3- Create a blendColors for each connection attrs and joint chains.
    # 4- Connect all attributes.
    if type(in1) is not list or in1 == []: return False
    if type(in2) is not list or in2 == []: return False
    if type(outChain) is not list or outChain == []: return False
    if type(blender) is not list: return False
    if type(attrName) is not str: return False
    if type(conn) is not list or conn == []: return False
    for x in range(len(conn)):
        if conn[x].upper() not in ['T', 'R', 'S']: return False
    # ------
    if len(in1) == len(in2) and len(in1) == len(outChain):
        for x in range(len(in1) - 1):
            nodeName = '_'.join(outChain[x].split('_')[:3])+attrName
            for y in range(len(conn)):
                bcNode = cmds.createNode('blendColors', n=nodeName+conn[y]+'_fNode')
                if blender == [] or blender == None: pass
                else: cmds.connectAttr(blender[0]+'.'+blender[1], bcNode+'.blender')
                cmds.connectAttr(in1[x]+'.'+conn[y].lower(), bcNode+'.color1')
                cmds.connectAttr(in2[x]+'.'+conn[y].lower(), bcNode+'.color2')
                cmds.connectAttr(bcNode+'.output', outChain[x]+'.'+conn[y].lower())
    else:
        pass


def getPoleVectorChain(inChain):
    startPos = cmds.xform(inChain[0], q=True, ws=True, t=True)
    midPos = cmds.xform(inChain[1], q=True, ws=True, t=True)
    endPos = cmds.xform(inChain[2], q=True, ws=True, t=True)
    startV = om2.MVector(startPos[0], startPos[1], startPos[2])
    midV = om2.MVector(midPos[0], midPos[1], midPos[2])
    endV = om2.MVector(endPos[0], endPos[1], endPos[2])
    startEnd = endV - startV
    startMid = midV - startV
    dotP = startMid * startEnd
    proj = float(dotP) / float(startEnd.length())
    startEndN = startEnd.normal()
    projV = startEndN * proj
    arrowV = startMid - projV
    arrowV *= 4
    finalV = arrowV + midV
    cross1 = startEnd ^ startMid
    cross1.normalize()
    cross2 = cross1 ^ arrowV
    cross2.normalize()
    arrowV.normalize()
    matrixV = [arrowV.x, arrowV.y, arrowV.z, 0,
               cross1.x, cross1.y, cross1.z, 0,
               cross2.x, cross2.y, cross2.z, 0,
               0, 0, 0, 1]
    matrixM = om2.MMatrix(matrixV)
    matrixFn = om2.MTransformationMatrix(matrixM)
    rot = matrixFn.rotation(asQuaternion=False)
    grp = cmds.group(empty=True, n='PVTEST')
    cmds.xform(grp, ws=True, t=(finalV.x, finalV.y, finalV.z))
    cmds.xform(grp, ws=True, ro=((rot.x / math.pi * 180.0),
                                 (rot.y / math.pi * 180.0),
                                 (rot.z / math.pi * 180.0))) # Radians to degrees


def createReverseLimb(h, o, i, t, chain, ik, ctrl):
    # 1- Create nulls
    # 2- Translate the nulls to correct position
    # 3- Create hierarchy
    # 4- Create attrs
    # 5- Setup reverse limb
    name = '_'.join(ctrl.split('_')[:2])+'_'
    ikParent = cmds.listRelatives(ik, p=True)[0]
    footHeel = h
    footOuter = o
    footInner = i
    footTip = t # Foot Toe
    footBall = cmds.group(em=True, n=name+'footBall_srt')
    footToeBend = cmds.group(em=True, n=name+'toeBendPivot_srt')
    pos = cmds.xform(chain[3], q=True, ws=True, rp=True)
    cmds.xform(footBall, ws=True, t=(pos[0], pos[1], pos[2]))
    cmds.xform(footToeBend, ws=True, t=(pos[0], pos[1], pos[2]))
    # Create Hierarchy
    cmds.parent(ik[0], footBall)
    cmds.parent(ik[1], footBall)
    cmds.parent(ik[2], footToeBend)
    cmds.parent(footBall, footTip)
    cmds.parent(footToeBend, footTip)
    cmds.parent(footTip, footInner)
    cmds.parent(footInner, footOuter)
    cmds.parent(footOuter, footHeel)
    cmds.parent(footHeel, ikParent)
    # Create Attrs
    ctrlPath = getDagPath(ctrl)
    cmds.addAttr(ctrlPath, ln='FOOTLABEL', nn='FOOT_____________________', at='enum', en='__________:')
    cmds.setAttr(ctrlPath+'.FOOTLABEL', e=True, channelBox=True, l=True)
    cmds.addAttr(ctrlPath, ln='foot', at='compound', nc=12)
    cmds.addAttr(ctrlPath, ln='footRoll', at='float', dv=0, p='foot', k=True)
    cmds.addAttr(ctrlPath, ln='footRollBreak', at='float', dv=45, p='foot', k=True)
    cmds.addAttr(ctrlPath, ln='footRollStraight', at='float', dv=70, p='foot', k=True)
    cmds.addAttr(ctrlPath, ln='footBank', at='float', dv=0, p='foot', k=True)
    cmds.addAttr(ctrlPath, ln='footTipSpin', at='doubleAngle', dv=0, p='foot', k=True)
    cmds.addAttr(ctrlPath, ln='footHeelSpin', at='doubleAngle', dv=0, p='foot', k=True)
    cmds.addAttr(ctrlPath, ln='ankleBend', at='float', dv=0, p='foot', k=True)
    cmds.addAttr(ctrlPath, ln='ankleTwist', at='doubleAngle', dv=0, p='foot', k=True)
    cmds.addAttr(ctrlPath, ln='ankleSpin', at='doubleAngle', dv=0, p='foot', k=True)
    cmds.addAttr(ctrlPath, ln='toeBend', at='doubleAngle', dv=0, p='foot', k=True)
    cmds.addAttr(ctrlPath, ln='toeTwist', at='doubleAngle', dv=0, p='foot', k=True)
    cmds.addAttr(ctrlPath, ln='toeSpin', at='doubleAngle', dv=0, p='foot', k=True)
    cmds.setAttr(ctrlPath+'.foot', e=True, channelBox=True)
    # Create Nodes
    rollPlusAnkleBend = cmds.createNode('addDoubleLinear', n='%sfootRollPlusAnkleBend_fNode' % name)
    bankClamp = cmds.createNode('clamp', n='%sfootBankClamp_fNode' % name)
    bendToStraightClamp = cmds.createNode('clamp', n='%sfootBendToStraightClamp_fNode' % name)
    heelRotClamp = cmds.createNode('clamp', n='%sfootHeelRotClamp_fNode' % name)
    zeroToBendClamp = cmds.createNode('clamp', n='%sfootZeroToBendClamp_fNode' % name)
    bendToStraightNormal = cmds.createNode('multDoubleLinear', n='%sfootBendToStraightNormallize_fNode' % name)
    rollMult = cmds.createNode('multDoubleLinear', n='%sfootRollMult_fNode' % name)
    rollPercent = cmds.createNode('multDoubleLinear', n='%sfootRollPercent_fNode' % name)
    bendToStraightInverse = cmds.createNode('floatMath', n='%sfootBendToStraightInverse_fNode' % name)
    bendToStraightRange = cmds.createNode('setRange', n='%sfootBendToStraightRange_fNode' % name)
    zeroToBendRange = cmds.createNode('setRange', n='%sfootZeroToBendRange_fNode' % name)
    # Setup Foot Roll
    cmds.connectAttr('%s.footRoll' % ctrl, '%s.inputR' % heelRotClamp)
    cmds.setAttr('%s.minR' % heelRotClamp, -90, l=True)
    cmds.connectAttr('%s.outputR' % heelRotClamp, '%s.rx' % footHeel)
    cmds.connectAttr('%s.footRoll' % ctrl, '%s.inputR' % zeroToBendClamp)
    cmds.connectAttr('%s.footRollBreak' % ctrl, '%s.maxR' % zeroToBendClamp)
    cmds.connectAttr('%s.minR' % zeroToBendClamp, '%s.oldMinX' % zeroToBendRange)
    cmds.connectAttr('%s.maxR' % zeroToBendClamp, '%s.oldMaxX' % zeroToBendRange)
    cmds.connectAttr('%s.inputR' % zeroToBendClamp, '%s.valueX' % zeroToBendRange)
    cmds.setAttr('%s.maxX' % zeroToBendRange, 1, l=True)
    cmds.connectAttr('%s.footRoll' % ctrl, '%s.inputR' % bendToStraightClamp)
    cmds.connectAttr('%s.footRollBreak' % ctrl, '%s.minR' % bendToStraightClamp)
    cmds.connectAttr('%s.footRollStraight' % ctrl, '%s.maxR' % bendToStraightClamp)
    cmds.connectAttr('%s.minR' % bendToStraightClamp, '%s.oldMinX' % bendToStraightRange)
    cmds.connectAttr('%s.maxR' % bendToStraightClamp, '%s.oldMaxX' % bendToStraightRange)
    cmds.connectAttr('%s.inputR' % bendToStraightClamp, '%s.valueX' % bendToStraightRange)
    cmds.setAttr('%s.maxX' % bendToStraightRange, 1, l=True)
    cmds.connectAttr('%s.outValueX' % bendToStraightRange, '%s.input1' % bendToStraightNormal)
    cmds.connectAttr('%s.inputR' % bendToStraightClamp, '%s.input2' % bendToStraightNormal)
    cmds.connectAttr('%s.output' % bendToStraightNormal, '%s.rx' % footTip)
    cmds.setAttr('%s.floatA' % bendToStraightInverse, 1, l=True)
    cmds.connectAttr('%s.outValueX' % bendToStraightRange, '%s.floatB' % bendToStraightInverse)
    cmds.setAttr('%s.operation' % bendToStraightInverse, 1, l=True)
    cmds.connectAttr('%s.outValueX' % zeroToBendRange, '%s.input1' % rollPercent)
    cmds.connectAttr('%s.outFloat' % bendToStraightInverse, '%s.input2' % rollPercent)
    cmds.connectAttr('%s.output' % rollPercent, '%s.input1' % rollMult)
    cmds.connectAttr('%s.footRoll' % ctrl, '%s.input2' % rollMult)
    cmds.connectAttr('%s.output' % rollMult, '%s.input1' % rollPlusAnkleBend)
    cmds.connectAttr('%s.ankleBend' % ctrl, '%s.input2' % rollPlusAnkleBend)
    cmds.connectAttr('%s.output' % rollPlusAnkleBend, '%s.rx' % footBall)
    # Setup Foot Bank
    cmds.connectAttr('%s.footBank' % ctrl, '%s.inputR' % bankClamp)
    cmds.connectAttr('%s.footBank' % ctrl, '%s.inputG' % bankClamp)
    cmds.setAttr('%s.minR' % bankClamp, 0, l=True)
    cmds.setAttr('%s.minG' % bankClamp, -90, l=True)
    cmds.setAttr('%s.maxR' % bankClamp, 90, l=True)
    cmds.setAttr('%s.maxG' % bankClamp, 0, l=True)
    cmds.connectAttr('%s.outputR' % bankClamp, '%s.rz' % footOuter)
    cmds.connectAttr('%s.outputG' % bankClamp, '%s.rz' % footInner)
    # Setup Other connections
    cmds.connectAttr('%s.footHeelSpin' % ctrl, '%s.ry' % footHeel)
    cmds.connectAttr('%s.footTipSpin' % ctrl, '%s.ry' % footTip)
    cmds.connectAttr('%s.ankleSpin' % ctrl, '%s.ry' % footBall)
    cmds.connectAttr('%s.ankleTwist' % ctrl, '%s.rz' % footBall)
    cmds.connectAttr('%s.toeBend' % ctrl, '%s.rx' % footToeBend)
    cmds.connectAttr('%s.toeSpin' % ctrl, '%s.ry' % footToeBend)
    cmds.connectAttr('%s.toeTwist' % ctrl, '%s.rz' % footToeBend)

def setupPv(pvCtrl, ikCtrl, ikHdle):
    # 1- Create Attrs
    # 2- Create Nulls
    # 3- Orient autoPvPivot null to pv control
    # 4- Create PV constraint
    # 5- Create and setup blend nodes
    name = '_'.join(ikHdle.split('_')[:2])
    if cmds.objExists('%s_cmpnt' % name):
        nonTransformPath = getDagPath('%s_cmpnt' % name)
        nonTransformPath += '|%s_nonTransform_srt' % name
        if not cmds.objExists(nonTransformPath): return False
        ikHdleName = ikHdle.split('_')[2]
        ikCtrlPath = getDagPath(ikCtrl)
        if not cmds.attributeQuery('autoManualPv', n=ikCtrl, ex=True):
            cmds.addAttr(ikCtrlPath, ln='autoManualPv', nn='Auto/Manual Pv', at='enum', en='auto:manual:', k=True)
        if not cmds.attributeQuery('kneeTwist', n=ikCtrl, ex=True):
            cmds.addAttr(ikCtrlPath, ln='kneeTwist', at='doubleAngle', dv=0, k=True)
        autoPvPivot = cmds.group(em=True, n='%s_autoPvPivot_srt' % name)
        autoPv = cmds.group(em=True, n='%s_autoPv_srt' % name)
        cmds.parent(autoPv, autoPvPivot)
        pos = cmds.xform(ikHdle, q=True, ws=True, rp=True)
        cmds.xform(autoPvPivot, ws=True, t=(pos[0], pos[1], pos[2]))
        cmds.xform(autoPv, ws=True, t=(10, 0, 0), r=True)
        cmds.parent(autoPvPivot, nonTransformPath)
        cmds.select(pvCtrl, autoPvPivot)
        const = cmds.aimConstraint(o=(0, 0, 0), w=1, aim=(0, 0, 1), u=(0, 1, 0), wut='objectrotation', wu=(0, 1, 0), wuo=ikHdle, sk=('x', 'z'))
        offsetValue = cmds.getAttr('%s.ry' % autoPvPivot)
        cmds.delete(const)
        cmds.xform(autoPvPivot, ws=True, ro=(0, 0, 0))
        cmds.select(autoPv, pvCtrl, ikHdle)
        pvConst = cmds.poleVectorConstraint(w=1)[0]
        autoPvOffset = cmds.createNode('addDoubleLinear', n='%s_autoPvOffset_fNode' % name)
        autoPvSwitch = cmds.createNode('condition', n='%s_autoManualPvSwitch_fNode' % name)
        autoPvReverseWeights = cmds.createNode('reverse', n='%s_autoManualPvReverseWeights_fNode' % name)
        ikHdleWMatrix = cmds.createNode('decomposeMatrix', n='%s_%sIKHdleWMatrix_fNode' % (name, ikHdleName))
        cmds.connectAttr('%s.autoManualPv' % ikCtrl, '%s.firstTerm' % autoPvSwitch)
        cmds.setAttr('%s.secondTerm' % autoPvSwitch, 0, l=True)
        cmds.setAttr('%s.colorIfTrueR' % autoPvSwitch, 90, l=True) # Twist IK
        cmds.setAttr('%s.colorIfTrueG' % autoPvSwitch, 1, l=True) # Const Weights
        cmds.setAttr('%s.colorIfTrueB' % autoPvSwitch, 0, l=True) # Control Vis
        cmds.setAttr('%s.colorIfFalseR' % autoPvSwitch, 0, l=True) # Twist IK
        cmds.setAttr('%s.colorIfFalseG' % autoPvSwitch, 0, l=True) # Const Weights
        cmds.setAttr('%s.colorIfFalseB' % autoPvSwitch, 1, l=True) # Control Vis
        cmds.connectAttr('%s.outColorR' % autoPvSwitch, '%s.twist' % ikHdle)
        cmds.connectAttr('%s.outColorG' % autoPvSwitch, '%s.%sW0' % (pvConst, autoPv))
        cmds.connectAttr('%s.outColorG' % autoPvSwitch, '%s.inputX' % autoPvReverseWeights)
        cmds.connectAttr('%s.outColorB' % autoPvSwitch, '%s.visibility' % pvCtrl)
        cmds.connectAttr('%s.outputX' % autoPvReverseWeights, '%s.%sW1' % (pvConst, pvCtrl))
        cmds.connectAttr('%s.kneeTwist' % ikCtrl, '%s.input1' % autoPvOffset)
        cmds.setAttr('%s.input2' % autoPvOffset, offsetValue, l=True)
        cmds.connectAttr('%s.output' % autoPvOffset, '%s.ry' % autoPvPivot)
        cmds.connectAttr('%s.worldMatrix' % ikHdle, '%s.inputMatrix' % ikHdleWMatrix)
        cmds.connectAttr('%s.outputTranslate' % ikHdleWMatrix, '%s.t' % autoPvPivot)
    else: return False

def setupSoftIK2(ikHdle, ctrl, upaxis):
    ikHdlePath = getDagPath(ikHdle)
    ctrlPath = getDagPath(ctrl)
    cmpntName = '_'.join(ikHdle.split('_')[:2])
    startJoint = cmds.listConnections('%s.startJoint' % ikHdle)
    endEffector = cmds.listConnections('%s.endEffector' % ikHdle)
    endJoint = cmds.listConnections(endEffector, d=False, s=True)[0]
    cmds.select(startJoint, hi=True)
    cmds.select(endJoint, hi=True, d=True)
    cmds.select(endEffector, d=True)
    cmds.select(endJoint, add=True)
    joints = cmds.ls(sl=True)
    midJoint = joints[1]
    cmds.select(cl=True)
    firstPos = cmds.xform(joints[0], q=True, ws=True, rp=True)
    lastPos = cmds.xform(joints[-1], q=True, ws=True, rp=True)
    ikHdlePivot = cmds.listRelatives(ikHdle, p=True)[0]
    # Find chainLength
    if not cmds.objExists('%s_chainLength_fNode' % cmpntName):
        nChainLength = cmds.createNode('addDoubleLinear', n='%s_chainLength_fNode' % cmpntName)
        cmds.setAttr('%s.input1' % nChainLength, cmds.getAttr('%s.tx' % midJoint))
        cmds.setAttr('%s.input2' % nChainLength, cmds.getAttr('%s.tx' % endJoint))
    else:
        nChainLength = '%s_chainLength_fNode' % cmpntName
    # Create the measures
    if not cmds.objExists('%s_thighPos_srt' % cmpntName):
        thighPos = cmds.group(em=True, n='%s_thighPos_srt' % cmpntName)
    else:
        thighPos = '%s_thighPos_srt' % cmpntName
    if not cmds.objExists('%s_anklePos_srt' % cmpntName):
        anklePos = cmds.group(em=True, n='%s_anklePos_srt' % cmpntName)
    else:
        anklePos = '%s_anklePos_srt' % cmpntName
    cmds.xform(thighPos, t=firstPos, ws=True)
    cmds.xform(anklePos, t=lastPos, ws=True)
    if not cmds.objExists('%s_stretchDist_fNode' % cmpntName):
        stretchDist = cmds.createNode('distanceBetween', n='%s_stretchDist_fNode' % cmpntName)
        cmds.connectAttr('%s.worldMatrix' % thighPos, '%s.inMatrix1' % stretchDist)
        cmds.connectAttr('%s.worldMatrix' % anklePos, '%s.inMatrix2' % stretchDist)
    else:
        stretchDist = '%s_stretchDist_fNode' % cmpntName
    if not cmds.objExists('%s_stretchDistGlobalScaleDiv_fNode' % cmpntName):
        if not cmds.objExists('global_M_globalScale_fNode'):
            masterGlobalScale = cmds.createNode('floatMath', n='global_M_globalScale_fNode')
            char = ctrlPath.split('|')[1]
            child = '%s|globalTransform_hrc' % char
            if cmds.objExists(child):
                while child is not None:
                    try:
                        child = cmds.listRelatives(child, c=True, type='transform', f=True)[0]
                    except:
                    	break
            try:
                wMatrix = cmds.listConnections(child, type='decomposeMatrix')[0]
            except TypeError as err:
                wMatrix = cmds.createNode('decomposeMatrix', n='global_M_masterCtrlWMatrix_fNode')
                cmds.connectAttr('%s.worldMatrix' % child, '%s.inputMatrix' % wMatrix)
            cmds.setAttr('%s.floatA' % masterGlobalScale, 1, l=True)
            cmds.setAttr('%s.operation' % masterGlobalScale, 3, l=True)
            cmds.connectAttr('%s.outputScaleY' % wMatrix, '%s.floatB' % masterGlobalScale)
        else:
            masterGlobalScale = 'global_M_globalScale_fNode'
        stretchDistGlobalScale = cmds.createNode('multDoubleLinear', n='%s_stretchDistGlobalScaleDiv_fNode' % cmpntName)
        cmds.connectAttr('%s.distance' % stretchDist, '%s.input1' % stretchDistGlobalScale)
        cmds.connectAttr('%s.outFloat' % masterGlobalScale, '%s.input2' % stretchDistGlobalScale)
    else:
        stretchDistGlobalScale = '%s_stretchDistGlobalScaleDiv_fNode' % cmpntName
    # Create attributes and soft Dist curve
    if not cmds.attributeQuery('dSoft', n=ikHdle, ex=True):
        cmds.addAttr(ikHdlePath, ln='dSoft', at='double', min=0.001, max=5, dv=0.001)
        cmds.setAttr('%s.dSoft' % ikHdlePath, e=True, cb=True)
    if not cmds.attributeQuery('softIK', n=ctrl, ex=True):
        cmds.addAttr(ctrlPath, ln='softIK', at='double', min=0, max=5, dv=0, k=True)
    softCurve = cmds.createNode('remapValue', n='%s_softDistCurve_fNode' % cmpntName)
    cmds.connectAttr('%s.softIK' % ctrl, '%s.inputValue' % softCurve)
    cmds.setAttr('%s.inputMin' % softCurve, 0)
    cmds.setAttr('%s.inputMax' % softCurve, 5)
    cmds.setAttr('%s.outputMin' % softCurve, 0.001)
    cmds.setAttr('%s.outputMax' % softCurve, 5)
    cmds.connectAttr('%s.outValue' % softCurve, '%s.dSoft' % ikHdle)
    # Setup node network
    #### NEW
    softRatio = cmds.createNode('floatMath', n='%s_softRatio_fNode' % cmpntName)
    softStretchBlend = cmds.createNode('blendColors', n='%s_softStretchBlend_fNode' % cmpntName)
    softDistPlusTranslation = cmds.createNode('addDoubleLinear', n='%s_softDistPlusTranslation_fNode' % cmpntName)
    #### END NEW
    clMinusDSoft = cmds.createNode('floatMath', n='%s_softChainLengthMinusDSoft_fNode' % cmpntName)
    stretchDistMinusSoftCl = cmds.createNode('floatMath', n='%s_softStretchDistMinusSoftCl_fNode' % cmpntName)
    negateSoftStretchDist = cmds.createNode('multDoubleLinear', n='%s_softNegateSoftStretchDist_fNode' % cmpntName)
    divByDSoft = cmds.createNode('floatMath', n='%s_softDivByDSoft_fNode' % cmpntName)
    powerE = cmds.createNode('floatMath', n='%s_softPowerE_fNode' % cmpntName)
    oneMinusPowerE = cmds.createNode('floatMath', n='%s_softOneMinusPowerE_fNode' % cmpntName)
    resPowerETimesDSoft = cmds.createNode('multDoubleLinear', n='%s_softResPowerETimesDSoft_fNode' % cmpntName)
    plusClMinusDSoft = cmds.createNode('addDoubleLinear', n='%s_softPlusChainLengthMinusDSoft_fNode' % cmpntName)
    softChainBend = cmds.createNode('condition', n='%s_softChainBend_fNode' % cmpntName)
    softDistDiff = cmds.createNode('floatMath', n='%s_softDistDiff_fNode' % cmpntName)
    softDistDefaultPos = cmds.createNode('floatMath', n='%s_softDistDefaultPos_fNode' % cmpntName)
    #### NEW
    cmds.setAttr('%s.operation' % softRatio, 3, l=True)
    #### END NEW
    cmds.setAttr('%s.operation' % clMinusDSoft, 1, l=True)
    cmds.setAttr('%s.operation' % stretchDistMinusSoftCl, 1, l=True)
    cmds.setAttr('%s.operation' % divByDSoft, 3, l=True)
    cmds.setAttr('%s.operation' % powerE, 6, l=True)
    cmds.setAttr('%s.operation' % oneMinusPowerE, 1, l=True)
    cmds.setAttr('%s.operation' % softChainBend, 5, l=True)
    cmds.setAttr('%s.operation' % softDistDiff, 1, l=True)
    cmds.setAttr('%s.operation' % softDistDefaultPos, 1, l=True)
    if upaxis.upper() == 'X' and defPos > 0: cmds.setAttr('%s.operation' % softDistDefaultPos, 0)
    elif upaxis.upper() == 'Z' and defPos < 0: cmds.setAttr('%s.operation' % softDistDefaultPos, 0)
    cmds.connectAttr('%s.output' % nChainLength, '%s.floatA' % clMinusDSoft)
    cmds.connectAttr('%s.dSoft' % ikHdle, '%s.floatB' % clMinusDSoft)
    cmds.connectAttr('%s.output' % stretchDistGlobalScale, '%s.floatA' % stretchDistMinusSoftCl) # Global Scale Stretch Dist
    cmds.connectAttr('%s.outFloat' % clMinusDSoft, '%s.floatB' % stretchDistMinusSoftCl)
    cmds.connectAttr('%s.outFloat' % stretchDistMinusSoftCl, '%s.input1' % negateSoftStretchDist)
    cmds.setAttr('%s.input2' % negateSoftStretchDist, -1, l=True)
    cmds.connectAttr('%s.output' % negateSoftStretchDist, '%s.floatA' % divByDSoft)
    cmds.connectAttr('%s.dSoft' % ikHdle, '%s.floatB' % divByDSoft)
    cmds.setAttr('%s.floatA' % powerE, math.exp(1), l=True)
    cmds.connectAttr('%s.outFloat' % divByDSoft, '%s.floatB' % powerE)
    cmds.setAttr('%s.floatA' % oneMinusPowerE, 1, l=True)
    cmds.connectAttr('%s.outFloat' % powerE, '%s.floatB' % oneMinusPowerE)
    cmds.connectAttr('%s.outFloat' % oneMinusPowerE, '%s.input1' % resPowerETimesDSoft)
    cmds.connectAttr('%s.dSoft' % ikHdle, '%s.input2' % resPowerETimesDSoft)
    cmds.connectAttr('%s.output' % resPowerETimesDSoft, '%s.input1' % plusClMinusDSoft)
    cmds.connectAttr('%s.outFloat' % clMinusDSoft, '%s.input2' % plusClMinusDSoft)
    cmds.connectAttr('%s.outFloat' % clMinusDSoft, '%s.firstTerm' % softChainBend)
    cmds.connectAttr('%s.output' % stretchDistGlobalScale, '%s.secondTerm' % softChainBend) # Global Scale Stretch Dist
    cmds.connectAttr('%s.output' % stretchDistGlobalScale, '%s.colorIfFalseR' % softChainBend) # Global Scale Stretch Dist
    cmds.connectAttr('%s.output' % plusClMinusDSoft, '%s.colorIfTrueR' % softChainBend)
    cmds.connectAttr('%s.outColorR' % softChainBend, '%s.floatA' % softDistDiff)
    cmds.connectAttr('%s.output' % stretchDistGlobalScale, '%s.floatB' % softDistDiff) # Global Scale Stretch Dist
    cmds.setAttr('%s.floatA' % softDistDefaultPos, 0, l=True)
    cmds.connectAttr('%s.outFloat' % softDistDiff, '%s.floatB' % softDistDefaultPos)
    #### NEW
    cmds.connectAttr('%s.output' % stretchDistGlobalScale, '%s.floatA' % softRatio)
    cmds.connectAttr('%s.outColorR' % softChainBend, '%s.floatB' % softRatio)
    cmds.connectAttr('%s.outFloat' % softRatio, '%s.color1R' % softStretchBlend)
    cmds.connectAttr('%s.outFloat' % softRatio, '%s.color1G' % softStretchBlend)
    cmds.setAttr('%s.color1B' % softStretchBlend, 0, l=True)
    cmds.setAttr('%s.color2R' % softStretchBlend, 1, l=True)
    cmds.setAttr('%s.color2G' % softStretchBlend, 1, l=True)
    cmds.connectAttr('%s.outFloat' % softDistDefaultPos, '%s.color2B' % softStretchBlend)
    cmds.connectAttr('%s.ty' % ctrl, '%s.input1' % softDistPlusTranslation)
    cmds.connectAttr('%s.outputB' % softStretchBlend, '%s.input2' % softDistPlusTranslation)
    cmds.connectAttr('%s.output' % softDistPlusTranslation, '%s.t%s' % (ikHdlePivot, upaxis.lower()), f=True)
    #### END NEW
    cmds.setAttr('ikRPsolver.tolerance', 1e-07)


def setupSoftIK(ikHdle, ctrl, upaxis):
    ikHdlePath = getDagPath(ikHdle)
    ctrlPath = getDagPath(ctrl)
    cmpntName = '_'.join(ikHdle.split('_')[:2])
    ctrlName = '_'.join(ctrl.split('_')[:3])
    startJoint = cmds.listConnections('%s.startJoint' % ikHdle)
    endEffector = cmds.listConnections('%s.endEffector' % ikHdle)
    endJoint = cmds.listConnections(endEffector, d=False, s=True)
    cmds.select(startJoint, hi=True)
    cmds.select(endJoint, hi=True, d=True)
    cmds.select(endEffector, d=True)
    cmds.select(endJoint, add=True)
    joints = cmds.ls(sl=True)
    midJoint = chain[1]
    cmds.select(cl=True)
    firstPos = cmds.xform(joints[0], q=True, ws=True, rp=True)
    lastPos = cmds.xform(joints[-1], q=True, ws=True, rp=True)
    # Find chainLength
    nChainLength = cmds.createNode('addDoubleLinear', n='%s_chainLength_fNode' % cmpntName)
    cmds.setAttr('%s.input1' % nChainLength, cmds.getAttr('%s.tx' % midJoint))
    cmds.setAttr('%s.input2' % nChainLength, cmds.getAttr('%s.tx' % endJoint))
    # chainLength = 0
    # for x in range(len(joints) - 1):
    #     a = cmds.xform(joints[x], q=True, ws=True, rp=True)
    #     b = cmds.xform(joints[x + 1], q=True, ws=True, rp=True)
    #     x = b[0] - a[0]
    #     y = b[1] - a[1]
    #     z = b[2] - a[2]
    #     v = [x, y, z]
    #     chainLength += math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2) + math.pow(v[2], 2))
    # defPos = cmds.getAttr('%s.translate%s' % (ikHdle, upaxis))
    # if upaxis.upper() == 'X' and lastPos[0] < 0: defPos = defPos * -1
    # elif upaxis.upper() == 'Y' and lastPos[1] < 0: defPos = defPos * -1
    # elif upaxis.upper() == 'Z' and lastPos[2] < 0: defPos = defPos * -1
    # Create the measures
    thighPos = cmds.group(em=True, n='%s_thighPos_srt' % cmpntName)
    anklePos = cmds.group(em=True, n='%s_anklePos_srt' % cmpntName)
    cmds.xform(thighPos, t=firstPos, ws=True)
    cmds.xform(anklePos, t=lastPos, ws=True)
    # cmds.parent(anklePos, ctrl)
    ctrlWMatrix = cmds.createNode('decomposeMatrix', n='%sWMatrix_fNode' % ctrlName)
    cmds.connectAttr('%s.worldMatrix' % ctrl, '%s.inputMatrix' % ctrlWMatrix)
    cmds.connectAttr('%s.outputTranslate' % ctrlWMatrix, '%s.t' % anklePos)
    stretchDist = cmds.createNode('distanceBetween', n='%s_stretchDist_fNode' % cmpntName)
    cmds.connectAttr('%s.worldMatrix' % thighPos, '%s.inMatrix1' % stretchDist)
    cmds.connectAttr('%s.worldMatrix' % anklePos, '%s.inMatrix2' % stretchDist)
    # Create attributes and soft Dist curve
    if not cmds.attributeQuery('dSoft', n=ikHdle, ex=True):
        cmds.addAttr(ikHdlePath, ln='dSoft', at='double', min=0.001, max=5, dv=0.001)
        cmds.setAttr('%s.dSoft' % ikHdlePath, e=True, cb=True)
    if not cmds.attributeQuery('softIK', n=ctrl, ex=True):
        cmds.addAttr(ctrlPath, ln='softIK', at='double', min=0, max=5, dv=0, k=True)
    softCurve = cmds.createNode('remapValue', n='%s_softDistCurve_fNode' % cmpntName)
    cmds.connectAttr('%s.softIK' % ctrl, '%s.inputValue' % softCurve)
    cmds.setAttr('%s.inputMin' % softCurve, 0)
    cmds.setAttr('%s.inputMax' % softCurve, 5)
    cmds.setAttr('%s.outputMin' % softCurve, 0.001)
    cmds.setAttr('%s.outputMax' % softCurve, 5)
    cmds.connectAttr('%s.outValue' % softCurve, '%s.dSoft' % ikHdle)
    # Setup node network
    clMinusDSoft = cmds.createNode('floatMath', n='%s_softChainLengthMinusDSoft_fNode' % cmpntName)
    stretchDistMinusSoftCl = cmds.createNode('floatMath', n='%s_softStretchDistMinusSoftCl_fNode' % cmpntName)
    negateSoftStretchDist = cmds.createNode('multDoubleLinear', n='%s_softNegateSoftStretchDist_fNode' % cmpntName)
    divByDSoft = cmds.createNode('floatMath', n='%s_softDivByDSoft_fNode' % cmpntName)
    powerE = cmds.createNode('floatMath', n='%s_softPowerE_fNode' % cmpntName)
    oneMinusPowerE = cmds.createNode('floatMath', n='%s_softOneMinusPowerE_fNode' % cmpntName)
    resPowerETimesDSoft = cmds.createNode('multDoubleLinear', n='%s_softResPowerETimesDSoft_fNode' % cmpntName)
    plusClMinusDSoft = cmds.createNode('addDoubleLinear', n='%s_softPlusChainLengthMinusDSoft_fNode' % cmpntName)
    softChainBend = cmds.createNode('condition', n='%s_softChainBend_fNode' % cmpntName)
    softDistDiff = cmds.createNode('floatMath', n='%s_softDistDiff_fNode' % cmpntName)
    softDistDefaultPos = cmds.createNode('floatMath', n='%s_softDistDefaultPos_fNode' % cmpntName)
    cmds.setAttr('%s.operation' % clMinusDSoft, 1, l=True)
    cmds.setAttr('%s.operation' % stretchDistMinusSoftCl, 1, l=True)
    cmds.setAttr('%s.operation' % divByDSoft, 3, l=True)
    cmds.setAttr('%s.operation' % powerE, 6, l=True)
    cmds.setAttr('%s.operation' % oneMinusPowerE, 1, l=True)
    cmds.setAttr('%s.operation' % softChainBend, 5, l=True)
    cmds.setAttr('%s.operation' % softDistDiff, 1, l=True)
    cmds.setAttr('%s.operation' % softDistDefaultPos, 1, l=True)
    if upaxis.upper() == 'X' and defPos > 0: cmds.setAttr('%s.operation' % softDistDefaultPos, 0)
    elif upaxis.upper() == 'Z' and defPos < 0: cmds.setAttr('%s.operation' % softDistDefaultPos, 0)
    cmds.connectAttr('%s.output' % nChainLength, '%s.floatA' % clMinusDSoft)
    cmds.connectAttr('%s.dSoft' % ikHdle, '%s.floatB' % clMinusDSoft)
    cmds.connectAttr('%s.distance' % stretchDist, '%s.floatA' % stretchDistMinusSoftCl)
    cmds.connectAttr('%s.outFloat' % clMinusDSoft, '%s.floatB' % stretchDistMinusSoftCl)
    cmds.connectAttr('%s.outFloat' % stretchDistMinusSoftCl, '%s.input1' % negateSoftStretchDist)
    cmds.setAttr('%s.input2' % negateSoftStretchDist, -1, l=True)
    cmds.connectAttr('%s.output' % negateSoftStretchDist, '%s.floatA' % divByDSoft)
    cmds.connectAttr('%s.dSoft' % ikHdle, '%s.floatB' % divByDSoft)
    cmds.setAttr('%s.floatA' % powerE, math.exp(1), l=True)
    cmds.connectAttr('%s.outFloat' % divByDSoft, '%s.floatB' % powerE)
    cmds.setAttr('%s.floatA' % oneMinusPowerE, 1, l=True)
    cmds.connectAttr('%s.outFloat' % powerE, '%s.floatB' % oneMinusPowerE)
    cmds.connectAttr('%s.outFloat' % oneMinusPowerE, '%s.input1' % resPowerETimesDSoft)
    cmds.connectAttr('%s.dSoft' % ikHdle, '%s.input2' % resPowerETimesDSoft)
    cmds.connectAttr('%s.output' % resPowerETimesDSoft, '%s.input1' % plusClMinusDSoft)
    cmds.connectAttr('%s.outFloat' % clMinusDSoft, '%s.input2' % plusClMinusDSoft)
    cmds.connectAttr('%s.outFloat' % clMinusDSoft, '%s.firstTerm' % softChainBend)
    cmds.connectAttr('%s.distance' % stretchDist, '%s.secondTerm' % softChainBend)
    cmds.connectAttr('%s.distance' % stretchDist, '%s.colorIfFalseR' % softChainBend)
    cmds.connectAttr('%s.output' % plusClMinusDSoft, '%s.colorIfTrueR' % softChainBend)
    cmds.connectAttr('%s.outColorR' % softChainBend, '%s.floatA' % softDistDiff)
    cmds.connectAttr('%s.distance' % stretchDist, '%s.floatB' % softDistDiff)
    cmds.setAttr('%s.floatA' % softDistDefaultPos, defPos, l=True)
    cmds.connectAttr('%s.outFloat' % softDistDiff, '%s.floatB' % softDistDefaultPos)
    # cmds.connectAttr('%s.outFloat' % softDistDefaultPos, '%s.translate%s' % (ikHdle, upaxis.upper()))
    cmds.setAttr('ikRPsolver.tolerance', 1e-07)


def setupStretchIK(chain, ikCtrl, pvCtrl, softNodes=None):
    translateBased = True
    ikCtrlPath = om2.MSelectionList().add(ikCtrl).getDagPath(0).fullPathName()
    pvCtrlPath = om2.MSelectionList().add(pvCtrl).getDagPath(0).fullPathName()
    cmpntName = '_'.join(ikCtrl.split('_')[:2])
    if not cmds.objExists('%s_thighPos_srt' % cmpntName):
        thighPos = cmds.group(em=True, n='%s_thighPos_srt' % cmpntName)
        pos = cmds.xform(chain[0], q=True, ws=True, rp=True)
        cmds.xform(thighPos, ws=True, t=(pos[0], pos[1], pos[2]))
    else:
        thighPos = '%s_thighPos_srt' % cmpntName
    if not cmds.objExists('%s_anklePos_srt' % cmpntName):
        anklePos = cmds.group(em=True, n='%s_anklePos_srt' % cmpntName)
        pos = cmds.xform(chain[2], q=True, ws=True, rp=True)
        cmds.xform(anklePos, ws=True, t=(pos[0], pos[1], pos[2]))
    else:
        anklePos = '%s_anklePos_srt' % cmpntName
    if not cmds.objExists('%s_pvPos_srt' % cmpntName):
        pvPos = cmds.group(em=True, n='%s_pvPos_srt' % cmpntName)
        cmds.parent(pvPos, pvCtrl)
        cmds.xform(pvPos, t=(0, 0, 0), ro=(0, 0, 0))
    else:
        pvPos = '%s_pvPos_srt' % cmpntName
    # Calculate distances
    if not cmds.objExists('%s_stretchDist_fNode' % cmpntName):
        stretchDist = cmds.createNode('distanceBetween', n='%s_stretchDist_fNode' % cmpntName)
        cmds.connectAttr('%s.worldMatrix' % thighPos, '%s.inMatrix1' % stretchDist)
        cmds.connectAttr('%s.worldMatrix' % anklePos, '%s.inMatrix2' % stretchDist)
    else:
        stretchDist = '%s_stretchDist_fNode' % cmpntName
    if not cmds.objExists('%s_chainLength_fNode' % cmpntName):
        chainLength = cmds.createNode('addDoubleLinear', n='%s_chainLength_fNode' % cmpntName)
        cmds.setAttr('%s.input1' % chainLength, cmds.getAttr('%s.tx' % chain[1]), l=True)
        cmds.setAttr('%s.input2' % chainLength, cmds.getAttr('%s.tx' % chain[2]), l=True)
    else:
        chainLength = '%s_chainLength_fNode' % cmpntName
    # Create attributes
    cmds.addAttr(ikCtrlPath, ln='kneeSlide', at='double', min=-1, max=1, dv=0, k=True)
    cmds.addAttr(ikCtrlPath, ln='softIK', at='double', min=0, max=5, dv=0, k=True)
    cmds.addAttr(ikCtrlPath, ln='stretch', at='bool', k=True)
    cmds.addAttr(ikCtrlPath, ln='squash', at='bool', k=True)
    cmds.addAttr(ikCtrlPath, ln='clampStretch', at='bool', k=True)
    cmds.addAttr(ikCtrlPath, ln='clampValue', at='double', min=1, dv=1.5, k=True)
    cmds.addAttr(ikCtrlPath, ln='curStretchValue', at='double', dv=0)
    cmds.setAttr('%s.curStretchValue' % ikCtrlPath, e=True, cb=True)
    cmds.addAttr(ikCtrlPath, ln='thighStretchMult', at='double', min=0, dv=1, k=True)
    cmds.addAttr(ikCtrlPath, ln='thighSquashFBMult', nn='Thigh Squash FB Mult', at='double', min=0, dv=1, k=True)
    cmds.addAttr(ikCtrlPath, ln='thighSquashLRMult', nn='Thigh Squash LR Mult', at='double', min=0, dv=1, k=True)
    cmds.addAttr(ikCtrlPath, ln='shinStretchMult', at='double', min=0, dv=1, k=True)
    cmds.addAttr(ikCtrlPath, ln='shinSquashFBMult', nn='Shin Squash FB Mult', at='double', min=0, dv=1, k=True)
    cmds.addAttr(ikCtrlPath, ln='shinSquashLRMult', nn='Shin Squash LR Mult', at='double', min=0, dv=1, k=True)
    cmds.addAttr(pvCtrlPath, ln='pinKnee', at='double', min=0, max=1, dv=0, k=True)
    cmds.addAttr(pvCtrlPath, ln='pinKneeDist', at='double', k=True)
    # Create Stretch nodes
    if translateBased == True:
        stretchTransConvert = cmds.createNode('multiplyDivide', n='%s_stretchTransConvert_fNode' % cmpntName)
    if not cmds.objExists('global_M_globalScale_fNode'):
        masterGlobalScale = cmds.createNode('floatMath', n='global_M_globalScale_fNode')
        char = ikCtrlPath.split('|')[1]
        child = '%s|globalTransform_hrc' % char
        if cmds.objExists(child):
            while child is not None:
                try:
                    child = cmds.listRelatives(child, c=True, type='transform', f=True)[0]
                except:
                	break
        try:
            wMatrix = cmds.listConnections(child, type='decomposeMatrix')[0]
        except TypeError as err:
            wMatrix = cmds.createNode('decomposeMatrix', n='global_M_masterCtrlWMatrix_fNode')
            cmds.connectAttr('%s.worldMatrix' % child, '%s.inputMatrix' % wMatrix)
        cmds.setAttr('%s.floatA' % masterGlobalScale, 1, l=True)
        cmds.setAttr('%s.operation' % masterGlobalScale, 3, l=True)
        cmds.connectAttr('%s.outputScaleY' % wMatrix, '%s.floatB' % masterGlobalScale)
    else:
        masterGlobalScale = 'global_M_globalScale_fNode'
    if not cmds.objExists('%s_stretchDistGlobalScaleDiv_fNode' % cmpntName):
        stretchDistGlobalScale = cmds.createNode('multDoubleLinear', n='%s_stretchDistGlobalScaleDiv_fNode' % cmpntName)
    else:
        stretchDistGlobalScale = '%s_stretchDistGlobalScaleDiv_fNode' % cmpntName
    stretchDiv = cmds.createNode('floatMath', n='%s_stretchDiv_fNode' % cmpntName)
    stretchChainBend = cmds.createNode('condition', n='%s_stretchChainBend_fNode' % cmpntName)
    stretchMultSwitch = cmds.createNode('condition', n='%s_stretchMultSwitch_fNode' % cmpntName)
    stretchMult = cmds.createNode('multiplyDivide', n='%s_stretchMult_fNode' % cmpntName)
    clampStretchSwitch = cmds.createNode('floatCondition', n='%s_clampStretchSwitch_fNode' % cmpntName)
    clampStretch = cmds.createNode('clamp', n='%s_clampStretch_fNode' % cmpntName)
    thighSlide = cmds.createNode('floatMath', n='%s_thighSlide_fNode' % cmpntName)
    shinSlide = cmds.createNode('floatMath', n='%s_shinSlide_fNode' % cmpntName)
    slideClamp = cmds.createNode('clamp', n='%s_slideClamp_fNode' % cmpntName)
    stretchDiff = cmds.createNode('floatMath', n='%s_stretchDiff_fNode' % cmpntName)
    stretchSlide = cmds.createNode('floatMath', n='%s_stretchSlide_fNode' % cmpntName)
    stretchSlideMult = cmds.createNode('multiplyDivide', n='%s_stretchSlideMult_fNode' % cmpntName)
    squashSwitch = cmds.createNode('multDoubleLinear', n='%s_squashSwitch_fNode' % cmpntName)
    squashSqrt = cmds.createNode('floatMath', n='%s_squashSqrt_fNode' % cmpntName)
    squashInv = cmds.createNode('multiplyDivide', n='%s_squashInv_fNode' % cmpntName)
    thighSquashMultSwitch = cmds.createNode('condition', n='%s_thighSquashMultSwitch_fNode' % cmpntName)
    shinSquashMultSwitch = cmds.createNode('condition', n='%s_shinSquashMultSwitch_fNode' % cmpntName)
    thighSquashMult = cmds.createNode('multiplyDivide', n='%s_thighSquashMult_fNode' % cmpntName)
    shinSquashMult = cmds.createNode('multiplyDivide', n='%s_shinSquashMult_fNode' % cmpntName)
    thighToPvDist = cmds.createNode('distanceBetween', n='%s_thighToPvDist_fNode' % cmpntName)
    pvToAnkleDist = cmds.createNode('distanceBetween', n='%s_pvToAnkleDist_fNode' % cmpntName)
    cmds.connectAttr('%s.worldMatrix' % thighPos, '%s.inMatrix1' % thighToPvDist)
    cmds.connectAttr('%s.worldMatrix' % pvPos, '%s.inMatrix2' % thighToPvDist)
    cmds.connectAttr('%s.worldMatrix' % pvPos, '%s.inMatrix1' % pvToAnkleDist)
    cmds.connectAttr('%s.worldMatrix' % anklePos, '%s.inMatrix2' % pvToAnkleDist)
    pinKneeSwitch = cmds.createNode('blendColors', n='%s_pinKneeSwitch_fNode' % cmpntName)
    pinKnee = cmds.createNode('multiplyDivide', n='%s_pinKneeDiv_fNode' % cmpntName)
    pinKneeDist = cmds.createNode('multDoubleLinear', n='%s_pinKneeDist_fNode' % cmpntName)
    stretchAutoManualPvSwitch = cmds.createNode('condition', n='%s_stretchAutoManualPvSwitch_fNode' % cmpntName)
    # Create Setup
    cmds.connectAttr('%s.distance' % stretchDist, '%s.input1' % stretchDistGlobalScale)
    cmds.connectAttr('%s.outFloat' % masterGlobalScale, '%s.input2' % stretchDistGlobalScale)
    cmds.connectAttr('%s.output' % stretchDistGlobalScale, '%s.floatA' % stretchDiv)
    cmds.connectAttr('%s.output' % chainLength, '%s.floatB' % stretchDiv)
    cmds.setAttr('%s.operation' % stretchDiv, 3, l=True)
    cmds.connectAttr('%s.outFloat' % stretchDiv, '%s.firstTerm' % stretchChainBend)
    cmds.setAttr('%s.secondTerm' % stretchChainBend, 1, l=True)
    cmds.setAttr('%s.operation' % stretchChainBend, 3, l=True)
    cmds.setAttr('%s.colorIfFalseR' % stretchChainBend, 1, l=True)
    cmds.connectAttr('%s.outFloat' % stretchDiv, '%s.colorIfTrueR' % stretchChainBend)
    cmds.connectAttr('%s.outColorR' % stretchChainBend, '%s.inputR' % clampStretch)
    cmds.connectAttr('%s.clampValue' % ikCtrl, '%s.maxR' % clampStretch)
    cmds.connectAttr('%s.outputR' % clampStretch, '%s.floatA' % clampStretchSwitch)
    cmds.connectAttr('%s.outColorR' % stretchChainBend, '%s.floatB' % clampStretchSwitch)
    cmds.connectAttr('%s.clampStretch' % ikCtrl, '%s.condition' % clampStretchSwitch)
    cmds.connectAttr('%s.stretch' % ikCtrl, '%s.firstTerm' % stretchMultSwitch)
    cmds.setAttr('%s.secondTerm' % stretchMultSwitch, 1, l=True)
    cmds.setAttr('%s.operation' % stretchMultSwitch, 0, l=True)
    cmds.connectAttr('%s.outFloat' % clampStretchSwitch, '%s.colorIfTrueR' % stretchMultSwitch) # '%s.outFloat' % clampStretchSwitch
    cmds.connectAttr('%s.thighStretchMult' % ikCtrl, '%s.colorIfTrueG' % stretchMultSwitch)
    cmds.connectAttr('%s.shinStretchMult' % ikCtrl, '%s.colorIfTrueB' % stretchMultSwitch)
    cmds.setAttr('%s.colorIfFalse' % stretchMultSwitch, 1, 1, 1, l=True)
    cmds.setAttr('%s.operation' % stretchMult, 1, l=True)
    cmds.connectAttr('%s.outColorG' % stretchMultSwitch, '%s.input1X' % stretchMult)
    cmds.connectAttr('%s.outColorB' % stretchMultSwitch, '%s.input1Y' % stretchMult)
    cmds.connectAttr('%s.outColorR' % stretchMultSwitch, '%s.input2X' % stretchMult)
    cmds.connectAttr('%s.outColorR' % stretchMultSwitch, '%s.input2Y' % stretchMult)
    cmds.connectAttr('%s.outColorR' % stretchMultSwitch, '%s.curStretchValue' % ikCtrl)
    cmds.connectAttr('%s.squash' % ikCtrl, '%s.input1' % squashSwitch)
    cmds.setAttr('%s.input2' % squashSwitch, 2, l=True)
    cmds.connectAttr('%s.outFloat' % clampStretchSwitch, '%s.floatA' % squashSqrt) # '%s.outFloat' % clampStretchSwitch
    cmds.setAttr('%s.floatB' % squashSqrt, 0.5, l=True)
    cmds.setAttr('%s.operation' % squashSqrt, 6, l=True)
    cmds.setAttr('%s.input1X' % squashInv, 1, l=True)
    cmds.connectAttr('%s.outFloat' % squashSqrt, '%s.input2X' % squashInv)
    cmds.connectAttr('%s.output' % squashSwitch, '%s.operation' % squashInv)
    cmds.connectAttr('%s.squash' % ikCtrl, '%s.firstTerm' % thighSquashMultSwitch)
    cmds.connectAttr('%s.squash' % ikCtrl, '%s.firstTerm' % shinSquashMultSwitch)
    cmds.setAttr('%s.secondTerm' % thighSquashMultSwitch, 1, l=True)
    cmds.setAttr('%s.secondTerm' % shinSquashMultSwitch, 1, l=True)
    cmds.setAttr('%s.operation' % thighSquashMultSwitch, 0, l=True)
    cmds.setAttr('%s.operation' % shinSquashMultSwitch, 0, l=True)
    cmds.connectAttr('%s.outputX' % squashInv, '%s.colorIfTrueR' % thighSquashMultSwitch)
    cmds.connectAttr('%s.thighSquashFBMult' % ikCtrl, '%s.colorIfTrueG' % thighSquashMultSwitch)
    cmds.connectAttr('%s.thighSquashLRMult' % ikCtrl, '%s.colorIfTrueB' % thighSquashMultSwitch)
    cmds.connectAttr('%s.outputX' % squashInv, '%s.colorIfTrueR' % shinSquashMultSwitch)
    cmds.connectAttr('%s.shinSquashFBMult' % ikCtrl, '%s.colorIfTrueG' % shinSquashMultSwitch)
    cmds.connectAttr('%s.shinSquashLRMult' % ikCtrl, '%s.colorIfTrueB' % shinSquashMultSwitch)
    cmds.setAttr('%s.colorIfFalse' % thighSquashMultSwitch, 1, 1, 1, l=True)
    cmds.setAttr('%s.colorIfFalse' % shinSquashMultSwitch, 1, 1, 1, l=True)
    cmds.setAttr('%s.operation' % thighSquashMult, 1, l=True)
    cmds.setAttr('%s.operation' % shinSquashMult, 1, l=True)
    cmds.connectAttr('%s.outColorG' % thighSquashMultSwitch, '%s.input1X' % thighSquashMult)
    cmds.connectAttr('%s.outColorB' % thighSquashMultSwitch, '%s.input1Y' % thighSquashMult)
    cmds.connectAttr('%s.outColorR' % thighSquashMultSwitch, '%s.input2X' % thighSquashMult)
    cmds.connectAttr('%s.outColorR' % thighSquashMultSwitch, '%s.input2Y' % thighSquashMult)
    cmds.connectAttr('%s.outColorG' % shinSquashMultSwitch, '%s.input1X' % shinSquashMult)
    cmds.connectAttr('%s.outColorB' % shinSquashMultSwitch, '%s.input1Y' % shinSquashMult)
    cmds.connectAttr('%s.outColorR' % shinSquashMultSwitch, '%s.input2X' % shinSquashMult)
    cmds.connectAttr('%s.outColorR' % shinSquashMultSwitch, '%s.input2Y' % shinSquashMult)
    cmds.setAttr('%s.input1' % pinKneeDist, -1, l=True)
    cmds.connectAttr('%s.pinKneeDist' % pvCtrl, '%s.input2' % pinKneeDist)
    cmds.connectAttr('%s.output' % pinKneeDist, '%s.tx' % pvPos)
    cmds.setAttr('%s.operation' % pinKnee, 2, l=True)
    cmds.connectAttr('%s.distance' % thighToPvDist, '%s.input1X' % pinKnee)
    cmds.connectAttr('%s.distance' % pvToAnkleDist, '%s.input1Y' % pinKnee)
    cmds.connectAttr('%s.input1' % chainLength, '%s.input2X' % pinKnee)
    cmds.connectAttr('%s.input2' % chainLength, '%s.input2Y' % pinKnee)
    cmds.connectAttr('%s.pinKnee' % pvCtrl, '%s.blender' % pinKneeSwitch)
    cmds.connectAttr('%s.outputX' % pinKnee, '%s.color1R' % pinKneeSwitch)
    cmds.connectAttr('%s.outputY' % pinKnee, '%s.color1G' % pinKneeSwitch)
    cmds.connectAttr('%s.outColorR' % stretchChainBend, '%s.color2R' % pinKneeSwitch)
    cmds.connectAttr('%s.outColorR' % stretchChainBend, '%s.color2G' % pinKneeSwitch)
    cmds.connectAttr('%s.autoManualPv' % ikCtrl, '%s.firstTerm' % stretchAutoManualPvSwitch)
    cmds.setAttr('%s.secondTerm' % stretchAutoManualPvSwitch, 0, l=True)
    cmds.setAttr('%s.operation' % stretchAutoManualPvSwitch, 0, l=True)
    cmds.connectAttr('%s.outputX' % stretchMult, '%s.colorIfTrueR' % stretchAutoManualPvSwitch)
    cmds.connectAttr('%s.outputY' % stretchMult, '%s.colorIfTrueG' % stretchAutoManualPvSwitch)
    cmds.connectAttr('%s.outputR' % pinKneeSwitch, '%s.colorIfFalseR' % stretchAutoManualPvSwitch)
    cmds.connectAttr('%s.outputG' % pinKneeSwitch, '%s.colorIfFalseG' % stretchAutoManualPvSwitch)
    cmds.connectAttr('%s.outputX' % stretchMult, '%s.floatA' % thighSlide)
    cmds.connectAttr('%s.outputY' % stretchMult, '%s.floatA' % shinSlide)
    cmds.connectAttr('%s.kneeSlide' % ikCtrl, '%s.floatB' % thighSlide)
    cmds.connectAttr('%s.kneeSlide' % ikCtrl, '%s.floatB' % shinSlide)
    cmds.setAttr('%s.operation' % thighSlide, 0, l=True)
    cmds.setAttr('%s.operation' % shinSlide, 1, l=True)
    cmds.connectAttr('%s.outFloat' % thighSlide, '%s.inputR' % slideClamp)
    cmds.connectAttr('%s.outFloat' % shinSlide, '%s.inputG' % slideClamp)
    cmds.setAttr('%s.minR' % slideClamp, 0.05, l=True)
    cmds.setAttr('%s.minG' % slideClamp, 0.05, l=True)
    cmds.setAttr('%s.maxR' % slideClamp, 1.95, l=True)
    cmds.setAttr('%s.maxG' % slideClamp, 1.95, l=True)
    cmds.connectAttr('%s.outputX' % stretchSlideMult, '%s.color2R' % pinKneeSwitch, f=True)
    cmds.connectAttr('%s.outputY' % stretchSlideMult, '%s.color2G' % pinKneeSwitch, f=True)
    cmds.connectAttr('%s.outputR' % slideClamp, '%s.colorIfTrueR' % stretchAutoManualPvSwitch, f=True)
    cmds.connectAttr('%s.outputG' % slideClamp, '%s.colorIfTrueG' % stretchAutoManualPvSwitch, f=True)
    cmds.connectAttr('%s.outFloat' % clampStretchSwitch, '%s.floatA' % stretchDiff) # '%s.outFloat' % clampStretchSwitch
    cmds.setAttr('%s.floatB' % stretchDiff, 1, l=True)
    cmds.setAttr('%s.operation' % stretchDiff, 1, l=True)
    cmds.connectAttr('%s.outFloat' % clampStretchSwitch, '%s.floatA' % stretchSlide) # '%s.outFloat' % clampStretchSwitch
    cmds.connectAttr('%s.outFloat' % stretchDiff, '%s.floatB' % stretchSlide)
    cmds.setAttr('%s.operation' % stretchSlide, 1, l=True)
    cmds.connectAttr('%s.outFloat' % stretchSlide, '%s.floatA' % thighSlide, f=True)
    cmds.connectAttr('%s.outFloat' % stretchSlide, '%s.floatA' % shinSlide, f=True)
    cmds.connectAttr('%s.outputX' % stretchMult, '%s.input1X' % stretchSlideMult)
    cmds.connectAttr('%s.outputY' % stretchMult, '%s.input1Y' % stretchSlideMult)
    cmds.connectAttr('%s.outputR' % slideClamp, '%s.input2X' % stretchSlideMult)
    cmds.connectAttr('%s.outputG' % slideClamp, '%s.input2Y' % stretchSlideMult)
    cmds.setAttr('%s.operation' % stretchSlideMult, 1, l=True)
    cmds.connectAttr('%s.outputX' % stretchSlideMult, '%s.colorIfTrueR' % stretchAutoManualPvSwitch, f=True)
    cmds.connectAttr('%s.outputY' % stretchSlideMult, '%s.colorIfTrueG' % stretchAutoManualPvSwitch, f=True)
    if translateBased == True:
        cmds.connectAttr('%s.input1' % chainLength, '%s.input1X' % stretchTransConvert)
        cmds.connectAttr('%s.input2' % chainLength, '%s.input1Y' % stretchTransConvert)
        cmds.connectAttr('%s.outColorR' % stretchAutoManualPvSwitch, '%s.input2X' % stretchTransConvert)
        cmds.connectAttr('%s.outColorG' % stretchAutoManualPvSwitch, '%s.input2Y' % stretchTransConvert)
        cmds.connectAttr('%s.outputX' % stretchTransConvert, '%s.tx' % chain[1])
        cmds.connectAttr('%s.outputY' % stretchTransConvert, '%s.tx' % chain[2])
    else:
        cmds.connectAttr('%s.outColorR' % stretchAutoManualPvSwitch, '%s.sx' % chain[0])
        cmds.connectAttr('%s.outColorG' % stretchAutoManualPvSwitch, '%s.sx' % chain[1])
    cmds.connectAttr('%s.outputX' % thighSquashMult, '%s.sy' % chain[0])
    cmds.connectAttr('%s.outputY' % thighSquashMult, '%s.sz' % chain[0])
    cmds.connectAttr('%s.outputX' % shinSquashMult, '%s.sy' % chain[1])
    cmds.connectAttr('%s.outputY' % shinSquashMult, '%s.sz' % chain[1])



def matrixConstraint(parent, child, name, mo=False, conn=['T', 'R', 'S']):
    if type(parent) is not list or parent == []: return False
    if type(child) is not str: return False
    if len(parent) < 1 or len(parent) > 2: return False
    if type(name) is not str or name == '': return False
    if type(conn) is not list or conn == []: return False
    if type(mo) is not bool: return False
    for x in range(len(conn)):
        if conn[x].upper() not in ['T', 'R', 'S']: return False
    decompConn = {'T':'outputTranslate', 'R':'outputRotate', 'S':'outputScale'}
    nodeName = '_'.join(child.split('_')[:3])+name
    multNode = cmds.createNode('multMatrix', n=nodeName+'_fNode')
    decompNode = cmds.createNode('decomposeMatrix', n=nodeName+'Decomp_fNode')
    if len(parent) == 1:
        if mo == False:
            cmds.connectAttr(parent[0]+'.worldMatrix', multNode+'.matrixIn[0]')
            cmds.connectAttr(child+'.parentInverseMatrix', multNode+'.matrixIn[1]')
        else:
            sel = om2.MSelectionList()
            sel.add(parent[0])
            sel.add(child)
            dag = sel.getDagPath(0)
            parentWorldMatrix = dag.inclusiveMatrix()
            dag = sel.getDagPath(1)
            childWorldMatrix = dag.inclusiveMatrix()
            localOffset = childWorldMatrix * parentWorldMatrix.inverse()
            cmds.setAttr(multNode+'.matrixIn[0]', localOffset, type='matrix')
            cmds.connectAttr(parent[0]+'.worldMatrix', multNode+'.matrixIn[1]')
            cmds.connectAttr(child+'.parentInverseMatrix', multNode+'.matrixIn[2]')
    elif len(parent) == 2:
        addNode = cmds.createNode('wtAddMatrix', n=nodeName+'BlendParents_fNode')
        for x in range(len(parent)):
            if mo == False:
                cmds.connectAttr(parent[x]+'.worldMatrix', addNode+'.wtMatrix[%s].matrixIn'%(x))
                cmds.setAttr(addNode+'.wtMatrix[%s].weightIn'%(x), 0.5)
            else:
                parMultNode = cmds.createNode('multMatrix', n=nodeName+'Parent%sOffset_fNode'%(x))
                sel = om2.MSelectionList()
                sel.add(parent[x])
                sel.add(child)
                dag = sel.getDagPath(0)
                parentWorldMatrix = dag.inclusiveMatrix()
                dag = sel.getDagPath(1)
                childWorldMatrix = dag.inclusiveMatrix()
                localOffset = childWorldMatrix * parentWorldMatrix.inverse()
                cmds.setAttr(parMultNode+'.matrixIn[%s]'%(x), localOffset, type='matrix')
                cmds.connectAttr(parent[x]+'.worldMatrix', parMultNode+'.matrixIn[%s]'%(x+1))
                cmds.connectAttr(parMultNode+'.matrixSum', addNode+'.wtMatrix[%s].matrixIn'%(x))
                cmds.setAttr(addNode+'.wtMatrix[%s].weightIn'%(x), 0.5)
        cmds.connectAttr(addNode+'.matrixSum', multNode+'.matrixIn[0]')
        cmds.connectAttr(child+'.parentInverseMatrix', multNode+'.matrixIn[1]')
    cmds.connectAttr(multNode+'.matrixSum', decompNode+'.inputMatrix')
    for x in range(len(conn)):
        attr = decompConn.get(conn[x])
        cmds.connectAttr(decompNode+'.'+attr, child+'.'+conn[x].lower())
