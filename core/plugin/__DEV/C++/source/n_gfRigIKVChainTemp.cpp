#include "n_gfRigIKVChain.h"

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
MObject IKVChainSolver::inPreferredAngle;
MObject IKVChainSolver::inPvMode;
MObject IKVChainSolver::inTwist;
MObject IKVChainSolver::inHierarchyMode;
MObject IKVChainSolver::inRestLength1;
MObject IKVChainSolver::inRestLength2;
MObject IKVChainSolver::inCompressionLimit;
MObject IKVChainSolver::inSoftness;
MObject IKVChainSolver::inStretch;
MObject IKVChainSolver::inClampStretch;
MObject IKVChainSolver::inClampValue;
MObject IKVChainSolver::inSquash;
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

    inRoot = mAttr.create("root", "root", MFnMatrixAttribute::kFloat, &status);
    INPUT_ATTR(mAttr);

    inHandle = mAttr.create("handle", "handle", MFnMatrixAttribute::kFloat, &status);
    INPUT_ATTR(mAttr);

    inUpVector = mAttr.create("upVector", "up", MFnMatrixAttribute::kFloat, &status);
    INPUT_ATTR(mAttr);

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

    inStretch = nAttr.create("stretch", "st", MFnNumericData::kFloat, 0.0f, &status);
    nAttr.setMin(0.0f);
    nAttr.setMax(1.0f);
    INPUT_ATTR(nAttr);

    inClampStretch = nAttr.create("clampStretch", "cst", MFnNumericData::kFloat, 0.0f, &status);
    nAttr.setMin(0.0f);
    nAttr.setMax(1.0f);
    INPUT_ATTR(nAttr);

    inClampValue = nAttr.create("clampValue", "cstv", MFnNumericData::kFloat, 1.5f, &status);
    nAttr.setMin(1.0f);
    nAttr.setSoftMax(1.8f);
    INPUT_ATTR(nAttr);

    inSquash = nAttr.create("squash", "sq", MFnNumericData::kFloat, 0.0f, &status);
    nAttr.setMin(0.0f);
    nAttr.setMax(1.0f);
    INPUT_ATTR(nAttr);

    outChain = mAttr.create("outChain", "oc", MFnMatrixAttribute::kFloat, &status);
    mAttr.setArray(true);
    OUTPUT_ATTR(mAttr);

    addAttribute(inRoot);
    addAttribute(inHandle);
    addAttribute(inUpVector);
    addAttribute(inPreferredAngle);
    addAttribute(inPvMode);
    addAttribute(inTwist);
    addAttribute(inHierarchyMode);
    addAttribute(inRestLength1);
    addAttribute(inRestLength2);
    addAttribute(inCompressionLimit);
    addAttribute(inSoftness);
    addAttribute(inStretch);
    addAttribute(inClampStretch);
    addAttribute(inClampValue);
    addAttribute(inSquash);
    addAttribute(outChain);
    attributeAffects(inRoot, outChain);
    attributeAffects(inHandle, outChain);
    attributeAffects(inUpVector, outChain);
    attributeAffects(inPreferredAngle, outChain);
    attributeAffects(inPvMode, outChain);
    attributeAffects(inTwist, outChain);
    attributeAffects(inHierarchyMode, outChain);
    attributeAffects(inRestLength1, outChain);
    attributeAffects(inRestLength2, outChain);
    attributeAffects(inCompressionLimit, outChain);
    attributeAffects(inSoftness, outChain);
    attributeAffects(inStretch, outChain);
    attributeAffects(inClampStretch, outChain);
    attributeAffects(inClampValue, outChain);
    attributeAffects(inSquash, outChain);

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
    short pvMode = dataBlock.inputValue(inPvMode).asShort();
    MFloatMatrix mRoot = dataBlock.inputValue(inRoot).asFloatMatrix();
    MFloatMatrix mHandle = dataBlock.inputValue(inHandle).asFloatMatrix();
    MFloatMatrix mUpVector = dataBlock.inputValue(inUpVector).asFloatMatrix();
    double prefAngle = dataBlock.inputValue(inPreferredAngle).asAngle().asRadians();
    double twist = dataBlock.inputValue(inTwist).asAngle().asRadians();
    MFloatVector vRoot = MFloatVector(mRoot[3][0], mRoot[3][1], mRoot[3][2]);
    MFloatVector vHandle = MFloatVector(mHandle[3][0], mHandle[3][1], mHandle[3][2]);
    MFloatVector vUpVector = MFloatVector(mUpVector[3][0], mUpVector[3][1], mUpVector[3][2]);
    MFloatVector vXDirection = vHandle - vRoot;
    float xDist = vXDirection.length();
    MFloatVector nXAxis = vXDirection.normal();
    MFloatVector nYAxis;
    if (pvMode == 0){
        MFloatVector vUpDirection = vUpVector - vRoot;
        MFloatVector vYDirection = vUpDirection - ((vUpDirection * nXAxis) * nXAxis);
        nYAxis = vYDirection.normal();
    }
    else
        nYAxis = MFloatVector(std::cosf(static_cast<float>(prefAngle)), 0.0f, std::sinf(static_cast<float>(prefAngle)));
    MFloatVector nZAxis = nXAxis ^ nYAxis;
    float basis[4][4] = {
        nXAxis.x, nXAxis.y, nXAxis.z, 0.0f,
        nYAxis.x, nYAxis.y, nYAxis.z, 0.0f,
        nZAxis.x, nZAxis.y, nZAxis.z, 0.0f,
        vRoot.x, vRoot.y, vRoot.z, 1.0f
    };
    MFloatMatrix mBasisLocal = MFloatMatrix(basis);
    MFloatMatrix mTwist = MFloatMatrix();
    mTwist[1][1] = std::cosf(static_cast<float>(twist));
    mTwist[1][2] = std::sinf(static_cast<float>(twist));
    mTwist[2][1] = -std::sinf(static_cast<float>(twist));
    mTwist[2][2] = std::cosf(static_cast<float>(twist));
    MFloatMatrix mBasis;
    if (pvMode == 0)
        mBasis = mBasisLocal;
    else
        mBasis = mTwist * mBasisLocal;

    // Solve triangle
    float l1 = dataBlock.inputValue(inRestLength1).asFloat();
    float l2 = dataBlock.inputValue(inRestLength2).asFloat();
    float compressionLimit = dataBlock.inputValue(inCompressionLimit).asFloat();
    float softValue = dataBlock.inputValue(inSoftness).asFloat();
    float l1m = l1;
    float l2m = l2;
    float chainLength = l1m + l2m;
    float l3rigid = std::max(std::min(xDist, chainLength), chainLength * compressionLimit);
    float dc = chainLength;
    float da = (1.0f - softValue) * dc;
    float l3;
    float l3soft = 1.0f;
    if ((xDist > da) && (softValue > 0.0f)){
        float ds = dc - da;
        l3soft = ds * (1.0f - std::powf(static_cast<float>(M_E), (da - xDist) / ds)) + da;
        l3 = l3soft;
    }
    else
        l3 = l3rigid;

    // Angle mesurement
    bool hierarchyMode = dataBlock.inputValue(inHierarchyMode).asBool();
    float betaCos = (std::powf(l1m, 2.0f) + std::powf(l3, 2.0f) - std::powf(l2m, 2.0f)) / (2.0f * l1m * l3);
    if (betaCos < -1.0f)
        betaCos = -1.0f;
    float beta = std::acosf(betaCos);
    float betaSin = std::sinf(beta);
    float gammaCos = (std::powf(l1m, 2.0f) + std::powf(l2m, 2.0f) - std::powf(l3, 2.0f)) / (2.0f * l1m * l2m);
    if (gammaCos > 1.0f)
        gammaCos = 1.0f;
    float gamma = std::acosf(gammaCos);
    float gammaComplement;
    if (hierarchyMode == true)
        gammaComplement = gamma - static_cast<float>(M_PI);
    else
        gammaComplement = gamma + beta - static_cast<float>(M_PI);
    float gammaComplementCos = std::cosf(gammaComplement);
    float gammaComplementSin = std::sinf(gammaComplement);
    float alpha = static_cast<float>(M_PI) - beta - gamma;
    float alphaCos = std::cosf(alpha);
    float alphaSin = std::sinf(alpha);

    // Cartoony features
    float stretch = dataBlock.inputValue(inStretch).asFloat();
    float stretchFactor;
    float squashFactor;
    if (stretch > 0.0f){
        float clampStretch = dataBlock.inputValue(inClampStretch).asFloat();
        float clampStretchValue = dataBlock.inputValue(inClampValue).asFloat();
        float squash = dataBlock.inputValue(inSquash).asFloat();
        float scaleFactor;
        if ((xDist > da) && (softValue > 0.0f))
            scaleFactor = xDist / l3soft;
        else
            scaleFactor = xDist / chainLength;
        if (xDist >= da){
            float clampFactor = (1.0f - clampStretch) * scaleFactor + clampStretch * std::min(scaleFactor, clampStretchValue);
            stretchFactor = (1.0f - stretch) + stretch * clampFactor;
        }
        else
            stretchFactor = 1.0f;
        squashFactor = (1.0f - squash) + squash * (1.0f / std::sqrtf(stretchFactor));
    }
    else{
        stretchFactor = 1.0f;
        squashFactor = 1.0f;
    }

    // Output transforms
    MArrayDataHandle outChainHandle = dataBlock.outputArrayValue(outChain);
    std::vector<MFloatMatrix> srtList;

    MFloatMatrix mScale;
    MFloatMatrix mLocal;
    MFloatMatrix mResult;

    if (hierarchyMode){
        mScale = MFloatMatrix();
        mScale[0][0] = stretchFactor;
        mScale[1][1] = squashFactor;
        mScale[2][2] = squashFactor;
        mLocal = MFloatMatrix();
        mLocal[0][0] = betaCos;
        mLocal[0][1] = betaSin;
        mLocal[1][0] = -betaSin;
        mLocal[1][1] = betaCos;
        mResult = mScale * mLocal * mBasis;
        srtList.push_back(mResult);
        mLocal = MFloatMatrix();
        mLocal[0][0] = gammaComplementCos;
        mLocal[0][1] = gammaComplementSin;
        mLocal[1][0] = -gammaComplementSin;
        mLocal[1][1] = gammaComplementCos;
        mResult = mScale * mLocal;
        mResult[3][0] = l1m;
        srtList.push_back(mResult);
        mLocal = MFloatMatrix();
        mLocal[0][0] = alphaCos;
        mLocal[0][1] = alphaSin;
        mLocal[1][0] = -alphaSin;
        mLocal[1][1] = alphaCos;
        mLocal[3][0] = l2m;
        srtList.push_back(mLocal);
    }
    else{
        mScale = MFloatMatrix();
        mScale[0][0] = stretchFactor;
        mScale[1][1] = squashFactor;
        mScale[2][2] = squashFactor;
        mLocal = MFloatMatrix();
        mLocal[0][0] = betaCos;
        mLocal[0][1] = betaSin;
        mLocal[1][0] = -betaSin;
        mLocal[1][1] = betaCos;
        mResult = mScale * mLocal * mBasis;
        srtList.push_back(mResult);
        mLocal = MFloatMatrix();
        mLocal[0][0] = gammaComplementCos;
        mLocal[0][1] = gammaComplementSin;
        mLocal[1][0] = -gammaComplementSin;
        mLocal[1][1] = gammaComplementCos;
        mLocal[3][0] = betaCos * l1m * stretchFactor;
        mLocal[3][1] = betaSin * l1m * stretchFactor;
        mResult = mScale * mLocal * mBasis;
        srtList.push_back(mResult);
        mLocal = mHandle;
        mLocal[3][0] = mBasis[3][0] + mBasis[0][0] * l3 * stretchFactor;
        mLocal[3][1] = mBasis[3][1] + mBasis[0][1] * l3 * stretchFactor;
        mLocal[3][2] = mBasis[3][2] + mBasis[0][2] * l3 * stretchFactor;
        mResult = mScale * mLocal;
        srtList.push_back(mResult);
    }

    for (uint32_t i = 0; i < outChainHandle.elementCount(); i++){
        outChainHandle.jumpToArrayElement(i);
        MDataHandle resultHandle = outChainHandle.outputValue();
        if ((i < outChainHandle.elementCount()) && (i < srtList.size()))
            resultHandle.setMFloatMatrix(srtList[i]);
        else
            resultHandle.setMFloatMatrix(MFloatMatrix());
    }

    outChainHandle.setAllClean();

    return MStatus::kSuccess;
}