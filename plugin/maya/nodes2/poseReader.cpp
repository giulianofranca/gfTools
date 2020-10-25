#include "headers/poseReader.hpp"

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
PoseReader::PoseReader(){}
PoseReader::~PoseReader(){}


// Members initialization
MObject PoseReader::inMode;
MObject PoseReader::inTarget;
MObject PoseReader::inTargetAxis;
MObject PoseReader::inVecAngInterp;
MObject PoseReader::inPose;
MObject PoseReader::inEnvelope;
MObject PoseReader::inPosition;
MObject PoseReader::inStartAngle;
MObject PoseReader::outWeight;




MPxNode::SchedulingType PoseReader::schedulingType() const{
    return MPxNode::SchedulingType::kParallel;
}

void* PoseReader::creator(){
    return new PoseReader();
}

MStatus PoseReader::initialize(){
    // Defines the set of attributes for this node. The attributes declared in this 
    // function are assigned as static members to PoseReader class. Instances of 
    // PoseReader will use these attributes to create plugs for use in the compute()
    // method.
    MStatus status;
    MFnMatrixAttribute mAttr;
    MFnEnumAttribute eAttr;
    MFnCompoundAttribute cAttr;
    MFnNumericAttribute nAttr;
    MRampAttribute rAttr;

    inMode = eAttr.create("mode", "mode", 0, &status);
    eAttr.addField("Vector Angle", Mode::vectorAngle);
    eAttr.addField("RBF", Mode::rbf);
    INPUT_ATTR(eAttr);

    inTarget = mAttr.create("target", "tgt", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inTargetAxis = eAttr.create("targetAxis", "taxis", 0, &status);
    eAttr.addField("X Axis", Axis::xAxis);
    eAttr.addField("Y Axis", Axis::yAxis);
    eAttr.addField("Z Axis", Axis::zAxis);
    INPUT_ATTR(eAttr);

    inVecAngInterp = rAttr.createCurveRamp("vectorAngleInterpolation", "vai", &status);

    inEnvelope = nAttr.create("envelope", "env", MFnNumericData::kFloat, 1.0f, &status);
    nAttr.setMin(0.0f);
    nAttr.setMax(1.0f);
    INPUT_ATTR(nAttr);

    inPosition = nAttr.createPoint("position", "pos", &status);
    INPUT_ATTR(nAttr);

    inStartAngle = nAttr.create("startAngle", "ma", MFnNumericData::kFloat, 90.0f, &status);
    nAttr.setMin(0.001f);
    nAttr.setMax(180.0f);
    INPUT_ATTR(nAttr);

    outWeight = nAttr.create("outWeight", "ow", MFnNumericData::kFloat, 0.0f, &status);
    nAttr.setArray(true);
    OUTPUT_ATTR(nAttr);

    inPose = cAttr.create("pose", "pose", &status);
    cAttr.addChild(inEnvelope);
    cAttr.addChild(inPosition);
    cAttr.addChild(inStartAngle);
    cAttr.setArray(true);

    addAttribute(inMode);
    addAttribute(inTarget);
    addAttribute(inTargetAxis);
    addAttribute(inVecAngInterp);
    addAttribute(inPose);
    addAttribute(outWeight);
    attributeAffects(inMode, outWeight);
    attributeAffects(inTarget, outWeight);
    attributeAffects(inTargetAxis, outWeight);
    attributeAffects(inVecAngInterp, outWeight);
    attributeAffects(inEnvelope, outWeight);
    attributeAffects(inPosition, outWeight);
    attributeAffects(inStartAngle, outWeight);

    return MStatus::kSuccess;
}

void PoseReader::postConstructor(){
    // Internally Maya creates two objects when a user defined node is created, the
    // internal MObject and the user derived object. The association between the these
    // two objects is not made until after the MPxNode constructor is called. This
    // implies that no MPxNode member function can be called from the MPxNode
    // constructor. The postConstructor will get called immediately after the
    // constructor when it is safe to call any MPxNode member function.
    MObject thisMob = thisMObject();
    MRampAttribute ramp = MRampAttribute(thisMob, inVecAngInterp);
    MFloatArray pos, val;
    MIntArray interp;
    pos.append(1.0f);
    val.append(1.0f);
    interp.append(MRampAttribute::kLinear);
    ramp.addEntries(pos, val, interp);
}

void PoseReader::degToRad(float& deg){
    // Convert a degrees angle value to radians.
    deg = deg * (static_cast<float>(M_PI) / 180.0f);
}

MStatus PoseReader::compute(const MPlug& plug, MDataBlock& dataBlock){
    // Node computation method:
    //     * plug is a connection point related to one of our node attributes.
    //     * dataBlock contains the data on which we will base our computations.
    if (plug != outWeight)
        return MStatus::kUnknownParameter;

    short mode = dataBlock.inputValue(inMode).asShort();
    MMatrix mTarget = dataBlock.inputValue(inTarget).asMatrix();
    MArrayDataHandle poseHandle = dataBlock.inputArrayValue(inPose);
    MArrayDataHandle outWeightHandle = dataBlock.outputArrayValue(outWeight);

    MVector targetPos = MVector(mTarget[3][0], mTarget[3][1], mTarget[3][2]);
    MFloatArray weights;

    if (mode == Mode::vectorAngle){
        // Vector Angle algorithm
        short axis = dataBlock.inputValue(inTargetAxis).asShort();
        MRampAttribute interpolation = MRampAttribute(thisMObject(), inVecAngInterp);
        MVector vTarget;
        switch (axis){
            case Axis::xAxis:
                vTarget = MVector(mTarget[0][0], mTarget[0][1], mTarget[0][2]);
                break;
            case Axis::yAxis:
                vTarget = MVector(mTarget[1][0], mTarget[1][1], mTarget[1][2]);
                break;
            case Axis::zAxis:
                vTarget = MVector(mTarget[2][0], mTarget[2][1], mTarget[2][2]);
                break;
        }
        vTarget.normalize();

        for (unsigned int i = 0; i < poseHandle.elementCount(); i++){
            poseHandle.jumpToArrayElement(i);
            MDataHandle curPoseHandle = poseHandle.inputValue();
            float envelope = curPoseHandle.child(inEnvelope).asFloat();
            MVector pos = MVector(curPoseHandle.child(inPosition).asFloat3());
            float startAngle = curPoseHandle.child(inStartAngle).asFloat();
            degToRad(startAngle);
            MVector vPose = pos - targetPos;
            vPose.normalize();

            float theta = std::acos(vPose * vTarget);
            float ratio = std::max(1.0f - (theta / startAngle), 0.0f);
            float weight = ratio * envelope;
            float finalWeight;
            interpolation.getValueAtPosition(weight, finalWeight);
            weights.append(finalWeight);
        }
    }
    else if (mode == Mode::rbf){
        // Radial Basis Function algorithm
        MString toPrint("RBF mode is not implemented yet. You should use Vector Angle mode.");
        MGlobal::displayWarning(toPrint);
    }

    for (unsigned int i = 0; i < outWeightHandle.elementCount(); i++){
        outWeightHandle.jumpToArrayElement(i);
        MDataHandle resultHandle = outWeightHandle.outputValue();
        if (i < weights.length())
            resultHandle.setFloat(weights[i]);
        else
            resultHandle.setFloat(0.0f);
    }
    outWeightHandle.setAllClean();

    return MStatus::kSuccess;
}