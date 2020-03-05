#include "utils.cpp"


static const char kModuleDoc[] = "An example of Python C extension that makes use of Maya functionality.";
static PyMethodDef endMethods{NULL, NULL, 0, NULL};


static PyMethodDef gfRigSystemAPIMethods[] = {
    unfreezeTransformationsDef,
    getPoleVectorPositionDef,
    endMethods
};

extern "C" PyMODINIT_FUNC init_gfRigSystemAPI(){
    PyObject* module = Py_InitModule3(
        "_gfRigSystemAPI",
        gfRigSystemAPIMethods,
        kModuleDoc
    );
    if (module == NULL)
        return;
}