#include "headers/n_gfUtilFindParamFromCurveLength.h"

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
FindParamFromLength::FindParamFromLength() {}

// Destructor.
FindParamFromLength::~FindParamFromLength() {}

MObject FindParamFromLength::inCurve;
MObject FindParamFromLength::inArcLength;
MObject FindParamFromLength::outParam;

void* FindParamFromLength::creator(){
    // Maya creator function.
    return new FindParamFromLength();
}

MStatus FindParamFromLength::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to FindParamFromLength class. Instances of FindParamFromLength will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnUnitAttribute uAttr;

    inCurve = tAttr.create("inputCurve", "icrv", MFnData::kNurbsCurve, MObject::kNullObj, &status);
    INPUT_ATTR(tAttr);

    inArcLength = uAttr.create("arcLength", "length", MFnUnitAttribute::kDistance, 0.0, &status);
    INPUT_ATTR(uAttr);

    outParam = nAttr.create("outParam", "param", MFnNumericData::kDouble, 0.0, &status);
    OUTPUT_ATTR(nAttr);

    addAttribute(inCurve);
    addAttribute(inArcLength);
    addAttribute(outParam);
    attributeAffects(inCurve, outParam);
    attributeAffects(inArcLength, outParam);

    return status;
}

MStatus FindParamFromLength::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outParam)
        return MStatus::kUnknownParameter;

    MDataHandle curveHdle = dataBlock.inputValue(inCurve);
    MObject curveMob = curveHdle.asNurbsCurve();
    double arcLen = dataBlock.inputValue(inArcLength).asDouble();

    MFnNurbsCurve curveFn(curveMob);
    double param = curveFn.findParamFromLength(arcLen);

    MDataHandle outParamHdle = dataBlock.outputValue(outParam);
    outParamHdle.setDouble(param);
    outParamHdle.setClean();

    return MStatus::kSuccess;
}