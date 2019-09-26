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
import math
import maya.cmds as cmds
import maya.api._OpenMaya_py2 as om2


kCharOutlinerColor = om2.MColor([0.988, 0.961, 0.392])


def connectAttr(startAttr, endAttr):
    """Connect attributes from two nodes.

    Args:
        startAttr (string): The name of the output plug attribute.
        endAttr (string): The name of the input plug attribute.

    Returns:
        True: If succeed.

    Raises:
        TypeError: If the objects passed is not a dag node.
    """
    startNodeName = startAttr.split(".")[0]
    startAttrName = startAttr.split(".")[1]
    endNodeName = endAttr.split(".")[0]
    endAttrName = endAttr.split(".")[1]
    startObj = om2.MSelectionList().add(startNodeName).getDependNode(0)
    endObj = om2.MSelectionList().add(endNodeName).getDependNode(0)
    if not startObj.hasFn(om2.MFn.kDagNode) or not endObj.hasFn(om2.MFn.kDagNode):
        raise TypeError("Objects must be a dag node.")
    dagFn = om2.MFnDagNode(startObj)
    startPlug = dagFn.findPlug(startAttrName, False)
    dagFn.setObject(endObj)
    endPlug = dagFn.findPlug(endAttrName, False)
    mdgmod = om2.MDGModifier()
    mdgmod.connect(startPlug, endPlug)
    mdgmod.doIt()
    return True

def createChar(name):
    """Create a character node hierarchy.

    Args:
        name (string): The name of the character node.

    Returns:
        string: The Dag Path of the char node.
    """
    charObj = om2.MFnDagNode().create("unknownTransform", "%s_char" % name)
    om2.MFnDagNode().create("unknownTransform", "deform_hrc", charObj)
    om2.MFnDagNode().create("unknownTransform", "geometry_hrc", charObj)
    nodeFn = om2.MFnDependencyNode(charObj)
    plug = nodeFn.findPlug("useOutlinerColor", True)
    plug.setBool(True)
    plug = nodeFn.findPlug("outlinerColor", True)
    dataHandle = plug.asMDataHandle()
    dataHandle.set3Float(kCharOutlinerColor.r, kCharOutlinerColor.g, kCharOutlinerColor.b)
    plug.setMDataHandle(dataHandle)
    om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectObjectMode)
    selList = om2.MSelectionList().add(charObj)
    om2.MGlobal.setActiveSelectionList(selList)
    createMessageAttribute("components", "components")
    createMessageAttribute("APICharacter", "APICharacter")
    sel = om2.MSelectionList().add(nodeFn.name())
    charPath = sel.getDagPath(0)
    om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectObjectMode)
    om2.MGlobal.setActiveSelectionList(sel)
    return charPath.fullPathName()

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
    charName = char if "_char" in char else "".join([char, "_char"])
    charObj = om2.MSelectionList().add(charName).getDependNode(0)
    nodeFn = om2.MFnDependencyNode(charObj)
    if not charObj.hasFn(om2.MFn.kDagNode) or not nodeFn.hasAttribute("APICharacter"):
        raise RuntimeError("The specified char name is not a char or don't exists.")
    om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectObjectMode)
    charPath = om2.MDagPath().getAPathTo(charObj)
    deformObj = charPath.child(0)
    cmpntObj = om2.MFnDagNode().create("unknownTransform", "%s_cmpnt" % name, deformObj)
    cmpntPath = om2.MDagPath().getAPathTo(cmpntObj)
    ioConnObj = om2.MFnDagNode().create("unknownTransform", "%s_ioConnections_srt" % name, cmpntObj)
    ioConnPath = om2.MDagPath().getAPathTo(ioConnObj)
    om2.MFnDagNode().create("unknownTransform", "%s_joints_hrc" % name, cmpntObj)
    om2.MFnDagNode().create("unknownTransform", "%s_controls_hrc" % name, cmpntObj)
    om2.MFnDagNode().create("unknownTransform", "%s_ikHandles_hrc" % name, cmpntObj)
    om2.MFnDagNode().create("unknownTransform", "%s_misc_hrc" % name, cmpntObj)
    charComponentsAttr = "%s.components" % charPath.fullPathName()
    selList = om2.MSelectionList().add(cmpntObj)
    om2.MGlobal.setActiveSelectionList(selList)
    createMessageAttribute("character", "character")
    createMessageAttribute("joints", "joints")
    createMessageAttribute("controls", "controls")
    createMessageAttribute("ikHandles", "ikHandles")
    createMessageAttribute("ioConn", "ioConn")
    cmpntCharacterAttr = "%s.character" % cmpntPath.fullPathName()
    cmpntIoAttr = "%s.ioConn" % cmpntPath.fullPathName()
    selList = om2.MSelectionList().add(ioConnObj)
    om2.MGlobal.setActiveSelectionList(selList)
    createMessageAttribute("component", "component")
    createNumericAttribute("displayJoints", "displayJoints", AttributeTypes.kBool)
    createNumericAttribute("displayControls", "displayControls", AttributeTypes.kBool)
    ioComponentAttr = "%s.component" % ioConnPath.fullPathName()
    connectAttr(charComponentsAttr, cmpntCharacterAttr)
    connectAttr(cmpntIoAttr, ioComponentAttr)
    sel = om2.MSelectionList().add(cmpntObj)
    om2.MGlobal.setActiveSelectionList(sel)
    return cmpntPath.fullPathName()

class AttributeTypes(object):
    """Enum of attribute types.

    This can be used to create an attribute with createAttribute() function.

    Constant types are:
    kInt, kFloat, kDouble, kShort, kLong, kBool, kAngle, kDistance, kTime, kFloatMatrix, kDoubleMatrix,
    kString, kMesh, kNurbsCurve, kNurbsSurface, kLattice, kIntArray, kDoubleArray, kPointArray,
    kVectorArray and kStringArray.
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
    kLattice = 15
    kIntArray = 16
    kDoubleArray = 17
    kPointArray = 18
    kVectorArray = 19
    kStringArray = 20

def createNumericAttribute(longName, shortName, attrType, minVal=None, maxVal=None, default=0,
                           writable=True, readable=True, keyable=True, storable=True, channelBox=False):
    """Create a custom numeric attribute in selected objects.

    Args:
        longName (string): The long name of the attribute about to be created.
        shortName (string): The short name of the attribute about to be created.
        attrType ({AttributeTypes} Type constant): The type of the attribute.
        minVal (float: None [Optional]): The minimum value of the attribute.
        maxVal (float: None [Optional]): The maximum value of the attribute.
        default (float: 0 [Optional]): The default value of the attribute.
        writable (bool: True [Optional]): Create as writable attribute.
        readable (bool: True [Optional]): Create as readable attribute.
        keyable (bool: True [Optional]): Create as keyable attribute.
        storable (bool: True [Optional]): Create as storable attribute.
        channelBox (bool: False [Optional]): Create as channelBox attribute.

    Returns:
        list: The names of the attributes created.

    Raises:
        TypeError: If the attrType is not a numeric type.
    """
    selList = om2.MGlobal.getActiveSelectionList()
    if selList.length() < 1:
        return None
    if attrType < 0 or attrType > 5:
        raise TypeError("Argument attrType must be a numeric type.")
    if attrType == 0:
        data = om2.MFnNumericData.kInt
    elif attrType == 1:
        data = om2.MFnNumericData.kFloat
    elif attrType == 2:
        data = om2.MFnNumericData.kDouble
    elif attrType == 3:
        data = om2.MFnNumericData.kShort
    elif attrType == 4:
        data = om2.MFnNumericData.kLong
    else:
        data = om2.MFnNumericData.kBoolean
    objectNames = []
    for i in range(selList.length()):
        curObj = selList.getDependNode(i)
        nodeFn = om2.MFnDependencyNode(curObj)
        objectNames.append("%s.%s" % (nodeFn.name(), longName))
        attrFn = om2.MFnNumericAttribute()
        attr = attrFn.create(longName, shortName, data, default)
        attrFn.writable = writable
        attrFn.readable = readable
        attrFn.keyable = keyable
        attrFn.storable = storable
        attrFn.channelBox = channelBox
        if minVal is not None:
            attrFn.setMin(minVal)
        if maxVal is not None:
            attrFn.setMax(maxVal)
        nodeFn.addAttribute(attr)
    return objectNames

def createUnitAttribute(longName, shortName, attrType, minVal=None, maxVal=None, default=0,
                        writable=True, readable=True, keyable=True, storable=True, channelBox=False):
    """Create custom unit attribute in selected objects.

    Args:
        longName (string): The long name of the attribute about to be created.
        shortName (string): The short name of the attribute about to be created.
        attrType ({AttributeTypes} Type constant): The type of the attribute.
        minVal (float: None [Optional]): The minimum value of the attribute.
        maxVal (float: None [Optional]): The maximum value of the attribute.
        default (float: 0 [Optional]): The default value of the attribute.
        writable (bool: True [Optional]): Create as writable attribute.
        readable (bool: True [Optional]): Create as readable attribute.
        keyable (bool: True [Optional]): Create as keyable attribute.
        storable (bool: True [Optional]): Create as storable attribute.
        channelBox (bool: False [Optional]): Create as channelBox attribute.

    Returns:
        list: The names of the attributes created.

    Raises:
        TypeError: If the attrType is not a unit type.
    """
    selList = om2.MGlobal.getActiveSelectionList()
    if selList.length() < 1:
        return None
    if attrType < 6 or attrType > 8:
        raise TypeError("Argument attrType must be a unit type.")
    if attrType == 6:
        data = om2.MFnUnitAttribute.kAngle
    elif attrType == 7:
        data = om2.MFnUnitAttribute.kDistance
    else:
        data = om2.MFnUnitAttribute.kTime
    objectNames = []
    for i in range(selList.length()):
        curObj = selList.getDependNode(i)
        nodeFn = om2.MFnDependencyNode(curObj)
        objectNames.append("%s.%s" % (nodeFn.name(), longName))
        attrFn = om2.MFnUnitAttribute()
        attr = attrFn.create(longName, shortName, data, default)
        attrFn.writable = writable
        attrFn.readable = readable
        attrFn.keyable = keyable
        attrFn.storable = storable
        attrFn.channelBox = channelBox
        if minVal is not None:
            attrFn.setMin(minVal)
        if maxVal is not None:
            attrFn.setMax(maxVal)
        nodeFn.addAttribute(attr)
    return objectNames

def createMatrixAttribute(longName, shortName, attrType, writable=True, readable=True,
                          keyable=True, storable=True, channelBox=False):
    """Create custom matrix attribute in selected objects.

    Args:
        longName (string): The long name of the attribute about to be created.
        shortName (string): The short name of the attribute about to be created.
        attrType ({AttributeTypes} Type constant): The type of the attribute.
        writable (bool: True [Optional]): Create as writable attribute.
        readable (bool: True [Optional]): Create as readable attribute.
        keyable (bool: True [Optional]): Create as keyable attribute.
        storable (bool: True [Optional]): Create as storable attribute.
        channelBox (bool: False [Optional]): Create as channelBox attribute.

    Returns:
        list: The names of the attributes created.

    Raises:
        TypeError: If the attrType is not a matrix type.
    """
    selList = om2.MGlobal.getActiveSelectionList()
    if selList.length() < 1:
        return None
    if attrType < 9 or attrType > 10:
        raise TypeError("Argument attrType must be a matrix type.")
    if attrType == 9:
        data = om2.MFnMatrixAttribute.kFloat
    else:
        data = om2.MFnMatrixAttribute.kDouble
    objectNames = []
    for i in range(selList.length()):
        curObj = selList.getDependNode(i)
        nodeFn = om2.MFnDependencyNode(curObj)
        objectNames.append("%s.%s" % (nodeFn.name(), longName))
        attrFn = om2.MFnMatrixAttribute()
        attr = attrFn.create(longName, shortName, data)
        attrFn.writable = writable
        attrFn.readable = readable
        attrFn.keyable = keyable
        attrFn.storable = storable
        attrFn.channelBox = channelBox
        nodeFn.addAttribute(attr)
    return objectNames

def createTypedAttribute(longName, shortName, attrType, writable=True, readable=True,
                         keyable=True, storable=True, channelBox=False):
    """Create custom typed  attribute in selected objects.

    Args:
        longName (string): The long name of the attribute about to be created.
        shortName (string): The short name of the attribute about to be created.
        attrType ({AttributeTypes} Type constant): The type of the attribute.
        writable (bool: True [Optional]): Create as writable attribute.
        readable (bool: True [Optional]): Create as readable attribute.
        keyable (bool: True [Optional]): Create as keyable attribute.
        storable (bool: True [Optional]): Create as storable attribute.
        channelBox (bool: False [Optional]): Create as channelBox attribute.

    Returns:
        list: The names of the attributes created.

    Raises:
        TypeError: If the attrType is not a typed type.
    """
    selList = om2.MGlobal.getActiveSelectionList()
    if selList.length() < 1:
        return None
    if attrType < 11 or attrType > 20:
        raise TypeError("Argument attrType must be a typed type.")
    if attrType == 11:
        data = om2.MFnData.kString
    elif attrType == 12:
        data = om2.MFnData.kMesh
    elif attrType == 13:
        data = om2.MFnData.kNurbsCurve
    elif attrType == 14:
        data = om2.MFnData.kNurbsSurface
    elif attrType == 15:
        data = om2.MFnData.kLattice
    elif attrType == 16:
        data = om2.MFnData.kIntArray
    elif attrType == 17:
        data = om2.MFnData.kDoubleArray
    elif attrType == 18:
        data = om2.MFnData.kPointArray
    elif attrType == 19:
        data = om2.MFnData.kVectorArray
    elif attrType == 20:
        data = om2.MFnData.kStringArray
    objectNames = []
    for i in range(selList.length()):
        curObj = selList.getDependNode(i)
        nodeFn = om2.MFnDependencyNode(curObj)
        objectNames.append("%s.%s" % (nodeFn.name(), longName))
        attrFn = om2.MFnTypedAttribute()
        attr = attrFn.create(longName, shortName, data)
        attrFn.writable = writable
        attrFn.readable = readable
        attrFn.keyable = keyable
        attrFn.storable = storable
        attrFn.channelBox = channelBox
        nodeFn.addAttribute(attr)
    return objectNames

def createEnumAttribute(longName, shortName, enum, writable=True, readable=True,
                        keyable=True, storable=True, channelBox=False):
    """Create custom enum attribute in selected objects.

    Args:
        longName (string): The long name of the attribute about to be created.
        shortName (string): The short name of the attribute about to be created.
        enum (dict): Create an enum attr with a dict key as name and dict value as index.
        writable (bool: True [Optional]): Create as writable attribute.
        readable (bool: True [Optional]): Create as readable attribute.
        keyable (bool: True [Optional]): Create as keyable attribute.
        storable (bool: True [Optional]): Create as storable attribute.
        channelBox (bool: False [Optional]): Create as channelBox attribute.

    Returns:
        list: The names of the attributes created.

    Raises:
        RuntimeError: If the enum argument is not a dict or its empty.
    """
    selList = om2.MGlobal.getActiveSelectionList()
    if selList.length() < 1:
        return None
    if not isinstance(enum, dict) or not bool(enum):
        raise RuntimeError("Argument enum must be a filled dict.")
    objectNames = []
    for i in range(selList.length()):
        curObj = selList.getDependNode(i)
        nodeFn = om2.MFnDependencyNode(curObj)
        objectNames.append("%s.%s" % (nodeFn.name(), longName))
        attrFn = om2.MFnEnumAttribute()
        attr = attrFn.create(longName, shortName)
        sortedEnums = sorted(enum.items(), key=lambda x: x[1])
        for field in sortedEnums:
            attrFn.addField(field[0], field[1])
        attrFn.default = min(enum.values())
        attrFn.writable = writable
        attrFn.readable = readable
        attrFn.keyable = keyable
        attrFn.storable = storable
        attrFn.channelBox = channelBox
        nodeFn.addAttribute(attr)
    return objectNames

def createMessageAttribute(longName, shortName, writable=True, readable=True,
                           keyable=True, storable=True, channelBox=False):
    """Create custom message attribute in selected objects.

    Args:
        longName (string): The long name of the attribute about to be created.
        shortName (string): The short name of the attribute about to be created.
        writable (bool: True [Optional]): Create as writable attribute.
        readable (bool: True [Optional]): Create as readable attribute.
        keyable (bool: True [Optional]): Create as keyable attribute.
        storable (bool: True [Optional]): Create as storable attribute.
        channelBox (bool: False [Optional]): Create as channelBox attribute.

    Returns:
        list: The names of the attributes created.
    """
    selList = om2.MGlobal.getActiveSelectionList()
    if selList.length() < 1:
        return None
    objectNames = []
    for i in range(selList.length()):
        curObj = selList.getDependNode(i)
        nodeFn = om2.MFnDependencyNode(curObj)
        objectNames.append("%s.%s" % (nodeFn.name(), longName))
        attrFn = om2.MFnMessageAttribute()
        attr = attrFn.create(longName, shortName)
        attrFn.writable = writable
        attrFn.readable = readable
        attrFn.keyable = keyable
        attrFn.storable = storable
        attrFn.channelBox = channelBox
        nodeFn.addAttribute(attr)
    return objectNames

def createVectorAttribute(longName, shortName, attrType, length=3, writable=True,
                          readable=True, keyable=True, storable=True, channelBox=False):
    """Create a custom vector attribute in selected objects.

    Args:
        longName (string): The long name of the attribute about to be created.
        shortName (string): The short name of the attribute about to be created.
        attrType ({AttributeTypes} Type constant): The type of the attribute.
        length (int: 3 [Optional]): The length of the vector (must be 2 or 3).
        writable (bool: True [Optional]): Create as writable attribute.
        readable (bool: True [Optional]): Create as readable attribute.
        keyable (bool: True [Optional]): Create as keyable attribute.
        storable (bool: True [Optional]): Create as storable attribute.
        channelBox (bool: False [Optional]): Create as channelBox attribute.

    Returns:
        list: The names of the attributes created.

    Raises:
        IndexError: If the length argument is different than 2 and 3.
        TypeError: If the attrType argument is not a numeric type.
    """
    selList = om2.MGlobal.getActiveSelectionList()
    if selList.length() < 1:
        return None
    if length < 2 or length > 3:
        raise IndexError("Argument length must be 2 or 3")
    if attrType < 0 or attrType > 7 or attrType == 5:
        raise TypeError("Argument attrType must be a numeric type.")
    if attrType == 0:
        data = om2.MFnNumericData.kInt
    elif attrType == 1:
        data = om2.MFnNumericData.kFloat
    elif attrType == 2:
        data = om2.MFnNumericData.kDouble
    elif attrType == 3:
        data = om2.MFnNumericData.kShort
    elif attrType == 4:
        data = om2.MFnNumericData.kLong
    elif attrType == 6:
        data = om2.MFnUnitAttribute.kAngle
    elif attrType == 7:
        data = om2.MFnUnitAttribute.kDistance
    objectNames = []
    for i in range(selList.length()):
        curObj = selList.getDependNode(i)
        nodeFn = om2.MFnDependencyNode(curObj)
        objectNames.append("%s.%s" % (nodeFn.name(), longName))
        if attrType < 5:
            attrFn = om2.MFnNumericAttribute()
        else:
            attrFn = om2.MFnUnitAttribute()
        attrX = attrFn.create("%sX" % longName, "%sx" % shortName, data)
        attrY = attrFn.create("%sY" % longName, "%sy" % shortName, data)
        if length == 3:
            attrZ = attrFn.create("%sZ" % longName, "%sz" % shortName, data)
        attrFn = om2.MFnNumericAttribute()
        if length == 3:
            attr = attrFn.create(longName, shortName, attrX, attrY, attrZ)
        else:
            attr = attrFn.create(longName, shortName, attrX, attrY)
        attrFn.writable = writable
        attrFn.readable = readable
        attrFn.keyable = keyable
        attrFn.storable = storable
        attrFn.channelBox = channelBox
        nodeFn.addAttribute(attr)
    return objectNames

def createColorAttribute(longName, shortName, writable=True, readable=True, keyable=True,
                         storable=True, channelBox=False):
    """Create a custom color attribute in selected objects.

    Args:
        longName (string): The long name of the attribute about to be created.
        shortName (string): The short name of the attribute about to be created.
        writable (bool: True [Optional]): Create as writable attribute.
        readable (bool: True [Optional]): Create as readable attribute.
        keyable (bool: True [Optional]): Create as keyable attribute.
        storable (bool: True [Optional]): Create as storable attribute.
        channelBox (bool: False [Optional]): Create as channelBox attribute.

    Returns:
        list: The names of the attributes created.
    """
    selList = om2.MGlobal.getActiveSelectionList()
    if selList.length() < 1:
        return None
    objectNames = []
    for i in range(selList.length()):
        curObj = selList.getDependNode(i)
        nodeFn = om2.MFnDependencyNode(curObj)
        objectNames.append("%s.%s" % (nodeFn.name(), longName))
        attrFn = om2.MFnNumericAttribute()
        attr = attrFn.createColor(longName, shortName)
        attrFn.writable = writable
        attrFn.readable = readable
        attrFn.keyable = keyable
        attrFn.storable = storable
        attrFn.channelBox = channelBox
        nodeFn.addAttribute(attr)
    return objectNames

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
                shapeObjPath = om2.MDagPath().getAPathTo(shapeObj)
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
    if obj.hasFn(om2.MFn.kDagNode):
        dagFn = om2.MFnDagNode(obj)
        name = dagFn.fullPathName()
    else:
        nodeFn.setObject(obj)
        name = nodeFn.name()
    sel = om2.MSelectionList().add(name)
    om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectObjectMode)
    om2.MGlobal.setActiveSelectionList(sel)
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
    objsList = []
    for i in range(sel.length()):
        obj = sel.getDependNode(i)
        if not obj.hasFn(om2.MFn.kDagNode):
            objName = om2.MFnDependencyNode(obj).name()
            raise TypeError("The object %s is not a dag node or don't exists." % objName)
        objPath = om2.MDagPath().getAPathTo(obj)
        transFn = om2.MFnTransform(objPath)
        objTrans = transFn.translation(om2.MSpace.kWorld)
        objRot = transFn.rotation(om2.MSpace.kWorld, asQuaternion=True)
        if namePreffix is not None:
            newObj = dagFn.create(objType, "%s%s" % (namePreffix, i+1))
        else:
            newObj = dagFn.create(objType, namePreffix)
        transFn.setObject(newObj)
        transFn.translateBy(objTrans, om2.MSpace.kTransform)
        transFn.rotateBy(objRot, om2.MSpace.kTransform)
        objsList.append(om2.MFnDependencyNode(newObj).name())
    selList = om2.MSelectionList().add(newObj)
    om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectObjectMode)
    om2.MGlobal.setActiveSelectionList(selList)
    return objsList

def getPoleVectorPosition(distance=1.0):
    """Find the right pole vector position based on selection.

    Create an transform object in the right position. To use this command select 3 dag nodes in the scene.
    (More than 3 object will be ignored).

    Args:
        distance (float: 1.0 [Optional]): The distance multiplier between the joint chain and the pole vector position.

    Returns:
        string: The path of the transform object created on position.

    Raises:
        RuntimeError: When the selection list is less than 3.
        ValueError: When the distance is not a float value.
    """
    sel = om2.MGlobal.getActiveSelectionList()
    if not isinstance(distance, float):
        raise ValueError("Distance argument must be a float type.")
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
        vArrow *= distance
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
        transFn.translateBy(vFinal, om2.MSpace.kTransform)
        transFn.rotateBy(quat, om2.MSpace.kTransform)
        objSel = om2.MSelectionList().add(posObjPath)
        om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectObjectMode)
        om2.MGlobal.setActiveSelectionList(objSel)
        return posObjPath.fullPathName()
    else:
        raise RuntimeError("Selection list is less than 3. Select at least 3 objects.")

def findPreferredAngleIK():
    """Find preferred angle for the gfRigIKVChain node.

    Select the root joint, handle Joint and the pole vector control and run the command.

    Args:

    Returns:
        float: The angle of the rotation between pole vector and world x axis.

    Raises:
    """
    sel = om2.MGlobal.getActiveSelectionList()
    rootJntPath = sel.getDagPath(0)
    handleJntPath = sel.getDagPath(1)
    pvPath = sel.getDagPath(2)
    transFn = om2.MFnTransform(rootJntPath)
    vRoot = transFn.translation(om2.MSpace.kWorld)
    transFn.setObject(handleJntPath)
    vHandle = transFn.translation(om2.MSpace.kWorld)
    transFn.setObject(pvPath)
    vUpVector = transFn.translation(om2.MSpace.kWorld)

    nXAxis = vHandle - vRoot
    nXAxis.normalize()
    vUpDirection = vUpVector - vRoot
    nYAxis = vUpDirection - ((vUpDirection * nXAxis) * nXAxis)
    nYAxis.normalize()
    nWXAxis = om2.MVector(1.0, 0.0, 0.0)

    theta = math.acos(nWXAxis * nYAxis)
    return theta
