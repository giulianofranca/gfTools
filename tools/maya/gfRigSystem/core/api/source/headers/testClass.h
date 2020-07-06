/*
https://docs.python.org/2/extending/newtypes.html
http://python3porting.com/cextensions.html
http://www.oilshell.org/blog/snapshots/2017-04/lcov-report/Objects/classobject.c.gcov.html
http://opendip.ru/lib/Python-3.7.4/Python/symtable.c
https://docs.python.org/fr/3.5/extending/newtypes.html - Part 2.2.6. Weak Reference Support
https://www.pythonsheets.com/notes/python-c-extensions.html

#if PY_MAJOR_VERSION >= 3
    static const char* test = "Oi";
#endif

*/
#ifndef TESTCLASS_H_INCLUDED
#define TESTCLASS_H_INCLUDED

#include <cstdint>

#include <python2.7/Python.h>
#include <python2.7/structmember.h>

// -------------------------------------------------------------------------------------------
// ---------- Struct
// -------------------------------------------------------------------------------------------
typedef struct{
    PyObject_HEAD
    PyObject* dict;
    int count;
} TestUtils;


// -------------------------------------------------------------------------------------------
// ---------- Members
// -------------------------------------------------------------------------------------------
static PyMemberDef dictMemberDef{
    "dict", T_OBJECT, offsetof(TestUtils, dict), 0,
    "The dictionary of values collected so far."
};

static PyMemberDef countMemberDef{
    "count", T_INT, offsetof(TestUtils, count), 0,
    "The number of times set() has been called."
};

static PyMemberDef TestUtils_members[] = {
    dictMemberDef,
    countMemberDef,
    {NULL, NULL, 0, NULL}
};

// -------------------------------------------------------------------------------------------
// ---------- Methods
// -------------------------------------------------------------------------------------------
// Constructor
int TestUtils_init(TestUtils* self, PyObject* args, PyObject *kwds);

// Destructor
void TestUtils_dealloc(TestUtils* self);

// Str
static PyObject* TestUtils_str(TestUtils* self){
    return PyString_FromFormat("_gfRigSystemAPI.TestUtils(%d)", self->count);
}

// Set
PyObject* TestUtils_set(TestUtils* self, PyObject* args);


static PyMethodDef TestUtils_methods[] = {
    {
        "set", (PyCFunction)TestUtils_set, METH_VARARGS,
        "Set a key and increment the count."
    },
    {NULL, NULL, 0, NULL}
};


// -------------------------------------------------------------------------------------------
// ---------- Type Object
// -------------------------------------------------------------------------------------------
static PyTypeObject TestUtilsType = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "testClass.TestUtils",                      /* tp_name */
    sizeof(TestUtils),                          /* tp_basicsize */
    0,                                          /* tp_itemsize */
    (destructor)TestUtils_dealloc,              /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_compare */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    (reprfunc)TestUtils_str,                    /* tp_str  */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,   /* tp_flags*/
    "TestUtils object",                         /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    TestUtils_methods,                          /* tp_methods */
    TestUtils_members,                          /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    (initproc)TestUtils_init,                   /* tp_init */
    0,                                          /* tp_alloc */
    0,                                          /* tp_new */
};


// -------------------------------------------------------------------------------------------
// ---------- Initialize Class
// -------------------------------------------------------------------------------------------
static const char* className = "TestUtils";
static PyObject* classType = (PyObject*)&TestUtilsType;

static bool testUtilsInitialize(PyObject* module){
    // Fill in some slots in the type, and make it ready.
    TestUtilsType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&TestUtilsType) < 0)
        return false;

    // Add the type to the module.
    Py_XINCREF(&TestUtilsType);
    PyModule_AddObject(module, className, classType);
    return true;
}

#endif