/*
Copyright (c) 2019 Giuliano França

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

====================================================================================================

How to use:
    * Copy the parent folder to the MAYA_SCRIPT_PATH.
    * To find MAYA_SCRIPT_PATH paste this command in a Python tab:
        import os; os.environ["MAYA_SCRIPT_PATH"].split(";")
    * In Maya, go to Windows > Settings/Preferences > Plug-in Manager.
    * Browse for "gfTools > plug-ins > release".
    * Find gfTools plugin (Windows: gfTools.mll, OSX: gfTools.bundle, Linux: gfTools.so) and import it.

    * Copy and paste this file in the MAYA_PLUG_IN_PATH.
    * To find MAYA_PLUG_IN_PATH paste this command in a Python tab on script editor:
        import os; os.environ["MAYA_PLUG_IN_PATH"].split(";")
    * In Maya, go to Windows > Settings/Preferences > Plug-in Manager.
    * Find this file and import it.

Requirements:
    * Maya 2017 or above.

Todo:
    * NDA

Sources:
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