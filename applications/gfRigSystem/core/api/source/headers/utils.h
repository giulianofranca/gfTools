#include <cstdint>
#include <typeinfo>
#include <assert.h>

#include <python2.7/Python.h>

#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>
#include <maya/MDagPath.h>
#include <maya/MFnTransform.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MVector.h>
#include <maya/MPoint.h>
#include <maya/MMatrix.h>
#include <maya/MTransformationMatrix.h>
#include <maya/MQuaternion.h>

template<typename Base, typename T>
inline bool isinstance(const T*){
    // if(isinstance<Class>(instance))
    return std::is_base_of<Base, T>::value;
}


// -------------------------------------------------------------------------------------------
// FUNCTIONS
// -------------------------------------------------------------------------------------------

// unfreezeTransformations
static void unfreezeTransformations();
static void unfreezeTransformationsUNDO();
static PyObject* unfreezeTransformationsPy(PyObject* self, PyObject* args);

static const char kUnfreezeTransformationsDoc[] = "Unfreeze selected objects translation.";
static PyMethodDef unfreezeTransformationsDef{
    "unfreezeTransformations", unfreezeTransformationsPy, METH_NOARGS,
    kUnfreezeTransformationsDoc
};


// getPoleVectorPosition
static const char* getPoleVectorPosition(double distance=1.0);
static const char* getPoleVectorPositionUNDO();
static PyObject* getPoleVectorPositionPy(PyObject* self, PyObject* args);

static const char kGetPoleVectorPositionDoc[] = "Find the right pole vector position based on selection.";
static PyMethodDef getPoleVectorPositionDef{
    "getPoleVectorPosition", getPoleVectorPositionPy, METH_VARARGS,
    kGetPoleVectorPositionDoc
};