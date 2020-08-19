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

MObject TwistExtractor::inRotation;
MObject TwistExtractor::inRotationOrder;
MObject TwistExtractor::inUseUpVec;
MObject TwistExtractor::inUpVec;
MObject TwistExtractor::inInvTwist;
MObject TwistExtractor::inRevDist;
MObject TwistExtractor::outTwist;
MObject TwistExtractor::outTwistDist;

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
    MFnUnitAttribute uAttr;
    MFnNumericAttribute nAttr;
    MFnEnumAttribute eAttr;

    MObject rotX = uAttr.create("rotationX", "rotx", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject rotY = uAttr.create("rotationY", "roty", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject rotZ = uAttr.create("rotationZ", "rotz", MFnUnitAttribute::kAngle, 0.0, &status);
    inRotation = nAttr.create("rotation", "rot", rotX, rotY, rotZ, &status);
    INPUT_ATTR(nAttr);

    inRotationOrder = eAttr.create("rotationOrder", "roo", 0, &status);
    eAttr.addField("xyz", 0);
    eAttr.addField("yzx", 1);
    eAttr.addField("zxy", 2);
    eAttr.addField("xzy", 3);
    eAttr.addField("yxz", 4);
    eAttr.addField("zyx", 5);
    INPUT_ATTR(eAttr);

    inUseUpVec = nAttr.create("useUpVector", "useup", MFnNumericData::kBoolean, false, &status);
    INPUT_ATTR(nAttr);

    inUpVec = nAttr.createPoint("upVector", "upVector", &status);
    nAttr.setDefault(0.0, 1.0, 0.0);
    INPUT_ATTR(nAttr);

    inInvTwist = nAttr.create("inverseTwist", "itwist", MFnNumericData::kBoolean, false, &status);
    INPUT_ATTR(nAttr);

    inRevDist = nAttr.create("reverseDistribution", "rdist", MFnNumericData::kBoolean, false, &status);
    INPUT_ATTR(nAttr);

    outTwist = uAttr.create("twist", "twist", MFnUnitAttribute::kAngle, 0.0, &status);
    OUTPUT_ATTR(uAttr);

    outTwistDist = uAttr.create("twistDistribution", "twistd", MFnUnitAttribute::kAngle, 0.0, &status);
    uAttr.setArray(true);
    OUTPUT_ATTR(uAttr);

    addAttribute(inRotation);
    addAttribute(inRotationOrder);
    addAttribute(inUseUpVec);
    addAttribute(inUpVec);
    addAttribute(inInvTwist);
    addAttribute(inRevDist);
    addAttribute(outTwist);
    addAttribute(outTwistDist);
    attributeAffects(rotX, outTwist);
    attributeAffects(rotY, outTwist);
    attributeAffects(rotZ, outTwist);
    attributeAffects(inRotationOrder, outTwist);
    attributeAffects(inUseUpVec, outTwist);
    attributeAffects(inUpVec, outTwist);
    attributeAffects(inInvTwist, outTwist);
    attributeAffects(rotX, outTwistDist);
    attributeAffects(rotY, outTwistDist);
    attributeAffects(rotZ, outTwistDist);
    attributeAffects(inRotationOrder, outTwistDist);
    attributeAffects(inUseUpVec, outTwistDist);
    attributeAffects(inUpVec, outTwistDist);
    attributeAffects(inInvTwist, outTwistDist);
    attributeAffects(inRevDist, outTwistDist);

    return status;
}

MStatus TwistExtractor::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    double3& rotation = dataBlock.inputValue(inRotation).asDouble3();
    short rotOrder = dataBlock.inputValue(inRotationOrder).asShort();
    MEulerRotation eRoll = MEulerRotation(rotation, (MEulerRotation::RotationOrder)rotOrder);
    bool useUpVec = dataBlock.inputValue(inUseUpVec).asBool();
    bool invTwist = dataBlock.inputValue(inInvTwist).asBool();

    MEulerRotation::RotationOrder twistOrder = MEulerRotation::RotationOrder::kXYZ;
    eRoll.reorderIt(twistOrder);

    MTransformationMatrix mtxFn = MTransformationMatrix();
    mtxFn.rotateBy(eRoll, MSpace::kWorld);
    MMatrix mRoll = mtxFn.asMatrix();

    MQuaternion qNonRoll = MQuaternion();
    MVector nAim = MVector(mRoll[0][0], mRoll[0][1], mRoll[0][2]);
    nAim.normalize();
    MVector nAimAxis = MVector::xAxis;
    MQuaternion qAim = MQuaternion(nAimAxis, nAim);
    qNonRoll *= qAim;

    if (useUpVec){
        MVector vUp = MVector(dataBlock.inputValue(inUpVec).asFloat3());
        MVector nNormal = vUp - ((vUp * nAim) * nAim);
        nNormal.normalize();
        MVector nUp = MVector::yAxis.rotateBy(qAim);
        double angle = nUp.angle(nNormal);
        MQuaternion qNormal = MQuaternion(angle, nAim);
        if (!nNormal.isEquivalent(nUp.rotateBy(qNormal), 1.0e-5)){
            angle = 2.0 * M_PI - angle;
            qNormal = MQuaternion(angle, nAim);
        };
        qNonRoll *= qNormal;
    }
    MEulerRotation eNonRoll = qNonRoll.asEulerRotation();
    eNonRoll = MEulerRotation(eNonRoll.x, eNonRoll.y, eNonRoll.z, twistOrder);

    MQuaternion qRoll = eRoll.asQuaternion();
    MQuaternion qExtract180 = qNonRoll * qRoll.inverse();
    MEulerRotation eExtract180 = qExtract180.asEulerRotation();
    double twist = -eExtract180.x;
    if (invTwist)
        twist *= -1.0;

    if (plug == outTwist){
        MDataHandle outTwistHdle = dataBlock.outputValue(outTwist);
        outTwistHdle.setMAngle(MAngle(twist));
        outTwistHdle.setClean();
    }

    if (plug == outTwistDist){
        bool revDist = dataBlock.inputValue(inRevDist).asBool();
        MArrayDataHandle outTwistDistHdle = dataBlock.outputArrayValue(outTwistDist);
        uint32_t outputs = outTwistDistHdle.elementCount();
        double step = outputs > 1 ? twist / (outputs - 1) : twist;
        std::vector<uint32_t> outList(outputs);
        std::iota(std::begin(outList), std::end(outList), 0);   // Equivalent to range()
        if (!revDist)
            std::reverse(std::begin(outList), std::end(outList));
        for (uint32_t i = 0; i < outList.size(); i++){
            outTwistDistHdle.jumpToArrayElement(i);
            MDataHandle resultHdle = outTwistDistHdle.outputValue();
            double result = outputs > 1 ? step * outList[i] : twist;
            resultHdle.setMAngle(MAngle(result));
        }
        outTwistDistHdle.setAllClean();
    }

    return MStatus::kSuccess;
}