#include "headers/n_gfRigIKVChain.h"

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
IKVChainSolver::IKVChainSolver() {}

// Destructor.
IKVChainSolver::~IKVChainSolver() {}

MObject IKVChainSolver::inRoot;
MObject IKVChainSolver::inHandle;
MObject IKVChainSolver::inUpVector;
MObject IKVChainSolver::inParInvMtx;
MObject IKVChainSolver::inJointOrient;
MObject IKVChainSolver::inPreferredAngle;
MObject IKVChainSolver::inPvMode;
MObject IKVChainSolver::inTwist;
MObject IKVChainSolver::inHierarchyMode;
MObject IKVChainSolver::inRestLength1;
MObject IKVChainSolver::inRestLength2;
MObject IKVChainSolver::inCompressionLimit;
MObject IKVChainSolver::inSoftness;
MObject IKVChainSolver::inSnapUpVector;
MObject IKVChainSolver::inSnapObj;
MObject IKVChainSolver::inStretch;
MObject IKVChainSolver::inClampStretch;
MObject IKVChainSolver::inClampValue;
MObject IKVChainSolver::inSquash;
MObject IKVChainSolver::inFlipOri;
MObject IKVChainSolver::outChain;

void* IKVChainSolver::creator(){
    // Maya creator function.
    return new IKVChainSolver();
}

MStatus IKVChainSolver::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to IKVChainSolver class. Instances of IKVChainSolver will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnMatrixAttribute mAttr;
    MFnNumericAttribute nAttr;
    MFnUnitAttribute uAttr;
    MFnEnumAttribute eAttr;

    inRoot = mAttr.create("root", "root", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inHandle = mAttr.create("handle", "handle", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inUpVector = mAttr.create("upVector", "up", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inParInvMtx = mAttr.create("parentInverseMatrix", "pim", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    MObject jntOriX = uAttr.create("jointOrientX", "jox", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject jntOriY = uAttr.create("jointOrientY", "joy", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject jntOriZ = uAttr.create("jointOrientZ", "joz", MFnUnitAttribute::kAngle, 0.0, &status);
    inJointOrient = nAttr.create("jointOrient", "jo", jntOriX, jntOriY, jntOriZ, &status);
    nAttr.setArray(true);
    INPUT_ATTR(nAttr);

    inPreferredAngle = uAttr.create("preferredAngle", "pa", MFnUnitAttribute::kAngle, 0.0, &status);
    uAttr.setMin(0.0);
    uAttr.setMax(2.0 * M_PI);
    INPUT_ATTR(uAttr);

    inPvMode = eAttr.create("pvMode", "pvm", 0, &status);
    eAttr.addField("Manual", 0);
    eAttr.addField("Auto", 1);
    INPUT_ATTR(eAttr);

    inTwist = uAttr.create("twist", "tw", MFnUnitAttribute::kAngle, 0.0, &status);
    INPUT_ATTR(uAttr);

    inHierarchyMode = nAttr.create("hierarchyMode", "hm", MFnNumericData::kBoolean, true, &status);
    INPUT_ATTR(nAttr);

    inRestLength1 = nAttr.create("restLength1", "rl1", MFnNumericData::kFloat, 1.0f, &status);
    nAttr.setMin(0.001f);
    INPUT_ATTR(nAttr);

    inRestLength2 = nAttr.create("restLength2", "rl2", MFnNumericData::kFloat, 1.0f, &status);
    nAttr.setMin(0.001f);
    INPUT_ATTR(nAttr);

    inCompressionLimit = nAttr.create("compressionLimit", "cl", MFnNumericData::kFloat, 0.1f, &status);
    nAttr.setMin(0.001f);
    nAttr.setMax(0.4f);
    INPUT_ATTR(nAttr);

    inSoftness = nAttr.create("softness", "soft", MFnNumericData::kFloat, 0.0f, &status);
    nAttr.setMin(0.0f);
    nAttr.setSoftMax(0.4f);
    nAttr.setMax(1.0f);
    INPUT_ATTR(nAttr);

    inSnapUpVector = nAttr.create("snapPoleVector", "snap", MFnNumericData::kFloat, 0.0, &status);
    nAttr.setMin(0.0f);
    nAttr.setMax(1.0f);
    INPUT_ATTR(nAttr);

    inSnapObj = mAttr.create("snapObject", "sobj", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inStretch = nAttr.create("stretch", "st", MFnNumericData::kDouble, 0.0, &status);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    INPUT_ATTR(nAttr);

    inClampStretch = nAttr.create("clampStretch", "cst", MFnNumericData::kDouble, 0.0, &status);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    INPUT_ATTR(nAttr);

    inClampValue = nAttr.create("clampValue", "cstv", MFnNumericData::kDouble, 1.5, &status);
    nAttr.setMin(1.0);
    nAttr.setSoftMax(1.8);
    INPUT_ATTR(nAttr);

    inSquash = nAttr.create("squash", "sq", MFnNumericData::kDouble, 0.0, &status);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    INPUT_ATTR(nAttr);

    inFlipOri = nAttr.create("flipOrientation", "flip", MFnNumericData::kBoolean, false, &status);
    INPUT_ATTR(nAttr);

    outChain = mAttr.create("outChain", "oc", MFnMatrixAttribute::kDouble, &status);
    mAttr.setArray(true);
    OUTPUT_ATTR(mAttr);

    addAttribute(inRoot);
    addAttribute(inHandle);
    addAttribute(inUpVector);
    addAttribute(inParInvMtx);
    addAttribute(inJointOrient);
    addAttribute(inPreferredAngle);
    addAttribute(inPvMode);
    addAttribute(inTwist);
    addAttribute(inHierarchyMode);
    addAttribute(inRestLength1);
    addAttribute(inRestLength2);
    addAttribute(inCompressionLimit);
    addAttribute(inSoftness);
    addAttribute(inSnapUpVector);
    addAttribute(inSnapObj);
    addAttribute(inStretch);
    addAttribute(inClampStretch);
    addAttribute(inClampValue);
    addAttribute(inSquash);
    addAttribute(inFlipOri);
    addAttribute(outChain);
    attributeAffects(inRoot, outChain);
    attributeAffects(inHandle, outChain);
    attributeAffects(inUpVector, outChain);
    attributeAffects(inParInvMtx, outChain);
    attributeAffects(inJointOrient, outChain);
    attributeAffects(inPreferredAngle, outChain);
    attributeAffects(inPvMode, outChain);
    attributeAffects(inTwist, outChain);
    attributeAffects(inHierarchyMode, outChain);
    attributeAffects(inRestLength1, outChain);
    attributeAffects(inRestLength2, outChain);
    attributeAffects(inCompressionLimit, outChain);
    attributeAffects(inSoftness, outChain);
    attributeAffects(inSnapUpVector, outChain);
    attributeAffects(inSnapObj, outChain);
    attributeAffects(inStretch, outChain);
    attributeAffects(inClampStretch, outChain);
    attributeAffects(inClampValue, outChain);
    attributeAffects(inSquash, outChain);
    attributeAffects(inFlipOri, outChain);

    return status;
}

MStatus IKVChainSolver::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outChain)
        return MStatus::kUnknownParameter;

    // Get basis matrix
    float snap = dataBlock.inputValue(inSnapUpVector).asFloat();
    short pvMode = dataBlock.inputValue(inPvMode).asShort();
    MMatrix mRoot = dataBlock.inputValue(inRoot).asMatrix();
    MMatrix mHandle = dataBlock.inputValue(inHandle).asMatrix();
    MMatrix mUpVector = dataBlock.inputValue(inUpVector).asMatrix();
    MMatrix mSnap = dataBlock.inputValue(inSnapObj).asMatrix();
    double prefAngle = dataBlock.inputValue(inPreferredAngle).asAngle().asRadians();
    double twist = dataBlock.inputValue(inTwist).asAngle().asRadians();
    bool flip = dataBlock.inputValue(inFlipOri).asBool();
    MVector vRoot = MVector(mRoot[3][0], mRoot[3][1], mRoot[3][2]);
    MVector vHandle = MVector(mHandle[3][0], mHandle[3][1], mHandle[3][2]);
    MVector vUpVector = MVector(mUpVector[3][0], mUpVector[3][1], mUpVector[3][2]);
    MVector vSnap = MVector(mSnap[3][0], mSnap[3][1], mSnap[3][2]);
    MVector vXDirection = vHandle - vRoot;
    double xDist = vXDirection.length();
    MVector nXAxis = vXDirection.normal();
    MVector vL1Snap = vSnap - vRoot;
    MVector vL2Snap = vSnap - vHandle;
    MVector nYAxis, nYAxisSnap, vYDirection;
    if (pvMode == 0){
        MVector vUpDirection = vUpVector - vRoot;
        vYDirection = vUpDirection - ((vUpDirection * nXAxis) * nXAxis);
        nYAxis = vYDirection.normal();
    }
    else{
        MVector vAutoPosWorld = vRoot + MVector(cos(twist + prefAngle), 0.0, sin(twist + prefAngle));
        MVector vAutoPosLocal = vAutoPosWorld - vRoot;
        vYDirection = vAutoPosLocal - ((vAutoPosLocal * nXAxis) * nXAxis);
        nYAxis = vYDirection.normal();
    }
    if (snap > 0.0f){
        MVector vSnapDirection = vL1Snap - ((vL1Snap * nXAxis) * nXAxis);
        MVector nSnapDirection = vSnapDirection.normal();
        nYAxisSnap = (1.0f - snap) * nYAxis + snap * nSnapDirection;
    }
    else
        nYAxisSnap = nYAxis;
    MVector nZAxis = nXAxis ^ nYAxisSnap;
    double basis[4][4] = {
        {nXAxis.x, nXAxis.y, nXAxis.z, 0.0},
        {nYAxisSnap.x, nYAxisSnap.y, nYAxisSnap.z, 0.0},
        {nZAxis.x, nZAxis.y, nZAxis.z, 0.0},
        {vRoot.x, vRoot.y, vRoot.z, 1.0}
    };
    MMatrix mBasis = MMatrix(basis);

    // Solve triangle
    float l1 = dataBlock.inputValue(inRestLength1).asFloat();
    float l2 = dataBlock.inputValue(inRestLength2).asFloat();
    float compressionLimit = dataBlock.inputValue(inCompressionLimit).asFloat();
    float softValue = dataBlock.inputValue(inSoftness).asFloat();
    double l1m = l1;
    double l2m = l2;
    double l1Snap = vL1Snap.length();
    double l2Snap = vL2Snap.length();
    double length1 = (1.0f - snap) * l1m + snap * l1Snap;
    double length2 = (1.0f - snap) * l2m + snap * l2Snap;
    double chainLength = (1.0f - snap) * (l1m + l2m) + snap * (l1Snap + l2Snap);
    double l3rigid = max(min(xDist, chainLength), chainLength * compressionLimit);
    double dc = chainLength;
    double da = (1.0f - softValue) * dc;
    double l3;
    double l3soft = 1.0f;
    double l3SnapSoft = l3soft;
    if ((xDist > da) && (softValue > 0.0f)){
        double ds = dc - da;
        l3soft = ds * (1.0 - pow(M_E, (da - xDist) / ds)) + da;
        l3SnapSoft = (1.0f - snap) * l3soft + snap * l3rigid;
        l3 = l3SnapSoft;
    }
    else
        l3 = l3rigid;

    // Angle mesurement
    bool hierarchyMode = dataBlock.inputValue(inHierarchyMode).asBool();
    double betaCos = (pow(length1, 2.0) + pow(l3, 2.0) - pow(length2, 2.0)) / (2.0 * length1 * l3);
    if (betaCos < -1.0)
        betaCos = -1.0;
    double beta = acos(betaCos);
    double betaSin = sin(beta);
    double gammaCos = (pow(length1, 2.0) + pow(length2, 2.0) - pow(l3, 2.0)) / (2.0 * length1 * length2);
    if (gammaCos > 1.0)
        gammaCos = 1.0;
    double gamma = acos(gammaCos);
    double gammaComplement;
    if (hierarchyMode == true)
        gammaComplement = gamma - M_PI;
    else
        gammaComplement = gamma + beta - M_PI;
    double gammaComplementCos = cos(gammaComplement);
    double gammaComplementSin = sin(gammaComplement);
    double alpha = M_PI - beta - gamma;
    double alphaCos = cos(alpha);
    double alphaSin = sin(alpha);

    // Cartoony features
    double stretch = dataBlock.inputValue(inStretch).asDouble();
    double stretchFactor;
    double squashFactor;
    if (stretch > 0.0f){
        double clampStretch = dataBlock.inputValue(inClampStretch).asDouble();
        double clampStretchValue = dataBlock.inputValue(inClampValue).asDouble();
        double squash = dataBlock.inputValue(inSquash).asDouble();
        double scaleFactor;
        if ((xDist > da) && (softValue > 0.0f))
            scaleFactor = xDist / l3SnapSoft;
        else
            scaleFactor = xDist / chainLength;
        if (xDist >= da){
            double clampFactor = (1.0 - clampStretch) * scaleFactor + clampStretch * min(scaleFactor, clampStretchValue);
            stretchFactor = (1.0 - stretch) + stretch * clampFactor;
        }
        else
            stretchFactor = 1.0;
        squashFactor = (1.0 - squash) + squash * (1.0 / sqrt(stretchFactor));
    }
    else{
        stretchFactor = 1.0;
        squashFactor = 1.0;
    }

    // Output transforms
    MArrayDataHandle outChainHandle = dataBlock.outputArrayValue(outChain);
    vector<MMatrix> srtList;
    vector<MMatrix> jntOriList;
    MArrayDataHandle jntOriHandle = dataBlock.inputArrayValue(inJointOrient);
    MTransformationMatrix mtxFn;
    MMatrix mFlip;
    if (flip){
        mtxFn = MTransformationMatrix();
        mtxFn.rotateBy(MEulerRotation(0.0, 0.0, -M_PI), MSpace::kTransform);
        mFlip = mtxFn.asMatrix();
    }
    for (uint32_t i = 0; i < jntOriHandle.elementCount(); i++){
        jntOriHandle.jumpToArrayElement(i);
        MEulerRotation eOri = MEulerRotation(jntOriHandle.inputValue().asDouble3());
        mtxFn = MTransformationMatrix();
        mtxFn.rotateBy(eOri, MSpace::kTransform);
        MMatrix mOri = mtxFn.asMatrix();
        jntOriList.push_back(mOri);
    }
    if (hierarchyMode){
        MMatrix mParInv = dataBlock.inputValue(inParInvMtx).asMatrix();
        MMatrix mScale = MMatrix();
        MMatrix mLocal = MMatrix();
        MMatrix mResult = MMatrix();
        mScale[0][0] = stretchFactor;
        mScale[1][1] = squashFactor;
        mScale[2][2] = squashFactor;
        mLocal = MMatrix();
        mLocal[0][0] = betaCos;
        mLocal[0][1] = betaSin;
        mLocal[1][0] = -betaSin;
        mLocal[1][1] = betaCos;
        mResult = MMatrix();
        if (flip)
            mLocal *= mFlip;
        if (jntOriList.size() >= 1)
            mResult = mScale * mLocal * mBasis * mParInv * jntOriList[0].inverse();
        else
            mResult = mScale * mLocal * mBasis * mParInv;
        srtList.push_back(mResult);
        mLocal = MMatrix();
        mLocal[0][0] = gammaComplementCos;
        mLocal[0][1] = gammaComplementSin;
        mLocal[1][0] = -gammaComplementSin;
        mLocal[1][1] = gammaComplementCos;
        mResult = MMatrix();
        if (jntOriList.size() >= 2)
            mResult = mScale * mLocal * jntOriList[1].inverse();
        else
            mResult = mScale * mLocal;
        if (flip)
            mResult[3][0] = -length1;
        else
            mResult[3][0] = length1;
        srtList.push_back(mResult);
        mLocal = MMatrix();
        mLocal[0][0] = alphaCos;
        mLocal[0][1] = alphaSin;
        mLocal[1][0] = -alphaSin;
        mLocal[1][1] = alphaCos;
        if (flip)
            mLocal[3][0] = -length2;
        else
            mLocal[3][0] = length2;
        srtList.push_back(mLocal);
    }
    else{
        MMatrix mScale = MMatrix();
        MMatrix mLocal = MMatrix();
        MMatrix mResult = MMatrix();
        mScale[0][0] = stretchFactor;
        mScale[1][1] = squashFactor;
        mScale[2][2] = squashFactor;
        mLocal = MMatrix();
        mLocal[0][0] = betaCos;
        mLocal[0][1] = betaSin;
        mLocal[1][0] = -betaSin;
        mLocal[1][1] = betaCos;
        mResult = MMatrix();
        mResult = mScale * mLocal * mBasis;
        srtList.push_back(mResult);
        mLocal = MMatrix();
        mLocal[0][0] = gammaComplementCos;
        mLocal[0][1] = gammaComplementSin;
        mLocal[1][0] = -gammaComplementSin;
        mLocal[1][1] = gammaComplementCos;
        mLocal[3][0] = betaCos * l1m * stretchFactor;
        mLocal[3][1] = betaSin * l1m * stretchFactor;
        mResult = MMatrix();
        mResult = mScale * mLocal * mBasis;
        srtList.push_back(mResult);
        mLocal = mHandle;
        mLocal[3][0] = mBasis[3][0] + mBasis[0][0] * l3 * stretchFactor;
        mLocal[3][1] = mBasis[3][1] + mBasis[0][1] * l3 * stretchFactor;
        mLocal[3][2] = mBasis[3][2] + mBasis[0][2] * l3 * stretchFactor;
        mResult = MMatrix();
        mResult = mScale * mLocal;
        srtList.push_back(mResult);
    }

    for (uint32_t i = 0; i < outChainHandle.elementCount(); i++){
        outChainHandle.jumpToArrayElement(i);
        MDataHandle resultHandle = outChainHandle.outputValue();
        if ((i < outChainHandle.elementCount()) && (i < srtList.size()))
            resultHandle.setMMatrix(srtList[i]);
        else
            resultHandle.setMMatrix(MMatrix());
    }

    outChainHandle.setAllClean();

    return MStatus::kSuccess;
}