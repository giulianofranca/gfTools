#include "n_gfUtilVectorToEuler.h"


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

    MObject vectorX = nAttr.create("vectorX", "vecx", MFnNumericData::kDouble, 0.0, &status);
    MObject vectorY = nAttr.create("vectorY", "vecy", MFnNumericData::kDouble, 0.0, &status);
    MObject vectorZ = nAttr.create("vectorZ", "vecz", MFnNumericData::kDouble, 0.0, &status);
    inVector = nAttr.create("vector", "vec", vectorX, vectorY, vectorZ, &status);
    INPUT_ATTR(nAttr);

    MObject outEulerX = uAttr.create("outEulerX", "oex", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject outEulerY = uAttr.create("outEulerY", "oey", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject outEulerZ = uAttr.create("outEulerZ", "oez", MFnUnitAttribute::kAngle, 0.0, &status);
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
    if (plug != outEuler)
        return MStatus::kUnknownParameter;
    
    MVector vVector = dataBlock.inputValue(inVector).asVector();
    MEulerRotation eEuler = MEulerRotation(
        MAngle(vVector.x, MAngle::kDegrees).asRadians(),
        MAngle(vVector.y, MAngle::kDegrees).asRadians(),
        MAngle(vVector.z, MAngle::kDegrees).asRadians()
    );

    MDataHandle outEulerHandle = dataBlock.outputValue(outEuler);
    outEulerHandle.setMVector(eEuler.asVector());
    outEulerHandle.setClean();

    return MStatus::kSuccess;
}