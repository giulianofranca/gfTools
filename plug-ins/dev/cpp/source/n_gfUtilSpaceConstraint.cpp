#include "headers/n_gfUtilSpaceConstraint.h"

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

MObject SpaceConstraint::inSpace;
MObject SpaceConstraint::inSpaceMatch;
MObject SpaceConstraint::inTarget;
MObject SpaceConstraint::inOffset;
MObject SpaceConstraint::inRestPose;
MObject SpaceConstraint::inTargetList;
MObject SpaceConstraint::inMatchMatrix;
MObject SpaceConstraint::outConstTrans;
MObject SpaceConstraint::outConstRot;
MObject SpaceConstraint::outConstRotX;
MObject SpaceConstraint::outConstRotY;
MObject SpaceConstraint::outConstRotZ;
MObject SpaceConstraint::outConstSca;

// Constructor.
SpaceConstraint::SpaceConstraint(){}

// Destructor.
SpaceConstraint::~SpaceConstraint(){}

void* SpaceConstraint::creator(){
    // Maya creator function.
    return new SpaceConstraint();
}

MPxNode::SchedulingType SpaceConstraint::schedulingType() const{
    return MPxNode::SchedulingType::kParallel;
}

void SpaceConstraint::postConstructor(){
    // Post constructor.
    MObject thisMob = thisMObject();
    short curSpace = MPlug(thisMob, inSpace).asShort();
    fLastSpace = curSpace;
}

MStatus SpaceConstraint::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to BlendTransform class. Instances of BlendTransform will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnMatrixAttribute mAttr;
    MFnNumericAttribute nAttr;
    MFnUnitAttribute uAttr;
    MFnCompoundAttribute cAttr;

    inSpace = nAttr.create("space", "space", MFnNumericData::kShort, 0, &status);
    nAttr.setMin(0);
    INPUT_ATTR(nAttr);

    inSpaceMatch = nAttr.create("spaceMatch", "spaceMatch", MFnNumericData::kBoolean, true, &status);
    INPUT_ATTR(nAttr);

    inTarget = mAttr.create("target", "target", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inOffset = mAttr.create("offset", "offset", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inRestPose = mAttr.create("restPose", "restPose", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inTargetList = cAttr.create("targetList", "tlist", &status);
    cAttr.addChild(inTarget);
    cAttr.addChild(inOffset);
    cAttr.addChild(inRestPose);
    cAttr.setArray(true);

    inMatchMatrix = mAttr.create("matchMatrix", "mmtx", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);
    mAttr.setHidden(true);

    outConstTrans = nAttr.createPoint("constraintTranslate", "ctrans", &status);
    OUTPUT_ATTR(nAttr);

    outConstRotX = uAttr.create("constraintRotateX", "crotx", MFnUnitAttribute::kAngle, 0.0, &status);
    outConstRotY = uAttr.create("constraintRotateY", "croty", MFnUnitAttribute::kAngle, 0.0, &status);
    outConstRotZ = uAttr.create("constraintRotateZ", "crotz", MFnUnitAttribute::kAngle, 0.0, &status);
    outConstRot = nAttr.create("constraintRotate", "crot", outConstRotX, outConstRotY, outConstRotZ, &status);
    OUTPUT_ATTR(nAttr);

    outConstSca = nAttr.createPoint("constraintScale", "csca", &status);
    nAttr.setDefault(1.0, 1.0, 1.0);
    OUTPUT_ATTR(nAttr);

    addAttribute(inSpace);
    addAttribute(inSpaceMatch);
    addAttribute(inTargetList);
    addAttribute(inMatchMatrix);
    addAttribute(outConstTrans);
    addAttribute(outConstRot);
    addAttribute(outConstSca);
    attributeAffects(inSpace, outConstTrans);
    attributeAffects(inSpaceMatch, outConstTrans);
    attributeAffects(inTarget, outConstTrans);
    attributeAffects(inOffset, outConstTrans);
    attributeAffects(inRestPose, outConstTrans);
    attributeAffects(inMatchMatrix, outConstTrans);
    attributeAffects(inSpace, outConstRot);
    attributeAffects(inSpaceMatch, outConstRot);
    attributeAffects(inTarget, outConstRot);
    attributeAffects(inOffset, outConstRot);
    attributeAffects(inRestPose, outConstRot);
    attributeAffects(inMatchMatrix, outConstRot);
    attributeAffects(inSpace, outConstSca);
    attributeAffects(inSpaceMatch, outConstSca);
    attributeAffects(inTarget, outConstSca);
    attributeAffects(inOffset, outConstSca);
    attributeAffects(inRestPose, outConstSca);
    attributeAffects(inMatchMatrix, outConstSca);

    return status;
}

MStatus SpaceConstraint::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    MArrayDataHandle targetListHdle = dataBlock.inputArrayValue(inTargetList);

    MMatrixArray offsetList, targetList, restList;

    uint32_t targetLen = targetListHdle.elementCount();
    for (uint32_t i = 0; i < targetLen; i++){
        targetListHdle.jumpToArrayElement(i);
        MDataHandle curTargetHdle = targetListHdle.inputValue();
        MMatrix mTarget = curTargetHdle.child(inTarget).asMatrix();
        MMatrix mOffset = curTargetHdle.child(inOffset).asMatrix();
        MMatrix mRest = curTargetHdle.child(inRestPose).asMatrix();
        targetList.append(mTarget);
        offsetList.append(mOffset);
        restList.append(mRest);
    }

    short curSpace = dataBlock.inputValue(inSpace).asShort();
    short lastSpace = fLastSpace;
    MObject thisMob = thisMObject();
    MPlug matchMtxPlug = MPlug(thisMob, inMatchMatrix);
    MDataHandle matchMtxHdle = matchMtxPlug.asMDataHandle();
    // 1- Check if curSpace is in range of valid inputs.
    short validSpaces = targetLen - 1;
    if (curSpace > validSpaces)
        curSpace = validSpaces;
    // 2- Check if space match is enable.
    bool match = dataBlock.inputValue(inSpaceMatch).asBool();
    // 3- Get the match matrix.
    MMatrix mMatchResult = dataBlock.inputValue(inMatchMatrix).asMatrix();
    if (match){
        // 4- Get the current target.
        MMatrix mCurTarget = targetList[curSpace];
        // 5- Check if the space changed.
        if (curSpace != lastSpace){
            // 6A - Get the current world matrix of the target.
            MMatrix mCurOffset = offsetList[curSpace];
            MMatrix mCurOutputW = mCurOffset * mCurTarget;
            // 7A - Get the last world matrix of the target.
            MMatrix mLastTarget = targetList[lastSpace];
            MMatrix mLastOffset = offsetList[lastSpace];
            MMatrix mLastOutputW = mMatchResult * mLastOffset * mLastTarget;
            // 8A - Get the result of the match and set it into the plug.
            if ((mCurTarget == restList[curSpace]) &&
                (mLastTarget == restList[lastSpace])){
                // Reset the match matrix if both target is on rest pose.
                mMatchResult = MMatrix();
                matchMtxHdle.setMMatrix(mMatchResult);
                matchMtxPlug.setMDataHandle(matchMtxHdle);
            }
            else{
                mMatchResult = mLastOutputW * mCurOutputW.inverse();
                matchMtxHdle.setMMatrix(mMatchResult);
                matchMtxPlug.setMDataHandle(matchMtxHdle);
            }
            // 9A - Store the current space value in class to be accessed later on.
            fLastSpace = curSpace;
        }
        // else{
        //     // If the space doesn't change, reset the match matrix if both poses is on rest pose.
        //     // 6B - Get the last used target.
        //     MMatrix mLastTarget = targetList[fLastUsedSpace];
        //     // 7B- Check if the last and current target is on rest pose.
        //     if ((mCurTarget == restList[curSpace]) &&
        //         (mLastTarget == restList[fLastUsedSpace])){
        //         // Reset the match matrix if both target is on rest pose.
        //         fOffsetMatch = MMatrix();
        //     }
        // }
    }
    else{
        mMatchResult = MMatrix();
        matchMtxHdle.setMMatrix(mMatchResult);
        matchMtxPlug.setMDataHandle(matchMtxHdle);
    }

    MMatrix mResult = MMatrix();
    MTransformationMatrix mtxFn = MTransformationMatrix();
    if (targetLen != 0){
        mResult = mMatchResult * offsetList[curSpace] * targetList[curSpace];
    }

    if (plug == outConstTrans){
        MDataHandle outTransHdle = dataBlock.outputValue(outConstTrans);
        MVector vTrans = MVector(mResult[3][0], mResult[3][1], mResult[3][2]);
        outTransHdle.setMFloatVector(vTrans);
        outTransHdle.setClean();
    }

    if ((plug == outConstRot) ||
        (plug == outConstRotX) ||
        (plug == outConstRotY) ||
        (plug == outConstRotZ)){
        MDataHandle outRotHdle = dataBlock.outputValue(outConstRot);
        mtxFn = MTransformationMatrix(mResult);
        MEulerRotation eRot = mtxFn.eulerRotation();
        outRotHdle.set3Double(eRot.x, eRot.y, eRot.z);
        outRotHdle.setClean();
    }

    if (plug == outConstSca){
        MDataHandle outScaHdle = dataBlock.outputValue(outConstSca);
        mtxFn = MTransformationMatrix(mResult);
        double scale[3];
        mtxFn.getScale(scale, MSpace::kWorld);
        MVector outSca = MVector(scale[0], scale[1], scale[2]);
        outScaHdle.setMFloatVector(outSca);
        outScaHdle.setClean();
    }

    return MStatus::kSuccess;
}
