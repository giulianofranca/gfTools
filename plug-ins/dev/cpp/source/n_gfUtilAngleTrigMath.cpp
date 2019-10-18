#include "headers/n_gfUtilAngleTrigMath.h"

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
AngularTrigMath::AngularTrigMath() {}

// Destructor.
AngularTrigMath::~AngularTrigMath() {}

MObject AngularTrigMath::inAngle1;
MObject AngularTrigMath::inAngle2;
MObject AngularTrigMath::inOperation;
MObject AngularTrigMath::outAngle;

void* AngularTrigMath::creator(){
    return new AngularTrigMath();
}

MStatus AngularTrigMath::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to AngularTrigMath class. Instances of AngularTrigMath will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnUnitAttribute uAttr;
    MFnEnumAttribute eAttr;

    inAngle1 = uAttr.create("angle1", "a1", MFnUnitAttribute::kAngle, 0.0, &status);
    INPUT_ATTR(uAttr);

    inAngle2 = uAttr.create("angle2", "a2", MFnUnitAttribute::kAngle, 0.0, &status);
    INPUT_ATTR(uAttr);

    inOperation = eAttr.create("operation", "operation", 0, &status);
    eAttr.addField("No Operation", 0);
    eAttr.addField("Cosine", 1);
    eAttr.addField("Sine", 2);
    eAttr.addField("Tangent", 3);
    eAttr.addField("Arccos", 4);
    eAttr.addField("Arcsin", 5);
    eAttr.addField("Arctan", 6);
    eAttr.addField("Arctan2", 7);
    INPUT_ATTR(eAttr);

    outAngle = uAttr.create("outAngle", "oa", MFnUnitAttribute::kAngle, 0.0, &status);
    OUTPUT_ATTR(uAttr);

    addAttribute(inOperation);
    addAttribute(inAngle1);
    addAttribute(inAngle2);
    addAttribute(outAngle);
    attributeAffects(inOperation, outAngle);
    attributeAffects(inAngle1, outAngle);
    attributeAffects(inAngle2, outAngle);

    return status;
}

MStatus AngularTrigMath::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outAngle)
        return MStatus::kUnknownParameter;

    MAngle angle1 = dataBlock.inputValue(inAngle1).asAngle();
    short operation = dataBlock.inputValue(inOperation).asShort();

    MDataHandle outAngleHandle = dataBlock.outputValue(outAngle);
    double resAngle;
    double rangeAngle = angle1.asDegrees();

    switch (operation)
    {
    case 0:
        outAngleHandle.setMAngle(angle1);
        break;
    case 1:
        resAngle = std::cos(angle1.asRadians());
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    case 2:
        resAngle = std::sin(angle1.asRadians());
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    case 3:
        resAngle = std::tan(angle1.asRadians());
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    case 4:
        if (rangeAngle > 1.0)
            rangeAngle = 1.0;
        else if (rangeAngle < -1.0)
            rangeAngle = -1.0;
        resAngle = std::acos(rangeAngle);
        outAngleHandle.setMAngle(MAngle(resAngle));
        break;
    case 5:
        if (rangeAngle > 1.0)
            rangeAngle = 1.0;
        else if (rangeAngle < -1.0)
            rangeAngle = -1.0;
        resAngle = std::asin(rangeAngle);
        outAngleHandle.setMAngle(MAngle(resAngle));
        break;
    case 6:
        resAngle = std::atan(angle1.asRadians());
        outAngleHandle.setMAngle(MAngle(resAngle));
        break;
    case 7:
        MAngle angle2 = dataBlock.inputValue(inAngle2).asAngle();
        resAngle = std::atan2(angle1.asRadians(), angle2.asRadians());
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kRadians));
        break;
    }
    outAngleHandle.setClean();

    return MStatus::kSuccess;
}