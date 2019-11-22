#include "headers/n_gfUtilParentConstraint.h"

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
ParentConstraint::ParentConstraint() {}

// Destructor.
ParentConstraint::~ParentConstraint() {}

MObject ParentConstraint::inConstraintJntOri;
MObject ParentConstraint::inConstraintRotOrder;
MObject ParentConstraint::inConstraintParInvMtx;
MObject ParentConstraint::inConstraintParSca;
MObject ParentConstraint::inTargetWorldMatrix;
MObject ParentConstraint::inTargetOffset;
MObject ParentConstraint::inTargetWeight;
MObject ParentConstraint::inTargetList;
MObject ParentConstraint::outConstTrans;
MObject ParentConstraint::outConstRot;
MObject ParentConstraint::outConstSca;


void* ParentConstraint::creator(){
    // Maya creator function.
    return new ParentConstraint();
}

MStatus ParentConstraint::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to ParentConstraint class. Instances of ParentConstraint will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnMatrixAttribute mAttr;
    MFnNumericAttribute nAttr;
    MFnUnitAttribute uAttr;
    MFnEnumAttribute eAttr;
    MFnCompoundAttribute cAttr;

    MObject constJntOriX = uAttr.create("constraintJointOrientX", "cjorx", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject constJntOriY = uAttr.create("constraintJointOrientY", "cjory", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject constJntOriZ = uAttr.create("constraintJointOrientZ", "cjorz", MFnUnitAttribute::kAngle, 0.0, &status);
    inConstraintJntOri = nAttr.create("constraintJointOrient", "cjor", constJntOriX, constJntOriY, constJntOriZ, &status);
    INPUT_ATTR(nAttr);

    inConstraintRotOrder = eAttr.create("constraintRotateOrder", "croo", 0, &status);
    eAttr.addField("xyz", 0);
    eAttr.addField("yzx", 1);
    eAttr.addField("zxy", 2);
    eAttr.addField("xzy", 3);
    eAttr.addField("yxz", 4);
    eAttr.addField("zyx", 5);
    INPUT_ATTR(eAttr);

    inConstraintParInvMtx = mAttr.create("constraintParentInverseMatrix", "cpim", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inConstraintParSca = nAttr.createPoint("constraintParentScale", "cps", &status);
    nAttr.setDefault(1.0, 1.0, 1.0);
    INPUT_ATTR(nAttr);

    inTargetWorldMatrix = mAttr.create("targetWorldMatrix", "twmtx", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inTargetOffset = mAttr.create("targetOffset", "toff", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inTargetWeight = nAttr.create("targetWeight", "twght", MFnNumericData::kDouble, 1.0, &status);
    INPUT_ATTR(nAttr);

    inTargetList = cAttr.create("targetList", "tlist", &status);
    cAttr.addChild(inTargetWorldMatrix);
    cAttr.addChild(inTargetOffset);
    cAttr.addChild(inTargetWeight);
    cAttr.setArray(true);

    outConstTrans = nAttr.createPoint("constraintTranslate", "ctrans", &status);
    OUTPUT_ATTR(nAttr);

    MObject outConstRotX = uAttr.create("constraintRotateX", "crox", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject outConstRotY = uAttr.create("constraintRotateY", "croy", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject outConstRotZ = uAttr.create("constraintRotateZ", "croz", MFnUnitAttribute::kAngle, 0.0, &status);
    outConstRot = nAttr.create("constraintRotate", "cro", outConstRotX, outConstRotY, outConstRotZ, &status);
    OUTPUT_ATTR(nAttr);

    outConstSca = nAttr.createPoint("constraintScale", "csca", &status);
    nAttr.setDefault(1.0, 1.0, 1.0);
    OUTPUT_ATTR(nAttr);

    addAttribute(inConstraintJntOri);
    addAttribute(inConstraintRotOrder);
    addAttribute(inConstraintParInvMtx);
    addAttribute(inConstraintParSca);
    addAttribute(inTargetList);
    addAttribute(outConstTrans);
    addAttribute(outConstRot);
    addAttribute(outConstSca);
    attributeAffects(inConstraintJntOri, outConstTrans);
    attributeAffects(inConstraintRotOrder, outConstTrans);
    attributeAffects(inConstraintParInvMtx, outConstTrans);
    attributeAffects(inConstraintParSca, outConstTrans);
    attributeAffects(inTargetWorldMatrix, outConstTrans);
    attributeAffects(inTargetOffset, outConstTrans);
    attributeAffects(inTargetWeight, outConstTrans);
    attributeAffects(inConstraintJntOri, outConstRot);
    attributeAffects(inConstraintRotOrder, outConstRot);
    attributeAffects(inConstraintParInvMtx, outConstRot);
    attributeAffects(inConstraintParSca, outConstRot);
    attributeAffects(inTargetWorldMatrix, outConstRot);
    attributeAffects(inTargetOffset, outConstRot);
    attributeAffects(inTargetWeight, outConstRot);
    attributeAffects(inConstraintJntOri, outConstSca);
    attributeAffects(inConstraintRotOrder, outConstSca);
    attributeAffects(inConstraintParInvMtx, outConstSca);
    attributeAffects(inConstraintParSca, outConstSca);
    attributeAffects(inTargetWorldMatrix, outConstSca);
    attributeAffects(inTargetOffset, outConstSca);
    attributeAffects(inTargetWeight, outConstSca);

    return status;
}

MStatus ParentConstraint::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    MEulerRotation eConstJntOri = MEulerRotation(dataBlock.inputValue(inConstraintJntOri).asDouble3());
    MMatrix mConstParInv = dataBlock.inputValue(inConstraintParInvMtx).asMatrix();
    short constRotOrder = dataBlock.inputValue(inConstraintRotOrder).asShort();
    float3& constParSca = dataBlock.inputValue(inConstraintParSca).asFloat3();
    MArrayDataHandle targetListHandle = dataBlock.inputArrayValue(inTargetList);

    MMatrix mTargetsAdded = MMatrix();
    MTransformationMatrix mtxFn = MTransformationMatrix();
    double constParScaD[3] = {constParSca[0], constParSca[1], constParSca[2]};
    mtxFn.addScale(constParScaD, MSpace::kTransform);
    MMatrix mInvSca = mtxFn.asMatrix();
    MMatrix mTarget;

    for (uint32_t i = 0; i < targetListHandle.elementCount(); i++){
        targetListHandle.jumpToArrayElement(i);
        MDataHandle targetHandle = targetListHandle.inputValue();
        MMatrix mTargetW = targetHandle.child(inTargetWorldMatrix).asMatrix();
        MMatrix mOffset = targetHandle.child(inTargetOffset).asMatrix();
        double targetWeight = targetHandle.child(inTargetWeight).asDouble();

        mTarget = mOffset * (mTargetW * targetWeight);
        if (mTargetsAdded == MMatrix())
            mTargetsAdded = mTarget;
        else
            mTargetsAdded += mTarget;
    }

    MMatrix mResult = mTargetsAdded * mConstParInv * mInvSca;

    {
        MString toPrint = MString("mTargetsAdded = ");
        toPrint += mTargetsAdded[3][0];
        toPrint += ", ";
        toPrint += mTargetsAdded[3][1];
        toPrint += ", ";
        toPrint += mTargetsAdded[3][2];
        MGlobal::displayInfo(toPrint);
    }

    {
        MString toPrint = MString("mConstParInv = ");
        toPrint += mConstParInv[3][0];
        toPrint += ", ";
        toPrint += mConstParInv[3][1];
        toPrint += ", ";
        toPrint += mConstParInv[3][2];
        MGlobal::displayInfo(toPrint);
    }

    {
        MString toPrint = MString("mInvSca = ");
        toPrint += mInvSca[0][0];
        toPrint += ", ";
        toPrint += mInvSca[1][1];
        toPrint += ", ";
        toPrint += mInvSca[2][2];
        MGlobal::displayInfo(toPrint);
    }

    {
        MString toPrint = MString("mResult = ");
        toPrint += mResult[3][0];
        toPrint += ", ";
        toPrint += mResult[3][1];
        toPrint += ", ";
        toPrint += mResult[3][2];
        MGlobal::displayInfo(toPrint);
    }

    if (plug == outConstTrans){
        MDataHandle outTransHandle = dataBlock.outputValue(outConstTrans);
        MVector outTrans = MVector(mResult[3][0], mResult[3][1], mResult[3][2]);
        {
            MString toPrint = MString("outTrans = ");
            toPrint += outTrans.x;
            toPrint += ", ";
            toPrint += outTrans.y;
            toPrint += ", ";
            toPrint += outTrans.z;
            MGlobal::displayInfo(toPrint);
        }
        outTransHandle.setMFloatVector(outTrans);
        outTransHandle.setClean();
    }
    if (plug == outConstRot){
        MDataHandle outRotHandle = dataBlock.outputValue(outConstRot);
        mtxFn = MTransformationMatrix(mResult);
        MEulerRotation eRotMtx = mtxFn.eulerRotation();
        MQuaternion qRotMtx = eRotMtx.asQuaternion();
        MQuaternion qConstJntOri = eConstJntOri.asQuaternion();
        MQuaternion qOutRot = qRotMtx * qConstJntOri.invertIt();
        MEulerRotation outRot = qOutRot.asEulerRotation().reorderIt((MEulerRotation::RotationOrder)constRotOrder);
        outRotHandle.setMVector(outRot.asVector());
        outRotHandle.setClean();
    }
    if (plug == outConstSca){
        MDataHandle outScaHandle = dataBlock.outputValue(outConstSca);
        mtxFn = MTransformationMatrix(mResult);
        double sca[3];
        mtxFn.getScale(sca, MSpace::kWorld);
        MVector outSca = MVector(sca[0], sca[1], sca[2]);
        outScaHandle.setMFloatVector(outSca);
        outScaHandle.setClean();
    }

    return MStatus::kSuccess;
}