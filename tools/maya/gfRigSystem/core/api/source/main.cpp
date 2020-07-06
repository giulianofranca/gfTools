#include "headers/utils.h"
#include "headers/testClass.h"


static const char kModuleDoc[] = "An example of Python C extension that makes use of Maya functionality.";
static PyMethodDef endMethods{NULL, NULL, 0, NULL};


static PyMethodDef gfRigSystemAPIMethods[] = {
    unfreezeTransformationsDef,
    getPoleVectorPositionDef,
    endMethods
};


// extern "C"
PyMODINIT_FUNC init_gfRigSystemAPI(void){
    PyObject* module = Py_InitModule3(
        "_gfRigSystemAPI",
        gfRigSystemAPIMethods,
        kModuleDoc
    );
    if (module == NULL)
        return;
    
    // Initialize objects.
    bool status = testUtilsInitialize(module);
    if (!status)
        return;
}
