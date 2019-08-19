import sys
import math
import maya.cmds as cmds
from maya.api import OpenMaya as om2

def degToRad(deg):
    # RETURNS: result radians as float value.
    # 0- FORMULA: deg/180*pi
    # 1- Get the degrees value
    # 2- Return the radians value
    rad = deg / 180 * math.pi
    return rad

def radToDeg(rad):
    # RETURNS: result degrees as float value.
    # 0- FORMULA: rad*180/pi
    # 1- Get the radians value
    # 2- Return the degrees value
    deg = rad * 180 / math.pi
    return deg

def distanceBetween(obj1, obj2):
    # RETURNS: result distance as float value.
    # 0- FORMULA: ((A.x-B.x)**2+(A.y-B.y)**2+(A.z-B.z)**2)**0.5
    # 1- If both objects exists
    # 2- Get world xform from both objects
    # 3- Find vector AB
    # 4- Find distance between the 2 vectors
    if obj1 is None or not cmds.objExists(obj1): return False
    if obj2 is None or not cmds.objExists(obj2): return False
    objs = om2.MSelectionList()
    obj1Dag = objs.add(obj1).getDagPath(0)
    obj2Dag = objs.add(obj2).getDagPath(1)
    transFn = om2.MFnTransform(obj1Dag)
    vecA = transFn.translation(om2.MSpace.kWorld)
    transFn.setObject(obj2Dag)
    vecB = transFn.translation(om2.MSpace.kWorld)
    distance = math.sqrt(math.pow(vecA.x - vecB.x, 2) + math.pow(vecA.y - vecB.y, 2) + math.pow(vecA.z - vecB.z, 2))
    return distance

def lerp(obj1, obj2, wt):
    # RETURNS: result position as tuple3 value.
    # 0- FORMULA: (1-wt)*A+wt*B
    # 1- If both objects exists
    # 2- If weight value is between 0 and 1
    # 3- Get world xform from both objects
    # 4- Find lerp Value
    try: wt = float(wt)
    except: return False
    if wt < 0.0 or wt > 1.0: return False
    if obj1 is None or not cmds.objExists(obj1): return False
    if obj2 is None or not cmds.objExists(obj2): return False
    objs = om2.MSelectionList()
    obj1Dag = objs.add(obj1).getDagPath(0)
    obj2Dag = objs.add(obj2).getDagPath(1)
    transFn = om2.MFnTransform()
    transFn.setObject(obj1Dag)
    vecA = transFn.translation(om2.MSpace.kWorld)
    transFn.setObject(obj2Dag)
    vecB = transFn.translation(om2.MSpace.kWorld)
    lerp = (1 - wt) * vecA + wt * vecB
    lerp = (lerp.x, lerp.y, lerp.z)
    return lerp

def decomposeMatrix(obj, world=True, api=True):
    # RETURNS: result translation, rotation and scale as Maya Python API 2.0 functions or tuple values.
    # 0- FORMULA: Use MTransformationMatrix to decompose a matrix from a object
    # 1- Parse arguments
    # 2- Get world matrix from object
    # 3- Attach matrix into a MTransformationMatrix
    # 4- Extract decomposed channels into separated variables
    if type(obj) is not str: return False
    if type(world) is not bool: return False
    if type(api) is not bool: return False
    objDag = om2.MSelectionList().add(obj).getDagPath(0)
    matrix = objDag.inclusiveMatrix()
    if world is False:
        parentObj = om2.MFnDagNode(objDag).parent(0)
        parentDag = om2.MFnDagNode(parentObj).getPath()
        childWMatrix = matrix
        parentInverseWMatrix = parentDag.inclusiveMatrix().inverse()
        childLMatrix = childWMatrix * parentInverseWMatrix
        matrix = childLMatrix
    transMatrix = om2.MTransformationMatrix(matrix)
    translate = transMatrix.translation(om2.MSpace.kWorld)
    rotate = transMatrix.rotation(asQuaternion=False)
    scale = transMatrix.scale(om2.MSpace.kWorld)
    if api is False:
        translate = (translate.x, translate.y, translate.z)
        rotate = (radToDeg(rotate.x), radToDeg(rotate.y), radToDeg(rotate.z))
        scale = (scale[0], scale[1], scale[2])
        return translate, rotate, scale
    else: return translate, rotate, scale
