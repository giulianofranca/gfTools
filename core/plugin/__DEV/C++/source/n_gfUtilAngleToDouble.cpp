#include "n_gfUtilAngleToDouble.h"

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
AngleToDouble::AngleToDouble() {}

// Destructor.
AngleToDouble::~AngleToDouble() {}

MObject AngleToDouble::inAngle;
MObject AngleToDouble::outDouble;

void* AngleToDouble::creator(){
    // Maya creator function.
    return new AngleToDouble();
}

MStatus AngleToDouble::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to AngleToDouble class. Instances of AngleToDouble will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnUnitAttribute uAttr;
    MFnNumericAttribute nAttr;

    inAngle = uAttr.create("angle", "angle", MFnUnitAttribute::kAngle, 0.0, &status);
    INPUT_ATTR(uAttr);

    outDouble = nAttr.create("outDouble", "od", MFnNumericData::kDouble, 0.0, &status);
    OUTPUT_ATTR(nAttr);

    addAttribute(inAngle);
    addAttribute(outDouble);
    attributeAffects(inAngle, outDouble);

    return status;
}

MStatus AngleToDouble::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outDouble)
        return MStatus::kUnknownParameter;

    double angle = dataBlock.inputValue(inAngle).asAngle().asDegrees();
    MDataHandle outDoubleHandle = dataBlock.outputValue(outDouble);

    outDoubleHandle.setDouble(angle);
    outDoubleHandle.setClean();

    return MStatus::kSuccess;
}