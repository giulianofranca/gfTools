#include "headers/n_gfUtilEulerScalarMath.h"


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
EulerScalarMath::EulerScalarMath() {}

// Destructor.
EulerScalarMath::~EulerScalarMath() {}

MObject EulerScalarMath::inOperation;
MObject EulerScalarMath::inEuler;
MObject EulerScalarMath::inEulerX;
MObject EulerScalarMath::inEulerY;
MObject EulerScalarMath::inEulerZ;
MObject EulerScalarMath::inEulerRotOrder;
MObject EulerScalarMath::inScalar;
MObject EulerScalarMath::inResRotOrder;
MObject EulerScalarMath::outEuler;
MObject EulerScalarMath::outEulerX;
MObject EulerScalarMath::outEulerY;
MObject EulerScalarMath::outEulerZ;


void* EulerScalarMath::creator(){
    // Maya creator function.
    return new EulerScalarMath();
}

MStatus EulerScalarMath::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to TestNode class. Instances of TestNode will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnEnumAttribute eAttr;
    MFnUnitAttribute uAttr;
    MFnNumericAttribute nAttr;

    inOperation = eAttr.create("operation", "operation", 0, &status);
    eAttr.addField("No Operation", 0);
    eAttr.addField("Add", 1);
    eAttr.addField("Subtract", 2);
    eAttr.addField("Multiply", 3);
    INPUT_ATTR(eAttr);

    inEulerX = uAttr.create("eulerX", "ex", MFnUnitAttribute::kAngle, 0.0, &status);
    inEulerY = uAttr.create("eulerY", "ey", MFnUnitAttribute::kAngle, 0.0, &status);
    inEulerZ = uAttr.create("eulerZ", "ez", MFnUnitAttribute::kAngle, 0.0, &status);
    inEuler = nAttr.create("euler", "e", inEulerX, inEulerY, inEulerZ, &status);
    INPUT_ATTR(nAttr);

    inEulerRotOrder = eAttr.create("rotateOrderEuler", "roe", 0, &status);
    eAttr.addField("xyz", 0);
    eAttr.addField("yzx", 1);
    eAttr.addField("zxy", 2);
    eAttr.addField("xzy", 3);
    eAttr.addField("yxz", 4);
    eAttr.addField("zyx", 5);
    INPUT_ATTR(eAttr);

    inScalar = nAttr.create("scalar", "scalar", MFnNumericData::kDouble, 0.0, &status);
    INPUT_ATTR(nAttr);

    inResRotOrder = eAttr.create("rotateOrderOutEuler", "rooe", 0, &status);
    eAttr.addField("xyz", 0);
    eAttr.addField("yzx", 1);
    eAttr.addField("zxy", 2);
    eAttr.addField("xzy", 3);
    eAttr.addField("yxz", 4);
    eAttr.addField("zyx", 5);
    INPUT_ATTR(eAttr);

    outEulerX = uAttr.create("outEulerX", "oex", MFnUnitAttribute::kAngle, 0.0, &status);
    outEulerY = uAttr.create("outEulerY", "oey", MFnUnitAttribute::kAngle, 0.0, &status);
    outEulerZ = uAttr.create("outEulerZ", "oez", MFnUnitAttribute::kAngle, 0.0, &status);
    outEuler = nAttr.create("outEuler", "oe", outEulerX, outEulerY, outEulerZ, &status);
    OUTPUT_ATTR(nAttr);

    addAttribute(inOperation);
    addAttribute(inEuler);
    addAttribute(inEulerRotOrder);
    addAttribute(inScalar);
    addAttribute(inResRotOrder);
    addAttribute(outEuler);
    attributeAffects(inOperation, outEuler);
    attributeAffects(inEuler, outEuler);
    attributeAffects(inEulerRotOrder, outEuler);
    attributeAffects(inScalar, outEuler);
    attributeAffects(inResRotOrder, outEuler);

    return status;
}

MStatus EulerScalarMath::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if ((plug != outEuler) &&
        (plug != outEulerX) &&
        (plug != outEulerY) &&
        (plug != outEulerZ)){
        return MStatus::kUnknownParameter;
    }

    short operation = dataBlock.inputValue(inOperation).asShort();
    double3 &euler = dataBlock.inputValue(inEuler).asDouble3();
    double scalar = dataBlock.inputValue(inScalar).asDouble();
    short eulerRotOrder = dataBlock.inputValue(inEulerRotOrder).asShort();
    short outRotOrder = dataBlock.inputValue(inResRotOrder).asShort();

    MEulerRotation eEuler = MEulerRotation(
        euler[0], 
        euler[1],
        euler[2],
        (MEulerRotation::RotationOrder) eulerRotOrder
    );

    MDataHandle outEulerHdle = dataBlock.outputValue(outEuler);
    MEulerRotation eScalar, eOutEuler;

    switch (operation)
    {
    case 0:
        eEuler.reorderIt((MEulerRotation::RotationOrder) outRotOrder);
        outEulerHdle.set3Double(eEuler.x, eEuler.y, eEuler.z);
        break;
    case 1:
        eEuler.reorderIt((MEulerRotation::RotationOrder) outRotOrder);
        eScalar = MEulerRotation(
            MAngle(scalar, MAngle::kDegrees).asRadians(),
            MAngle(scalar, MAngle::kDegrees).asRadians(),
            MAngle(scalar, MAngle::kDegrees).asRadians(),
            (MEulerRotation::RotationOrder) outRotOrder
        );
        eOutEuler = eEuler + eScalar;
        outEulerHdle.set3Double(eOutEuler.x, eOutEuler.y, eOutEuler.z);
        break;
    case 2:
        eEuler.reorderIt((MEulerRotation::RotationOrder) outRotOrder);
        eScalar = MEulerRotation(
            MAngle(scalar, MAngle::kDegrees).asRadians(),
            MAngle(scalar, MAngle::kDegrees).asRadians(),
            MAngle(scalar, MAngle::kDegrees).asRadians(),
            (MEulerRotation::RotationOrder) outRotOrder
        );
        eOutEuler = eEuler - eScalar;
        outEulerHdle.set3Double(eOutEuler.x, eOutEuler.y, eOutEuler.z);
        break;
    case 3:
        eEuler.reorderIt((MEulerRotation::RotationOrder) outRotOrder);
        eOutEuler = eEuler * scalar;
        outEulerHdle.set3Double(eOutEuler.x, eOutEuler.y, eOutEuler.z);
        break;
    }

    outEulerHdle.setClean();

    return MStatus::kSuccess;
}