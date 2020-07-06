#include "headers/testClass.h"

int TestUtils_init(TestUtils* self, PyObject* args, PyObject *kwds){
    // Constructor (__init__)
    self->dict = PyDict_New();
    self->count = 0;
    return 0;
}

void TestUtils_dealloc(TestUtils* self){
    // Destructor
    Py_XDECREF(self->dict);
    self->ob_type->tp_free((PyObject*)self);
}

// PyObject* TestUtils_str(PyObject* self){
//     // return PyString_FromFormat("Repr-ified_TestUtils{{size:\%d}}");
//     return PyString_FromFormat("TestUtils(%d)", (TestUtils*)self->count);
// }

PyObject* TestUtils_set(TestUtils* self, PyObject* args){
    const char* key;
    PyObject* value;

    if (!PyArg_ParseTuple(args, "sO:set", &key, &value)){
        Py_DECREF(value);
        return NULL;
    }

    if (PyDict_SetItemString(self->dict, key, value) < 0){
        Py_DECREF(value);
        return NULL;
    }

    self->count++;

    return Py_BuildValue("i", self->count);
}