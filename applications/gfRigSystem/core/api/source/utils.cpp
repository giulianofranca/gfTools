#include "headers/utils.h"


// -------------------------------------------------------------------------------------------
// FUNCTIONS
// -------------------------------------------------------------------------------------------

// unfreezeTransformations

static void unfreezeTransformations(){
    /* Unfreeze selected objects translation.

    Returns:
        True: If succeed.
    */
    MSelectionList sel;
    MGlobal::getActiveSelectionList(sel, true);
    for (uint32_t i = 0; i < sel.length(); i++){
        MDagPath obj;
        sel.getDagPath(i, obj);
        MFnTransform transFn(obj);
        MPoint rp = transFn.rotatePivot(MSpace::kWorld);
        MVector vPos = MVector(rp.x, rp.y, rp.z);
        transFn.translateBy(-vPos, MSpace::kWorld);
        MString makeIdentity = MString("cmds.makeIdentity(a=True, t=True, r=False, s=False, n=False, pn=True)");
        MGlobal::executePythonCommand(makeIdentity);
        transFn.translateBy(vPos, MSpace::kWorld);
    }
    return;
}

static void unfreezeTransformationsUNDO(){
}

static PyObject* unfreezeTransformationsPy(PyObject* self, PyObject* args){
    PyGILState_STATE pyGILState = PyGILState_Ensure();

    unfreezeTransformations();

    PyGILState_Release(pyGILState);
    Py_RETURN_TRUE;
}


// getPoleVectorPosition

static const char* getPoleVectorPosition(double distance){
    /*Find the right pole vector position based on selection.

    Create an transform object in the right position. To use this command select 3 dag nodes in the scene.
    (More than 3 object will be ignored).

    Args:
        distance (double: 1.0 [Optional]): The distance multiplier between the joint chain and the pole vector position.

    Returns:
        string: The path of the transform object created on position.

    Raises:
        RuntimeError: When the selection list is less than 3.
        ValueError: When the distance is not a double value.
    */
    MStatus status;
    MSelectionList sel;
    MGlobal::getActiveSelectionList(sel, true);
    MDagPath startPath, midPath, endPath;
    sel.getDagPath(0, startPath);
    sel.getDagPath(1, midPath);
    sel.getDagPath(2, endPath);
    MFnTransform transFn(startPath);
    MVector vStart = transFn.translation(MSpace::kWorld);
    transFn.setObject(midPath);
    MVector vMid = transFn.translation(MSpace::kWorld);
    transFn.setObject(endPath);
    MVector vEnd = transFn.translation(MSpace::kWorld);
    MVector vStartEnd = vEnd - vStart;
    MVector vStartMid = vMid - vStart;
    double dotP = vStartMid * vStartEnd;
    double proj = dotP / vStartEnd.length();
    MVector nStartEnd = vStartEnd.normal();
    MVector vProj = nStartEnd * proj;
    MVector vArrow = vStartMid - vProj;
    vArrow *= distance;
    MVector vFinal = vArrow + vMid;
    MVector vCross1 = vStartEnd ^ vStartMid;
    vCross1.normalize();
    MVector vCross2 = vCross1 ^ vArrow;
    vCross2.normalize();
    vArrow.normalize();
    double matrix[4][4] = {
        {vArrow.x, vArrow.y, vArrow.z, 0.0},
        {vCross1.x, vCross1.y, vCross1.z, 0.0},
        {vCross2.x, vCross2.y, vCross2.z, 0.0},
        {0.0, 0.0, 0.0, 1.0}
    };
    MMatrix mMtx = MMatrix(matrix);
    MTransformationMatrix mtxFn = MTransformationMatrix(mMtx);
    MQuaternion quat = mtxFn.rotation();
    MObject posObj = MFnDependencyNode().create("transform", &status);
    MDagPath posObjPath;
    MDagPath::getAPathTo(posObj, posObjPath);
    transFn.setObject(posObjPath);
    transFn.translateBy(vFinal, MSpace::kTransform);
    transFn.rotateBy(quat, MSpace::kTransform);
    MSelectionList objSel = MSelectionList();
    objSel.add(posObjPath);
    MGlobal::setSelectionMode(MGlobal::kSelectObjectMode);
    MGlobal::setActiveSelectionList(objSel);
    return posObjPath.fullPathName().asChar();
}

static PyObject* getPoleVectorPositionPy(PyObject* self, PyObject* args){
    double distance;
    if (!PyArg_ParseTuple(args, "d", &distance))
        return NULL;

    PyGILState_STATE pyGILState = PyGILState_Ensure();

    MSelectionList sel;
    MGlobal::getActiveSelectionList(sel, true);
    const char* pathName;
    if (sel.length() >= 3)
        pathName = getPoleVectorPosition(distance);
    else{
        PyErr_Format(PyExc_RuntimeError, "Selection list is less than 3. Select at least 3 objects.");
        return NULL;
    }

    PyObject* result = Py_BuildValue("s", pathName);

    PyGILState_Release(pyGILState);

    return result;
}