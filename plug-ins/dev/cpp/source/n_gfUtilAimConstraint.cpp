#include "headers/n_gfUtilAimConstraint.h"

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
AimConstraint::AimConstraint(){}

// Destructor.
AimConstraint::~AimConstraint(){}

MObject AimConstraint::inUpVecType;
MObject AimConstraint::inOffset;
MObject AimConstraint::inWorldUpVector;
MObject AimConstraint::inWorldUpMtx;
MObject AimConstraint::inTargetWMtx;
MObject AimConstraint::inTargetWeight;
MObject AimConstraint::inConstWMtx;
MObject AimConstraint::inConstParInvMtx;
MObject AimConstraint::inConstJntOri;
MObject AimConstraint::inConstRotOrder;
MObject AimConstraint::inConstParSca;
MObject AimConstraint::outConstraint;

void* AimConstraint::creator(){
    // Maya creator function.
    return new AimConstraint();
}

MStatus AimConstraint::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to BlendTransform class. Instances of BlendTransform will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnEnumAttribute eAttr;
    MFnMatrixAttribute mAttr;
    MFnNumericAttribute nAttr;
    MFnUnitAttribute uAttr;

    inUpVecType = eAttr.create("upVectorType", "upt", 0, &status);
    eAttr.addField("World Up", 0);
    eAttr.addField("Object Up", 1);
    INPUT_ATTR(eAttr);

    MObject offsetX = uAttr.create("offsetX", "offsetX", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject offsetY = uAttr.create("offsetY", "offsetY", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject offsetZ = uAttr.create("offsetZ", "offsetZ", MFnUnitAttribute::kAngle, 0.0, &status);
    inOffset = nAttr.create("offset", "offset", offsetX, offsetY, offsetZ, &status);
    INPUT_ATTR(nAttr);

    inWorldUpVector = nAttr.createPoint("worldUpVector", "wuv", &status);
    nAttr.setDefault(0.0f, 1.0f, 0.0f);
    INPUT_ATTR(nAttr);

    inWorldUpMtx = mAttr.create("worldUpMatrix", "wum", MFnMatrixAttribute::kFloat, &status);
    INPUT_ATTR(mAttr);

    inTargetWMtx = mAttr.create("targetWorldMatrix", "twmtx", MFnMatrixAttribute::kFloat, &status);
    INPUT_ATTR(mAttr);

    inTargetWeight = nAttr.create("targetWeight", "tw", MFnNumericData::kDouble, 1.0, &status);
    INPUT_ATTR(nAttr);

    inConstWMtx = mAttr.create("constraintWorldMatrix", "cwmtx", MFnMatrixAttribute::kFloat, &status);
    INPUT_ATTR(mAttr);

    inConstParInvMtx = mAttr.create("constraintParentInverseMatrix", "cpim", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    MObject jntOriX = uAttr.create("constraintJointOrientX", "cjorx", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject jntOriY = uAttr.create("constraintJointOrientY", "cjory", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject jntOriZ = uAttr.create("constraintJointOrientZ", "cjorz", MFnUnitAttribute::kAngle, 0.0, &status);
    inConstJntOri = nAttr.create("constraintJointOrient", "cjor", jntOriX, jntOriY, jntOriZ, &status);
    INPUT_ATTR(nAttr);

    inConstRotOrder = eAttr.create("constraintRotateOrder", "cro", 0, &status);
    eAttr.addField("xyz", 0);
    eAttr.addField("yzx", 1);
    eAttr.addField("zxy", 2);
    eAttr.addField("xzy", 3);
    eAttr.addField("yxz", 4);
    eAttr.addField("zyx", 5);
    INPUT_ATTR(eAttr);

    inConstParSca = nAttr.createPoint("constraintParentScale", "cps");
    nAttr.setDefault(1.0f, 1.0f, 1.0f);
    INPUT_ATTR(nAttr);

    MObject outConstraintX = uAttr.create("contraintX", "cx", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject outConstraintY = uAttr.create("contraintY", "cy", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject outConstraintZ = uAttr.create("contraintZ", "cz", MFnUnitAttribute::kAngle, 0.0, &status);
    outConstraint = nAttr.create("contraint", "const", outConstraintX, outConstraintY, outConstraintZ, &status);
    OUTPUT_ATTR(nAttr);

    addAttribute(inUpVecType);
    addAttribute(inOffset);
    addAttribute(inWorldUpVector);
    addAttribute(inWorldUpMtx);
    addAttribute(inTargetWMtx);
    addAttribute(inTargetWeight);
    addAttribute(inConstWMtx);
    addAttribute(inConstParInvMtx);
    addAttribute(inConstJntOri);
    addAttribute(inConstRotOrder);
    addAttribute(inConstParSca);
    addAttribute(outConstraint);
    attributeAffects(inUpVecType, outConstraint);
    attributeAffects(inOffset, outConstraint);
    attributeAffects(inWorldUpVector, outConstraint);
    attributeAffects(inWorldUpMtx, outConstraint);
    attributeAffects(inTargetWMtx, outConstraint);
    attributeAffects(inTargetWeight, outConstraint);
    attributeAffects(inConstWMtx, outConstraint);
    attributeAffects(inConstParInvMtx, outConstraint);
    attributeAffects(inConstJntOri, outConstraint);
    attributeAffects(inConstRotOrder, outConstraint);
    attributeAffects(inConstParSca, outConstraint);

    return status;
}

MStatus AimConstraint::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outConstraint)
        return MStatus::kUnknownParameter;

    short upVecType = dataBlock.inputValue(inUpVecType).asShort();
    MEulerRotation eOffset = MEulerRotation(dataBlock.inputValue(inOffset).asDouble3());
    MFloatMatrix mTargetWorld = dataBlock.inputValue(inTargetWMtx).asFloatMatrix();
    double targetWeight = dataBlock.inputValue(inTargetWeight).asDouble();
    MFloatMatrix mConstWorld = dataBlock.inputValue(inConstWMtx).asFloatMatrix();
    MMatrix mConstParInv = dataBlock.inputValue(inConstParInvMtx).asMatrix();
    MEulerRotation eConstJntOri = MEulerRotation(dataBlock.inputValue(inConstJntOri).asDouble3());
    short constRotOrder = dataBlock.inputValue(inConstRotOrder).asShort();
    MFloatVector vConstParSca = dataBlock.inputValue(inConstParSca).asFloatVector();

    double constParSca[3] = {vConstParSca.x, vConstParSca.y, vConstParSca.z};

    MFloatVector vTargetPos = MFloatVector(mTargetWorld[3][0], mTargetWorld[3][1], mTargetWorld[3][2]);
    MFloatVector vConstPos = MFloatVector(mConstWorld[3][0], mConstWorld[3][1], mConstWorld[3][2]);
    MFloatVector nAim = vTargetPos - vConstPos;
    nAim.normalize();
    MFloatVector nNormal, nBinormal;
    if (upVecType == 0){
        MFloatVector nWorldUp = dataBlock.inputValue(inWorldUpVector).asFloatVector();
        nWorldUp.normalize();
        nBinormal = nWorldUp ^ nAim;
        nBinormal.normalize();
        nNormal = nAim ^ nBinormal;
        nNormal.normalize();
    }
    else if (upVecType == 1){
        MFloatMatrix mWorldUp = dataBlock.inputValue(inWorldUpMtx).asFloatMatrix();
        MFloatVector vWorldUp = MFloatVector(mWorldUp[3][0], mWorldUp[3][1], mWorldUp[3][2]);
        nNormal = vWorldUp - vConstPos;
        nNormal.normalize();
        nBinormal = nAim ^ nNormal;
        nBinormal.normalize();
    }
    float aim[4][4] = {
        {nAim.x, nAim.y, nAim.z, 0.0f},
        {nNormal.x, nNormal.y, nNormal.z, 0.0f},
        {nBinormal.x, nBinormal.y, nBinormal.z, 0.0f},
        {0.0f, 0.0f, 0.0f, 1.0f}
    };
    MMatrix mAim = MMatrix(aim);
    MTransformationMatrix mtxFn = MTransformationMatrix();
    mtxFn.addScale(constParSca, MSpace::kTransform);
    MMatrix mInvSca = mtxFn.asMatrix();
    mtxFn = MTransformationMatrix();
    mtxFn.rotateBy(eConstJntOri, MSpace::kTransform);
    MMatrix mConstJntOri = mtxFn.asMatrix();
    mtxFn = MTransformationMatrix();
    mtxFn.rotateBy(eOffset.invertIt(), MSpace::kTransform);
    MMatrix mOffset = mtxFn.asMatrix();
    MMatrix mResult = mOffset * mAim * mConstParInv * mInvSca * mConstJntOri.inverse();
    MEulerRotation eConstraint = MTransformationMatrix(mResult).eulerRotation();
    eConstraint.reorderIt((MEulerRotation::RotationOrder)constRotOrder);
    eConstraint *= targetWeight;
    MVector vConstraint = eConstraint.asVector();
    MDataHandle outConstraintHandle = dataBlock.outputValue(outConstraint);
    outConstraintHandle.setMVector(vConstraint);
    outConstraintHandle.setClean();

    return MStatus::kSuccess;
}
