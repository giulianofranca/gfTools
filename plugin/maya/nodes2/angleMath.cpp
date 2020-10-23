#include "headers/angleMath.hpp"

// Configure a input attribute.
#define INPUT_ATTR(FNATTR)      \
    FNATTR.setWritable(true);   \
    FNATTR.setReadable(true);   \
    FNATTR.setStorable(true);   \
    FNATTR.setKeyable(true);    \
    CHECK_MSTATUS_AND_RETURN_IT(status);

// Configure a output attribute.
#define OUTPUT_ATTR(FNATTR)     \
    FNATTR.setWritable(false);  \
    FNATTR.setReadable(true);   \
    FNATTR.setStorable(false);  \
    FNATTR.setKeyable(false);   \
    CHECK_MSTATUS_AND_RETURN_IT(status);


// Constructors and Destructors
AngleMath::AngleMath(){}
AngleMath::~AngleMath(){}


// Members initialization
MObject AngleMath::inAngle1;
MObject AngleMath::inAngle2;
MObject AngleMath::inOperation;
MObject AngleMath::outAngle;




MPxNode::SchedulingType AngleMath::schedulingType() const{
    return MPxNode::SchedulingType::kParallel;
}

void* AngleMath::creator(){
    return new AngleMath();
}

MStatus AngleMath::initialize(){
    // Defines the set of attributes for this node. The attributes declared in this 
    // function are assigned as static members to AngleMath class. Instances of 
    // AngleMath will use these attributes to create plugs for use in the compute()
    // method.
    MStatus status;
    MFnEnumAttribute eAttr;
    MFnUnitAttribute uAttr;

    inOperation = eAttr.create("operation", "op", 0, &status);
    eAttr.addField("No Operation", Operation::noOp);
    eAttr.addField("Add", Operation::add);
    eAttr.addField("Subtract", Operation::subtract);
    eAttr.addField("Multiply", Operation::multiply);
    eAttr.addField("Divide", Operation::divide);
    eAttr.addField("Power", Operation::power);
    eAttr.addField("Min", Operation::min);
    eAttr.addField("Max", Operation::max);
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

    return MStatus::kSuccess;
}

MStatus AngleMath::compute(const MPlug& plug, MDataBlock& dataBlock){
    // Node computation method:
    //     * plug is a connection point related to one of our node attributes.
    //     * dataBlock contains the data on which we will base our computations.
    if (plug != outAngle)
        return MStatus::kUnknownParameter;

    double angle1 = dataBlock.inputValue(inAngle1).asAngle().asDegrees();
    double angle2 = dataBlock.inputValue(inAngle2).asAngle().asDegrees();
    short operation = dataBlock.inputValue(inOperation).asShort();

    MDataHandle outAngleHandle = dataBlock.outputValue(outAngle);
    MAngle resAngle;

    switch (operation){
        case Operation::noOp:
            resAngle = MAngle(angle1, MAngle::kDegrees);
            break;
        case Operation::add:
            resAngle = MAngle(angle1 + angle2, MAngle::kDegrees);
            break;
        case Operation::subtract:
            resAngle = MAngle(angle1 - angle2, MAngle::kDegrees);
            break;
        case Operation::multiply:
            resAngle = MAngle(angle1 * angle2, MAngle::kDegrees);
            break;
        case Operation::divide:
            if (angle2 != 0.0)
                resAngle = MAngle(angle1 / angle2, MAngle::kDegrees);
            else
                resAngle = MAngle(9999.999, MAngle::kDegrees);
            break;
        case Operation::power:
            resAngle = MAngle(std::pow(angle1, angle2), MAngle::kDegrees);
            break;
        case Operation::min:
            resAngle = MAngle(std::min(angle1, angle2), MAngle::kDegrees);
            break;
        case Operation::max:
            resAngle = MAngle(std::max(angle1, angle2), MAngle::kDegrees);
            break;
    }
    outAngleHandle.setMAngle(resAngle);
    outAngleHandle.setClean();

    return MStatus::kSuccess;
}