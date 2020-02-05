#include "headers/n_gfRigIKVChain2.h"

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
MObject IKVChainSolver::inPoleVector;
MObject IKVChainSolver::inOffset;
MObject IKVChainSolver::inJntOri;
MObject IKVChainSolver::inParInvMtx;
MObject IKVChainSolver::inRestLenStart;
MObject IKVChainSolver::inRestLenEnd;
MObject IKVChainSolver::inPreferredAngle;
MObject IKVChainSolver::inTwist;
MObject IKVChainSolver::inPvMode;
MObject IKVChainSolver::inHierarchyMode;
MObject IKVChainSolver::inUseScale;
MObject IKVChainSolver::inCompressionLimit;
MObject IKVChainSolver::inSnapUpVector;
MObject IKVChainSolver::inSnap;
MObject IKVChainSolver::inSoftness;
MObject IKVChainSolver::inStretch;
MObject IKVChainSolver::inClampStretch;
MObject IKVChainSolver::inClampValue;
MObject IKVChainSolver::inSquash;
MObject IKVChainSolver::inSquashMultStart;
MObject IKVChainSolver::inSquashMultEnd;
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
    MFnEnumAttribute eAttr;
    MFnUnitAttribute uAttr;

    inRoot = mAttr.create("root", "root", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr)

    inHandle = mAttr.create("handle", "handle", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inPoleVector = mAttr.create("poleVector", "pole", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    MObject offX = uAttr.create("offsetX", "offx", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject offY = uAttr.create("offsetY", "offy", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject offZ = uAttr.create("offsetZ", "offz", MFnUnitAttribute::kAngle, 0.0, &status);
    inOffset = nAttr.create("offset", "off", offX, offY, offZ, &status);
    nAttr.setArray(true);
    INPUT_ATTR(nAttr);

    MObject jntOriX = uAttr.create("jointOrientX", "jox", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject jntOriY = uAttr.create("jointOrientY", "joy", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject jntOriZ = uAttr.create("jointOrientZ", "joz", MFnUnitAttribute::kAngle, 0.0, &status);
    inJntOri = nAttr.create("jointOrient", "jo", jntOriX, jntOriY, jntOriZ, &status);
    nAttr.setArray(true);
    INPUT_ATTR(nAttr);

    inParInvMtx = mAttr.create("parentInverseMatrix", "pim", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inRestLenStart = nAttr.create("restLengthStart", "rls", MFnNumericData::kFloat, 1.0f, &status);
    nAttr.setMin(0.001f);
    INPUT_ATTR(nAttr);
    nAttr.setChannelBox(true);

    inRestLenEnd = nAttr.create("restLengthEnd", "rle", MFnNumericData::kFloat, 1.0f, &status);
    nAttr.setMin(0.001f);
    INPUT_ATTR(nAttr);
    nAttr.setChannelBox(true);

    inPreferredAngle = uAttr.create("preferredAngle", "pa", MFnUnitAttribute::kAngle, 0.0, &status);
    uAttr.setMin(0.0);
    uAttr.setMax(2.0 * M_PI);
    INPUT_ATTR(uAttr);
    uAttr.setChannelBox(true);

    inTwist = uAttr.create("twist", "twist", MFnUnitAttribute::kAngle, 0.0, &status);
    INPUT_ATTR(uAttr);

    inPvMode = eAttr.create("pvMode", "pvm", 0);
    eAttr.addField("Manual", 0);
    eAttr.addField("Auto", 1);
    INPUT_ATTR(eAttr);

    inHierarchyMode = nAttr.create("hierarchyMode", "hm", MFnNumericData::kBoolean, true, &status);
    INPUT_ATTR(nAttr);

    inUseScale = nAttr.create("useStretchAsScale", "usca", MFnNumericData::kBoolean, false, &status);
    INPUT_ATTR(nAttr);

    inCompressionLimit = nAttr.create("compressionLimit", "cl", MFnNumericData::kFloat, 0.1f, &status);
    nAttr.setMin(0.001f);
    nAttr.setMax(0.4f);
    INPUT_ATTR(nAttr);

    inSnapUpVector = nAttr.create("snapUpVector", "supv", MFnNumericData::kFloat, 0.0f, &status);
    nAttr.setMin(0.0f);
    nAttr.setMax(1.0f);
    INPUT_ATTR(nAttr);

    inSnap = mAttr.create("snap", "snap", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inSoftness = nAttr.create("softness", "soft", MFnNumericData::kFloat, 0.0f, &status);
    nAttr.setMin(0.0f);
    nAttr.setSoftMax(0.2f);
    nAttr.setMax(1.0f);
    INPUT_ATTR(nAttr);

    inStretch = nAttr.create("stretch", "st", MFnNumericData::kFloat, 0.0f, &status);
    nAttr.setMin(0.0f);
    nAttr.setMax(1.0f);
    INPUT_ATTR(nAttr);

    inClampStretch = nAttr.create("clampStretch", "cst", MFnNumericData::kFloat, 0.0f, &status);
    nAttr.setMin(0.0f);
    nAttr.setMax(1.0f);
    INPUT_ATTR(nAttr);

    inClampValue = nAttr.create("clampValue", "cstv", MFnNumericData::kDouble, 1.5, &status);
    nAttr.setMin(1.0);
    nAttr.setSoftMax(1.8);
    INPUT_ATTR(nAttr);

    inSquash = nAttr.create("squash", "sq", MFnNumericData::kFloat, 0.0f, &status);
    nAttr.setMin(0.0f);
    nAttr.setMax(1.0f);
    INPUT_ATTR(nAttr);

    MObject startSqX = nAttr.create("squashMultStartX", "sqmsx", MFnNumericData::kDouble, 1.0, &status);
    MObject startSqY = nAttr.create("squashMultStartY", "sqmsy", MFnNumericData::kDouble, 1.0, &status);
    inSquashMultStart = nAttr.create("squashMultStart", "sqms", startSqX, startSqY, MObject::kNullObj, &status);
    nAttr.setMin(0.001, 0.001);
    INPUT_ATTR(nAttr);

    MObject endSqX = nAttr.create("squashMultEndX", "sqmex", MFnNumericData::kDouble, 1.0, &status);
    MObject endSqY = nAttr.create("squashMultEndY", "sqmey", MFnNumericData::kDouble, 1.0, &status);
    inSquashMultEnd = nAttr.create("squashMultEnd", "sqme", endSqX, endSqY, MObject::kNullObj, &status);
    nAttr.setMin(0.001, 0.001);
    INPUT_ATTR(nAttr);

    outChain = mAttr.create("outChain", "oc", MFnMatrixAttribute::kDouble, &status);
    mAttr.setArray(true);
    OUTPUT_ATTR(mAttr);

    addAttribute(inRoot);
    addAttribute(inHandle);
    addAttribute(inPoleVector);
    addAttribute(inOffset);
    addAttribute(inJntOri);
    addAttribute(inParInvMtx);
    addAttribute(inRestLenStart);
    addAttribute(inRestLenEnd);
    addAttribute(inPreferredAngle);
    addAttribute(inTwist);
    addAttribute(inPvMode);
    addAttribute(inHierarchyMode);
    addAttribute(inUseScale);
    addAttribute(inCompressionLimit);
    addAttribute(inSnapUpVector);
    addAttribute(inSnap);
    addAttribute(inSoftness);
    addAttribute(inStretch);
    addAttribute(inClampStretch);
    addAttribute(inClampValue);
    addAttribute(inSquash);
    addAttribute(inSquashMultStart);
    addAttribute(inSquashMultEnd);
    addAttribute(outChain);
    attributeAffects(inRoot, outChain);
    attributeAffects(inHandle, outChain);
    attributeAffects(inPoleVector, outChain);
    attributeAffects(inOffset, outChain);
    attributeAffects(inJntOri, outChain);
    attributeAffects(inParInvMtx, outChain);
    attributeAffects(inRestLenStart, outChain);
    attributeAffects(inRestLenEnd, outChain);
    attributeAffects(inPreferredAngle, outChain);
    attributeAffects(inTwist, outChain);
    attributeAffects(inPvMode, outChain);
    attributeAffects(inHierarchyMode, outChain);
    attributeAffects(inUseScale, outChain);
    attributeAffects(inCompressionLimit, outChain);
    attributeAffects(inSnapUpVector, outChain);
    attributeAffects(inSnap, outChain);
    attributeAffects(inSoftness, outChain);
    attributeAffects(inStretch, outChain);
    attributeAffects(inClampStretch, outChain);
    attributeAffects(inClampValue, outChain);
    attributeAffects(inSquash, outChain);
    attributeAffects(inSquashMultStart, outChain);
    attributeAffects(inSquashMultEnd, outChain);

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

    // Get Basis Transformation
    MMatrix mRoot = dataBlock.inputValue(inRoot).asMatrix();
    MMatrix mHandle = dataBlock.inputValue(inHandle).asMatrix();
    MMatrix mPoleVector = dataBlock.inputValue(inPoleVector).asMatrix();
    short pvMode = dataBlock.inputValue(inPvMode).asShort();
    double prefAngle = dataBlock.inputValue(inPreferredAngle).asAngle().asRadians();
    double twist = dataBlock.inputValue(inTwist).asAngle().asRadians();
    float snap = dataBlock.inputValue(inSnap).asFloat();
    MMatrix mSnap = dataBlock.inputValue(inSnap).asMatrix();

    MVector vRoot = MVector(mRoot[3][0], mRoot[3][1], mRoot[3][2]);
    MVector vHandle = MVector(mHandle[3][0], mHandle[3][1], mHandle[3][2]);
    MVector vPoleVector = MVector(mPoleVector[3][0], mPoleVector[3][1], mPoleVector[3][2]);
    MVector vSnap = MVector(mSnap[3][0], mSnap[3][1], mSnap[3][2]);

    MQuaternion qBasis = MQuaternion();

    MVector vAim = vHandle - vRoot;
    MVector nAim = vAim.normal();
    MQuaternion qAim = MQuaternion(MVector::xAxis, nAim);
    qBasis *= qAim;

    MVector vStartSnap = vSnap - vRoot;
    MVector vEndSnap = vSnap - vHandle;

    MVector vUp;
    if (pvMode == 0)
        vUp = vPoleVector - vRoot;
    else{
        MQuaternion qTwist = MQuaternion(prefAngle + twist, nAim);
        vUp = MVector::yAxis.rotateBy(qTwist);
    }
    MVector nNormalPole = vUp - ((vUp * nAim) * nAim);
    nNormalPole.normalize();
    MVector nNormal;
    if (snap > 0.0f){
        MVector nNormalSnap = vStartSnap - ((vStartSnap * nAim) * nAim);
        nNormalSnap.normalize();
        nNormal = (1.0f - snap) * nNormalPole + snap * nNormalSnap;
    }
    else
        nNormal = nNormalPole;
    MVector nUp = MVector::yAxis.rotateBy(qAim);
    double angle = nUp.angle(nNormal);
    MQuaternion qNormal = MQuaternion(angle, nAim);
    if (!nNormal.isEquivalent(nUp.rotateBy(qNormal), 1.0e-5)){
        angle = 2.0 * M_PI - angle;
        qNormal = MQuaternion(angle, nAim);
    }
    qBasis *= qNormal;


    // Solve Triangle
    float restStartLen = dataBlock.inputValue(inRestLenStart).asFloat();
    float restEndLen = dataBlock.inputValue(inRestLenEnd).asFloat();
    float compressionLimit = dataBlock.inputValue(inCompressionLimit).asFloat();
    float softVal = dataBlock.inputValue(inSoftness).asFloat();

    double startLen = (1.0f - snap) * restStartLen + snap * vStartSnap.length();
    double endLen = (1.0f - snap) * restEndLen + snap * vEndSnap.length();
    double chainLen = (1.0f - snap) * (restStartLen + restEndLen) + snap * (vStartSnap.length() + vEndSnap.length());
    double handleLen = vAim.length();

    double rigidLen = std::max(std::min(handleLen, chainLen), chainLen * compressionLimit);
    double dc = chainLen;
    double da = (1.0f - softVal) * dc;
    double solverLen;
    if (handleLen > da && softVal > 0.0f){
        double ds = dc - da;
        double softLen = ds * (1.0 - pow(M_E, (da - handleLen) / ds)) + da;
        solverLen = (1.0f - snap) * softLen + snap * rigidLen;
    }
    else
        solverLen = rigidLen;


    // Pre Calculations
    double startLenSquared = pow(startLen, 2.0);
    double endLenSquared = pow(endLen, 2.0);
    double solverLenSquared = pow(solverLen, 2.0);
    float stretch = dataBlock.inputValue(inStretch).asFloat();
    double2& squashMultStart = dataBlock.inputValue(inSquashMultStart).asDouble2();
    double2& squashMultEnd = dataBlock.inputValue(inSquashMultEnd).asDouble2();
    double stretchFactor;
    double squashFactor;
    if (stretch > 0.0f){
        float clampStretch = dataBlock.inputValue(inClampStretch).asFloat();
        double clampValue = dataBlock.inputValue(inClampValue).asDouble();
        float squash = dataBlock.inputValue(inSquash).asFloat();
        double scaleFactor;
        if (handleLen > da && softVal > 0.0f)
            scaleFactor = handleLen / solverLen;
        else
            scaleFactor = handleLen / chainLen;
        double stretchFactor;
        if (handleLen >= da){
            double clampFactor = (1.0f - clampStretch) * scaleFactor + clampStretch * std::min(scaleFactor, clampValue);
            stretchFactor = (1.0f - stretch) + stretch * clampFactor;
        }
        else
            stretchFactor = 1.0;
        squashFactor = (1.0f - squash) + squash * (1.0 / sqrt(stretchFactor));
    }
    else{
        stretchFactor = 1.0;
        squashFactor = 1.0;
    }

    bool hierarchyMode = dataBlock.inputValue(inHierarchyMode).asBool();
    bool useScale = dataBlock.inputValue(inUseScale).asBool();
    MArrayDataHandle outChainHandle = dataBlock.outputArrayValue(outChain);
    MArrayDataHandle offsetHandle = dataBlock.inputArrayValue(inOffset);
    MArrayDataHandle jntOriHandle = dataBlock.inputArrayValue(inJntOri);
    MMatrix mParInv = dataBlock.inputValue(inParInvMtx).asMatrix();
    std::vector<MMatrix> srtList;
    std::vector<MQuaternion> offsetList;
    std::vector<MQuaternion> jntOriList;

    for (uint32_t i = 0; i < offsetHandle.elementCount(); i++){
        offsetHandle.jumpToArrayElement(i);
        MEulerRotation eOff = MEulerRotation(offsetHandle.inputValue().asDouble3());
        MQuaternion qOff = eOff.asQuaternion();
        offsetList.push_back(qOff);
    }

    for (uint32_t i = 0; i < jntOriHandle.elementCount(); i++){
        jntOriHandle.jumpToArrayElement(i);
        MEulerRotation eOri = MEulerRotation(jntOriHandle.inputValue().asDouble3());
        MQuaternion qOri = eOri.asQuaternion();
        jntOriList.push_back(qOri);
    }


    // First Output
    // Scale
    double firstStretch = stretchFactor;
    double firstScaX = firstStretch;
    if (!useScale)
        firstStretch = 1.0;
    double firstSquash[2] = {squashFactor * squashMultStart[0], squashFactor * squashMultStart[1]};
    double firstSca[3] = {firstStretch, firstSquash[0], firstSquash[1]};
    // Rotation
    double betaCosPure = (startLenSquared + solverLenSquared - endLenSquared) / (2.0 * startLen * solverLen);
    double betaCos = std::min(std::max(betaCosPure, -1.0), 1.0);
    #ifdef __linux__
        double beta = acos(betaCos);
    #else
        double beta = std::acos(betaCos);
    #endif
    MQuaternion qBeta = MQuaternion(beta, MVector::zAxis);
    MQuaternion qFirstRot = MQuaternion();
    MQuaternion qFirstRotW = qBeta * qBasis;
    if (offsetList.size() >= 1)
        qFirstRot *= offsetList[0];
    qFirstRot *= qFirstRotW;
    if (jntOriList.size() >= 1)
        qFirstRot *= jntOriList[0].invertIt();
    // Translation
    MVector vFirstPos = vRoot;
    // Matrix Output
    MTransformationMatrix mtxFn = MTransformationMatrix();
    mtxFn.setScale(firstSca, MSpace::kTransform);
    mtxFn.setRotationOrientation(qFirstRot);
    mtxFn.setTranslation(vFirstPos, MSpace::kTransform);
    MMatrix mFirstW = mtxFn.asMatrix();
    MMatrix mFirstL = mFirstW * mParInv;
    srtList.push_back(mFirstL);

    return MStatus::kSuccess;
}