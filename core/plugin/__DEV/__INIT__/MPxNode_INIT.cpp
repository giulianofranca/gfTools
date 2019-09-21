/*
Copyright (c) 2019 Giuliano França

Maya IDs:
    Prototypes: 0x0012f7c0 - 0x0012f7ff
    Releases: 0x00130d80 - 0x00130e7f

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfTestNode node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.

How to use:
    * Copy and paste this file to a Maya plugins path, default: "C:/Users/<user>/Documents/maya/<version>/plug-ins".
        You can create a "plug-ins" folder if not exists.
    * Open your Maya (same version).
    * Go to Windows > Settings/Preferences > Plug-in Manager.
    * Mark this file as loaded.

Requirements:
    Maya 2017 or above.

Todo:
    * NDA
*/
#pragma once

#include <maya\MPxNode.h>

#include <maya\MFnPlugin.h>
#include <maya\MString.h>
#include <maya\MTypeId.h>

#include <maya\MFnNumericAttribute.h>
#include <maya\MVector.h>


class TestNode : MPxNode{
public:
    TestNode();
    virtual ~TestNode();

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

    static MObject                      inAttr;
    static MObject                      outAttr;
};


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
TestNode::TestNode() {}

// Destructor.
TestNode::~TestNode() {}

MObject TestNode::inAttr;
MObject TestNode::outAttr;


void* TestNode::creator(){
    // Maya creator function.
    return new TestNode();
}

MStatus TestNode::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to TestNode class. Instances of TestNode will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnNumericAttribute nAttr;

    inAttr = nAttr.createPoint("inAttr", "ina", &status);
    INPUT_ATTR(nAttr);

    outAttr = nAttr.createPoint("outAttr", "outa", &status);
    OUTPUT_ATTR(nAttr);

    addAttribute(inAttr);
    addAttribute(outAttr);
    attributeAffects(inAttr, outAttr);

    return status;
}

MStatus TestNode::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outAttr)
        return MStatus::kUnknownParameter;

    MVector inAttrValue = dataBlock.inputValue(inAttr).asVector();

    MDataHandle outAttrHandle = dataBlock.outputValue(outAttr);
    outAttrHandle.setMVector(inAttrValue);
    outAttrHandle.setClean();

    return MStatus::kSuccess;
}


#define REGISTER_NODE(NODE, PLUGIN)         \
    status = PLUGIN.registerNode(           \
        NODE::kNodeName,                    \
        NODE::kNodeID,                      \
        NODE::creator,                      \
        NODE::initialize,                   \
        MPxNode::kDependNode,               \
        &NODE::kNodeClassify                \
    );                                      \
    CHECK_MSTATUS(status);                  \

#define DEREGISTER_NODE(NODE, PLUGIN)       \
    status = PLUGIN.deregisterNode(         \
        NODE::kNodeID                       \
    );                                      \
    CHECK_MSTATUS(status);                  \


const char* kAuthor = "Giuliano Franca";
const char* kVersion = "Test";
const char* kRequiredAPIVersion = "Any";

const MString TestNode::kNodeName = "gfTestNode";
const MString TestNode::kNodeClassify = "utility/general";
const MTypeId TestNode::kNodeID = 0x000fff;


MStatus initializePlugin(MObject mobject){
    MStatus status;
    MFnPlugin mPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion, &status);
    status = mPlugin.setName("Test");

    REGISTER_NODE(TestNode, mPlugin);

    return status;
}

MStatus uninitializePlugin(MObject mobject){
    MStatus status;
    MFnPlugin mPlugin(mobject, kAuthor, kVersion, kRequiredAPIVersion, &status);

    DEREGISTER_NODE(TestNode, mPlugin);

    return status;
}