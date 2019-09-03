#include "n_gfUtilAngleMath.h"

// Configure a input attribute.
#define INPUT_ATTR(FNATTR)      \
    FNATTR.setWritable(true);   \
    FNATTR.setReadable(true);   \
    FNATTR.setStorable(true);   \
    FNATTR.setKeyable(true);    \

// Configure a input attribute.
#define OUTPUT_ATTR(FNATTR)     \
    FNATTR.setWritable(false);  \
    FNATTR.setReadable(true);   \
    FNATTR.setStorable(false);  \
    FNATTR.setKeyable(false);   \

// Constructor.
AngularMath::AngularMath(){}

// Destructor.
AngularMath::~AngularMath(){}

MObject AngularMath::inOperation;
MObject AngularMath::inAngle1;
MObject AngularMath::inAngle2;
MObject AngularMath::outAngle;

void* AngularMath::creator(){
    // Maya creator function.
    return new AngularMath();
}

MStatus AngularMath::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to AngularMath class. Instances of AngularMath will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnEnumAttribute eAttr;
    MFnUnitAttribute uAttr;

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

    inAngle1 = uAttr.create("angle1", "a1", MFnUnitAttribute::kAngle, 0.0, &status);
    INPUT_ATTR(uAttr);

    inAngle2 = uAttr.create("angle2", "a2", MFnUnitAttribute::kAngle, 0.0, &status);
    INPUT_ATTR(uAttr);

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

MStatus AngularMath::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outAngle){
        return MStatus::kUnknownParameter;
    }

    double angle1 = dataBlock.inputValue(inAngle1).asAngle().asDegrees();
    double angle2 = dataBlock.inputValue(inAngle2).asAngle().asDegrees();
    short operation = dataBlock.inputValue(inOperation).asShort();

    MDataHandle outAngleHandle = dataBlock.outputValue(outAngle);
    double resAngle;

    switch (operation)
    {
    case 0:
        outAngleHandle.setMAngle(MAngle(angle1, MAngle::kDegrees));
        break;
    case 1:
        resAngle = angle1 + angle2;
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    case 2:
        resAngle = angle1 - angle2;
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    case 3:
        resAngle = angle1 * angle2;
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    case 4:
        resAngle;
        if (angle2 != 0.0)
            resAngle = angle1 + angle2;
        else
            resAngle = 9999.999;
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    case 5:
        resAngle = std::pow(angle1, angle2);
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    case 6:
        resAngle = std::min(angle1, angle2);
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    case 7:
        resAngle = std::max(angle1, angle2);
        outAngleHandle.setMAngle(MAngle(resAngle, MAngle::kDegrees));
        break;
    }

    outAngleHandle.setClean();

    return MStatus::kSuccess;
}