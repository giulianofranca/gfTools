#include "headers/n_gfUtilEulerMath.h"


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
EulerMath::EulerMath() {}

// Destructor.
EulerMath::~EulerMath() {}

MObject EulerMath::inOperation;
MObject EulerMath::inEuler1;
MObject EulerMath::inEuler1X;
MObject EulerMath::inEuler1Y;
MObject EulerMath::inEuler1Z;
MObject EulerMath::inEuler1RotOrder;
MObject EulerMath::inEuler2;
MObject EulerMath::inEuler2X;
MObject EulerMath::inEuler2Y;
MObject EulerMath::inEuler2Z;
MObject EulerMath::inEuler2RotOrder;
MObject EulerMath::inResRotOrder;
MObject EulerMath::outEuler;
MObject EulerMath::outEulerX;
MObject EulerMath::outEulerY;
MObject EulerMath::outEulerZ;


void* EulerMath::creator(){
    // Maya creator function.
    return new EulerMath();
}

MStatus EulerMath::initialize(){
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

    inEuler1X = uAttr.create("euler1X", "e1x", MFnUnitAttribute::kAngle, 0.0, &status);
    inEuler1Y = uAttr.create("euler1Y", "e1y", MFnUnitAttribute::kAngle, 0.0, &status);
    inEuler1Z = uAttr.create("euler1Z", "e1z", MFnUnitAttribute::kAngle, 0.0, &status);
    inEuler1 = nAttr.create("euler1", "e1", inEuler1X, inEuler1Y, inEuler1Z, &status);
    INPUT_ATTR(nAttr);

    inEuler1RotOrder = eAttr.create("rotateOrderEuler1", "roe1", 0, &status);
    eAttr.addField("xyz", 0);
    eAttr.addField("yzx", 1);
    eAttr.addField("zxy", 2);
    eAttr.addField("xzy", 3);
    eAttr.addField("yxz", 4);
    eAttr.addField("zyx", 5);
    INPUT_ATTR(eAttr);

    inEuler2X = uAttr.create("euler2X", "e2x", MFnUnitAttribute::kAngle, 0.0, &status);
    inEuler2Y = uAttr.create("euler2Y", "e2y", MFnUnitAttribute::kAngle, 0.0, &status);
    inEuler2Z = uAttr.create("euler2Z", "e2z", MFnUnitAttribute::kAngle, 0.0, &status);
    inEuler2 = nAttr.create("euler2", "e2", inEuler2X, inEuler2Y, inEuler2Z, &status);
    INPUT_ATTR(nAttr);

    inEuler2RotOrder = eAttr.create("rotateOrderEuler2", "roe2", 0, &status);
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

    inResRotOrder = eAttr.create("rotateOrderOutEuler", "rooe", 0, &status);
    eAttr.addField("xyz", 0);
    eAttr.addField("yzx", 1);
    eAttr.addField("zxy", 2);
    eAttr.addField("xzy", 3);
    eAttr.addField("yxz", 4);
    eAttr.addField("zyx", 5);
    INPUT_ATTR(eAttr);

    addAttribute(inOperation);
    addAttribute(inEuler1);
    addAttribute(inEuler1RotOrder);
    addAttribute(inEuler2);
    addAttribute(inEuler2RotOrder);
    addAttribute(inResRotOrder);
    addAttribute(outEuler);
    attributeAffects(inOperation, outEuler);
    attributeAffects(inEuler1, outEuler);
    attributeAffects(inEuler1RotOrder, outEuler);
    attributeAffects(inEuler2, outEuler);
    attributeAffects(inEuler2RotOrder, outEuler);
    attributeAffects(inResRotOrder, outEuler);

    return status;
}

MStatus EulerMath::compute(const MPlug& plug, MDataBlock& dataBlock){
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
    double3 &euler1 = dataBlock.inputValue(inEuler1).asDouble3();
    double3 &euler2 = dataBlock.inputValue(inEuler2).asDouble3();
    short euler1RotOrder = dataBlock.inputValue(inEuler1RotOrder).asShort();
    short euler2RotOrder = dataBlock.inputValue(inEuler2RotOrder).asShort();
    short outRotOrder = dataBlock.inputValue(inResRotOrder).asShort();

    MEulerRotation eEuler1 = MEulerRotation(
        euler1[0], 
        euler1[1],
        euler1[2],
        (MEulerRotation::RotationOrder) euler1RotOrder
    );
    MEulerRotation eEuler2 = MEulerRotation(
        euler2[0], 
        euler2[1],
        euler2[2],
        (MEulerRotation::RotationOrder) euler2RotOrder
    );

    MDataHandle outEulerHdle = dataBlock.outputValue(outEuler);
    MEulerRotation eOutEuler;

    switch (operation)
    {
    case 0:
        eEuler1.reorderIt((MEulerRotation::RotationOrder) outRotOrder);
        outEulerHdle.set3Double(eEuler1.x, eEuler1.y, eEuler1.z);
        break;
    case 1:
        eEuler1.reorderIt((MEulerRotation::RotationOrder) outRotOrder);
        eEuler2.reorderIt((MEulerRotation::RotationOrder) outRotOrder);
        eOutEuler = eEuler1 + eEuler2;
        outEulerHdle.set3Double(eOutEuler.x, eOutEuler.y, eOutEuler.z);
        break;
    case 2:
        eEuler1.reorderIt((MEulerRotation::RotationOrder) outRotOrder);
        eEuler2.reorderIt((MEulerRotation::RotationOrder) outRotOrder);
        eOutEuler = eEuler1 - eEuler2;
        outEulerHdle.set3Double(eOutEuler.x, eOutEuler.y, eOutEuler.z);
        break;
    case 3:
        eEuler1.reorderIt((MEulerRotation::RotationOrder) outRotOrder);
        eEuler2.reorderIt((MEulerRotation::RotationOrder) outRotOrder);
        eOutEuler = eEuler1 * eEuler2;
        outEulerHdle.set3Double(eOutEuler.x, eOutEuler.y, eOutEuler.z);
        break;
    }

    outEulerHdle.setClean();

    return MStatus::kSuccess;
}