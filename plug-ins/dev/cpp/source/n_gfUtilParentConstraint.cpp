#include "headers/n_gfUtilParentConstraint.h"

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
ParentConstraint::ParentConstraint() {}

// Destructor.
ParentConstraint::~ParentConstraint() {}

MObject ParentConstraint::inTarget;
MObject ParentConstraint::inOffset;
MObject ParentConstraint::inWeight;
MObject ParentConstraint::outConstraint;

void* ParentConstraint::creator(){
    // Maya creator function.
    return new ParentConstraint();
}

MStatus ParentConstraint::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to ParentConstraint class. Instances of ParentConstraint will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnMatrixAttribute mAttr;
    MFnNumericAttribute nAttr;

    inTarget = mAttr.create("target", "target", MFnMatrixAttribute::kDouble, &status);
    mAttr.setArray(true);
    INPUT_ATTR(mAttr);

    inOffset = mAttr.create("offset", "offset", MFnMatrixAttribute::kDouble, &status);
    mAttr.setArray(true);
    INPUT_ATTR(mAttr);

    inWeight = nAttr.create("weight", "weight", MFnNumericData::kFloat, 1.0f, &status);
    nAttr.setArray(true);
    nAttr.setMin(0.0f);
    nAttr.setMax(1.0f);
    INPUT_ATTR(nAttr);

    outConstraint = mAttr.create("constraint", "constraint", MFnMatrixAttribute::kDouble, &status);
    OUTPUT_ATTR(mAttr);

    addAttribute(inTarget);
    addAttribute(inOffset);
    addAttribute(inWeight);
    addAttribute(outConstraint);
    attributeAffects(inTarget, outConstraint);
    attributeAffects(inOffset, outConstraint);
    attributeAffects(inWeight, outConstraint);

    return status;
}

MStatus ParentConstraint::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outConstraint)
        return MStatus::kUnknownParameter;

    MArrayDataHandle targetHandle = dataBlock.inputArrayValue(inTarget);
    MArrayDataHandle offsetHandle = dataBlock.inputArrayValue(inOffset);
    MArrayDataHandle weightHandle = dataBlock.inputArrayValue(inWeight);

    vector<MMatrix> targetList;
    uint32_t minList[] = {
        targetHandle.elementCount(),
        offsetHandle.elementCount(),
        weightHandle.elementCount()
    };
    uint32_t index = *min_element(begin(minList), end(minList));
    for (uint32_t i = 0; i < index; i++){
        targetHandle.jumpToArrayElement(i);
        offsetHandle.jumpToArrayElement(i);
        weightHandle.jumpToArrayElement(i);
        MMatrix mTarget = targetHandle.inputValue().asMatrix();
        MMatrix mOffset = offsetHandle.inputValue().asMatrix();
        float weight = weightHandle.inputValue().asFloat();
        targetList.push_back((mOffset * mTarget) * weight);
    }

    MMatrix mAdd = MMatrix();
    for(int i = 0; i < targetList.size(); i++){
        mAdd += targetList[i];
    }

    MMatrix mConstraint = mAdd * MMatrix(); // Parent Inverse Matrix
    MDataHandle outConstraintHandle = dataBlock.outputValue(outConstraint);
    outConstraintHandle.setMMatrix(mConstraint);
    outConstraintHandle.setClean();

    return MStatus::kSuccess;
}