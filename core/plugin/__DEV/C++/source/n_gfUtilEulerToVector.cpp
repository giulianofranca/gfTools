#include "n_gfUtilEulerToVector.h"


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

    MObject eulerX = uAttr.create("eulerX", "ex", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject eulerY = uAttr.create("eulerY", "ey", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject eulerZ = uAttr.create("eulerZ", "ez", MFnUnitAttribute::kAngle, 0.0, &status);
    inEuler = nAttr.create("euler", "e", eulerX, eulerY, eulerZ, &status);
    INPUT_ATTR(nAttr);

    MObject outVectorX = nAttr.create("outVectorX", "ovx", MFnNumericData::kDouble, 0.0, &status);
    MObject outVectorY = nAttr.create("outVectorY", "ovy", MFnNumericData::kDouble, 0.0, &status);
    MObject outVectorZ = nAttr.create("outVectorZ", "ovz", MFnNumericData::kDouble, 0.0, &status);
    outVector = nAttr.create("outVector", "ov", outVectorX, outVectorY, outVectorZ, &status);
    OUTPUT_ATTR(nAttr);

    addAttribute(inEuler);
    addAttribute(outVector);
    attributeAffects(inEuler, outVector);

    return status;
}

MStatus EulerToVector::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outVector)
        return MStatus::kUnknownParameter;
    
    MVector vEuler = dataBlock.inputValue(inEuler).asVector();
    MEulerRotation eEuler = MEulerRotation(
        MAngle(vEuler.x, MAngle::kRadians).asDegrees(),
        MAngle(vEuler.y, MAngle::kRadians).asDegrees(),
        MAngle(vEuler.z, MAngle::kRadians).asDegrees()
    );

    MDataHandle outVectorHandle = dataBlock.outputValue(outVector);
    outVectorHandle.setMVector(eEuler.asVector());
    outVectorHandle.setClean();

    return MStatus::kSuccess;
}