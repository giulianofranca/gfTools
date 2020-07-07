#include "headers/n_gfUtilDoubleToAngle.h"

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
DoubleToAngle::DoubleToAngle() {}

// Destructor.
DoubleToAngle::~DoubleToAngle() {}

MObject DoubleToAngle::inDouble;
MObject DoubleToAngle::outAngle;

void* DoubleToAngle::creator(){
    // Maya creator function.
    return new DoubleToAngle();
}

MStatus DoubleToAngle::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to DoubleToAngle class. Instances of DoubleToAngle will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnNumericAttribute nAttr;
    MFnUnitAttribute uAttr;

    inDouble = nAttr.create("double", "double", MFnNumericData::kDouble, 0.0, &status);
    INPUT_ATTR(nAttr);

    outAngle = uAttr.create("outAngle", "oa", MFnUnitAttribute::kAngle, 0.0, &status);
    OUTPUT_ATTR(uAttr);

    addAttribute(inDouble);
    addAttribute(outAngle);
    attributeAffects(inDouble, outAngle);

    return status;
}

MStatus DoubleToAngle::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outAngle)
        return MStatus::kUnknownParameter;

    double doubleVal = dataBlock.inputValue(inDouble).asDouble();
    MDataHandle outAngleHandle = dataBlock.outputValue(outAngle);

    outAngleHandle.setMAngle(MAngle(doubleVal, MAngle::kDegrees));
    outAngleHandle.setClean();

    return MStatus::kSuccess;
}