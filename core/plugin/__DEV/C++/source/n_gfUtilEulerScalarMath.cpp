#include "n_gfUtilEulerScalarMath.h"


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
MObject EulerScalarMath::inEulerRotOrder;
MObject EulerScalarMath::inScalar;
MObject EulerScalarMath::inResRotOrder;
MObject EulerScalarMath::outEuler;


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

    MObject eulerX = uAttr.create("eulerX", "ex", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject eulerY = uAttr.create("eulerY", "ey", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject eulerZ = uAttr.create("eulerZ", "ez", MFnUnitAttribute::kAngle, 0.0, &status);
    inEuler = nAttr.create("euler", "e", eulerX, eulerY, eulerZ, &status);
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

    MObject outEulerX = uAttr.create("outEulerX", "oex", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject outEulerY = uAttr.create("outEulerY", "oey", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject outEulerZ = uAttr.create("outEulerZ", "oez", MFnUnitAttribute::kAngle, 0.0, &status);
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
    if (plug != outEuler)
        return MStatus::kUnknownParameter;
    short operation = dataBlock.inputValue(inOperation).asShort();
    MVector vEuler = dataBlock.inputValue(inEuler).asVector();
    double scalar = dataBlock.inputValue(inScalar).asDouble();
    short eulerRotOrder = dataBlock.inputValue(inEulerRotOrder).asShort();
    short outRotOrder = dataBlock.inputValue(inResRotOrder).asShort();

    MEulerRotation eEuler = EulerScalarMath::createMEulerRotation(vEuler, eulerRotOrder);

    MDataHandle outEulerHandle = dataBlock.outputValue(outEuler);
    MVector vResult, vScalar;
    MEulerRotation eOutEuler;

    switch (operation)
    {
    case 0:
        EulerScalarMath::reorderMEulerRotation(eEuler, outRotOrder);
        vResult = eEuler.asVector();
        outEulerHandle.setMVector(vResult);
        break;
    case 1:
        EulerScalarMath::reorderMEulerRotation(eEuler, outRotOrder);
        vScalar = MVector(
            MAngle(scalar, MAngle::kDegrees).asRadians(),
            MAngle(scalar, MAngle::kDegrees).asRadians(),
            MAngle(scalar, MAngle::kDegrees).asRadians()
        );
        vResult = eEuler.asVector() + vScalar;
        outEulerHandle.setMVector(vResult);
        break;
    case 2:
        EulerScalarMath::reorderMEulerRotation(eEuler, outRotOrder);
        vScalar = MVector(
            MAngle(scalar, MAngle::kDegrees).asRadians(),
            MAngle(scalar, MAngle::kDegrees).asRadians(),
            MAngle(scalar, MAngle::kDegrees).asRadians()
        );
        vResult = eEuler.asVector() - vScalar;
        outEulerHandle.setMVector(vResult);
        break;
    case 3:
        EulerScalarMath::reorderMEulerRotation(eEuler, outRotOrder);
        eOutEuler = eEuler * scalar;
        vResult = eOutEuler.asVector();
        outEulerHandle.setMVector(vResult);
        break;
    }

    outEulerHandle.setClean();

    return MStatus::kSuccess;
}

MEulerRotation EulerScalarMath::createMEulerRotation(MVector& value, short rotOrder){
    /*
    Create an MEulerRotation instance based on a double3 typed values and short typed
    rotation order.
    */
    MEulerRotation::RotationOrder order = MEulerRotation::kXYZ;
    switch (rotOrder)
    {
    case 0:
        order = MEulerRotation::kXYZ;
        break;
    case 1:
        order = MEulerRotation::kYZX;
        break;
    case 2:
        order = MEulerRotation::kZXY;
        break;
    case 3:
        order = MEulerRotation::kXZY;
        break;
    case 4:
        order = MEulerRotation::kYXZ;
        break;
    case 5:
        order = MEulerRotation::kZYX;
        break;
    }
    MEulerRotation eResult = MEulerRotation(value, order);
    return eResult;
}

void EulerScalarMath::reorderMEulerRotation(MEulerRotation& euler, short rotOrder){
    MEulerRotation::RotationOrder order;
    switch (rotOrder)
    {
    case 0:
        order = MEulerRotation::kXYZ;
        break;
    case 1:
        order = MEulerRotation::kYZX;
        break;
    case 2:
        order = MEulerRotation::kZXY;
        break;
    case 3:
        order = MEulerRotation::kXZY;
        break;
    case 4:
        order = MEulerRotation::kYXZ;
        break;
    case 5:
        order = MEulerRotation::kZYX;
        break;
    }
    euler.reorderIt(order);
}