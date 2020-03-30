#include "headers/n_gfRigMeshController2.h"

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


static float sCurve[][3] = {
    {0.0f, 0.0f, 0.0f},
    {1.0f, 1.0f, 0.0f},
    {2.0f, 1.0f, 0.0f},
    {3.0f, 0.0f, 0.0f}
};

static unsigned sCurvePointCount = 4;


MeshController::MeshController() {
    // Constructor.
    basicCurvePoints.setLength(sCurvePointCount);
    for (unsigned i = 0; i < sCurvePointCount; i++){
        basicCurvePoints[i].x = sCurve[i][0];
        basicCurvePoints[i].y = sCurve[i][1];
        basicCurvePoints[i].z = sCurve[i][2];
        basicCurvePoints[i].w = 1.0;
    }
}

// Destructor.
MeshController::~MeshController() {}

MObject MeshController::inColor;
MPointArray MeshController::basicCurvePoints;


void *MeshController::creator(){
	// Maya creator function.
	return new MeshController();
}

MStatus MeshController::initialize(){
	/*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to MeshController class. Instances of MeshController will use these attributes to create plugs
    for use in the compute() method.
    */
   	MStatus status;
    MFnNumericAttribute nAttr;

    inColor = nAttr.createColor("color", "color", &status);
    nAttr.setDefault(1.0, 0.455, 0.086);
    INPUT_ATTR(nAttr);

    addAttribute(inColor);

	return status;
}

bool MeshController::isBounded() const{
    /* isBounded? */
    return true;
}

MBoundingBox MeshController::boundingBox() const{
    /* Return the BoundingBox */
    MPoint corner1(0.0, 0.0, 0.0);
    MPoint corner2(3.0, 1.0, 0.0);
    return MBoundingBox(corner1, corner2);
}

void MeshController::points(MPointArray &points) const{
    points.setLength(sCurvePointCount);
    for (unsigned i = 0; i < sCurvePointCount; i ++){
        points.set(basicCurvePoints[i], i);
    }
}


MeshControllerUI::MeshControllerUI() {}

MeshControllerUI::~MeshControllerUI() {}

void *MeshControllerUI::creator(){
    // Maya creator function.
	return new MeshControllerUI();
}

void MeshControllerUI::getDrawRequests(const MDrawInfo &info, bool objectAndActiveOnly,
                                       MDrawRequestQueue &requests){
    /*
    Add draw requests to the draw queue.
        * info [MDrawInfo] is the current drawing state.
        * objectAndActiveOnly [bool]
    */
}