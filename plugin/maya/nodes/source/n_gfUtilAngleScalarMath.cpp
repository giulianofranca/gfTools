#include "headers/n_gfUtilAngleScalarMath.h"

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
AngularScalarMath::AngularScalarMath() {}

// Destructor.
AngularScalarMath::~AngularScalarMath() {}

MObject AngularScalarMath::inAngle;
MObject AngularScalarMath::inScalar;
MObject AngularScalarMath::inOperation;
MObject AngularScalarMath::outAngle;

void* AngularScalarMath::creator(){
    // Maya creator function.
    return new AngularScalarMath();
}

MStatus AngularScalarMath::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to AngularScalarMath class. Instances of AngularScalarMath will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnUnitAttribute uAttr;
    MFnNumericAttribute nAttr;
    MFnEnumAttribute eAttr;

    inAngle = uAttr.create("angle", "angle", MFnUnitAttribute::kAngle, 0.0, &status);
    INPUT_ATTR(uAttr);

    inScalar = nAttr.create("scalar", "scalar", MFnNumericData::kDouble, 0.0, &status);
    INPUT_ATTR(nAttr);

    inOperation = eAttr.create("operation", "operation", 0, &status);
    eAttr.addField("No Operation", 0);
    eAttr.addField("Add", 1);
    eAttr.addField("Subtract", 2);
    eAttr.addField("Multiply", 3);
    eAttr.addField("Divide", 4);
    eAttr.addField("Power", 5);
    eAttr.addField("Min", 6);
    eAttr.addField("Max", 7);
    INPUT_ATTR(eAttr);

    outAngle = uAttr.create("outAngle", "oa", MFnUnitAttribute::kAngle, 0.0, &status);
    OUTPUT_ATTR(uAttr);

    addAttribute(inOperation);
    addAttribute(inAngle);
    addAttribute(inScalar);
    addAttribute(outAngle);
    attributeAffects(inOperation, outAngle);
    attributeAffects(inAngle, outAngle);
    attributeAffects(inScalar, outAngle);

    return status;
}

MStatus AngularScalarMath::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outAngle)
        return MStatus::kUnknownParameter;

    double angle = dataBlock.inputValue(inAngle).asAngle().asDegrees();
    double scalar = dataBlock.inputValue(inScalar).asDouble();
    short operation = dataBlock.inputValue(inOperation).asShort();

    MDataHandle outAngleHandle = dataBlock.outputValue(outAngle);
    double resAngle;

    switch (operation)
    {
    case 0:
        outAngleHandle.setMAngle(MAngle(angle, MAngle::kDegrees));
        break;
    case 1:
        resAngle = angle + scalar;
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    case 2:
        resAngle = angle - scalar;
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    case 3:
        resAngle = angle * scalar;
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    case 4:
        if (scalar != 0.0)
            resAngle = angle + scalar;
        else
            resAngle = 9999.999;
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    case 5:
        resAngle = pow(angle, scalar);
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    case 6:
        resAngle = min(angle, scalar);
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    case 7:
        resAngle = max(angle, scalar);
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    }
    outAngleHandle.setClean();

    return MStatus::kSuccess;
}