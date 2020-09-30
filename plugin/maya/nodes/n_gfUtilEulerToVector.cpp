#include "headers/n_gfUtilEulerToVector.h"


// Configure a input attribute.
#define INPUT_ATTR(FNATTR)		\
	FNATTR.setWritable(true);	\
	FNATTR.setReadable(true);	\
	FNATTR.setStorable(true);	\
	FNATTR.setKeyable(true);	\

// Configure a output attribute.
#define OUTPUT_ATTR(FNATTR)		\
	FNATTR.setWritable(false);	\
	FNATTR.setReadable(true);	\
	FNATTR.setStorable(false);	\
	FNATTR.setKeyable(false);	\


// Constructor.
EulerToVector::EulerToVector() {}

// Destructor.
EulerToVector::~EulerToVector() {}

MObject EulerToVector::inEuler;
MObject EulerToVector::inEulerX;
MObject EulerToVector::inEulerY;
MObject EulerToVector::inEulerZ;
MObject EulerToVector::inToDegrees;
MObject EulerToVector::outVector;


void* EulerToVector::creator(){
    // Maya creator function.
    return new EulerToVector();
}

MStatus EulerToVector::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to TestNode class. Instances of TestNode will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnUnitAttribute uAttr;
    MFnNumericAttribute nAttr;

    inEulerX = uAttr.create("eulerX", "ex", MFnUnitAttribute::kAngle, 0.0, &status);
    inEulerY = uAttr.create("eulerY", "ey", MFnUnitAttribute::kAngle, 0.0, &status);
    inEulerZ = uAttr.create("eulerZ", "ez", MFnUnitAttribute::kAngle, 0.0, &status);
    inEuler = nAttr.create("euler", "e", inEulerX, inEulerY, inEulerZ, &status);
    INPUT_ATTR(nAttr);

    inToDegrees = nAttr.create("convertToDegrees", "todeg", MFnNumericData::kBoolean, true, &status);
    INPUT_ATTR(nAttr);

    outVector = nAttr.createPoint("outVector", "ov", &status);
    OUTPUT_ATTR(nAttr);

    addAttribute(inEuler);
    addAttribute(inToDegrees);
    addAttribute(outVector);
    attributeAffects(inEuler, outVector);
    attributeAffects(inToDegrees, outVector);

    return status;
}

MStatus EulerToVector::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    double3 &rot = dataBlock.inputValue(inEuler).asDouble3();
    bool toDegrees = dataBlock.inputValue(inToDegrees).asBool();
    double euler[3];

    if (toDegrees){
        for (unsigned int i = 0; i < 3; i++){
            euler[i] = rot[i] * (180.0 / M_PI);
        }
    }
    else{
        for (unsigned int i = 0; i < 3; i++){
            euler[i] = rot[i];
        }
    }
    MFloatVector vVector = MFloatVector(euler);

    MDataHandle outVectorHandle = dataBlock.outputValue(outVector);
    outVectorHandle.setMFloatVector(vVector);
    outVectorHandle.setClean();

    return MStatus::kSuccess;
}