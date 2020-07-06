#include "headers/n_gfRigDistributeAlongSurface.h"

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
DistributeAlongSurface::DistributeAlongSurface() {}

// Destructor.
DistributeAlongSurface::~DistributeAlongSurface() {}

MObject DistributeAlongSurface::inSurface;
MObject DistributeAlongSurface::inDistributeAlong;
MObject DistributeAlongSurface::inDisplace;
MObject DistributeAlongSurface::inAlwaysUniform;
MObject DistributeAlongSurface::outTransform;

void* DistributeAlongSurface::creator(){
    // Maya creator function.
    return new DistributeAlongSurface();
}

MStatus DistributeAlongSurface::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to DistributeAlongSurface class. Instances of DistributeAlongSurface will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnTypedAttribute tAttr;
    MFnEnumAttribute eAttr;
    MFnNumericAttribute nAttr;
    MFnMatrixAttribute mAttr;

    inSurface = tAttr.create("inputSurface", "isurf", MFnData::kNurbsSurface, &status);
    INPUT_ATTR(tAttr);

    inDistributeAlong = eAttr.create("distributeAlong", "da", 0, &status);
    eAttr.addField("U", 0);
    eAttr.addField("V", 1);
    INPUT_ATTR(eAttr);

    inDisplace = nAttr.create("displaceTangent", "dtan", MFnNumericData::kFloat, 0.0f, &status);
    nAttr.setMin(0.0f);
    nAttr.setMax(1.0f);
    INPUT_ATTR(nAttr);

    inAlwaysUniform = nAttr.create("alwaysUniform", "auni", MFnNumericData::kBoolean, false, &status);
    INPUT_ATTR(nAttr);

    outTransform = mAttr.create("outputTransform", "ot", MFnMatrixAttribute::kDouble, &status);
    mAttr.setArray(true);
    OUTPUT_ATTR(mAttr);

    addAttribute(inSurface);
    addAttribute(inDistributeAlong);
    addAttribute(inDisplace);
    addAttribute(inAlwaysUniform);
    addAttribute(outTransform);
    attributeAffects(inSurface, outTransform);
    attributeAffects(inDistributeAlong, outTransform);
    attributeAffects(inDisplace, outTransform);
    attributeAffects(inAlwaysUniform, outTransform);

    return status;
}

MStatus DistributeAlongSurface::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outTransform)
        return MStatus::kUnknownParameter;

    MDataHandle surfaceHandle = dataBlock.inputValue(inSurface);
    MObject surface = surfaceHandle.asNurbsSurface();
    short distAlong = dataBlock.inputValue(inDistributeAlong).asShort();
    float displace = dataBlock.inputValue(inDisplace).asFloat();
    bool alwaysUniform = dataBlock.inputValue(inAlwaysUniform).asBool();
    MArrayDataHandle outTransHandle = dataBlock.outputArrayValue(outTransform);

    uint32_t numOutputs = outTransHandle.elementCount();
    MFnNurbsSurface surfaceFn(surface);
    float step = numOutputs > 1 ? 1.0f / (numOutputs - 1) : 0.0f;
    MObject curveData = MFnNurbsCurveData().create();
    MFnNurbsCurve curveFn(curveData);
    double curveLength;

    if (alwaysUniform){
        int numCVs = distAlong == 0 ? surfaceFn.numCVsInU() : surfaceFn.numCVsInV();
        MPointArray curvePnts = MPointArray();
        MDoubleArray curveKnots;
        distAlong == 0 ? surfaceFn.getKnotsInU(curveKnots) : surfaceFn.getKnotsInV(curveKnots);
        int curveDegree = distAlong == 0 ? surfaceFn.degreeU() : surfaceFn.degreeV();
        MFnNurbsSurface::Form curveForm = distAlong == 0 ? surfaceFn.formInU() : 
            surfaceFn.formInV();
        bool curveIs2d = false;
        bool curveRational = false;
        for (uint32_t i = 0; i < (uint32_t)numCVs; i++){
            MPoint cvPos;
            if (distAlong == 0)
                surfaceFn.getCV(i, static_cast<uint32_t>(displace), cvPos);
            else
                surfaceFn.getCV(static_cast<uint32_t>(displace), i, cvPos);
            curvePnts.append(cvPos);
        }
        curveFn.create(curvePnts, curveKnots, curveDegree, (MFnNurbsCurve::Form)curveForm,
                       curveIs2d, curveRational, curveData);
        curveLength = curveFn.length();
    }

    double parU, parV;
    for (uint32_t i = 0; i < numOutputs; i++){
        if (alwaysUniform){
            parU = distAlong == 0 ? curveFn.findParamFromLength(curveLength * step * i) : displace;
            parV = distAlong == 0 ? displace : curveFn.findParamFromLength(curveLength * step * i);
        }
        else{
            parU = distAlong == 0 ? step * i : displace;
            parV = distAlong == 0 ? displace : step * i;
        }
        MPoint pos;
        MVector tangentU, tangentV;
        MVector normal = surfaceFn.normal(parU, parV, MSpace::kWorld).normal();
        surfaceFn.getPointAtParam(parU, parV, pos, MSpace::kWorld);
        surfaceFn.getTangents(parU, parV, tangentU, tangentV, MSpace::kWorld);
        MVector aim = distAlong == 0 ? tangentU.normal() : tangentV.normal();
        MVector binormal = distAlong == 0 ? tangentV.normal() : tangentU.normal();
        double mtx[4][4] = {
            {aim.x, aim.y, aim.z, 0.0},
            {normal.x, normal.y, normal.z, 0.0},
            {binormal.x, binormal.y, binormal.z, 0.0},
            {pos.x, pos.y, pos.z, 1.0}
        };
        MMatrix mOut(mtx);
        outTransHandle.jumpToArrayElement(i);
        MDataHandle resultHandle = outTransHandle.outputValue();
        resultHandle.setMMatrix(mOut);
    }

    surfaceHandle.setClean();
    outTransHandle.setAllClean();

    return MStatus::kSuccess;
}