#include "headers/n_gfRigMeshController.h"

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
MeshController::MeshController() {}

// Destructor.
MeshController::~MeshController() {}

MObject MeshController::inIndexList;
MObject MeshController::inOffset;
MObject MeshController::inMesh;
MObject MeshController::inColor;
std::vector<MPointArray> MeshController::ctrlVertices;
MBoundingBox MeshController::bBox;


void MeshController::postConstructor(){
    // Post Constructor.
    MObject thisMob = thisMObject();
    MFnDependencyNode(thisMob).setName("gfMeshControllerShape#");
}

void* MeshController::creator(){
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
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;

    inIndexList = tAttr.create("indexList", "index", MFnData::kString, MObject::kNullObj, &status);
    INPUT_ATTR(tAttr);

    inOffset = nAttr.create("offset", "offset", MFnNumericData::kFloat, 0.0f, &status);
    INPUT_ATTR(nAttr);

    inMesh = tAttr.create("controlMesh", "controlMesh", MFnData::kMesh, MObject::kNullObj, &status);
    INPUT_ATTR(tAttr);

    inColor = nAttr.createColor("color", "color", &status);
    nAttr.setDefault(1.0, 0.455, 0.086);
    INPUT_ATTR(nAttr);

    addAttribute(inIndexList);
    addAttribute(inOffset);
    addAttribute(inMesh);
    addAttribute(inColor);

	return status;
}

MIntArray MeshController::listToMIntArray(MStringArray &strList){
    /* Convert a list of str to a MIntArray instance. */
    MIntArray instance = MIntArray();
    for (uint32_t i = 0; i < strList.length(); i++){
        instance.append(strList[i].asInt());
    }
    return instance;
}

void MeshController::getGeometryPoints(MObject &meshMob, MString &indexStr, float &offset,
                                       MMatrix &transform){
    /* Find the info of the geomtry who will be drawed. */

    std::vector<MPointArray> outPnts;
    float pntOffTol = 0.01f;
    float tolerance = offset + pntOffTol;
    MBoundingBox bBox;

    if (!meshMob.isNull()){
        MStringArray strList;
        indexStr.split(',', strList);
        MIntArray polyIndexList = MeshController::listToMIntArray(strList);
        MItMeshPolygon itPoly(meshMob);
        int curIndex;
        for (uint32_t i = 0; i < polyIndexList.length(); i++){
            itPoly.setIndex(polyIndexList[i], curIndex);
            MVectorArray polyVtxNormals;
            itPoly.getNormals(polyVtxNormals);
            MPointArray polyVtxPos;
            itPoly.getPoints(polyVtxPos, MSpace::kWorld);
            MPointArray outPolyVtxPos;
            for (uint32_t j = 0; j < polyVtxPos.length(); j++){
                MPoint curPnt = polyVtxPos[j];
                MVector curNormal = polyVtxNormals[j];
                MPoint outPnt = (curPnt + (curNormal * tolerance)) * transform;
                bBox.expand(outPnt);
                outPolyVtxPos.append(outPnt);
            }
            outPnts.push_back(outPolyVtxPos);
        }
    }
    MeshController::ctrlVertices = outPnts;
    MeshController::bBox = bBox;
    return;
}

MStatus MeshController::compute(const MPlug &plug, MDataBlock &dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    return MStatus::kSuccess;
}

void MeshController::draw(M3dView &view, const MDagPath &path, M3dView::DisplayStyle style,
                          M3dView::DisplayStatus status){
    /*
    Draw custom geometry in the viewport using OpenGL calls.
        * view [M3dView] is a 3D view that is being drawn into.
        * path [MDagPath] to the parent (transform node) of this locator in the DAG.  To obtain the locator shape node,
            use MDagPath::extendToShape() if there is only one shape node under the transform or
            MDagPath::extendToShapeDirectlyBelow(unsigned int index) with the shape index if there are multiple
            shapes under the transform.
        * style [M3dView.DisplayStyle] is the style to draw object in.
        * status [M3dView.DisplayStatus] is the selection status of the object.
    */
    // NO DRAWING IN VIEWPORT 1.0 JUST RETURN
    return;
}

bool MeshController::isBounded() const{
    /* isBounded? */
    return false;
}

bool MeshController::isTransparent() const{
    /* isTransparent? */
    return false;
}

MStatus MeshController::preEvaluation(const MDGContext &context,
                                      const MEvaluationNode &evaluationNode){
    /*
    Called before this node is evaluated by Evaluation Manager.
    * context [MDGContext] is the context which the evaluation is happening.
    * evaluationNode [MEvaluationNode] the evaluation node which contains information
        about the dirty plugs that are about to be evaluated for the context.
        Should be only used to query information.
    */
    if (context.isNormal()){
        MStatus status;
        if (((evaluationNode.dirtyPlugExists(inOffset, &status)) ||
             (evaluationNode.dirtyPlugExists(inIndexList, &status)) ||
             (evaluationNode.dirtyPlugExists(inMesh, &status))) && status)
            MHWRender::MRenderer::setGeometryDrawDirty(thisMObject());
    }

    return MStatus::kSuccess;
}


//////////////////////////////////////////////////////////////////////////////////////////
////////// VIEWPORT 2.0 IMPLEMENTATION
//////////////////////////////////////////////////////////////////////////////////////////

MeshControllerDrawOverride::MeshControllerDrawOverride(const MObject &obj)
: MHWRender::MPxDrawOverride(obj, NULL, false){
    fModelEditorChangedCbId = MEventMessage::addEventCallback(
        "modelEditorChanged", onModelEditorChanged, this
    );

    MStatus status;
    MFnDependencyNode node(obj, &status);
    fMeshController = status ? dynamic_cast<MeshController*>(node.userNode()) : NULL;
}

MeshControllerDrawOverride::~MeshControllerDrawOverride(){
    fMeshController = NULL;

    if (fModelEditorChangedCbId != 0){
        MMessage::removeCallback(fModelEditorChangedCbId);
        fModelEditorChangedCbId = 0;
    }
}

MHWRender::MPxDrawOverride* MeshControllerDrawOverride::creator(const MObject& obj){
    // MPxDrawOverride creator function.
    return new MeshControllerDrawOverride(obj);
}

void MeshControllerDrawOverride::onModelEditorChanged(void *clientData){
    // Mark the node as being dirty so that it can update on display appearance
    // switch among wireframe and shaded.
    MeshControllerDrawOverride *ovr = static_cast<MeshControllerDrawOverride*>(clientData);
    if (ovr && ovr->fMeshController)
        MHWRender::MRenderer::setGeometryDrawDirty(ovr->fMeshController->thisMObject());
}

MHWRender::DrawAPI MeshControllerDrawOverride::supportedDrawAPIs() const{
    // This plugin supports both GL and DX
    return (MHWRender::kOpenGL | MHWRender::kOpenGLCoreProfile | MHWRender::kDirectX11);
}

bool MeshControllerDrawOverride::isBounded(const MDagPath &objPath,
                                           const MDagPath &cameraPath) const{
    /* isBounded? */
    return true;
}

MBoundingBox MeshControllerDrawOverride::boundingBox(const MDagPath &objPath,
                                                     const MDagPath &cameraPath) const{
    /* Return the BoundingBox */
    if (MeshController::ctrlVertices.size() < 1){
        MObject thisMob = objPath.node();
        MDagPath thisPath, transformPath;
        MObject parentMob = MFnDagNode(thisPath).parent(0);
        MDagPath::getAPathTo(thisMob, thisPath);
        MDagPath::getAPathTo(parentMob, transformPath);
        MMatrix mWorldInv = transformPath.inclusiveMatrixInverse();
        MString indexStr = MPlug(thisMob, MeshController::inIndexList).asString();
        float offset = MPlug(thisMob, MeshController::inOffset).asFloat();
        MObject mesh = MPlug(thisMob, MeshController::inMesh).asMDataHandle().asMesh();
        MeshController::getGeometryPoints(mesh, indexStr, offset, mWorldInv);
    }
    return MeshController::bBox;
}

bool MeshControllerDrawOverride::isTransparent() const{
    /* isTransparent? */
    return false;
}

MUserData *MeshControllerDrawOverride::prepareForDraw(const MDagPath &objPath, 
                                                      const MDagPath &cameraPath,
                                                      const MHWRender::MFrameContext &frameContext,
                                                      MUserData *oldData){
    /*
    Called by Maya each time the object needs to be drawn.
    Any data needed from the Maya dependency graph must be retrieved and cached in this stage.
    Returns the data to be passed toe the draw callback method.
        * objPath [MDagPath] is the path to the object being drawn.
        * cameraPath [MDagPath] is the path to the camera that is being used to draw.
        * frameContext [MFrameContext] is the frame level context information.
        * oldData [MUserData] is the data cached by the previous draw of the instance.
    */
    clock_t startTime = clock();

    MeshControllerData *data = dynamic_cast<MeshControllerData*>(oldData);
    if (!data)
        data = new MeshControllerData();
    
    MObject thisMob = objPath.node();
    MDagPath transformPath;
    MObject parentMob = MFnDagNode(objPath).parent(0);
    MDagPath::getAPathTo(parentMob, transformPath);
    MMatrix mWorldInv = transformPath.inclusiveMatrixInverse();
    MString indexStr = MPlug(thisMob, MeshController::inIndexList).asString();
    float offset = MPlug(thisMob, MeshController::inOffset).asFloat();
    MObject mesh = MPlug(thisMob, MeshController::inMesh).asMDataHandle().asMesh();
    MFloatVector color = MPlug(thisMob, MeshController::inColor).asMDataHandle().asFloatVector();

    // If plug are dirty calculate the geometry points
    MeshController::getGeometryPoints(mesh, indexStr, offset, mWorldInv);

    data->fVtxPositions = MeshController::ctrlVertices;

    MHWRender::DisplayStatus status = MHWRender::MGeometryUtilities::displayStatus(objPath);
    float alpha;
    if (status == MHWRender::DisplayStatus::kDormant)
        // Not selected
        alpha = 0.25f;
    else if (status == MHWRender::DisplayStatus::kActive)
        // Multiselection
        alpha = 0.65f;
    else if (status == MHWRender::DisplayStatus::kLead)
        // Selected
        alpha = 0.5f;
    data->fColor = MColor(color.x, color.y, color.z, alpha);

    double runTime = (double)(clock() - startTime);
    {
        MString toPrint("prepareForDraw time: ");
        toPrint += runTime;
        toPrint += " ms";
        MGlobal::displayInfo(toPrint);
    }

    return data;
}

bool MeshControllerDrawOverride::hasUIDrawables() const{
    /* Has ui drawables? */
    return true;
}

void MeshControllerDrawOverride::addUIDrawables(const MDagPath &objPath,
                                                MHWRender::MUIDrawManager &drawManager,
                                                const MHWRender::MFrameContext &frameContext,
                                                const MUserData *data){
    /*
    Provides access to the MUIDrawManager, which can be used to queue up operations to draw simple UI
    shapes like lines, circles, text, etc.
    It is called after prepareForDraw() and carries the same restrictions on the sorts of operations it
    can perform.
        * objPath [MDagPath] is the path to the object being drawn.
        * drawManager [MUIDrawManager] it can be used to draw some simple geometry including text.
        * frameContext [MFrameContext] is the frame level context information.
        * data [MUserData] is the data cached by the prepareForDraw().
    */
    clock_t startTime = clock();

    MeshControllerData *locatorData = (MeshControllerData*)data;
    if (!locatorData)
        return;

    drawManager.beginDrawable(MHWRender::MUIDrawManager::Selectability::kSelectable);
    drawManager.beginDrawInXray();

    MHWRender::MUIDrawManager::Primitive mode = MHWRender::MUIDrawManager::Primitive::kTriStrip;
    MUintArray index;
    MPointArray pnts;
    // index.append(0);
    // index.append(1);
    // index.append(3);
    // index.append(2);
    for(uint32_t i = 0; i < locatorData->fVtxPositions.size(); i++){
        index.append(0 + (4 * i));
        index.append(1 + (4 * i));
        index.append(3 + (4 * i));
        index.append(2 + (4 * i));
        pnts.append(locatorData->fVtxPositions[i][0]);
        pnts.append(locatorData->fVtxPositions[i][1]);
        pnts.append(locatorData->fVtxPositions[i][2]);
        pnts.append(locatorData->fVtxPositions[i][3]);
    }

    drawManager.setColor(locatorData->fColor);

    drawManager.setDepthPriority(MHWRender::MRenderItem::sSelectionDepthPriority);
    drawManager.mesh(mode, pnts, NULL, NULL, &index);
    // for(uint32_t i = 0; i < locatorData->fVtxPositions.size(); i++){
    //     drawManager.mesh(mode, locatorData->fVtxPositions[i], NULL, NULL, &index);
    // }

    drawManager.endDrawInXray();
    drawManager.endDrawable();

    double runTime = (double)(clock() - startTime);
    {
        MString toPrint("draw time: ");
        toPrint += runTime;
        toPrint += " ms";
        MGlobal::displayInfo(toPrint);
    }
}

bool MeshControllerDrawOverride::traceCallSequence() const{
    /* Return true if internal tracing is desired. */
    return false;
}

void MeshControllerDrawOverride::handleTraceMessage(const MString &message) const{
    MGlobal::displayInfo("MeshControllerDrawOverride: " + message);

    // Some simple custom message formatting.
    fprintf(stderr, "MeshControllerDrawOverride: ");
    fprintf(stderr, message.asChar());
    fprintf(stderr, "\n");
}