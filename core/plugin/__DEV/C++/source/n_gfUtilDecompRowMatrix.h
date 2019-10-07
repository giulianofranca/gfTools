#pragma once

#include <maya/MPxNode.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFloatMatrix.h>
#include <maya/MFloatVector.h>

class DecomposeRowMatrix : MPxNode{
public:
    DecomposeRowMatrix();
    virtual ~DecomposeRowMatrix();

    virtual MPxNode::SchedulingType schedulingType(){
        return MPxNode::SchedulingType::kParallel;
    }

    virtual MStatus                     compute(const MPlug& plug, MDataBlock& dataBlock);
    static MStatus                      initialize();
    static void*                        creator();

public:
    const static MString                kNodeName;
    const static MString                kNodeClassify;
    const static MTypeId                kNodeID;

    static MObject                      inMatrix;
    static MObject                      inNormalizeOutput;
    static MObject                      outRow1;
    static MObject                      outRow2;
    static MObject                      outRow3;
    static MObject                      outRow4;
};