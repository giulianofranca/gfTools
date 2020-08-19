#include "headers/n_gfRigHelperJoint.h"

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
HelperJoint::HelperJoint() {}

// Destructor.
HelperJoint::~HelperJoint() {}

MObject HelperJoint::inSource;
MObject HelperJoint::inSourceParent;
MObject HelperJoint::inParInvMtx;
MObject HelperJoint::inSourceParSca;
MObject HelperJoint::inPositionOffset;
MObject HelperJoint::inRotationOffset;
MObject HelperJoint::inRotAngle;
MObject HelperJoint::inRestAngle;
MObject HelperJoint::inRotInterp;
MObject HelperJoint::inPosMult;
MObject HelperJoint::inNegMult;
MObject HelperJoint::inTargetList;
MObject HelperJoint::outTransform;

void* HelperJoint::creator(){
    // Maya creator function.
    return new HelperJoint();
}

MStatus HelperJoint::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to HelperJoint class. Instances of HelperJoint will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnNumericAttribute nAttr;
    MFnMatrixAttribute mAttr;
    MFnUnitAttribute uAttr;
    MFnCompoundAttribute cAttr;

    inSource = mAttr.create("source", "s", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inSourceParent = mAttr.create("sourceParent", "sp", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inParInvMtx = mAttr.create("targetParentInverseMatrix", "tpimtx", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inSourceParSca = nAttr.createPoint("sourceParentScale", "spsca", &status);
    nAttr.setDefault(1.0, 1.0, 1.0);
    INPUT_ATTR(nAttr)

    inPositionOffset = nAttr.createPoint("positionOffset", "posoff", &status);
    INPUT_ATTR(nAttr);

    MObject rotOffX = uAttr.create("rotationOffsetX", "rotoffx", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject rotOffY = uAttr.create("rotationOffsetY", "rotoffy", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject rotOffZ = uAttr.create("rotationOffsetZ", "rotoffz", MFnUnitAttribute::kAngle, 0.0, &status);
    inRotationOffset = nAttr.create("rotationOffset", "rotoff", rotOffX, rotOffY, rotOffZ, &status);
    INPUT_ATTR(nAttr);

    inRotAngle = uAttr.create("rotationAngle", "rotangle", MFnUnitAttribute::kAngle, 0.0, &status);
    INPUT_ATTR(uAttr);

    inRestAngle = uAttr.create("restAngle", "rang", MFnUnitAttribute::kAngle, 0.0, &status);
    INPUT_ATTR(uAttr);

    inRotInterp = nAttr.create("rotationInterpolation", "roti", MFnNumericData::kFloat, 0.5f, &status);
    nAttr.setMin(0.0f);
    nAttr.setMax(1.0f);
    INPUT_ATTR(nAttr);

    inPosMult = nAttr.create("positiveMultiplier", "posmult", MFnNumericData::kFloat, 0.0f, &status);
    INPUT_ATTR(nAttr);

    inNegMult = nAttr.create("negativeMultiplier", "negmult", MFnNumericData::kFloat, 0.0f, &status);
    INPUT_ATTR(nAttr);

    inTargetList = cAttr.create("targetList", "tgtl", &status);
    cAttr.addChild(inPositionOffset);
    cAttr.addChild(inRotationOffset);
    cAttr.addChild(inRotAngle);
    cAttr.addChild(inRestAngle);
    cAttr.addChild(inRotInterp);
    cAttr.addChild(inPosMult);
    cAttr.addChild(inNegMult);
    cAttr.setArray(true);

    outTransform = mAttr.create("outTransform", "outtrans", MFnMatrixAttribute::kDouble, &status);
    mAttr.setArray(true);
    OUTPUT_ATTR(mAttr);

    addAttribute(inSource);
    addAttribute(inSourceParent);
    addAttribute(inParInvMtx);
    addAttribute(inSourceParSca);
    addAttribute(inTargetList);
    addAttribute(outTransform);
    attributeAffects(inSource, outTransform);
    attributeAffects(inSourceParent, outTransform);
    attributeAffects(inParInvMtx, outTransform);
    attributeAffects(inSourceParSca, outTransform);
    attributeAffects(inPositionOffset, outTransform);
    attributeAffects(inRotationOffset, outTransform);
    attributeAffects(inRotAngle, outTransform);
    attributeAffects(inRestAngle, outTransform);
    attributeAffects(inRotInterp, outTransform);
    attributeAffects(inPosMult, outTransform);
    attributeAffects(inNegMult, outTransform);

    return status;
}

MStatus HelperJoint::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outTransform)
        return MStatus::kUnknownParameter;

    MMatrix mSource = dataBlock.inputValue(inSource).asMatrix();
    MTransformationMatrix mtxFn = MTransformationMatrix(mSource);
    double neutralSca[3] = {1.0, 1.0, 1.0};
    mtxFn.setScale(neutralSca, MSpace::kTransform);
    mSource = mtxFn.asMatrix();
    MMatrix mSourceParent = dataBlock.inputValue(inSourceParent).asMatrix();

    MMatrix mParInv = dataBlock.inputValue(inParInvMtx).asMatrix();
    float3& sourceParSca = dataBlock.inputValue(inSourceParSca).asFloat3();
    double sourceParScaD[3] = {sourceParSca[0], sourceParSca[1], sourceParSca[2]};
    mtxFn = MTransformationMatrix();
    mtxFn.addScale(sourceParScaD, MSpace::kTransform);
    MMatrix mInvSca = mtxFn.asMatrix();
    MArrayDataHandle targetListHandle = dataBlock.inputArrayValue(inTargetList);

    std::vector<MMatrix> outputList;

    for (uint32_t i = 0; i < targetListHandle.elementCount(); i++){
        targetListHandle.jumpToArrayElement(i);
        MDataHandle targetHandle = targetListHandle.inputValue();
        MVector vPosOffset = MVector(targetHandle.child(inPositionOffset).asFloat3());
        MEulerRotation eRotOffset = MEulerRotation(targetHandle.child(inRotationOffset).asDouble3());
        double angle = targetHandle.child(inRotAngle).asAngle().asRadians();
        double restAngle = targetHandle.child(inRestAngle).asAngle().asRadians();
        float rotInterp = targetHandle.child(inRotInterp).asFloat();
        float posMult = targetHandle.child(inPosMult).asFloat();
        float negMult = targetHandle.child(inNegMult).asFloat();

        MMatrix mPositionOffset = MMatrix();
        mPositionOffset[3][0] = vPosOffset.x;
        mPositionOffset[3][1] = vPosOffset.y;
        mPositionOffset[3][2] = vPosOffset.z;
        double multTranslation = abs(angle) * posMult;
        if (angle < restAngle)
            multTranslation = abs(angle) * negMult;
        vPosOffset.normalize();
        MMatrix mMultiplier = MMatrix();
        mMultiplier[3][0] = vPosOffset.x * multTranslation;
        mMultiplier[3][1] = vPosOffset.y * multTranslation;
        mMultiplier[3][2] = vPosOffset.z * multTranslation;
        MMatrix mTargetPoint = mMultiplier * mPositionOffset * mSource;
        MMatrix mTargetOrient = mInvSca * (mSource * (double)(1.0f - rotInterp)) + (mSourceParent * rotInterp);

        MVector vResultPos = MVector(mTargetPoint[3][0], mTargetPoint[3][1], mTargetPoint[3][2]);
        mtxFn = MTransformationMatrix(mTargetOrient);
        MEulerRotation eResultOri = eRotOffset + mtxFn.eulerRotation();
        mtxFn = MTransformationMatrix();
        mtxFn.rotateTo(eResultOri);
        mtxFn.setTranslation(vResultPos, MSpace::kTransform);
        MMatrix mResult = mtxFn.asMatrix() * mParInv;
        outputList.push_back(mResult);
    }

    MArrayDataHandle outTransHandle = dataBlock.outputArrayValue(outTransform);
    for (uint32_t i = 0; i < outTransHandle.elementCount(); i++){
        outTransHandle.jumpToArrayElement(i);
        MDataHandle resultHandle = outTransHandle.outputValue();
        if (i < outTransHandle.elementCount() && i < outputList.size())
            resultHandle.setMMatrix(outputList[i]);
        else
            resultHandle.setMMatrix(MMatrix::identity);
    }

    outTransHandle.setAllClean();

    return MStatus::kSuccess;
}