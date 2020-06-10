# -*- coding: utf-8 -*-
"""
Testing.

Todo:
    * TODO(createAttributeTypes): Add support to create Compounds.
    * TODO(addMetadataChar): Add metadata in char node create by createChar() and catch in createComponent().
    * TODO(addSelectionAddAttrs): Add selection list support to create attribute functions.

Source:
    * https://docs.python.org/2/extending/embedding.html
    * https://www.youtube.com/watch?v=P9edayG8rkg
"""
# pylint: disable=too-many-lines
import math
import maya.cmds as cmds
import maya.api._OpenMaya_py2 as om2


kCharOutlinerColor = om2.MColor([0.988, 0.961, 0.392])
kPrimaryControlColor = om2.MColor([1.0, 1.0, 1.0])
kSecondaryControlColor = om2.MColor([1.0, 1.0, 1.0])
kTertiaryControlColor = om2.MColor([1.0, 1.0, 1.0])
kQuaternaryControlColor = om2.MColor([1.0, 1.0, 1.0])
kGlobalControlColor = om2.MColor([1.0, 1.0, 1.0])


def copyCurveShape(source, target, maintainOffset=False, shapes=None):
    """Copy all shapes from source NURBS curve to another NURBS curve. [CONTROL TOOLS]

    Args:
        source (str): The name of the source NURBS Curve.
        target (str): The name of the target NURBS Curve.
        maintainOffset (bool: False [Optional]): Maintain offset position of CVs.
        shapes (list, MIntArray: None [Optional]): The list of indexes of the specific shapes to copy.
    
    Returns:
        True: If succeed.

    Raises:
       AttributeError: If source or target objects don't exist.
    TODO: Add the ability to act in the selection.
    """
    try:
        sourcePath = om2.MSelectionList().add(source).getDagPath(0)
    except RuntimeError:
        raise AttributeError("Object %s does not exist." % source)
    try:
        targetPath = om2.MSelectionList().add(target).getDagPath(0)
    except RuntimeError:
        raise AttributeError("Object %s does not exist." % target)
    if shapes is not None:
        assert isinstance(shapes, (list, om2.MIntArray))
        if isinstance(shapes, list):
            shapesIndices = om2.MIntArray()
            for i in range(len(shapes)):
                try:
                    shapesIndices.append(i)
                except TypeError:
                    om2.MGlobal.displayWarning("Shape index %s is invalid. Entry skipped." % i)
            shapes = shapesIndices

    dagFn = om2.MFnDagNode(sourcePath)
    childCount = dagFn.childCount()
    mSource = sourcePath.inclusiveMatrix()
    mTargetInv = targetPath.inclusiveMatrixInverse()

    if childCount:
        targetMob = targetPath.node()
        for i in range(childCount):
            if shapes is not None:
                if i not in shapes:
                    continue
            childMob = dagFn.child(i)
            if childMob.hasFn(om2.MFn.kNurbsCurve):
                shapePath = om2.MDagPath.getAPathTo(childMob)
                curveFn = om2.MFnNurbsCurve(childMob)
                if not maintainOffset:
                    cvsPos = curveFn.cvPositions()
                else:
                    cvsPos = om2.MPointArray()
                    for pnt in curveFn.cvPositions():
                        newPnt = (pnt * mSource) * mTargetInv
                        cvsPos.append(newPnt)
                knots = curveFn.knots()
                degree = curveFn.degree
                form = curveFn.form
                is2D = False
                rational = False
                shapeMob = om2.MFnNurbsCurve().create(cvsPos, knots, degree, form, is2D, rational, targetMob)
                dagMod = om2.MDagModifier()
                nameNumber = str(i + 1) if childCount > 1 else ""
                dagMod.renameNode(shapeMob, "%sShape%s" % (target, nameNumber))
                dagMod.doIt()

    return True


def mirrorCurveShape(across="YZ"):
    """Mirror curve nodes shapes selected withou mess with transform node.

    Args:
        across (str): The axis of the mirror. Can be "XY", "YZ" or "XZ".
    
    Returns:
        True: If succeed.

    Raises:
        RuntimeError: If nothing is selected.
        TypeError: If across argument is invalid.
        TypeError: If node selected is not a NURBS Curve.
    """
    selList = om2.MGlobal.getActiveSelectionList()
    if selList.length() < 1:
        raise RuntimeError("Must select at least one object.")
    if not isinstance(across, str):
        raise TypeError("Across parameter is invalid.")
    if across.upper() == "XY":
        eAcross = om2.MEulerRotation(0.0, 0.0, math.pi)
    elif across.upper() == "YZ":
        eAcross = om2.MEulerRotation(math.pi, 0.0, 0.0)
    elif across.upper() == "XZ":
        eAcross = om2.MEulerRotation(0.0, math.pi, 0.0)
    else:
        raise TypeError("Across parameter is invalid.")

    mtxFn = om2.MTransformationMatrix()
    mtxFn.setRotation(eAcross)
    mMirror = mtxFn.asMatrix()

    for i in range(selList.length()):
        curObjMob = selList.getDependNode(i)
        nodeFn = om2.MFnDependencyNode(curObjMob)
        if curObjMob.hasFn(om2.MFn.kDagNode):
            curObjPath = om2.MDagPath.getAPathTo(curObjMob)
            dagFn = om2.MFnDagNode(curObjPath)
            childCount = dagFn.childCount()
            if childCount:
                for j in range(childCount):
                    shapeMob = dagFn.child(j)
                    if shapeMob.hasFn(om2.MFn.kTransform):
                        continue
                    elif shapeMob.hasFn(om2.MFn.kNurbsCurve):
                        curveFn = om2.MFnNurbsCurve(shapeMob)
                        cvsPos = om2.MPointArray()
                        for pnt in curveFn.cvPositions():
                            finalPnt = pnt * mMirror
                            cvsPos.append(finalPnt)
                        curveFn.setCVPositions(cvsPos)
                        curveFn.updateCurve()
                    else:
                        raise TypeError("Object %s is not a NURBS Curve." % nodeFn.name())
            else:
                raise TypeError("Object %s is not a NURBS Curve." % nodeFn.name())
        else:
            raise TypeError("Object %s is not a NURBS Curve." % nodeFn.name())

    return True


def curveDistribution(curve, numObj, upVec=om2.MVector.kYaxisVector, objType="transform",
                      hierarchical=False, nonUniformSegments=False):
    """Non-uniform algorithm by distance between CVs.

    1- Select the curve and put in the MFnNurbsCurve to get all the info
    2- Get the number of CVs.
    3- Number of object per segment = numObj / numCVs
    4- Get the transformation matrix of the outputs. (Translation and Orientation).
    5- Put them in hierarchy in prompted.
    6- Put the result in a parent group if not.

    Args:
        curve (str, MObject or MDagPath): The base curve.
        (numCVs - 1) * numPerSegment

    Returns:
        True: If succeed.

    Raises:
        True.

    TODO: Connect inverse scale to joints. [parentScale to childInverseScale]
    """
    assert isinstance(curve, (str, om2.MObject, om2.MDagPath))
    if isinstance(curve, str):
        try:
            crvPath = om2.MSelectionList().add(curve).getDagPath(0)
        except:
            raise RuntimeError("Object %s is not valid or not exists." % curve)
        curve = crvPath

    curveFn = om2.MFnNurbsCurve(curve)
    transFn = om2.MFnTransform()
    dagFn = om2.MFnDagNode()
    lastObj = om2.MObject.kNullObj
    if nonUniformSegments:
        numCVs = curveFn.numCVs
        perSegment = numObj / (numCVs - 1)
        for i in range(numCVs):
            if i < numCVs - 1:
                curCVPos = curveFn.cvPosition(i, om2.MSpace.kWorld)
                nextCVPos = curveFn.cvPosition(i + 1, om2.MSpace.kWorld)
                param1 = curveFn.closestPoint(curCVPos, space=om2.MSpace.kWorld)[1]
                param2 = curveFn.closestPoint(nextCVPos, space=om2.MSpace.kWorld)[1]
                length1 = curveFn.findLengthFromParam(param1)
                length2 = curveFn.findLengthFromParam(param2)
                length = length2 - length1
                stepLength = length / perSegment
                for j in range(perSegment):
                    param = curveFn.findParamFromLength(stepLength * j + length1)
                    pos = curveFn.getPointAtParam(param)
                    nAim = curveFn.tangent(param, om2.MSpace.kWorld)
                    nAim.normalize()
                    nNormal = upVec - ((upVec * nAim) * nAim)
                    nNormal.normalize()
                    nBinormal = nAim ^ nNormal
                    nBinormal.normalize()
                    ori = [
                        nAim.x, nAim.y, nAim.z, 0.0,
                        nNormal.x, nNormal.y, nNormal.z, 0.0,
                        nBinormal.x, nBinormal.y, nBinormal.z, 0.0,
                        0.0, 0.0, 0.0, 1.0
                    ]
                    mOri = om2.MMatrix(ori)
                    mtxFn = om2.MTransformationMatrix(mOri)
                    qOri = mtxFn.rotation(asQuaternion=True)
                    obj = dagFn.create(objType, parent=lastObj)
                    objPath = om2.MDagPath.getAPathTo(obj)
                    transFn.setObject(objPath)
                    transFn.setTranslation(om2.MVector(pos), om2.MSpace.kWorld)
                    transFn.setRotation(qOri, om2.MSpace.kWorld)
                    if hierarchical:
                        lastObj = obj
            else:
                lastCVPos = curveFn.cvPosition(i, om2.MSpace.kWorld)
                pos, param = curveFn.closestPoint(lastCVPos, space=om2.MSpace.kWorld)
                nAim = curveFn.tangent(param, om2.MSpace.kWorld)
                nAim.normalize()
                nNormal = upVec - ((upVec * nAim) * nAim)
                nNormal.normalize()
                nBinormal = nAim ^ nNormal
                nBinormal.normalize()
                ori = [
                    nAim.x, nAim.y, nAim.z, 0.0,
                    nNormal.x, nNormal.y, nNormal.z, 0.0,
                    nBinormal.x, nBinormal.y, nBinormal.z, 0.0,
                    0.0, 0.0, 0.0, 1.0
                ]
                mOri = om2.MMatrix(ori)
                mtxFn = om2.MTransformationMatrix(mOri)
                qOri = mtxFn.rotation(asQuaternion=True)
                obj = dagFn.create(objType, parent=lastObj)
                objPath = om2.MDagPath.getAPathTo(obj)
                transFn.setObject(objPath)
                transFn.setTranslation(om2.MVector(pos), om2.MSpace.kWorld)
                transFn.setRotation(qOri, om2.MSpace.kWorld)
                if hierarchical:
                    lastObj = obj
    else:
        crvLength = curveFn.length()
        step = 1.0 / (numObj - 1.0) if numObj > 1 else 0.0
        for i in range(numObj):
            length = crvLength * step * i
            param = curveFn.findParamFromLength(length)
            pos = curveFn.getPointAtParam(param)
            nAim = curveFn.tangent(param, om2.MSpace.kWorld)
            nAim.normalize()
            nNormal = upVec - ((upVec * nAim) * nAim)
            nNormal.normalize()
            nBinormal = nAim ^ nNormal
            nBinormal.normalize()
            ori = [
                nAim.x, nAim.y, nAim.z, 0.0,
                nNormal.x, nNormal.y, nNormal.z, 0.0,
                nBinormal.x, nBinormal.y, nBinormal.z, 0.0,
                0.0, 0.0, 0.0, 1.0
            ]
            mOri = om2.MMatrix(ori)
            mtxFn = om2.MTransformationMatrix(mOri)
            qOri = mtxFn.rotation(asQuaternion=True)
            obj = dagFn.create(objType, parent=lastObj)
            objPath = om2.MDagPath.getAPathTo(obj)
            transFn.setObject(objPath)
            transFn.setTranslation(om2.MVector(pos), om2.MSpace.kWorld)
            transFn.setRotation(qOri, om2.MSpace.kWorld)
            if hierarchical:
                lastObj = obj

    return True


def createBezierCurve(ctrlPnts, returnData=False):
    """Create a Bezier curve with given control points.

    For N degree curve you must specify at least N+1 CVs to get a curve
    with a single span
    The number of knots required for a curve is M + 2N - 1 or N + CVS - 1.
    If you want the curve to start exactly at the first CV and end
    exactly at the last CV, then the knot vector must be structured
    to have degree N "multiplicity" at beggining and end. This means
    that the first N knots must be identical and the last N knots
    must be identical.
    Lines and polylines are usually degree 1, circles are degree 2,
    and most free-form curves are degree 3 or 5.
    Degree can be linear (1), quadratic (2), cubic (3) and quintic (5).
    The order of NURBS curve is a positive whole number equal to
    (degree+1)
    It is possible to increase the degree of a NURBS curve and not
    change its shape but is not possible to reduce.
    Control points are a list of at least degree + 1 points.
    The control points have an associated number called a weight.
    With a few exceptions, weights are positive numbers. When a curve's
    control points all have the same weight (usually 1), the curve is
    called non-rational, otherwise the curve is called rational.
    The knot numbers have to stay the same or get larger as you go down
    the list and to limit the number of duplicate values to no more
    than the degree.
    The number of times a knot values is duplicated is called the
    knot's multiplicity.
    Full multiplicity knot is the knot that appears degree times.
    Simple knot is the knot that appears one time.
    If a list of knots starts with a full multiplicity knot, is
    followed by simple knots, terminates with a full multiplicity knot,
    and the values are equally spaced, then the knots are called
    uniform. Otherwise is non-uniform.
    Duplicate knot values in the middle of the knot list make a NURBS
    curve less smooth. At the extreme, a full multiplicity knot in the
    middle of the knot list means there is a place on the NURBS curve
    that can be bent into a sharp kink. For this reason, some designers
    like to add and remove knots and then adjust control points to make
    curves have smoother of kinkier shapes.

    Args:
        ctrlPnts (MPointArray or list): The array position of the control points.
        returnData (bool: False [Optional]): Create as virtual MFnNurbsCurveData.

    Returns:
        MObject: The curve object or the curve data created.

    Raises:
        AttributeError: If the ctrlPnts argument is not a MPointArray or list.
    """
    assert isinstance(ctrlPnts, om2.MPointArray) or isinstance(ctrlPnts, list)
    if isinstance(ctrlPnts, list):
        for pnt in ctrlPnts:
            if (not isinstance(pnt, list) or
                    not isinstance(pnt, tuple)):
                raise AttributeError("CtrlPnts must be an MPointArray or list of 3D points.")
            else:
                if len(pnt) != 3:
                    raise AttributeError("CtrlPnt must be an MPointArray or list of 3D points.")
        ctrlPnts = om2.MPointArray(ctrlPnts)

    numCvs = len(ctrlPnts) # Degree + Spans
    degree = 3
    spans = numCvs - degree
    numKnots = spans + 2 * degree - 1
    knots = om2.MDoubleArray()
    curKnot = 1
    form = om2.MFnNurbsCurve.kOpen
    is2d = False
    rational = True
    for i in range(numKnots):
        if i + 1 <= degree:
            knots.append(0.0)
        elif i + 1 > numKnots - degree:
            knots.append(curKnot)
        else:
            knots.append(curKnot)
            curKnot += 1
    if returnData:
        curveData = om2.MFnNurbsCurveData().create()
        curveFn = om2.MFnNurbsCurve(curveData)
        curveFn.create(ctrlPnts, knots, degree, form, is2d, rational, curveData)
        resultMob = curveData
    else:
        curveFn = om2.MFnNurbsCurve()
        curveFn.create(ctrlPnts, knots, degree, form, is2d, rational)
        resultMob = curveFn.parent(0)
        resultObj = om2.MDagPath.getAPathTo(resultMob).fullPathName()
        sel = om2.MSelectionList().add(resultObj)
        om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectObjectMode)
        om2.MGlobal.setActiveSelectionList(sel)
        cmds.nurbsCurveToBezier()
    return resultMob


def findUpVectorPosition(const, parent=None, create=False):
    """Find up vector local position based on a object matrix.

    Args:
        const (string, MObject or MDagPath): The name of the constraint object.
        parent (string, MObject or MDagPath: None [Optional]): The parent object to parent the result.
        create (bool: False [Optional]): If the function is allowed to create the object automatically.

    Returns:
        MVector: The local vector to apply in the final object.

    Raises:
        AttributeError: If the const argument is not a string.
    """
    if (not isinstance(const, str) and
            not isinstance(const, om2.MObject) and
            not isinstance(const, om2.MDagPath)):
        raise AttributeError("Argument const must be a string.")
    if (not isinstance(parent, str) and
            not isinstance(parent, om2.MObject) and
            not isinstance(parent, om2.MDagPath) and
            parent is not None):
        raise AttributeError("Argument parent must be a string.")
    if isinstance(const, str):
        constDag = om2.MSelectionList().add(const).getDagPath(0)
    elif isinstance(const, om2.MObject):
        constDag = om2.MDagPath.getAPathTo(const)
    elif isinstance(const, om2.MDagPath):
        constDag = const
    mConstWorld = constDag.inclusiveMatrix()
    mUpLocal = om2.MMatrix()
    mUpLocal[13] = 1.0
    mUpWorld = mUpLocal * mConstWorld
    vConst = om2.MVector(mConstWorld[12], mConstWorld[13], mConstWorld[14])
    vUp = om2.MVector(mUpWorld[12], mUpWorld[13], mUpWorld[14])
    vResult = vUp - vConst
    if create:
        parentObj = om2.MSelectionList().add(parent).getDependNode(0)
        upVecObj = om2.MFnDagNode().create("transform", "upVectorObject", parentObj)
        upVecDag = om2.MDagPath.getAPathTo(upVecObj)
        transFn = om2.MFnTransform(upVecDag)
        transFn.translateBy(vResult, om2.MSpace.kTransform)
        om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectObjectMode)
        om2.MGlobal.setActiveSelectionList(om2.MSelectionList().add(upVecDag))
    return vResult


def connectAttr(startAttr, endAttr):
    """Connect attributes from two nodes.

    Args:
        startAttr (string or MPlug): The name of the output plug attribute.
        endAttr (string or MPlug): The name of the input plug attribute.

    Returns:
        True: If succeed.

    Raises:
        AttributeError: If any argument is not a string or a MPlug.
        TypeError: If the objects passed is not a dag node.
    """
    if not isinstance(startAttr, str) and not isinstance(startAttr, om2.MPlug):
        raise AttributeError("Argument startAttr must be a string or MPlug.")
    if not isinstance(endAttr, str) and not isinstance(endAttr, om2.MPlug):
        raise AttributeError("Argument endAttr must be a string or MPlug.")
    if isinstance(startAttr, str):
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
    else:
        startPlug = startAttr
        endPlug = endAttr
    mdgmod = om2.MDGModifier()
    mdgmod.connect(startPlug, endPlug)
    mdgmod.doIt()
    return True

def lockAndHideAttributes(objects, attributes, lock=True, hide=True):
    """Lock and hide attributes.

    Args:
        objects (list of string or list of MObjects): The list of objects.
        attributes (list of string or list of MObjects): The list of attributes.
        lock (bool: True [Optional]): The state of locking.
        hide (bool: True [Optional]): The state of hiding.

    Returns:
        list: The names of the attributes locked.

    Raises:
        AttributeError: If any argument is not a list of strings or a list of MObjects.
        RuntimeError: If any object or attribute don't exists.
    """
    if not isinstance(objects, list):
        raise AttributeError("Argument objects must be a list of strings or a list of MObjects.")
    for parseObj in objects:
        if not isinstance(parseObj, str) and not isinstance(parseObj, om2.MObject):
            raise AttributeError("Argument objects must be a list of strings or a list of MObjects.")
    if not isinstance(attributes, list):
        raise AttributeError("Argument attributes must be a list of strings or a list of MObjects.")
    for parseAttr in attributes:
        if not isinstance(parseAttr, str) and not isinstance(parseAttr, om2.MObject):
            raise AttributeError("Argument attributes must be a list of strings or a list of MObjects.")
    for obj in objects:
        if isinstance(obj, str):
            curObj = om2.MSelectionList().add(obj).getDependNode(0)
        else:
            curObj = obj
        nodeFn = om2.MFnDependencyNode(curObj)
        for attr in attributes:
            if not nodeFn.hasAttribute(attr):
                raise RuntimeError("Object %s don't have %s attribute." % (nodeFn.name(), attr))
            curAttr = nodeFn.attribute(attr)
            curPlug = om2.MPlug(curObj, curAttr)
            curPlug.isLocked = lock
            if curPlug.isCompound:
                for i in range(curPlug.numChildren()):
                    curChildPlug = curPlug.child(i)
                    curChildPlug.isChannelBox = not hide
                    curChildPlug.isKeyable = not hide
            else:
                curPlug.isChannelBox = not hide
                curPlug.isKeyable = not hide
    return None

def createChar(name):
    """Create a character node hierarchy.

    Args:
        name (string): The name of the character node.

    Returns:
        string: The Dag Path of the char node.
    """
    om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectObjectMode)
    charObj = om2.MFnDagNode().create("transform", "%s_char" % name)
    deformObj = om2.MFnDagNode().create("transform", "deform_hrc", charObj)
    geometryObj = om2.MFnDagNode().create("transform", "geometry_hrc", charObj)
    geoIOObj = om2.MFnDagNode().create("transform", "geometry_settings_io", geometryObj)
    nodeFn = om2.MFnDependencyNode(charObj)
    plug = nodeFn.findPlug("useOutlinerColor", False)
    plug.setBool(True)
    plug = nodeFn.findPlug("outlinerColor", False)
    dataHandle = plug.asMDataHandle()
    dataHandle.set3Float(kCharOutlinerColor.r, kCharOutlinerColor.g, kCharOutlinerColor.b)
    plug.setMDataHandle(dataHandle)
    lockAndHideAttributes([charObj, deformObj, geometryObj, geoIOObj],
                          ["translate", "rotate", "scale", "shear"])
    lockAndHideAttributes([deformObj, geometryObj, geoIOObj], ["visibility"])
    createTypedAttribute("APIType", "APIType", AttributeTypes.kString, selList=[nodeFn.name()])
    apiTypePlug = nodeFn.findPlug("APIType", False)
    apiTypePlug.setString("char")
    apiTypePlug.isLocked = True
    createMessageAttribute("deformHrc", "deformHrc", selList=[nodeFn.name()])
    charDeformPlug = nodeFn.findPlug("deformHrc", False)
    createMessageAttribute("geometryHrc", "geometryHrc", selList=[nodeFn.name()])
    charGeoPlug = nodeFn.findPlug("geometryHrc", False)
    nodeFn.setObject(deformObj)
    createTypedAttribute("APIType", "APIType", AttributeTypes.kString, selList=[nodeFn.name()])
    apiTypePlug = nodeFn.findPlug("APIType", False)
    apiTypePlug.setString("hierarchy")
    apiTypePlug.isLocked = True
    createMessageAttribute("character", "character", selList=[nodeFn.name()])
    deformCharPlug = nodeFn.findPlug("character", False)
    createMessageAttribute("components", "components", selList=[nodeFn.name()])
    nodeFn.setObject(geometryObj)
    createTypedAttribute("APIType", "APIType", AttributeTypes.kString, selList=[nodeFn.name()])
    apiTypePlug = nodeFn.findPlug("APIType", False)
    apiTypePlug.setString("hierarchy")
    apiTypePlug.isLocked = True
    createMessageAttribute("character", "character", selList=[nodeFn.name()])
    geoCharPlug = nodeFn.findPlug("character", False)
    createMessageAttribute("ioConn", "ioConn", selList=[nodeFn.name()])
    geoIOConnPlug = nodeFn.findPlug("ioConn", False)
    createMessageAttribute("bindLayer1", "bindLayer1", selList=[nodeFn.name()])
    nodeFn.setObject(geoIOObj)
    createTypedAttribute("APIType", "APIType", AttributeTypes.kString, selList=[nodeFn.name()])
    apiTypePlug = nodeFn.findPlug("APIType", False)
    apiTypePlug.setString("io")
    apiTypePlug.isLocked = True
    createMessageAttribute("geometryHrc", "geometryHrc", selList=[nodeFn.name()])
    geoPlug = nodeFn.findPlug("geometryHrc", False)
    createEnumAttribute("displayGeo", "displayGeo", {"Hide": 0, "Show": 1, "Reference":2}, selList=[nodeFn.name()])
    displayGeoPlug = nodeFn.findPlug("displayGeo", False)
    displayGeoPlug.setShort(1)
    connectAttr(charDeformPlug, deformCharPlug)
    connectAttr(charGeoPlug, geoCharPlug)
    connectAttr(geoIOConnPlug, geoPlug)
    charPath = om2.MDagPath().getAPathTo(charObj)
    sel = om2.MSelectionList().add(charPath)
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
        RuntimeError: If don't find deform_hrc.
    """
    charName = char if "_char" in char else "".join([char, "_char"])
    charObj = om2.MSelectionList().add(charName).getDependNode(0)
    nodeFn = om2.MFnDependencyNode(charObj)
    if not charObj.hasFn(om2.MFn.kDagNode) or not nodeFn.hasAttribute("APIType"):
        raise RuntimeError("The specified char name is not a char or don't exists.")
    if nodeFn.findPlug("APIType", False).asString() != "char":
        raise RuntimeError("The specified char name is not a char or don't exists.")
    om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectObjectMode)
    charPath = om2.MDagPath().getAPathTo(charObj)
    deformObj = None
    for i in range(charPath.childCount()):
        if om2.MFnDependencyNode(charPath.child(i)).name() == "deform_hrc":
            deformObj = charPath.child(i)
            break
    if deformObj is None:
        raise RuntimeError("Can't find deform_hrc")
    cmpntObj = om2.MFnDagNode().create("transform", "%s_cmpnt" % name, deformObj)
    ioConnObj = om2.MFnDagNode().create("transform", "%s_settings_io" % name, cmpntObj)
    jntsObj = om2.MFnDagNode().create("transform", "%s_joints_hrc" % name, cmpntObj)
    ctrlsObj = om2.MFnDagNode().create("transform", "%s_controls_hrc" % name, cmpntObj)
    ikHdlesObj = om2.MFnDagNode().create("transform", "%s_ikHandles_hrc" % name, cmpntObj)
    miscObj = om2.MFnDagNode().create("transform", "%s_misc_hrc" % name, cmpntObj)
    lockAndHideAttributes([cmpntObj, ioConnObj, jntsObj, ctrlsObj, ikHdlesObj, miscObj],
                          ["translate", "rotate", "scale", "shear"])
    nodeFn.setObject(deformObj)
    deformComponentsPlug = om2.MPlug(deformObj, nodeFn.attribute("components"))
    nodeFn.setObject(cmpntObj)
    createTypedAttribute("APIType", "APIType", AttributeTypes.kString, selList=[nodeFn.name()])
    apiTypePlug = nodeFn.findPlug("APIType", False)
    apiTypePlug.setString("component")
    apiTypePlug.isLocked = True
    createMessageAttribute("deformHrc", "deformHrc", selList=[nodeFn.name()])
    createMessageAttribute("bindLayer1", "bindLayer1", selList=[nodeFn.name()])
    createMessageAttribute("controls", "controls", selList=[nodeFn.name()])
    createMessageAttribute("ikHandles", "ikHandles", selList=[nodeFn.name()])
    createMessageAttribute("ioConn", "ioConn", selList=[nodeFn.name()])
    cmpntDeformPlug = om2.MPlug(cmpntObj, nodeFn.attribute("deformHrc"))
    cmpntIoPlug = om2.MPlug(cmpntObj, nodeFn.attribute("ioConn"))
    nodeFn.setObject(ioConnObj)
    createTypedAttribute("APIType", "APIType", AttributeTypes.kString, selList=[nodeFn.name()])
    apiTypePlug = nodeFn.findPlug("APIType", False)
    apiTypePlug.setString("io")
    apiTypePlug.isLocked = True
    createMessageAttribute("component", "component", selList=[nodeFn.name()])
    createNumericAttribute("displayJoints", "displayJoints", AttributeTypes.kBool, default=True, selList=[nodeFn.name()])
    createNumericAttribute("displayControls", "displayControls", AttributeTypes.kBool, default=True, selList=[nodeFn.name()])
    createNumericAttribute("displayIKHandles", "displayIKHandles", AttributeTypes.kBool, default=True, selList=[nodeFn.name()])
    createNumericAttribute("displayMisc", "displayMisc", AttributeTypes.kBool, default=True, selList=[nodeFn.name()])
    ioComponentPlug = om2.MPlug(ioConnObj, nodeFn.attribute("component"))
    ioDisplayJointsPlug = om2.MPlug(ioConnObj, nodeFn.attribute("displayJoints"))
    ioDisplayControlsPlug = om2.MPlug(ioConnObj, nodeFn.attribute("displayControls"))
    ioDisplayIKHandlesPlug = om2.MPlug(ioConnObj, nodeFn.attribute("displayIKHandles"))
    ioDisplayMiscPlug = om2.MPlug(ioConnObj, nodeFn.attribute("displayMisc"))
    jntsVisPlug = om2.MPlug(jntsObj, om2.MFnDependencyNode(jntsObj).attribute("visibility"))
    ctrlsVisPlug = om2.MPlug(ctrlsObj, om2.MFnDependencyNode(ctrlsObj).attribute("visibility"))
    ikHdlesVisPlug = om2.MPlug(ikHdlesObj, om2.MFnDependencyNode(ikHdlesObj).attribute("visibility"))
    miscVisPlug = om2.MPlug(miscObj, om2.MFnDependencyNode(miscObj).attribute("visibility"))
    connectAttr(deformComponentsPlug, cmpntDeformPlug)
    connectAttr(cmpntIoPlug, ioComponentPlug)
    connectAttr(ioDisplayJointsPlug, jntsVisPlug)
    connectAttr(ioDisplayControlsPlug, ctrlsVisPlug)
    connectAttr(ioDisplayIKHandlesPlug, ikHdlesVisPlug)
    connectAttr(ioDisplayMiscPlug, miscVisPlug)
    lockAndHideAttributes([ioConnObj, jntsObj, ctrlsObj, ikHdlesObj, miscObj], ["visibility"])
    cmpntPath = om2.MDagPath().getAPathTo(cmpntObj)
    sel = om2.MSelectionList().add(cmpntPath)
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
                           writable=True, readable=True, keyable=True, storable=True, channelBox=False, selList=None):
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
        selList (list: None [Optional]): The selection list of the objects to be modified.

    Returns:
        list: The names of the attributes created.

    Raises:
        TypeError: If the attrType is not a numeric type.
    """
    if not isinstance(selList, list) or selList is None:
        selList = om2.MGlobal.getActiveSelectionList()
    else:
        listObjs = selList
        selList = om2.MSelectionList()
        for obj in listObjs:
            selList.add(obj)
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
                        writable=True, readable=True, keyable=True, storable=True, channelBox=False, selList=None):
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
        selList (list: None [Optional]): The selection list of the objects to be modified.

    Returns:
        list: The names of the attributes created.

    Raises:
        TypeError: If the attrType is not a unit type.
    """
    if not isinstance(selList, list) or selList is None:
        selList = om2.MGlobal.getActiveSelectionList()
    else:
        listObjs = selList
        selList = om2.MSelectionList()
        for obj in listObjs:
            selList.add(obj)
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
                          keyable=True, storable=True, channelBox=False, selList=None):
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
        selList (list: None [Optional]): The selection list of the objects to be modified.

    Returns:
        list: The names of the attributes created.

    Raises:
        TypeError: If the attrType is not a matrix type.
    """
    if not isinstance(selList, list) or selList is None:
        selList = om2.MGlobal.getActiveSelectionList()
    else:
        listObjs = selList
        selList = om2.MSelectionList()
        for obj in listObjs:
            selList.add(obj)
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
                         keyable=True, storable=True, channelBox=False, selList=None):
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
        selList (list: None [Optional]): The selection list of the objects to be modified.

    Returns:
        list: The names of the attributes created.

    Raises:
        TypeError: If the attrType is not a typed type.
    """
    if not isinstance(selList, list) or selList is None:
        selList = om2.MGlobal.getActiveSelectionList()
    else:
        listObjs = selList
        selList = om2.MSelectionList()
        for obj in listObjs:
            selList.add(obj)
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
                        keyable=True, storable=True, channelBox=False, selList=None):
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
        selList (list: None [Optional]): The selection list of the objects to be modified.

    Returns:
        list: The names of the attributes created.

    Raises:
        RuntimeError: If the enum argument is not a dict or its empty.
    """
    if not isinstance(selList, list) or selList is None:
        selList = om2.MGlobal.getActiveSelectionList()
    else:
        listObjs = selList
        selList = om2.MSelectionList()
        for obj in listObjs:
            selList.add(obj)
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
                           keyable=True, storable=True, channelBox=False, selList=None):
    """Create custom message attribute in selected objects.

    Args:
        longName (string): The long name of the attribute about to be created.
        shortName (string): The short name of the attribute about to be created.
        writable (bool: True [Optional]): Create as writable attribute.
        readable (bool: True [Optional]): Create as readable attribute.
        keyable (bool: True [Optional]): Create as keyable attribute.
        storable (bool: True [Optional]): Create as storable attribute.
        channelBox (bool: False [Optional]): Create as channelBox attribute.
        selList (list: None [Optional]): The selection list of the objects to be modified.

    Returns:
        list: The names of the attributes created.
    """
    if not isinstance(selList, list) or selList is None:
        selList = om2.MGlobal.getActiveSelectionList()
    else:
        listObjs = selList
        selList = om2.MSelectionList()
        for obj in listObjs:
            selList.add(obj)
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
                          readable=True, keyable=True, storable=True, channelBox=False, selList=None):
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
        selList (list: None [Optional]): The selection list of the objects to be modified.

    Returns:
        list: The names of the attributes created.

    Raises:
        IndexError: If the length argument is different than 2 and 3.
        TypeError: If the attrType argument is not a numeric type.
    """
    if not isinstance(selList, list) or selList is None:
        selList = om2.MGlobal.getActiveSelectionList()
    else:
        listObjs = selList
        selList = om2.MSelectionList()
        for obj in listObjs:
            selList.add(obj)
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
                         storable=True, channelBox=False, selList=None):
    """Create a custom color attribute in selected objects.

    Args:
        longName (string): The long name of the attribute about to be created.
        shortName (string): The short name of the attribute about to be created.
        writable (bool: True [Optional]): Create as writable attribute.
        readable (bool: True [Optional]): Create as readable attribute.
        keyable (bool: True [Optional]): Create as keyable attribute.
        storable (bool: True [Optional]): Create as storable attribute.
        channelBox (bool: False [Optional]): Create as channelBox attribute.
        selList (list: None [Optional]): The selection list of the objects to be modified.

    Returns:
        list: The names of the attributes created.
    """
    if not isinstance(selList, list) or selList is None:
        selList = om2.MGlobal.getActiveSelectionList()
    else:
        listObjs = selList
        selList = om2.MSelectionList()
        for obj in listObjs:
            selList.add(obj)
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

def createFK(sections=1, rootList=None, connect=True):
    """Create a FK Chain with given roots.

    Rotation attributes can be connected automatically with connect argument setted to True.

    Args:
        sections (int: 1 [Optional]): The number of controls to be created in each segment.
        rootList (list: None [Optional]): The list of the root objects. If None, the function will get the active selection list.
        connect (bool: True [Optional]): Auto-connect rotate attributes.

    Returns:
        True: If succeed.

    Raises:
        AssertionError: If sections argument is not integer.
        AssertionError: If sections argument is less than 1.
    """
    assert isinstance(sections, int), "Argument sections must be int."
    assert sections >= 1, "Argument sections must be greater than 1."
    if not isinstance(rootList, list) or rootList is None:
        rootList = om2.MGlobal.getActiveSelectionList()
    else:
        listObjs = rootList
        rootList = om2.MSelectionList()
        for obj in listObjs:
            rootList.add(obj)
    objCreator = om2.MFnDagNode()
    dagMod = om2.MDagModifier()
    for root in range(rootList.length()):
        rootPath = rootList.getDagPath(root)
        rootName = rootPath.partialPathName()
        itDag = om2.MItDag()
        itDag.reset(rootPath, om2.MItDag.kDepthFirst)
        rootGrp = objCreator.create("transform", "%s_ctrlGrp" % rootName)
        parentDict = dict()
        while not itDag.isDone():
            curObjPath = itDag.getPath()
            if curObjPath.childCount() >= 1:
                curObjName = curObjPath.partialPathName()
                curParObjPath = om2.MDagPath.getAPathTo(om2.MFnDagNode(curObjPath).parent(0))
                curParObjName = curParObjPath.partialPathName()
                transformation = curObjPath.inclusiveMatrix()
                # Create objects
                if sections == 1:
                    curBuffName = "%s_bufferCtrl" % curObjName
                    curCtrlName = "%s_ctrl" % curObjName
                    curBuff = objCreator.create("transform", curBuffName, rootGrp)
                    ctrl = cmds.circle(c=(0, 0, 0), nr=(1, 0, 0), sw=360, r=4, d=3,
                                       ut=False, s=8, ch=False)[0]
                    curCtrl = om2.MSelectionList().add(ctrl).getDependNode(0)
                    dagMod.reparentNode(curCtrl, curBuff)
                    dagMod.renameNode(curCtrl, curCtrlName)
                    dagMod.doIt()
                    parentDict[curObjName] = {
                        "Buffer": curBuff,
                        "Control": curCtrl,
                        "Transformation": transformation
                    }
                # Configure objects
                curTrans = parentDict[curObjName]["Buffer"]
                curMtxW = parentDict[curObjName]["Transformation"]
                curCtrlPath = om2.MDagPath.getAPathTo(curTrans)
                transFn = om2.MFnTransform(curCtrlPath)
                if curParObjName != "":
                    if curParObjName in parentDict.keys():
                        parent = parentDict[curParObjName]["Control"]
                        current = parentDict[curObjName]["Buffer"]
                        dagMod.reparentNode(current, parent)
                        dagMod.doIt()
                        parentMtxW = parentDict[curParObjName]["Transformation"]
                    else:
                        parentMtxW = om2.MMatrix.kIdentity
                    curMtx = curMtxW * parentMtxW.inverse()
                    mtxFn = om2.MTransformationMatrix(curMtx)
                    objTrans = mtxFn.translation(om2.MSpace.kWorld)
                    objRot = mtxFn.rotation(asQuaternion=False)
                    objSca = mtxFn.scale(om2.MSpace.kWorld)
                    transFn.setTranslation(objTrans, om2.MSpace.kTransform)
                    transFn.setRotation(objRot, om2.MSpace.kTransform)
                    transFn.setScale(objSca)
                else:
                    mtxFn = om2.MTransformationMatrix(curMtxW)
                    objTrans = mtxFn.translation(om2.MSpace.kWorld)
                    objRot = mtxFn.rotation(asQuaternion=False)
                    objSca = mtxFn.scale(om2.MSpace.kWorld)
                    transFn.setTranslation(objTrans, om2.MSpace.kTransform)
                    transFn.setRotation(objRot, om2.MSpace.kTransform)
                    transFn.setScale(objSca)
                if connect:
                    dagFn = om2.MFnDagNode(curObjPath)
                    targetRotPlug = dagFn.findPlug("rotate", False)
                    nodeFn = om2.MFnDependencyNode(parentDict[curObjName]["Control"])
                    sourceRotPlug = nodeFn.findPlug("rotate", False)
                    dagMod.connect(sourceRotPlug, targetRotPlug)
                    dagMod.doIt()
            itDag.next()
    return True
