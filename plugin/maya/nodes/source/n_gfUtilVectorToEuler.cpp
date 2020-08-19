#include "headers/n_gfUtilVectorToEuler.h"


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
VectorToEuler::VectorToEuler() {}

// Destructor.
VectorToEuler::~VectorToEuler() {}

MObject VectorToEuler::inVector;
MObject VectorToEuler::outEuler;
MObject VectorToEuler::outEulerX;
MObject VectorToEuler::outEulerY;
MObject VectorToEuler::outEulerZ;


void* VectorToEuler::creator(){
    // Maya creator function.
    return new VectorToEuler();
}

MStatus VectorToEuler::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to TestNode class. Instances of TestNode will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnUnitAttribute uAttr;
    MFnNumericAttribute nAttr;

    inVector = nAttr.createPoint("vector", "vec", &status);
    INPUT_ATTR(nAttr);

    outEulerX = uAttr.create("outEulerX", "oex", MFnUnitAttribute::kAngle, 0.0, &status);
    outEulerY = uAttr.create("outEulerY", "oey", MFnUnitAttribute::kAngle, 0.0, &status);
    outEulerZ = uAttr.create("outEulerZ", "oez", MFnUnitAttribute::kAngle, 0.0, &status);
    outEuler = nAttr.create("outEuler", "oe", outEulerX, outEulerY, outEulerZ, &status);
    OUTPUT_ATTR(nAttr);

    addAttribute(inVector);
    addAttribute(outEuler);
    attributeAffects(inVector, outEuler);

    return status;
}

MStatus VectorToEuler::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    float3 &pos = dataBlock.inputValue(inVector).asFloat3();
    double euler[3];
    for (unsigned int i = 0; i < 3; i++){
        euler[i] = pos[i] * (M_PI / 180.0);
    }

    MDataHandle outEulerHandle = dataBlock.outputValue(outEuler);
    outEulerHandle.set3Double(euler[0], euler[1], euler[2]);
    outEulerHandle.setClean();

    return MStatus::kSuccess;
}