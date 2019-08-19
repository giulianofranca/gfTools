#pragma once


#include <python2.7\Python.h>

int cFib(int n) {
	if (n < 2) {
		return n;
	}
	else {
		return cFib(n - 1) + cFib(n - 2);
	}
}

static PyObject* fib(PyObject* self, PyObject* args) {
	int n;

	if (!PyArg_ParseTuple(args, "i", &n)) {
		return NULL;
	}
	else {
		return Py_BuildValue("i", cFib(n));
	}
}

static PyObject* version(PyObject* self) {
	return Py_BuildValue("s", "Version 1.0");
}

static PyObject* fib2(PyObject* self, PyObject* args);


static PyMethodDef myMethods[] = {
	{"fib", fib, METH_VARARGS, "Calculates the fibonacci numbers."},
	{"version", (PyCFunction)version, METH_NOARGS, "Returns the version."},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef myModule = {
	PyModuleDef_HEAD_INIT,
	"myModule",
	"Fibonacci Module",
	-1,
	myMethods
};

PyMODINIT_FUNC init_m_rigAPI(void) {
	return PyModule_Create(&myModule);
}