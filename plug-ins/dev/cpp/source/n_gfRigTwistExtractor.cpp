#include "headers/n_gfRigTwistExtractor.h"

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
TwistExtractor::TwistExtractor() {}

// Destructor.
TwistExtractor::~TwistExtractor() {}

MObject TwistExtractor::inTargetWorldMatrix;
MObject TwistExtractor::inTargetParInvMtx;
MObject TwistExtractor::inTargetJointOrient;
MObject TwistExtractor::inUseAxisAsAim;
MObject TwistExtractor::inAimWorldMatrix;
MObject TwistExtractor::inAimAxis;
MObject TwistExtractor::outTwistAngle;

void* TwistExtractor::creator(){
    // Maya creator function.
    return new TwistExtractor();
}

MStatus TwistExtractor::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to TwistExtractor class. Instances of TwistExtractor will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnMatrixAttribute mAttr;
    MFnUnitAttribute uAttr;
    MFnNumericAttribute nAttr;
    MFnEnumAttribute eAttr;

    inTargetWorldMatrix = mAttr.create("targetWorldMatrix", "twmtx", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inTargetParInvMtx = mAttr.create("targetParentInverseMatrix", "tpim", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    MObject tarJntOriX = uAttr.create("targetJointOrientX", "tjox", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject tarJntOriY = uAttr.create("targetJointOrientY", "tjoy", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject tarJntOriZ = uAttr.create("targetJointOrientZ", "tjoz", MFnUnitAttribute::kAngle, 0.0, &status);
    inTargetJointOrient = nAttr.create("TargetJointOrient", "tjo", tarJntOriX, tarJntOriY, tarJntOriZ, &status);
    INPUT_ATTR(nAttr);

    inUseAxisAsAim = nAttr.create("useAxisAsAim", "useAA", MFnNumericData::kBoolean, false, &status);
    INPUT_ATTR(nAttr);

    inAimWorldMatrix = mAttr.create("aimWorldMatrix", "awmtx", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inAimAxis = eAttr.create("aimAxis", "aaxis", 0, &status);
    eAttr.addField("Positive X", 0);
    eAttr.addField("Negative X", 1);
    eAttr.addField("Positive Y", 2);
    eAttr.addField("Negative X", 3);
    eAttr.addField("Positive Z", 4);
    eAttr.addField("Negative X", 5);
    INPUT_ATTR(eAttr);

    outTwistAngle = uAttr.create("outTwist", "twist", MFnUnitAttribute::kAngle, 0.0, &status);
    OUTPUT_ATTR(uAttr);

    addAttribute(inTargetWorldMatrix);
    addAttribute(inTargetParInvMtx);
    addAttribute(inTargetJointOrient);
    addAttribute(inUseAxisAsAim);
    addAttribute(inAimWorldMatrix);
    addAttribute(inAimAxis);
    addAttribute(outTwistAngle);
    attributeAffects(inTargetWorldMatrix, outTwistAngle);
    attributeAffects(inTargetParInvMtx, outTwistAngle);
    attributeAffects(inTargetJointOrient, outTwistAngle);
    attributeAffects(inUseAxisAsAim, outTwistAngle);
    attributeAffects(inAimWorldMatrix, outTwistAngle);
    attributeAffects(inAimAxis, outTwistAngle);

    return status;
}

MStatus TwistExtractor::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outTwistAngle)
        return MStatus::kUnknownParameter;

    MMatrix mTargetW = dataBlock.inputValue(inTargetWorldMatrix).asMatrix();
    MMatrix mParentInv = dataBlock.inputValue(inTargetParInvMtx).asMatrix();
    MEulerRotation eTargetJntOri = MEulerRotation(dataBlock.inputValue(inTargetJointOrient).asDouble3());
    bool useAxis = dataBlock.inputValue(inUseAxisAsAim).asBool();
    MDataHandle outTwistHandle = dataBlock.outputValue(outTwistAngle);

    MMatrix mTargetL = mTargetW * mParentInv;
    MQuaternion qTargetJntOri = eTargetJntOri.asQuaternion();

    MVector vTargetPos = MVector(mTargetW[3][0], mTargetW[3][1], mTargetW[3][2]);
    MVector nAim;
    if (useAxis){
        short axis = dataBlock.inputValue(inAimAxis).asShort();
        switch (axis){
        case 0:
            nAim = MVector(mTargetW[0][0], mTargetW[0][1], mTargetW[0][2]);
            break;
        case 1:
            nAim = -MVector(mTargetW[0][0], mTargetW[0][1], mTargetW[0][2]);
            break;
        case 2:
            nAim = MVector(mTargetW[1][0], mTargetW[1][1], mTargetW[1][2]);
            break;
        case 3:
            nAim = -MVector(mTargetW[1][0], mTargetW[1][1], mTargetW[1][2]);
            break;
        case 4:
            nAim = MVector(mTargetW[2][0], mTargetW[2][1], mTargetW[2][2]);
            break;
        case 5:
            nAim = -MVector(mTargetW[2][0], mTargetW[2][1], mTargetW[2][2]);
            break;
        };
    }
    else{
        MMatrix mAimW = dataBlock.inputValue(inAimWorldMatrix).asMatrix();
        MVector vAimPos = MVector(mAimW[3][0], mAimW[3][1], mAimW[3][2]);
        nAim = vAimPos - vTargetPos;
        nAim.normalize();
    }
    MVector nAimAxis = MVector(1.0, 0.0, 0.0);
    MVector nRotAxis = nAimAxis ^ nAim;
    double angle = nAimAxis.angle(nAim);
    MQuaternion qAim = MQuaternion(angle, nRotAxis);

    MTransformationMatrix mtxFn = MTransformationMatrix(mTargetL);
    MQuaternion qTarget = mtxFn.rotation();
    qTarget *= qTargetJntOri.invertIt();
    MQuaternion qExtract = qAim * qTarget.invertIt();

    MEulerRotation eExtract = qExtract.asEulerRotation();
    MAngle twist = MAngle(eExtract.x);
    outTwistHandle.setMAngle(twist);
    outTwistHandle.setClean();

    return MStatus::kSuccess;
}