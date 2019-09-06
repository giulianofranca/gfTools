#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Testing.

Todo:
    * TODO(createAttributeTypes): Add support to create Compounds.
    * TODO(addMetadataChar): Add metadata in char node create by createChar() and catch in createComponent().

Source:
    * https://docs.python.org/2/extending/embedding.html
    * https://www.youtube.com/watch?v=P9edayG8rkg
"""
import maya.cmds as cmds
import maya.api._OpenMaya_py2 as om2


def createChar(name):
    """Create a character node hierarchy.

    Args:
        name (string): The name of the character node.

    Returns:
        string: The Dag Path of the char node.
    """
    charObj = om2.MFnDagNode().create("transform", "%s_char" % name)
    om2.MFnDagNode().create("transform", "deform_hrc", charObj)
    om2.MFnDagNode().create("transform", "geometry_hrc", charObj)
    nodeFn = om2.MFnDependencyNode(charObj)
    plug = nodeFn.findPlug("useOutlinerColor", True)
    plug.setBool(True)
    plug = nodeFn.findPlug("outlinerColor", True)
    dataHandle = plug.asMDataHandle()
    dataHandle.set3Float(0.988, 0.961, 0.392)
    plug.setMDataHandle(dataHandle)
    sel = om2.MSelectionList().add(nodeFn.name())
    charPath = sel.getDagPath(0)
    om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectObjectMode)
    om2.MGlobal.setActiveSelectionList(sel)
    return charPath

def createComponent(char, name):
    """Create a component node hierarchy in a char node hierarchy.

    Args:
        char (string): The name of the character node.
        name (string): The name of the component node.

    Returns:
        string: The Dag Path of the component node.

    Raises:
        RuntimeError: If char don't exists.
    """
    if "_char" not in char:
        charName = "".join([char, "_char"])
    else:
        charName = char
    charPath = om2.MSelectionList().add(charName).getDagPath(0)
    dagFn = om2.MFnDagNode(charPath)
    deformObj = None
    for i in range(dagFn.childCount()):
        nextChildName = om2.MFnDependencyNode(dagFn.child(i)).name()
        if nextChildName == "deform_hrc":
            deformObj = om2.MSelectionList().add("%s|deform_hrc" % charPath.fullPathName()).getDependNode(0)
            break
    if deformObj is None:
        raise RuntimeError("The specified char name is not a char or don't exists.")
    cmpntObj = om2.MFnDagNode().create("transform", "%s_cmpnt" % name, deformObj)
    om2.MFnDagNode().create("transform", "%s_ioConnections_srt" % name, cmpntObj)
    om2.MFnDagNode().create("transform", "%s_joints_hrc" % name, cmpntObj)
    om2.MFnDagNode().create("transform", "%s_controls_hrc" % name, cmpntObj)
    om2.MFnDagNode().create("transform", "%s_ikHandles_hrc" % name, cmpntObj)
    om2.MFnDagNode().create("transform", "%s_misc_hrc" % name, cmpntObj)
    sel = om2.MSelectionList().add(om2.MFnDependencyNode(cmpntObj).name())
    cmpntPath = sel.getDagPath(0)
    om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectObjectMode)
    om2.MGlobal.setActiveSelectionList(sel)
    return cmpntPath

class AttributeTypes(object):
    """Enum of attribute types.

    This can be used to create an attribute with createAttribute() function. Constant types are:
    kInt, kFloat, kDouble, kShort, kLong, kBool, kAngle, kDistance, kTime, kFloatMatrix, kDoubleMatrix,
    kString, kMesh, kNurbsCurve, kNurbsSurface and kEnum.
    """
    kInt = 0
    kFloat = 1
    kDouble = 2
    kShort = 3
    kLong = 4
    kBool = 5
    kAngle = 6
    kDistance = 7
    kTime = 8
    kFloatMatrix = 9
    kDoubleMatrix = 10
    kString = 11
    kMesh = 12
    kNurbsCurve = 13
    kNurbsSurface = 14
    kEnum = 15

def createAttribute(longName, shortName, attrType, length=1,
                    minVal=None, maxVal=None, default=None, keyable=True, enum=None):
    """Create custom attribute types in selected objects.

    Args:
        longName (string): The longName of the attribute about to be created.
        shortName (string): The short name of the attribute about to be created.
        attrType ({AttributeTypes} Type constant): The type of the attribute.
        length (int: 1 [Optional]): The number of childs, used to create vector types.
        minVal (list: None [Optional]): The minimum value of the attribute.
        maxVal (list: None [Optional]): The maximum value of the attribute.
        default (list: None [Optional]): The default value of the attribute.
        keyable (bool: True [Optional]): Create as keyable attribute.
        enum (dict: None [Optional]): Create an enum attr with a dict key as name and dick value as index.

    Returns:
        True: If succeed.

    Raises:
        ValueError: If the attribute type is not a `AttributeTypes` class constant.
        KeyError: If the attribute type is kEnum and `enum` attribute was not specified.
    """
    sel = om2.MGlobal.getActiveSelectionList()
    for i in range(sel.length()):
        currentNode = om2.MFnDependencyNode(sel.getDependNode(i))
        attr = om2.MObject()
        attrFn = None
        attrFnVec = None
        attrData = None

        if attrType >= 0 and attrType <= 5:
            attrFn = om2.MFnNumericAttribute()
            attrFnVec = om2.MFnNumericAttribute()
            if attrType == 0:
                attrData = om2.MFnNumericData.kInt
            elif attrType == 1:
                attrData = om2.MFnNumericData.kFloat
            elif attrType == 2:
                attrData = om2.MFnNumericData.kDouble
            elif attrType == 3:
                attrData = om2.MFnNumericData.kShort
            elif attrType == 4:
                attrData = om2.MFnNumericData.kLong
            elif attrType == 5:
                attrData = om2.MFnNumericData.kBoolean
        elif attrType >= 6 and attrType <= 8:
            attrFn = om2.MFnUnitAttribute()
            attrFnVec = om2.MFnNumericAttribute()
            if attrType == 6:
                attrData = om2.MFnUnitAttribute.kAngle
            elif attrType == 7:
                attrData = om2.MFnUnitAttribute.kDistance
            elif attrType == 8:
                attrData = om2.MFnUnitAttribute.kTime
        elif attrType >= 9 and attrType <= 10:
            attrFn = om2.MFnMatrixAttribute()
            attrFnVec = om2.MFnNumericAttribute()
            if attrType == 9:
                attrData = om2.MFnMatrixAttribute.kFloat
            elif attrType == 10:
                attrData = om2.MFnMatrixAttribute.kDouble
        elif attrType >= 11 and attrType <= 14:
            attrFn = om2.MFnTypedAttribute()
            attrFnVec = om2.MFnNumericAttribute()
            if attrType == 11:
                attrData = om2.MFnData.kString
            elif attrType == 12:
                attrData = om2.MFnData.kMesh
            elif attrType == 13:
                attrData = om2.MFnData.kNurbsCurve
            elif attrType == 14:
                attrData = om2.MFnData.kNurbsSurface
        elif attrType == 15:
            attrFn = om2.MFnEnumAttribute()
        else:
            raise ValueError("Attribute type must be a AttributeTypes class constant.")

        if length == 1:
            if attrType == 15:
                if enum is not None:
                    attr = attrFn.create(longName, shortName)
                    sortedEnums = sorted(enum.items(), key=lambda x: x[1])
                    for field in sortedEnums:
                        attrFn.addField(field[0], field[1])
                    attrFn.default = min(enum.values())
                else:
                    raise KeyError("Attribute `enum` have to be specified to create a Enum Attribute.")
            else:
                attr = attrFn.create(longName, shortName, attrData)
                if default is not None:
                    attrFn.default = default[0:1]
                if minVal is not None:
                    attrFn.setMin(minVal[0:1])
                if maxVal is not None:
                    attrFn.setMax(maxVal[0:1])
            if keyable:
                attrFn.keyable = True
            else:
                attrFn.keyable = False
            attrFn.writable = True
            attrFn.readable = True
            attrFn.storable = True
            currentNode.addAttribute(attr)
        elif length == 2:
            if attrType == 15:
                attrFnVec = attrFn
                if enum is not None:
                    attr = attrFnVec.create(longName, shortName)
                    sortedEnums = sorted(enum, key=lambda x: x[1])
                    for enum in sortedEnums:
                        attrFnVec.addField(enum[0], enum[1])
                else:
                    raise KeyError("Attribute `enum` have to be specified to create a Enum Attribute.")
            else:
                attrX = attrFn.create("%sX" % longName, "%sx" % shortName, attrData)
                attrY = attrFn.create("%sY" % longName, "%sy" % shortName, attrData)
                attr = attrFnVec.create(longName, shortName, attrX, attrY)
                if default is not None:
                    attrFnVec.default = default[0:2]
                if minVal is not None:
                    attrFnVec.setMin(minVal[0:2])
                if maxVal is not None:
                    attrFnVec.setMax(maxVal[0:2])
            if keyable:
                attrFnVec.keyable = True
            else:
                attrFnVec.keyable = False
            attrFnVec.writable = True
            attrFnVec.readable = True
            attrFnVec.storable = True
            currentNode.addAttribute(attr)
        elif length == 3:
            if attrType == 15:
                attrFnVec = attrFn
                if enum is not None:
                    attr = attrFnVec.create(longName, shortName)
                    sortedEnums = sorted(enum, key=lambda x: x[1])
                    for enum in sortedEnums:
                        attrFnVec.addField(enum[0], enum[1])
                else:
                    raise KeyError("Attribute `enum` have to be specified to create a Enum Attribute.")
            else:
                attrX = attrFn.create("%sX" % longName, "%sx" % shortName, attrData)
                attrY = attrFn.create("%sY" % longName, "%sy" % shortName, attrData)
                attrZ = attrFn.create("%sZ" % longName, "%sz" % shortName, attrData)
                attr = attrFnVec.create(longName, shortName, attrX, attrY, attrZ)
                if default is not None:
                    attrFnVec.default = default[0:3]
                if minVal is not None:
                    attrFnVec.setMin(minVal[0:3])
                if maxVal is not None:
                    attrFnVec.setMax(maxVal[0:3])
            if keyable:
                attrFnVec.keyable = True
            else:
                attrFnVec.keyable = False
            attrFnVec.writable = True
            attrFnVec.readable = True
            attrFnVec.storable = True
            currentNode.addAttribute(attr)
    return True

def unfreezeTransformations():
    """Unfreeze selected objects translation.

    Returns:
        True: If succeed.
    """
    sel = om2.MGlobal.getActiveSelectionList()
    for s in range(sel.length()):
        obj = sel.getDagPath(s)
        fnTrans = om2.MFnTransform(obj)
        rp = fnTrans.rotatePivot(om2.MSpace.kWorld)
        vPos = om2.MVector(rp.x, rp.y, rp.z)
        fnTrans.translateBy(-vPos, om2.MSpace.kWorld)
        cmds.makeIdentity(a=True, t=True, r=True, s=True, n=False, pn=True)
        fnTrans.translateBy(vPos, om2.MSpace.kWorld)
    return True

def mirrorControlShape(xAxis=True, yAxis=True, zAxis=True):
    """Mirror control shapes selected.

    Args:
        xAxis (bool: True [Optional]): Apply on the X Axis.
        yAxis (bool: True [Optional]): Apply on the Y Axis.
        zAxis (bool: True [Optional]): Apply on the Z Axis.

    Returns:
        True: If succeed.

    Raises:
        RuntimeError: If nothing is selected.
        TypeError: If control attribute is not a kNurbsCurve.
    """
    sel = om2.MGlobal.getActiveSelectionList()
    if sel.length() < 1:
        raise RuntimeError("Must select at least one object.")
    shapeObjPath = None
    for s in range(sel.length()):
        transformObjPath = sel.getDagPath(s)
        dagFn = om2.MFnDagNode(transformObjPath)
        for i in range(dagFn.childCount()):
            nextChild = dagFn.child(i)
            if nextChild.apiType() == om2.MFn.kNurbsCurve:
                shapeObj = nextChild
                shapeName = om2.MFnDependencyNode(shapeObj).name()
                shapeObjPath = om2.MSelectionList().add(shapeName).getDagPath(0)
                break
        if shapeObjPath is None:
            raise TypeError("The selection must be a Nurbs Curve.")
        curveFn = om2.MFnNurbsCurve(shapeObjPath)
        for i in range(curveFn.numSpans):
            cvPoint = curveFn.cvPosition(i)
            vCvPos = om2.MVector(cvPoint.x, cvPoint.y, cvPoint.z)
            xVal = -vCvPos.x if xAxis else vCvPos.x
            yVal = -vCvPos.y if yAxis else vCvPos.y
            zVal = -vCvPos.z if zAxis else vCvPos.z
            cvPointMir = om2.MPoint(xVal, yVal, zVal)
            curveFn.setCVPosition(i, cvPointMir)
            curveFn.updateCurve()
    return True

def createObject(objType, name=None):
    """Create object of specific type.

    Args:
        objType (string): The type of the object.
        name (string: None [Optional]): The name of the object.

    Returns:
        string: The name of the new object created.
    """
    nodeFn = om2.MFnDependencyNode()
    obj = nodeFn.create(objType, name)
    try:
        dagFn = om2.MFnDagNode(obj)
        name = dagFn.fullPathName()
    except RuntimeError:
        nodeFn.setObject(obj)
        name = nodeFn.name()
    sel = om2.MSelectionList().add(name)
    om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectObjectMode)
    om2.MGlobal.setActiveSelectionList(sel, om2.MGlobal.kReplaceList)
    return name

def createObjectOnTransform(objType="transform", namePreffix=None):
    """Create objects in top of selected objects.

    Args:
        objType (string: "transform" [Optional]): The type of the object.
        namePreffix (string: None [Optional]): The name preffix of the objects about to be created.

    Returns:
        list: The list of the created objects names.

    Raises:
        TypeError: If the objType is not a DagNode or don't exists.
    """
    sel = om2.MGlobal.getActiveSelectionList()
    dagFn = om2.MFnDagNode()
    parentObj = dagFn.create("transform", namePreffix)
    dagFn.setObject(parentObj)
    parentObjName = dagFn.fullPathName()
    try:
        for i in range(sel.length()):
            obj = sel.getDagPath(i)
            transFn = om2.MFnTransform(obj)
            objTrans = transFn.translation(om2.MSpace.kWorld)
            objRot = transFn.rotation(om2.MSpace.kWorld, asQuaternion=True)
            if namePreffix is not None:
                newObj = dagFn.create(objType, "%s%s" % (namePreffix, i+1), parentObj)
            else:
                newObj = dagFn.create(objType, namePreffix, parentObj)
            transFn.setObject(newObj)
            transFn.translateBy(objTrans, om2.MSpace.kTransform)
            transFn.rotateBy(objRot, om2.MSpace.kTransform)
    except RuntimeError:
        cmds.delete(parentObjName)
        raise TypeError("The object type is not a DagNode or don't exists.")
    sel = om2.MSelectionList().add(parentObj)
    om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectObjectMode)
    om2.MGlobal.setActiveSelectionList(sel)
    return parentObjName

def getPoleVectorPosition(distance=0.0):
    """Find the right pole vector position based on selection.

    Create an transform object in the right position. To use this command select 3 dag nodes in the scene.
    (More than 3 object will be ignored).

    Args:
        distance (float: 0.0 [Optional]): The distance between the joint chain and the pole vector position.

    Returns:
        string: The path of the transform object created on position.

    Raises:
        RuntimeError: When the selection list is less than 3.
        ValueError: When the distance is not a float value.
    """
    sel = om2.MGlobal.getActiveSelectionList()
    if sel.length() >= 3:
        transFn = om2.MFnTransform(sel.getDagPath(0))
        vStart = transFn.translation(om2.MSpace.kWorld)
        transFn.setObject(sel.getDagPath(1))
        vMid = transFn.translation(om2.MSpace.kWorld)
        transFn.setObject(sel.getDagPath(2))
        vEnd = transFn.translation(om2.MSpace.kWorld)
        vStartEnd = vEnd - vStart
        vStartMid = vMid - vStart
        dotP = vStartMid * vStartEnd
        proj = dotP / vStartEnd.length()
        nStartEnd = vStartEnd.normal()
        vProj = nStartEnd * proj
        vArrow = vStartMid - vProj
        vArrow *= 0.0
        vFinal = vArrow + vMid
        vCross1 = vStartEnd ^ vStartMid
        vCross1.normalize()
        vCross2 = vCross1 ^ vArrow
        vCross2.normalize()
        vArrow.normalize()
        matrix = [
            vArrow.x, vArrow.y, vArrow.z, 0.0,
            vCross1.x, vCross1.y, vCross1.z, 0.0,
            vCross2.x, vCross2.y, vCross2.z, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ]
        mMtx = om2.MMatrix(matrix)
        mtxFn = om2.MTransformationMatrix(mMtx)
        quat = mtxFn.rotation(asQuaternion=True)
        nodeFn = om2.MFnDependencyNode()
        posObj = nodeFn.create("transform")
        nodeFn.setObject(posObj)
        posObjPath = om2.MSelectionList().add(nodeFn.name()).getDagPath(0)
        transFn.setObject(posObjPath)
        try:
            vFinal += om2.MVector(distance, 0.0, 0.0)
        except ValueError:
            cmds.delete(posObjPath.fullPathName())
            raise ValueError("Distance argument must be a float type.")
        transFn.translateBy(vFinal, om2.MSpace.kTransform)
        transFn.rotateBy(quat, om2.MSpace.kTransform)
        objSel = om2.MSelectionList().add(posObjPath)
        om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectObjectMode)
        om2.MGlobal.setActiveSelectionList(objSel)
        return posObjPath.fullPathName()
    else:
        raise RuntimeError("Selection list is less than 3. Select at least 3 objects.")
