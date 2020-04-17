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

// Constructor.
SpaceConstraint::SpaceConstraint(){
    fLastSpace = 0;
    fOffsetMatch = MMatrix();
    fConstraintObject = MObject::kNullObj;
}

// Destructor.
SpaceConstraint::~SpaceConstraint(){}

MObject SpaceConstraint::inSpace;
MObject SpaceConstraint::inOffset;
MObject SpaceConstraint::inTarget;
MObject SpaceConstraint::inRestPose;
MObject SpaceConstraint::inAutoFillOff;
MObject SpaceConstraint::inSpaceMatch;
MObject SpaceConstraint::outConstTrans;
MObject SpaceConstraint::outConstRot;
MObject SpaceConstraint::outConstSca;


void* SpaceConstraint::creator(){
    // Maya creator function.
    return new SpaceConstraint();
}

MPxNode::SchedulingType SpaceConstraint::schedulingType() const{
    return MPxNode::SchedulingType::kParallel;
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

    inSpace = nAttr.create("space", "space", MFnNumericData::kShort, 0, &status);
    nAttr.setMin(0);
    INPUT_ATTR(nAttr);

    inOffset = mAttr.create("offset", "offset", MFnMatrixAttribute::kDouble, &status);
    mAttr.setArray(true);
    INPUT_ATTR(mAttr);

    inTarget = mAttr.create("target", "target", MFnMatrixAttribute::kDouble, &status);
    mAttr.setArray(true);
    INPUT_ATTR(mAttr);

    inRestPose = mAttr.create("restPose", "restPose", MFnMatrixAttribute::kDouble, &status);
    mAttr.setArray(true);
    INPUT_ATTR(mAttr);
    mAttr.setKeyable(false);

    inAutoFillOff = nAttr.create("autoFillOffsets", "afoff", MFnNumericData::kBoolean, true, &status);
    INPUT_ATTR(nAttr);

    inSpaceMatch = nAttr.create("spaceMatch", "spaceMatch", MFnNumericData::kBoolean, true, &status);
    INPUT_ATTR(nAttr);

    outConstTrans = nAttr.createPoint("constraintTranslate", "ctrans", &status);
    OUTPUT_ATTR(nAttr);

    MObject rotX = uAttr.create("constraintRotateX", "crotx", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject rotY = uAttr.create("constraintRotateY", "croty", MFnUnitAttribute::kAngle, 0.0, &status);
    MObject rotZ = uAttr.create("constraintRotateZ", "crotz", MFnUnitAttribute::kAngle, 0.0, &status);
    outConstRot = nAttr.create("constraintRotate", "crot", rotX, rotY, rotZ, &status);
    OUTPUT_ATTR(nAttr);

    outConstSca = nAttr.createPoint("constraintScale", "csca", &status);
    nAttr.setDefault(1.0, 1.0, 1.0);
    OUTPUT_ATTR(nAttr);

    addAttribute(inSpace);
    addAttribute(inAutoFillOff);
    addAttribute(inSpaceMatch);
    addAttribute(inOffset);
    addAttribute(inTarget);
    addAttribute(inRestPose);
    addAttribute(outConstTrans);
    addAttribute(outConstRot);
    addAttribute(outConstSca);
    attributeAffects(inSpace, outConstTrans);
    attributeAffects(inOffset, outConstTrans);
    attributeAffects(inTarget, outConstTrans);
    attributeAffects(inSpaceMatch, outConstTrans);
    attributeAffects(inSpace, outConstRot);
    attributeAffects(inOffset, outConstRot);
    attributeAffects(inTarget, outConstRot);
    attributeAffects(inSpaceMatch, outConstRot);
    attributeAffects(inSpace, rotX);
    attributeAffects(inOffset, rotX);
    attributeAffects(inTarget, rotX);
    attributeAffects(inSpaceMatch, rotX);
    attributeAffects(inSpace, rotY);
    attributeAffects(inOffset, rotY);
    attributeAffects(inTarget, rotY);
    attributeAffects(inSpaceMatch, rotY);
    attributeAffects(inSpace, rotZ);
    attributeAffects(inOffset, rotZ);
    attributeAffects(inTarget, rotZ);
    attributeAffects(inSpaceMatch, rotZ);
    attributeAffects(inSpace, outConstSca);
    attributeAffects(inOffset, outConstSca);
    attributeAffects(inTarget, outConstSca);
    attributeAffects(inSpaceMatch, outConstSca);

    return status;
}

MStatus SpaceConstraint::connectionMade(const MPlug &plug, const MPlug &otherPlug,
                                        bool asSrc){
    /*
    This method gets called when connections are made to attributes of this node.
        * plug (MPlug) is the attribute on this node.
        * otherPlug (MPlug) is the attribute on the other node.
        * asSrc (bool) is this plug a source of the connection.
    */
    MObject thisMob = thisMObject();
    bool autoFill = MPlug(thisMob, inAutoFillOff).asBool();
    checkOutputConnections();
    if (plug == inTarget){
        // Create empty slots in offset attribute if they don't exists.
        uint32_t targetIndex = plug.logicalIndex();
        MPlug offsetPlug = MPlug(thisMob, inOffset);
        MPlug curOffPlug = offsetPlug.elementByLogicalIndex(targetIndex);
        curOffPlug.asMDataHandle();
        // Create slots in restPose attribute with the current target value.
        MPlug restPlug = MPlug(thisMob, inRestPose);
        MPlug curRestPlug = restPlug.elementByLogicalIndex(targetIndex);
        MPlug targetPlug = MPlug(thisMob, inTarget);
        MPlug curTargetPlug = targetPlug.elementByLogicalIndex(targetIndex);
        MObject curTargetObj = curTargetPlug.asMObject();
        MFnMatrixData mtxDataFn(curTargetObj);
        MMatrix mTarget = mtxDataFn.matrix();
        MDataHandle curRestHdle = curRestPlug.asMDataHandle();
        curRestHdle.setMMatrix(mTarget);
        curRestPlug.setMDataHandle(curRestHdle);
        // Auto fill offset if it has a connected output.
        if (autoFill)
            autoFillOffset(targetIndex);
    }
    else if ((plug == outConstTrans) ||
             (plug == outConstRot) ||
             (plug == outConstSca)){
            // Check if it has a target input connection. If true, autoFill the offsets.
            MPlug targetPlug = MPlug(thisMob, inTarget);
            uint32_t numTarget = targetPlug.numElements();
            if (numTarget > 0 && autoFill){
                for (uint32_t targetIndex = 0; targetIndex < numTarget; targetIndex++){
                    autoFillOffset(targetIndex);
                }
            }
        }
    return MPxNode::connectionMade(plug, otherPlug, asSrc);
}

MStatus SpaceConstraint::connectionBroken(const MPlug &plug, const MPlug &otherPlug,
                                          bool asSrc){
    /*
    This method gets called when connections of this node are broken.
        * plug (MPlug) is the attribute on this node.
        * otherPlug (MPlug) is the attribute on the other node.
        * asSrc (bool) is this plug a source of the connection.
    */
    MObject thisMob = thisMObject();
    checkOutputConnections();
    if (plug == inTarget){
        // Create slots in restPose attribute with the current target value.
        uint32_t targetIndex = plug.logicalIndex();
        MPlug restPlug = MPlug(thisMob, inRestPose);
        MPlug curRestPlug = restPlug.elementByLogicalIndex(targetIndex);
        MDataHandle curRestHdle = curRestPlug.asMDataHandle();
        curRestHdle.setMMatrix(MMatrix());
        curRestPlug.setMDataHandle(curRestHdle);
    }
    return MPxNode::connectionBroken(plug, otherPlug, asSrc);
}


void SpaceConstraint::autoFillOffset(uint32_t &index){
    // Auto fill offsets attributes.
    MObject thisMob = thisMObject();
    bool allClear = checkOutputConnections();
    if (!allClear){
        if (fConstraintObject.hasFn(MFn::kDagNode)){
            MFnDagNode dagFn(fConstraintObject);
            MDagPath objPath;
            dagFn.getPath(objPath);
            MMatrix mOut = objPath.inclusiveMatrix();
            MPlug targetPlug = MPlug(thisMob, inTarget);
            MPlug curTargetPlug = targetPlug.elementByLogicalIndex(index);
            MObject curTargetObj = curTargetPlug.asMObject();
            MFnMatrixData mtxDataFn(curTargetObj);
            MMatrix mTarget = mtxDataFn.matrix();
            MMatrix mOffset = mOut * mTarget.inverse();
            MPlug offsetPlug = MPlug(thisMob, inOffset);
            MPlug curOffsetPlug = offsetPlug.elementByLogicalIndex(index);
            MDataHandle curOffsetHdle = curOffsetPlug.asMDataHandle();
            MMatrix mCurOffset = curOffsetHdle.asMatrix();
            if (mCurOffset == MMatrix()){
                curOffsetHdle.setMMatrix(mOffset);
                curOffsetPlug.setMDataHandle(curOffsetHdle);
            }
        }
    }
}

bool SpaceConstraint::checkOutputConnections(){
    /*
    Check if any output plug is connected.
    If it have connections, return False and the object connected.
    */
    MObject thisMob = thisMObject();
    MPlugArray outPlugArray = MPlugArray();
    outPlugArray.append(MPlug(thisMob, outConstTrans));
    outPlugArray.append(MPlug(thisMob, outConstRot));
    outPlugArray.append(MPlug(thisMob, outConstSca));
    bool allClear = true;
    MObject obj = MObject::kNullObj;
    for (uint32_t i = 0; i < outPlugArray.length(); i++){
        MPlug plug = outPlugArray[i];
        if (plug.isConnected()){
            allClear = false;
            MPlugArray objPlugs;
            MStatus status;
            plug.connectedTo(objPlugs, false, true, &status);
            obj = objPlugs[0].node();
            for (uint32_t j = 0; j < objPlugs.length(); j++){
                MPlug outPlug = objPlugs[j];
                MObject outNode = outPlug.node();
                if (!fConstraintObject.isNull()){
                    if (outNode == fConstraintObject){
                        obj = fConstraintObject;
                        break;
                    }
                }
            }
            break;
        }
    }
    fConstraintObject = (allClear) ? MObject::kNullObj : obj;
    return allClear;
}

MStatus SpaceConstraint::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    MArrayDataHandle offsetHdle = dataBlock.inputArrayValue(inOffset);
    MArrayDataHandle targetHdle = dataBlock.inputArrayValue(inTarget);
    MArrayDataHandle restHdle = dataBlock.inputArrayValue(inRestPose);

    std::vector<MMatrix> offsetList;
    std::vector<MMatrix> targetList;
    std::vector<MMatrix> restList;

    uint32_t offLen = offsetHdle.elementCount();
    for (uint32_t i = 0; i < offLen; i++){
        offsetHdle.jumpToArrayElement(i);
        MMatrix mOff = offsetHdle.inputValue().asMatrix();
        offsetList.push_back(mOff);
    }

    uint32_t tgtLen = targetHdle.elementCount();
    for (uint32_t i = 0; i < tgtLen; i++){
        targetHdle.jumpToArrayElement(i);
        MMatrix mTgt = targetHdle.inputValue().asMatrix();
        targetList.push_back(mTgt);
    }

    uint32_t restLen = restHdle.elementCount();
    for (uint32_t i = 0; i < restLen; i++){
        restHdle.jumpToArrayElement(i);
        MMatrix mRest = restHdle.inputValue().asMatrix();
        restList.push_back(mRest);
    }

    short curSpace = dataBlock.inputValue(inSpace).asShort();
    short lastSpace = fLastSpace;
    short maxSpace = std::min(offLen, tgtLen) - 1;
    if (curSpace > maxSpace)
        curSpace = maxSpace;
    if (curSpace != lastSpace){
        // 1- Check if automatic space matching is enable.
        bool match = dataBlock.inputValue(inSpaceMatch).asBool();
        if (match){
            // 2- Check if any output is been used and get the output object.
            MObject thisMob = thisMObject();
            bool allClear = checkOutputConnections();
            // 3- If the node have necessary connections...
            if (!allClear && (maxSpace + 1) > 0){
                if (fConstraintObject.hasFn(MFn::kDagNode)){
                    // 4- Get the last world matrix of the target.
                    MMatrix mOffset = offsetList[lastSpace];
                    MMatrix mTarget = targetList[lastSpace];
                    MMatrix mLastOutputW = fOffsetMatch * mOffset * mTarget;
                    // 5- Get the current world matrix of the target.
                    mOffset = offsetList[curSpace];
                    mTarget = targetList[curSpace];
                    MMatrix mCurOutputW = mOffset * mTarget;
                    // 6- Get the result of the match and set it into the variable.
                    if ((targetList[curSpace] == restList[curSpace]) &&
                        (targetList[lastSpace] == restList[lastSpace])){
                            // Reset the match matrix if both targets is on rest pose.
                            fOffsetMatch = MMatrix();
                    }
                    else{
                        MMatrix mMatchResult = mLastOutputW * mCurOutputW.inverse();
                        fOffsetMatch = mMatchResult;
                    }
                }
            }
        }
        else
            fOffsetMatch = MMatrix();
        // 7- Store the current space value in class to be accessed later on.
        fLastSpace = curSpace;
    }

    MMatrix mResult;
    if (offLen == 0 || tgtLen == 0)
        mResult = MMatrix();
    else{
        mResult = fOffsetMatch * offsetList[curSpace] * targetList[curSpace];
    }

    MTransformationMatrix mtxFn(mResult);

    if (plug == outConstTrans){
        MVector vTransD(mResult[3][0], mResult[3][1], mResult[3][2]);
        MFloatVector vTrans = MFloatVector(vTransD);
        MDataHandle outTransHdle = dataBlock.outputValue(outConstTrans);
        outTransHdle.setMFloatVector(vTrans);
        outTransHdle.setClean();
    }

    else if (plug == outConstRot){
        MEulerRotation eRot = mtxFn.eulerRotation();
        MDataHandle outRotHdle = dataBlock.outputValue(outConstRot);
        outRotHdle.setMVector(eRot.asVector());
        outRotHdle.setClean();
    }

    else if (plug == outConstSca){
        double scale[3];
        mtxFn.getScale(scale, MSpace::kWorld);
        MFloatVector vScale = MFloatVector(scale);
        MDataHandle outScaHdle = dataBlock.outputValue(outConstSca);
        outScaHdle.setMFloatVector(vScale);
        outScaHdle.setClean();
    }

    return MStatus::kSuccess;
}
