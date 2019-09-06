#include "n_gfUtilAimConstraint.h"

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
MObject AimConstraint::inTarget;
MObject AimConstraint::inWorldUp;
MObject AimConstraint::inUpObj;
MObject AimConstraint::inPivot;
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

    inTarget = mAttr.create("target", "target", MFnMatrixAttribute::kFloat, &status);
    INPUT_ATTR(mAttr);

    inUpObj = mAttr.create("up", "up", MFnMatrixAttribute::kFloat, &status);
    INPUT_ATTR(mAttr);

    inWorldUp = nAttr.createPoint("worldUp", "wu", &status);
    nAttr.setDefault(0.0f, 1.0f, 0.0f);
    INPUT_ATTR(nAttr);

    inPivot = mAttr.create("pivot", "pivot", MFnMatrixAttribute::kFloat, &status);
    INPUT_ATTR(mAttr);

    MObject outConstraintX = uAttr.create("contraintX", "cx", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject outConstraintY = uAttr.create("contraintY", "cy", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject outConstraintZ = uAttr.create("contraintZ", "cz", MFnUnitAttribute::kAngle, 0.0, &status);
    outConstraint = nAttr.create("contraint", "const", outConstraintX, outConstraintY, outConstraintZ, &status);
    OUTPUT_ATTR(nAttr);

    addAttribute(inUpVecType);
    addAttribute(inTarget);
    addAttribute(inUpObj);
    addAttribute(inWorldUp);
    addAttribute(inPivot);
    addAttribute(outConstraint);
    attributeAffects(inUpVecType, outConstraint);
    attributeAffects(inTarget, outConstraint);
    attributeAffects(inUpObj, outConstraint);
    attributeAffects(inWorldUp, outConstraint);
    attributeAffects(inPivot, outConstraint);

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

    short upType = dataBlock.inputValue(inUpVecType).asShort();
    MFloatMatrix mTarget = dataBlock.inputValue(inTarget).asFloatMatrix();
    MFloatMatrix mPivot = dataBlock.inputValue(inPivot).asFloatMatrix();
    MFloatVector vTarget = MFloatVector(mTarget[3][0], mTarget[3][1], mTarget[3][2]);
    MFloatVector vPivot = MFloatVector(mPivot[3][0], mPivot[3][1], mPivot[3][2]);
    MFloatVector vAim = vTarget - vPivot;
    MFloatVector nAim = vAim.normal();
    MFloatVector nNormal;
    MFloatVector nBinormal;
    if (upType == 0){
        MFloatVector vWorldUp = dataBlock.inputValue(inWorldUp).asFloatVector();
        MFloatVector nWorldUp = vWorldUp.normal();
        nBinormal = nAim ^ -nWorldUp;
        nNormal = nAim ^ nBinormal;
    }
    else if (upType == 1){
        MFloatMatrix mUpObj = dataBlock.inputValue(inUpObj).asFloatMatrix();
        MFloatVector vUpObj = MFloatVector(mUpObj[3][0], mUpObj[3][1], mUpObj[3][2]);
        MFloatVector vNormal = vUpObj - vPivot;
        nNormal = vNormal.normal();
        nBinormal = nAim ^ nNormal;
    }
    float aim[4][4] = {
        {nAim.x, nAim.y, nAim.z, 0.0f},
        {nNormal.x, nNormal.y, nNormal.z, 0.0f},
        {nBinormal.x, nBinormal.y, nBinormal.z, 0.0f},
        {0.0f, 0.0f, 0.0f, 1.0f}
    };
    MMatrix mAim = MMatrix(aim);
    MTransformationMatrix mtxFn = MTransformationMatrix(mAim);
    MVector eAim = mtxFn.rotation().asEulerRotation().asVector();
    MDataHandle outConstraintHandle = dataBlock.outputValue(outConstraint);
    outConstraintHandle.setMVector(eAim);
    outConstraintHandle.setClean();

    return MStatus::kSuccess;
}