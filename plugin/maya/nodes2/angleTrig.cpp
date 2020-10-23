#include "headers/angleTrig.hpp"

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
AngleTrig::AngleTrig(){}
AngleTrig::~AngleTrig(){}


// Members initialization
MObject AngleTrig::inAngle1;
MObject AngleTrig::inAngle2;
MObject AngleTrig::inOperation;
MObject AngleTrig::outAngle;




MPxNode::SchedulingType AngleTrig::schedulingType() const{
    return MPxNode::SchedulingType::kParallel;
}

void* AngleTrig::creator(){
    return new AngleTrig();
}

MStatus AngleTrig::initialize(){
    // Defines the set of attributes for this node. The attributes declared in this 
    // function are assigned as static members to AngleTrig class. Instances of 
    // AngleTrig will use these attributes to create plugs for use in the compute()
    // method.
    MStatus status;
    MFnEnumAttribute eAttr;
    MFnUnitAttribute uAttr;

    inOperation = eAttr.create("operation", "op", 0, &status);
    eAttr.addField("No Operation", Operation::noOp);
    eAttr.addField("Cosine", Operation::cosine);
    eAttr.addField("Sine", Operation::sine);
    eAttr.addField("Tangent", Operation::tangent);
    eAttr.addField("Arccos", Operation::arccos);
    eAttr.addField("Arcsin", Operation::arcsin);
    eAttr.addField("Arctan", Operation::arctan);
    eAttr.addField("Arctan2", Operation::arctan2);
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

MStatus AngleTrig::compute(const MPlug& plug, MDataBlock& dataBlock){
    // Node computation method:
    //     * plug is a connection point related to one of our node attributes.
    //     * dataBlock contains the data on which we will base our computations.
    if (plug != outAngle)
        return MStatus::kUnknownParameter;

    MAngle angle1 = dataBlock.inputValue(inAngle1).asAngle();
    short operation = dataBlock.inputValue(inOperation).asShort();

    MDataHandle outAngleHandle = dataBlock.outputValue(outAngle);
    MAngle clampedAngle, resAngle;

    switch (operation){
        case Operation::noOp:
            resAngle = angle1;
            break;
        case Operation::cosine:
            resAngle = MAngle(std::cos(angle1.asRadians()), MAngle::kDegrees);
            break;
        case Operation::sine:
            resAngle = MAngle(std::sin(angle1.asRadians()), MAngle::kDegrees);
            break;
        case Operation::tangent:
            resAngle = MAngle(std::tan(angle1.asRadians()), MAngle::kDegrees);
            break;
        case Operation::arccos:
            clampedAngle = MAngle(angle1);
            if (angle1.asDegrees() > 1.0)
                clampedAngle = MAngle(1.0, MAngle::kDegrees);
            else if (angle1.asDegrees() < -1.0)
                clampedAngle = MAngle(-1.0, MAngle::kDegrees);
            resAngle = MAngle(std::acos(clampedAngle.asDegrees()));
            break;
        case Operation::arcsin:
            clampedAngle = MAngle(angle1);
            if (angle1.asDegrees() > 1.0)
                clampedAngle = MAngle(1.0, MAngle::kDegrees);
            else if (angle1.asDegrees() < -1.0)
                clampedAngle = MAngle(-1.0, MAngle::kDegrees);
            resAngle = MAngle(std::asin(clampedAngle.asDegrees()));
            break;
        case Operation::arctan:
            resAngle = MAngle(std::atan(angle1.asRadians()), MAngle::kDegrees);
            break;
        case Operation::arctan2:
            MAngle angle2 = dataBlock.inputValue(inAngle2).asAngle();
            resAngle = MAngle(std::atan2(angle1.asRadians(), angle2.asRadians()), 
                              MAngle::kRadians);
            break;
    }
    outAngleHandle.setMAngle(resAngle);
    outAngleHandle.setClean();

    return MStatus::kSuccess;
}