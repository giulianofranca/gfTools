#include "headers/n_gfUtilPoleVectorConstraint.h"

// Configure a input attribute.
#define INPUT_ATTR(FNATTR)      \
    FNATTR.setWritable(true);   \
    FNATTR.setReadable(true);   \
    FNATTR.setStorable(true);   \
    FNATTR.setKeyable(true);    \

// Configure a input attribute.
#define OUTPUT_ATTR(FNATTR)     \
    FNATTR.setWritable(false);  \
    FNATTR.setReadable(true);   \
    FNATTR.setStorable(false);  \
    FNATTR.setKeyable(false);   \

// Constructor.
PoleVectorConstraint::PoleVectorConstraint(){}

// Destructor.
PoleVectorConstraint::~PoleVectorConstraint(){}

MObject PoleVectorConstraint::inRootWMtx;
MObject PoleVectorConstraint::inTargetWMtx;
MObject PoleVectorConstraint::inTargetWeight;
MObject PoleVectorConstraint::inConstParInvMtx;
MObject PoleVectorConstraint::inRestPosition;
MObject PoleVectorConstraint::inNormalizeOutput;
MObject PoleVectorConstraint::outConstraint;

void* PoleVectorConstraint::creator(){
    // Maya creator function.
    return new PoleVectorConstraint();
}

MStatus PoleVectorConstraint::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to BlendTransform class. Instances of BlendTransform will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnMatrixAttribute mAttr;
    MFnNumericAttribute nAttr;

    inRootWMtx = mAttr.create("rootWorldMatrix", "rootm", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inTargetWMtx = mAttr.create("targetWorldMatrix", "tgtm", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inTargetWeight = nAttr.create("targetWeight", "tw", MFnNumericData::kDouble, 1.0, &status);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    INPUT_ATTR(nAttr);

    inConstParInvMtx = mAttr.create("constraintParentInverseMatrix", "cpim", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inRestPosition = nAttr.createPoint("restPosition", "rest", &status);
    nAttr.setWritable(true);
    nAttr.setReadable(true);
    nAttr.setStorable(true);
    nAttr.setKeyable(false);

    inNormalizeOutput = nAttr.create("normalizeOutput", "normalize", MFnNumericData::kBoolean, false, &status);
    INPUT_ATTR(nAttr);

    outConstraint = nAttr.createPoint("constraint", "const", &status);
    OUTPUT_ATTR(nAttr);

    addAttribute(inRootWMtx);
    addAttribute(inTargetWMtx);
    addAttribute(inTargetWeight);
    addAttribute(inConstParInvMtx);
    addAttribute(inRestPosition);
    addAttribute(inNormalizeOutput);
    addAttribute(outConstraint);
    attributeAffects(inRootWMtx, outConstraint);
    attributeAffects(inTargetWMtx, outConstraint);
    attributeAffects(inTargetWeight, outConstraint);
    attributeAffects(inConstParInvMtx, outConstraint);
    attributeAffects(inRestPosition, outConstraint);
    attributeAffects(inNormalizeOutput, outConstraint);

    return status;
}

MStatus PoleVectorConstraint::connectionMade(const MPlug &plug, const MPlug &otherPlug,
                                             bool asSrc){
    /*
    This method gets called when connections are made to attributes of this node.
        * plug (MPlug) is the attribute on this node.
        * otherPlug (MPlug) is the attribute on the other node.
        * asSrc (bool) is this plug a source of the connection.
    */
   if (plug == inTargetWMtx){
       MObject thisMob = thisMObject();
       MPlug restPosPlug = MPlug(thisMob, inRestPosition);
       MObject targetMob = otherPlug.asMObject();
       MFnMatrixData mtxDataFn(targetMob);
       MMatrix mTarget = mtxDataFn.matrix();
       MVector vTarget(mTarget[3][0], mTarget[3][1], mTarget[3][2]);
       MFloatVector vTargetF(vTarget);
       MDataHandle restPosHandle = restPosPlug.asMDataHandle();
       restPosHandle.setMFloatVector(vTargetF);
       restPosPlug.setMDataHandle(restPosHandle);
   }
   return MPxNode::connectionMade(plug, otherPlug, asSrc);
}

MStatus PoleVectorConstraint::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outConstraint)
        return MStatus::kUnknownParameter;

    MMatrix mRoot = dataBlock.inputValue(inRootWMtx).asMatrix();
    MMatrix mTarget = dataBlock.inputValue(inTargetWMtx).asMatrix();
    MMatrix mConstParInv = dataBlock.inputValue(inConstParInvMtx).asMatrix();
    double targetWeight = dataBlock.inputValue(inTargetWeight).asDouble();
    MVector vRest(dataBlock.inputValue(inRestPosition).asFloat3());
    bool normalize = dataBlock.inputValue(inNormalizeOutput).asBool();

    MVector vRoot(mRoot[3][0], mRoot[3][1], mRoot[3][2]);
    MVector vTarget(mTarget[3][0], mTarget[3][1], mTarget[3][2]);

    MVector vPoleDirection = (vTarget - vRoot) * mConstParInv;
    MVector vRestDirection = (vRest - vRoot) * mConstParInv;
    MVector vPole = (1.0 - targetWeight) * vRestDirection + targetWeight * vPoleDirection;

    MFloatVector vResult(vPole);
    if (normalize)
        vResult.normalize();
    MDataHandle outConstHdle = dataBlock.outputValue(outConstraint);
    outConstHdle.setMFloatVector(vResult);
    outConstHdle.setClean();

    return MStatus::kSuccess;
}
