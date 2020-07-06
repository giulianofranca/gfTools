#include "headers/n_gfUtilDecompRowMatrix.h"

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
DecomposeRowMatrix::DecomposeRowMatrix(){}

// Destructor.
DecomposeRowMatrix::~DecomposeRowMatrix(){}

MObject DecomposeRowMatrix::inMatrix;
MObject DecomposeRowMatrix::inNormalizeOutput;
MObject DecomposeRowMatrix::outRow1;
MObject DecomposeRowMatrix::outRow2;
MObject DecomposeRowMatrix::outRow3;
MObject DecomposeRowMatrix::outRow4;


void* DecomposeRowMatrix::creator(){
    // Maya creator function.
    return new DecomposeRowMatrix();
}

MStatus DecomposeRowMatrix::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to DecomposeRowMatrix class. Instances of DecomposeRowMatrix will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnNumericAttribute nAttr;
    MFnMatrixAttribute mAttr;

    inMatrix = mAttr.create("inputMatrix", "im", MFnMatrixAttribute::kFloat, &status);
    INPUT_ATTR(mAttr);

    inNormalizeOutput = nAttr.create("normalizeOutput", "no", MFnNumericData::kBoolean, false, &status);
    INPUT_ATTR(nAttr);

    outRow1 = nAttr.createPoint("row1", "r1", &status);
    OUTPUT_ATTR(nAttr);

    outRow2 = nAttr.createPoint("row2", "r2", &status);
    OUTPUT_ATTR(nAttr);

    outRow3 = nAttr.createPoint("row3", "r3", &status);
    OUTPUT_ATTR(nAttr);

    outRow4 = nAttr.createPoint("row4", "r4", &status);
    OUTPUT_ATTR(nAttr);

    addAttribute(inMatrix);
    addAttribute(inNormalizeOutput);
    addAttribute(outRow1);
    addAttribute(outRow2);
    addAttribute(outRow3);
    addAttribute(outRow4);
    attributeAffects(inMatrix, outRow1);
    attributeAffects(inNormalizeOutput, outRow1);
    attributeAffects(inMatrix, outRow2);
    attributeAffects(inNormalizeOutput, outRow2);
    attributeAffects(inMatrix, outRow3);
    attributeAffects(inNormalizeOutput, outRow3);
    attributeAffects(inMatrix, outRow4);
    attributeAffects(inNormalizeOutput, outRow4);

    return status;
}

MStatus DecomposeRowMatrix::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    MFloatMatrix mInput = dataBlock.inputValue(inMatrix).asFloatMatrix();
    bool normalize = dataBlock.inputValue(inNormalizeOutput).asBool();

    if (plug == outRow1){
        MFloatVector vRow1 = MFloatVector(mInput[0][0], mInput[0][1], mInput[0][2]);
        if (normalize)
            vRow1.normalize();
        MDataHandle outRow1Handle = dataBlock.outputValue(outRow1);
        outRow1Handle.setMFloatVector(vRow1);
        outRow1Handle.setClean();
    }
    else if (plug == outRow2){
        MFloatVector vRow2 = MFloatVector(mInput[1][0], mInput[1][1], mInput[1][2]);
        if (normalize)
            vRow2.normalize();
        MDataHandle outRow2Handle = dataBlock.outputValue(outRow2);
        outRow2Handle.setMFloatVector(vRow2);
        outRow2Handle.setClean();
    }
    else if (plug == outRow3){
        MFloatVector vRow3 = MFloatVector(mInput[2][0], mInput[2][1], mInput[2][2]);
        if (normalize)
            vRow3.normalize();
        MDataHandle outRow3Handle = dataBlock.outputValue(outRow3);
        outRow3Handle.setMFloatVector(vRow3);
        outRow3Handle.setClean();
    }
    else if (plug == outRow4){
        MFloatVector vRow4 = MFloatVector(mInput[3][0], mInput[3][1], mInput[3][2]);
        if (normalize)
            vRow4.normalize();
        MDataHandle outRow4Handle = dataBlock.outputValue(outRow4);
        outRow4Handle.setMFloatVector(vRow4);
        outRow4Handle.setClean();
    }
    else
        return MStatus::kUnknownParameter;

    return MStatus::kSuccess;
}