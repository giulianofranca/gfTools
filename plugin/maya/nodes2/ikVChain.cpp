#include "headers/ikVChain.hpp"

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
IKVChain::IKVChain(){}
IKVChain::~IKVChain(){}


// Members initialization
MObject IKVChain::inRoot;
MObject IKVChain::inHandle;
MObject IKVChain::inPole;
MObject IKVChain::inPrimAxis;
MObject IKVChain::inUpAxis;
MObject IKVChain::outTranslate;
MObject IKVChain::outRotate;
MObject IKVChain::outScale;
MObject IKVChain::outTransforms;




MPxNode::SchedulingType IKVChain::schedulingType() const{
    return MPxNode::SchedulingType::kParallel;
}

void* IKVChain::creator(){
    return new IKVChain();
}

MStatus IKVChain::initialize(){
    // Defines the set of attributes for this node. The attributes declared in this 
    // function are assigned as static members to IKVChain class. Instances of 
    // IKVChain will use these attributes to create plugs for use in the compute()
    // method.
    MStatus status;
    MFnMatrixAttribute mAttr;
    MFnEnumAttribute eAttr;
    MFnNumericAttribute nAttr;
    MFnUnitAttribute uAttr;
    MFnCompoundAttribute cAttr;

    inRoot = mAttr.create("root", "root", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inHandle = mAttr.create("handle", "handle", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inPole = mAttr.create("pole", "pole", MFnMatrixAttribute::kDouble, &status);
    INPUT_ATTR(mAttr);

    inPrimAxis = eAttr.create("primaryAxis", "paxis", Axis::xAxis, &status);
    eAttr.addField("X Axis", Axis::xAxis);
    eAttr.addField("Y Axis", Axis::yAxis);
    eAttr.addField("Z Axis", Axis::zAxis);
    INPUT_ATTR(eAttr);

    inUpAxis = eAttr.create("upAxis", "uaxis", Axis::yAxis, &status);
    eAttr.addField("X Axis", Axis::xAxis);
    eAttr.addField("Y Axis", Axis::yAxis);
    eAttr.addField("Z Axis", Axis::zAxis);
    INPUT_ATTR(eAttr);

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

    addAttribute(inRoot);
    addAttribute(inHandle);
    addAttribute(inPole);
    addAttribute(inPrimAxis);
    addAttribute(inUpAxis);
    addAttribute(outTransforms);
    attributeAffects(inRoot, outTranslate);
    attributeAffects(inHandle, outTranslate);
    attributeAffects(inPole, outTranslate);
    attributeAffects(inPrimAxis, outTranslate);
    attributeAffects(inUpAxis, outTranslate);

    return MStatus::kSuccess;
}

MStatus IKVChain::setDependentsDirty(const MPlug& plugBeingDirtied,
MPlugArray& affectedPlugs){
    MObject thisMob = thisMObject();
    if (plugBeingDirtied.isChild()){
        if (plugBeingDirtied.parent().partialName() == "outt"){
            affectedPlugs.append(MPlug(thisMob, outTranslate));
        }
        else if (plugBeingDirtied.parent().partialName() == "outr"){
            affectedPlugs.append(MPlug(thisMob, outRotate));
        }
        else if (plugBeingDirtied.parent().partialName() == "outs"){
            affectedPlugs.append(MPlug(thisMob, outScale));
        }
    }

    return MStatus::kSuccess;
}

MVector IKVChain::axisEnumToMVector(Axis axis){
    switch (axis){
    case Axis::xAxis:
        return MVector::xAxis;
    case Axis::yAxis:
        return MVector::yAxis;
    case Axis::zAxis:
        return MVector::zAxis;
    }
}

MStatus IKVChain::compute(const MPlug& plug, MDataBlock& dataBlock){
    // Node computation method:
    //     * plug is a connection point related to one of our node attributes.
    //     * dataBlock contains the data on which we will base our computations.
    MMatrix rootMtx = dataBlock.inputValue(inRoot).asMatrix();
    MMatrix handleMtx = dataBlock.inputValue(inHandle).asMatrix();
    MMatrix poleMtx = dataBlock.inputValue(inPole).asMatrix();
    Axis primIndex = static_cast<Axis>(dataBlock.inputValue(inPrimAxis).asShort());
    Axis upIndex = static_cast<Axis>(dataBlock.inputValue(inUpAxis).asShort());

    MVector rootV = MVector(rootMtx[3][0], rootMtx[3][1], rootMtx[3][2]);
    MVector handleV = MVector(handleMtx[3][0], handleMtx[3][1], handleMtx[3][2]);
    MVector poleV = MVector(poleMtx[3][0], poleMtx[3][1], poleMtx[3][2]);

    const MVector primAxis = axisEnumToMVector(primIndex);
    const MVector upAxis = axisEnumToMVector(upIndex);

    // Aim Vector
    MVector aimV = handleV - rootV;
    double solverLength = aimV.length();
    aimV.normalize();

    // Up Vector
    MVector upV = poleV - rootV;
    upV = upV - ((upV * aimV) * aimV);
    upV.normalize();

    // Basis Quaternion
    MQuaternion basisQ = MQuaternion(primAxis, aimV);

    return MStatus::kSuccess;
}