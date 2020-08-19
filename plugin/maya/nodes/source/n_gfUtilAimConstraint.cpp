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
MObject AimConstraint::inAngleUp;
MObject AimConstraint::inTargetWMtx;
MObject AimConstraint::inTargetWeight;
MObject AimConstraint::inConstWMtx;
MObject AimConstraint::inConstParInvMtx;
MObject AimConstraint::inConstJntOri;
MObject AimConstraint::inConstRotOrder;
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
    eAttr.addField("None", 0);
    eAttr.addField("World Up", 1);
    eAttr.addField("Object Up", 2);
    eAttr.addField("Angle Up", 3);
    INPUT_ATTR(eAttr);
    eAttr.setChannelBox(true);

    MObject offsetX = uAttr.create("offsetX", "offsetX", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject offsetY = uAttr.create("offsetY", "offsetY", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject offsetZ = uAttr.create("offsetZ", "offsetZ", MFnUnitAttribute::kAngle, 0.0, &status);
    inOffset = nAttr.create("offset", "offset", offsetX, offsetY, offsetZ, &status);
    INPUT_ATTR(nAttr);

    inWorldUpVector = nAttr.createPoint("worldUpVector", "wuv", &status);
    nAttr.setDefault(0.0f, 1.0f, 0.0f);
    INPUT_ATTR(nAttr);

    inAngleUp = uAttr.create("angleUp", "angle", MFnUnitAttribute::kAngle, 0.0, &status);
    uAttr.setMin(0.0);
    uAttr.setMax(2.0 * M_PI);
    INPUT_ATTR(uAttr);

    inWorldUpMtx = mAttr.create("worldUpMatrix", "wum", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inTargetWMtx = mAttr.create("targetWorldMatrix", "twmtx", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inTargetWeight = nAttr.create("targetWeight", "tw", MFnNumericData::kDouble, 1.0, &status);
    INPUT_ATTR(nAttr);

    inConstWMtx = mAttr.create("constraintWorldMatrix", "cwmtx", MFnMatrixAttribute::kDouble, &status);
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

    MObject outConstraintX = uAttr.create("contraintX", "cx", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject outConstraintY = uAttr.create("contraintY", "cy", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject outConstraintZ = uAttr.create("contraintZ", "cz", MFnUnitAttribute::kAngle, 0.0, &status);
    outConstraint = nAttr.create("contraint", "const", outConstraintX, outConstraintY, outConstraintZ, &status);
    OUTPUT_ATTR(nAttr);

    addAttribute(inUpVecType);
    addAttribute(inOffset);
    addAttribute(inWorldUpVector);
    addAttribute(inWorldUpMtx);
    addAttribute(inAngleUp);
    addAttribute(inTargetWMtx);
    addAttribute(inTargetWeight);
    addAttribute(inConstWMtx);
    addAttribute(inConstParInvMtx);
    addAttribute(inConstJntOri);
    addAttribute(inConstRotOrder);
    addAttribute(outConstraint);
    attributeAffects(inUpVecType, outConstraint);
    attributeAffects(inOffset, outConstraint);
    attributeAffects(inWorldUpVector, outConstraint);
    attributeAffects(inWorldUpMtx, outConstraint);
    attributeAffects(inAngleUp, outConstraint);
    attributeAffects(inTargetWMtx, outConstraint);
    attributeAffects(inTargetWeight, outConstraint);
    attributeAffects(inConstWMtx, outConstraint);
    attributeAffects(inConstParInvMtx, outConstraint);
    attributeAffects(inConstJntOri, outConstraint);
    attributeAffects(inConstRotOrder, outConstraint);

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
    MQuaternion qOffset = eOffset.asQuaternion();
    MMatrix mTargetW = dataBlock.inputValue(inTargetWMtx).asMatrix();
    double targetWeight = dataBlock.inputValue(inTargetWeight).asDouble();
    MMatrix mConstW = dataBlock.inputValue(inConstWMtx).asMatrix();
    MMatrix mConstParInv = dataBlock.inputValue(inConstParInvMtx).asMatrix();
    MEulerRotation eConstJntOri = MEulerRotation(dataBlock.inputValue(inConstJntOri).asDouble3());
    MQuaternion qConstJntOri = eConstJntOri.asQuaternion();
    short constRotOrder = dataBlock.inputValue(inConstRotOrder).asShort();

    MVector vTarget = MVector(mTargetW[3][0], mTargetW[3][1], mTargetW[3][2]);
    MVector vConst = MVector(mConstW[3][0], mConstW[3][1], mConstW[3][2]);
    MTransformationMatrix mtxFn = MTransformationMatrix(mConstParInv);
    MQuaternion qConstParInv = mtxFn.rotation();

    MVector primAxis = MVector::xAxis;
    MVector secAxis = MVector::yAxis;
    MQuaternion qAimConst = MQuaternion();

    MVector nAim = vTarget - vConst;
    nAim.normalize();
    MQuaternion qAim = MQuaternion(primAxis, nAim);
    qAimConst *= qAim;

    if (upVecType != 0){
        MVector vUp;
        if (upVecType == 1){
            MVector nWorldUp = MVector(dataBlock.inputValue(inWorldUpVector).asFloat3());
            nWorldUp.normalize();
            vUp = nWorldUp;
        }
        else if (upVecType == 2){
            MMatrix mWorldUp = dataBlock.inputValue(inWorldUpMtx).asMatrix();
            MVector vWorldUp = MVector(mWorldUp[3][0], mWorldUp[3][1], mWorldUp[3][2]);
            vUp = vWorldUp - vConst;
        }
        else if (upVecType == 3){
            double angleUp = dataBlock.inputValue(inAngleUp).asAngle().asRadians();
            MQuaternion qTwist = MQuaternion(angleUp, nAim);
            vUp = secAxis.rotateBy(qTwist);
        }
        MVector nNormal = vUp - ((vUp * nAim) * nAim);
        nNormal.normalize();

        MVector nUp = secAxis.rotateBy(qAim);
        double angle = nUp.angle(nNormal);
        MQuaternion qNormal = MQuaternion(angle, nAim);
        if (!nNormal.isEquivalent(nUp.rotateBy(qNormal), 1.0e-5)){
            angle = 2.0 * M_PI - angle;
            qNormal = MQuaternion(angle, nAim);
        }
        qAimConst *= qNormal;
    }

    MQuaternion qResult = MQuaternion();
    qResult *= qOffset.invertIt();
    qResult *= qAimConst;
    qResult *= qConstParInv;
    qResult *= qConstJntOri.invertIt();
    MEulerRotation eResult = qResult.asEulerRotation();
    eResult.reorderIt((MEulerRotation::RotationOrder)constRotOrder);
    eResult *= targetWeight;
    MVector vResult = eResult.asVector();
    MDataHandle outConstraintHandle = dataBlock.outputValue(outConstraint);
    outConstraintHandle.setMVector(vResult);
    outConstraintHandle.setClean();

    return MStatus::kSuccess;
}
