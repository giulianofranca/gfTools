#include "headers/n_gfRigPSDVectorAngle.h"

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
VectorAnglePSD::VectorAnglePSD() {}

// Destructor.
VectorAnglePSD::~VectorAnglePSD() {}

MObject VectorAnglePSD::inBase;
MObject VectorAnglePSD::inSource;
MObject VectorAnglePSD::inTarget;
MObject VectorAnglePSD::inTargetEnvelope;
MObject VectorAnglePSD::inTargetFalloff;
MObject VectorAnglePSD::inRampWeights;
MObject VectorAnglePSD::outWeights;


static float degToRad(float deg){
    // Convert degrees to radians.
    return deg * (static_cast<float>(M_PI) / 180.0f);
}

void VectorAnglePSD::postConstructor(){
    // Post Constructor.
    MObject thisMob = thisMObject();
    MRampAttribute ramp = MRampAttribute(thisMob, inRampWeights);
    MFloatArray pos = MFloatArray();
    MFloatArray val = MFloatArray();
    MIntArray interp = MIntArray();
    pos.append(1.0f);
    val.append(1.0f);
    interp.append(MRampAttribute::kLinear);
    ramp.addEntries(pos, val, interp);
}

void* VectorAnglePSD::creator(){
    // Maya creator function.
    return new VectorAnglePSD();
}

MStatus VectorAnglePSD::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to IKVChain class. Instances of IKVChain will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnMatrixAttribute mAttr;
    MFnNumericAttribute nAttr;
    MRampAttribute rAttr;

    inBase = mAttr.create("base", "base", MFnMatrixAttribute::kFloat, &status);
    INPUT_ATTR(mAttr);

    inSource = mAttr.create("source", "source", MFnMatrixAttribute::kFloat, &status);
    INPUT_ATTR(mAttr);

    inTarget = mAttr.create("target", "target", MFnMatrixAttribute::kFloat, &status);
    mAttr.setArray(true);
    INPUT_ATTR(mAttr);

    inTargetEnvelope = nAttr.create("targetEnvelope", "te", MFnNumericData::kFloat, 1.0f, &status);
    nAttr.setMin(0.0f);
    nAttr.setMax(1.0f);
    nAttr.setArray(true);
    INPUT_ATTR(nAttr);

    inTargetFalloff = nAttr.create("targetFalloff", "tf", MFnNumericData::kFloat, 90.0f, &status);
    nAttr.setMin(0.0f);
    nAttr.setMax(180.0f);
    nAttr.setArray(true);
    INPUT_ATTR(nAttr);

    inRampWeights = rAttr.createCurveRamp("rampWeights", "rw", &status);

    outWeights = nAttr.create("outWeights", "ow", MFnNumericData::kFloat, 0.0f, &status);
    nAttr.setArray(true);
    OUTPUT_ATTR(nAttr);

    addAttribute(inBase);
    addAttribute(inSource);
    addAttribute(inTarget);
    addAttribute(inTargetEnvelope);
    addAttribute(inTargetFalloff);
    addAttribute(inRampWeights);
    addAttribute(outWeights);
    attributeAffects(inBase, outWeights);
    attributeAffects(inSource, outWeights);
    attributeAffects(inTarget, outWeights);
    attributeAffects(inTargetEnvelope, outWeights);
    attributeAffects(inTargetFalloff, outWeights);
    attributeAffects(inRampWeights, outWeights);

    return status;
}

MStatus VectorAnglePSD::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outWeights)
        return MStatus::kUnknownParameter;

    MFloatMatrix mBase = dataBlock.inputValue(inBase).asFloatMatrix();
    MFloatMatrix mSource = dataBlock.inputValue(inSource).asFloatMatrix();

    MArrayDataHandle targetHandle = dataBlock.inputArrayValue(inTarget);
    MArrayDataHandle targetEnvelopeHandle = dataBlock.inputArrayValue(inTargetEnvelope);
    MArrayDataHandle targetFalloffHandle = dataBlock.inputArrayValue(inTargetFalloff);
    MArrayDataHandle outWeightsHandle = dataBlock.inputArrayValue(outWeights);

    MFloatVector vBase = MFloatVector(mBase[3][0], mBase[3][1], mBase[3][2]);
    MFloatVector vSource = MFloatVector(mSource[3][0], mSource[3][1], mSource[3][2]);

    MFloatVector vCurPose = vSource - vBase;
    MFloatVector nCurPose = vCurPose.normal();

    std::vector<MFloatVector> targetList;
    std::vector<float> envelopeList;
    std::vector<float> falloffList;
    
    for (uint32_t i = 0; i < targetHandle.elementCount(); i++){
        targetHandle.jumpToArrayElement(i);
        MFloatMatrix mtx = targetHandle.inputValue().asFloatMatrix();
        MFloatVector vec = MFloatVector(mtx[3][0], mtx[3][1], mtx[3][2]);
        MFloatVector vTargetPose = vec - vBase;
        MFloatVector nTargetPose = vTargetPose.normal();
        targetList.push_back(nTargetPose);
    }

    for (uint32_t i = 0; i < targetEnvelopeHandle.elementCount(); i++){
        targetEnvelopeHandle.jumpToArrayElement(i);
        float env = targetEnvelopeHandle.inputValue().asFloat();
        envelopeList.push_back(env);
    }

    for (uint32_t i = 0; i < targetFalloffHandle.elementCount(); i++){
        targetFalloffHandle.jumpToArrayElement(i);
        float fall = targetFalloffHandle.inputValue().asFloat();
        falloffList.push_back(fall);
    }

    for(uint32_t i = 0; i < outWeightsHandle.elementCount(); i++){
        outWeightsHandle.jumpToArrayElement(i);
        MDataHandle resultHandle = outWeightsHandle.outputValue();
        if ((i < outWeightsHandle.elementCount()) &&
            (i < targetHandle.elementCount()) &&
            (i < targetEnvelopeHandle.elementCount()) &&
            (i < targetFalloffHandle.elementCount())){
                float theta = std::acosf(targetList[i] * nCurPose);
                float ratio = std::min(std::max(theta / degToRad(falloffList[i]), -1.0f), 1.0f);
                float weight;
                if (ratio == 0.0f)
                    weight = envelopeList[i];
                else if (ratio > 0.0f)
                    weight = envelopeList[i] * (1.0f - ratio);
                else if (ratio < 0.0f)
                    weight = envelopeList[i] * (1.0f + ratio);

                MObject thisMob = thisMObject();
                MRampAttribute rampAttr = MRampAttribute(thisMob, inRampWeights);
                float resultWeight;
                rampAttr.getValueAtPosition(weight, resultWeight);
                resultHandle.setFloat(resultWeight);
            }
        else
            resultHandle.setFloat(0.0f);
        
        resultHandle.setClean();
    }

    return MStatus::kSuccess;
}