#include "headers/ikVChain2.hpp"

// Configure a input attribute.
#define INPUT_ATTR(FNATTR)      \
    FNATTR.setWritable(true);   \
    FNATTR.setReadable(true);   \
    FNATTR.setStorable(true);   \
    FNATTR.setKeyable(true);    \
    CHECK_MSTATUS_AND_RETURN_IT(status);

// Configure a output attribute.
#define OUTPUT_ATTR(FNATTR)     \
    FNATTR.setWritable(false);  \
    FNATTR.setReadable(true);   \
    FNATTR.setStorable(false);  \
    FNATTR.setKeyable(false);   \
    CHECK_MSTATUS_AND_RETURN_IT(status);


// Constructors and Destructors
IKSolver::IKSolver(){}
IKSolver::~IKSolver(){}


// Members initialization
MObject IKSolver::inPrimAxis;
MObject IKSolver::inUpAxis;
MObject IKSolver::inFlatMode;
MObject IKSolver::inStretchScale;
MObject IKSolver::inRoot;
MObject IKSolver::inHandle;
MObject IKSolver::inPole;
MObject IKSolver::inRestStartLen;
MObject IKSolver::inRestEndLen;
MObject IKSolver::inStartJntOri;
MObject IKSolver::inMidJntOri;
MObject IKSolver::inEndJntOri;
MObject IKSolver::inStartOffset;
MObject IKSolver::inMidOffset;
MObject IKSolver::inEndOffset;
MObject IKSolver::inParInvMtx;
MObject IKSolver::inSoftness;
MObject IKSolver::inStretch;
MObject IKSolver::inSquash;
MObject IKSolver::inStartStMult;
MObject IKSolver::inEndStMult;
MObject IKSolver::inStartSqMult;
MObject IKSolver::inEndSqMult;
MObject IKSolver::outTranslate;
MObject IKSolver::outRotate;
MObject IKSolver::outScale;
MObject IKSolver::outTransforms;




MPxNode::SchedulingType IKSolver::schedulingType() const{
    return MPxNode::SchedulingType::kParallel;
}

void* IKSolver::creator(){
    return new IKSolver();
}

MStatus IKSolver::initialize(){
    // Defines the set of attributes for this node. The attributes declared in this 
    // function are assigned as static members to IKSolver class. Instances of 
    // IKSolver will use these attributes to create plugs for use in the compute()
    // method.
    MStatus status;
    MFnEnumAttribute eAttr;
    MFnMatrixAttribute mAttr;
    MFnNumericAttribute nAttr;
    MFnUnitAttribute uAttr;
    MFnCompoundAttribute cAttr;

    inPrimAxis = eAttr.create("primaryAxis", "paxis", Axis::xAxis, &status);
    eAttr.addField("X Axis", Axis::xAxis);
    eAttr.addField("-X Axis", Axis::xAxisNeg);
    eAttr.addField("Y Axis", Axis::yAxis);
    eAttr.addField("-Y Axis", Axis::yAxisNeg);
    eAttr.addField("Z Axis", Axis::zAxis);
    eAttr.addField("-Z Axis", Axis::zAxisNeg);
    INPUT_ATTR(eAttr);

    inUpAxis = eAttr.create("upAxis", "uaxis", Axis::yAxis, &status);
    eAttr.addField("X Axis", Axis::xAxis);
    eAttr.addField("-X Axis", Axis::xAxisNeg);
    eAttr.addField("Y Axis", Axis::yAxis);
    eAttr.addField("-Y Axis", Axis::yAxisNeg);
    eAttr.addField("Z Axis", Axis::zAxis);
    eAttr.addField("-Z Axis", Axis::zAxisNeg);
    INPUT_ATTR(eAttr);

    inFlatMode = nAttr.create("flatMode", "fm", MFnNumericData::kBoolean, false, &status);
    INPUT_ATTR(nAttr);

    inStretchScale = nAttr.create("applyStretchAsScale", "asas", MFnNumericData::kBoolean, false, &status);
    INPUT_ATTR(nAttr);

    inRoot = mAttr.create("root", "root", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inHandle = mAttr.create("handle", "handle", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inPole = mAttr.create("pole", "pole", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inRestStartLen = nAttr.create("restStartLen", "rslen", MFnNumericData::kFloat, 1.0f, &status);
    nAttr.setMin(0.001f);
    INPUT_ATTR(nAttr);

    inRestEndLen = nAttr.create("restEndLen", "relen", MFnNumericData::kFloat, 1.0f, &status);
    nAttr.setMin(0.001f);
    INPUT_ATTR(nAttr);

    MObject sjox = uAttr.create("startJointOrientX", "sjox", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject sjoy = uAttr.create("startJointOrientY", "sjoy", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject sjoz = uAttr.create("startJointOrientZ", "sjoz", MFnUnitAttribute::kAngle, 0.0, &status);
    inStartJntOri = nAttr.create("startJointOrient", "sjo", sjox, sjoy, sjoz, &status);
    INPUT_ATTR(nAttr);

    MObject mjox = uAttr.create("midJointOrientX", "mjox", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject mjoy = uAttr.create("midJointOrientY", "mjoy", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject mjoz = uAttr.create("midJointOrientZ", "mjoz", MFnUnitAttribute::kAngle, 0.0, &status);
    inMidJntOri = nAttr.create("midJointOrient", "mjo", mjox, mjoy, mjoz, &status);
    INPUT_ATTR(nAttr);

    MObject ejox = uAttr.create("endJointOrientX", "ejox", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject ejoy = uAttr.create("endJointOrientY", "ejoy", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject ejoz = uAttr.create("endJointOrientZ", "ejoz", MFnUnitAttribute::kAngle, 0.0, &status);
    inEndJntOri = nAttr.create("endJointOrient", "ejo", ejox, ejoy, ejoz, &status);
    INPUT_ATTR(nAttr);

    MObject sofx = uAttr.create("startOffsetX", "sofx", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject sofy = uAttr.create("startOffsetY", "sofy", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject sofz = uAttr.create("startOffsetZ", "sofz", MFnUnitAttribute::kAngle, 0.0, &status);
    inStartOffset = nAttr.create("startOffset", "soff", sofx, sofy, sofz, &status);
    INPUT_ATTR(nAttr);

    MObject mofx = uAttr.create("midOffsetX", "mofx", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject mofy = uAttr.create("midOffsetY", "mofy", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject mofz = uAttr.create("midOffsetZ", "mofz", MFnUnitAttribute::kAngle, 0.0, &status);
    inMidOffset = nAttr.create("midOffset", "moff", mofx, mofy, mofz, &status);
    INPUT_ATTR(nAttr);

    MObject eofx = uAttr.create("endOffsetX", "eofx", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject eofy = uAttr.create("endOffsetY", "eofy", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject eofz = uAttr.create("endOffsetZ", "eofz", MFnUnitAttribute::kAngle, 0.0, &status);
    inEndOffset = nAttr.create("endOffset", "eoff", eofx, eofy, eofz, &status);
    INPUT_ATTR(nAttr);

    inParInvMtx = mAttr.create("parentInverseMatrix", "pim", MFnMatrixAttribute::kDouble, &status);
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

    inSquash = nAttr.create("squash", "sq", MFnNumericData::kFloat, 0.0f, &status);
    nAttr.setMin(0.0f);
    nAttr.setMax(1.0f);
    INPUT_ATTR(nAttr);

    inStartStMult = nAttr.create("startStretchMult", "sstm", MFnNumericData::kFloat, 1.0f, &status);
    nAttr.setMin(0.0f);
    INPUT_ATTR(nAttr);

    inEndStMult = nAttr.create("endStretchMult", "estm", MFnNumericData::kFloat, 1.0f, &status);
    nAttr.setMin(0.0f);
    INPUT_ATTR(nAttr);

    inStartSqMult = nAttr.create("startSquashMult", "ssqm", MFnNumericData::kFloat, 1.0f, &status);
    nAttr.setMin(0.0f);
    INPUT_ATTR(nAttr);

    inEndSqMult = nAttr.create("endSquashMult", "esqm", MFnNumericData::kFloat, 1.0f, &status);
    nAttr.setMin(0.0f);
    INPUT_ATTR(nAttr);

    outTranslate = nAttr.createPoint("outTranslate", "outt", &status);
    OUTPUT_ATTR(nAttr);

    MObject oRotX = uAttr.create("outRotateX", "outrx", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject oRotY = uAttr.create("outRotateY", "outry", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject oRotZ = uAttr.create("outRotateZ", "outrz", MFnUnitAttribute::kAngle, 0.0, &status);
    outRotate = nAttr.create("outRotate", "outr", oRotX, oRotY, oRotZ, &status);
    OUTPUT_ATTR(nAttr);

    MObject oScaX = nAttr.create("outScaleX", "outsx", MFnNumericData::kDouble, 1.0, &status);
    MObject oScaY = nAttr.create("outScaleY", "outsy", MFnNumericData::kDouble, 1.0, &status);
    MObject oScaZ = nAttr.create("outScaleZ", "outsz", MFnNumericData::kDouble, 1.0, &status);
    outScale = nAttr.create("outScale", "outs", oScaX, oScaY, oScaZ, &status);
    OUTPUT_ATTR(nAttr);

    outTransforms = cAttr.create("outTransforms", "trans", &status);
    cAttr.addChild(outTranslate);
    cAttr.addChild(outRotate);
    cAttr.addChild(outScale);
    cAttr.setArray(true);
    OUTPUT_ATTR(cAttr)

    addAttribute(inPrimAxis);
    addAttribute(inUpAxis);
    addAttribute(inFlatMode);
    addAttribute(inStretchScale);
    addAttribute(inRoot);
    addAttribute(inHandle);
    addAttribute(inPole);
    addAttribute(inRestStartLen);
    addAttribute(inRestEndLen);
    addAttribute(inStartJntOri);
    addAttribute(inMidJntOri);
    addAttribute(inEndJntOri);
    addAttribute(inStartOffset);
    addAttribute(inMidOffset);
    addAttribute(inEndOffset);
    addAttribute(inParInvMtx);
    addAttribute(inSoftness);
    addAttribute(inStretch);
    addAttribute(inSquash);
    addAttribute(inStartStMult);
    addAttribute(inEndStMult);
    addAttribute(inStartSqMult);
    addAttribute(inEndSqMult);
    addAttribute(outTransforms);
    attributeAffects(inPrimAxis, outTranslate);
    attributeAffects(inUpAxis, outTranslate);
    attributeAffects(inFlatMode, outTranslate);
    attributeAffects(inStretchScale, outTranslate);
    attributeAffects(inRoot, outTranslate);
    attributeAffects(inHandle, outTranslate);
    attributeAffects(inPole, outTranslate);
    attributeAffects(inRestStartLen, outTranslate);
    attributeAffects(inRestEndLen, outTranslate);
    attributeAffects(inStartJntOri, outTranslate);
    attributeAffects(inMidJntOri, outTranslate);
    attributeAffects(inEndJntOri, outTranslate);
    attributeAffects(inStartOffset, outTranslate);
    attributeAffects(inMidOffset, outTranslate);
    attributeAffects(inEndOffset, outTranslate);
    attributeAffects(inParInvMtx, outTranslate);
    attributeAffects(inSoftness, outTranslate);
    attributeAffects(inStretch, outTranslate);
    attributeAffects(inSquash, outTranslate);
    attributeAffects(inStartStMult, outTranslate);
    attributeAffects(inEndStMult, outTranslate);
    attributeAffects(inStartSqMult, outTranslate);
    attributeAffects(inEndSqMult, outTranslate);
    attributeAffects(inPrimAxis, outRotate);
    attributeAffects(inUpAxis, outRotate);
    attributeAffects(inFlatMode, outRotate);
    attributeAffects(inStretchScale, outRotate);
    attributeAffects(inRoot, outRotate);
    attributeAffects(inHandle, outRotate);
    attributeAffects(inPole, outRotate);
    attributeAffects(inRestStartLen, outRotate);
    attributeAffects(inRestEndLen, outRotate);
    attributeAffects(inStartJntOri, outRotate);
    attributeAffects(inMidJntOri, outRotate);
    attributeAffects(inEndJntOri, outRotate);
    attributeAffects(inStartOffset, outRotate);
    attributeAffects(inMidOffset, outRotate);
    attributeAffects(inEndOffset, outRotate);
    attributeAffects(inParInvMtx, outRotate);
    attributeAffects(inSoftness, outRotate);
    attributeAffects(inStretch, outRotate);
    attributeAffects(inSquash, outRotate);
    attributeAffects(inStartStMult, outRotate);
    attributeAffects(inEndStMult, outRotate);
    attributeAffects(inStartSqMult, outRotate);
    attributeAffects(inEndSqMult, outRotate);
    attributeAffects(inPrimAxis, outScale);
    attributeAffects(inUpAxis, outScale);
    attributeAffects(inFlatMode, outScale);
    attributeAffects(inStretchScale, outScale);
    attributeAffects(inRoot, outScale);
    attributeAffects(inHandle, outScale);
    attributeAffects(inPole, outScale);
    attributeAffects(inRestStartLen, outScale);
    attributeAffects(inRestEndLen, outScale);
    attributeAffects(inStartJntOri, outScale);
    attributeAffects(inMidJntOri, outScale);
    attributeAffects(inEndJntOri, outScale);
    attributeAffects(inStartOffset, outScale);
    attributeAffects(inMidOffset, outScale);
    attributeAffects(inEndOffset, outScale);
    attributeAffects(inParInvMtx, outScale);
    attributeAffects(inSoftness, outScale);
    attributeAffects(inStretch, outScale);
    attributeAffects(inSquash, outScale);
    attributeAffects(inStartStMult, outScale);
    attributeAffects(inEndStMult, outScale);
    attributeAffects(inStartSqMult, outScale);
    attributeAffects(inEndSqMult, outScale);

    return MStatus::kSuccess;
}

MVector IKSolver::axisEnumToMVector(Axis axis){
    switch (axis){
    case Axis::xAxis:
        return MVector(1.0, 0.0, 0.0);
    case Axis::xAxisNeg:
        return MVector(-1.0, 0.0, 0.0);
    case Axis::yAxis:
        return MVector(0.0, 1.0, 0.0);
    case Axis::yAxisNeg:
        return MVector(0.0, -1.0, 0.0);
    case Axis::zAxis:
        return MVector(0.0, 0.0, 1.0);
    case Axis::zAxisNeg:
        return MVector(0.0, 0.0, -1.0);
    default:
        return MVector(1.0, 0.0, 0.0);
    }
}

double IKSolver::clamp(double val, double minVal, double maxVal){
    return val < minVal ? minVal : val > maxVal ? maxVal : val;
}

MStatus IKSolver::compute(const MPlug& plug, MDataBlock& dataBlock){
    // Node computation method:
    //     * plug is a connection point related to one of our node attributes.
    //     * dataBlock contains the data on which we will base our computations.

    Axis primIndex = static_cast<Axis>(dataBlock.inputValue(inPrimAxis).asShort());
    Axis upIndex = static_cast<Axis>(dataBlock.inputValue(inUpAxis).asShort());
    bool flatMode = dataBlock.inputValue(inFlatMode).asBool();
    bool applyStretchAsScale = dataBlock.inputValue(inStretchScale).asBool();
    MMatrix rootMtx = dataBlock.inputValue(inRoot).asMatrix();
    MMatrix handleMtx = dataBlock.inputValue(inHandle).asMatrix();
    MMatrix poleMtx = dataBlock.inputValue(inPole).asMatrix();
    MMatrix parInvMtx = dataBlock.inputValue(inParInvMtx).asMatrix();
    float restStartLen = dataBlock.inputValue(inRestStartLen).asFloat();
    float restEndLen = dataBlock.inputValue(inRestEndLen).asFloat();
    MEulerRotation startJntOri = MEulerRotation(dataBlock.inputValue(inStartJntOri).asDouble3());
    MEulerRotation midJntOri = MEulerRotation(dataBlock.inputValue(inMidJntOri).asDouble3());
    MEulerRotation endJntOri = MEulerRotation(dataBlock.inputValue(inEndJntOri).asDouble3());
    MEulerRotation startOff = MEulerRotation(dataBlock.inputValue(inStartOffset).asDouble3());
    MEulerRotation midOff = MEulerRotation(dataBlock.inputValue(inMidOffset).asDouble3());
    MEulerRotation endOff = MEulerRotation(dataBlock.inputValue(inEndOffset).asDouble3());
    float softness = dataBlock.inputValue(inSoftness).asFloat();
    float stretch = dataBlock.inputValue(inStretch).asFloat();
    float squash = dataBlock.inputValue(inSquash).asFloat();
    float startStretchMult = dataBlock.inputValue(inStartStMult).asFloat();
    float endStretchMult = dataBlock.inputValue(inEndStMult).asFloat();
    float startSquashMult = dataBlock.inputValue(inStartSqMult).asFloat();
    float endSquashMult = dataBlock.inputValue(inEndSqMult).asFloat();
    MVector primAxis = axisEnumToMVector(primIndex);
    MVector upAxis = axisEnumToMVector(upIndex);
    MVector rootV = MVector(rootMtx[3][0], rootMtx[3][1], rootMtx[3][2]);
    MVector handleV = MVector(handleMtx[3][0], handleMtx[3][1], handleMtx[3][2]);
    MVector poleV = MVector(poleMtx[3][0], poleMtx[3][1], poleMtx[3][2]);
    MQuaternion startJntOriQ = startJntOri.asQuaternion();
    MQuaternion midJntOriQ = midJntOri.asQuaternion();
    MQuaternion endJntOriQ = endJntOri.asQuaternion();
    MQuaternion startOffQ = startOff.asQuaternion();
    MQuaternion midOffQ = midOff.asQuaternion();
    MQuaternion endOffQ = endOff.asQuaternion();

    // Aim quaternion.
    MVector aim = handleV - rootV;
    double aimLen = aim.length();
    aim.normalize();
    MQuaternion aimQ(primAxis, aim);

    // Up quaternion.
    MVector up = poleV - rootV;
    up.normalize();
    MVector bin = aim ^ up;
    bin.normalize();
    up = bin ^ aim;
    MVector upAdjusted = upAxis.rotateBy(aimQ);
    double angle = up.angle(upAdjusted);
    MQuaternion upQ(angle, aim);
    if (!up.isEquivalent(upAdjusted.rotateBy(upQ), 1.0e-5)){
        angle = 2.0 * M_PI - angle;
        upQ = MQuaternion(angle, aim);
    }

    // Basis quaternion.
    MQuaternion basisQ = aimQ * upQ;

    // Solver length.
    double compressionLimit = 0.1f;
    double startLen = restStartLen * startStretchMult;
    double endLen = restEndLen * endStretchMult;
    double chainLen = startLen + endLen;
    double solverLen;
    double rigidLen = clamp(aimLen, chainLen * compressionLimit, chainLen);
    double dc = chainLen;
    double da = (1.0 - softness) * dc;
    if (aimLen > da && softness > 0.0f){
        double ds = dc - da;
        double softLen = ds * (1.0 - std::pow(M_E, (da - aimLen) / ds)) + da;
        solverLen = softLen;
    }
    else
        solverLen = rigidLen;

    // Pre calculations.
    double startLenSquared = std::pow(startLen, 2.0);
    double endLenSquared = std::pow(endLen, 2.0);
    double solverLenSquared = std::pow(solverLen, 2.0);
    double stretchFactor, squashFactor;
    if (stretch > 0.0f){
        double scaleFactor;
        if (aimLen > da && softness > 0.0f)
            scaleFactor = aimLen / solverLen;
        else
            scaleFactor = aimLen / chainLen;
        if (aimLen >= da)
            stretchFactor = (1.0f - stretch) + stretch * scaleFactor;
        else
            stretchFactor = 1.0;
        squashFactor = (1.0f - squash) + squash * (1.0 / std::pow(stretchFactor, 0.5));
    }
    else{
        stretchFactor = 1.0;
        squashFactor = 1.0;
    }

    // Chain transforms.
    MMatrixArray outputs;
    MTransformationMatrix mtxFn;

    if (flatMode){
        // Flat mode.
        double curSq;
        // First output.
        MVector firstPos = rootV;
        double firstAngleCos = startLen < 0.000001 ? 0.0 :
            (startLenSquared + solverLenSquared - endLenSquared) / (2.0 * startLen * solverLen);
        firstAngleCos = clamp(firstAngleCos, -1.0, 1.0);
        double firstAngle = std::acos(firstAngleCos);
        MQuaternion firstSolverAngle(firstAngle, bin);
        MQuaternion firstRot = startOffQ * basisQ * firstSolverAngle * startJntOriQ.inverse();
        curSq = squashFactor * startSquashMult;
        double firstSca[3] = {1.0, curSq, curSq};
        mtxFn = MTransformationMatrix();
        mtxFn.setScale(firstSca, MSpace::kWorld);
        mtxFn.rotateBy(firstRot, MSpace::kWorld);
        mtxFn.setTranslation(firstPos, MSpace::kWorld);
        MMatrix firstMtx = mtxFn.asMatrix() * parInvMtx;
        outputs.append(firstMtx);
        
        // Second output.
        MVector secPos = rootV + aim.rotateBy(firstSolverAngle) * (startLen * stretchFactor);
        double secAngleCos = solverLen < 0.000001 ? 1.0 :
            (startLenSquared + endLenSquared - solverLenSquared) / (2.0 * startLen * endLen);
        secAngleCos = clamp(secAngleCos, -1.0, 1.0);
        double secAngle = std::acos(secAngleCos) + firstAngle - M_PI;
        MQuaternion secSolverAngle(secAngle, bin);
        MQuaternion secRot = midOffQ * basisQ * secSolverAngle * midJntOriQ.inverse();
        curSq = squashFactor * endSquashMult;
        double secSca[3] = {1.0, curSq, curSq};
        mtxFn = MTransformationMatrix();
        mtxFn.setScale(secSca, MSpace::kWorld);
        mtxFn.rotateBy(secRot, MSpace::kWorld);
        mtxFn.setTranslation(secPos, MSpace::kWorld);
        MMatrix secMtx = mtxFn.asMatrix() * parInvMtx;
        outputs.append(secMtx);

        // Third output.
        MVector thirdPos = rootV + (aim * (solverLen * stretchFactor));
        MQuaternion thirdRot = endOffQ * basisQ * endJntOriQ.inverse();
        double thirdSca[3] = {1.0, 1.0, 1.0};
        mtxFn = MTransformationMatrix();
        mtxFn.setScale(thirdSca, MSpace::kWorld);
        mtxFn.rotateBy(thirdRot, MSpace::kWorld);
        mtxFn.setTranslation(thirdPos, MSpace::kWorld);
        MMatrix thirdMtx = mtxFn.asMatrix() * parInvMtx;
        outputs.append(thirdMtx);
    }

    else{
        // Hierarchical mode.
        double curSt;
        double curSq;
        // First output.
        MVector firstPos = rootV;
        double firstAngleCos = startLen < 0.000001 ? 0.0 :
            (startLenSquared + solverLenSquared - endLenSquared) / (2.0 * startLen * solverLen);
        firstAngleCos = clamp(firstAngleCos, -1.0, 1.0);
        double firstAngle = std::acos(firstAngleCos);
        MQuaternion firstSolverAngle(firstAngle, bin);
        MQuaternion firstRot = startOffQ * basisQ * firstSolverAngle;
        curSt = applyStretchAsScale ? stretchFactor : 1.0;
        curSq = squashFactor * startSquashMult;
        double firstSca[3] = {curSt, curSq, curSq};
        mtxFn = MTransformationMatrix();
        mtxFn.setScale(firstSca, MSpace::kWorld);
        mtxFn.rotateBy(firstRot * startJntOriQ.inverse(), MSpace::kWorld);
        mtxFn.setTranslation(firstPos, MSpace::kWorld);
        MMatrix firstMtx = mtxFn.asMatrix() * parInvMtx;
        outputs.append(firstMtx);

        // Second output.
        MVector secPos = primAxis * startLen;
        if (!applyStretchAsScale)
            secPos *= stretchFactor;
        double secAngleCos = solverLen < 0.000001 ? 1.0 :
            (startLenSquared + endLenSquared - solverLenSquared) / (2.0 * startLen * endLen);
        secAngleCos = clamp(secAngleCos, -1.0, 1.0);
        double secAngle = std::acos(secAngleCos) - M_PI;
        MQuaternion secSolverAngle(secAngle, bin);
        MQuaternion secRot = firstRot * secSolverAngle * firstRot.inverse();
        curSt = applyStretchAsScale ? stretchFactor : 1.0;
        curSq = squashFactor * endSquashMult;
        double secSca[3] = {curSt, curSq, curSq};
        mtxFn = MTransformationMatrix();
        mtxFn.setScale(secSca, MSpace::kWorld);
        mtxFn.rotateBy(secRot * midJntOriQ.inverse(), MSpace::kWorld);
        mtxFn.setTranslation(secPos, MSpace::kWorld);
        MMatrix secMtx = mtxFn.asMatrix();
        outputs.append(secMtx);

        // Third output.
        MVector thirdPos = primAxis * endLen;
        if (!applyStretchAsScale)
            thirdPos *= stretchFactor;
        double thirdAngle = M_PI - (secAngle + M_PI) - firstAngle;
        MQuaternion thirdSolverAngle(thirdAngle, bin);
        MQuaternion parentRot = startOffQ * basisQ * secSolverAngle;
        MQuaternion thirdRot = parentRot * thirdSolverAngle * parentRot.inverse();
        double thirdSca[3] = {1.0, 1.0, 1.0};
        mtxFn = MTransformationMatrix();
        mtxFn.setScale(thirdSca, MSpace::kWorld);
        mtxFn.rotateBy(thirdRot * endJntOriQ.inverse(), MSpace::kWorld);
        mtxFn.setTranslation(thirdPos, MSpace::kWorld);
        MMatrix thirdMtx = mtxFn.asMatrix();
        outputs.append(thirdMtx);
    }

    // Output transformations.
    MArrayDataHandle outTransHandle = dataBlock.outputArrayValue(outTransforms);
    for (unsigned int i = 0; i < outTransHandle.elementCount(); i++){
        outTransHandle.jumpToArrayElement(i);
        MDataHandle curTransHandle = outTransHandle.outputValue();
        MDataHandle transHandle = curTransHandle.child(outTranslate);
        MDataHandle rotHandle = curTransHandle.child(outRotate);
        MDataHandle scaHandle = curTransHandle.child(outScale);
        mtxFn = MTransformationMatrix(outputs[i]);
        if (outputs.length() - 1 < i){
            transHandle.setMFloatVector(MFloatVector(0.0f, 0.0f, 0.0f));
            rotHandle.setMVector(MVector(0.0, 0.0, 0.0));
            scaHandle.setMVector(MVector(0.0, 0.0, 0.0));
        }
        else{
            MVector curPos = mtxFn.getTranslation(MSpace::kWorld);
            MVector curRot = mtxFn.rotation().asEulerRotation().asVector();
            double sca[3];
            mtxFn.getScale(sca, MSpace::kWorld);
            MVector curSca(sca);
            transHandle.setMFloatVector(curPos);
            rotHandle.setMVector(curRot);
            scaHandle.setMVector(curSca);
        }
    }
    outTransHandle.setAllClean();
    

    return MStatus::kSuccess;
}