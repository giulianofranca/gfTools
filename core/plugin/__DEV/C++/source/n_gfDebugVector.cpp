#include "n_gfDebugVector.h"

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
DebugVector::DebugVector() {}

// Destructor.
DebugVector::~DebugVector() {}

MObject DebugVector::inLineWidth;
MObject DebugVector::inColor;
MObject DebugVector::inRadius;
MObject DebugVector::inTipSize;
MObject DebugVector::inSubdivisions;
MObject DebugVector::inXRay;
MObject DebugVector::inOperation;
MObject DebugVector::inVec1;
MObject DebugVector::inVec2;
MObject DebugVector::inNormalize;
MObject DebugVector::outVector;
const MColor DebugVector::kActiveColor = MColor(0.3f, 1.0f, 1.0f);
const MColor DebugVector::kLeadColor = MColor(1.0f, 1.0f, 1.0f);

void DebugVector::postConstructor(){
    // Post Constructor.
    MObject thisMob = thisMObject();
    MFnDependencyNode(thisMob).setName("gfDebugVectorShape#");
}


void* DebugVector::creator(){
    // Maya creator function.
    return new DebugVector();
}

MStatus DebugVector::initialize(){
    /*
    Defines the set of attributes for this node. The attributes declared in this function are assigned
    as static members to DebugVector class. Instances of DebugVector will use these attributes to create plugs
    for use in the compute() method.
    */
    MStatus status;
    MFnNumericAttribute nAttr;
    MFnEnumAttribute eAttr;

    inLineWidth = nAttr.create("lineWidth", "lw", MFnNumericData::kFloat, 3.0f, &status);
    nAttr.setMin(1.0f);
    nAttr.setSoftMax(5.0f);
    INPUT_ATTR(nAttr);

    inColor = nAttr.createColor("color", "color", &status);
    nAttr.setDefault(1.0, 1.0, 0.0);
    INPUT_ATTR(nAttr);

    inTipSize = nAttr.create("tipSize", "tipSize", MFnNumericData::kFloat, 0.1f, &status);
    nAttr.setMin(0.1f);
    nAttr.setMax(1.0f);
    INPUT_ATTR(nAttr);

    inSubdivisions = nAttr.create("subdivisions", "subd", MFnNumericData::kInt, 4, &status);
    nAttr.setMin(2);
    nAttr.setMax(12);
    INPUT_ATTR(nAttr);

    inRadius = nAttr.create("radius", "radius", MFnNumericData::kFloat, 1.0f, &status);
    nAttr.setMin(0.0f);
    nAttr.setSoftMax(5.0f);
    INPUT_ATTR(nAttr);

    inXRay = nAttr.create("XRay", "XRay", MFnNumericData::kBoolean, false, &status);
    INPUT_ATTR(nAttr);

    inOperation = eAttr.create("operation", "op", 0, &status);
    eAttr.addField("No Operation", 0);
    eAttr.addField("Add", 1);
    eAttr.addField("Subtract", 2);
    eAttr.addField("Cross Product", 3);
    INPUT_ATTR(eAttr);

    inVec1 = nAttr.createPoint("vector1", "v1", &status);
    INPUT_ATTR(nAttr);

    inVec2 = nAttr.createPoint("vector2", "v2", &status);
    INPUT_ATTR(nAttr);

    inNormalize = nAttr.create("normalizeOutput", "no", MFnNumericData::kBoolean, false, &status);
    INPUT_ATTR(nAttr);

    outVector = nAttr.createPoint("outVector", "ov", &status);
    OUTPUT_ATTR(nAttr);

    addAttribute(inLineWidth);
    addAttribute(inColor);
    addAttribute(inTipSize);
    addAttribute(inSubdivisions);
    addAttribute(inRadius);
    addAttribute(inXRay);
    addAttribute(inOperation);
    addAttribute(inVec1);
    addAttribute(inVec2);
    addAttribute(inNormalize);
    addAttribute(outVector);
    attributeAffects(inOperation, outVector);
    attributeAffects(inVec1, outVector);
    attributeAffects(inVec2, outVector);
    attributeAffects(inNormalize, outVector);

    return status;
}

void DebugVector::drawArrow(MFloatVector& startPnt, MFloatVector& endPnt, float size,
                            float radius, int subd, float lineW){
    // Drawing arrow in viewport 1.0
    float tipSize = 1.0f - size;
    double step = 2.0 * M_PI / subd;
    MFloatVector vAim = endPnt - startPnt;
    MFloatVector vBaseOrigin = vAim * tipSize;
    MFloatVector nAim = vAim.normal();
    MFloatVector nWorld(0.0f, 1.0f, 0.0f);
    MFloatVector nBinormal = nWorld ^ nAim;
    nBinormal.normalize();
    MFloatVector nNormal = nAim ^ nBinormal;
    nNormal.normalize();
    double aim[4][4] = {
        nAim.x, nAim.y, nAim.z, 0.0,
        nNormal.x, nNormal.y, nNormal.z, 0.0,
        nBinormal.y, nBinormal.y, nBinormal.z, 0.0,
        startPnt.x, startPnt.y, startPnt.z, 1.0
    };
    MMatrix mBase = MMatrix(aim);
    MMatrix mOrigin = MMatrix();
    mOrigin[3][0] = vBaseOrigin.length();
    MMatrix mBaseOrigin = mOrigin * mBase;
    glLineWidth(lineW);
    glBegin(GL_LINES);
    glVertex3f(startPnt.x, startPnt.y, startPnt.z);
    glVertex3f(endPnt.x, endPnt.y, endPnt.z);
    glEnd();
    for (int i = 0; i < subd; i++){
        double theta = step * i;
        MMatrix mPoint = MMatrix();
        mPoint[3][1] = std::cos(theta) * radius;
        mPoint[3][2] = std::sin(theta) * radius;
        MMatrix mArrow = mPoint * mBaseOrigin;
        glBegin(GL_LINES);
        glVertex3d(mBaseOrigin[3][0], mBaseOrigin[3][1], mBaseOrigin[3][2]);
        glVertex3d(mArrow[3][0], mArrow[3][1], mArrow[3][2]);
        glVertex3d(mArrow[3][0], mArrow[3][1], mArrow[3][2]);
        glVertex3f(endPnt.x, endPnt.y, endPnt.z);
        glEnd();
    }
}

void DebugVector::drawArrow(MFloatVector& startPnt, MFloatVector& endPnt, float size, 
                            float radius, int subd, MPointArray& lineList){
    // Drawing arrow in viewport 2.0
    float tipSize = 1.0f - size;
    double step = 2.0 * M_PI / subd;
    MFloatVector vAim = endPnt - startPnt;
    MFloatVector vBaseOrigin = vAim * tipSize;
    MFloatVector nAim = vAim.normal();
    MFloatVector nWorld(0.0f, 1.0f, 0.0f);
    MFloatVector nBinormal = nWorld ^ nAim;
    nBinormal.normalize();
    MFloatVector nNormal = nAim ^ nBinormal;
    nNormal.normalize();
    double aim[4][4] = {
        nAim.x, nAim.y, nAim.z, 0.0,
        nNormal.x, nNormal.y, nNormal.z, 0.0,
        nBinormal.y, nBinormal.y, nBinormal.z, 0.0,
        startPnt.x, startPnt.y, startPnt.z, 1.0
    };
    MMatrix mBase = MMatrix(aim);
    MMatrix mOrigin = MMatrix();
    mOrigin[3][0] = vBaseOrigin.length();
    MMatrix mBaseOrigin = mOrigin * mBase;
    lineList.append(MPoint(startPnt));
    lineList.append(MPoint(endPnt));
    for (int i = 0; i < subd; i++){
        double theta = step * i;
        MMatrix mPoint = MMatrix();
        mPoint[3][1] = std::cos(theta) * radius;
        mPoint[3][2] = std::sin(theta) * radius;
        MMatrix mArrow = mPoint * mBaseOrigin;
        lineList.append(MPoint(mBaseOrigin[3][0], mBaseOrigin[3][1], mBaseOrigin[3][2]));
        lineList.append(MPoint(mArrow[3][0], mArrow[3][1], mArrow[3][2]));
        lineList.append(MPoint(mArrow[3][0], mArrow[3][1], mArrow[3][2]));
        lineList.append(MPoint(endPnt));
    }
}

MStatus DebugVector::compute(const MPlug& plug, MDataBlock& dataBlock){
    /*
    Node computation method:
        * plug is a connection point related to one of our node attributes (either an input or an output).
        * dataBlock contains the data on which we will base our computations.
    */
    if (plug != outVector)
        return MStatus::kUnknownParameter;

    short operation = dataBlock.inputValue(inOperation).asShort();
    MFloatVector vVector1 = dataBlock.inputValue(inVec1).asFloatVector();
    MFloatVector vVector2 = dataBlock.inputValue(inVec2).asFloatVector();
    bool normalize = dataBlock.inputValue(inNormalize).asBool();

    MFloatVector vStart, vEnd, vFinal;
    switch (operation)
    {
    case 0:
        vEnd = vVector1;
        break;
    case 1:
        vFinal = vVector1 + vVector2;
        vEnd = vFinal;
        break;
    case 2:
        vFinal = vVector1 - vVector2;
        vEnd = vFinal;
        break;
    case 3:
        vFinal = vVector1 ^ vVector2;
        vEnd = vFinal;
        break;
    }

    vStart = MFloatVector();
    if (normalize)
        vEnd.normalize();

    MDataHandle outVectorHandle = dataBlock.outputValue(outVector);
    outVectorHandle.setMFloatVector(vEnd);
    outVectorHandle.setClean();

    return MStatus::kSuccess;
}

void DebugVector::draw(M3dView& view, const MDagPath& path, M3dView::DisplayStyle style,
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
    MObject thisMob = thisMObject();
    float lineW = MPlug(thisMob, inLineWidth).asFloat();
    MFloatVector color = MPlug(thisMob, inColor).asMDataHandle().asFloatVector();
    float tipSize = MPlug(thisMob, inTipSize).asFloat();
    int subd = MPlug(thisMob, inSubdivisions).asInt();
    float radius = MPlug(thisMob, inRadius).asFloat();
    bool xray = MPlug(thisMob, inXRay).asBool();

    short operation = MPlug(thisMob, inOperation).asShort();
    MFloatVector vVector1 = MPlug(thisMob, inVec1).asMDataHandle().asFloatVector();
    MFloatVector vVector2 = MPlug(thisMob, inVec2).asMDataHandle().asFloatVector();
    bool normalize = MPlug(thisMob, inNormalize).asBool();

    MFloatVector vStart, vEnd, vFinal;
    switch (operation)
    {
    case 0:
        vEnd = vVector1;
        break;
    case 1:
        vFinal = vVector1 + vVector2;
        vEnd = vFinal;
        break;
    case 2:
        vFinal = vVector1 - vVector2;
        vEnd = vFinal;
        break;
    case 3:
        vFinal = vVector1 ^ vVector2;
        vEnd = vFinal;
        break;
    }

    vStart = MFloatVector();
    if (normalize)
        vEnd.normalize();

    view.beginGL();

    glPushAttrib(GL_CURRENT_BIT);
    glDisable(GL_CULL_FACE);
    if (xray){
        glEnable(GL_DEPTH_TEST);
        glClear(GL_DEPTH_BUFFER_BIT);
    }

    if (status == M3dView::kActive)
        glColor3f(kActiveColor.r, kActiveColor.g, kActiveColor.b);
    else if (status == M3dView::kLead)
        glColor3f(kLeadColor.r, kLeadColor.g, kLeadColor.b);
    else if (status == M3dView::kDormant)
        glColor3f(color.x, color.y, color.z);

    DebugVector::drawArrow(vStart, vEnd, tipSize, radius, subd, lineW);

    if (xray)
        glDisable(GL_DEPTH_TEST);
    glPopAttrib();
    glLineWidth(1.0f);

    view.endGL();
}
//---------------------------------------------------------------------------------
//---------------------------------------------------------------------------------
//----------   Viewport 2.0 Implementation   --------------------------------------
//---------------------------------------------------------------------------------
//---------------------------------------------------------------------------------

DebugVectorDrawOverride::DebugVectorDrawOverride(const MObject& obj)
                       : MHWRender::MPxDrawOverride(obj, NULL, false)
                       , fDebugVector(obj){
    mCurrentBoundingBox = MBoundingBox();
    fModelEditorChangedCbId = MEventMessage::addEventCallback(
        "modelEditorChanged", OnModelEditorChanged, this);

    MGlobal::displayInfo("Constructed!");
}

DebugVectorDrawOverride::~DebugVectorDrawOverride() {
    if (fModelEditorChangedCbId != 0){
        MMessage::removeCallback(fModelEditorChangedCbId);
        fModelEditorChangedCbId = 0;
    }
}

void DebugVectorDrawOverride::OnModelEditorChanged(void* clientData){
    // Mark the node as being dirty so that it can update on display appearance
    // switch among wireframe and shaded.
    DebugVectorDrawOverride *ovr = static_cast<DebugVectorDrawOverride*>(clientData);
    if (ovr)
        MHWRender::MRenderer::setGeometryDrawDirty(ovr->fDebugVector);
}

MHWRender::MPxDrawOverride* DebugVectorDrawOverride::creator(const MObject& obj){
    // MPxDrawOverride creator function.
    return new DebugVectorDrawOverride(obj);
}

bool DebugVectorDrawOverride::isBounded(const MDagPath& objPath, 
                                        const MDagPath& cameraPath){
    // isBounded?
    return true;
}

MBoundingBox DebugVectorDrawOverride::boundingBox(const MDagPath& objPath,
                                                  const MDagPath& cameraPath){
    // Return the bounding box
    MObject node = objPath.node();
    short operation = MPlug(node, DebugVector::inOperation).asShort();
    MFloatVector vVector1 = MPlug(node, DebugVector::inVec1).asMDataHandle().asFloatVector();
    MFloatVector vVector2 = MPlug(node, DebugVector::inVec2).asMDataHandle().asFloatVector();
    bool normalize = MPlug(node, DebugVector::inNormalize).asBool();

    MFloatVector vStart, vEnd, vFinal;
    switch (operation)
    {
    case 0:
        vEnd = vVector1;
        break;
    case 1:
        vFinal = vVector1 + vVector2;
        vEnd = vFinal;
        break;
    case 2:
        vFinal = vVector1 - vVector2;
        vEnd = vFinal;
        break;
    case 3:
        vFinal = vVector1 ^ vVector2;
        vEnd = vFinal;
        break;
    }

    vStart = MFloatVector();
    if (normalize)
        vEnd.normalize();

    MPoint corner1 = MPoint(vStart.x, vStart.y, vStart.z);
    MPoint corner2 = MPoint(vEnd.x, vEnd.y, vEnd.z);
    this->mCurrentBoundingBox.clear();                // this->
    this->mCurrentBoundingBox.expand(corner1);
    this->mCurrentBoundingBox.expand(corner2);

    return this->mCurrentBoundingBox;
}

MUserData* DebugVectorDrawOverride::prepareForDraw(const MDagPath& objPath, 
                                                   const MDagPath& cameraPath,
                                                   const MHWRender::MFrameContext& frameContext,
                                                   MUserData* oldData){
    /*
    Called by Maya each time the object needs to be drawn.
    Any data needed from the Maya dependency graph must be retrieved and cached in this stage.
    Returns the data to be passed to the draw callback method.
        * objPath [MDagPath] is the path to the object being drawn.
        * cameraPath [MDagPath] is the path to the camera that is being used to draw.
        * frameContext [MFrameContext] is the frame level context information.
        * oldData [MUserData] is the data cached by the previous draw of the instance.
    */
    MGlobal::displayInfo("Getting ready to draw some cool stuff");
    DebugVectorData* data = dynamic_cast<DebugVectorData*>(oldData);
    if (!data)
        data = new DebugVectorData();

    MObject node = objPath.node();
    float lineW = MPlug(node, DebugVector::inLineWidth).asFloat();
    MFloatVector color = MPlug(node, DebugVector::inColor).asMDataHandle().asFloatVector();
    float tipSize = MPlug(node, DebugVector::inTipSize).asFloat();
    int subd = MPlug(node, DebugVector::inSubdivisions).asInt();
    float radius = MPlug(node, DebugVector::inRadius).asFloat();
    bool xray = MPlug(node, DebugVector::inXRay).asBool();
    short operation = MPlug(node, DebugVector::inOperation).asShort();
    MFloatVector vVector1 = MPlug(node, DebugVector::inVec1).asMDataHandle().asFloatVector();
    MFloatVector vVector2 = MPlug(node, DebugVector::inVec2).asMDataHandle().asFloatVector();
    bool normalize = MPlug(node, DebugVector::inNormalize).asBool();

    data->fDormantColor = MColor(color.x, color.y, color.z);
    data->fActiveColor = DebugVector::kActiveColor;
    data->fLeadColor = DebugVector::kLeadColor;
    data->fLineWidth = lineW;
    data->fTipSize = tipSize;
    data->fSubd = subd;
    data->fRadius = radius;
    data->fXray = xray;
    data->fOperation = operation;

    MFloatVector vStart, vEnd, vFinal;
    switch (operation)
    {
    case 0:
        vEnd = vVector1;
        break;
    case 1:
        vFinal = vVector1 + vVector2;
        vEnd = vFinal;
        break;
    case 2:
        vFinal = vVector1 - vVector2;
        vEnd = vFinal;
        break;
    case 3:
        vFinal = vVector1 ^ vVector2;
        vEnd = vFinal;
        break;
    }

    vStart = MFloatVector();
    if (normalize)
        vEnd.normalize();

    data->fLineList.clear();
    DebugVector::drawArrow(vStart, vEnd, tipSize, radius, subd, data->fLineList);

    MGlobal::displayInfo("Draw prepared! Draw some shit right here dude!");

    return data;
}

void DebugVectorDrawOverride::addUIDrawables(const MDagPath& objPath,
                                             MHWRender::MUIDrawManager& drawManager,
                                             const MHWRender::MFrameContext& frameContext,
                                             const MUserData* data){
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
    DebugVectorData* locatorData = (DebugVectorData*)data;
    if (!locatorData)
        MGlobal::displayInfo("Returning from addUIDrawables");
        return;

    MHWRender::DisplayStatus status = MHWRender::MGeometryUtilities::displayStatus(objPath);

    if (locatorData->fXray)
        drawManager.beginDrawInXray();
    else
        drawManager.beginDrawable();

    if (status == MHWRender::DisplayStatus::kActive)
        drawManager.setColor(locatorData->fActiveColor);
    else if (status == MHWRender::DisplayStatus::kLead)
        drawManager.setColor(locatorData->fLeadColor);
    else if (status == MHWRender::DisplayStatus::kDormant)
        drawManager.setColor(locatorData->fDormantColor);

    drawManager.setDepthPriority(5);

    drawManager.setLineWidth(locatorData->fLineWidth);
    drawManager.mesh(MHWRender::MUIDrawManager::kLines, locatorData->fLineList);

    if (locatorData->fXray)
        drawManager.endDrawInXray();
    else
        drawManager.endDrawable();

    MGlobal::displayInfo("Ending of drawing");

}